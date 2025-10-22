from typing import Optional, List
from pydantic import BaseModel


class ProjectModel(BaseModel):
    id: int
    name: str
    description: str
    created_at: str

class ProjectCreateModel(BaseModel):
    name: str
    description: str

class ProjectUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
