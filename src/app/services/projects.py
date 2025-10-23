from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.projects import Project
from app.models.tasks import Task
from app.schemas.projects import ProjectCreateModel, ProjectUpdateModel
from app.schemas.tasks import TaskCreateModel


class ProjectService:
    """Service layer for project operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(
            self,
            project_data: ProjectCreateModel) -> Project:
        """
        Create a new project.

        Args:
            project_data: The project creation data

        Returns:
            The created project

        Raises:
            Exception: If project creation fails
        """
        project = Project(
            name=project_data.name,
            description=project_data.description
        )

        self.db.add(project)

        await self.db.commit()

        await self.db.refresh(project)

        return project

    async def get_project_by_id(
            self, project_id: uuid.UUID) -> Optional[Project]:
        """
        Retrieve a project by its ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            The project if found, None otherwise
        """
        statement = select(Project).where(Project.id == project_id)
        result = await self.db.execute(statement)
        project = result.scalar_one_or_none()
        return project

    async def get_all_projects(self) -> List[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects
        """
        statement = select(Project)
        result = await self.db.execute(statement)
        projects_list = result.scalars().all()
        return list(projects_list)

    async def update_project(
            self,
            project_id: uuid.UUID,
            project_data: ProjectUpdateModel) -> Optional[Project]:
        """
        Update an existing project.

        Args:
            project_id: The unique identifier of the project
            project_data: The updated project data

        Returns:
            The updated project if found and updated successfully, None otherwise

        Raises:
            Exception: If project update fails
        """
        statement = select(Project).where(Project.id == project_id)
        result = await self.db.execute(statement)
        project = result.scalar_one_or_none()

        if not project:
            return None

        if project_data.name is not None:
            project.name = project_data.name
        if project_data.description is not None:
            project.description = project_data.description

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def delete_project(self, project_id: uuid.UUID) -> bool:
        """
        Delete a project by its ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            True if project was deleted successfully, False if not found

        Raises:
            Exception: If project deletion fails
        """
        statement = select(Project).where(Project.id == project_id)
        result = await self.db.execute(statement)
        project = result.scalar_one_or_none()

        if not project:
            return False

        await self.db.delete(project)
        await self.db.commit()

        return True

    async def project_exists(self, project_id: uuid.UUID) -> bool:
        """
        Check if a project exists by its ID.

        Args:
            project_id: The unique identifier of the project

        Returns:
            True if project exists, False otherwise
        """
        statement = select(Project).where(Project.id == project_id)
        result = await self.db.execute(statement)
        project = result.scalar_one_or_none()
        return project is not None

    async def create_task_for_project(
            self,
            project_id: uuid.UUID,
            task_data: TaskCreateModel) -> Task:
        """
        Create a new task under a specific project.

        Args:
            project_id: The project ID to create the task under
            task_data: The task creation data

        Returns:
            The created task

        Raises:
            HTTPException: If project not found
        """
        project = await self.get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        task = Task(
            title=task_data.title,
            priority=task_data.priority,
            completed=task_data.completed,
            project_id=project_id,
            due_date=task_data.due_date
        )

        self.db.add(task)

        await self.db.commit()

        await self.db.refresh(task)

        return task

    async def get_tasks_for_project(self, project_id: uuid.UUID) -> List[Task]:
        """
        Get all tasks under a specific project.

        Args:
            project_id: The project ID to get tasks for

        Returns:
            List of tasks for the project

        Raises:
            HTTPException: If project not found
        """
        project = await self.get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        statement = select(Task).where(
            Task.project_id == project_id).order_by(
            Task.priority.desc())
        result = await self.db.execute(statement)
        tasks_list = result.scalars().all()
        return list(tasks_list)
