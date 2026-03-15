arr = []
arr.append(1)
arr.pop()

dict = {}
dict[0] = 1
dict.get(2, 0)
for key, value in dict.items():
    pass

# set
s = set()
s.add(1)
s.remove(1)

# counter


# stack

stack = []
stack.append(1)
stack.pop()

from collections import deque

queue = deque()
queue.append(1)
queue.popleft()

import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappop(heap)
