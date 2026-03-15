# Sliding Window — Complete Guide

## 1. Core Idea

Maintain a window [left, right] over an array/string. Expand right to include more, shrink left to maintain constraints. Converts O(n²) brute force to O(n).

Two types:
- **Fixed size:** Window always has size k.
- **Variable size:** Window expands/shrinks based on a condition.

---

## 2. Templates

### Template 1: Fixed Window
```python
def fixed_window(arr, k):
    # Initialize first window
    window_sum = sum(arr[:k])
    best = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # slide: add right, remove left
        best = max(best, window_sum)
    return best
```

### Template 2: Variable Window — Longest/Largest
"Find longest subarray/substring satisfying condition."
```python
def longest_window(arr):
    left = 0
    best = 0
    state = ...  # window state (counter, sum, set, etc.)
    
    for right in range(len(arr)):
        # Expand: add arr[right] to state
        update_state(arr[right])
        
        while not valid(state):
            # Shrink: remove arr[left] from state
            remove_state(arr[left])
            left += 1
        
        best = max(best, right - left + 1)
    return best
```

### Template 3: Variable Window — Shortest/Smallest
"Find shortest subarray satisfying condition."
```python
def shortest_window(arr, target):
    left = 0
    best = float('inf')
    curr_sum = 0
    
    for right in range(len(arr)):
        curr_sum += arr[right]
        
        while curr_sum >= target:  # condition met — try shrinking
            best = min(best, right - left + 1)
            curr_sum -= arr[left]
            left += 1
    
    return best if best != float('inf') else 0
```

### Template 4: Variable Window — Count of Subarrays
"Count subarrays satisfying condition."
```python
# atMost(k) counts subarrays with at most k distinct elements
# exactly(k) = atMost(k) - atMost(k-1)

def at_most_k(nums, k):
    left = 0
    count = 0
    freq = defaultdict(int)
    
    for right in range(len(nums)):
        freq[nums[right]] += 1
        
        while len(freq) > k:
            freq[nums[left]] -= 1
            if freq[nums[left]] == 0:
                del freq[nums[left]]
            left += 1
        
        count += right - left + 1  # all subarrays ending at right
    return count

def exactly_k(nums, k):
    return at_most_k(nums, k) - at_most_k(nums, k - 1)
```

**Why `right - left + 1`?** For every valid window [left, right], there are (right - left + 1) subarrays ending at `right`: [left, right], [left+1, right], ..., [right, right]. All are valid because the window is valid.

### Template 5: String Anagram / Fixed Window with Frequency
```python
def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    s_count = Counter(s[:len(p)])
    result = []
    
    if s_count == p_count:
        result.append(0)
    
    for i in range(len(p), len(s)):
        s_count[s[i]] += 1
        left_char = s[i - len(p)]
        s_count[left_char] -= 1
        if s_count[left_char] == 0:
            del s_count[left_char]
        if s_count == p_count:
            result.append(i - len(p) + 1)
    
    return result
```

### Template 6: Minimum Window Substring
```python
def min_window(s, t):
    need = Counter(t)
    have = 0
    required = len(need)
    left = 0
    best = (float('inf'), 0, 0)  # (length, left, right)
    window = defaultdict(int)
    
    for right in range(len(s)):
        c = s[right]
        window[c] += 1
        if c in need and window[c] == need[c]:
            have += 1
        
        while have == required:
            length = right - left + 1
            if length < best[0]:
                best = (length, left, right)
            
            lc = s[left]
            window[lc] -= 1
            if lc in need and window[lc] < need[lc]:
                have -= 1
            left += 1
    
    l, r = best[1], best[2]
    return s[l:r+1] if best[0] != float('inf') else ""
```

---

## 3. The exactly(K) = atMost(K) - atMost(K-1) Trick

This is the most important non-obvious sliding window technique. Many problems ask "exactly K" but the sliding window naturally handles "at most K."

**Examples:**
- Subarrays with exactly K distinct integers → atMost(K) - atMost(K-1)
- Substrings with exactly K 1s → atMost(K) - atMost(K-1)
- Binary subarrays with sum K → atMost(K) - atMost(K-1)

---

## 4. When to Use

- **Contiguous subarray/substring** — keyword.
- **Longest/shortest with constraint** → variable window.
- **Fixed size k** → fixed window.
- **"At most K" / "exactly K"** → atMost trick.
- **Anagram/permutation check** → fixed window with frequency map.

---

## 5. Edge Cases

- **Empty string/array** — return 0 or empty.
- **Window larger than array** — handle k > n.
- **All same elements** — window might never shrink.
- **No valid window** — return 0 / empty / -1.
- **Negative numbers** — sliding window for sum problems may not work (can't shrink reliably). Use prefix sum + hashmap instead.

---

## 6. LeetCode Problems

### Fixed Window
| # | Problem | Key Concept |
|---|---------|-------------|
| 643 | Maximum Average Subarray I | Fixed window sum |
| 438 | Find All Anagrams in a String | Fixed window + frequency |
| 567 | Permutation in String | Fixed window + frequency |
| 239 | Sliding Window Maximum | Monotonic deque (see monotonic guide) |

### Variable Window — Longest
| # | Problem | Key Concept |
|---|---------|-------------|
| 3 | Longest Substring Without Repeating Characters | Set + shrink on duplicate |
| 159 | Longest Substring with At Most Two Distinct | Counter + shrink when > 2 |
| 340 | Longest Substring with At Most K Distinct | Counter + shrink when > K |
| 424 | Longest Repeating Character Replacement | max_freq trick |
| 1004 | Max Consecutive Ones III | At most K flips |
| 1695 | Maximum Erasure Value | Set/sum + shrink on duplicate |

### Variable Window — Shortest
| # | Problem | Key Concept |
|---|---------|-------------|
| 76 | Minimum Window Substring | Frequency match + shrink |
| 209 | Minimum Size Subarray Sum | Sum ≥ target |
| 862 | Shortest Subarray with Sum at Least K | Deque (handles negatives) |

### Counting / Exactly K
| # | Problem | Key Concept |
|---|---------|-------------|
| 992 | Subarrays with K Different Integers | atMost(K) - atMost(K-1) |
| 930 | Binary Subarrays With Sum | atMost(K) - atMost(K-1) |
| 1248 | Count Number of Nice Subarrays | atMost(K) - atMost(K-1) |

### Study Order
**Phase 1 (2-3 days):** 643, 3, 209, 438
**Phase 2 (2-3 days):** 567, 424, 1004, 76
**Phase 3 (2-3 days):** 992, 930, 340, 239
