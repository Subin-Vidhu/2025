from typing import List
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        Returns the indices of the two numbers in the list that add up to the target.

        Args:
        numbers (list[int]): A list of integers.
        target (int): The target sum.

        Returns:
        list[int]: A list containing the 1-indexed positions of the two numbers.
        """
        num_map = {}
        
        for i, num in enumerate(numbers):
            complement = target - num
            if complement in num_map:
                return [num_map[complement] + 1, i + 1]
            num_map[num] = i
        
        return None


# Example usage:
solution = Solution()
numbers = [2, 7, 11, 15]
target = 26
result = solution.twoSum(numbers, target)
print(result)  # Output: [3, 4] (1-indexed positions of 11 and 15)
# Example usage with a different input
numbers = [1, 2, 3, 4, 5]
target = 6
result = solution.twoSum(numbers, target)
print(result)  # Output: [1, 5] (1-indexed positions of 1 and 5)