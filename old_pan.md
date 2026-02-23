<!-- Banner -->
<div align="center">

# 🚀 Coding Interview Techniques & Algorithms

### _A Playbook & Checklist for Mastery_

<img src="https://img.shields.io/badge/Data%20Structures-Algorithms-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Topic-Interview%20Prep-brightgreen?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Focus-Problem%20Solving-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Language-Python%2FJava%2FC++-yellow?style=for-the-badge"/>

</div>

---

A high-coverage roadmap of **patterns + classic algorithms**.  
Master these and you’ll be able to solve most interview problems **quickly and reliably**.

---

## 📌 Core Patterns (the 80/20)

### 1️⃣ Two Pointers

- Use on sorted arrays/strings to converge from ends: dedup, partition, pair sums, Dutch flag.
- **Triggers:** sorted + pair/sum; remove duplicates; palindrome check.

### 2️⃣ Sliding Window (fixed/variable)

- Maintain a window and counts/invariants.
- 💡 Trick: `exactly(K) = atMost(K) − atMost(K−1)`
- **Triggers:** subarray/substring longest/shortest/number of..., _at most/at least K_.

### 3️⃣ Prefix Sum / Prefix XOR + Hash Map

- Convert range queries to O(1) checks; count with differences.
- **Triggers:** subarray sum/xor == K; balance +1/−1; range updates.

### 4️⃣ Sorting + Greedy

- Sort, then make locally optimal choices (interval exchange arguments).
- **Triggers:** merge/overlap intervals, meeting rooms, activity selection.

### 5️⃣ Binary Search (index or on answer)

- Search smallest feasible value with monotone `ok(x)`.
- **Triggers:** minimize the maximum / maximize the minimum; capacity/speed; kth element.

---

## 🧭 Quick Mapping (Clues → Techniques)

| Problem Clue                         | Technique                     |
| ------------------------------------ | ----------------------------- |
| subarray/substring at most/exactly K | Sliding Window OR Prefix+Hash |
| count subarrays sum==k / xor==k      | Prefix + HashMap              |
| min rooms / overlap / merge          | Sort+Greedy OR Heap           |
| minimize max / maximize min          | Binary Search on Answer       |
| next greater / histogram             | Monotonic Stack               |
| unweighted shortest path             | BFS                           |
| weighted shortest path               | Dijkstra / 0-1 BFS            |
| kth smallest / running median        | Heaps / Quickselect           |
| connectivity / cycles                | DSU or DFS                    |
| dependencies                         | Toposort (+ DP on DAG)        |
| range query + updates                | BIT / Segment Tree            |
| generate all with constraints        | Backtracking + pruning        |
| longest palindrome                   | Manacher                      |
| duplicate substrings                 | Rolling Hash / Suffix Array   |

---

## 📆 4-Week Practice Plan

- **Week 1:** Arrays/Strings → Two Pointers, Sliding Window, Prefix+Hash, Monotonic Stack
- **Week 2:** Greedy/Search → Sorting+Greedy, Binary Search on Answer, Heaps
- **Week 3:** Graphs/Trees → BFS/DFS, DSU, Dijkstra/0-1 BFS, Trees+LCA
- **Week 4:** DP & Range → Knapsack, LIS, LCS/Edit Distance, BIT/Segment Tree

🎯 Bonus: Rotate Strings (KMP, Horspool) + 1 Advanced topic each week.

---

## ✅ Mastery Checklist

- [ ] Map problem clues → correct technique within 10–20 sec
- [ ] Write sliding window & prefix-sum+hash from scratch in <5 min
- [ ] Implement DSU, Dijkstra, KMP, Segment Tree from memory
- [ ] Explain time/space complexity & edge cases

---

## 🧠 Complexity Heuristics

- \( n \approx 1e5 \) → target O(n) or O(n log n). Avoid O(n²).
- Use monotonicity → binary search on answer.
- Prefer hash maps over arrays for large ranges.
- Pre-sort if greedy needs order; avoid re-sorting inside loops.

---

## 📌 Optional Advanced Topics

- Heavy-Light Decomposition, Euler Tour + RMQ
- Persistent Segment Trees, Treaps/AVL
- Dinic vs. Edmonds-Karp (Max Flow)
- A\* search heuristics, Centroid Decomposition
- Mo’s + Hilbert Order

---

<div align="center">

✨ _Tip: Build a personal **pattern → template** snippet library._  
🔥 _Redo 10 favorite problems per pattern a week before interviews._

</div>
