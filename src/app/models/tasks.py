
from typing import Optional
from pydantic import BaseModel


class TaskModel(BaseModel):
    id: int
    project_id: int
    title: str
    priority: int
    completed: bool
    due_date: Optional[str] = None

class TaskCreateModel(BaseModel):
    title: str
    priority: int = 1
    completed: bool = False
    due_date: Optional[str] = None

class TaskUpdateModel(BaseModel):
    project_id: Optional[int] = None
    title: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None
