from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import uuid
from app.schemas.tasks import TaskModel, TaskCreateModel, TaskUpdateModel
from app.services.tasks import TaskService
from app.core.db.database import get_db


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    """Dependency to get TaskService instance."""
    return TaskService(db)


@router.put(
        "/{task_id}",
        summary="Update a task by ID",
        status_code=200,
        response_model=TaskModel)
async def update_task(
    task_id: uuid.UUID,
    updated_task: TaskUpdateModel,
    task_service: TaskService = Depends(get_task_service)
):
    task = await task_service.update_task(task_id, updated_task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete(
        "/{task_id}",
        summary="Delete a task by ID",
        status_code=204)
async def delete_task(
    task_id: uuid.UUID,
    task_service: TaskService = Depends(get_task_service)
):
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
