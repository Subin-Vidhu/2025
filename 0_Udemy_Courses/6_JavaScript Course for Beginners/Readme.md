### Course -  [JavaScript for Beginners: Learn JavaScript from Scratch & Build Interactive Websites](udemy.com/course/javascript-course-beginners)

Notes taken from the Course
---

- Section 1: Javascript

    - JavaScript is a programming language that is used to make web pages interactive.
    - JavaScript is a client-side scripting language, which means that it runs in the user's web browser rather than on the server.
    - JavaScript is an interpreted language, which means that it is executed line by line rather than being compiled into machine code.
    - JavaScript is a high-level language, which means that it is easy to read and write.
    - JavaScript is a dynamic language, which means that it can change at runtime.


    - Key Features

        - Client Side Scripting Language: JavaScript is a client-side scripting language, which means that it runs in the user's web browser rather than on the server. This allows for faster and more responsive web applications.

        - Light weight and Versatile: JavaScript is a lightweight and versatile language that can be used for a wide range of applications, from simple web pages to complex web applications.

        - Event Driven: JavaScript is an event-driven language, which means that it can respond to user actions such as clicks, mouse movements, and keyboard input. This allows for interactive and dynamic web pages.

        - Asynchronous: JavaScript is an asynchronous language, which means that it can perform multiple tasks at the same time without blocking the main thread. This allows for faster and more responsive web applications.

        - Cross Platform: JavaScript is a cross-platform language, which means that it can run on any operating system and web browser. This allows for greater compatibility and accessibility for users.

        - Extended by Libraries and Frameworks: JavaScript can be extended by libraries and frameworks such as jQuery, React, and Angular. These libraries and frameworks provide additional functionality and make it easier to develop complex web applications.

        - Object Oriented: JavaScript is an object-oriented language, which means that it can create and manipulate objects. This allows for greater flexibility and reusability of code.

    - Common Uses

        - DOM Manipulation: JavaScript can be used to manipulate the Document Object Model (DOM) of a web page, allowing for dynamic changes to the content and structure of the page.
        - Form Validation: JavaScript can be used to validate user input in forms, ensuring that the data entered is correct and complete before it is submitted to the server.
        - Animation: JavaScript can be used to create animations and transitions on web pages, making them more visually appealing and engaging for users.
        - AJAX: JavaScript can be used to make asynchronous requests to the server, allowing for dynamic updates to the page without requiring a full page reload.
        - Fetch Data from API: JavaScript can be used to fetch data from APIs, allowing for the integration of external data sources into web applications.
        - Create Web Applications: JavaScript can be used to create complex web applications, such as single-page applications (SPAs) and progressive web applications (PWAs).

- Section 2: 

    - Javascript Syntax

        - JavaScript is a case-sensitive language, which means that it treats uppercase and lowercase letters as different characters.
        - JavaScript statements are executed line by line, from top to bottom.
        - JavaScript statements can be separated by semicolons (;), but this is not required if each statement is on a separate line.
        - JavaScript comments can be added using // for single-line comments and /* */ for multi-line comments.

        - JavaScript variables can be declared using var, let, or const. The var keyword is used to declare a variable that can be reassigned, while the let and const keywords are used to declare block-scoped variables. The const keyword is used to declare a variable that cannot be reassigned.
        - JavaScript variables can be assigned values using the = operator. The value can be a number, string, boolean, array, or object.
        - JavaScript variables can be reassigned using the = operator. The new value can be of the same type or a different type.
        - JavaScript variables can be declared without an initial value, in which case they will be assigned the value undefined.
        - example:
            ```javascript
            var x; // variable declaration without initial value
            console.log(x); // undefined
            ```
        - JavaScript variables can be declared with an initial value, in which case they will be assigned the value of the initial value.
        - example:
            ```javascript
            var x = 5; // variable declaration with initial value
            console.log(x); // 5
            ```
        - JavaScript variables can be declared with a value of null, which means that the variable has no value.
        - example:
            ```javascript
            var x = null; // variable declaration with null value
            console.log(x); // null
            ```

    - Adding Javascript to HTML

        - JavaScript can be added to HTML using the `<script>` tag. The `<script>` tag can be placed in the head or body of the HTML document.
        - The `<script>` tag can be used to include an external JavaScript file using the src attribute. The src attribute specifies the URL of the external JavaScript file.
        - The `<script>` tag can also be used to include inline JavaScript code. Inline JavaScript code is placed between the opening and closing `<script>` tags.

        - examples for inline, internal and external JS - refer javascript.html in Resources folder

