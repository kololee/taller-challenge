from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy import ForeignKey
from datetime import datetime
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
    description: str | None = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=datetime.now,
            nullable=False
        )
    )
    project_id: uuid.UUID | None = Field(
        sa_column=Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    )
    due_date: datetime | None = Field(
        sa_column=Column(TIMESTAMP(timezone=True))
    )
    
    # Relationship to project
    project: Optional["Project"] = Relationship(back_populates="tasks")