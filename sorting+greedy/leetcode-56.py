# 56. Merge Intervals
class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """
        intervals.sort()
        results = [intervals[0]]
        for i in range(1, len(intervals)):
            if results[-1][1] >= intervals[i][0]:
                results[-1][1] = max(intervals[i][1], results[-1][1])
            else:
                results.append(intervals[i])
        return results
        # return intervals
