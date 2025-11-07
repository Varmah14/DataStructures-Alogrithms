class Solution(object):
    def shipWithinDays(self, weights, days):
        """
        :type weights: List[int]
        :type days: int
        :rtype: int
        """

        def ok(x):
            weight = 0
            day = 1
            for i in weights:
                weight += i
                if weight > x:
                    weight = i
                    day += 1
            return day <= days

        lo, high = max(weights), sum(weights)
        while lo < high:
            mid = (lo + high) // 2
            if ok(mid):
                high = mid
            else:
                lo = mid + 1
        return lo
