class Solution(object):
    def splitArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        def ok(x):
            s = 0
            d = 1
            for i in nums:
                s += i
                if s > x:
                    s = i
                    d += 1
                    if d > k:
                        return False
            # print(d,k)
            return True

        low = max(nums)
        high = sum(nums)
        r = 0
        while low < high:
            mid = (low + high) // 2
            if ok(mid):
                high = mid
            else:
                low = mid + 1
        return low
