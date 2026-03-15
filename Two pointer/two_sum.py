# leetcode-167

from typing import List


class Solution:
    # solving to learn two pointer technique
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        j = len(numbers) - 1
        i = 0
        while i < j:
            s = numbers[j] + numbers[i]
            if s == target:
                return [i + 1, j + 1]
            elif s < target:
                i += 1
            else:
                j -= 1
        return []