- Section 3 : Console | Comments

    - JS Console

        - The console is a built-in JavaScript object that provides access to the browser's debugging console.
        - The console can be used to log messages, errors, and warnings to the console.
        - The console can be used to execute JavaScript code in the browser's console.
        - The console can be used to inspect and manipulate the DOM.
        - example:
            ```javascript
            console.log("Hello, World!"); // logs "Hello, World!" to the console
            console.error("This is an error message"); // logs an error message to the console
            console.warn("This is a warning message"); // logs a warning message to the console
            console.info("This is an info message"); // logs an info message to the console
            ```

    - JS Comments

        - JavaScript comments are used to add notes and explanations to the code.
        - JavaScript comments can be single-line or multi-line.
        - Single-line comments are created using //, while multi-line comments are created using /* */.
        - example:
            ```javascript
            // This is a single-line comment
            console.log("Hello, World!"); // This is a single-line comment
            /* This is a multi-line comment
            console.log("Hello, World!"); */
            ```
        - JavaScript comments are ignored by the browser and do not affect the execution of the code.

- Section 4 : Variables and Dataypes

    - Variables

        - Variables are used to store data in JavaScript.
        - Variables can be declared using the var, let, or const keywords.
            - var declares a variable that can be reassigned, with function-scoped scope and hoisting.
            - let declares a variable that can be reassigned, with block-scoped scope and no hoisting.
            - const declares a constant variable that cannot be reassigned, with block-scoped scope and no hoisting.

        - examples for var, let and const:
            ```javascript
            var x = 5; // variable declaration with initial value
            console.log(x); // 5
            ```
            ```javascript
            let y = 10; // variable declaration with initial value
            console.log(y); // 10
            ```
            ```javascript
            const z = 15; // variable declaration with initial value
            console.log(z); // 15
            ```

    - Data Types

        - JavaScript has several built-in data types, including:
            - Number: Represents numeric values, both integers and floating-point numbers.
            - String: Represents a sequence of characters enclosed in single or double quotes.
            - Boolean: Represents a logical value, either true or false.
            - Object: Represents a collection of key-value pairs.
            - Array: Represents an ordered list of values.
            - Null: Represents the absence of a value.
            - Undefined: Represents a variable that has been declared but has not been assigned a value.

        - example:
            ```javascript
            var x = 5; // number
            var y = "Hello"; // string
            var z = true; // boolean
            var obj = { name: "John", age: 30 }; // object        
            var arr = [1, 2, 3]; // array
            var n = null; // null
            var u; // undefined
            ```
        - JavaScript is a dynamically typed language, which means that variables can change types at runtime.
        - example:
            ```javascript
            var x = 5; // number
            console.log(typeof x); // number
            x = "Hello"; // string
            console.log(typeof x); // string
            ```

        - JavaScript provides several built-in functions for converting between data types, including:
            - Number(): Converts a value to a number.
            - String(): Converts a value to a string.
            - Boolean(): Converts a value to a boolean.
            - parseInt(): Converts a string to an integer.
            - parseFloat(): Converts a string to a floating-point number.
            - isNaN(): Checks if a value is NaN (Not a Number).
            - isFinite(): Checks if a value is finite (not Infinity or NaN).
            - example:
                ```javascript
                var x = "5"; // string
                console.log(typeof x); // string
                x = Number(x); // converts to number
                console.log(typeof x); // number
                ```
                ```javascript
                var x = "5.5"; // string
                console.log(typeof x); // string
                x = parseFloat(x); // converts to floating-point number
                console.log(typeof x); // number
                ```
                ```javascript
                var x = "Hello"; // string
                console.log(typeof x); // string
                x = Number(x); // converts to NaN, not a number, because "Hello" cannot be converted to a number
                console.log(typeof x); // number, but value is NaN
                console.log(x); // NaN
                console.log(isNaN(x)); // true
                ```
                
- Section 5: Operators and Functions

    - Operators

        - Operators are used to perform operations on variables and values.
        - JavaScript has several built-in operators, including:
            - Arithmetic Operators: +, -, *, /, %, ++, --
            - Assignment Operators: =, +=, -=, *=, /=, %=
            - Comparison Operators: ==, ===, !=, !==, >, <, >=, <=
            - Logical Operators: &&, ||, !
            - Bitwise Operators: &, |, ^, ~, <<, >>
            - Ternary Operator: ? :

        - example:
            ```javascript
            var x = 5; // number
            var y = 10; // number
            var z = x + y; // addition
            console.log(z); // 15
            ```

    - Functions

        - Functions are used to group code into reusable blocks.
        - Functions can take parameters and return values.
        - Functions can be declared using the function keyword or as arrow functions.
        - example for function declaration, function expression and arrow functions:
            ```javascript
            function add(x, y) { // function declaration
                return x + y; // return statement
            }
            console.log(add(5, 10)); // 15
            ```
            ```javascript
            const add = (x, y) => { // arrow function
                return x + y; // return statement
            }
            console.log(add(5, 10)); // 15
            ```

            ```javascript
            // function expression
            const add = function(x, y) { // function expression
                return x + y; // return statement
            }
            console.log(add(5, 10)); // 15
            ```

            