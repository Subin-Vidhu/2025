- Course taken from Telegram | [Link](https://t.me/ZTM_ACADEMY)

1. Introduction

    - 001 Interview-Mind-Map | [Link](https://coggle.it/diagram/W5u8QkZs6r4sZM3J/t/master-the-interview)

    - 001 Technical-Interview-Mind-Map | [Link](https://coggle.it/diagram/W5E5tqYlrXvFJPsq/t/master-the-interview)

2. Getting More Interviews

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

        - `Readable`
        - Efficient
        - Maintainable
        - `Scalable`: Time and Space Complexity
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

6. Data Structures Arrays

    - What is an Array?
        - An array is a collection of elements stored in contiguous memory locations.
        - Each element can be accessed using an index, which represents its position in the array.

        - eg:

            - ```Strings = ["Hello", "World", "Python"]```, this takes 3 memory locations, each containing a string, each string takes 4 bytes of memory, so the total memory used is 12 bytes.
            - ```Numbers = [1, 2, 3, 4, 5]```, this takes 5 memory locations, each containing an integer, each integer takes 4 bytes of memory, so the total memory used is 20 bytes.
            - ```Booleans = [True, False, True]```, this takes 3 memory locations, each containing a boolean value, each boolean takes 1 byte of memory, so the total memory used is 3 bytes.
            - ```Mixed = [1, "Hello", True]```, this takes 3 memory locations, each containing a different data type, the total memory used is 4 + 4 + 1 = 9 bytes.

        - Optional Classes

            - Reference Types
                - Classes are reference types, meaning they store a reference to the object in memory rather than the actual object itself.
                - When you create an instance of a class, it is stored in the heap memory, and the variable holds a reference to that memory location.
                - eg: 
                    - ```python
                      class Person:
                          def __init__(self, name):
                              self.name = name

                      person1 = Person("Alice")
                      person2 = person1  # person2 holds a reference to the same object as person1
                      print(person1.name)  # Output: Alice
                      print(person2.name)  # Output: Alice
                      ```

            - Context vs Scope
                - Context refers to the `environment in which a piece of code is executed`(ie, it tells you where you are within the object, in js, it refers to the value of `this`), while scope refers to the visibility and accessibility of variables and functions within that context.
                - In JavaScript, the context is determined by how a function is called, while the scope is determined by where a variable is declared.
                - a simple trick is to use `console.log(this)` to see the context of the current function, `what is to the left of the dot` is the context, and `what is to the right of the dot` is the scope.
                - In Python, the context is determined by the class or module in which a function is defined, while the scope is determined by the indentation level of the code.
                - eg:
                    - ```javascript
                      function showContext() {
                          console.log(this);
                      }

                      const obj = {
                          name: "Alice",
                          show: showContext
                      };

                      obj.show();  // Output: { name: 'Alice', show: [Function: showContext] }, this refers to the obj object and the showContext function is called on the obj object, so this refers to the obj object. 
                      ```
                    - ```python
                      class Person:
                          def show_context(self):
                              print(self)

                      person = Person()
                      person.show_context()  # Output: <__main__.Person object at 0x...>
                      # The self parameter refers to the instance of the class, and it is used to access the attributes and methods of the class.
                      # the scope here is the class Person, and the context is the instance of the class Person.
                      ```
            - Instantiation
                - Instantiation is the process of creating an instance of a class.
                - In Python, you create an instance of a class by calling the class as if it were a function.
                - In JavaScript, you create an instance of a class using the `new` keyword.
                - eg:
                    - ```python
                      class Dog:
                          def __init__(self, name):
                              self.name = name

                      my_dog = Dog("Buddy")  # Instantiation in Python
                      print(my_dog.name)  # Output: Buddy
                      ```
                    - ```javascript
                      class Dog {
                          constructor(name) {
                              this.name = name;
                          }
                      }

                      const myDog = new Dog("Buddy");  // Instantiation in JavaScript
                      console.log(myDog.name);  // Output: Buddy
                      ```

7. Data Structures Hash Tables

    - What is a Hash Table?
        - A hash table is a data structure that maps keys to values using a hash function.
        - It allows for efficient data retrieval and storage by using a unique key to access the corresponding value.

    - How Does a Hash Table Work?
        - A hash function takes an input (key) and produces a fixed-size output (hash code).
        - The hash code is used to determine the index in the hash table where the value will be stored.
        - When retrieving a value, the same hash function is applied to the key to find the corresponding index.

    - Advantages of Hash Tables
        - Fast data retrieval: Average time complexity for search, insert, and delete operations is O(1).
        - Efficient memory usage: Hash tables can dynamically resize to accommodate more elements.
        - Flexible key-value pairs: Keys can be of any data type, allowing for versatile data storage.

    - Index, lookup, delete, search - all have a time complexity of O(1) on average.
    - Disadvantages of Hash Tables
        - Hash collisions: When two different keys produce the same hash code, leading to potential data loss or retrieval issues.
        - Memory overhead: Hash tables may require more memory than other data structures due to their dynamic resizing and storage of keys and values.
        - Not ordered: Hash tables do not maintain the order of elements, making them unsuitable for scenarios where order matters.
    - Hash Collisions
        - A hash collision occurs when two different keys produce the same hash code.
        - To handle collisions, hash tables use techniques like chaining (linked lists) or open addressing (probing).
        - Chaining: Each index in the hash table points to a linked list of key-value pairs.
        - Open Addressing: When a collision occurs, the algorithm searches for the next available index.

    - Example of a Hash Table
        - ```python
          class HashTable:
              def __init__(self):
                  self.table = [None] * 10  # Initialize a hash table with 10 slots

              def hash_function(self, key):
                  return hash(key) % len(self.table)  # Simple hash function

              def insert(self, key, value):
                  index = self.hash_function(key)
                  if self.table[index] is None:
                      self.table[index] = []
                  self.table[index].append((key, value))  # Store key-value pair

              def search(self, key):
                  index = self.hash_function(key)
                  if self.table[index] is not None:
                      for k, v in self.table[index]:
                          if k == key:
                              return v
                  return None  # Key not found

          ht = HashTable()
          ht.insert("name", "Alice")
          ht.insert("age", 30)
          print(ht.search("name"))  # Output: Alice
          print(ht.search("age"))   # Output: 30
          ```

    - Real-World Applications of Hash Tables
        - Hash tables are widely used in various applications, including:
            - Caching: Storing frequently accessed data for quick retrieval.
            - Database indexing: Efficiently mapping keys to records in a database.
            - Symbol tables in compilers: Associating variable names with their values.
            - Implementing sets and dictionaries in programming languages.

    - Hash Tables vs Arrays
        - Hash tables provide faster data retrieval compared to arrays, especially for large datasets.
        - Arrays have a fixed size and require resizing when full, while hash tables can dynamically resize.
        - Arrays maintain the order of elements, while hash tables do not.
        - The time complexity for search, insert, and delete operations in arrays is O(n) in the worst case, while hash tables have an average time complexity of O(1).

8. Data Structures Linked Lists

    - What is a Linked List?
        - A linked list is a data structure consisting of nodes, where each node contains data and a reference (or pointer) to the next node in the sequence.
        - Unlike arrays, linked lists do not require contiguous memory allocation, allowing for dynamic resizing.

    - Types of Linked Lists
        - Singly Linked List: Each node points to the next node, and the last node points to null.
        - Doubly Linked List: Each node has two pointers, one to the next node and one to the previous node.
        - Circular Linked List: The last node points back to the first node, forming a circle.

    - Advantages of Linked Lists
        - Dynamic size: Linked lists can grow and shrink in size as needed.
        - Efficient insertions/deletions: Adding or removing nodes is more efficient than in arrays, especially for large datasets.

    - Disadvantages of Linked Lists
        - Memory overhead: Each node requires additional memory for the pointer(s).
        - Sequential access: Linked lists do not support random access, making certain operations slower.

    - Example of a Singly Linked List
        - ```python
          class Node:
              def __init__(self, data):
                  self.data = data
                  self.next = None

          class LinkedList:
              def __init__(self):
                  self.head = None

              def insert(self, data):
                  new_node = Node(data)
                  new_node.next = self.head
                  self.head = new_node

              def display(self):
                  current = self.head
                  while current:
                      print(current.data, end=" -> ")
                      current = current.next
                  print("None")

          ll = LinkedList()
          ll.insert(3)
          ll.insert(2)
          ll.insert(1)
          ll.display()  # Output: 1 -> 2 -> 3 -> None
          ```

    - Real-World Applications of Linked Lists
        - Linked lists are used in various applications, including:
            - Implementing stacks and queues.
            - Managing memory in dynamic data structures.
            - Representing graphs and adjacency lists.

    - Conclusion
        - Linked lists are a fundamental data structure with various applications in computer science.
        - Understanding linked lists is crucial for mastering more complex data structures and algorithms.

    - Pointer

        - A pointer is a variable that stores the memory address of another variable or object.
        - In linked lists, pointers are used to connect nodes, allowing traversal and manipulation of the list.
        - Pointers can be null, indicating the end of the list or the absence of a node.

    - Garbage Collection

        - Garbage collection is the automatic process of reclaiming memory occupied by objects that are no longer in use.
        - In languages like Python and Java, garbage collectors periodically check for unreachable objects and free their memory.
        - In C and C++, developers must manually manage memory allocation and deallocation using functions like `malloc` and `free`.

        - Example of Garbage Collection in Python
            - ```python
              class Node:
                  def __init__(self, data):
                      self.data = data
                      self.next = None

              class LinkedList:
                  def __init__(self):
                      self.head = None

              ll = LinkedList()
              ll.head = Node(1)
              ll.head.next = Node(2)
              ll.head.next.next = Node(3)

              # After this point, the linked list nodes will be automatically garbage collected when they are no longer referenced.
              ```

    - External Resources
        - [GeeksforGeeks - Linked List](https://www.geeksforgeeks.org/data-structures/linked-list/)
        - [VisuAlgo - Linked List](https://visualgo.net/en/list)
        