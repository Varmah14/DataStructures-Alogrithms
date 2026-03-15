# Prefix Sum + HashMap — Complete Guide

## 1. Core Idea

**Prefix sum** converts any range sum query `sum(arr[i..j])` into `prefix[j+1] - prefix[i]` in O(1).

**Combined with a HashMap**, it counts subarrays with sum == K in O(n): for each prefix[j], check how many earlier prefixes equal prefix[j] - K.

---

## 2. Templates

### Template 1: Basic Prefix Sum Array
```python
def build_prefix(nums):
    prefix = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        prefix[i + 1] = prefix[i] + nums[i]
    return prefix

# Range sum [i, j] inclusive
def range_sum(prefix, i, j):
    return prefix[j + 1] - prefix[i]
```

### Template 2: Subarray Sum Equals K
```python
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}  # empty prefix
    
    for num in nums:
        prefix += num
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    
    return count
```
**Why `{0: 1}`?** If `prefix == k`, the subarray from index 0 is valid. We need `prefix - k = 0` to exist in the map.

### Template 3: Prefix XOR + HashMap
```python
# Count subarrays with XOR == K
def count_xor_subarrays(nums, k):
    count = 0
    prefix_xor = 0
    seen = {0: 1}
    
    for num in nums:
        prefix_xor ^= num
        count += seen.get(prefix_xor ^ k, 0)
        seen[prefix_xor] = seen.get(prefix_xor, 0) + 1
    
    return count
```

### Template 4: Longest Subarray with Sum K (or balance == 0)
```python
# Longest subarray with sum == k
def max_length(nums, k):
    prefix = 0
    first_seen = {0: -1}  # store first occurrence of each prefix
    best = 0
    
    for i, num in enumerate(nums):
        prefix += num
        if prefix - k in first_seen:
            best = max(best, i - first_seen[prefix - k])
        if prefix not in first_seen:
            first_seen[prefix] = i  # only store first occurrence
    return best
```

### Template 5: Equal 0s and 1s (Balance Trick)
Convert 0 → -1, then find longest subarray with sum 0.
```python
def find_max_length(nums):
    prefix = 0
    first_seen = {0: -1}
    best = 0
    
    for i, num in enumerate(nums):
        prefix += 1 if num == 1 else -1
        if prefix in first_seen:
            best = max(best, i - first_seen[prefix])
        else:
            first_seen[prefix] = i
    return best
```

### Template 6: 2D Prefix Sum
```python
def build_2d_prefix(matrix):
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            prefix[i][j] = (matrix[i-1][j-1] + prefix[i-1][j] 
                           + prefix[i][j-1] - prefix[i-1][j-1])
    return prefix

# Sum of rectangle (r1,c1) to (r2,c2) inclusive
def region_sum(prefix, r1, c1, r2, c2):
    return (prefix[r2+1][c2+1] - prefix[r1][c2+1] 
            - prefix[r2+1][c1] + prefix[r1][c1])
```

### Template 7: Difference Array (Range Updates)
```python
# Add val to all elements in range [l, r]
def range_update(diff, l, r, val):
    diff[l] += val
    if r + 1 < len(diff):
        diff[r + 1] -= val

# Reconstruct array from difference array
def reconstruct(diff):
    result = [0] * len(diff)
    result[0] = diff[0]
    for i in range(1, len(diff)):
        result[i] = result[i-1] + diff[i]
    return result
```

---

## 3. Key Insight: Prefix Sum + HashMap Duality

| Problem | Transform | HashMap Key | HashMap Value |
|---|---|---|---|
| Subarray sum == K | prefix sum | prefix - K | count of occurrences |
| Subarray XOR == K | prefix XOR | prefix ^ K | count |
| Longest with sum K | prefix sum | prefix - K | first index |
| Equal 0s and 1s | 0 → -1, prefix sum | prefix | first index |
| Divisible by K | prefix sum mod K | prefix % K | count |

---

## 4. Edge Cases

- **Empty array** — return 0.
- **Initialize HashMap with `{0: 1}`** for count problems or `{0: -1}` for length problems. Forgetting this is the #1 bug.
- **Negative numbers** — prefix sum still works, but sliding window doesn't. This is why prefix+hash is essential.
- **Modular arithmetic** — for "divisible by K", use `prefix % K`. Handle negative mod: `((prefix % K) + K) % K` in languages with negative modulo.
- **Overflow** — prefix sums can overflow in languages with fixed-size ints.

---

## 5. LeetCode Problems

### Core Prefix Sum + HashMap
| # | Problem | Key Concept |
|---|---------|-------------|
| 560 | Subarray Sum Equals K | The canonical problem |
| 974 | Subarray Sums Divisible by K | Prefix mod K |
| 525 | Contiguous Array | 0→-1, longest with sum 0 |
| 523 | Continuous Subarray Sum | Prefix mod K, length ≥ 2 |
| 1 | Two Sum | HashMap for complement (not prefix, but same pattern) |

### Prefix Sum Applications
| # | Problem | Key Concept |
|---|---------|-------------|
| 303 | Range Sum Query - Immutable | Basic prefix sum |
| 304 | Range Sum Query 2D - Immutable | 2D prefix sum |
| 238 | Product of Array Except Self | Prefix and suffix products |
| 1480 | Running Sum of 1d Array | Direct prefix sum |

### Advanced
| # | Problem | Key Concept |
|---|---------|-------------|
| 930 | Binary Subarrays With Sum | Prefix sum + count (also sliding window) |
| 1248 | Count Number of Nice Subarrays | Transform + prefix sum |
| 1109 | Corporate Flight Bookings | Difference array |
| 370 | Range Addition | Difference array |

### Study Order
**Phase 1 (2 days):** 303, 1480, 560, 1
**Phase 2 (2-3 days):** 525, 974, 523, 238
**Phase 3 (2-3 days):** 304, 930, 1109, 1248
