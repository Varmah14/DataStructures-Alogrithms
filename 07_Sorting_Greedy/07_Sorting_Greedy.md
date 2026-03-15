# Sorting + Greedy — Complete Guide

## 1. Core Idea

Greedy algorithms make the **locally optimal choice** at each step, hoping it leads to the globally optimal solution. They work when the problem has **greedy choice property** (local optimum leads to global optimum) and **optimal substructure**.

**Sorting is the enabler.** Most greedy problems require sorting first to create the right order for greedy decisions.

---

## 2. When Does Greedy Work?

**Proof techniques (GATE-level):**
- **Exchange argument:** Show that swapping any non-greedy choice with the greedy choice doesn't worsen the solution.
- **Greedy stays ahead:** Show by induction that after each step, greedy is at least as good as any other strategy.

**Interview heuristic:** If sorting + one-pass scan gives O(n log n) and the problem asks for min/max, greedy is likely correct.

**Greedy fails when:** Future choices affect past decisions (use DP instead). Example: 0/1 knapsack is NOT greedy, but fractional knapsack IS.

---

## 3. Sorting Algorithms — Quick Reference

| Algorithm | Best | Average | Worst | Space | Stable? |
|---|---|---|---|---|---|
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Tim Sort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Radix Sort | O(d(n + k)) | O(d(n + k)) | O(d(n + k)) | O(n + k) | Yes |
| Bucket Sort | O(n + k) | O(n + k) | O(n²) | O(n + k) | Yes |

**Python's sort:** Tim Sort. Hybrid of merge sort + insertion sort. O(n log n) worst case, O(n) on nearly sorted data. Stable.

**GATE favorites:** Comparison-based lower bound is Ω(n log n). Counting/radix sort break this by not comparing. Quicksort worst case = O(n²) (already sorted + bad pivot). Randomized quicksort = O(n log n) expected.

---

## 4. Key Patterns

### Pattern A: Interval Scheduling / Activity Selection
Sort by **end time**. Greedily pick the earliest-ending non-overlapping interval.
```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])  # sort by end
    count = 0
    last_end = float('-inf')
    
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    return count
```
**Exchange argument:** Any non-greedy choice has a later end time, which can only reduce future options.

### Pattern B: Merge / Overlap Intervals
Sort by **start time**. Merge overlapping intervals.
```python
def merge_intervals(intervals):
    intervals.sort()
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

### Pattern C: Meeting Rooms / Minimum Resources
Sort by start time. Use a heap to track end times (covered in heap guide).
```python
def min_rooms(intervals):
    intervals.sort()
    heap = []  # end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)
```

### Pattern D: Task Assignment / Pair Matching
Sort both arrays and pair corresponding elements.
```python
# Assign workers to tasks, minimize max difficulty (or total cost)
# Often: sort both, pair smallest with smallest
workers.sort()
tasks.sort()
pairs = list(zip(workers, tasks))
```

### Pattern E: Jump Game / Reach Greedy
Track the farthest reachable position.
```python
def can_jump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
    return True

def min_jumps(nums):
    jumps = 0
    curr_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = farthest
    return jumps
```

### Pattern F: Gas Station (Circular Greedy)
```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start
```
**Key insight:** If total gas ≥ total cost, a solution exists. The start is the point right after the last "failure."

### Pattern G: Sort by Custom Criteria
Sometimes the greedy ordering is non-obvious.
```python
# Largest number from array (LC 179)
from functools import cmp_to_key
def largest_number(nums):
    nums = list(map(str, nums))
    nums.sort(key=cmp_to_key(lambda a, b: -1 if a+b > b+a else 1))
    return str(int(''.join(nums)))

# Queue reconstruction by height (LC 406)
def reconstruct_queue(people):
    people.sort(key=lambda x: (-x[0], x[1]))  # tallest first, then by k
    result = []
    for p in people:
        result.insert(p[1], p)
    return result
```

### Pattern H: Huffman-Style (Always Merge Two Smallest)
```python
def min_cost_connect_sticks(sticks):
    heapq.heapify(sticks)
    total = 0
    while len(sticks) > 1:
        a = heapq.heappop(sticks)
        b = heapq.heappop(sticks)
        cost = a + b
        total += cost
        heapq.heappush(sticks, cost)
    return total
```

---

## 5. Greedy vs DP Decision

| Indicator | Greedy | DP |
|---|---|---|
| Local choice stays optimal | ✅ | Not required |
| No "undo" needed | ✅ | Can revise via subproblems |
| Sorting gives natural order | ✅ | Not always |
| "Number of ways" | ❌ | ✅ |
| Optimal substructure only | May work | ✅ always works |
| Overlapping subproblems | Not needed | Required |

---

## 6. Edge Cases

- **Empty intervals:** Handle empty input.
- **Single element:** Often trivially correct.
- **Ties in sorting:** Specify tiebreak carefully (e.g., by end time then start time).
- **Overlapping vs touching:** `start == end` — is this overlapping? Problem-dependent.
- **Negative values:** Greedy assumptions may break with negative costs.

---

## 7. LeetCode Problems

### Interval Problems
| # | Problem | Key Concept |
|---|---------|-------------|
| 56 | Merge Intervals | Sort by start, merge overlapping |
| 57 | Insert Interval | Binary search or linear merge |
| 435 | Non-overlapping Intervals | Activity selection (min removals) |
| 252 | Meeting Rooms | Sort, check overlap |
| 253 | Meeting Rooms II | Sort + heap (min rooms) |
| 1288 | Remove Covered Intervals | Sort by start (desc by end), scan |

### Classic Greedy
| # | Problem | Key Concept |
|---|---------|-------------|
| 55 | Jump Game | Farthest reachable |
| 45 | Jump Game II | BFS-style level expansion |
| 134 | Gas Station | Circular greedy |
| 135 | Candy | Two-pass greedy (left then right) |
| 763 | Partition Labels | Last occurrence + merge intervals |
| 406 | Queue Reconstruction by Height | Sort descending, insert by k |

### Sorting-Based
| # | Problem | Key Concept |
|---|---------|-------------|
| 179 | Largest Number | Custom comparator |
| 452 | Minimum Number of Arrows to Burst Balloons | Activity selection variant |
| 1353 | Maximum Number of Events | Sort by end day, greedily attend |
| 870 | Advantage Shuffle | Sort both, match or waste smallest |

### Advanced Greedy
| # | Problem | Key Concept |
|---|---------|-------------|
| 455 | Assign Cookies | Sort both, two pointers |
| 860 | Lemonade Change | Simulate with greedy change |
| 1029 | Two City Scheduling | Sort by cost difference |
| 621 | Task Scheduler | Greedy cooldown (see heap guide) |
| 846 | Hand of Straights | Greedy grouping with sorted map |

### Study Order
**Phase 1 (2-3 days):** 56, 435, 252, 55, 45
**Phase 2 (2-3 days):** 134, 763, 135, 406, 179
**Phase 3 (2-3 days):** 452, 253, 870, 1029
**Phase 4 (2-3 days):** 846, 621, 1353, 860
