# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import all the components we just created in the other files
import models
import schemas
from database import SessionLocal, engine

# This line creates the "tasks" table in the database based on our models.py definition
# It will only do this if the table doesn't already exist.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Dependency ---
# This function gets a database session for each request and closes it afterwards.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD Endpoints ---

# CREATE a task
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Convert Pydantic schema to a SQLAlchemy model instance
    db_task = models.TaskItem(title=task.title, description=task.description)
    db.add(db_task)  # Add the new task to the database session
    db.commit()     # Commit the transaction to save it to the database
    db.refresh(db_task) # Refresh the instance to get the new ID from the DB
    return db_task

# READ all tasks
@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(models.TaskItem).offset(skip).limit(limit).all()
    return tasks

# READ a single task
@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskItem).filter(models.TaskItem.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task