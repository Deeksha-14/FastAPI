from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# 1. The Model: It Defines what a Todo looks like
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# 2. In-memory Database
todo_db = []

# --- ROUTES ---

# GET: Fetch all todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todo_db

# POST: Create a new todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    # Check if ID already exists
    if any(t.id == todo.id for t in todo_db):
        raise HTTPException(status_code=400, detail="ID already exists")
    todo_db.append(todo)
    return todo

# GET: Fetch a single todo by ID
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todo_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# PUT: Update a todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            todo_db[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

# DELETE: Remove a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todo_db):
        if todo.id == todo_id:
            todo_db.pop(index)
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")