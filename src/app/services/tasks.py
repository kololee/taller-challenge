from typing import List, Optional
import uuid
from datetime import datetime
from sqlmodel import Session
from fastapi import HTTPException

from app.models.tasks import Task
from app.schemas.tasks import TaskCreateModel, TaskUpdateModel
from app.test.mock_tasks import tasks
from app.test.mock_projects import projects


class TaskService:
    """Service layer for task operations."""
    
    def __init__(self, db: Session):
        self.db = db
    

    async def update_task(self, task_id: int, task_data: TaskUpdateModel) -> Optional[dict]:
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
        # Find the task
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                # Validate project exists if project_id is being updated
                if task_data.project_id is not None:
                    project = next((proj for proj in projects if proj["id"] == task_data.project_id), None)
                    if not project:
                        raise HTTPException(status_code=404, detail="Project not found")
                    tasks[index]["project_id"] = task_data.project_id
                
                # Update other fields that were provided
                if task_data.title is not None:
                    tasks[index]["title"] = task_data.title
                if task_data.priority is not None:
                    tasks[index]["priority"] = task_data.priority
                if task_data.completed is not None:
                    tasks[index]["completed"] = task_data.completed
                if task_data.due_date is not None:
                    tasks[index]["due_date"] = task_data.due_date
                
                return tasks[index]
        
        return None
    
    async def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The unique identifier of the task
            
        Returns:
            True if task was deleted successfully, False if not found
            
        Raises:
            Exception: If task deletion fails
        """
        global tasks
        original_length = len(tasks)
        tasks[:] = [task for task in tasks if task["id"] != task_id]
        
        return len(tasks) < original_length
