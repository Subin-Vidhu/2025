#!/bin/bash

function hello {
    echo "Hello World"
}
hello

function hello {
    echo "Hello $1, $2"
}
hello "alice" "message"
hello "bob" "something"
hello "charles" "great"[]


function hello { 
    echo "Hello World" 
    local VAR="Hello" 
    echo $VAR 
} 
hello 
echo $VAR # returns nothing, because VAR is local to the function

X="Hello"
# This is a global variable
function hello {
    echo "Hello World"
    local VAR="Hello"
    echo $VAR  # returns nothing, because VAR is local to the function
    echo $X # returns Hello, because X is global
}

hello
echo $VAR # returns nothing, because VAR is local to the function
echo $X # returns Hello, because X is global