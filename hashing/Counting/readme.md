# Hashing & Counting — Complete Theory + LC Problem Set

---

## 1. What is Hashing?

Hashing is the process of mapping a **key of arbitrary type** to a **fixed-range integer index** via a **hash function** `h(k)`, used to achieve O(1) average-case insert, delete, and lookup.

The core tension: the key universe is huge (all possible strings, integers, etc.), but your table size `m` is finite → **collisions are inevitable** (Pigeonhole Principle).

---

## 2. Hash Functions

A good hash function is:

- **Deterministic** — same key always gives same hash
- **Uniform** — distributes keys evenly across buckets
- **Fast** to compute

### Integer Keys — Division Method

```
h(k) = k mod m
```

Choose `m` = prime not close to a power of 2. Avoids clustering from patterns in keys.

### Integer Keys — Multiplication Method

```
h(k) = floor(m × (k × A mod 1)),  A ≈ (√5 - 1)/2  (Knuth)
```

Less sensitive to choice of `m`.

### String Keys — Polynomial Rolling Hash

```
h(s) = (s[0]·p^(n-1) + s[1]·p^(n-2) + ... + s[n-1]) mod M
```

Typically `p = 31` (lowercase letters) or `p = 131`, `M = 10^9+7` (large prime).

This is the foundation of **Rabin-Karp** and all rolling hash problems.

### Universal Hashing

Pick `h(k) = ((ak + b) mod p) mod m` where `a,b` random, `p` prime > universe size. Guarantees **expected O(1)** regardless of input — important for adversarial inputs.

---

## 3. Collision Resolution

### Chaining (Closed Addressing)

Each bucket holds a **linked list** of all keys that hash there.

```
Insert:  O(1) — prepend to list
Search:  O(1 + α) average,  O(n) worst  (α = load factor = n/m)
Delete:  O(1 + α) average
```

Load factor `α = n/m`. Keep `α ≤ 1` for good performance. Python's `dict` uses this (with open addressing actually — see below).

### Open Addressing (Closed Hashing)

All elements stored **in the table itself**. On collision, probe for next slot.

**Linear Probing**: `h(k, i) = (h(k) + i) mod m`

- Simple, cache-friendly
- Suffers from **primary clustering** — long runs of occupied slots form

**Quadratic Probing**: `h(k, i) = (h(k) + c₁i + c₂i²) mod m`

- Reduces primary clustering
- Suffers from **secondary clustering** — same initial hash → same probe sequence

**Double Hashing**: `h(k, i) = (h₁(k) + i·h₂(k)) mod m`

- Best distribution among open addressing schemes
- No clustering if `h₂(k)` is coprime to `m`

### Comparison

|             | Chaining               | Open Addressing            |
| ----------- | ---------------------- | -------------------------- |
| Space       | Extra pointer overhead | No extra space             |
| Cache       | Poor (pointer chasing) | Excellent (array access)   |
| Load factor | Can exceed 1           | Must stay < 1              |
| Deletion    | Easy                   | Tricky (tombstones needed) |

---

## 4. Load Factor & Rehashing

**Load factor** `α = n/m` (n = elements, m = table size).

- Chaining: performance degrades as `α` grows past 1
- Open addressing: degrades rapidly past `α ≈ 0.7`

**Rehashing**: when `α` exceeds threshold, allocate a table of size `≈2m` and reinsert all elements.

- Cost of one rehash: O(n)
- But amortized over all inserts: **O(1) amortized per insert**
- This is the same argument as dynamic array doubling

Python's `dict` rehashes at `α ≈ 2/3`.

---

## 5. Expected vs Worst Case

|                                | Average       | Worst Case   | When worst occurs                |
| ------------------------------ | ------------- | ------------ | -------------------------------- |
| HashMap get/put                | O(1)          | O(n)         | All keys collide into one bucket |
| HashMap with universal hashing | O(1) expected | O(log n) whp | —                                |

In interviews, always say **O(1) average** for hash map ops. In GATE, know the worst case proof.

---

## 6. Python's `dict` Internals (Relevant for Interviews)

Python dicts use **open addressing with pseudo-random probing**:

```
i = (5*i + 1 + perturb) mod m;  perturb >>= 5
```

- Initial size = 8, resizes at 2/3 load
- From Python 3.7+, **insertion order is preserved** (implementation detail made spec)
- Keys must be **hashable** (immutable): int, str, tuple of hashables — not list, dict, set

---

## 7. Counting Patterns — The Core Interview Toolkit

