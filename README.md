# 🚀 Coding Interview Techniques & Algorithms — Playbook & Checklist

A high‑coverage roadmap of patterns + classic algorithms.
Master these and you’ll be able to solve most interview problems quickly and reliably.

---

## 📌 CORE PATTERNS (The 80/20)

1. Two Pointers
   - Use on sorted arrays/strings to converge from ends (dedup, partition, pair sums, Dutch flag).
   - Triggers: sorted + pair/sum; remove duplicates; palindrome check.

2. Sliding Window (fixed/variable)
   - Maintain a window and counts/invariants.
   - Tricks: exactly(K) = atMost(K) − atMost(K−1).
   - Triggers: subarray/substring longest/shortest/number of..., at most/at least K.

3. Prefix Sum / Prefix XOR + Hash Map
   - Convert range queries to O(1); count with differences.
   - Triggers: subarray sum/xor == K; balance +1/−1; range updates.

4. Sorting + Greedy
   - Sort, then make locally optimal choices (interval exchange arguments).
   - Triggers: merge/overlap intervals, meeting rooms, activity selection.

5. Binary Search (index or on answer)
   - Search smallest feasible value with monotone ok(x).
   - Triggers: minimize the maximum / maximize the minimum; capacity/speed; kth element.

6. Monotonic Stack
   - Next greater/smaller, span problems, largest rectangle, daily temps.
   - Triggers: nearest greater L/R; histogram; stock span.

7. Heaps / Priority Queue
   - Pick current best; streaming medians; Dijkstra.
   - Triggers: top‑K, merge K lists, min meeting rooms, scheduling.

8. Hashing / Counting
   - Sets/maps for existence, frequency, dedup, anagrams.
   - Triggers: two‑sum, anagram groups, first unique, frequency buckets.

9. BFS / DFS on Graphs & Grids
   - Components, shortest path in unweighted graphs, flood fill.
   - Triggers: number of islands, word ladder, cycle detection.

10. Union‑Find (Disjoint Set Union)
    - Connectivity, cycle detection, Kruskal MST.
    - Triggers: dynamic connectivity, redundant connection, accounts merge.

11. Trees (Basics + LCA)
    - Traversals, subtree sums, diameters; BST inorder = sorted.
    - Triggers: kth in BST, path sums, distance queries; LCA (binary lifting).

12. Dynamic Programming (Fundamentals)
    - Memo/tabulation for overlapping subproblems & optimal substructure.
    - Families: knapsack, coin change, LIS, LCS/edit distance, grid paths.
    - Triggers: min/max cost/ways; choose/split; sequence alignments.

13. Backtracking / Search with Pruning
    - Generate permutations/combos; constraint search.
    - Triggers: N‑Queens, combination sum, word search, phone keypad.

14. Math & Bit Tricks
    - XOR, bitmasks, popcount, power‑of‑two, GCD/LCM, fast pow, sieve.
    - Triggers: subset enumeration, parity, number theory checks.

15. String Toolbelt
    - KMP/Z for pattern search; rolling hash for duplicates; Trie for prefixes.
    - Triggers: fast substring search, repeated substrings, autocomplete.

---

## 🎯 INTERMEDIATE / HIGH-ROI EXTRAS

16. Monotonic Queue (Deque) — sliding window min/max; DP speedups.
17. Topological Sort + DP on DAGs — scheduling, longest path in DAG.
18. Range DS — Fenwick (BIT), Segment Tree (+ lazy), Sparse Table.
19. Shortest‑Path Variants — Dijkstra, 0‑1 BFS, Bellman‑Ford, Floyd‑Warshall.
20. Flow & Matching — Bipartite matching, Max‑Flow, Min‑cut.
21. Mo’s Algorithm (offline) — near‑linear queries on arrays.
22. Advanced DP Optimizations — Divide‑&‑Conquer DP, Knuth, CHT.
23. Meet‑in‑the‑Middle — split sets, combine subset sums.
24. Suffix Structures & Palindromes — suffix array/automaton, LCP, Manacher.
25. Geometry & Sweep Line — orientation, interval/segment sweep.

---

## 🧭 QUICK MAPPING: Clues → Techniques

