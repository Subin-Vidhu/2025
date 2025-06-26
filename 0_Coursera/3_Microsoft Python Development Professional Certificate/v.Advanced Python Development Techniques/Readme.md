- Week 1

    - [Advanced Python data structures I: Stacks and queues](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/HUSwc/advanced-python-data-structures-i-stacks-and-queues)

    - [Advanced Python data structures II: Graphs, trees, linked lists](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/JEueg/advanced-python-data-structures-ii-graphs-trees-linked-lists)

    - [Decorator, generator, and context manager patterns](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/AYnyd/building-a-timer-decorator-track-your-functions-speed)

    - [Metaprogramming](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/ukbqh/metaprogramming-use-cases-beyond-the-basics)

- Week 2

    - [Effective Prompts](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/svEnx/best-practices-for-effective-prompts-with-genai)

- Week 3 : Just did the assignment

- Week 4:

    - Documentation

        - Inline comments
        - Type hints
        - Readme files

    - Automating Documentation Tasks

        - [Sphinx](https://www.sphinx-doc.org/en/master/)
        - [MkDocs](https://www.mkdocs.org/)
        - [pdoc](https://pdoc3.github.io/pdoc/)

    - Clean Code

        - Readability
        - Simplicity
        - Modularity
        - Testability
        - Maintainability

        - [Solid Principles](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/gewNr/solid-principles-building-robust-and-flexible-code)

            - Single Responsibility Principle (SRP):
                - A class should have only one reason to change, meaning it should only have one job or responsibility. 
                - This principle helps in reducing the complexity of the code and makes it easier to maintain.
                - eg:
                    ```python
                    class User:
                        def __init__(self, name):
                            self.name = name

                        def save(self):
                            # code to save user to database
                            pass

                        def send_email(self, message):
                            # code to send email
                            pass
                    ```
                    - In the above example, the `User` class has two responsibilities: saving the user to the database and sending an email.
                    - To adhere to the SRP, we can refactor the code as follows:
                    ```python
                    class User:
                        def __init__(self, name):
                            self.name = name

                        def save(self):
                            # code to save user to database
                            pass

                    class EmailService:
                        def send_email(self, user, message):
                            # code to send email
                            pass
                    ```
            - Open/Closed Principle (OCP):
                - Software entities (classes, modules, functions, etc.) should be open for extension but closed for modification.
                - This means you should be able to add new functionality without changing existing code.
                - eg:
                    ```python
                    class Shape:
                        def area(self):
                            pass

                    class Rectangle(Shape):
                        def __init__(self, width, height):
                            self.width = width
                            self.height = height

                        def area(self):
                            return self.width * self.height

                    class Circle(Shape):
                        def __init__(self, radius):
                            self.radius = radius

                        def area(self):
                            return 3.14 * self.radius * self.radius
                    ```
                - In the above example, the `Shape` class is open for extension (you can add new shapes like `Circle`, `Rectangle`, etc.) but closed for modification (you don't need to change the `Shape` class to add new shapes).

            - Liskov Substitution Principle (LSP):
                - Objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.
                - This means that subclasses should extend the behavior of the superclass without changing its expected behavior.
                - eg:
                    ```python
                    class Bird:
                        def fly(self):
                            return "Flying"

                    class Sparrow(Bird):
                        def fly(self):
                            return "Sparrow flying"

                    class Ostrich(Bird):
                        def fly(self):
                            raise Exception("Ostriches can't fly")
                    ```
                - In this example, `Ostrich` violates LSP because it cannot be substituted for `Bird` without causing an error. if a function expects a `Bird` and receives an `Ostrich`, it will fail when trying to call the `fly` method.
                - To adhere to LSP, we can refactor the code as follows:
                    ```python
                    class Bird:
                        def move(self):
                            return "Moving"

                    class FlyingBird(Bird):
                        def fly(self):
                            return "Flying"

                    class Sparrow(FlyingBird):
                        def fly(self):
                            return "Sparrow flying"

                    class Ostrich(Bird):
                        def run(self):
                            return "Running"
                    ```

                    - This way, `Sparrow` can be substituted for `FlyingBird`, and `Ostrich` can be used without violating the expected behavior of `Bird`.


            - Interface Segregation Principle (ISP):
                - Clients should not be forced to depend on interfaces they do not use.
                - This means that interfaces should be small and specific to the client’s needs, rather than large and general-purpose.
                - eg:
                    ```python
                    class Printer:
                        def print(self):
                            pass

                        def scan(self):
                            pass

                    class SimplePrinter(Printer):
                        def print(self):
                            return "Printing"

                    class MultiFunctionPrinter(Printer):
                        def print(self):
                            return "Printing"

                        def scan(self):
                            return "Scanning"
                    ```
                - In this example, `SimplePrinter` does not need the `scan` method, but it is forced to implement it because it inherits from `Printer`. To adhere to ISP, we can refactor the code as follows:
                    ```python
                    class Printer:
                        def print(self):
                            pass

                    class Scanner:
                        def scan(self):
                            pass

                    class SimplePrinter(Printer):
                        def print(self):
                            return "Printing"

                    class MultiFunctionPrinter(Printer, Scanner):
                        def print(self):
                            return "Printing"

                        def scan(self):
                            return "Scanning"
                    ```

            - Dependency Inversion Principle (DIP):
                - High-level modules should not depend on low-level modules. Both should depend on abstractions.
                - Abstractions should not depend on details. Details should depend on abstractions.
                - This means that you should depend on interfaces or abstract classes rather than concrete implementations.
                - eg:
                    ```python
                    class Database:
                        def connect(self):
                            pass

                    class MySQLDatabase(Database):
                        def connect(self):
                            return "Connecting to MySQL"

                    class UserService:
                        def __init__(self, database: Database):
                            self.database = database

                        def save_user(self, user):
                            self.database.connect()
                            # code to save user
                    ```
                - In this example, `UserService` depends on the `Database` abstraction rather than a concrete implementation like `MySQLDatabase`. This allows for easier testing and flexibility in changing the database implementation without affecting the `UserService`.
                
                - To adhere to DIP, we can use dependency injection to pass the database implementation to the `UserService` class, allowing it to work with any database that implements the `Database` interface.



            - Refer [video](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/lecture/Aw6tc/demo-applying-solid-principles) for a demo of applying SOLID principles in Python.

    - Asynchronous vs. synchronous code: A comparative analysis

        - Synchronous code executes sequentially, blocking the execution of subsequent code until the current operation completes.
        - Asynchronous code allows for non-blocking execution, enabling other operations to run while waiting for a task to complete.

        - Example of synchronous code:
            ```python
            import time

            def fetch_data():
                time.sleep(2)  # Simulating a blocking operation
                return "Data fetched"

            print(fetch_data())
            print("This will wait until fetch_data is done")
            ```

        - Example of asynchronous code:
            ```python
            import asyncio

            async def fetch_data():
                await asyncio.sleep(2)  # Simulating a non-blocking operation
                return "Data fetched"

            async def main():
                data = await fetch_data()
                print(data)
                print("This will not wait for fetch_data to complete")

            asyncio.run(main())
            ```
        - In the synchronous example, the program waits for `fetch_data` to complete before moving on to the next line. In the asynchronous example, the program can continue executing other tasks while waiting for `fetch_data` to complete.
        - Asynchronous code is particularly useful in scenarios where tasks can be performed concurrently, such as I/O-bound operations (e.g., network requests, file I/O) or when dealing with multiple tasks that can run independently.
        - Asynchronous code can improve performance and responsiveness, especially in applications that require handling multiple tasks simultaneously, such as web servers or GUI applications.
        - However, asynchronous code can be more complex to write and debug, as it involves managing the flow of execution and handling potential race conditions or deadlocks.

        - [Python's asyncio library](https://docs.python.org/3/library/asyncio.html) for asynchronous programming

        - [Asyncio](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/mir6r/asyncio-the-foundation-of-asynchronous-python)
        
        - Threads and Multiprocessing

            - Threads: Lightweight, share memory space, suitable for I/O-bound tasks.
            - Multiprocessing: Heavyweight, separate memory space, suitable for CPU-bound tasks.

            - [Python's threading module](https://docs.python.org/3/library/threading.html) for multithreading
            - [Python's multiprocessing module](https://docs.python.org/3/library/multiprocessing.html) for parallel processing

        - Comparison of Asynchronous, Multithreading, and Multiprocessing

            - Asynchronous programming is best suited for I/O-bound tasks where waiting for external resources (like network requests) is common.
            - Multithreading is useful for tasks that can run concurrently but share the same memory space, such as handling multiple user requests in a web server.
            - Multiprocessing is ideal for CPU-bound tasks that require heavy computation and can benefit from parallel execution across multiple CPU cores.

- Week 5:

    - [Testing and Debugging](https://www.coursera.org/learn/microsoft-advanced-python-development-techniques/supplement/2b0d1/testing-and-debugging-best-practices-for-python-developers)

        - Unit Testing
            - [unittest](https://docs.python.org/3/library/unittest.html) for unit testing
            - [pytest](https://docs.pytest.org/en/stable/) for advanced testing features

        - Debugging
            - [pdb](https://docs.python.org/3/library/pdb.html) for interactive debugging
            - [logging](https://docs.python.org/3/library/logging.html) for logging messages

        - Test-Driven Development (TDD)
            - Write tests before implementing code to ensure correctness and maintainability.            

        - Unit Testing and Integration Testing

            - Unit testing focuses on testing individual components or functions in isolation.
            - Integration testing verifies the interaction between different components or modules.

            