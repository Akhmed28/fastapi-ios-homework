# schemas.py (Full Version)
from pydantic import BaseModel
from typing import List

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    tasks: List[Task] = []

    class Config:
        from_attributes = True