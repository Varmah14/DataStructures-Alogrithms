## Heaps

Six main patterns of heap

1.  Find the kth largest / smallest element
    maintain a heap of size k(min or max based on the condition if largest or smallest is required) and return the root element.
    For kth largest, use a min-heap of size k — the root is your answer. For kth smallest, use a max-heap of size k. Each insertion is O(log k), total O(n log k).

2.  Merge K Sorted Sequences
