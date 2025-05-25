# Step 1: Use with open() in write mode and file.write() to add the initial to-do items to a file named todo.txt

with open("todo.txt", "w") as file:
    file.write("Finish project report\n")
    file.write("Schedule dentist appointment\n")

# Step 3: Use with open() in append mode and file.write() to append two additional items to the todo.txt file

with open("todo.txt", "a") as file:
    file.write("Buy groceries\n")
    file.write("Call mom\n")