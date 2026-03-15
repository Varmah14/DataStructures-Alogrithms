# Union-Find (Disjoint Set Union) — Complete Guide

## 1. What Is DSU?

A data structure that tracks a collection of **disjoint (non-overlapping) sets**. Supports two operations:
- **Find(x):** Which set does element x belong to? (returns the representative/root)
- **Union(x, y):** Merge the sets containing x and y.

Think of it as maintaining connected components dynamically — you can add edges but not remove them.

---

## 2. Core Implementation

### Naive (just parent array)
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py
```
**Problem:** Trees can degenerate to chains → O(n) per find.

### Optimized: Path Compression + Union by Rank
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px  # attach smaller tree under larger
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True  # merged two components
```

### Amortized Complexity
With both optimizations: **O(α(n))** per operation, where α is the inverse Ackermann function. For all practical purposes, α(n) ≤ 4 for any n that fits in the universe. Treat it as **O(1) amortized**.

**Path compression alone:** O(log n) amortized.
**Union by rank alone:** O(log n) worst case.
**Both together:** O(α(n)) — this is the standard you should always implement.

---

## 3. Variants

### Union by Size (alternative to union by rank)
Track subtree size instead of rank. Useful when you need component sizes.
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        return True
    
    def get_size(self, x):
        return self.size[self.find(x)]
```

### DSU with Component Count
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n  # track number of components
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True
```

### Weighted / Distance DSU
Track a value (distance/weight) from each node to its root. Used in problems like "is the relationship consistent?"
```python
class WeightedDSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.weight = [0] * n  # weight[x] = distance from x to parent[x]
    
    def find(self, x):
        if self.parent[x] != x:
            root = self.find(self.parent[x])
            self.weight[x] += self.weight[self.parent[x]]  # accumulate path weight
            self.parent[x] = root
        return self.parent[x]
    
    def union(self, x, y, w):
        # w = weight(x) - weight(y), i.e., x is w heavier than y
        px, py = self.find(x), self.find(y)
        if px == py:
            return self.weight[x] - self.weight[y] == w  # consistency check
        # weight[x] + diff(px to new root) = w + weight[y] + diff(py to new root)
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
            self.weight[px] = w + self.weight[y] - self.weight[x]
        else:
            self.parent[py] = px
            self.weight[py] = -w + self.weight[x] - self.weight[y]
            if self.rank[px] == self.rank[py]:
                self.rank[px] += 1
        return True
```

---

## 4. Key Patterns

### Pattern A: Dynamic Connectivity
Process edges one by one, answer "are x and y connected?" queries.
```python
dsu = DSU(n)
for u, v in edges:
    dsu.union(u, v)
# Query
if dsu.find(a) == dsu.find(b):
    print("connected")
```

### Pattern B: Detect Redundant Edge (Cycle Detection)
If union returns False, the edge connects already-connected nodes → redundant.
```python
dsu = DSU(n)
for u, v in edges:
    if not dsu.union(u, v):
        print(f"Redundant edge: {u}-{v}")
```

### Pattern C: Kruskal's MST
Sort edges by weight, greedily add if they connect different components.
```python
def kruskal(n, edges):
    edges.sort(key=lambda x: x[2])  # sort by weight
    dsu = DSU(n)
    mst_weight = 0
    mst_edges = []
    
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
    
    return mst_weight, mst_edges
```

### Pattern D: Grid Connectivity
Map 2D grid to 1D indices for DSU.
```python
def grid_index(r, c, cols):
    return r * cols + c

dsu = DSU(rows * cols)
# Connect adjacent cells
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':
            for dr, dc in [(0,1),(1,0)]:  # only right and down to avoid double-counting
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    dsu.union(grid_index(r, c, cols), grid_index(nr, nc, cols))
```

