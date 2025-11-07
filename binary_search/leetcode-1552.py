class Solution(object):
    def maxDistance(self, positions, m):
        positions.sort()
        """
        :type position: List[int]
        :type m: int
        :rtype: int
        """

        def ok(dist):
            placed = 1
            last = positions[0]
            for p in positions[1:]:
                if p - last >= dist:
                    placed += 1
                    last = p
                    if placed == m:
                        return True
            return False

        low, high = 1, positions[-1] - positions[0]
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if ok(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans
