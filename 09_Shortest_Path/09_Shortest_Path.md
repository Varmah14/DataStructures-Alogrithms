# Shortest Path Algorithms — Complete Guide

## 1. Algorithm Selection

| Algorithm | Weights | Negative? | Time | Use When |
|---|---|---|---|---|
| BFS | All = 1 | N/A | O(V+E) | Unweighted graph |
| 0-1 BFS | 0 or 1 | No | O(V+E) | Binary weights |
| Dijkstra | Non-negative | No | O((V+E)logV) | General non-negative |
| Bellman-Ford | Any | Yes | O(VE) | Negative edges, k-stop limit |
| Floyd-Warshall | Any | Yes | O(V³) | All-pairs, small V |
| DAG relaxation | Any | Yes (DAG) | O(V+E) | DAG only |

---

## 2. Dijkstra (Most Common in Interviews)

```python
import heapq

def dijkstra(graph, src, n):
    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale — lazy deletion
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```

### With Path Reconstruction
```python
def dijkstra_path(graph, src, dst, n):
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    path = []
    node = dst
    while node != -1:
        path.append(node)
        node = prev[node]
    return path[::-1], dist[dst]
```

### On Grid
```python
def dijkstra_grid(grid, sr, sc, er, ec):
    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[sr][sc] = grid[sr][sc]
    heap = [(grid[sr][sc], sr, sc)]
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > dist[r][c]:
            continue
        if r == er and c == ec:
            return d
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nd = dist[r][c] + grid[nr][nc]
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return dist[er][ec]
```

### Min-Max Path (Bottleneck)
```python
def min_bottleneck(graph, src, dst, n):
    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        for v, w in graph[u]:
            cost = max(d, w)  # bottleneck = max edge on path
            if cost < dist[v]:
                dist[v] = cost
                heapq.heappush(heap, (cost, v))
    return dist[dst]
```

### Why Dijkstra Fails with Negative Weights
A→B (weight 1), A→C (weight 5), C→B (weight -10). Dijkstra finalizes B with dist=1 via A→B. Misses A→C→B with dist=-5. Greedy assumption breaks.

---

## 3. 0-1 BFS

```python
from collections import deque

def bfs_01(graph, src, n):
    dist = [float('inf')] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)  # free edge → front
                else:
                    dq.append(v)      # cost-1 edge → back
    return dist
```
O(V+E) — no heap overhead. Use when weights are binary.

---

## 4. Bellman-Ford

```python
def bellman_ford(n, edges, src):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Negative cycle detection
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # negative cycle
    return dist
```

### K-Stop Limited (LC 787)
```python
def cheapest_k_stops(n, flights, src, dst, k):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(k + 1):
        new_dist = dist[:]  # MUST copy — can't use current round's updates
        for u, v, w in flights:
            if dist[u] != float('inf') and dist[u] + w < new_dist[v]:
                new_dist[v] = dist[u] + w
        dist = new_dist
    return dist[dst] if dist[dst] != float('inf') else -1
```

---

## 5. Floyd-Warshall

```python
def floyd_warshall(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w
    
    for k in range(n):         # k MUST be outermost
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

---

## 6. LeetCode Problems

### Dijkstra
| # | Problem | Key Concept |
|---|---------|-------------|
| 743 | Network Delay Time | Textbook Dijkstra |
| 1631 | Path With Minimum Effort | Min-max on grid |
| 778 | Swim in Rising Water | Min-max on grid |
| 1514 | Path with Maximum Probability | Max-product Dijkstra |

### BFS / 0-1 BFS
| # | Problem | Key Concept |
|---|---------|-------------|
| 1091 | Shortest Path in Binary Matrix | Grid BFS |
| 1368 | Min Cost Valid Path in Grid | 0-1 BFS |
| 2290 | Min Obstacle Removal | 0-1 BFS on grid |

### Bellman-Ford / Floyd-Warshall
| # | Problem | Key Concept |
|---|---------|-------------|
| 787 | Cheapest Flights Within K Stops | BF with k iterations |
| 1334 | Find City With Smallest Neighbors | Floyd-Warshall |

### Study Order
**Phase 1 (2-3 days):** 743, 1091, 787
**Phase 2 (2-3 days):** 1631, 778, 1368
**Phase 3 (2-3 days):** 1514, 2290, 1334
