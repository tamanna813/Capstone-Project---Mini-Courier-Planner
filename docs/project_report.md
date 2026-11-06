# Mini-Courier Planner — Project Report

## 1. Problem Statement
The project develops a prototype courier planner. Given parcel information and a weighted road graph, it prioritizes parcels, chooses a high-value subset that fits a vehicle capacity, computes shortest paths, and constructs an approximate delivery tour.

## 2. Objectives
- Prioritize parcels using delivery priority and deadline.
- Select parcels without exceeding the vehicle's weight capacity.
- Find shortest distances from the warehouse to customer locations.
- Produce a practical approximate tour through selected destinations.
- Measure the runtime of sorting and dynamic programming for different input sizes.

## 3. Input Data and Design
Each parcel has an ID, destination, weight, value, priority, and deadline. The road network is represented as an adjacency-list graph. Each edge has a non-negative distance in kilometres. The sample dataset contains eight parcels and six customers.

## 4. Methodology
### 4.1 Sorting
Parcels are sorted by descending priority, ascending deadline, and parcel ID. This gives a deterministic order. Python's built-in sorting uses Timsort, with `O(n log n)` worst-case time.

### 4.2 Package Selection — 0/1 Knapsack
Let `DP[i][c]` be the maximum value obtainable from the first `i` parcels with capacity `c`.
- If parcel `i` is too heavy: `DP[i][c] = DP[i-1][c]`.
- Otherwise: `DP[i][c] = max(DP[i-1][c], value[i] + DP[i-1][c-weight[i]])`.
The selected items are recovered by tracing backwards through the table. Complexity is `O(nW)` time and `O(nW)` space.

### 4.3 Shortest Paths — Dijkstra
The graph is stored as an adjacency list. A min-heap repeatedly extracts the closest unprocessed vertex and relaxes its outgoing edges. Since all distances are non-negative, Dijkstra is appropriate. Complexity per source is `O((V+E) log V)` with a binary heap.

### 4.4 Overall Route — Nearest-Neighbour TSP
Starting at the warehouse, the planner repeatedly chooses the nearest unvisited selected destination using the shortest-path distance matrix. It then returns to the warehouse. This is a heuristic approximation; it is not guaranteed to produce the globally shortest tour.

## 5. Results
Run `python src/main.py` to reproduce the console output. The program reports:
- Prioritized parcel list.
- Selected parcel IDs and total weight/value.
- Warehouse-to-customer shortest distances.
- Approximate round-trip delivery route and distance.
- Sorting and knapsack runtime measurements.

The exact timing values depend on the computer and current system load. The benchmark records are generated locally and saved as JSON; the accompanying chart is an illustrative run from this environment, not a universal performance claim.

## 6. Complexity Analysis

| Component | Time complexity | Space complexity |
|---|---|---|
| Parcel sorting | `O(n log n)` | `O(n)` for sorted output |
| 0/1 Knapsack DP | `O(nW)` | `O(nW)` |
| Dijkstra (one source) | `O((V+E) log V)` | `O(V+E)` |
| All-pairs via repeated Dijkstra | `O(V(V+E) log V)` | `O(V²)` for distance matrix |
| Nearest-Neighbour TSP | `O(k²)` | `O(k)` |

Here `n` is parcel count, `W` is capacity, `V` and `E` are graph vertices and edges, and `k` is the number of selected customer destinations.

## 7. Testing and Validation
- Capacity constraint: selected total weight must be less than or equal to 15 kg.
- Knapsack result: selected value is the maximum among subsets that fit the capacity.
- Graph test: each edge is undirected and has a non-negative distance.
- Route test: route starts and ends at Warehouse and includes every selected destination exactly once.
- Reproducibility: sample CSV datasets are included.

## 8. Limitations
The demonstration assumes one vehicle and one trip, static non-negative distances, an undirected graph, and one visit per customer. The TSP stage uses a greedy nearest-neighbour heuristic. Sorting order does not directly change the knapsack optimum because knapsack considers all parcels.

## 9. Future Scope
Introduce real map data and traffic, delivery time windows, multiple vehicles, fuel costs, priority-weighted parcel values, stronger TSP approximation methods, and interactive route visualization.

## 10. Conclusion
The Mini-Courier Planner integrates sorting, dynamic programming, graph shortest paths, and approximation algorithms into one executable Python application. It demonstrates how algorithmic techniques can be combined to solve a simplified real-world logistics problem.
