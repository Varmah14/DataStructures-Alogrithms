# BFS / DFS on Graphs & Grids — Complete Guide

## 1. Graph Representation

### Adjacency List (preferred for sparse graphs — most interview problems)
```python
# Unweighted
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # undirected

# Weighted
graph = defaultdict(list)
for u, v, w in edges:
    graph[u].append((v, w))
```

### Adjacency Matrix (dense graphs, O(1) edge lookup)
```python
mat = [[0] * n for _ in range(n)]
mat[u][v] = 1  # or weight
```

### Implicit Graph (grids)
No explicit construction. Neighbors generated on the fly:
```python
directions = [(0,1),(0,-1),(1,0),(-1,0)]
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        # (nr, nc) is a neighbor
```

**Space:** Adjacency list = O(V + E). Matrix = O(V²). For grids, V = rows × cols, E ≈ 4V.

---

## 2. BFS (Breadth-First Search)

### Core Idea
Explore level by level using a queue. Guarantees **shortest path in unweighted graphs**.

### Time/Space: O(V + E) time, O(V) space (queue + visited)

### Template: Standard BFS
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Template: BFS with Distance Tracking
```python
def bfs_distance(graph, start):
    dist = {start: 0}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist
```

### Template: BFS Level-by-Level
```python
def bfs_levels(graph, start):
    visited = {start}
    queue = deque([start])
    level = 0
    
    while queue:
        size = len(queue)  # freeze current level size
        for _ in range(size):
            node = queue.popleft()
            # process node at this level
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        level += 1
```

### Template: Grid BFS (Flood Fill / Shortest Path)
```python
def grid_bfs(grid, sr, sc):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    visited[sr][sc] = True
    queue = deque([(sr, sc, 0)])  # row, col, distance
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    
    while queue:
        r, c, d = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] != '#':
                visited[nr][nc] = True
                queue.append((nr, nc, d + 1))
```

### Template: Multi-Source BFS
Start BFS from multiple sources simultaneously. Used for "distance from nearest X" problems.
```python
def multi_source_bfs(grid, sources):
    rows, cols = len(grid), len(grid[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    queue = deque()
    
    for r, c in sources:
        dist[r][c] = 0
        queue.append((r, c))
    
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == float('inf'):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist
```

### When to Use BFS
- Shortest path in **unweighted** graph/grid
- Level-order traversal
- "Minimum number of steps/moves"
- "Nearest X from every cell" (multi-source BFS)
- Checking bipartiteness (2-colorability)

---

## 3. DFS (Depth-First Search)

### Core Idea
Explore as deep as possible before backtracking. Uses stack (explicit or recursion).

### Time/Space: O(V + E) time, O(V) space (recursion stack + visited)

### Template: Recursive DFS
```python
def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

### Template: Iterative DFS
```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

**Note:** Iterative DFS processes nodes in a different order than recursive DFS (reversed neighbor order). Usually doesn't matter, but be aware.

### Template: DFS on Grid
```python
def dfs_grid(grid, r, c, visited):
    rows, cols = len(grid), len(grid[0])
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if visited[r][c] or grid[r][c] == '0':
        return
    visited[r][c] = True
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs_grid(grid, r + dr, c + dc, visited)
```

### Template: DFS with Entry/Exit Times (important for tree/graph problems)
```python
timer = 0
entry = {}
exit_time = {}

def dfs_timed(graph, node, visited):
    global timer
    visited.add(node)
    timer += 1
    entry[node] = timer
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_timed(graph, neighbor, visited)
    
    timer += 1
    exit_time[node] = timer
```

**Use:** Node `u` is an ancestor of `v` iff `entry[u] < entry[v] < exit[v] < exit[u]`. Useful for subtree queries.

### When to Use DFS
- Connected components
- Cycle detection
- Topological sort (via post-order)
- Path finding (any path, not necessarily shortest)
- Subtree computations on trees
- Backtracking problems

---

## 4. Cycle Detection

### Undirected Graph — DFS
```python
def has_cycle_undirected(graph, n):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # back edge = cycle
        return False
    
    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    return False
```

### Directed Graph — DFS with Colors (White/Gray/Black)
```python
def has_cycle_directed(graph, n):
    # 0 = white (unvisited), 1 = gray (in stack), 2 = black (done)
    color = [0] * n
    
    def dfs(node):
        color[node] = 1  # gray
        for neighbor in graph[node]:
            if color[neighbor] == 1:
                return True  # back edge = cycle
            if color[neighbor] == 0:
                if dfs(neighbor):
                    return True
        color[node] = 2  # black
        return False
    
    for i in range(n):
        if color[i] == 0:
            if dfs(i):
                return True
    return False
```

**Key insight:** In directed graphs, only **back edges** (to gray nodes) indicate cycles. Cross edges (to black nodes) are fine.

