# Binary Search — Complete Guide

## 1. Core Idea

Binary search works on any **monotonic** predicate. If you can define a function `ok(x)` that flips from False to True (or True to False) at some boundary, you can binary search for that boundary.

**Not just for sorted arrays.** Binary search on the answer space is arguably more common in interviews than searching in an array.

---

## 2. Templates

### Template 1: Standard Search (find exact value)
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1  # not found
```

### Template 2: Find Leftmost (first True / lower bound)
"Find smallest index where condition is true."
```python
def first_true(lo, hi, condition):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if condition(mid):
            hi = mid       # mid might be the answer, search left
        else:
            lo = mid + 1   # mid is definitely not, search right
    return lo  # lo == hi == first position where condition is true
```
Equivalent to `bisect_left` for sorted arrays.

### Template 3: Find Rightmost (last True / upper bound)
"Find largest index where condition is true."
```python
def last_true(lo, hi, condition):
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # ceiling division to avoid infinite loop
        if condition(mid):
            lo = mid       # mid might be the answer, search right
        else:
            hi = mid - 1   # mid is definitely not, search left
    return lo  # lo == hi == last position where condition is true
```

### Template 4: Binary Search on Answer
"Find the minimum value x such that ok(x) is true."
```python
def binary_search_on_answer(lo, hi, feasible):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**"Minimize the maximum"** → binary search on the answer (the maximum value). Check if you can achieve that max. Search for smallest feasible max.

**"Maximize the minimum"** → binary search on the answer (the minimum value). Check if you can achieve that min. Search for largest feasible min.

---

## 3. Python bisect Module

```python
import bisect

# bisect_left: leftmost position to insert val (first index >= val)
idx = bisect.bisect_left(arr, val)

# bisect_right: rightmost position to insert val (first index > val)
idx = bisect.bisect_right(arr, val)

# insort: insert maintaining sorted order
bisect.insort_left(arr, val)

# Find exact match
def search(arr, val):
    idx = bisect.bisect_left(arr, val)
    if idx < len(arr) and arr[idx] == val:
        return idx
    return -1

# Count occurrences of val
def count(arr, val):
    return bisect.bisect_right(arr, val) - bisect.bisect_left(arr, val)

# First element >= val
def lower_bound(arr, val):
    return bisect.bisect_left(arr, val)

# First element > val
def upper_bound(arr, val):
    return bisect.bisect_right(arr, val)
```

---

## 4. Key Patterns

### Pattern A: Search in Sorted Array Variants
```python
# First and last position of target (LC 34)
def search_range(nums, target):
    left = bisect.bisect_left(nums, target)
    right = bisect.bisect_right(nums, target) - 1
    if left <= right and left < len(nums) and nums[left] == target:
        return [left, right]
    return [-1, -1]
```

### Pattern B: Search in Rotated Sorted Array
```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

### Pattern C: Binary Search on Answer — Minimize Maximum
```python
# Split array into k subarrays, minimize the largest sum (LC 410)
def split_array(nums, k):
    def feasible(max_sum):
        count, curr = 1, 0
        for num in nums:
            curr += num
            if curr > max_sum:
                count += 1
                curr = num
        return count <= k
    
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Pattern D: Binary Search on Answer — Maximize Minimum
```python
# Place k balls in positions, maximize minimum distance (LC 1552)
def max_distance(positions, k):
    positions.sort()
    
    def feasible(min_dist):
        count, last = 1, positions[0]
        for pos in positions[1:]:
            if pos - last >= min_dist:
                count += 1
                last = pos
        return count >= k
    
    lo, hi = 1, positions[-1] - positions[0]
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # ceiling — searching for last true
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
```

