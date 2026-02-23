# Heap Pattern Templates (Python)

Pattern 1: Top-K (Min-Heap of Size K)
This is the most common heap pattern. Maintain a min-heap of size k — anything smaller gets evicted.

```
import heapq

def top_k_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # evict the smallest
    return heap  # heap[0] is the kth largest

# For top-k smallest → use max-heap (negate values)
def top_k_smallest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)
        if len(heap) > k:
            heapq.heappop(heap)
    return [-x for x in heap]

```

When to use: "kth largest", "k most frequent", "k closest". Anything asking for k best out of n.

Pattern 2: Max-Heap via Negation
Python only has min-heap. Negate to simulate max-heap.

```
import heapq

# Max-heap operations
max_heap = []
heapq.heappush(max_heap, -val)        # push
top = -max_heap[0]                      # peek max
top = -heapq.heappop(max_heap)         # pop max

# With tuples (sort by first element negated)
# e.g., max-heap by frequency, tiebreak by word
heapq.heappush(heap, (-freq, word))
```

Pattern 3: Custom Ordering with Tuples
Heapq compares tuples lexicographically. Use this to your advantage.

```
import heapq

# (priority, tiebreaker_counter, actual_object)
# counter prevents comparing non-comparable objects
counter = 0
heap = []

def push(heap, priority, item):
    global counter
    heapq.heappush(heap, (priority, counter, item))
    counter += 1

# Example: task scheduling by processing time, then by arrival
# heappush(heap, (processing_time, arrival_time, task_id))
```

Why the counter? If two items have the same priority and the item itself isn't comparable (e.g., a ListNode), Python throws an error. The counter is always unique, so comparison never reaches the item.

Pattern 4: Merge K Sorted Sequences

```
import heapq

def merge_k_sorted(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            # (value, list_index, element_index)
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_i, elem_i = heapq.heappop(heap)
        result.append(val)
        if elem_i + 1 < len(lists[list_i]):
            next_val = lists[list_i][elem_i + 1]
            heapq.heappush(heap, (next_val, list_i, elem_i + 1))
    return result

# For linked lists (LC 23):
# Push (node.val, counter, node) — counter as tiebreaker
# On pop, push node.next if it exists
Complexity: O(N log k) where N = total elements, k = number of lists. The heap never exceeds size k.
```

Pattern 5: Two-Heap for Running Median

```
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated) — left half
        self.hi = []  # min-heap — right half

    def addNum(self, num):
        # Always push to max-heap first, then balance
        heapq.heappush(self.lo, -num)
        # Move the max of lo to hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # If hi is bigger, move one back
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

Invariant: len(lo) == len(hi) or len(lo) == len(hi) + 1. The lo max-heap stores the smaller half, hi min-heap stores the larger half. Median is always accessible from the tops.

Pattern 6: Lazy Deletion
When you can't do decrease-key (Python heapq doesn't support it), push a new entry and skip stale ones on pop.

```
import heapq

heap = []
removed = set()  # or a dict tracking valid entries

def add(val, id):
    heapq.heappush(heap, (val, id))

def remove(id):
    removed.add(id)

def pop_valid():
    while heap:
        val, id = heapq.heappop(heap)
        if id not in removed:
            return val, id
    return None

# Used in: Dijkstra, sliding window median, any problem
# where entries become invalid but you can't remove from heap
```

Pattern 7: Dijkstra (Min-Heap + Lazy Deletion)

```
import heapq

def dijkstra(graph, src, n):
    # graph: adjacency list, graph[u] = [(v, weight), ...]
    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:  # stale entry — skip (lazy deletion)
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist

```

The if d > dist[u]: continue line is the lazy deletion. Without it, you'd process the same node multiple times. This single check is what makes Dijkstra with a plain heap correct and efficient.

Pattern 8: Greedy Scheduling (Sort + Heap)

```
import heapq

def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])  # sort by start
    heap = []  # tracks end times of ongoing meetings

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # reuse the room
        heapq.heappush(heap, end)

    return len(heap)  # heap size = rooms needed

# Generalized pattern:
# 1. Sort events by some criteria (usually start time)
# 2. Heap tracks the "state" of active resources
# 3. Pop from heap when a resource is freed
# 4. Push new state
# 5. Answer is often max heap size or final heap state
```

Pattern 9: Greedy — Always Pick Best Available

```
import heapq

# "Connect ropes" / "Huffman-style" — always merge two smallest
def min_cost_connect(ropes):
    heapq.heapify(ropes)  # O(n)
    total = 0
    while len(ropes) > 1:
        a = heapq.heappop(ropes)
        b = heapq.heappop(ropes)
        cost = a + b
        total += cost
        heapq.heappush(ropes, cost)
    return total

# "Reorganize string" — always place the most frequent char
def reorganize(s):
    freq = Counter(s)
    heap = [(-cnt, ch) for ch, cnt in freq.items()]
    heapq.heapify(heap)
    result = []
    prev = (0, '')  # previously used char (cooling off)

    while heap:
        cnt, ch = heapq.heappop(heap)
        result.append(ch)
        if prev[0] < 0:  # previous char still has count left
            heapq.heappush(heap, prev)
        prev = (cnt + 1, ch)  # decrement (remember it's negated)

    return ''.join(result) if len(result) == len(s) else ""
```

Pattern 10: Heap with Lazy Expansion (K Pairs / K-way)
For problems where the full search space is huge but you only need top-k results.

```
import heapq

def k_smallest_pairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []

    heap = [(nums1[0] + nums2[0], 0, 0)]
    visited = {(0, 0)}
    result = []

    while heap and len(result) < k:
        total, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])

        # Expand neighbors — only push what you might need next
        if i + 1 < len(nums1) and (i + 1, j) not in visited:
            heapq.heappush(heap, (nums1[i+1] + nums2[j], i+1, j))
            visited.add((i + 1, j))
        if j + 1 < len(nums2) and (i, j + 1) not in visited:
            heapq.heappush(heap, (nums1[i] + nums2[j+1], i, j+1))
            visited.add((i, j + 1))

    return result
```

Key insight: You don't generate all pairs. You expand lazily from the smallest, only pushing adjacent candidates. The heap stays small.
