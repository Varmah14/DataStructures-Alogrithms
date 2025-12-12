import math


class Solution(object):
    def minEatingSpeed(self, piles, h):
        def ok(x):
            hours = 0
            for p in piles:
                hours += (p + x - 1) // x  # integer ceil
            return hours <= h

        lo, hi = 1, max(piles)

        while lo < hi:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo
