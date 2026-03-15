# Backtracking / Search with Pruning — Complete Guide

## 1. Core Idea

Backtracking = DFS through the decision space, building a solution incrementally. At each step:
1. **Choose** — make a decision (add an element to the current path).
2. **Explore** — recurse with the updated state.
3. **Unchoose** — undo the decision and try the next option.

If the current partial solution violates constraints, **prune** — don't recurse further.

**Time complexity** is usually exponential (O(2^n), O(n!), O(k^n)), but pruning makes it practical.

---

## 2. Master Template

```python
def backtrack(state, choices, result, path):
    if is_goal(state):
        result.append(path[:])  # copy the current path
        return
    
    for choice in choices:
        if not is_valid(choice, state):
            continue  # prune
        
        path.append(choice)         # choose
        make_move(state, choice)
        
        backtrack(state, next_choices, result, path)  # explore
        
        path.pop()                  # unchoose
        undo_move(state, choice)
```

**Critical:** Always copy the path (`path[:]` or `list(path)`) when adding to result. Otherwise all entries point to the same mutated list.

---

## 3. Pattern Templates

### Pattern A: Subsets (Power Set)
Generate all 2^n subsets.
```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])  # every partial path is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1: don't reuse elements
            path.pop()
    
    backtrack(0, [])
    return result
```

### Pattern B: Subsets with Duplicates
```python
def subsets_with_dup(nums):
    nums.sort()  # sort to group duplicates
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue  # skip duplicate at same level
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result
```
**Key:** `i > start` (not `i > 0`). This ensures we skip duplicates only at the same recursion level, not across levels.

### Pattern C: Permutations
```python
def permutations(nums):
    result = []
    
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    
    backtrack([], [False] * len(nums))
    return result
```

### Pattern D: Permutations with Duplicates
```python
def permute_unique(nums):
    nums.sort()
    result = []
    
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: same value as previous, and previous wasn't used at this level
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    
    backtrack([], [False] * len(nums))
    return result
```

### Pattern E: Combination Sum (reuse allowed)
```python
def combination_sum(candidates, target):
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i, not i+1 (reuse)
            path.pop()
    
    backtrack(0, [], target)
    return result
```

### Pattern F: Combination Sum (no reuse, with duplicates)
```python
def combination_sum2(candidates, target):
    candidates.sort()
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # prune: sorted, so all future candidates too large
            if i > start and candidates[i] == candidates[i-1]:
                continue  # skip duplicates at same level
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result
```

### Pattern G: Grid Search (Word Search)
```python
def word_search(board, word):
    rows, cols = len(board), len(board[0])
    
    def backtrack(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False
        
        temp = board[r][c]
        board[r][c] = '#'  # mark visited
        
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                return True
        
        board[r][c] = temp  # unmark
        return False
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

### Pattern H: N-Queens
```python
def solve_n_queens(n):
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    board = [['.' * n] for _ in range(n)]
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row] = list('.' * n)
            board[row][col] = 'Q'
            
            backtrack(row + 1)
            
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    backtrack(0)
    return result
```

---

## 4. Pruning Techniques

1. **Sort + early termination:** If candidates are sorted and current exceeds target, break.
2. **Skip duplicates:** `if i > start and nums[i] == nums[i-1]: continue`
3. **Constraint sets:** N-Queens uses sets for O(1) conflict check.
4. **Bound checking:** If remaining capacity < 0 or remaining elements insufficient, prune.
5. **Symmetry breaking:** If problem has symmetry (e.g., first queen can only be in first half of row), reduce search space.

---

## 5. Subsets vs Permutations vs Combinations — Quick Reference

| Type | Elements | Order | Reuse | Template Key |
|---|---|---|---|---|
| Subsets | Choose any | Doesn't matter | No | `start` parameter, collect at every node |
| Combinations (k) | Choose k | Doesn't matter | No | `start` parameter, collect at len == k |
| Permutations | Choose all | Matters | No | `used` array, no `start` |
| Combination Sum | Choose to target | Doesn't matter | Yes | `start` parameter, `backtrack(i, ...)` |

---

## 6. Edge Cases & Pitfalls

- **Forgetting to copy path:** `result.append(path[:])` not `result.append(path)`.
- **Duplicate handling:** Must sort first. The `i > start` check only works on sorted input.
- **Permutation duplicate pruning:** The condition `not used[i-1]` is counterintuitive. It ensures we only use the first occurrence of a duplicate at each position.
- **Grid backtracking:** Remember to unmark visited cells. Use in-place marking (set to '#') to avoid copying visited arrays.
- **Recursion depth:** For n = 20+ with permutations, n! is enormous. Pruning is essential.
- **Empty input:** Handle nums = [] — usually return [[]] for subsets, [] for permutations.

---

## 7. LeetCode Problems

### Subsets / Combinations
| # | Problem | Key Concept |
|---|---------|-------------|
| 78 | Subsets | Basic subset generation |
| 90 | Subsets II | Duplicates — sort + skip |
| 77 | Combinations | Choose k from n |
| 39 | Combination Sum | Reuse allowed |
| 40 | Combination Sum II | No reuse + duplicates |
| 216 | Combination Sum III | k numbers that sum to n |

### Permutations
| # | Problem | Key Concept |
|---|---------|-------------|
| 46 | Permutations | Basic permutation |
| 47 | Permutations II | Duplicates — used array trick |
| 31 | Next Permutation | Not backtracking but important pattern |

### Grid / String Search
| # | Problem | Key Concept |
|---|---------|-------------|
| 79 | Word Search | Grid backtracking |
| 212 | Word Search II | Grid + Trie (advanced) |
| 17 | Letter Combinations of a Phone Number | Digit to letters mapping |
| 22 | Generate Parentheses | Open/close count constraint |

### Classic Constraint Problems
| # | Problem | Key Concept |
|---|---------|-------------|
| 51 | N-Queens | Row-by-row with constraint sets |
| 52 | N-Queens II | Count solutions only |
| 37 | Sudoku Solver | Row/col/box constraint sets |
| 131 | Palindrome Partitioning | Partition string into palindromes |

### Advanced
| # | Problem | Key Concept |
|---|---------|-------------|
| 93 | Restore IP Addresses | Partition with validation |
| 698 | Partition to K Equal Sum Subsets | Bitmask or backtracking with pruning |
| 473 | Matchsticks to Square | Partition into 4 equal sides |
| 140 | Word Break II | Backtracking with memo |

### Study Order
**Phase 1 (2-3 days):** 78, 90, 46, 47, 77
**Phase 2 (2-3 days):** 39, 40, 17, 22, 216
**Phase 3 (2-3 days):** 79, 131, 51, 93
**Phase 4 (2-3 days):** 212, 37, 698, 140
