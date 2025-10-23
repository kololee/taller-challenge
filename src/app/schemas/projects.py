from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import uuid


class ProjectModel(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

class ProjectCreateModel(BaseModel):
    name: str
    description: str

class ProjectUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