This is where theory meets almost every interview problem in this topic.

### Pattern A — Frequency Map

```python
from collections import Counter
freq = Counter(arr)          # O(n)
freq['a']                    # O(1)
freq.most_common(k)          # O(n log k)
```

### Pattern B — Prefix Sum + HashMap (★ Most Important)

**Problem**: count subarrays with sum == K

Key insight: `sum(i..j) == K` ↔ `prefix[j] - prefix[i-1] == K` ↔ `prefix[i-1] == prefix[j] - K`

```python
def subarray_sum(nums, k):
    count = {0: 1}   # prefix sum 0 seen once before array starts
    prefix = 0
    ans = 0
    for x in nums:
        prefix += x
        ans += count.get(prefix - k, 0)
        count[prefix] = count.get(prefix, 0) + 1
    return ans
```

This pattern generalizes to: prefix XOR == K, balance of +1/-1, etc.

### Pattern C — Complement / Pair Lookup

Two-sum style: for each element, check if its **complement** exists in a set.

```python
seen = set()
for x in nums:
    if target - x in seen: return True
    seen.add(x)
```

### Pattern D — Anagram / Permutation via Frequency Signature

Two strings are anagrams iff their frequency vectors are equal.

```python
Counter(s) == Counter(t)           # O(n)
tuple(sorted(s)) == tuple(sorted(t))   # O(n log n) — use as dict key for grouping
```

### Pattern E — Sliding Window + Hash Map

Track character frequencies in a window. Expand right, shrink left when invariant breaks.

```python
window = {}
left = 0
for right, c in enumerate(s):
    window[c] = window.get(c, 0) + 1
    while <invariant broken>:
        window[s[left]] -= 1
        if window[s[left]] == 0: del window[s[left]]
        left += 1
```

### Pattern F — Bucket / Pigeonhole

When values are bounded, use an array as hash map. O(1) access, O(range) space.
Used in: first missing positive, top K frequent (bucket sort), counting sort.

### Pattern G — Coordinate Compression

When values span huge range but count is small, compress to `[0, n)` via sorting + mapping.

```python
ranks = {v: i for i, v in enumerate(sorted(set(arr)))}
compressed = [ranks[x] for x in arr]
```

---

## 8. Hash Set vs Hash Map

|         | HashSet                | HashMap                            |
| ------- | ---------------------- | ---------------------------------- |
| Stores  | Keys only              | Key-value pairs                    |
| Use for | Existence check, dedup | Frequency, mapping, grouping       |
| Python  | `set()`                | `dict()`, `Counter`, `defaultdict` |

`defaultdict(int)` saves you from checking key existence — initializes missing keys to 0 automatically.

---

## 9. Rolling Hash — For Substring Problems

Allows recomputing hash of a sliding window in O(1) instead of O(n).

```
hash(s[i+1..j+1]) = (hash(s[i..j]) - s[i]·p^(n-1)) · p + s[j+1]
```

Application: find all duplicate substrings of length L in O(n) average.
Core of **Rabin-Karp** algorithm.

**Collision risk**: use double hashing (two different mod values) to reduce false positives to negligible probability.

---

## 10. GATE-Specific Points

1. **Simple Uniform Hashing assumption**: each key equally likely to hash to any slot, independently. Under this, expected chain length = α.
2. **Expected number of probes** in open addressing:
   - Successful search: `(1/α) · ln(1/(1-α))`
   - Unsuccessful search: `1/(1-α)`
3. **Perfect hashing**: O(n) space, O(1) worst-case lookup — uses two-level scheme (Fredman-Komlós-Szemerédi). GATE loves this conceptually.
4. **Hash tables vs BSTs**: Hash → O(1) avg, no order. BST → O(log n), supports range queries, ordered iteration.
5. **Deletion in open addressing** requires **tombstone markers** — you can't just clear the slot or future probes break.
6. **Worst-case** for chaining is Θ(n) when all n keys hash to same slot.

---

## 11. LeetCode Problem Set — Full Coverage

### Tier 1 — Foundation

| #   | Problem                 | Concept                                  |
| --- | ----------------------- | ---------------------------------------- |
| 1   | Two Sum                 | Complement lookup, classic hash map      |
| 217 | Contains Duplicate      | HashSet existence check                  |
| 242 | Valid Anagram           | Frequency comparison                     |
| 383 | Ransom Note             | Frequency subtraction                    |
| 49  | Group Anagrams          | Sorted key / frequency tuple as dict key |
| 347 | Top K Frequent Elements | Counter + bucket sort or heap            |

