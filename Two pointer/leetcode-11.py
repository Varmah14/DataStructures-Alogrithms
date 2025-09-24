# 11. Container With Most Water

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        right = len(height) - 1
        left = 0
        area = 0
        while left < right:
            s = min(height[left],height[right]) * (right - left) 
            if area < s:
                area = s
            if height[right] > height[left]:
                left +=1
            else:
                right -= 1
        return area