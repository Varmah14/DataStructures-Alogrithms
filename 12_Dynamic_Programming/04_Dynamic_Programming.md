# Dynamic Programming — Complete Guide

## 1. When Is It DP?

Two conditions:
1. **Optimal substructure:** optimal solution contains optimal solutions to subproblems.
2. **Overlapping subproblems:** same subproblems are solved multiple times.

**Triggers in problem statements:** "minimum cost", "maximum profit", "number of ways", "is it possible", "longest/shortest subsequence", "partition into groups with constraint."

**Not DP if:** greedy gives optimal (no overlapping), or brute force is already polynomial.

---

## 2. Top-Down (Memoization) vs Bottom-Up (Tabulation)

### Top-Down
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(state):
    if base_case:
        return base_value
    return recurrence(dp(sub_states))
```
**Pros:** Only computes reachable states, natural recursive thinking.
**Cons:** Recursion overhead, stack depth limits.

### Bottom-Up
```python
dp = [base_values]
for state in order:
    dp[state] = recurrence(dp[sub_states])
return dp[final_state]
```
**Pros:** No recursion overhead, can optimize space.
**Cons:** Must determine correct iteration order.

**Interview tip:** Start with top-down (easier to get right), then convert to bottom-up if needed for optimization.

---

## 3. DP Families

### Family 1: 0/1 Knapsack
**Setup:** n items with weight and value. Capacity W. Maximize value.

```python
# Top-Down
@lru_cache(maxsize=None)
def knapsack(i, remaining):
    if i == n or remaining == 0:
        return 0
    # Don't take item i
    result = knapsack(i + 1, remaining)
    # Take item i (if it fits)
    if weights[i] <= remaining:
        result = max(result, values[i] + knapsack(i + 1, remaining - weights[i]))
    return result

# Bottom-Up
dp = [0] * (W + 1)
for i in range(n):
    for w in range(W, weights[i] - 1, -1):  # reverse to avoid reusing item
        dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
```
**Space optimization:** 1D array, iterate capacity in reverse.

**Variants:**
- Unbounded knapsack → iterate capacity forward (can reuse items)
- Subset sum → dp[j] = dp[j] or dp[j - nums[i]]
- Count of subsets with sum = target → dp[j] += dp[j - nums[i]]
- Partition equal subset sum → subset sum to total/2

### Family 2: Coin Change / Unbounded Knapsack
```python
# Minimum coins to make amount
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# Number of ways to make amount (combinations, not permutations)
def coin_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:       # coins in outer loop → combinations
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]
    return dp[amount]

# If permutations (order matters): swap loops
def coin_permutations(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for x in range(1, amount + 1):   # amount in outer loop → permutations
        for coin in coins:
            if x >= coin:
                dp[x] += dp[x - coin]
    return dp[amount]
```

### Family 3: Longest Increasing Subsequence (LIS)
```python
# O(n²) DP
def lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n) with patience sorting
import bisect
def lis_fast(nums):
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```
**Key insight for O(n log n):** `tails[i]` is the smallest tail element of all increasing subsequences of length i+1. Binary search to find where each element fits.

### Family 4: LCS / Edit Distance (Two-Sequence DP)
```python
# Longest Common Subsequence
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Edit Distance (Levenshtein)
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # delete
                                    dp[i][j-1],    # insert
                                    dp[i-1][j-1])  # replace
    return dp[m][n]
```
**Space optimization:** Both can be done with 2 rows (or even 1 row + variable for LCS).

### Family 5: Grid DP
```python
# Unique paths
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

# Minimum path sum
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]
            elif j == 0:
                grid[i][j] += grid[i-1][j]
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
    return grid[m-1][n-1]
```

### Family 6: Interval DP
```python
# Matrix Chain Multiplication / Burst Balloons style
# dp[i][j] = optimal for subarray i..j
for length in range(2, n + 1):       # subarray length
    for i in range(n - length + 1):
        j = i + length - 1
        for k in range(i, j):         # split point
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i, k, j))
```

### Family 7: Bitmask DP
```python
# State = bitmask representing which items are used
# dp[mask] = optimal value using the set of items in mask
dp = [float('inf')] * (1 << n)
dp[0] = 0

for mask in range(1 << n):
    for i in range(n):
        if not (mask & (1 << i)):  # item i not yet used
            new_mask = mask | (1 << i)
            dp[new_mask] = min(dp[new_mask], dp[mask] + cost(mask, i))
```
**Use when n ≤ 20.** State space is 2^n.

### Family 8: State Machine DP
```python
# Stock trading with cooldown / transaction limits
# States: holding, not_holding, cooldown
hold = -prices[0]
not_hold = 0
cooldown = 0

for i in range(1, n):
    new_hold = max(hold, not_hold - prices[i])
    new_not_hold = max(not_hold, cooldown)
    new_cooldown = hold + prices[i]
    hold, not_hold, cooldown = new_hold, new_not_hold, new_cooldown

