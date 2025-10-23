from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
import uuid
from app.schemas.projects import ProjectModel, ProjectCreateModel, ProjectUpdateModel
from app.schemas.tasks import TaskModel, TaskCreateModel
from app.services.projects import ProjectService
from app.core.db.database import get_db
from app.models.auth import User
from app.services.auth import get_current_user_dependency


router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service(db: AsyncSession = Depends(get_db)) -> ProjectService:
    """Dependency to get ProjectService instance."""
    return ProjectService(db)


@router.post(
        "/",
        summary="Create a new project",
        status_code=201,
        response_model=ProjectModel)
async def create_project(
    project: ProjectCreateModel,
    _current_user: User = Depends(get_current_user_dependency),
    project_service: ProjectService = Depends(get_project_service)
):
    return await project_service.create_project(project)


@router.get(
        "/{project_id}",
        summary="Get project details by ID",
        status_code=200,
        response_model=ProjectModel)
async def get_project_details(
    project_id: uuid.UUID,
    _current_user: User = Depends(get_current_user_dependency),
    project_service: ProjectService = Depends(get_project_service)
):
    project = await project_service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put(
        "/{project_id}",
        summary="Update project information by ID",
        status_code=200,
        response_model=ProjectModel)
async def update_project_info(
    project_id: uuid.UUID,
    updated_project: ProjectUpdateModel,
    _current_user: User = Depends(get_current_user_dependency),
    project_service: ProjectService = Depends(get_project_service)
):
    project = await project_service.update_project(project_id, updated_project)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete(
        "/{project_id}",
        summary="Delete a project by ID",
        status_code=204)
async def delete_project(
    project_id: uuid.UUID,
    _current_user: User = Depends(get_current_user_dependency),
    project_service: ProjectService = Depends(get_project_service)
):
    success = await project_service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None


@router.post(
        "/{project_id}/tasks/",
        summary="Create a new task under a specific project",
        status_code=201,
        response_model=TaskModel)
async def create_task_for_project(
    project_id: uuid.UUID, 
    task: TaskCreateModel,
    _current_user: User = Depends(get_current_user_dependency),
    project_service: ProjectService = Depends(get_project_service)
):
    return await project_service.create_task_for_project(project_id, task)


@router.get(
        "/{project_id}/tasks/",
        summary="Get all tasks under a specific project",
        status_code=200,
        response_model=List[TaskModel])
async def get_tasks_for_project(
    project_id: uuid.UUID,
    _current_user: User = Depends(get_current_user_dependency),
    project_service: ProjectService = Depends(get_project_service)
):
    return await project_service.get_tasks_for_project(project_id)