### Tier 2 — Prefix + HashMap (Core Pattern)

| #    | Problem                           | Concept                                      |
| ---- | --------------------------------- | -------------------------------------------- |
| 560  | Subarray Sum Equals K             | Prefix sum + hashmap — the canonical problem |
| 523  | Continuous Subarray Sum           | Prefix mod + hashmap (remainder trick)       |
| 525  | Contiguous Array                  | +1/-1 balance prefix, find equal 0s and 1s   |
| 974  | Subarray Sums Divisible by K      | Prefix mod, negative mod handling            |
| 1371 | Longest Subarray with Even Vowels | XOR bitmask prefix + hashmap                 |
| 1915 | Number of Wonderful Substrings    | Bitmask prefix XOR + hashmap                 |

### Tier 3 — Sliding Window + Hashing

| #    | Problem                                        | Concept                                     |
| ---- | ---------------------------------------------- | ------------------------------------------- |
| 3    | Longest Substring Without Repeating Characters | Window + set/map                            |
| 76   | Minimum Window Substring                       | Window + frequency map + have/need counters |
| 438  | Find All Anagrams in a String                  | Fixed window + frequency comparison         |
| 567  | Permutation in String                          | Same as 438, existence version              |
| 992  | Subarrays with K Different Integers            | exactly(K) = atMost(K) - atMost(K-1)        |
| 1248 | Count Number of Nice Subarrays                 | Prefix + hashmap on odd-count parity        |

### Tier 4 — Counting & Grouping

| #   | Problem                      | Concept                                    |
| --- | ---------------------------- | ------------------------------------------ |
| 128 | Longest Consecutive Sequence | Set + only start chains at sequence starts |
| 41  | First Missing Positive       | In-place bucket hashing (array as hashmap) |
| 169 | Majority Element             | Boyer-Moore / Counter                      |
| 229 | Majority Element II          | Extended Boyer-Moore, two candidates       |
| 380 | Insert Delete GetRandom O(1) | HashMap + array index trick                |
| 355 | Design Twitter               | HashMap + heap (combined pattern)          |

### Tier 5 — Advanced / Hard

| #   | Problem                                   | Concept                                        |
| --- | ----------------------------------------- | ---------------------------------------------- |
| 76  | Minimum Window Substring                  | Already listed — solve it properly             |
| 149 | Max Points on a Line                      | Slope as fraction key in hashmap               |
| 454 | 4Sum II                                   | Split into two 2Sums, complement map           |
| 336 | Palindrome Pairs                          | Trie or complement hashmap on reversed strings |
| 895 | Maximum Frequency Stack                   | Frequency of frequency map                     |
| 30  | Substring with Concatenation of All Words | Fixed-window sliding over word-length steps    |

---

## 12. Study Order

```
Day 1 — Theory: sections 1–5, implement chaining & open addressing from scratch
Day 2 — 1, 217, 242, 49, 347 — get the frequency/grouping patterns solid
Day 3 — 560, 523, 525, 974 — prefix+hashmap family, internalize the {0:1} init
Day 4 — 3, 76, 438, 992 — sliding window + hash map
Day 5 — 128, 41, 380 — counting tricks and design
Day 6 — 1371, 1915, 454, 149 — bitmask prefix and multi-dimensional hashing
Day 7 — 895, 30, 336 — hard problems; review all patterns
```

---

## Quick Reference Card

```
Use a HashMap when:
  ✓ Need O(1) lookup / existence check
  ✓ Counting frequencies
  ✓ Prefix sum/XOR + complement lookup
  ✓ Grouping by computed key (anagrams, slopes)
  ✓ Caching seen states

Key tricks:
  prefix+map  →  always init {0: 1} for empty prefix
  sliding window  →  expand right, shrink left on violation
  exactly(K)  →  atMost(K) − atMost(K−1)
  anagram check  →  sorted string or freq tuple as key
  large range  →  coordinate compress first
  O(1) amortized  →  rehashing doubles table size
```

Perfect. FAANG + mid-tier with 1–2 months means we go **pattern-depth over breadth** — you need to solve problems fast and explain your reasoning clearly, not just get AC.

Here's the recalibrated Hashing & Counting guide for your profile:

---

# Hashing & Counting — Interview-Focused (SWE, FAANG + Mid-tier)

---

## What Interviewers Actually Test Here

At Meta/Google/Amazon, hashing problems are rarely "implement a hash map." They test:

