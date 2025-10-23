
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
import uuid


class TaskModel(BaseModel):
    id: uuid.UUID
    title: str
    priority: int
    completed: bool
    project_id: Optional[uuid.UUID] = None
    due_date: Optional[date] = None

class TaskCreateModel(BaseModel):
    title: str
    priority: int = 1
    completed: bool = False
    project_id: Optional[uuid.UUID] = None
    due_date: Optional[date] = None

class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
    project_id: Optional[uuid.UUID] = None
    due_date: Optional[date] = None
