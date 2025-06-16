#Given two sorted arrays, we need to merge them and create one big sorted array.
#For example, array1 = [1,3,5,7], array2 = [2,4,6,8]
#The result should be array = [1,2,3,4,5,6,7,8]

#One solution can be : we compare the corresponding elements of both arrays
#We add the smaller element to a new array and increment the index of the array from which the element was added.
#Again we compare the elements of both arrays and repeat the procedure until all the elements have been added.

def merge(array1, array2):
    new_array = []
    flag = 0
    first_array_index = second_array_index = 0
    while not (first_array_index>=len(array1) or second_array_index>=len(array2)): #The loop runs until we reach the end of either of the arrays
        if array1[first_array_index] <= array2[second_array_index]:
            new_array.append(array1[first_array_index])
            first_array_index += 1
        else:
            new_array.append(array2[second_array_index])
            second_array_index += 1

    if first_array_index==len(array1): #When the loop finishes, we need to know which array's end was reached, so that the remaining elements of the other array can be appended to the new array
        flag = 1 #This flag will tell us if we reached the end of the first array or the second array

    if flag == 1: #If the end of the first array was reached, the remaining elements of the second array are added to the new array
        for item in array2[second_array_index:]:
            new_array.append(item)
    else: #And if the end of the second array was reached, the remaining elements of the first array are added to the new array
        for item in array1[first_array_index:]:
            new_array.append(item)

    return new_array

array1 = [1,3,5,7]
array2 = [2,4,6,8,10,12]
print(merge(array1,array2))
#[1, 2, 3, 4, 5, 6, 7, 8, 10, 12]


# #The time complexity of this algorithm is O(n) where n is the total number of elements in both arrays.
# #The space complexity is also O(n) because we are creating a new array of the same size as the total number of elements in both arrays.
# #This is the most efficient way to merge two sorted arrays.
# #Another way to do this is to use the built-in sorted function in Python.
def merge_sorted(array1, array2):
    return sorted(array1 + array2)  # This combines both arrays and sorts them in one go.
array1 = [1, 3, 5, 7]
array2 = [2, 4, 6, 8, 10, 12]   
print(merge_sorted(array1, array2))
# #This method is also O(n log n) in time complexity because of the sorting operation, and O(n) in space complexity.

# #However, it is not as efficient as the first method because it does not take advantage of the fact that both arrays are already sorted.
# #So, the first method is the best way to merge two sorted arrays.

# to remove flag variable
def merge(array1, array2):
    new_array = []
    first_array_index = second_array_index = 0

    # Merge smaller elements first
    while first_array_index < len(array1) and second_array_index < len(array2):
        if array1[first_array_index] <= array2[second_array_index]:
            new_array.append(array1[first_array_index])
            first_array_index += 1
        else:
            new_array.append(array2[second_array_index])
            second_array_index += 1

    # Append the remaining elements, if any
    new_array.extend(array1[first_array_index:])
    new_array.extend(array2[second_array_index:])

    return new_array

array1 = [1, 3, 5, 7]
array2 = [2, 4, 6, 8, 10, 12]
print(merge(array1, array2))

# This version of the merge function eliminates the need for a flag variable by directly extending the new_array with the remaining elements from either array after the main loop.
# The time complexity remains O(n) and the space complexity is also O(n).
# The code is now cleaner and more efficient without the flag variable.
# # This is a more Pythonic way to handle the merging of the two arrays.

# instead of extending the new_array, we can also use the `+=` operator
def merge(array1, array2):
    new_array = []
    first_array_index = second_array_index = 0

    # Merge smaller elements first
    while first_array_index < len(array1) and second_array_index < len(array2):
        if array1[first_array_index] <= array2[second_array_index]:
            new_array.append(array1[first_array_index])
            first_array_index += 1
        else:
            new_array.append(array2[second_array_index])
            second_array_index += 1

    # Append the remaining elements, if any
    new_array += array1[first_array_index:]
    new_array += array2[second_array_index:]

    return new_array
array1 = [1, 3, 5, 7]
array2 = [2, 4, 6, 8, 10, 12]
print(merge(array1, array2))
# This version uses the `+=` operator to append the remaining elements from both arrays, which is also a clean and efficient way to handle the merging. 
# The time complexity remains O(n) and the space complexity is also O(n).
# This is a more Pythonic way to handle the merging of the two arrays.
# This is a more Pythonic way to handle the merging of the two arrays.