- Subarray/substring at most/exactly K → Sliding window; or Prefix+Hash.
- Count subarrays sum==k / xor==k → Prefix + HashMap.
- Min rooms / overlap / merge → Sort + Greedy / Heap.
- Minimize max / maximize min → Binary search on answer.
- Next greater / histogram → Monotonic stack.
- Unweighted shortest path → BFS.
- Weighted shortest path → Dijkstra; {0,1} weights → 0‑1 BFS.
- Kth smallest / running median → Heaps / Quickselect.
- Connectivity / cycles → DSU or DFS.
- Dependencies → Toposort (+ DP on DAG).
- Range query + updates → BIT / SegTree / Sparse Table.
- Generate all with constraints → Backtracking + pruning.
- Longest palindrome → Manacher.
- Duplicate substrings → Rolling hash / Suffix array.

---

## 📚 NOTABLE ALGORITHMS TO PREPARE (One‑Liners)

Graphs & Trees:

- Kruskal MST — sort edges + DSU; O(E log E)
- Prim MST — grow from node via heap; O(E log V)
- Dijkstra — non‑negative weights; O(E log V)
- 0‑1 BFS — deque; O(V+E)
- Bellman‑Ford — handles negative edges; O(VE)
- Floyd‑Warshall — all pairs; O(V^3)
- Tarjan/Kosaraju — strongly connected components
- LCA — binary lifting or Euler+RMQ

Strings:

- Horspool/Boyer‑Moore — pattern search
- KMP — linear substring search
- Rabin–Karp — rolling hash
- Z‑Algorithm — substring matching
- Aho–Corasick — multi‑pattern search
- Manacher — longest palindrome O(n)
- Suffix Array / Automaton — distinct substrings

Range / Arrays / Math:

- Fenwick (BIT) — prefix sums O(log N)
- Segment Tree (+ Lazy) — range queries/updates O(log N)
- Sparse Table — static RMQ O(1)
- Quickselect — kth element O(n) avg
- Patience Sorting — LIS O(n log n)
- Euclid GCD / Extended GCD
- Fast Exponentiation — O(log n)
- Sieve of Eratosthenes — primes
- Sweep Line — interval/geometry

---

## 🧩 REUSABLE MINI‑TEMPLATES (Pseudocode)

Sliding Window (at least K):

```
ans = 0; left = 0
for right in [0..n):
add nums[right] to window
while predicate(window) is true:
ans += n - right
remove nums[left]
left += 1
return ans
```

Prefix Sum + HashMap (sum == K):

```
count = {0:1}; pref = 0; ans = 0
for x in nums:
pref += x
ans += count.get(pref - K, 0)
count[pref] = count.get(pref, 0) + 1
return ans
```

Binary Search on Answer:

```
lo, hi = min_possible, max_possible
while lo < hi:
mid = (lo + hi) // 2
if ok(mid):
hi = mid
else:
lo = mid + 1
return lo
```

## ✅ MASTERY CHECKLIST

Global Readiness:

- Map clues → technique within 10–20s
- Implement key patterns in <5 min
- Implement DSU, Dijkstra, KMP, SegTree from memory
- Explain time/space & edge cases

Per‑Technique:

- Learn concept + invariants
- Implement from scratch (clean API, tests)
- Solve: 3 Easy, 4 Medium, 2 Hard
- List edge cases
- 2‑minute whiteboard explanation
- Flashcards for triggers/pitfalls

---

## 🧠 COMPLEXITY & CONSTRAINTS HEURISTICS

- n ≈ 1e5 → aim O(n) or O(n log n); avoid O(n^2)
- Use monotonicity → binary search on answer
- Prefer hash maps over arrays for large ranges
- Pre‑sort when greedy needs order; avoid re‑sorting

---

## 📌 OPTIONAL ADVANCED TOPICS

- Heavy‑Light Decomposition (tree paths)
- Euler Tour + RMQ
- Persistent Segment Trees, Treaps/AVL
- Dinic vs. Edmonds‑Karp (Max Flow)
- A\* heuristics, Centroid Decomposition
- Mo’s Algorithm + Hilbert Order

---
