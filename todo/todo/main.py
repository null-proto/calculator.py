"""FastAPI application for todo management."""

import os
from typing import List
from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import get_db, create_tables, Todo as TodoModel
from .models import TodoCreate, TodoUpdate, TodoResponse

# Create FastAPI app
app = FastAPI(title="Todo App", description="A simple todo application")

# Setup templates and static files
templates_dir = os.path.join(os.path.dirname(__file__), "jinja")
static_dir = os.path.join(os.path.dirname(__file__), "static")

templates = Jinja2Templates(directory=templates_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Create database tables if they don't exist
try:
    create_tables()
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")
    print("Please ensure PostgreSQL is running and database 'todo' exists")


# API Routes
@app.get("/api/todos", response_model=List[TodoResponse])
async def get_todos(db: Session = Depends(get_db)):
    """Get all todos."""
    todos = db.query(TodoModel).all()
    return todos


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo."""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/api/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo."""
    db_todo = TodoModel(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo."""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo."""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}


# Web Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    """Render the todo list page."""
    todos = db.query(TodoModel).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


@app.post("/todos/create")
async def web_create_todo(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    """Create todo via web form."""
    todo = TodoCreate(title=title, description=description)
    db_todo = TodoModel(**todo.dict())
    db.add(db_todo)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/todos/{todo_id}/toggle")
async def web_toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    """Toggle todo completion status."""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.completed = not todo.completed
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/todos/{todo_id}/delete")
async def web_delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete todo via web interface."""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)