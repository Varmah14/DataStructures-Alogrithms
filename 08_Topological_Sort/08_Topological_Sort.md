# Topological Sort — Complete Guide

## 1. What Is It?

A **topological ordering** of a directed acyclic graph (DAG) is a linear ordering of vertices such that for every directed edge (u → v), u appears before v.

**Exists iff the graph is a DAG** (no directed cycles). If cycles exist, topological sort is impossible — this is how you detect cycles in directed graphs via BFS.

---

## 2. Two Approaches

### Kahn's Algorithm (BFS / Indegree)
```python
from collections import deque, defaultdict

def topo_sort_kahn(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    queue = deque([i for i in range(n) if indegree[i] == 0])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) == n:
        return order  # valid topological order
    return []  # cycle exists
```

**Why it works:** Nodes with indegree 0 have no unprocessed prerequisites. Process them, reduce indegrees of neighbors, repeat.

### DFS-Based (Post-Order Reverse)
```python
def topo_sort_dfs(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    visited = [0] * n  # 0=unvisited, 1=in-stack, 2=done
    order = []
    has_cycle = False
    
    def dfs(node):
        nonlocal has_cycle
        if has_cycle:
            return
        visited[node] = 1
        for neighbor in graph[node]:
            if visited[neighbor] == 1:
                has_cycle = True
                return
            if visited[neighbor] == 0:
                dfs(neighbor)
        visited[node] = 2
        order.append(node)  # post-order
    
    for i in range(n):
        if visited[i] == 0:
            dfs(i)
    
    if has_cycle:
        return []
    return order[::-1]  # reverse post-order = topological order
```

### When to Use Which

| | Kahn's (BFS) | DFS |
|---|---|---|
| Cycle detection | len(order) < n | Back edge (gray → gray) |
| Lexicographically smallest | Use min-heap instead of queue | Harder to control |
| DP on DAG | Natural — process in topo order | Use post-order directly |
| Implementation | Slightly more code | More natural recursion |

---

## 3. Key Patterns

### Pattern A: Course Schedule (Cycle Detection)
```python
def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return count == num_courses
```

### Pattern B: Course Schedule II (Return Order)
Same as above, but return the `order` list instead of checking `count == n`.

### Pattern C: DP on DAG (Longest Path)
Process nodes in topological order. For each node, update its neighbors.
```python
def longest_path_dag(n, edges, weights):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    dist = [0] * n  # or [-inf] if looking for longest from specific source
    queue = deque([i for i in range(n) if indegree[i] == 0])
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            dist[neighbor] = max(dist[neighbor], dist[node] + weights[(node, neighbor)])
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(dist)
```

### Pattern D: Parallel Job Scheduling (Critical Path)
Find minimum time to complete all tasks with dependencies.
```python
def min_completion_time(n, edges, durations):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    earliest = [0] * n
    queue = deque()
    for i in range(n):
        if indegree[i] == 0:
            earliest[i] = durations[i]
            queue.append(i)
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            earliest[neighbor] = max(earliest[neighbor], earliest[node] + durations[neighbor])
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return max(earliest)
```

### Pattern E: Lexicographically Smallest Topological Order
Replace `deque` with a min-heap.
```python
import heapq

def smallest_topo_order(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
    heap = [i for i in range(n) if indegree[i] == 0]
    heapq.heapify(heap)
    order = []
    
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
    
    return order
```

### Pattern F: Alien Dictionary
Build a graph from character ordering constraints, then topological sort.
```python
def alien_order(words):
    graph = defaultdict(set)
    indegree = {c: 0 for word in words for c in word}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""  # invalid: "abc" before "ab"
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    indegree[w2[j]] += 1
                break
    
    queue = deque([c for c in indegree if indegree[c] == 0])
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in graph[c]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) < len(indegree):
        return ""  # cycle
    return ''.join(order)
```

---

## 4. Properties & Theory

- **Number of topological orderings** can be exponential. But finding one is O(V + E).
- **DAG has at least one node with indegree 0** (otherwise there's a cycle by pigeonhole).
- **Longest path in DAG** is solvable in O(V + E) via DP on topo order. In general graphs, longest path is NP-hard.
- **Shortest path in DAG** is also O(V + E) — process in topo order, relax edges. Handles negative weights too (unlike Dijkstra).
- **All topological sorts:** Can be generated via backtracking, but usually not asked.

---

## 5. Edge Cases

- **Disconnected graph:** Kahn's handles this naturally (multiple sources).
- **Self-loops:** Indegree of self-loop node is always > 0 → cycle detected.
- **Multiple valid orderings:** Problem may ask for lexicographically smallest (use heap).
- **Node labels are strings, not ints:** Use dict-based indegree/graph instead of arrays.

---

## 6. LeetCode Problems

### Core Topological Sort
| # | Problem | Key Concept |
|---|---------|-------------|
| 207 | Course Schedule | Cycle detection via topo sort |
| 210 | Course Schedule II | Return valid topo ordering |
| 269 | Alien Dictionary | Build graph from word ordering |
| 310 | Minimum Height Trees | Peel leaves inward (reverse topo-like) |
| 1136 | Parallel Courses | Longest path in DAG = min semesters |

### DP on DAG
| # | Problem | Key Concept |
|---|---------|-------------|
| 329 | Longest Increasing Path in a Matrix | DFS + memo (implicit DAG) |
| 1857 | Largest Color Value in Directed Graph | Topo sort + DP tracking max freq per color |
| 2050 | Parallel Courses III | Critical path — max earliest completion |

### Advanced
| # | Problem | Key Concept |
|---|---------|-------------|
| 802 | Find Eventual Safe States | Reverse graph topo sort |
| 1203 | Sort Items by Groups Respecting Dependencies | Two-level topo sort |
| 2115 | Find All Possible Recipes | Topo sort with item dependencies |

### Study Order
**Phase 1 (2-3 days):** 207, 210, 269
**Phase 2 (2-3 days):** 310, 329, 1136
**Phase 3 (2-3 days):** 802, 2050, 1857
