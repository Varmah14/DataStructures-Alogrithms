# 435. Non-overlapping Intervals

class Solution(object):
    def eraseOverlapIntervals(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """
        # 56. Merge Intervals
        def myFunc(l):
            return l[1]

        intervals.sort(key = myFunc)
        count = 0
        results = [intervals[0]]
        print(intervals)
        for i in range(1, len(intervals)):
            if results[-1][1] > intervals[i][0]:
                count+=1
                # results[-1][1] = max(intervals[i][1],results[-1][1])
            else:
                results.append(intervals[i])
        return count
        # return intervals
