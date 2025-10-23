from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy import ForeignKey, Date
from datetime import datetime, date
import uuid
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .projects import Project

class Task(SQLModel, table=True):
    """Database model for a task."""
    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    title: str
    priority: int = Field(default=1, description="Task priority (higher number = higher priority)")
    completed: bool = Field(default=False)
    project_id: uuid.UUID | None = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    )
    due_date: date | None = Field(
        sa_column=Column(Date)
    )
    
    # Relationship to project
    project: Optional["Project"] = Relationship(back_populates="tasks")