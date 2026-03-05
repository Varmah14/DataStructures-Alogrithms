# Trees (Basics + LCA)

> **Interview Focus**: FAANG + Mid-tier | Pattern-depth over breadth

---

## What Interviewers Actually Test Here

Tree problems are the most consistent topic at FAANG — almost every loop includes one. They test:

- Can you **think recursively** and define clean base cases without prompting?
- Do you understand the **return-value contract** of your recursive calls?
- Can you handle **path problems** that cross through a root (not just top-down)?
- For BSTs, do you exploit the **sorted property** rather than treating it as a generic tree?

---

## Core Concepts

### Tree Node Structure

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### The Four Traversals

```python
# Inorder: Left → Root → Right  (BST inorder = sorted sequence)
def inorder(root):
    if not root: return
    inorder(root.left)
    process(root.val)
    inorder(root.right)

# Preorder: Root → Left → Right  (serialize tree, path problems)
def preorder(root):
    if not root: return
    process(root.val)
    preorder(root.left)
    preorder(root.right)

# Postorder: Left → Right → Root  (bottom-up: heights, diameters, deletions)
def postorder(root):
    if not root: return
    postorder(root.left)
    postorder(root.right)
    process(root.val)

# Level-order: BFS row by row
from collections import deque
def level_order(root):
    if not root: return
    queue = deque([root])
    while queue:
        for _ in range(len(queue)):   # process one level at a time
            node = queue.popleft()
            process(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
```

**BST inorder = sorted** is the single most exploited tree property in interviews.

---

## The 6 Core Patterns

---

### Pattern 1 — Bottom-Up Postorder (Height / Diameter)

The key insight: compute something at children first, combine at parent. Return a value upward.

```python
def height(root):
    if not root: return 0
    left_h = height(root.left)
    right_h = height(root.right)
    return 1 + max(left_h, right_h)
```

**Diameter of Binary Tree** — the path that crosses through a node:

```python
def diameter(root):
    self.ans = 0
    def depth(node):
        if not node: return 0
        l = depth(node.left)
        r = depth(node.right)
        self.ans = max(self.ans, l + r)   # path through this node
        return 1 + max(l, r)              # return height upward
    depth(root)
    return self.ans
```

**Pattern**: whenever the answer involves a path **crossing** through a node (not just going down), use a nonlocal/global variable updated at each node, while the function returns something different (height).

---

### Pattern 2 — Top-Down DFS (Path Problems)

Pass information **downward** — accumulated sum, current path, target.

```python
def has_path_sum(root, target):
    if not root: return False
    if not root.left and not root.right:   # leaf
        return root.val == target
    return (has_path_sum(root.left, target - root.val) or
            has_path_sum(root.right, target - root.val))
```

**Path Sum III** (paths anywhere, not just root-to-leaf) — combine with prefix sum:

```python
def path_sum(root, target):
    prefix = {0: 1}
    def dfs(node, curr_sum):
        if not node: return 0
        curr_sum += node.val
        ans = prefix.get(curr_sum - target, 0)
        prefix[curr_sum] = prefix.get(curr_sum, 0) + 1
        ans += dfs(node.left, curr_sum) + dfs(node.right, curr_sum)
        prefix[curr_sum] -= 1          # backtrack — critical
        return ans
    return dfs(root, 0)
```

**Always backtrack the prefix map** — this is the most common bug in this pattern.

---

### Pattern 3 — BST Operations

Exploit the sorted property at every step — you should never need O(n) for BST operations.

```python
# Search — O(h), O(log n) balanced
def search_bst(root, val):
    if not root or root.val == val: return root
    return search_bst(root.left if val < root.val else root.right, val)

# Insert — O(h)
def insert_bst(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left = insert_bst(root.left, val)
    else: root.right = insert_bst(root.right, val)
    return root

# Delete — O(h) — the tricky one
def delete_bst(root, key):
    if not root: return None
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:
        if not root.left: return root.right
        if not root.right: return root.left
        # find inorder successor (min of right subtree)
        successor = root.right
        while successor.left: successor = successor.left
        root.val = successor.val
        root.right = delete_bst(root.right, successor.val)
    return root
```

**Kth Smallest in BST**: inorder traversal, stop at kth element. Can be done iteratively with a stack for O(k) time.

**Validate BST**: pass min/max bounds down — don't just check parent.

```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if not (lo < root.val < hi): return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
```

---

### Pattern 4 — Level-Order / BFS on Trees

Use when problems mention "level," "row," "depth," "cousin," "zigzag."

```python
def level_order(root):
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

The `for _ in range(len(queue))` snapshot is the standard trick to process exactly one level.

---

### Pattern 5 — Construct Tree from Traversals

**From Preorder + Inorder**:

```python
def build_tree(preorder, inorder):
    if not inorder: return None
    root_val = preorder.pop(0)          # first of preorder = root
    root = TreeNode(root_val)
    mid = inorder.index(root_val)       # find root in inorder
    root.left = build_tree(preorder, inorder[:mid])
    root.right = build_tree(preorder, inorder[mid+1:])
    return root