### Undirected Graph — BFS Cycle Detection
```python
def has_cycle_bfs(graph, n):
    visited = set()
    for start in range(n):
        if start in visited:
            continue
        queue = deque([(start, -1)])
        visited.add(start)
        while queue:
            node, parent = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, node))
                elif neighbor != parent:
                    return True
    return False
```

---

## 5. Connected Components

### Undirected — Count Components
```python
def count_components(graph, n):
    visited = set()
    count = 0
    
    for i in range(n):
        if i not in visited:
            count += 1
            # BFS or DFS from i
            queue = deque([i])
            visited.add(i)
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
    return count
```

### Grid — Number of Islands (the classic)
```python
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                # Sink the island (DFS)
                stack = [(r, c)]
                grid[r][c] = '0'
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            stack.append((nr, nc))
    return count
```

**Trick:** Modify grid in-place to mark visited (set to '0'). Avoids separate visited array.

---

## 6. Bipartite Check (2-Coloring)

```python
def is_bipartite(graph, n):
    color = [-1] * n
    
    for start in range(n):
        if color[start] != -1:
            continue
        queue = deque([start])
        color[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
    return True
```

**Key:** A graph is bipartite iff it has no odd-length cycles.

---

## 7. Important Properties & Edge Cases

- **Disconnected graphs:** Always loop over all nodes to start BFS/DFS. Don't assume the graph is connected.
- **Self-loops:** Check `neighbor != node` if self-loops are possible.
- **Parallel edges:** Usually doesn't matter for BFS/DFS correctness, but affects cycle detection in undirected graphs. With adjacency lists, track parent by index, not by value.
- **0-indexed vs 1-indexed:** Read the problem carefully. Off-by-one is the #1 bug source.
- **Grid boundaries:** Always validate `0 <= nr < rows and 0 <= nc < cols` before accessing.
- **Visited marking timing:** In BFS, mark visited when **enqueuing**, not when dequeuing. Otherwise you'll enqueue duplicates. In DFS, mark when entering.
- **Recursion limit:** Python default is 1000. For large grids/graphs, either use iterative DFS or `sys.setrecursionlimit(N)`.

---

## 8. BFS vs DFS Decision Guide

| Scenario | Use |
|---|---|
| Shortest path (unweighted) | **BFS** |
| Level-order anything | **BFS** |
| Nearest X from every cell | **Multi-source BFS** |
| Connected components | Either (DFS slightly simpler) |
| Cycle detection | Either (DFS more natural for directed) |
| Topological sort | **DFS** (post-order) |
| Path exists? | Either |
| All paths | **DFS + backtracking** |
| Subtree computations | **DFS** |
| Strongly connected components | **DFS** (Tarjan/Kosaraju) |

---

## 9. LeetCode Problems

### Fundamentals (BFS/DFS Basics)
| # | Problem | Key Concept |
|---|---------|-------------|
| 200 | Number of Islands | Grid DFS/BFS — connected components |
| 733 | Flood Fill | Grid DFS — basic traversal |
| 695 | Max Area of Island | Grid DFS — track component size |
| 547 | Number of Provinces | Adjacency matrix — connected components |
| 841 | Keys and Rooms | DFS — reachability from node 0 |

### BFS Shortest Path
| # | Problem | Key Concept |
|---|---------|-------------|
| 994 | Rotting Oranges | Multi-source BFS |
| 1091 | Shortest Path in Binary Matrix | Grid BFS with 8 directions |
| 127 | Word Ladder | BFS on implicit graph (word transformations) |
| 752 | Open the Lock | BFS on state space |
| 1293 | Shortest Path in a Grid with Obstacles Elimination | BFS with state (row, col, remaining_k) |

### Cycle Detection
| # | Problem | Key Concept |
|---|---------|-------------|
| 207 | Course Schedule | Directed cycle detection |
| 802 | Find Eventual Safe States | Reverse topological / cycle detection |
| 684 | Redundant Connection | Undirected cycle (DSU also works) |

### Bipartite / Coloring
| # | Problem | Key Concept |
|---|---------|-------------|
| 785 | Is Graph Bipartite? | BFS/DFS 2-coloring |
| 886 | Possible Bipartition | Bipartite check with constraints |

### Advanced BFS/DFS
| # | Problem | Key Concept |
|---|---------|-------------|
| 417 | Pacific Atlantic Water Flow | Multi-source DFS from both oceans |
| 1162 | As Far from Land as Possible | Multi-source BFS from all land cells |
| 934 | Shortest Bridge | DFS to find island + BFS to expand |
| 1254 | Number of Closed Islands | Grid DFS — boundary handling |
| 542 | 01 Matrix | Multi-source BFS from all 0s |

### Study Order
**Phase 1 (2-3 days):** 200, 733, 695, 547, 841
**Phase 2 (2-3 days):** 994, 1091, 127, 752
**Phase 3 (2-3 days):** 207, 785, 684, 417
**Phase 4 (2-3 days):** 1162, 934, 1293, 542
