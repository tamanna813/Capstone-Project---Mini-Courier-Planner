"""
Mini-Courier Planner
Integrates parcel sorting, 0/1 knapsack, Dijkstra shortest paths,
Nearest-Neighbour TSP approximation, and runtime benchmarking.
Run: python main.py
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import csv
import heapq
import time
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

@dataclass
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    value: int
    priority: int
    deadline: int

def load_parcels(path: Path) -> List[Parcel]:
    parcels = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parcels.append(Parcel(row["parcel_id"], row["destination"],
                                  int(row["weight"]), int(row["value"]),
                                  int(row["priority"]), int(row["deadline"])))
    return parcels

def load_graph(path: Path) -> Dict[str, Dict[str, int]]:
    graph: Dict[str, Dict[str, int]] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            a, b, w = row["from"], row["to"], int(row["distance"])
            graph.setdefault(a, {})[b] = w
            graph.setdefault(b, {})[a] = w
    return graph

def prioritize_parcels(parcels: List[Parcel]) -> List[Parcel]:
    """Higher priority first, then earliest deadline, then parcel ID."""
    return sorted(parcels, key=lambda p: (-p.priority, p.deadline, p.parcel_id))

def knapsack_select(parcels: List[Parcel], capacity: int):
    """0/1 knapsack DP. Returns selected parcels, total weight and total value."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, parcel in enumerate(parcels, start=1):
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i-1][cap]
            if parcel.weight <= cap:
                dp[i][cap] = max(dp[i][cap],
                                 parcel.value + dp[i-1][cap-parcel.weight])
    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i-1][cap]:
            parcel = parcels[i-1]
            selected.append(parcel)
            cap -= parcel.weight
    selected.reverse()
    return selected, sum(p.weight for p in selected), sum(p.value for p in selected)

def dijkstra(graph: Dict[str, Dict[str, int]], source: str):
    """Single-source shortest paths using a min-priority queue."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        current_distance, node = heapq.heappop(queue)
        if current_distance != distances[node]:
            continue
        for neighbour, weight in graph[node].items():
            candidate = current_distance + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                previous[neighbour] = node
                heapq.heappush(queue, (candidate, neighbour))
    return distances, previous

def reconstruct_path(previous, destination):
    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    return list(reversed(path))

def all_pairs_shortest_paths(graph):
    return {node: dijkstra(graph, node)[0] for node in graph}

def nearest_neighbour_tsp(distances, start, destinations):
    """Approximate route: repeatedly visit the closest unvisited destination."""
    unvisited = set(destinations) - {start}
    route = [start]
    total = 0
    current = start
    while unvisited:
        nxt = min(unvisited, key=lambda node: (distances[current][node], node))
        total += distances[current][nxt]
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    if current != start:
        total += distances[current][start]
        route.append(start)
    return route, total

def run_benchmarks():
    """Measure sorting and DP with increasing input sizes (illustrative local runs)."""
    import random
    rng = random.Random(7)
    rows = []
    for n in [10, 25, 50, 100, 200]:
        parcels = [Parcel(str(i), "A", rng.randint(1, 10), rng.randint(10, 100),
                          rng.randint(1, 5), rng.randint(1, 30)) for i in range(n)]
        t0 = time.perf_counter()
        prioritize_parcels(parcels)
        sort_ms = (time.perf_counter() - t0) * 1000
        capacity = 100
        t0 = time.perf_counter()
        knapsack_select(parcels, capacity)
        dp_ms = (time.perf_counter() - t0) * 1000
        rows.append({"input_size": n, "sorting_ms": sort_ms, "knapsack_ms": dp_ms})
    return rows

def main():
    parcels = load_parcels(ROOT / "datasets" / "parcels.csv")
    graph = load_graph(ROOT / "datasets" / "routes.csv")
    ordered = prioritize_parcels(parcels)
    capacity = 15
    selected, weight, value = knapsack_select(ordered, capacity)

    print("\\n========== MINI-COURIER PLANNER ==========")
    print("\\n1. PARCEL PRIORITIZATION")
    for p in ordered:
        print(f"{p.parcel_id}: destination={p.destination}, priority={p.priority}, "
              f"deadline={p.deadline}, weight={p.weight}, value={p.value}")
    print("\\n2. OPTIMAL BOX FILLING (0/1 KNAPSACK)")
    print(f"Capacity: {capacity} kg")
    print("Selected:", ", ".join(p.parcel_id for p in selected))
    print(f"Total weight: {weight} kg | Total value: {value}")

    destinations = sorted({p.destination for p in selected})
    start = "Warehouse"
    shortest = all_pairs_shortest_paths(graph)
    print("\\n3. DIJKSTRA SHORTEST DISTANCES FROM WAREHOUSE")
    for dest in destinations:
        print(f"{dest}: {shortest[start][dest]} km")

    route, distance = nearest_neighbour_tsp(shortest, start, destinations)
    print("\\n4. NEAREST-NEIGHBOUR DELIVERY TOUR")
    print(" -> ".join(route))
    print(f"Approximate round-trip distance: {distance} km")

    print("\\n5. RUNTIME BENCHMARK")
    results = run_benchmarks()
    for row in results:
        print(row)
    (ROOT / "outputs" / "runtime_results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print("\\nBenchmark results saved to outputs/runtime_results.json")

if __name__ == "__main__":
    main()
