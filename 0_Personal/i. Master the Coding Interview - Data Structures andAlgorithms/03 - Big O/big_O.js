// Big O Notation - Copilot auto completion
// Big O Notation is a way to describe the performance or complexity of an algorithm.

// O(1) - Constant Time
function logFirstTwo(array){
    console.log(array[0]);
    console.log(array[1]);
}

logFirstTwo(nemo);

// O(n) - Linear Time
function logAll(array){
    for (let i=0; i<array.length;i++){
        console.log(array[i]);
    }
}
logAll(everyone);

// O(log n) - Logarithmic Time
function binarySearch(array, target){
    let left = 0;
    let right = array.length - 1;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (array[mid] === target) {
            return mid; // Found the target
        } else if (array[mid] < target) {
            left = mid + 1; // Search in the right half
        } else {
            right = mid - 1; // Search in the left half
        }
    }
    return -1; // Target not found
}
const sortedArray = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
console.log(binarySearch(sortedArray, 5)); // Should return the index of 5

// O(n log n) - Linearithmic Time
function mergeSort(array) {
    if (array.length <= 1) {
        return array; // Base case: an array of zero or one element is already sorted
    }

    const mid = Math.floor(array.length / 2);
    const left = mergeSort(array.slice(0, mid)); // Sort the left half
    const right = mergeSort(array.slice(mid)); // Sort the right half

    return merge(left, right); // Merge the sorted halves
}
function merge(left, right) {
    const result = [];
    let i = 0;
    let j = 0;

    // Merge the two sorted arrays
    while (i < left.length && j < right.length) {
        if (left[i] < right[j]) {
            result.push(left[i]);
            i++;
        } else {
            result.push(right[j]);
            j++;
        }
    }

    // If there are remaining elements in either array, add them
    return result.concat(left.slice(i)).concat(right.slice(j));
}
const unsortedArray = [38, 27, 43, 3, 9, 82, 10];
console.log(mergeSort(unsortedArray)); // Should return the sorted array

// O(n^2) - Quadratic Time
function logAllPairs(array){
    for (let i=0; i<array.length;i++){
        for (let j=0; j<array.length;j++){
            console.log(array[i], array[j]);
        }
    }
}
logAllPairs(everyone);

// O(n^3) - Cubic Time
function logAllTriples(array){
    for (let i=0; i<array.length;i++){
        for (let j=0; j<array.length;j++){
            for (let k=0; k<array.length;k++){
                console.log(array[i], array[j], array[k]);
            }
        }
    }
}
logAllTriples(everyone);


// O(2^n) - Exponential Time
function fibonacci(n) {
    if (n <= 1) {
        return n; // Base case: return n for 0 or 1
    }
    return fibonacci(n - 1) + fibonacci(n - 2); // Recursive case
}
console.log(fibonacci(5)); // Should return 5 (0, 1, 1, 2, 3, 5)

// O(n!) - Factorial Time
function factorial(n) {
    if (n <= 1) {
        return 1; // Base case: 0! = 1 and 1! = 1
    }
    return n * factorial(n - 1); // Recursive case
}
console.log(factorial(5)); // Should return 120 (5! = 5 * 4 * 3 * 2 * 1)

// O(n^k) - Polynomial Time (where k is a constant)
function polynomialTimeExample(n, k) {
    let result = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            for (let l = 0; l < k; l++) {
                result += i + j + l; // Some operation
            }
        }
    }
    return result;
}
console.log(polynomialTimeExample(3, 2)); // Should return a result based on the nested loops
