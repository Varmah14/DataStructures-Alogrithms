# Range Data Structures — BIT, Segment Tree, Sparse Table

## 1. When to Use What

| DS | Build | Point Update | Range Query | Use When |
|---|---|---|---|---|
| Prefix Sum | O(n) | O(n) rebuild | O(1) | Static array, sum queries |
| BIT (Fenwick) | O(n) | O(log n) | O(log n) | Dynamic prefix sums |
| Segment Tree | O(n) | O(log n) | O(log n) | Any associative operation + updates |
| Segment Tree + Lazy | O(n) | O(log n) | O(log n) | Range updates + range queries |
| Sparse Table | O(n log n) | ❌ | O(1) | Static array, min/max/gcd queries |

---

## 2. BIT (Binary Indexed Tree / Fenwick Tree)

### Core Idea
A tree stored in an array where each index is responsible for a range of elements. Index `i` covers elements from `i - lowbit(i) + 1` to `i`, where `lowbit(i) = i & (-i)`.

### Implementation
```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed
    
    def update(self, i, delta):
        """Add delta to index i (1-indexed)"""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    
    def query(self, i):
        """Prefix sum [1, i]"""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s
    
    def range_query(self, l, r):
        """Sum [l, r] inclusive (1-indexed)"""
        return self.query(r) - self.query(l - 1)
    
    def build(self, arr):
        """Build from array in O(n)"""
        for i in range(1, self.n + 1):
            self.tree[i] += arr[i - 1]
            j = i + (i & (-i))
            if j <= self.n:
                self.tree[j] += self.tree[i]
```

### How `i & (-i)` Works
`-i` in two's complement flips all bits and adds 1. `i & (-i)` isolates the lowest set bit.
- `i = 6 (110)` → `lowbit = 2 (010)` → covers indices 5-6
- `i = 8 (1000)` → `lowbit = 8 (1000)` → covers indices 1-8

**Update** climbs up: add `lowbit` to move to parent.
**Query** climbs down: subtract `lowbit` to accumulate prefix.

### BIT for Count of Inversions
```python
def count_inversions(nums):
    # Coordinate compress
    sorted_unique = sorted(set(nums))
    rank = {v: i+1 for i, v in enumerate(sorted_unique)}
    
    bit = BIT(len(sorted_unique))
    inversions = 0
    
    for num in reversed(nums):
        inversions += bit.query(rank[num] - 1)  # count smaller seen so far
        bit.update(rank[num], 1)
    
    return inversions
```

---

## 3. Segment Tree

### Core Idea
A full binary tree where each node stores the answer for a range. Leaves = individual elements. Internal nodes = merge of children.

### Implementation (Iterative — faster)
```python
class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (2 * n)
    
    def build(self, arr):
        # Fill leaves
        for i in range(self.n):
            self.tree[self.n + i] = arr[i]
        # Build internal nodes
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]
    
    def update(self, i, val):
        """Set index i to val (0-indexed)"""
        i += self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]
    
    def query(self, l, r):
        """Sum [l, r) (0-indexed, half-open)"""
        res = 0
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                res += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res
```

### Recursive Implementation (more flexible)
```python
class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2*node, start, mid)
        self._build(arr, 2*node+1, mid+1, end)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    
    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2*node, start, mid, idx, val)
        else:
            self._update(2*node+1, mid+1, end, idx, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0  # identity for sum
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self._query(2*node, start, mid, l, r) +
                self._query(2*node+1, mid+1, end, l, r))
    
    def update(self, idx, val):
        self._update(1, 0, self.n-1, idx, val)
    
    def query(self, l, r):
        return self._query(1, 0, self.n-1, l, r)
```

### Segment Tree with Lazy Propagation
For range updates (add val to all elements in [l, r]).
```python
class LazySegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)
    
    def _push_down(self, node, start, end):
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            self._apply(2*node, start, mid, self.lazy[node])
            self._apply(2*node+1, mid+1, end, self.lazy[node])
            self.lazy[node] = 0
    
    def _apply(self, node, start, end, val):
        self.tree[node] += val * (end - start + 1)
        self.lazy[node] += val
    
    def range_update(self, node, start, end, l, r, val):
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self._apply(node, start, end, val)
            return
        self._push_down(node, start, end)
        mid = (start + end) // 2
        self.range_update(2*node, start, mid, l, r, val)
        self.range_update(2*node+1, mid+1, end, l, r, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]
    
    def range_query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        self._push_down(node, start, end)
        mid = (start + end) // 2
        return (self.range_query(2*node, start, mid, l, r) +
                self.range_query(2*node+1, mid+1, end, l, r))
```

