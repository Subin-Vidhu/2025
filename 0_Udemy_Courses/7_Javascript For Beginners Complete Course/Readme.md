####  Course link : [here](https://www.udemy.com/course/javascript-for-beginners-complete-course/)

---

Learn Javascript Programming Language With Practical Interaction

---

1. Javascript Introduction

    - Client Side Scripting Language
    - It is untyed, multi-paradigm, functional and event-driven language. Untyped means you don't have to define the type of variable. Multi-paradigm means you can use different programming paradigms like functional, object-oriented, and imperative. Event-driven means it is based on events like mouse click, key press, etc.
    - Interpreted by browsers js engine, ie. Chrome uses V8 engine, Firefox uses SpiderMonkey, and Safari uses JavaScriptCore.
    - It is a high-level language, which means it is easy to read and write. It is also a dynamic language, which means you can change the type of variable at runtime.

    - Advantages:

        - Less Server Interactions
        - Immediate Feedback to the User
        - Rich User Interface
        - Increased Interactivity
        - Reduced Server Load
        - Increased Performance

2. Javascript Arrays

    
    - Arrays are used to store multiple values in a single variable.
    - It is a special type of object that has a length property and numeric keys.
    - You can create an array using the Array constructor or the array literal syntax.
    - You can access the elements of an array using the index. The index starts from 0.
    - You can also use the forEach() method to iterate over the elements of an array.

    - Array Methods:

        - push() : Adds one or more elements to the end of an array and returns the new length of the array.
        - pop() : Removes the last element from an array and returns that element.
        - shift() : Removes the first element from an array and returns that element.
        - unshift() : Adds one or more elements to the beginning of an array and returns the new length of the array.
        - splice() : Changes the contents of an array by removing or replacing existing elements and/or adding new elements in place.
        - slice() : Returns a shallow copy of a portion of an array into a new array object selected from start to end (end not included) where start and end represent the index of items in that array. The original array will not be modified.

        - code example for array methods:

            ```javascript
            let fruits = ["Banana", "Orange", "Apple", "Mango"];
            let numbers = [1, 2, 3, 4, 5];
            let mixed = ["Banana", 1, true, null, undefined, {name: "John"}, [1, 2, 3]];
            let empty = [];
            let array = new Array(1, 2, 3, 4, 5);
            let array2 = new Array(5); // creates an array with 5 empty slots

            // Array Methods
            fruits.push("Pineapple"); // adds "Pineapple" to the end of the array
            console.log(fruits); // ["Banana", "Orange", "Apple", "Mango", "Pineapple"]
            fruits.pop(); // removes the last element from the array
            console.log(fruits); // ["Banana", "Orange", "Apple", "Mango"]
            fruits.shift(); // removes the first element from the array
            console.log(fruits); // ["Orange", "Apple", "Mango"]
            fruits.unshift("Banana"); // adds "Banana" to the beginning of the array
            console.log(fruits); // ["Banana", "Orange", "Apple", "Mango"]
            fruits.splice(1, 2); // removes 2 elements from index 1

            console.log(fruits); // ["Banana", "Mango"]
            fruits.splice(1, 0, "Orange", "Apple"); // adds "Orange" and "Apple" at index 1
            console.log(fruits); // ["Banana", "Orange", "Apple", "Mango"]

            let sliced = fruits.slice(1, 3); // returns a shallow copy of the array from index 1 to index 3 (not included)
            console.log(sliced); // ["Orange", "Apple"]
            console.log(fruits); // ["Banana", "Orange", "Apple", "Mango"]
            ```
    - Array Iteration Methods:

        - forEach() : Executes a provided function once for each array element.
        - map() : Creates a new array populated with the results of calling a provided function on every element in the calling array.
        - filter() : Creates a new array with all elements that pass the test implemented by the provided function.
        - reduce() : Executes a reducer function (that you provide) on each element of the array, resulting in a single output value.
        - find() : Returns the value of the first element in the provided array that satisfies the provided testing function. If no values satisfy the testing function, undefined is returned.

        - code example for array iteration methods:

            ```javascript
            let numbers = [1, 2, 3, 4, 5];
            let fruits = ["Banana", "Orange", "Apple", "Mango"];

            // Array Iteration Methods
            numbers.forEach(function(number) {
                console.log(number); // prints each number in the array
            });

            let doubled = numbers.map(function(number) {
                return number * 2; // returns a new array with each number multiplied by 2
            });
            console.log(doubled); // [2, 4, 6, 8, 10]

            let filtered = numbers.filter(function(number) {
                return number > 2; // returns a new array with numbers greater than 2
            });
            console.log(filtered); // [3, 4, 5]

            let sum = numbers.reduce(function(total, number) {
                return total + number; // returns the sum of all numbers in the array
            }, 0);
            console.log(sum); // 15

            let found = fruits.find(function(fruit) {
                return fruit === "Apple"; // returns the first fruit that is "Apple"
            });
            console.log(found); // "Apple"
            ```