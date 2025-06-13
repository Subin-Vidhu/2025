def smartest_pair_sum(array, target_sum):
    """
    Checks if there's a pair of numbers in an array that sums up to a given target sum.

    Args:
        array (list): A list of integers.
        target_sum (int): The target sum.

    Returns:
        str: "Yes" if a pair is found, "No" otherwise.
    """
    dictionary = set()
    for item in array:
        comp = target_sum - item
        if comp in dictionary:
            return "Yes"
        dictionary.add(item)
    return "No"

# Example usage:
print(smartest_pair_sum([1, 2, 3, 4, 5], 7))  # Yes (2 + 5 = 7)
print(smartest_pair_sum([1, 2, 3, 4, 5], 10))  # No
print(smartest_pair_sum([10, 20, 30, 40, 50], 60))  # Yes (10 + 50 = 60)
print(smartest_pair_sum([10, 20, 30, 40, 50], 100))  # No