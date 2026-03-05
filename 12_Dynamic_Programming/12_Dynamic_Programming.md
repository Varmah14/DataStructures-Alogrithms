# Dynamic Programming (Fundamentals)

> **Interview Focus**: FAANG + Mid-tier | Pattern-depth over breadth

---

## What Interviewers Actually Test Here

DP is the hardest topic to fake. Interviewers test:

- Can you **identify** that a problem has overlapping subproblems and optimal substructure — without being told?
- Can you **define the state** clearly before writing any code?
- Do you know when to use **memoization (top-down)** vs **tabulation (bottom-up)** and why?
- Can you **optimize space** from O(n²) → O(n) when the recurrence only looks back a fixed number of steps?

The most common failure: jumping to code before defining `dp[i]` precisely. Always state your DP definition out loud first.

---

## Core Concepts

### The Two Prerequisites for DP

**Overlapping subproblems**: the same subproblem is solved multiple times in a naive recursive solution. Memoization eliminates this redundancy.

**Optimal substructure**: the optimal solution to the whole problem can be built from optimal solutions to subproblems. (Contrast: shortest path has this; longest path in a general graph does not.)

### Top-Down (Memoization) vs Bottom-Up (Tabulation)

```python
# Top-Down — recursive + cache
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(i):
    # base case
    if i <= 1: return i
    # recurrence
    return dp(i-1) + dp(i-2)
```

```python
# Bottom-Up — iterative + table
def dp_table(n):
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i-1] + table[i-2]
    return table[n]
```

| | Top-Down | Bottom-Up |
|---|---|---|
| Intuition | Easier — follows recursion naturally | Requires knowing order of computation |
| Stack overflow risk | Yes (deep recursion) | No |
| Only compute needed states | Yes | No (computes all states) |
| Space optimization | Harder | Easy (just keep last k rows) |
| Interview preference | Fine for derivation | Preferred for final solution |

**Strategy**: derive top-down first to understand the recurrence, then convert to bottom-up for the final answer.

---

## The 6 DP Families

---

### Family 1 — Linear DP (1D)

**State**: `dp[i]` = answer for first `i` elements.

**Climbing Stairs / Fibonacci**:
```python
dp[i] = dp[i-1] + dp[i-2]
```

**House Robber** — can't take adjacent:
```python
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
# Space optimized:
prev2, prev1 = 0, 0
for n in nums:
    prev2, prev1 = prev1, max(prev1, prev2 + n)
return prev1
```

**Interview tip**: whenever `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, reduce to two variables. Interviewers expect this optimization.

---

### Family 2 — Knapsack

**0/1 Knapsack**: each item used at most once.

```
dp[i][w] = max value using first i items with capacity w

dp[i][w] = max(dp[i-1][w],              # skip item i
               dp[i-1][w - weight[i]] + value[i])   # take item i
```

```python
# Space-optimized: iterate w in REVERSE to avoid using item twice
dp = [0] * (W + 1)
for weight, value in items:
    for w in range(W, weight - 1, -1):   # reverse!
        dp[w] = max(dp[w], dp[w - weight] + value)
```

**Unbounded Knapsack** (item can be used unlimited times — Coin Change):

```python
# Iterate w FORWARD — allows reuse of same item
dp = [float('inf')] * (amount + 1)
dp[0] = 0
for coin in coins:
    for w in range(coin, amount + 1):    # forward!
        dp[w] = min(dp[w], dp[w - coin] + 1)
```

**The key**: 0/1 = reverse inner loop. Unbounded = forward inner loop. This single distinction covers a huge class of problems.

---

### Family 3 — LIS (Longest Increasing Subsequence)

**State**: `dp[i]` = length of LIS ending at index `i`.

```python
# O(n²) — interview-acceptable, easy to explain
def lis(nums):
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

```python
# O(n log n) — via patience sorting + binary search
import bisect
def lis_fast(nums):
    tails = []
    for n in nums:
        pos = bisect.bisect_left(tails, n)
        if pos == len(tails):
            tails.append(n)
        else:
            tails[pos] = n
    return len(tails)
```

