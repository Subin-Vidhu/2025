- Week 1

     - How to set up code snippets in vs code

        1. To start, you will create the "calculate area" code snippet in this IDE with the following steps so that you can utilize it in your Python scripts.

        2. Navigate to File -> Preferences -> Configure User Snippets. Then search or scroll down in the resulting dropdown to select 'Python' from the list of options. This will open the python.json file where you will add your code snippet.

        3. Replace everything in python.json (including the placeholder snippet comments and curly braces) with the following code:  
            ```json
            {
            "calculate_area": {
                "prefix": "calc_area",
                "body": [
                    "def calculate_area(length, width):",
                    "  \"\"\"Calculates the area of a rectangle.\"\"\"",
                    "  # Calculate the area",
                    "  area = length * width",
                    "  ",
                    "  # Output the area",
                    "  return area",
                    "",
                    "# Example usage",
                    "length = $1",
                    "width = $2",
                    "print(calculate_area(length, width))"
                ],
                "description": "Calculate the area of a rectangle"
            }
            }
            ```

        4. Save the python.json file after adding the code snippet, and then open main.py from the file explorer on the left.

        5. Now try inserting your code snippet by typing calc_area into main.py and pressing tab when you see the IntelliSense suggestion for calc_area pop up.

        6. Your cursor should be automatically set to the first placeholder, length. Set length to 5 and width to 3 in your newly created snippet code. You can use tab to jump to the next placeholder after adding each value.

        7. Now test the snippet code by running the main.py script and see if you get the correct output in the terminal. To do this, open the terminal using the keyboard shortcut Ctrl+` or through the menu (View -> Terminal) and then enter python3 main.py in the terminal.

        8. After running the main.py script, you should see the following output: 15


- Week 2

    - Regex Reference [link](https://www.coursera.org/learn/microsoft-automation-scripting-with-python/supplement/DG8QY/reference-guide-to-regex)

- Week 3

    - APIs

- Week 4

    - Python Profiling tools

        - cProfile :
            - A built-in Python module for profiling code performance.
            - Use `cProfile.run('your_function()')` to profile a specific function.
            - Generate a report using `pstats` module to analyze the profiling results.
            - eg:
                ```python
                import cProfile
                import pstats

                def your_function():
                    # Your code here
                    pass

                cProfile.run('your_function()', 'output.prof')
                p = pstats.Stats('output.prof')
                p.sort_stats('cumulative').print_stats()
                ```
        - line_profiler
            - A third-party library for line-by-line profiling of Python code.
            - Use `@profile` decorator to mark functions for profiling.
            - Install with `pip install line_profiler`.
            - Run with `kernprof -l -v your_script.py` to see line-by-line profiling results.
            - eg:
                ```python
                @profile
                def your_function():
                    # Your code here
                    pass

                if __name__ == '__main__':
                    your_function()
                ```
        - memory_profiler
            - A third-party library for memory profiling of Python code.
            - Use `@profile` decorator to mark functions for memory profiling.
            - Install with `pip install memory_profiler`.
            - Run with `python -m memory_profiler your_script.py` to see memory usage line-by-line.
            - eg:
                ```python
                from memory_profiler import profile

                @profile
                def your_function():
                    # Your code here
                    pass

                if __name__ == '__main__':
                    your_function()
                ```
        - py-spy
            - A sampling profiler for Python applications.
            - Install with `pip install py-spy`.
            - Run with `py-spy top --pid <PID>` to see real-time profiling of a running Python process.
            - Can also generate flame graphs using `py-spy record -o output.svg --pid <PID>`.
            - eg:
                ```bash
                py-spy top --pid 12345
                py-spy record -o output.svg --pid 12345
                ```

    - Parallel Processing - Refer [here](https://www.coursera.org/learn/microsoft-automation-scripting-with-python/supplement/MXKIE/parallel-processing-with-python-concurrency-and-multiprocessing)

        - multiprocessing
            - A built-in Python module for parallel processing.
            - Use `multiprocessing.Pool` to create a pool of worker processes.
            - Use `map`, `apply`, or `apply_async` to distribute tasks across the worker processes.
            - eg:
                ```python
                from multiprocessing import Pool

                def square(x):
                    return x * x

                if __name__ == '__main__':
                    with Pool(4) as p:
                        results = p.map(square, range(10))
                    print(results)
                ```

        - concurrent.futures
            - A built-in Python module for high-level parallelism.
            - Use `ThreadPoolExecutor` or `ProcessPoolExecutor` to manage threads or processes.
            - Use `submit` or `map` to schedule tasks for execution.
            - eg:
                ```python
                from concurrent.futures import ProcessPoolExecutor

                def square(x):
                    return x * x

                if __name__ == '__main__':
                    with ProcessPoolExecutor(max_workers=4) as executor:
                        results = list(executor.map(square, range(10)))
                    print(results)
                ```

        - Asynchronous Programming
            - asyncio
                - A built-in Python module for writing asynchronous code using coroutines.
                - Use `async def` to define a coroutine and `await` to call other coroutines.
                - Use `asyncio.run()` to run the main coroutine.
                - eg:
                    ```python
                    import asyncio

                    async def fetch_data():
                        await asyncio.sleep(1)
                        return "Data fetched"

                    async def main():
                        data = await fetch_data()
                        print(data)

                    if __name__ == '__main__':
                        asyncio.run(main())
                    ```

        - aiohttp
            - A third-party library for making asynchronous HTTP requests.
            - Install with `pip install aiohttp`.
            - Use `aiohttp.ClientSession` to create a session and make requests asynchronously.
            - eg:
                ```python
                import aiohttp
                import asyncio

                async def fetch(url):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            return await response.text()

                async def main():
                    html = await fetch('https://example.com')
                    print(html)

                if __name__ == '__main__':
                    asyncio.run(main())
                ```

    - Logging

        - Python's built-in logging module provides a flexible framework for emitting log messages from Python programs.
        - Use `logging.basicConfig()` to configure the logging system.
        - Use different log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.
        - Example:
            ```python
            import logging

            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

            logging.debug('This is a debug message')
            logging.info('This is an info message')
            logging.warning('This is a warning message')
            logging.error('This is an error message')
            logging.critical('This is a critical message')
            ```

    - Unit Testing

        - Python's built-in unittest module provides a framework for writing and running tests.
        - Use `unittest.TestCase` to create test cases.
        - Use `assertEqual`, `assertTrue`, `assertFalse`, etc. to check conditions in tests.
        - Example:
            ```python
            import unittest

            def add(a, b):
                return a + b

            class TestMathOperations(unittest.TestCase):
                def test_add(self):
                    self.assertEqual(add(2, 3), 5)
                    self.assertEqual(add(-1, 1), 0)

            if __name__ == '__main__':
                unittest.main()
            ```

    - Pytest

        - A third-party testing framework that makes it easy to write simple and scalable test cases.
        - Install with `pip install pytest`.
        - Use `assert` statements to check conditions in tests.
        - Example:
            ```python
            def add(a, b):
                return a + b

            def test_add():
                assert add(2, 3) == 5
                assert add(-1, 1) == 0
            
            if __name__ == '__main__':
                import pytest
                pytest.main()
            ```

    - For more, refer to the [documentation](https://www.coursera.org/learn/microsoft-automation-scripting-with-python/supplement/ixqmG/types-of-testing-for-automation-scripts-unit-integration-and-end-to-end)

- Week 5

    - Git and Github

        - Git is a version control system that allows you to track changes in your code and collaborate with others.
        - GitHub is a platform for hosting Git repositories and collaborating on projects.
        - Basic Git commands:
            - `git init`: Initialize a new Git repository.
            - `git clone <repository_url>`: Clone a remote repository to your local machine.
            - `git add <file>`: Stage changes for commit.
            - `git commit -m "message"`: Commit staged changes with a message.
            - `git push`: Push local commits to the remote repository.
            - `git pull`: Fetch and merge changes from the remote repository.
            - `git branch`: List branches in the repository.
            - `git checkout <branch>`: Switch to a different branch.
            - `git merge <branch>`: Merge changes from another branch into the current branch.

        - For more, refer to the [documentation](https://www.coursera.org/learn/microsoft-automation-scripting-with-python/supplement/RabJi/cheat-sheet-for-streamlining-collaboration-with-git)