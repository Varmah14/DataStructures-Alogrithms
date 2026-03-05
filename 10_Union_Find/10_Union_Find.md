# Union-Find (Disjoint Set Union)

> **Interview Focus**: FAANG + Mid-tier | Pattern-depth over breadth

---

## What Interviewers Actually Test Here

DSU is one of the most elegant data structures in competitive programming — and interviewers love it because it's easy to misuse. They test:

- Can you recognize **dynamic connectivity** problems vs static ones (where DFS/BFS is enough)?
- Do you implement DSU with both **union by rank** and **path compression** — and can you explain why each matters?
- Can you augment DSU with extra state (size, weight) for harder problems?

---

## Core Concept

DSU maintains a **partition of elements into disjoint sets**. Two core operations:

- `find(x)` — which set does `x` belong to? (returns the root/representative)
- `union(x, y)` — merge the sets containing `x` and `y`

The magic: after optimizations, both operations are effectively **O(α(n))** — inverse Ackermann function, so slow-growing it's practically O(1) for any real input.

---

## Implementation — The One to Memorize

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n          # optional: track component sizes
        self.components = n          # optional: track number of components

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False             # already in same set
        # union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True                  # merged two different sets

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Path compression**: on every `find`, make each node point directly to root. Flattens the tree over time.

**Union by rank**: always attach the shorter tree under the taller one. Prevents degenerate chains.

Without optimizations: O(n) per operation. With both: O(α(n)) amortized — the theoretical gold standard.

---

## Why DSU Over DFS/BFS?

| Scenario | DFS/BFS | DSU |
|---|---|---|
| One-time connectivity check | ✅ Fine | Overkill |
| **Edges added dynamically** | ❌ Re-run each time | ✅ O(α(n)) per edge |
| Cycle detection during edge processing | Possible but verbose | ✅ Natural |
| Minimum spanning tree (Kruskal) | ❌ | ✅ Core algorithm |

**Rule of thumb**: if edges are added one-by-one and you need to answer connectivity queries after each — DSU.

---

## The 4 Patterns

---

### Pattern 1 — Dynamic Connectivity / Component Counting

Process edges one by one. After each `union`, check `dsu.components`.

```python
dsu = DSU(n)
for u, v in edges:
    dsu.union(u, v)
return dsu.components
```

**Interview tip**: adding `self.components` counter to DSU pays dividends — you avoid a final O(n) scan to count roots.

---

### Pattern 2 — Cycle Detection

An edge `(u, v)` creates a cycle if and only if `find(u) == find(v)` before the union.

```python
dsu = DSU(n)
for u, v in edges:
    if dsu.connected(u, v):
        return [u, v]          # this edge is redundant
    dsu.union(u, v)
```

This is the backbone of **Kruskal's MST** — process edges in sorted weight order, skip edges that form cycles.

---

### Pattern 3 — Kruskal's MST

```python
def kruskal(n, edges):
    edges.sort(key=lambda e: e[2])    # sort by weight
    dsu = DSU(n)
    mst_cost = 0
    mst_edges = 0
    for u, v, w in edges:
        if dsu.union(u, v):           # only add if not already connected
            mst_cost += w
            mst_edges += 1
            if mst_edges == n - 1:
                break                 # MST complete
    return mst_cost if mst_edges == n - 1 else -1   # -1 if disconnected
```

O(E log E) for sorting + O(E α(V)) for DSU operations = **O(E log E)** overall.

---

### Pattern 4 — Grouping / Accounts Merge

When entities need to be grouped by shared properties (same email = same person), DSU handles transitive grouping cleanly.

```python
# Map each email to an account index
email_to_id = {}
dsu = DSU(len(accounts))
for i, account in enumerate(accounts):
    for email in account[1:]:
        if email in email_to_id:
            dsu.union(i, email_to_id[email])
        else:
            email_to_id[email] = i
# Collect grouped results
groups = defaultdict(set)
for email, idx in email_to_id.items():
    groups[dsu.find(idx)].add(email)
```

