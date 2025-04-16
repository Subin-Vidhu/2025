from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(title="Sample Todo API")

# Sample in-memory database
todos = []

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

# Create endpoints with explicit operation_ids for better MCP tool names
@app.post("/todos/", operation_id="create_todo", response_model=Todo)
async def create_todo(todo: Todo):
    """
    Create a new todo item.
    """
    todo.id = len(todos) + 1
    todos.append(todo)
    return todo

@app.get("/todos/", operation_id="list_todos", response_model=List[Todo])
async def list_todos():
    """
    Get all todo items.
    """
    return todos

@app.get("/todos/{todo_id}", operation_id="get_todo", response_model=Todo)
async def get_todo(todo_id: int):
    """
    Get a specific todo item by ID.
    """
    if todo_id < 1 or todo_id > len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id - 1]

@app.put("/todos/{todo_id}", operation_id="update_todo", response_model=Todo)
async def update_todo(todo_id: int, todo: Todo):
    """
    Update a todo item by ID.
    """
    if todo_id < 1 or todo_id > len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.id = todo_id
    todos[todo_id - 1] = todo
    return todo

@app.delete("/todos/{todo_id}", operation_id="delete_todo")
async def delete_todo(todo_id: int):
    """
    Delete a todo item by ID.
    """
    if todo_id < 1 or todo_id > len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(todo_id - 1)
    return {"message": "Todo deleted successfully"}

# Initialize and mount the MCP server
mcp = FastApiMCP(
    app,
    name="Todo API MCP",
    description="A simple Todo API with MCP integration",
    base_url="http://localhost:8000",
)

# Mount the MCP server to the FastAPI app
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 