---

## 4. Sparse Table

### Core Idea
Precompute answers for all power-of-2 ranges. Query any range by combining two overlapping precomputed ranges. Only works for **idempotent** operations (min, max, gcd — where `f(a, a) = a`). Does NOT work for sum.

```python
import math

class SparseTable:
    def __init__(self, arr):
        n = len(arr)
        k = int(math.log2(n)) + 1
        self.table = [[0] * n for _ in range(k)]
        self.table[0] = arr[:]
        self.log = [0] * (n + 1)
        
        for i in range(2, n + 1):
            self.log[i] = self.log[i // 2] + 1
        
        for j in range(1, k):
            for i in range(n - (1 << j) + 1):
                self.table[j][i] = min(
                    self.table[j-1][i],
                    self.table[j-1][i + (1 << (j-1))]
                )
    
    def query(self, l, r):
        """Range minimum query [l, r] inclusive"""
        j = self.log[r - l + 1]
        return min(self.table[j][l], self.table[j][r - (1 << j) + 1])
```
**Build:** O(n log n). **Query:** O(1). **No updates.**

---

## 5. Comparison

| | Prefix Sum | BIT | Seg Tree | Seg Tree + Lazy | Sparse Table |
|---|---|---|---|---|---|
| Build | O(n) | O(n) | O(n) | O(n) | O(n log n) |
| Point update | O(n) | O(log n) | O(log n) | O(log n) | ❌ |
| Range update | ❌ | O(log n)* | ❌ | O(log n) | ❌ |
| Range query | O(1) | O(log n) | O(log n) | O(log n) | O(1) |
| Operations | Sum | Sum (invertible) | Any assoc. | Any assoc. | Idempotent |
| Code complexity | Low | Medium | High | Very high | Medium |

*BIT range update requires a second BIT (difference technique).

---

## 6. When to Use Each

- **Static array, sum queries** → Prefix sum (simplest)
- **Point updates + prefix/range sums** → BIT (cleanest code for sum)
- **Point updates + range min/max/any** → Segment tree
- **Range updates + range queries** → Segment tree with lazy
- **Static array, min/max queries, O(1) query needed** → Sparse table
- **Count inversions, count smaller after self** → BIT with coordinate compression

---

## 7. GATE Theory

- BIT: cannot handle non-invertible operations (max, min). Use segment tree instead.
- Segment tree size: `4n` is safe (some use `2 * next_power_of_2`, but `4n` always works).
- Lazy propagation: essential for range updates. Without it, range update is O(n log n).
- Sparse table: O(1) queries without updates make it ideal for RMQ as preprocessing for LCA (Euler tour + RMQ = O(n log n) / O(1) LCA).

---

## 8. LeetCode Problems

### BIT
| # | Problem | Key Concept |
|---|---------|-------------|
| 307 | Range Sum Query - Mutable | Basic BIT or seg tree |
| 315 | Count of Smaller Numbers After Self | BIT + coordinate compression |
| 493 | Reverse Pairs | BIT or merge sort |
| 1649 | Create Sorted Array through Instructions | BIT for count inversions |

### Segment Tree
| # | Problem | Key Concept |
|---|---------|-------------|
| 307 | Range Sum Query - Mutable | Basic seg tree |
| 699 | Falling Squares | Interval max update + query |
| 218 | The Skyline Problem | Sweep line + seg tree (or heap) |
| 732 | My Calendar III | Sweep or seg tree with lazy |

### Sparse Table / RMQ
| # | Problem | Key Concept |
|---|---------|-------------|
| 239 | Sliding Window Maximum | Monotonic deque (or sparse table) |
| 2104 | Sum of Subarray Ranges | Monotonic stack (related to RMQ) |

### Study Order
**Phase 1 (2-3 days):** 307 (BIT), 307 (seg tree), understand both
**Phase 2 (2-3 days):** 315, 493
**Phase 3 (2-3 days):** 699, 218, 732