- Can you **recognize** that a complement lookup / prefix map reduces O(n²) → O(n)?
- Can you handle **edge cases** in frequency counting without being prompted?
- Do you **naturally reach** for the right data structure or do you brute force first?

Your backend experience is an asset — frame your thinking in terms of tradeoffs (time vs space, correctness vs performance) just like you would in a system design.

---

## The 6 Patterns That Cover Everything

---

### Pattern 1 — Complement / Pair Lookup

**Idea**: instead of checking all pairs O(n²), store what you've seen and ask "does my complement exist?"

```python
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```

**Interview tip**: always clarify — can we use the same element twice? Are there multiple answers? This shows you think about spec before coding.

**Generalizes to**: 3Sum (fix one, two-sum the rest), 4Sum II (split into two halves).

---

### Pattern 2 — Frequency Map + Counting

**Idea**: `Counter` or `defaultdict(int)` to count, then reason about frequencies.

```python
from collections import Counter
freq = Counter(arr)
```

The sneaky variant: **frequency of frequencies**.

```python
# "how many elements appear exactly k times?"
freq = Counter(arr)
freq_of_freq = Counter(freq.values())
```

This shows up in harder problems like Maximum Frequency Stack (895).

**Interview tip**: when you see "most frequent," "at least K times," "majority element" — this is your pattern.

---

### Pattern 3 — Prefix Sum + HashMap ⭐ Most Important

**Core insight**: `sum(i..j) == K` → `prefix[j] - prefix[i] == K` → `prefix[i] == prefix[j] - K`

So for every `j`, look up `prefix[j] - K` in your map.

```python
def subarray_sum(nums, k):
    count = {0: 1}    # empty prefix — never forget this
    prefix = 0
    ans = 0
    for x in nums:
        prefix += x
        ans += count.get(prefix - k, 0)
        count[prefix] = count.get(prefix, 0) + 1
    return ans
```

**The `{0: 1}` initialization** is the most common mistake under pressure. The prefix sum before the array starts is 0, and it's been seen once. Forgetting this breaks subarrays that start at index 0.

**Variants** (same skeleton, different "prefix"):

| Variant           | What you accumulate | What you look up          |
| ----------------- | ------------------- | ------------------------- |
| Subarray sum == K | running sum         | `prefix - K`              |
| Subarray XOR == K | running XOR         | `prefix ^ K`              |
| Equal 0s and 1s   | +1 for 1, -1 for 0  | same prefix (seen before) |
| Divisible by K    | `prefix % K`        | same remainder            |

---

### Pattern 4 — Sliding Window + HashMap

**Idea**: maintain a window `[left, right]` with a frequency map. Expand right, shrink left when invariant breaks.

```python
window = defaultdict(int)
left = ans = 0
for right, c in enumerate(s):
    window[c] += 1
    while <invariant violated>:     # e.g. len(window) > k distinct chars
        window[s[left]] -= 1
        if window[s[left]] == 0:
            del window[s[left]]
        left += 1
    ans = max(ans, right - left + 1)
```

**The `exactly K` trick**: problems asking for subarrays with **exactly K** distinct things are hard to do directly. Instead:

```
exactly(K) = atMost(K) - atMost(K-1)
```

Write one clean `atMost(k)` function, call it twice. This comes up constantly at Google/Meta.

---

### Pattern 5 — Grouping by Hash Key

**Idea**: compute a canonical key for each element, group elements with same key.

```python
groups = defaultdict(list)
for s in strs:
    key = tuple(sorted(s))      # or: tuple(Counter(s).items())
    groups[key].append(s)
```

**Generalizes**: group anagrams (sorted string key), max points on a line (slope as fraction key), isomorphic strings (mapping key).

**Interview tip**: when you think "these things are equivalent," ask yourself "what's the canonical form?" — that's your hash key.

---

### Pattern 6 — Set for O(1) Existence + Boundary Trick

**Idea**: load everything into a set, then only start counting from **boundaries** to avoid redundant work.

```python
num_set = set(nums)
for n in num_set:
    if n - 1 not in num_set:      # only start a chain at its beginning
        cur = n
        length = 0
        while cur in num_set:
            cur += 1
            length += 1
        ans = max(ans, length)
```

Without the boundary check this is O(n²). With it, each element is visited at most twice → O(n). This is the insight interviewers want to see you articulate.

---

## Interview Execution — What to Actually Say

When you see a hashing problem in an interview:

