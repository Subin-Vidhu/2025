# FastAPI-MCP Sample Todo API

This is a sample implementation of a Todo API using FastAPI with Model Context Protocol (MCP) integration using fastapi-mcp.

## Features

- CRUD operations for Todo items
- Automatic MCP tool generation for all endpoints
- In-memory storage for simplicity
- Well-documented API endpoints

## Setup

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The server will start at `http://localhost:8000` with the following endpoints:
- API Documentation: `http://localhost:8000/docs`
- MCP Server: `http://localhost:8000/mcp`

## Available Endpoints

- `POST /todos/` - Create a new todo
- `GET /todos/` - List all todos
- `GET /todos/{todo_id}` - Get a specific todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

## Connecting to MCP

### Using Cursor

1. Open Cursor
2. Go to Settings -> MCP
3. Add `http://localhost:8000/mcp` as the SSE URL
4. The Todo API tools will be automatically available

### Using Claude Desktop with mcp-proxy

1. Install mcp-proxy: `pip install mcp-proxy`
2. Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "todo-api-mcp": {
      "command": "mcp-proxy",
      "args": ["http://localhost:8000/mcp"]
    }
  }
}
```

## Example Usage

To create a new todo using curl:
```bash
curl -X POST http://localhost:8000/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI-MCP", "completed": false}'
``` 
---
 The settings.json file is a copy of the file from `C:\Users\Subin-PC\AppData\Roaming\Code\User` and there was one `mcp.json` file inside the .vscode folder in the working dir[as this mcp server was configured for workspace settings instead of user settings]:

```
{
    "servers": {
        "test_fast_api": {
            "type": "sse",
            "url": "http://localhost:8000/mcp"
        }
    }
}
```

- Had to start the mcp server on settings.json file of vscode inorder for this to work.

```
"todo-api": {
                "command": "D:/2025/Cursor/VSCode_Agent/venv/Scripts/python.exe",
                "args": [
                    "D:/2025/Cursor/VSCode_Agent/main.py"
                ]
            },
```

- either start the above or the run app as normal `python main.py`