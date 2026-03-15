# Two Pointers — Complete Guide

## 1. Core Idea

Use two pointers (indices) to traverse a data structure, reducing O(n²) brute force to O(n). Three main variants:

1. **Opposite ends** — converge from both ends of sorted array.
2. **Same direction (fast/slow)** — one pointer leads, other follows.
3. **Two arrays** — one pointer per array.

---

## 2. Templates

### Template 1: Opposite Ends (Sorted Array)
```python
def two_sum_sorted(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []
```

### Template 2: Remove Duplicates In-Place
```python
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

### Template 3: Partition (Dutch National Flag)
Three-way partition — sort 0s, 1s, 2s in one pass.
```python
def sort_colors(nums):
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1
```

### Template 4: Fast/Slow (Linked List Cycle)
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def find_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

### Template 5: Container With Most Water
```python
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        area = min(height[lo], height[hi]) * (hi - lo)
        best = max(best, area)
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best
```
**Why move the shorter side?** Moving the taller side can only decrease or maintain the area (width shrinks, height limited by shorter). Moving the shorter side might find a taller line.

### Template 6: Three Sum
```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue  # skip duplicates
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                result.append([nums[i], nums[lo], nums[hi]])
                while lo < hi and nums[lo] == nums[lo+1]:
                    lo += 1  # skip duplicates
                while lo < hi and nums[hi] == nums[hi-1]:
                    hi -= 1
                lo += 1
                hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return result
```

### Template 7: Palindrome Check
```python
def is_palindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True
```

### Template 8: Merge Two Sorted Arrays
```python
def merge(nums1, m, nums2, n):
    # Merge from the end to avoid overwriting
    p1, p2, p = m - 1, n - 1, m + n - 1
    while p2 >= 0:
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
```

---

## 3. When to Use

- **Sorted array + pair/sum** → opposite ends
- **Remove duplicates / in-place modification** → read/write pointers
- **Partition / sort colors** → three-way partition
- **Linked list cycle** → fast/slow
- **Palindrome** → opposite ends
- **Merge sorted arrays** → two-array pointers
- **Container / trapping water** → opposite ends with greedy

---

## 4. Edge Cases

- **Empty array** or single element — lo > hi immediately.
- **All duplicates** — dedup logic must handle this.
- **Negative numbers** — affects sum-based problems.
- **Overflow** — sum of two large ints (other languages).
- **Pointer equality** — `lo < hi` vs `lo <= hi` — off-by-one.

---

## 5. LeetCode Problems

| # | Problem | Key Concept |
|---|---------|-------------|
| 167 | Two Sum II | Sorted + opposite ends |
| 15 | 3Sum | Fix one + two pointers |
| 11 | Container With Most Water | Opposite ends greedy |
| 42 | Trapping Rain Water | Two pointers or stack |
| 26 | Remove Duplicates from Sorted Array | Read/write pointers |
| 27 | Remove Element | Read/write |
| 75 | Sort Colors | Dutch National Flag |
| 125 | Valid Palindrome | Two pointers + char check |
| 680 | Valid Palindrome II | Allow one deletion |
| 88 | Merge Sorted Array | Merge from end |
| 283 | Move Zeroes | Read/write partition |
| 977 | Squares of Sorted Array | Opposite ends, compare absolutes |
| 141 | Linked List Cycle | Fast/slow |
| 142 | Linked List Cycle II | Find cycle start |
| 234 | Palindrome Linked List | Fast/slow to find mid + reverse |

### Study Order
**Phase 1 (2 days):** 167, 26, 27, 283, 125
**Phase 2 (2-3 days):** 15, 11, 75, 88, 977
**Phase 3 (2-3 days):** 42, 141, 142, 680, 234
