# String Algorithms — Complete Guide

## 1. Core Algorithms

### KMP (Knuth-Morris-Pratt)
Linear-time pattern matching. Build a failure/LPS (Longest Proper Prefix which is also Suffix) array, then match.

```python
def kmp_search(text, pattern):
    def build_lps(p):
        lps = [0] * len(p)
        length = 0
        i = 1
        while i < len(p):
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length > 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps
    
    lps = build_lps(pattern)
    result = []
    i = j = 0  # i for text, j for pattern
    
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
    return result
```
**Time:** O(n + m). **Space:** O(m) for LPS.

**LPS array intuition:** `lps[i]` = length of the longest proper prefix of pattern[0..i] that is also a suffix. When a mismatch occurs at position j, jump back to `lps[j-1]` instead of restarting.

### Z-Algorithm
`z[i]` = length of the longest substring starting at `i` that matches the prefix of the string.

```python
def z_function(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    l, r = 0, 0
    
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

# Pattern matching: concatenate pattern + "$" + text
# z[i] == len(pattern) means match at position i - len(pattern) - 1
```

### Rabin-Karp (Rolling Hash)
```python
def rabin_karp(text, pattern):
    base = 31
    mod = 10**9 + 7
    n, m = len(text), len(pattern)
    
    # Compute pattern hash
    p_hash = 0
    for c in pattern:
        p_hash = (p_hash * base + ord(c)) % mod
    
    # Compute hash of first window
    t_hash = 0
    power = pow(base, m - 1, mod)
    for c in text[:m]:
        t_hash = (t_hash * base + ord(c)) % mod
    
    result = []
    for i in range(n - m + 1):
        if t_hash == p_hash and text[i:i+m] == pattern:  # verify on hash match
            result.append(i)
        if i + m < n:
            t_hash = (t_hash - ord(text[i]) * power) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
    return result
```
**Average:** O(n + m). **Worst:** O(nm) due to hash collisions. Use double hashing to reduce collisions.

### Manacher's Algorithm (Longest Palindrome in O(n))
```python
def manacher(s):
    # Transform "abc" → "^#a#b#c#$"
    t = '^#' + '#'.join(s) + '#$'
    n = len(t)
    p = [0] * n  # p[i] = radius of palindrome centered at i
    c = r = 0    # center, right boundary
    
    for i in range(1, n - 1):
        mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[mirror])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    
    # Find maximum
    max_len = max(p)
    center_idx = p.index(max_len)
    start = (center_idx - max_len) // 2
    return s[start:start + max_len]
```

---

## 2. Trie (Prefix Tree)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True
    
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    
    def _find(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return None
            node = node.children[c]
        return node
```

### Trie with Count / Delete
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0       # words passing through
        self.end_count = 0   # words ending here
```

---

## 3. Common String Patterns

### Anagram Check / Grouping
```python
# Check anagram: sort or count
def is_anagram(s, t):
    return Counter(s) == Counter(t)

# Group anagrams
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))  # or count-based key
        groups[key].append(s)
    return list(groups.values())
```

### Palindrome Check
```python
def is_palindrome(s):
    return s == s[::-1]

# Expand around center (find longest palindromic substring)
def longest_palindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]
    
    best = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        best = max(best, odd, even, key=len)
    return best
```

### String Hashing
```python
def string_hash(s, mod=10**9+7, base=31):
    h = 0
    for c in s:
        h = (h * base + ord(c) - ord('a') + 1) % mod
    return h
```

---

## 4. When to Use What

| Need | Algorithm |
|---|---|
| Single pattern search | KMP or Z-algorithm |
| Multiple pattern search | Aho-Corasick (or Trie) |
| Repeated substring detection | Rolling hash / suffix array |
| Prefix queries | Trie |
| Longest palindrome | Manacher (O(n)) or expand around center (O(n²)) |
| Anagram detection | Sorting or frequency count |
| Autocomplete | Trie |

---

## 5. LeetCode Problems

### Basic String
| # | Problem | Key Concept |
|---|---------|-------------|
| 242 | Valid Anagram | Frequency count |
| 49 | Group Anagrams | Sorted key grouping |
| 5 | Longest Palindromic Substring | Expand around center |
| 647 | Palindromic Substrings | Count all palindromes |
| 125 | Valid Palindrome | Two pointers + char filter |

### Trie
| # | Problem | Key Concept |
|---|---------|-------------|
| 208 | Implement Trie | Basic trie operations |
| 211 | Design Add and Search Words | Trie + DFS for wildcard |
| 212 | Word Search II | Trie + grid backtracking |
| 14 | Longest Common Prefix | Trie or vertical scan |
| 720 | Longest Word in Dictionary | Trie + BFS |

### Pattern Matching
| # | Problem | Key Concept |
|---|---------|-------------|
| 28 | Find the Index of First Occurrence | KMP or built-in |
| 459 | Repeated Substring Pattern | KMP LPS array trick |
| 187 | Repeated DNA Sequences | Rolling hash or set |
| 1044 | Longest Duplicate Substring | Binary search + rolling hash |

### Advanced
| # | Problem | Key Concept |
|---|---------|-------------|
| 76 | Minimum Window Substring | Sliding window (see SW guide) |
| 3 | Longest Substring Without Repeating | Sliding window |
| 424 | Longest Repeating Character Replacement | Sliding window |
| 271 | Encode and Decode Strings | Length prefix encoding |
| 394 | Decode String | Stack-based parsing |

### Study Order
**Phase 1 (2-3 days):** 242, 49, 125, 5, 208
**Phase 2 (2-3 days):** 211, 647, 28, 459, 14
**Phase 3 (2-3 days):** 212, 187, 394, 1044
