- Big O Notation

    - Time Complexity
        - O(1) - Constant Time
            - The algorithm takes the same amount of time regardless of the input size.
            - Example: Accessing an element in an array by index.
        - O(log n) - Logarithmic Time
            - The algorithm's time increases logarithmically as the input size increases.
            - Example: Binary search in a sorted array. 

        - O(n) - Linear Time
            - The algorithm's time increases linearly with the input size.
            - Example: Iterating through an array to find a specific element.
        - O(n log n) - Linearithmic Time
            - The algorithm's time increases in a linearithmic manner, often seen in efficient sorting algorithms.
            - Example: Merge sort or quicksort. 
        - O(n^2) - Quadratic Time
            - The algorithm's time increases quadratically with the input size.
            - Example: Nested loops iterating through an array.
        - O(2^n) - Exponential Time
            - The algorithm's time doubles with each additional element in the input.
            - Example: Recursive algorithms that solve problems by breaking them down into smaller subproblems, like the Fibonacci sequence.
        - O(n!) - Factorial Time
            - The algorithm's time grows factorially with the input size.
            - Example: Generating all permutations of a set of elements.

    - Space Complexity
    
        - O(1) - Constant Space
            - The algorithm uses a fixed amount of space regardless of the input size.
            - Example: Swapping two variables.
        - O(n) - Linear Space
            - The algorithm's space usage increases linearly with the input size.
            - Example: Storing elements in an array or list.
        - O(n^2) - Quadratic Space
            - The algorithm's space usage increases quadratically with the input size.
            - Example: Creating a 2D matrix to store relationships between elements.

    - Rule Book
        - Rule 1: Worst Case Analysis
            - Always analyze the worst-case scenario for time complexity.
            - Example: Searching an array of size n has a worst-case time complexity of O(n), even if the element is found at the beginning. This is because we must consider the scenario where the element is not found or is at the end, and a break statement doesn't change the worst-case analysis.
        - Rule 2: Remove Constants
            - Focus on the highest-order term and ignore constant factors.
            - Example: O(2n) simplifies to O(n), as constants do not significantly affect performance for large input sizes.
        - Rule 3: Different term for Input Size
            - When analyzing algorithms, consider how the input size affects performance.
            - Example: An algorithm that processes an array of size n will have a different complexity than one that processes a linked list of the same size. ALso, if an algorithm has a loop that iterates through an array of size n and another loop that iterates through a linked list of size m, the overall complexity would be O(n + m) rather than O(n * m).
            - This is because the two loops operate independently, and we can analyze their complexities separately.
        - Rule 4: Drop Non-Dominant Terms
            - In big O notation, drop lower-order terms that do not significantly affect performance as input size grows.
            - Example: O(n^2 + n) simplifies to O(n^2).
    - Amortized Analysis
        - Average time complexity over a sequence of operations.
        - Example: Dynamic arrays that resize when they reach capacity, leading to occasional O(n) operations but average O(1) over many insertions.
    - Best, Worst, and Average Cases
        - Best Case: The minimum time required for an algorithm to complete.
            - Example: Finding an element at the beginning of a sorted array.
        - Worst Case: The maximum time required for an algorithm to complete.
            - Example: Searching for an element that is not present in a sorted array.
        - Average Case: The expected time required for an algorithm to complete, considering all possible inputs.
            - Example: Searching for an element in a randomly ordered array.
    - Practical Considerations
        - Real-world performance may differ from theoretical complexity.
        - Factors like hardware, compiler optimizations, and input characteristics can affect performance.
        - Always analyze the algorithm in the context of the specific problem and input data.
    - Common Mistakes
        - Ignoring constant factors and lower-order terms in complexity analysis.
        - Focusing solely on time complexity without considering space complexity.
        - Misunderstanding the difference between average and worst-case scenarios.
        - Overlooking the impact of data structures on algorithm performance.
    - Resources
        - [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
        - [Time Complexity Visualizations](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html)
        - More [here](https://www.cs.usfca.edu/~galles/visualization/)

    

