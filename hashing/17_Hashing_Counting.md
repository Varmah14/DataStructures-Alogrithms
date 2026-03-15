# Hashing / Counting — Complete Guide

## 1. Core Idea

Use hash maps (dictionaries) and hash sets for O(1) average lookups. Converts O(n²) brute force to O(n) for existence checks, frequency counting, deduplication, and grouping.

---

## 2. Templates

### Template 1: Two Sum (Complement Lookup)
```python
def two_sum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        comp = target - num
        if comp in seen:
            return [seen[comp], i]
        seen[num] = i
    return []
```

### Template 2: Frequency Count
```python
from collections import Counter

freq = Counter(nums)
# freq[x] = count of x
# freq.most_common(k) = top k by frequency

# Manual:
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
```

### Template 3: First Unique / Non-Repeating
```python
def first_unique(s):
    freq = Counter(s)
    for i, c in enumerate(s):
        if freq[c] == 1:
            return i
    return -1
```

### Template 4: Bucket Sort by Frequency
```python
def top_k_frequent(nums, k):
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)
    
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

### Template 5: Group by Key
```python
# Group anagrams
groups = defaultdict(list)
for s in strs:
    key = tuple(sorted(s))
    groups[key].append(s)
```

### Template 6: Sliding Window with HashMap
```python
# Count distinct in window — combine with sliding window
window = defaultdict(int)
distinct = 0

def add(x):
    global distinct
    window[x] += 1
    if window[x] == 1:
        distinct += 1

def remove(x):
    global distinct
    window[x] -= 1
    if window[x] == 0:
        distinct -= 1
        del window[x]
```

---

## 3. Hash Set Patterns

```python
# Existence check
seen = set()
if x in seen:  # O(1) average
    ...
seen.add(x)

# Intersection / Union / Difference
set_a & set_b  # intersection
set_a | set_b  # union
set_a - set_b  # difference

# Deduplication
unique = list(set(nums))  # loses order
# Preserve order:
seen = set()
unique = [x for x in nums if not (x in seen or seen.add(x))]
```

---

## 4. Edge Cases

- **Hash collisions** — Python dicts handle this internally. In interviews, mention average O(1) vs worst case O(n).
- **Unhashable types** — lists, dicts can't be set/dict keys. Use tuples or frozensets.
- **Counter arithmetic** — `Counter(a) - Counter(b)` drops zero and negative counts.
- **defaultdict vs get** — `defaultdict(int)` auto-initializes. `.get(key, default)` doesn't modify dict.

---

## 5. LeetCode Problems

| # | Problem | Key Concept |
|---|---------|-------------|
| 1 | Two Sum | Complement hashmap |
| 217 | Contains Duplicate | Set existence |
| 242 | Valid Anagram | Frequency count |
| 49 | Group Anagrams | Sorted key grouping |
| 347 | Top K Frequent Elements | Frequency + bucket sort |
| 128 | Longest Consecutive Sequence | Set + expand from sequence start |
| 387 | First Unique Character | Frequency scan |
| 560 | Subarray Sum Equals K | Prefix sum + hashmap |
| 349 | Intersection of Two Arrays | Set intersection |
| 205 | Isomorphic Strings | Two-way mapping |
| 290 | Word Pattern | Two-way mapping |
| 36 | Valid Sudoku | Sets for row/col/box |
| 692 | Top K Frequent Words | Freq + heap with tiebreak |

### Study Order
**Phase 1 (2 days):** 1, 217, 242, 387, 349
**Phase 2 (2-3 days):** 49, 347, 128, 205, 290
**Phase 3 (2-3 days):** 560, 36, 692