return max(not_hold, cooldown)
```

---

## 4. Space Optimization Techniques

1. **Rolling array:** If dp[i] only depends on dp[i-1], keep only 2 rows.
2. **1D compression:** If dp[i][j] depends on dp[i-1][j] and dp[i][j-1], a single 1D array works (iterate j forward or backward depending on dependency).
3. **Variable optimization:** If only a few previous values needed (Fibonacci, stock problems), use variables.

---

## 5. How to Approach a DP Problem

1. **Identify it's DP:** overlapping subproblems + optimal substructure.
2. **Define state:** What uniquely describes a subproblem? (index, remaining capacity, bitmask, etc.)
3. **Define recurrence:** How does the answer for this state relate to smaller states?
4. **Define base cases:** Smallest subproblems with known answers.
5. **Define answer:** Which state(s) give the final answer?
6. **Implement top-down first** (memo), then convert to bottom-up if needed.
7. **Optimize space** if possible.

---

## 6. Complexity Analysis

- **Time = number of states × work per state.**
- Knapsack: O(n × W) states × O(1) per state = O(nW). This is **pseudopolynomial** (polynomial in W, but W can be exponential in input size).
- LCS: O(m × n).
- Bitmask DP: O(2^n × n).
- Interval DP: O(n³).
- LIS (binary search): O(n log n).

---

## 7. Edge Cases & Pitfalls

- **Empty input:** Handle n = 0 or empty array.
- **Single element:** Often the base case itself is the answer.
- **Negative numbers:** Affects min/max — can't assume adding elements increases sum.
- **Integer overflow:** In "number of ways" problems, use modulo (usually 10^9 + 7).
- **0-indexed vs 1-indexed DP tables:** 1-indexed often cleaner for string/sequence DP (row/col 0 = empty prefix).
- **Top-down recursion depth:** Python limit = 1000. Set `sys.setrecursionlimit()` or convert to bottom-up.
- **Combinations vs permutations:** Coin change — outer loop over coins = combinations, outer loop over amounts = permutations.

---

## 8. LeetCode Problems

### 1D DP (Warm-Up)
| # | Problem | Key Concept |
|---|---------|-------------|
| 70 | Climbing Stairs | Fibonacci — dp[i] = dp[i-1] + dp[i-2] |
| 198 | House Robber | Take or skip — dp[i] = max(dp[i-1], dp[i-2] + nums[i]) |
| 213 | House Robber II | Circular — run twice excluding first/last |
| 139 | Word Break | dp[i] = any dp[j] where s[j:i] in wordDict |
| 300 | Longest Increasing Subsequence | Classic LIS |
| 152 | Maximum Product Subarray | Track both max and min (negatives flip) |

### Knapsack Family
| # | Problem | Key Concept |
|---|---------|-------------|
| 416 | Partition Equal Subset Sum | Subset sum to total/2 |
| 494 | Target Sum | Count subsets with sum = (total + target) / 2 |
| 322 | Coin Change | Minimum coins — unbounded knapsack |
| 518 | Coin Change II | Count combinations — unbounded knapsack |
| 474 | Ones and Zeroes | 2D knapsack (zeros and ones as two capacities) |

### Two-Sequence DP
| # | Problem | Key Concept |
|---|---------|-------------|
| 1143 | Longest Common Subsequence | Classic LCS |
| 72 | Edit Distance | Insert/delete/replace |
| 97 | Interleaving String | dp[i][j] = can we form s3[:i+j] from s1[:i] and s2[:j] |
| 115 | Distinct Subsequences | Count ways s matches subsequence of t |

### Grid DP
| # | Problem | Key Concept |
|---|---------|-------------|
| 62 | Unique Paths | Count paths top-left to bottom-right |
| 64 | Minimum Path Sum | Grid min cost |
| 221 | Maximal Square | dp[i][j] = side length of largest square ending at (i,j) |
| 85 | Maximal Rectangle | Histogram DP per row (combines with monotonic stack) |

### Interval / String DP
| # | Problem | Key Concept |
|---|---------|-------------|
| 516 | Longest Palindromic Subsequence | Interval DP or reverse + LCS |
| 312 | Burst Balloons | Interval DP — last balloon to burst in range |
| 647 | Palindromic Substrings | Expand around center or interval DP |
| 5 | Longest Palindromic Substring | Expand around center (O(n²)) or Manacher |

### Stock Problems (State Machine DP)
| # | Problem | Key Concept |
|---|---------|-------------|
| 121 | Best Time to Buy and Sell Stock | One transaction — track min so far |
| 122 | Best Time to Buy and Sell Stock II | Unlimited — take all upswings |
| 309 | Best Time with Cooldown | 3 states: hold, sold, rest |
| 188 | Best Time with K Transactions | dp[k][i] with state machine |

### Advanced DP
| # | Problem | Key Concept |
|---|---------|-------------|
| 1049 | Last Stone Weight II | Partition into two groups, minimize diff |
| 377 | Combination Sum IV | Permutation count (amounts outer loop) |
| 279 | Perfect Squares | BFS or coin change variant |
| 691 | Stickers to Spell Word | Bitmask DP |
| 10 | Regular Expression Matching | 2D DP on pattern + string |

### Study Order
**Phase 1 (3-4 days):** 70, 198, 213, 322, 518, 300
**Phase 2 (3-4 days):** 416, 494, 1143, 72, 62, 64
**Phase 3 (3-4 days):** 139, 152, 221, 5, 647, 121, 309
**Phase 4 (3-4 days):** 312, 516, 85, 188, 10, 691
