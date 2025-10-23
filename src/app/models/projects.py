from sqlmodel import Column, Field, SQLModel, Relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from datetime import datetime
import uuid
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .tasks import Task

class Project(SQLModel, table=True):
    """Database model for a project."""
    __tablename__ = "projects"

    id: uuid.UUID = Field(
        sa_column=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    )
    name: str
    description: str | None = None
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=datetime.now,
            nullable=False
        )
    )
    
    # Relationship to tasks
    tasks: List["Task"] = Relationship(
        back_populates="project",
        cascade_delete=True
    )