# BFS / DFS on Graphs & Grids

> **Interview Focus**: FAANG + Mid-tier | Pattern-depth over breadth

---

## What Interviewers Actually Test Here

Graph problems test whether you can **model an unfamiliar problem as a graph** and pick the right traversal. The algorithm itself is rarely the hard part — recognizing that "islands," "ladders," "clones," and "dependencies" are all just graph problems is the skill.

- Can you translate a grid into an implicit graph without building an adjacency list?
- Do you reach for BFS vs DFS for the right reasons?
- Can you detect cycles, track visited state, and handle disconnected components?

---

## Core Concepts

### Graph Representations

```python
# Adjacency List — standard for sparse graphs
graph = defaultdict(list)
graph[u].append(v)

# Implicit Graph (grids) — no need to build anything
# neighbors of (r, c): (r±1, c), (r, c±1)
directions = [(0,1),(0,-1),(1,0),(-1,0)]
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # process (nr, nc)
```

### BFS vs DFS — When to Use Which

| Situation | Use |
|---|---|
| Shortest path in **unweighted** graph | **BFS** — guarantees level-by-level expansion |
| Explore all paths / generate combinations | **DFS** |
| Connected components, flood fill | Either (DFS simpler) |
| Cycle detection (directed graph) | **DFS** with 3-color marking |
| Cycle detection (undirected graph) | DFS or DSU |
| Topological sort | **DFS** (postorder) or BFS (Kahn's) |
| Bipartite check | BFS (2-coloring) |

**Key rule**: if the problem asks for *minimum steps/distance*, reach for BFS first.

---

## The 5 Patterns

---

### Pattern 1 — BFS: Shortest Path (Unweighted)

```python
from collections import deque

def bfs(graph, start, target):
    queue = deque([(start, 0)])   # (node, distance)
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append((nei, dist + 1))
    return -1
```

**Mark visited when enqueuing, not when dequeuing** — otherwise you enqueue duplicates and lose O(V+E) guarantee.

---

### Pattern 2 — DFS: Components & Flood Fill

```python
def dfs(grid, r, c, visited):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if (r, c) in visited or grid[r][c] == '0':
        return
    visited.add((r, c))
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs(grid, r + dr, c + dc, visited)

def num_islands(grid):
    visited = set()
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(grid, r, c, visited)
                count += 1
    return count
```

**Alternative**: mutate the grid in-place (`grid[r][c] = '0'`) to avoid a visited set. Ask interviewer if mutation is allowed.

---

### Pattern 3 — Cycle Detection

**Undirected graph** — track parent to avoid trivial back-edges:

```python
def has_cycle_undirected(graph, n):
    visited = set()
    def dfs(node, parent):
        visited.add(node)
        for nei in graph[node]:
            if nei not in visited:
                if dfs(nei, node): return True
            elif nei != parent:
                return True          # back edge = cycle
        return False
    return any(dfs(i, -1) for i in range(n) if i not in visited)
```

**Directed graph** — 3-color: 0=unvisited, 1=in-stack, 2=done:

```python
def has_cycle_directed(graph, n):
    color = [0] * n
    def dfs(node):
        color[node] = 1             # gray: in current path
        for nei in graph[node]:
            if color[nei] == 1: return True     # back edge
            if color[nei] == 0 and dfs(nei): return True
        color[node] = 2             # black: fully processed
        return False
    return any(dfs(i) for i in range(n) if color[i] == 0)
```

---

### Pattern 4 — Multi-Source BFS

When you have **multiple starting points**, add them all to the queue at level 0. Classic in "nearest X" problems.

```python
queue = deque()
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 1:          # all sources start at dist 0
            queue.append((r, c, 0))
            visited.add((r, c))
while queue:
    r, c, dist = queue.popleft()
    for dr, dc in directions:
        # expand outward from all sources simultaneously
```

---

### Pattern 5 — BFS on Implicit State Space

The "node" doesn't have to be a grid cell — it can be a **word, a game state, a tuple**. Word Ladder is the canonical example.

```python
def ladder_length(begin, end, word_list):
    word_set = set(word_list)
    queue = deque([(begin, 1)])
    visited = {begin}
    while queue:
        word, steps = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                nei = word[:i] + c + word[i+1:]
                if nei == end: return steps + 1
                if nei in word_set and nei not in visited:
                    visited.add(nei)
                    queue.append((nei, steps + 1))
    return 0
```

**Key insight**: generate neighbors on the fly instead of prebuilding the graph. This is O(26 × L × N) vs O(N²) for prebuilding.

---

## Topological Sort (Bonus — High ROI)

Two approaches — know both:

**Kahn's Algorithm (BFS)** — intuitive for interview explanation:

```python
from collections import deque

def topo_sort(n, prerequisites):
    indegree = [0] * n
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return order if len(order) == n else []   # empty = cycle exists
```

---

## Complexity Reference

| Algorithm | Time | Space |
|---|---|---|
| BFS / DFS | O(V + E) | O(V) |
| BFS on grid (R×C) | O(R×C) | O(R×C) |
| Word Ladder | O(26 × L × N) | O(N) |
| Topological sort | O(V + E) | O(V) |

---

## Common Interview Traps

| Trap | Fix |
|---|---|
| Marking visited on dequeue (not enqueue) | Always mark when you **add** to queue |
| Forgetting disconnected components | Outer loop over all nodes, not just one BFS/DFS |
| Using recursion on large grids (stack overflow) | Switch to iterative DFS with explicit stack |
| Not handling directed vs undirected cycle detection differently | 3-color for directed; parent-tracking for undirected |
| Rebuilding graph for every BFS call | Build once outside, pass in |

---

## The 16 Problems — Pattern-Mapped

### Pattern 1 — BFS Shortest Path

| # | Problem | Why it's here |
|---|---|---|
| 127 | Word Ladder | Implicit state BFS. Google classic. |
| 1091 | Shortest Path in Binary Matrix | Grid BFS with 8-directional moves |
| 863 | All Nodes Distance K in Binary Tree | Convert tree to graph, then BFS |
| 433 | Minimum Genetic Mutation | Word Ladder variant — same template |

### Pattern 2 — DFS / BFS Components & Flood Fill

| # | Problem | Why it's here |
|---|---|---|
| 200 | Number of Islands | The canonical graph/grid DFS problem |
| 130 | Surrounded Regions | Reverse flood fill from boundary |
| 417 | Pacific Atlantic Water Flow | Multi-source DFS from both oceans |
| 695 | Max Area of Island | DFS + return size |

### Pattern 3 — Cycle Detection & Validation

| # | Problem | Why it's here |
|---|---|---|
| 207 | Course Schedule | Directed cycle detection (3-color DFS) |
| 210 | Course Schedule II | Topo sort — return the order |
| 261 | Graph Valid Tree | Undirected: connected + no cycle |

### Pattern 4 — Multi-Source BFS

| # | Problem | Why it's here |
|---|---|---|
| 994 | Rotting Oranges | Multi-source BFS, track time |
| 286 | Walls and Gates | Multi-source BFS from all gates |
| 542 | 01 Matrix | Multi-source BFS from all 0s |

### Pattern 5 — Clone / Advanced Graph

| # | Problem | Why it's here |
|---|---|---|
| 133 | Clone Graph | DFS/BFS + HashMap for node mapping |
| 684 | Redundant Connection | DSU or DFS cycle detection |
| 785 | Is Graph Bipartite? | BFS 2-coloring |

---

## 5-Day Execution Plan

```
Day 1 — Grid DFS:    200, 695, 130
Day 2 — BFS:         1091, 994, 542
Day 3 — Implicit:    127, 433
Day 4 — Topo Sort:   207, 210, 261
Day 5 — Advanced:    417, 863, 133, 785
```

**Target**: Medium in < 15 min, Hard in < 30 min.

---

## Quick Reference

```
Reach for BFS when:   shortest path, minimum steps, level-by-level
Reach for DFS when:   explore all paths, components, cycle detection, topo sort

Grid neighbor template:
  directions = [(0,1),(0,-1),(1,0),(-1,0)]
  for dr, dc in directions:
      nr, nc = r+dr, c+dc
      if 0 <= nr < R and 0 <= nc < C and (nr,nc) not in visited

Always mark visited on ENQUEUE not dequeue.
Multi-source: seed all sources into queue at level 0.
Implicit graph: generate neighbors on the fly (Word Ladder).
```