```

**Optimization**: use a hashmap for O(1) inorder index lookup instead of O(n) `.index()`.

Same idea applies to Postorder + Inorder (root is last element of postorder).

---

### Pattern 6 — LCA (Lowest Common Ancestor)

**Standard Binary Tree LCA**:

```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right: return root    # p and q are on different sides
    return left or right              # both on same side, or one found
```

**BST LCA** — exploit ordering:

```python
def lca_bst(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lca_bst(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lca_bst(root.right, p, q)
    return root    # split point = LCA
```

**Binary Lifting LCA** (for repeated queries on large trees — rarely needed in interviews but know conceptually):
- Precompute `ancestor[node][j]` = 2^j-th ancestor
- Answer each LCA query in O(log n)
- Total: O(n log n) preprocessing, O(log n) per query

---

## Key Tree Properties to Know Cold

| Property | Value |
|---|---|
| Height of complete binary tree with n nodes | ⌊log₂ n⌋ |
| Max nodes at level k (0-indexed) | 2^k |
| Total nodes in perfect binary tree of height h | 2^(h+1) - 1 |
| Leaves in a full binary tree with n internal nodes | n + 1 |
| BST inorder traversal | Sorted ascending |
| BST inorder predecessor | Max of left subtree |
| BST inorder successor | Min of right subtree |

---

## Complexity Reference

| Operation | Balanced BST | Skewed BST (worst) |
|---|---|---|
| Search / Insert / Delete | O(log n) | O(n) |
| Height | O(log n) | O(n) |
| Any traversal | O(n) | O(n) |
| LCA (naive) | O(log n) BST / O(n) general | O(n) |
| LCA (binary lifting) | O(log n) after O(n log n) prep | — |

---

## Common Interview Traps

| Trap | Fix |
|---|---|
| Diameter: returning diameter instead of height from recursive call | Function returns **height**; update global with `l + r` |
| Path Sum III: not backtracking prefix map | Always `prefix[curr] -= 1` after recursive calls |
| BST validation: only checking parent | Pass `lo` and `hi` bounds through recursion |
| Build tree: using `list.index()` in recursion — O(n²) total | Precompute `{val: idx}` hashmap |
| LCA: assuming nodes are always present | Handle `if not root` carefully |

---

## The 17 Problems — Pattern-Mapped

### Pattern 1 — Bottom-Up (Height / Diameter)

| # | Problem | Why it's here |
|---|---|---|
| 104 | Maximum Depth of Binary Tree | Height — the base pattern |
| 543 | Diameter of Binary Tree | Classic nonlocal ans + return height |
| 110 | Balanced Binary Tree | Return -1 as sentinel for imbalance |
| 124 | Binary Tree Maximum Path Sum | Same nonlocal trick, any-to-any path. Hard. |

### Pattern 2 — Top-Down / Path Problems

| # | Problem | Why it's here |
|---|---|---|
| 112 | Path Sum | Basic top-down DFS |
| 113 | Path Sum II | Collect paths — backtracking |
| 437 | Path Sum III | Prefix sum + DFS — most important |

### Pattern 3 — BST

| # | Problem | Why it's here |
|---|---|---|
| 230 | Kth Smallest in BST | Inorder traversal, stop early |
| 98 | Validate Binary Search Tree | Bounds passing |
| 450 | Delete Node in BST | Successor/predecessor logic |
| 235 | LCA of BST | Exploit BST ordering |

### Pattern 4 — Level Order

| # | Problem | Why it's here |
|---|---|---|
| 102 | Binary Tree Level Order Traversal | The template |
| 103 | Zigzag Level Order Traversal | Alternate direction per level |
| 199 | Binary Tree Right Side View | Last node per level |

### Pattern 5 — Construction

| # | Problem | Why it's here |
|---|---|---|
| 105 | Construct from Preorder and Inorder | Must know |
| 106 | Construct from Postorder and Inorder | Same idea, root at end |

### Pattern 6 — LCA

| # | Problem | Why it's here |
|---|---|---|
| 236 | LCA of Binary Tree | The general case |
| 1644 | LCA with nodes possibly absent | Handle null propagation carefully |

---

## 5-Day Execution Plan

```
Day 1 — Traversals + Height:  104, 543, 110, 102
Day 2 — Path problems:        112, 113, 437
Day 3 — BST:                  98, 230, 450, 235
Day 4 — Level order + Build:  103, 199, 105, 106
Day 5 — LCA + Hard:           236, 124
```

---

## Quick Reference

```
Bottom-up (postorder):  compute at children, combine at parent
Top-down (preorder):    pass state downward, check at leaves
BST property:           left < root < right; inorder = sorted

Diameter / Max Path Sum pattern:
  def dfs(node):
      l, r = dfs(left), dfs(right)
      ans = max(ans, l + r + node.val)   # path through node
      return max(l, r) + node.val         # height upward

Path Sum III pattern:
  prefix = {0: 1}
  curr += node.val
  ans += prefix.get(curr - target, 0)
  prefix[curr] += 1
  recurse children
  prefix[curr] -= 1   # ← ALWAYS backtrack

LCA pattern:
  if not root or root == p or root == q: return root
  l, r = lca(left, p, q), lca(right, p, q)
  return root if l and r else l or r
```
