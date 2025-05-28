def multiply(*args):
    """
    Multiplies all the arguments together.
    """
    result = 1
    for arg in args:
        result *= arg
    return result

print("Starting multiplication...")
result = multiply(1, 2, 3)
print(f"Multiplication result: {result}")
# This code snippet demonstrates a simple multiplication function.