1. **Brute force first** — say it out loud, state its complexity. "Naive is O(n²) checking all pairs."
2. **Identify the redundancy** — "We're re-checking things we've already seen."
3. **Propose the hash structure** — "If I store complements/prefixes/frequencies as I go, I can answer in O(1) per element."
4. **State the tradeoff** — "O(n) time, O(n) space — trading space for time."
5. **Handle edge cases before coding** — empty array, all same elements, negative numbers (prefix sum), k=0.

---

## The 18 Problems — Pattern-Mapped

### Pattern 1 — Complement / Pair Lookup

| #   | Problem                      | Why it's here                                                 |
| --- | ---------------------------- | ------------------------------------------------------------- |
| 1   | Two Sum                      | The template. Must solve in < 3 min.                          |
| 454 | 4Sum II                      | Split into two 2-sum halves. Meet in the middle with hashing. |
| 128 | Longest Consecutive Sequence | Set lookup + boundary trick. Amazon favorite.                 |

---

### Pattern 2 — Frequency Counting

| #   | Problem                 | Why it's here                                |
| --- | ----------------------- | -------------------------------------------- |
| 347 | Top K Frequent Elements | Counter + bucket sort. Know both approaches. |
| 169 | Majority Element        | Boyer-Moore vote. Understand why it works.   |
| 895 | Maximum Frequency Stack | Freq of freq map. Hard but shows depth.      |

---

### Pattern 3 — Prefix + HashMap

| #   | Problem                      | Why it's here                                 |
| --- | ---------------------------- | --------------------------------------------- |
| 560 | Subarray Sum Equals K        | The canonical prefix+map problem. No excuses. |
| 523 | Continuous Subarray Sum      | Prefix mod. The `{0: -1}` init variant.       |
| 525 | Contiguous Array             | +1/-1 balance trick. Equal 0s and 1s.         |
| 974 | Subarray Sums Divisible by K | Negative mod: `((prefix % k) + k) % k`.       |

---

### Pattern 4 — Sliding Window + HashMap

| #   | Problem                                   | Why it's here                                           |
| --- | ----------------------------------------- | ------------------------------------------------------- |
| 3   | Longest Substring Without Repeating Chars | Window + set. Warmup.                                   |
| 76  | Minimum Window Substring                  | Window + have/need counters. Meta asks this constantly. |
| 992 | Subarrays with K Different Integers       | exactly(K) = atMost(K) - atMost(K-1).                   |
| 438 | Find All Anagrams in a String             | Fixed window + freq comparison. Google favorite.        |

---

### Pattern 5 — Grouping

| #   | Problem              | Why it's here                                 |
| --- | -------------------- | --------------------------------------------- |
| 49  | Group Anagrams       | Sorted key grouping. Classic.                 |
| 149 | Max Points on a Line | Slope as reduced fraction key. Hard grouping. |

---

### Pattern 6 — Design + Hash

| #   | Problem                      | Why it's here                                       |
| --- | ---------------------------- | --------------------------------------------------- |
| 380 | Insert Delete GetRandom O(1) | HashMap + array swap trick. System-design adjacent. |
| 41  | First Missing Positive       | Array-as-hashmap. O(1) space constraint. Hard.      |

---

## 6-Day Execution Plan

```
Day 1 — Patterns 1 & 2:   1, 454, 128, 347, 169
Day 2 — Pattern 3:         560, 523, 525, 974  ← drill the {0:1} init
Day 3 — Pattern 4 part A:  3, 438, 567 (bonus)
Day 4 — Pattern 4 part B:  76, 992  ← these are hard, give them time
Day 5 — Patterns 5 & 6:   49, 149, 380, 41
Day 6 — Review day:        Redo 3 problems you were slowest on.
                           Time yourself: target < 15 min per medium.
```

---

## Common Interview Traps in This Topic

| Trap                                 | Fix                                                |
| ------------------------------------ | -------------------------------------------------- |
| Forgetting `{0: 1}` in prefix map    | Always write it first, before the loop             |
| Negative numbers breaking prefix mod | Use `((prefix % k) + k) % k`                       |
| Mutating Counter while iterating     | Collect keys first or iterate a copy               |
| Using list as dict key               | Convert to tuple — lists aren't hashable           |
| Assuming O(1) hash is always true    | Say "O(1) average" in interviews — shows awareness |

---

After this, you're moving into **BFS/DFS on Graphs & Grids** per your plan — that's the biggest topic left and the one that combines with everything (Dijkstra connects back to heaps, topological sort connects to DP). Let me know when you're ready.
