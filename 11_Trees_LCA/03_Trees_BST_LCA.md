# Trees (Basics + BST + LCA) — Complete Guide

## 1. Tree Fundamentals

A tree is a connected acyclic graph with n nodes and n-1 edges. A **rooted tree** has a designated root; every other node has exactly one parent.

### Representation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Key Properties
- **Height:** longest path from root to leaf. Single node = height 0.
- **Depth:** distance from root. Root = depth 0.
- **Complete binary tree:** all levels full except possibly last, filled left to right (heap property).
- **Full binary tree:** every node has 0 or 2 children.
- **Perfect binary tree:** all internal nodes have 2 children, all leaves at same level. Has 2^(h+1) - 1 nodes.
- **Balanced:** height = O(log n). AVL, Red-Black trees guarantee this.

---

## 2. Tree Traversals

### Inorder (Left → Root → Right)
```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Iterative (important — asked frequently)
def inorder_iterative(root):
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

### Preorder (Root → Left → Right)
```python
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Iterative
def preorder_iterative(root):
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)  # right first so left is processed first
        if node.left:
            stack.append(node.left)
    return result
```

### Postorder (Left → Right → Root)
```python
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# Iterative (trickier)
def postorder_iterative(root):
    if not root:
        return []
    result, stack = [], [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    return result[::-1]  # reverse of modified preorder (Root→Right→Left)
```

### Level-Order (BFS)
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

### Morris Traversal (O(1) space inorder)
```python
def morris_inorder(root):
    result = []
    curr = root
    while curr:
        if not curr.left:
            result.append(curr.val)
            curr = curr.right
        else:
            # Find inorder predecessor
            pred = curr.left
            while pred.right and pred.right != curr:
                pred = pred.right
            if not pred.right:
                pred.right = curr  # create thread
                curr = curr.left
            else:
                pred.right = None  # remove thread
                result.append(curr.val)
                curr = curr.right
    return result
```
**O(n) time, O(1) space.** Modifies tree temporarily. GATE loves asking about threaded binary trees — Morris traversal is the practical application.

---

## 3. Common Tree Patterns

### Pattern A: Height / Depth Computation
```python
def height(root):
    if not root:
        return -1  # or 0 depending on convention
    return 1 + max(height(root.left), height(root.right))
```

### Pattern B: Diameter (longest path between any two nodes)
```python
def diameter(root):
    ans = 0
    def height(node):
        nonlocal ans
        if not node:
            return 0
        left = height(node.left)
        right = height(node.right)
        ans = max(ans, left + right)  # path through this node
        return 1 + max(left, right)
    height(root)
    return ans
```

### Pattern C: Path Sum (root to leaf)
```python
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:  # leaf
        return root.val == target
    return has_path_sum(root.left, target - root.val) or \
           has_path_sum(root.right, target - root.val)
```

### Pattern D: Subtree as Return Value
Many tree problems follow this pattern: compute something for left and right subtrees, combine at the current node, and pass information up.
```python
# Example: check if balanced
def is_balanced(root):
    def check(node):
        if not node:
            return 0  # height
        left = check(node.left)
        right = check(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1  # -1 signals unbalanced
        return 1 + max(left, right)
    return check(root) != -1
```

### Pattern E: Construct Tree from Traversals
```python
# From preorder + inorder
def build_tree(preorder, inorder):
    if not preorder:
        return None
    root_val = preorder[0]
    root = TreeNode(root_val)
    mid = inorder.index(root_val)  # optimize with hashmap
    root.left = build_tree(preorder[1:mid+1], inorder[:mid])
    root.right = build_tree(preorder[mid+1:], inorder[mid+1:])
    return root
```
**Optimize:** Use a hashmap for inorder index lookup → O(n) total instead of O(n²).

### Pattern F: Serialize / Deserialize
```python
def serialize(root):
    if not root:
        return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"

def deserialize(data):
    vals = iter(data.split(","))
    def build():
        val = next(vals)
        if val == "null":
            return None
        node = TreeNode(int(val))
        node.left = build()
        node.right = build()
        return node
    return build()
```

---

## 4. BST (Binary Search Tree)

### Property
For every node: all values in left subtree < node.val < all values in right subtree.
**Inorder traversal of a BST gives sorted order.** This is the most important fact.

### Search: O(h)
```python
def search(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return search(root.left, val)
    return search(root.right, val)
```

### Insert: O(h)
```python
def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root
```

### Delete: O(h)
```python
def delete(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        # Node found
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        # Two children: replace with inorder successor
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root
```

### Kth Smallest in BST
```python
def kth_smallest(root, k):
    stack = []
    curr = root
    count = 0
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        count += 1
        if count == k:
            return curr.val
        curr = curr.right
```

### Validate BST
```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if root.val <= lo or root.val >= hi:
        return False
    return is_valid_bst(root.left, lo, root.val) and \
           is_valid_bst(root.right, root.val, hi)
```

---

## 5. Lowest Common Ancestor (LCA)

### LCA in Binary Tree (not BST)
```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root  # p and q are on different sides
    return left or right
```
**O(n) time, O(h) space.** This is the standard interview solution.

### LCA in BST
```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root  # split point
```
**O(h) time.** Exploits BST property.

### LCA with Binary Lifting (for trees with n > 10^5, multiple queries)
```python
LOG = 20  # log2(max_n)

def preprocess_lca(adj, root, n):
    depth = [0] * n
    up = [[0] * n for _ in range(LOG)]
    
    # BFS to set depth and parent
    visited = [False] * n
    queue = deque([root])
    visited[root] = True
    
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                depth[neighbor] = depth[node] + 1
                up[0][neighbor] = node
                queue.append(neighbor)
    
    # Fill sparse table
    for k in range(1, LOG):
        for v in range(n):
            up[k][v] = up[k-1][up[k-1][v]]
    
    return depth, up

def query_lca(u, v, depth, up):
    # Make u the deeper node
    if depth[u] < depth[v]:
        u, v = v, u
    
    # Lift u to same depth as v
    diff = depth[u] - depth[v]
    for k in range(LOG):
        if (diff >> k) & 1:
            u = up[k][u]
    
    if u == v:
        return u
    
    # Lift both until they meet
    for k in range(LOG - 1, -1, -1):
        if up[k][u] != up[k][v]:
            u = up[k][u]
            v = up[k][v]
    
    return up[0][u]
```
**Preprocessing:** O(n log n). **Each query:** O(log n). Use when you have many LCA queries on the same tree.

---

## 6. Important Tree Properties (GATE / Trivia)

- A binary tree with n nodes has exactly n+1 NULL pointers.
- Number of binary trees with n nodes = Catalan number = C(2n, n) / (n+1).
- In a full binary tree: leaves = internal nodes + 1.
- Inorder + Preorder uniquely determines a binary tree. Inorder + Postorder also works. Preorder + Postorder does NOT (ambiguous for nodes with one child).
- BST search, insert, delete are all O(h). For balanced BST, h = O(log n). For skewed BST, h = O(n).
- AVL tree: height difference of left and right subtrees ≤ 1 at every node. Guarantees h ≤ 1.44 log₂(n).
- Red-Black tree: h ≤ 2 log₂(n+1). Used in Java TreeMap, C++ std::map.

---

## 7. Edge Cases

- **Empty tree:** Always handle `root is None`.
- **Single node:** Leaf checks — `not root.left and not root.right`.
- **Skewed tree (linked list):** Recursion depth = n. Use iterative approaches or increase recursion limit.
- **Duplicate values in BST:** Convention varies — usually go right. Problem statement will specify.
- **Negative values:** Path sum problems can have negative nodes. Don't prune early.
- **LCA when one node is ancestor of the other:** The ancestor itself is the LCA.

---

## 8. LeetCode Problems

### Traversals & Basics
| # | Problem | Key Concept |
|---|---------|-------------|
| 94 | Binary Tree Inorder Traversal | Iterative inorder |
| 102 | Binary Tree Level Order Traversal | BFS level by level |
| 104 | Maximum Depth of Binary Tree | Basic recursion |
| 226 | Invert Binary Tree | Recursive swap |
| 101 | Symmetric Tree | Mirror check |
| 297 | Serialize and Deserialize Binary Tree | Preorder with null markers |

### Path & Subtree Problems
| # | Problem | Key Concept |
|---|---------|-------------|
| 112 | Path Sum | Root-to-leaf DFS |
| 113 | Path Sum II | DFS + backtracking to collect paths |
| 124 | Binary Tree Maximum Path Sum | Subtree return value pattern |
| 543 | Diameter of Binary Tree | Height computation + global max |
| 572 | Subtree of Another Tree | Subtree matching |
| 110 | Balanced Binary Tree | Height returns -1 for unbalanced |

### BST Problems
| # | Problem | Key Concept |
|---|---------|-------------|
| 98 | Validate Binary Search Tree | Min/max bounds recursion |
| 230 | Kth Smallest Element in BST | Inorder traversal |
| 235 | LCA of BST | BST split point |
| 108 | Convert Sorted Array to BST | Binary search on array |
| 450 | Delete Node in BST | Three cases — leaf, one child, two children |
| 700 | Search in BST | Basic BST search |

### LCA & Ancestors
| # | Problem | Key Concept |
|---|---------|-------------|
| 236 | LCA of Binary Tree | Standard LCA algorithm |
| 235 | LCA of BST | Exploit BST property |
| 1123 | LCA of Deepest Leaves | Modified LCA with depth |

### Construction & Conversion
| # | Problem | Key Concept |
|---|---------|-------------|
| 105 | Construct from Preorder + Inorder | Recursive build with hashmap |
| 106 | Construct from Inorder + Postorder | Similar — postorder gives root last |
| 114 | Flatten Binary Tree to Linked List | Preorder rewiring |

### Advanced
| # | Problem | Key Concept |
|---|---------|-------------|
| 199 | Binary Tree Right Side View | Level-order, take last per level |
| 437 | Path Sum III | Prefix sum on tree paths |
| 662 | Maximum Width of Binary Tree | Level-order with position indexing |
| 987 | Vertical Order Traversal | Column tracking with BFS |

### Study Order
**Phase 1 (2-3 days):** 94, 104, 226, 101, 102, 112
**Phase 2 (2-3 days):** 98, 230, 235, 700, 543, 110
**Phase 3 (2-3 days):** 236, 105, 124, 297, 199
**Phase 4 (2-3 days):** 437, 450, 662, 114, 987
