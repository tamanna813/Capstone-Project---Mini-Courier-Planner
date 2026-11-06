# Mini-Courier Planner (B.Tech Capstone)

## Overview
A modular Python prototype that prioritizes parcels, selects the most valuable feasible set for a delivery trip, calculates shortest paths, creates an approximate delivery tour, and benchmarks key algorithms.

## Algorithms
1. **Sorting:** Python's Timsort sorts by priority (descending), then deadline (ascending), then parcel ID. Complexity: `O(n log n)`.
2. **0/1 Knapsack (Dynamic Programming):** maximizes total parcel value subject to a weight capacity. Complexity: `O(nW)` time and `O(nW)` space, where `n` is parcel count and `W` is capacity.
3. **Dijkstra:** calculates shortest paths on a non-negative weighted undirected graph using a heap. Complexity: `O((V+E) log V)` per source.
4. **Nearest-Neighbour TSP approximation:** repeatedly visits the closest unvisited destination and returns to the warehouse. The heuristic is fast but does not guarantee the optimal TSP tour.

## Project structure
```text
mini_courier_planner/
├── src/main.py
├── datasets/parcels.csv
├── datasets/routes.csv
├── images/runtime_comparison.png
├── docs/project_report.md
├── outputs/runtime_results.json
├── mini_courier_planner.ipynb
├── requirements.txt
└── .gitignore
```

## Requirements
- Python 3.9+
- No third-party packages are required to run the planner.
- `matplotlib` is only needed to regenerate the runtime chart.

Install optional chart dependency:
```bash
python -m pip install -r requirements.txt
```

## Run
From the project root:
```bash
python src/main.py
```
The program prints parcel order, selected parcels, total load/value, shortest distances, approximate route, and benchmark timings. Benchmark data is written to `outputs/runtime_results.json`.

## Sample data assumptions
- Parcel weight is measured in kg; value is a project scoring value (not currency).
- Priority is an integer where larger means more urgent.
- Deadline is an integer day index where smaller means earlier.
- Route distances are non-negative kilometres.
- The road graph is undirected.
- The box capacity in the demo is 15 kg.
- Each customer destination is visited once in the route tour, even if multiple selected parcels share that destination.

## Testing
The demonstration uses the included sample CSV files. For additional tests, change the rows in `datasets/parcels.csv` and `datasets/routes.csv`. Every parcel destination must exist in the route graph.

## Limitations and future scope
- Nearest-Neighbour TSP is an approximation and can return a longer route than the optimum.
- The knapsack objective maximizes parcel value; priority is used to order parcels, not as the knapsack objective.
- The current model assumes one vehicle, one trip, fixed parcel weights, static distances, and an undirected graph.
- Future work: traffic-aware time-dependent edges, multiple vehicles, delivery time windows, priority-weighted knapsack value, route visualization, and exact/stronger TSP heuristics.

## GitHub submission
Create a **private** repository, upload this folder, then tag the final commit:
```bash
git tag v1.0-final-submission
git push origin v1.0-final-submission
```
Submit the repository URL through LMS/Zosima.
