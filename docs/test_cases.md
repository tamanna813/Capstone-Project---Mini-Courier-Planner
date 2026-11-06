# Test Cases

| Test | Input / action | Expected result |
|---|---|---|
| T1 | Run with supplied CSV files | Program completes without error |
| T2 | Vehicle capacity = 15 kg | Selected parcel weight is <= 15 kg |
| T3 | Increase one parcel priority | It moves earlier in the priority ordering |
| T4 | Add a shorter graph edge | Dijkstra may update the corresponding shortest path |
| T5 | Selected destinations exist in graph | Route includes all selected destinations once and returns to Warehouse |
| T6 | Run benchmarks | JSON results and runtime chart are produced |

Note: if you edit sample data, ensure every parcel destination is represented as a graph vertex.
