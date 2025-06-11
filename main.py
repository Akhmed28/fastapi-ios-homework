# main.py

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    description: str

class TaskCreate(BaseModel):
    
    title: str
    description: str

fake_db = [
    Task(id=1, title="Learn FastAPI", description="Study the official documentation."),
    Task(id=2, title="Build a CRUD API", description="Complete the basic level of the homework.")
]

app = FastAPI()



@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_to_create: TaskCreate):
    new_id = max(t.id for t in fake_db) + 1 if fake_db else 1
    new_task = Task(id=new_id, title=task_to_create.title, description=task_to_create.description)
    fake_db.append(new_task)
    return new_task

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    return fake_db

@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: int):
    for task in fake_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_updates: TaskCreate):
    for index, task in enumerate(fake_db):
        if task.id == task_id:
            updated_task = task.copy(update=task_updates.dict())
            fake_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task_to_delete = None
    for task in fake_db:
        if task.id == task_id:
            task_to_delete = task
            break
            
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
        
    fake_db.remove(task_to_delete)
    return None