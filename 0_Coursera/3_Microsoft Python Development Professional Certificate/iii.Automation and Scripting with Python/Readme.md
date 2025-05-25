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