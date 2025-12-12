class Solution(object):
    def minDays(self, bloomDay, m, k):
        """
        :type bloomDay: List[int]
        :type m: int
        :type k: int
        :rtype: int
        """

        def ok(x):
            boquets = 0
            run = 0
            for i in bloomDay:
                run = run + 1 if i <= x else 0
                if run == k:
                    boquets += 1
                    run = 0
            return boquets >= m

        if m * k > len(bloomDay):
            return -1
        low, high = min(bloomDay), max(bloomDay)
        while low < high:
            mid = (low + high) // 2
            if ok(mid):
                high = mid
            else:
                low = mid + 1
        return low
