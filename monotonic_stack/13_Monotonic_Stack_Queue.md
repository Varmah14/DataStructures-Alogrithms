# Monotonic Stack / Queue — Complete Guide

## 1. Monotonic Stack

### Core Idea
A stack where elements are always in sorted order (increasing or decreasing). When a new element violates the order, pop elements until the order is restored. Each element is pushed and popped at most once → O(n) total.

**What it finds:** For each element, the **nearest greater/smaller** element to the left or right.

### Template 1: Next Greater Element (Right)
```python
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices
    
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result
```

### Template 2: Next Smaller Element (Right)
```python
def next_smaller(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result
```

### Template 3: Previous Greater Element (Left)
```python
def prev_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    for i in range(n):
        while stack and nums[stack[-1]] <= nums[i]:
            stack.pop()
        if stack:
            result[i] = nums[stack[-1]]
        stack.append(i)
    return result
```

### Direction Table
| Want | Stack Order | Pop When | Iterate |
|---|---|---|---|
| Next greater (right) | Decreasing | stack[-1] < curr | Left → Right |
| Next smaller (right) | Increasing | stack[-1] > curr | Left → Right |
| Prev greater (left) | Decreasing | stack[-1] <= curr | Left → Right |
| Prev smaller (left) | Increasing | stack[-1] >= curr | Left → Right |
| Next greater (left) | Decreasing | stack[-1] < curr | Right → Left |

### Template 4: Largest Rectangle in Histogram
```python
def largest_rectangle(heights):
    stack = []  # stores indices of increasing heights
    max_area = 0
    heights.append(0)  # sentinel to flush remaining
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    heights.pop()  # remove sentinel
    return max_area
```
**Key insight:** When we pop index `j`, `heights[j]` is the smallest height in the range `(stack[-1], i)`. Width = distance between current right boundary `i` and new stack top (left boundary).

### Template 5: Daily Temperatures
```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []
    
    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result
```

### Template 6: Stock Span
```python
def stock_span(prices):
    result = []
    stack = []  # (price, span)
    
    for price in prices:
        span = 1
        while stack and stack[-1][0] <= price:
            span += stack.pop()[1]
        stack.append((price, span))
        result.append(span)
    return result
```

---

## 2. Monotonic Queue (Deque)

### Core Idea
A deque where elements are in monotonic order. Used for **sliding window min/max**. Maintains candidates for the window's extreme value.

### Template: Sliding Window Maximum
```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # stores indices, decreasing order of values
    result = []
    
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Maintain decreasing order
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])  # front is always the max
    return result
```

### Template: Sliding Window Minimum
Same but flip the comparison:
```python
def min_sliding_window(nums, k):
    dq = deque()  # increasing order
    result = []
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] >= nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

---

## 3. When to Use What

| Problem | Tool |
|---|---|
| Next/previous greater/smaller | Monotonic stack |
| Histogram / rectangle area | Monotonic stack |
| Stock span / daily temperatures | Monotonic stack |
| Sliding window max/min | Monotonic deque |
| DP optimization (min/max over sliding range) | Monotonic deque |

---

## 4. Edge Cases

- **Duplicate values:** `<` vs `<=` in the pop condition matters. For "strictly greater", use `<`. For "greater or equal", use `<=`.
- **Circular array:** Process the array twice (or use modular indexing) for circular next greater.
- **Empty stack after pops:** Check `if stack` before accessing `stack[-1]`. Means no previous greater/smaller exists.
- **Sentinel values:** Adding 0 or -1 at the end of heights array simplifies histogram logic.

---

## 5. LeetCode Problems

### Monotonic Stack
| # | Problem | Key Concept |
|---|---------|-------------|
| 739 | Daily Temperatures | Next warmer day |
| 496 | Next Greater Element I | Hash + monotonic stack |
| 503 | Next Greater Element II | Circular — iterate twice |
| 84 | Largest Rectangle in Histogram | Classic monotonic stack |
| 85 | Maximal Rectangle | Histogram per row |
| 901 | Online Stock Span | Running span calculation |
| 42 | Trapping Rain Water | Stack approach (also two pointers) |
| 907 | Sum of Subarray Minimums | Prev/next smaller + contribution |
| 402 | Remove K Digits | Monotonic increasing stack |
| 316 | Remove Duplicate Letters | Stack with frequency + visited |

### Monotonic Queue
| # | Problem | Key Concept |
|---|---------|-------------|
| 239 | Sliding Window Maximum | Classic monotonic deque |
| 862 | Shortest Subarray with Sum ≥ K | Deque + prefix sum |
| 1438 | Longest Subarray with Abs Diff ≤ Limit | Two deques (max and min) |

### Study Order
**Phase 1 (2-3 days):** 739, 496, 503, 901
**Phase 2 (2-3 days):** 84, 85, 42, 402
**Phase 3 (2-3 days):** 907, 239, 862, 1438
