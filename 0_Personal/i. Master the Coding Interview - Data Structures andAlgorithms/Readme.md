- Course taken from Telegram | [Link](https://t.me/ZTM_ACADEMY)

1. Introduction

    - 001 Interview-Mind-Map | [Link](https://coggle.it/diagram/W5u8QkZs6r4sZM3J/t/master-the-interview)

    - 001 Technical-Interview-Mind-Map | [Link](https://coggle.it/diagram/W5E5tqYlrXvFJPsq/t/master-the-interview)

2. Getting Mor Interviews

    - Resume

        - One Page
        - Relevant Skills
        - Personalized
        - Online Link

        - Use sites like [jobscan](https://www.jobscan.co/) to check your resume

        - Refer 005 Resources Resume Templates.html

        - Github - Refer htmls

    - LinkedIn
        - Profile Picture
        - Headline
        - Summary
        - Experience
        - Skills
        - Recommendations
        - Endorsements

    - Portfolio

        - Projects
        - GitHub
        - Blog
        - LinkedIn

    - Email

        - Professional
        - Clear Subject
        - Signature

    - 002 Resume-Template | [Link](https://www.resumemaker.online/)

        003 Resume-Cheat-Sheet | [Link](https://github.com/aneagoie/resume-checklist)

        004 JobScan | [Link](https://www.jobscan.co/)

        006 ZTM-Open-Source-Community | [Link](https://github.com/zero-to-masterystart-here-guidelines)

        006 ZTM-Job-Board | [Link](https://github.com/zero-to-mastery/ZtM-Job-Board)

3. Big O

    - Use sites like [repl.it](https://repl.it) and [glot.io](https://glot.io) to practice coding problems

    - 007 Big-O Cheat Sheet | [Link](https://www.bigocheatsheet.com/)

    - Good Code 

        - Readable
        - Efficient
        - Maintainable
        - Scalable: Time and Space Complexity
    - Time Complexity
        - O(1) - Constant Time
            - The algorithm's time remains constant regardless of the input size.
            - Example: Accessing an element in an array by index.
        - O(log n) - Logarithmic Time
            - The algorithm's time increases logarithmically with the input size.
            - Example: Binary search in a sorted array.
        - O(n) - Linear Time
            - The algorithm's time increases linearly with the input size.
            - Example: Iterating through an array to find a specific element.
        - O(n log n) - Linearithmic Time
            - The algorithm's time increases in a combination of linear and logarithmic growth.
            - Example: Efficient sorting algorithms like mergesort and heapsort.
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
            - Example: An algorithm that processes an array of size n will have a different complexity than one that processes a linked list of the same size. Also, if an algorithm has a loop that iterates through an array of size n and another loop that iterates through a linked list of size m, the overall complexity would be O(n + m) rather than O(n * m).
            - This is because the two loops operate independently, and we can analyze their complexities separately.
        - Rule 4: Drop Non-Dominant Terms
            - In big O notation, drop lower-order terms that do not significantly affect performance as input size grows.
            - Example: O(n^2 + n) simplifies to O(n^2).

    # Which code is best?

    | Category  | Icon          | Metric            | Description               |
    |-----------|---------------|-------------------|---------------------------|
    | Readable  | 💎 (Ruby gem) | Readability       | Code is easy to read and understand |
    | Memory    | 💾 (Memory)   | Space Complexity  | Code uses less memory     |
    | Speed     | ⏱️ (Clock)    | Time Complexity   | Code runs faster          |


4. How to Solve Coding Problems

    - Understand the Problem
        - Read the problem statement carefully.
        - Identify inputs and outputs.
        - Clarify any ambiguities.

    - Break Down the Problem
        - Divide the problem into smaller subproblems.
        - Solve each subproblem individually.

    - Plan Your Solution
        - Outline your approach before coding.
        - Consider edge cases and constraints.

    - Write Pseudocode
        - Draft a high-level outline of your solution in pseudocode.
        - Focus on logic rather than syntax.

    - Implement Your Solution
        - Translate your pseudocode into actual code.
        - Use meaningful variable names and comments.

    - Test Your Solution
        - Run test cases to verify correctness.
        - Handle edge cases and unexpected inputs.

    - Optimize Your Solution
        - Analyze time and space complexity.
        - Refactor code for efficiency if necessary.

    - What are companies looking for?
        - Analytic Skills
        - Coding Skills
        - Technical Skills
        - Communication Skills    

5. Data Structures Introduction

    - What is a Data Structure?
        - A data structure is a way of organizing and storing data(collection of values and relationships) in a computer so that it can be accessed and modified efficiently.
    - Why are Data Structures Important?
        - Data structures are essential for efficient data storage, retrieval, and manipulation.
        - They enable algorithms to operate on data effectively.
        - Choosing the right data structure can significantly impact the performance of an application.

    - Types of Data Structures
        - Primitive Data Structures
            - Basic data types like integers, floats, characters, and booleans.
            - Examples: int, float, char, bool in programming languages.
        - Non-Primitive Data Structures
            - More complex structures that can store multiple values or relationships.
            - Examples: Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Hash Tables.

    - Abstract Data Types (ADTs)
        - An abstract data type is a mathematical model for a certain class of data structures that have similar behavior.
        - ADTs define the data and operations on that data without specifying the implementation details.
        - Examples: Stack, Queue, List, Set, Map.
    - Choosing the Right Data Structure
        - Consider the type of data you need to store.
        - Analyze the operations you need to perform on the data.
        - Evaluate time and space complexity for different data structures.
        - Choose a data structure that best fits your requirements.

    - Data Structure Operations
        - Insertion: Adding an element to the data structure.
        - Deletion: Removing an element from the data structure.
        - Searching: Finding an element in the data structure.
        - Traversal: Accessing each element in the data structure.
        - Sorting: Arranging elements in a specific order (e.g., ascending or descending).

    - Data Structure Characteristics
        - Efficiency: How well the data structure performs operations like insertion, deletion, and searching.
        - Flexibility: The ability to adapt to different types of data and operations.
        - Memory Usage: The amount of memory required to store the data structure.
        - Ease of Use: How easy it is to implement and work with the data structure.

    - Data Structure Examples
        - Arrays: A collection of elements stored in contiguous memory locations.
        - Linked Lists: A collection of nodes where each node contains data and a reference to the next node.
        - Stacks: A Last In First Out (LIFO) data structure where elements are added and removed from the top.
        - Queues: A First In First Out (FIFO) data structure where elements are added at the back and removed from the front.
        - Trees: A hierarchical data structure with nodes connected by edges, where each node can have multiple children.
        - Graphs: A collection of nodes (vertices) connected by edges, representing relationships between entities.
        - Hash Tables: A data structure that uses a hash function to map keys to values for efficient retrieval.

    - Data Structure Visualization
        - Visualizing data structures can help understand their structure and operations.
        - Use diagrams, animations, or interactive tools to visualize data structures.
        - Examples: [VisuAlgo](https://visualgo.net/en), [Data Structure Visualizations](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html).

    - Data Structures:

        - How to build them
        - How to use them
        - How to analyze them
        - How to implement them
    - Data Structures in Real Life
        - Data structures are used in various applications, such as databases, search engines, social media platforms, and more.
        - Understanding data structures is crucial for software development, algorithm design, and problem-solving.

    - How Computers Store Data
        - Computers store data in binary format (0s and 1s).
        - Data is organized in memory using various data structures. Computers store data(variables) in RAM (Random Access Memory) and secondary storage devices like hard drives and SSDs.
        - Data structures help manage and organize this data for efficient access and manipulation.
        - The choice of data structure affects how efficiently data can be accessed and manipulated.

        - ie, When a program is run, the computer allocates memory for variables and data structures in RAM, the CPU accesses this memory to read and write data, asking the memory controller to retrieve or store data at specific addresses.

        - How RAM stores data
            - RAM stores data in binary format (0s and 1s).
            - Each memory cell has a unique address.
            - Data is organized in bytes (8 bits) and words (multiple bytes).
            - The CPU accesses RAM to read and write data using memory addresses. 