### Pattern E: Kth Element via Binary Search
```python
# Kth smallest in two sorted arrays / matrix
# Binary search on value, count elements <= mid
def kth_smallest_matrix(matrix, k):
    n = len(matrix)
    lo, hi = matrix[0][0], matrix[n-1][n-1]
    
    while lo < hi:
        mid = lo + (hi - lo) // 2
        count = count_le(matrix, mid, n)
        if count < k:
            lo = mid + 1
        else:
            hi = mid
    return lo

def count_le(matrix, mid, n):
    count = 0
    row, col = n - 1, 0
    while row >= 0 and col < n:
        if matrix[row][col] <= mid:
            count += row + 1
            col += 1
        else:
            row -= 1
    return count
```

### Pattern F: Binary Search on Floating Point
```python
def sqrt_float(x, eps=1e-9):
    lo, hi = 0, max(1, x)
    while hi - lo > eps:
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid
    return lo
```
**Or use fixed iterations:** `for _ in range(100)` instead of epsilon check. 100 iterations gives ~10^-30 precision.

---

## 5. Common Pitfalls

- **Infinite loop with `lo < hi` and `mid = (lo + hi) // 2` when `lo = mid`:** Happens when searching for rightmost. Use ceiling: `mid = lo + (hi - lo + 1) // 2`.
- **Off-by-one in bounds:** `lo = 0, hi = n-1` (inclusive) vs `lo = 0, hi = n` (exclusive). Be consistent.
- **Integer overflow for mid:** `mid = lo + (hi - lo) // 2` is safe. `mid = (lo + hi) // 2` can overflow in other languages.
- **Forgetting edge cases:** Array of size 0 or 1. Target smaller than all or larger than all.
- **Rotated array with duplicates:** Worst case becomes O(n) when duplicates obscure which half is sorted. Handle `nums[lo] == nums[mid]` with `lo += 1`.

---

## 6. Binary Search Identification

**Clues in problem statement:**
- "minimize the maximum" / "maximize the minimum"
- "minimum speed/capacity/time such that..."
- "kth smallest/largest"
- "can you do X within Y?"
- Sorted array/matrix
- Monotonic condition

**Constraint clues:**
- n ≈ 10^5 and need better than O(n²) → binary search
- Answer range is large but checkable → binary search on answer

---

## 7. LeetCode Problems

### Standard Binary Search
| # | Problem | Key Concept |
|---|---------|-------------|
| 704 | Binary Search | Basic search in sorted array |
| 34 | First and Last Position | bisect_left + bisect_right |
| 35 | Search Insert Position | Lower bound |
| 74 | Search a 2D Matrix | Treat matrix as flat sorted array |
| 162 | Find Peak Element | Binary search on unsorted — compare with neighbor |

### Rotated / Modified Arrays
| # | Problem | Key Concept |
|---|---------|-------------|
| 33 | Search in Rotated Sorted Array | Determine sorted half |
| 81 | Search in Rotated Sorted Array II | Duplicates — worst case O(n) |
| 153 | Find Minimum in Rotated Sorted Array | Compare mid with hi |
| 540 | Single Element in Sorted Array | XOR property + binary search on pairs |

### Binary Search on Answer
| # | Problem | Key Concept |
|---|---------|-------------|
| 875 | Koko Eating Bananas | Minimize speed — feasibility check |
| 1011 | Capacity To Ship Packages | Minimize capacity |
| 410 | Split Array Largest Sum | Minimize max subarray sum |
| 1552 | Magnetic Force Between Two Balls | Maximize min distance |
| 668 | Kth Smallest Number in Multiplication Table | Count ≤ mid per row |
| 774 | Minimize Max Distance to Gas Station | Float binary search |

### Advanced
| # | Problem | Key Concept |
|---|---------|-------------|
| 4 | Median of Two Sorted Arrays | Binary search on partition |
| 378 | Kth Smallest in Sorted Matrix | Binary search on value + count |
| 287 | Find the Duplicate Number | Binary search on value range |
| 1482 | Minimum Number of Days to Make Bouquets | Binary search on days |

### Study Order
**Phase 1 (2 days):** 704, 34, 35, 74, 162
**Phase 2 (2-3 days):** 33, 153, 875, 1011
**Phase 3 (2-3 days):** 410, 1552, 378, 540
**Phase 4 (2-3 days):** 4, 668, 287, 1482
