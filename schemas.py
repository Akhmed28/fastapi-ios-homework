# schemas.py
from pydantic import BaseModel

# This is our Pydantic model for creating a task
class TaskCreate(BaseModel):
    title: str
    description: str

# This is our main Pydantic model for reading a task
class Task(TaskCreate):
    id: int

    class Config:
        from_attributes = True