**Key insight**: you're unioning accounts (indices), not emails. Emails are just the bridge that tells you which accounts to merge.

---

## Augmented DSU

For harder problems, add extra state to each component:

```python
# Weighted DSU — track relative weight/distance to parent
def __init__(self, n):
    self.parent = list(range(n))
    self.weight = [0] * n        # weight[x] = weight of x relative to parent

def find(self, x):
    if self.parent[x] != x:
        root = self.find(self.parent[x])
        self.weight[x] += self.weight[self.parent[x]]   # accumulate on path
        self.parent[x] = root
    return self.parent[x]
```

Used in: LC 399 (Evaluate Division), LC 990 (Satisfiability of Equality Equations).

---

## Complexity Reference

| Operation | Naive | With Path Compression Only | With Both Optimizations |
|---|---|---|---|
| find | O(n) | O(log n) amortized | O(α(n)) amortized |
| union | O(n) | O(log n) amortized | O(α(n)) amortized |
| n operations | O(n²) | O(n log n) | O(n α(n)) ≈ O(n) |

α(n) < 5 for all practical values of n (up to 10^80).

---

## Common Interview Traps

| Trap | Fix |
|---|---|
| Forgetting path compression | Always use recursive `find` with reassignment |
| Union by size vs rank — mixing them up | Pick one and be consistent. Rank is slightly simpler to reason about. |
| Not returning False when nodes already connected | `union` should return bool — callers often need to know |
| String nodes (not integers) | Map strings to integers first with a dict, or use dict-based parent |
| Forgetting to decrement component count | Maintain `self.components`, only decrement when `px != py` |

---

## String-Key DSU (Common in Interview Problems)

When nodes are strings or non-integers:

```python
class DSU:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self.parent[self.find(x)] = self.find(y)
```

---

## The 12 Problems — Pattern-Mapped

### Pattern 1 — Dynamic Connectivity

| # | Problem | Why it's here |
|---|---|---|
| 323 | Number of Connected Components | DSU basics, component count |
| 547 | Number of Provinces | Same pattern, adjacency matrix input |
| 1971 | Find if Path Exists in Graph | Direct connectivity check |

### Pattern 2 — Cycle Detection

| # | Problem | Why it's here |
|---|---|---|
| 684 | Redundant Connection | Undirected cycle via DSU |
| 685 | Redundant Connection II | Directed graph — harder variant |
| 261 | Graph Valid Tree | Connected + no cycle = tree |

### Pattern 3 — Kruskal / MST-Adjacent

| # | Problem | Why it's here |
|---|---|---|
| 1584 | Min Cost to Connect All Points | Kruskal on Euclidean distances |
| 1135 | Connecting Cities with Min Cost | Pure Kruskal |
| 778 | Swim in Rising Water | Binary search + DSU or Dijkstra |

### Pattern 4 — Grouping / Merge

| # | Problem | Why it's here |
|---|---|---|
| 721 | Accounts Merge | Transitive grouping via shared emails |
| 990 | Satisfiability of Equality Equations | Equality/inequality constraints via DSU |
| 399 | Evaluate Division | Weighted DSU — advanced |

---

## 4-Day Execution Plan

```
Day 1 — Implement DSU from scratch (both optimizations + size/component tracking)
         Solve: 323, 547, 261
Day 2 — Cycle detection: 684, 685
         Kruskal: 1584, 1135
Day 3 — Grouping: 721, 990
Day 4 — Advanced: 399, 778
         Review: re-implement DSU cold from memory
```

---

## Quick Reference

```
DSU shines when:
  ✓ Edges added dynamically, connectivity queried after each
  ✓ Cycle detection during edge-by-edge processing
  ✓ Kruskal MST
  ✓ Transitive grouping (accounts merge, friend circles)

Template checklist:
  □ parent = list(range(n))
  □ rank/size array initialized
  □ find() with path compression
  □ union() with rank — return bool
  □ components counter (optional but useful)

Cycle trick: find(u) == find(v) BEFORE union → cycle exists.
Kruskal: sort edges by weight, union greedily, skip if same component.
```
