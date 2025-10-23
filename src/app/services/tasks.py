from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.tasks import Task
from app.models.projects import Project
from app.schemas.tasks import TaskCreateModel, TaskUpdateModel


class TaskService:
    """Service layer for task operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_task(self, task_id: uuid.UUID, task_data: TaskUpdateModel) -> Optional[Task]:
        """
        Update an existing task.
        
        Args:
            task_id: The unique identifier of the task
            task_data: The updated task data
            
        Returns:
            The updated task if found and updated successfully, None otherwise
            
        Raises:
            Exception: If task update fails
            ValueError: If project_id is provided but project doesn't exist
        """
        statement = select(Task).where(Task.id == task_id)
        result = await self.db.execute(statement)
        task = result.scalar_one_or_none()
        
        if not task:
            return None

        if task_data.project_id is not None:
            project_statement = select(Project).where(Project.id == task_data.project_id)
            project_result = await self.db.execute(project_statement)
            project = project_result.scalar_one_or_none()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            task.project_id = task_data.project_id

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.completed is not None:
            task.completed = task_data.completed
        if task_data.due_date is not None:
            task.due_date = task_data.due_date

        await self.db.commit()
        await self.db.refresh(task)
        
        return task
    
    async def delete_task(self, task_id: uuid.UUID) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The unique identifier of the task
            
        Returns:
            True if task was deleted successfully, False if not found
            
        Raises:
            Exception: If task deletion fails
        """
        statement = select(Task).where(Task.id == task_id)
        result = await self.db.execute(statement)
        task = result.scalar_one_or_none()
        
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        
        return True