`tails[i]` = smallest tail of all increasing subsequences of length `i+1`. The array stays sorted, enabling binary search. Note: `tails` itself is **not** the LIS — only its length is correct.

---

### Family 4 — LCS / Edit Distance (2D DP on Two Sequences)

**State**: `dp[i][j]` = answer for `s1[:i]` and `s2[:j]`.

**LCS (Longest Common Subsequence)**:

```python
dp = [[0] * (n+1) for _ in range(m+1)]
for i in range(1, m+1):
    for j in range(1, n+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Edit Distance**:

```python
dp = [[0] * (n+1) for _ in range(m+1)]
for i in range(m+1): dp[i][0] = i    # delete all of s1
for j in range(n+1): dp[0][j] = j    # insert all of s2
for i in range(1, m+1):
    for j in range(1, n+1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1]
        else:
            dp[i][j] = 1 + min(dp[i-1][j],    # delete
                                dp[i][j-1],    # insert
                                dp[i-1][j-1])  # replace
```

**Initialization matters**: base cases represent empty prefix operations.

---

### Family 5 — Grid DP

**State**: `dp[r][c]` = answer to reach cell `(r, c)`.

```python
# Unique paths
dp = [[1]*n for _ in range(m)]   # base: top row + left col = 1 way each
for r in range(1, m):
    for c in range(1, n):
        dp[r][c] = dp[r-1][c] + dp[r][c-1]
```

**Min path sum** — same structure, `min` instead of sum.

**Space optimization**: since `dp[r][c]` only depends on row `r-1` and column `c-1`, you can reduce to a 1D array (rolling row).

---

### Family 6 — Interval DP

**State**: `dp[i][j]` = answer for subarray/substring `[i..j]`.

**Fill order**: increasing length (outer loop = length, inner = start).

```python
# Burst Balloons
dp = [[0]*(n+2) for _ in range(n+2)]
for length in range(1, n+1):           # increasing length
    for left in range(1, n-length+2):
        right = left + length - 1
        for k in range(left, right+1): # which balloon to burst last
            dp[left][right] = max(dp[left][right],
                nums[left-1] * nums[k] * nums[right+1] +
                dp[left][k-1] + dp[k+1][right])