### Pattern E: Accounts Merge / Group by Equivalence
When items belong to the same group if they share any attribute.
```python
# Map each attribute to the first item that had it
# Union all items sharing an attribute
attribute_to_id = {}
dsu = DSU(n)

for i, attributes in enumerate(items):
    for attr in attributes:
        if attr in attribute_to_id:
            dsu.union(i, attribute_to_id[attr])
        else:
            attribute_to_id[attr] = i

# Group items by root
groups = defaultdict(list)
for i in range(n):
    groups[dsu.find(i)].append(i)
```

---

## 5. DSU vs DFS/BFS for Connectivity

| | DSU | DFS/BFS |
|---|---|---|
| Build time | O(n · α(n)) | O(V + E) |
| Dynamic edges (online) | ✅ natural | ❌ rebuild from scratch |
| Query after build | O(α(n)) | O(1) with preprocessing |
| Edge removal | ❌ not supported | ❌ not supported |
| Space | O(n) | O(V + E) for graph |

**Use DSU when:** edges arrive dynamically / online, you need cycle detection during construction, or the problem says "process edges one by one."

**Use DFS/BFS when:** the full graph is given upfront, you need shortest paths, or you need traversal order.

---

## 6. Edge Cases & Pitfalls

- **Self-loops:** `union(x, x)` should be a no-op. Check `px == py`.
- **0-indexed vs 1-indexed nodes:** Common bug source. Make DSU size `n+1` if nodes are 1-indexed.
- **Recursion depth for path compression:** For n > 1000, Python might hit recursion limit. Use iterative find:

```python
def find(self, x):
    root = x
    while self.parent[root] != root:
        root = self.parent[root]
    while self.parent[x] != root:  # path compression iteratively
        self.parent[x], x = root, self.parent[x]
    return root
```

- **Union return value:** Make `union()` return True/False — tells you if a merge happened. Essential for cycle detection and counting components.
- **Don't forget both optimizations:** Using only path compression or only union by rank gives O(log n). You want both for O(α(n)).

---

## 7. GATE-Level Theory

- **Proof that union by rank gives O(log n) height:** By induction — a tree of rank k has at least 2^k nodes. So rank ≤ log₂(n), and find follows at most log₂(n) links.
- **Inverse Ackermann:** α(n) grows absurdly slowly. α(2^65536) = 4. For interview purposes, just say "effectively constant."
- **Lower bound:** Ω(α(n)) per operation is tight (Fredman & Saks). You can't do better with a pointer-based structure.
- **Persistent DSU:** Possible with rollback (undo last union) using a stack. Don't use path compression — use union by rank only. Needed for offline divide & conquer.

---

## 8. LeetCode Problems

### Fundamentals
| # | Problem | Key Concept |
|---|---------|-------------|
| 547 | Number of Provinces | Basic DSU — count components |
| 684 | Redundant Connection | Union returns false = cycle edge |
| 721 | Accounts Merge | Group by shared attribute pattern |
| 323 | Number of Connected Components | Direct component counting |
| 261 | Graph Valid Tree | n-1 edges + no cycle = tree |

### Grid-Based DSU
| # | Problem | Key Concept |
|---|---------|-------------|
| 200 | Number of Islands | DSU on grid (compare with DFS approach) |
| 130 | Surrounded Regions | Union border O's with virtual node |
| 1102 | Path With Maximum Minimum Value | Sort cells by value + DSU |

### Advanced DSU
| # | Problem | Key Concept |
|---|---------|-------------|
| 399 | Evaluate Division | Weighted DSU (or BFS on graph) |
| 685 | Redundant Connection II | Directed graph — handle two cases |
| 1319 | Number of Operations to Make Network Connected | Components - 1 = operations needed |
| 947 | Most Stones Removed | Stones share row/col → same component |
| 990 | Satisfiability of Equality Equations | Union equals, check not-equals |
| 1584 | Min Cost to Connect All Points | Kruskal MST |

### Study Order
**Phase 1 (2 days):** 547, 684, 261, 323, 990
**Phase 2 (2-3 days):** 721, 200 (DSU approach), 130, 1319
**Phase 3 (2-3 days):** 399, 947, 1584, 685