```

**Key**: the "last action" trick — instead of first balloon burst, think about **which is the last** to burst. This makes the subproblems independent.

---

## State Definition — The Most Important Skill

Before writing any code, define your state explicitly:

> "`dp[i]` represents _____ considering the first `i` elements."

> "`dp[i][j]` represents _____ when we've processed `s1[:i]` and `s2[:j]`."

> "`dp[i][j]` represents the minimum cost for the subarray from index `i` to `j`."

If you can't fill in the blank clearly, you don't understand the DP yet. Do not write code until you can.

---

## How to Identify DP in an Interview

Ask yourself:
1. Does the problem ask for **min/max, count, or true/false** over some choices?
2. Can I make a choice at each step that affects future choices?
3. Does a brute-force recursive solution repeat the same subproblems?

If yes to all three → DP.

**Not DP**: greedy (when local optimal = global optimal, no overlapping subproblems).

---

## Space Optimization Patterns

| Recurrence depends on | Optimization |
|---|---|
| Only `dp[i-1]` | Two variables: `prev, curr` |
| Only `dp[i-1]` and `dp[i-2]` | Three variables |
| Entire previous row `dp[i-1][*]` | 1D rolling array |
| `dp[i-1][j-1]`, `dp[i-1][j]`, `dp[i][j-1]` | 1D array, careful update order |

---

## Complexity Reference

| Family | Time | Space | Optimized Space |
|---|---|---|---|
| 1D Linear | O(n) | O(n) | O(1) |
| 0/1 Knapsack | O(nW) | O(nW) | O(W) |
| LIS O(n²) | O(n²) | O(n) | — |
| LIS O(n log n) | O(n log n) | O(n) | — |
| LCS / Edit Distance | O(mn) | O(mn) | O(min(m,n)) |
| Grid DP | O(mn) | O(mn) | O(n) |
| Interval DP | O(n³) | O(n²) | — |

---

## Common Interview Traps

| Trap | Fix |
|---|---|
| Not defining `dp[i]` precisely before coding | State the definition aloud — don't skip this |
| Off-by-one in base cases | Trace through smallest inputs by hand |
| 0/1 knapsack: iterating inner loop forward (allows reuse) | Inner loop must go **reverse** for 0/1 |
| LIS: treating `tails` array as the actual subsequence | Only `len(tails)` is correct, not `tails` itself |
| Interval DP: wrong fill order | Always fill by **increasing length** |
| Edit distance: forgetting to initialize base cases | First row = `j`, first col = `i` |

---

## The 18 Problems — Pattern-Mapped

### Family 1 — Linear DP

| # | Problem | Why it's here |
|---|---|---|
| 70 | Climbing Stairs | Fibonacci DP — the warmup |
| 198 | House Robber | Skip-adjacent decision |
| 213 | House Robber II | Circular array — run twice |
| 152 | Maximum Product Subarray | Track both max and min (negatives flip) |

### Family 2 — Knapsack

| # | Problem | Why it's here |
|---|---|---|
| 416 | Partition Equal Subset Sum | 0/1 knapsack — target = sum/2 |
| 494 | Target Sum | Count ways — 0/1 knapsack variant |
| 322 | Coin Change | Unbounded knapsack — min coins |
| 518 | Coin Change II | Unbounded — count ways |

### Family 3 — LIS

| # | Problem | Why it's here |
|---|---|---|
| 300 | Longest Increasing Subsequence | The canonical problem — know O(n²) and O(n log n) |
| 354 | Russian Doll Envelopes | 2D LIS — sort by one dim, LIS on other |
| 368 | Largest Divisible Subset | LIS with divisibility condition |

### Family 4 — LCS / Edit Distance

| # | Problem | Why it's here |
|---|---|---|
| 1143 | Longest Common Subsequence | The base pattern |
| 72 | Edit Distance | Classic — must know cold |
| 115 | Distinct Subsequences | Count ways — harder LCS variant |

### Family 5 — Grid DP

| # | Problem | Why it's here |
|---|---|---|
| 62 | Unique Paths | Grid DP base |
| 64 | Minimum Path Sum | Same structure, min cost |
| 221 | Maximal Square | `dp[r][c] = min(up, left, diag) + 1` — elegant |

### Family 6 — Interval DP

| # | Problem | Why it's here |
|---|---|---|
| 647 | Palindromic Substrings | Count all palindromes — expand or DP |
| 5 | Longest Palindromic Substring | Interval DP or Manacher's |
| 312 | Burst Balloons | Hardest interval DP — "last burst" trick |

---

## 6-Day Execution Plan

```
Day 1 — Linear DP:       70, 198, 213, 152
Day 2 — Knapsack:        416, 494, 322, 518  ← drill forward vs reverse loop
Day 3 — LIS:             300, 354, 368
Day 4 — LCS/Edit:        1143, 72, 115
Day 5 — Grid + Interval: 62, 64, 221, 647, 5
Day 6 — Hard + Review:   312, redo 2 problems you were unsure on
                         Practice: state definition cold for 5 random problems
```

---

## Quick Reference

```
DP triggers:
  ✓ min/max over choices
  ✓ count number of ways
  ✓ true/false feasibility
  ✓ recursive brute force has repeated subproblems

State definition ritual:
  "dp[i] represents ___ for the first i elements"
  Write this before any code.

Family cheatsheet:
  Linear:      dp[i] = f(dp[i-1], dp[i-2])
  Knapsack:    dp[w] — reverse loop (0/1), forward loop (unbounded)
  LIS:         dp[i] = max(dp[j]+1) for j<i where nums[j]<nums[i]
  LCS:         dp[i][j] = dp[i-1][j-1]+1 (match) or max(dp[i-1][j], dp[i][j-1])
  Grid:        dp[r][c] = dp[r-1][c] + dp[r][c-1]
  Interval:    fill by increasing length; pick last action

Space optimization:
  Only uses dp[i-1] → two variables
  Only uses previous row → 1D rolling array
```
