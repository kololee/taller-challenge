from typing import List, Optional
import uuid
from datetime import datetime
from sqlmodel import Session
from fastapi import HTTPException

from app.models.projects import Project
from app.schemas.projects import ProjectCreateModel, ProjectUpdateModel
from app.test.mock_projects import projects
from app.test.mock_tasks import tasks


class ProjectService:
    """Service layer for project operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_project(self, project_data: ProjectCreateModel) -> dict:
        """
        Create a new project.
        
        Args:
            project_data: The project creation data
            
        Returns:
            The created project
            
        Raises:
            Exception: If project creation fails
        """
        new_id = max([p["id"] for p in projects], default=0) + 1
        new_project = {
            "id": new_id,
            "name": project_data.name,
            "description": project_data.description,
            "created_at": datetime.now().isoformat() + "Z"
        }
        projects.append(new_project)
        return new_project
    
    async def get_project_by_id(self, project_id: int) -> Optional[dict]:
        """
        Retrieve a project by its ID.
        
        Args:
            project_id: The unique identifier of the project
            
        Returns:
            The project if found, None otherwise
        """
        project = next((proj for proj in projects if proj["id"] == project_id), None)
        return project
    
    async def get_all_projects(self) -> List[dict]:
        """
        Retrieve all projects.
        
        Returns:
            List of all projects
        """
        return projects
    
    async def update_project(self, project_id: int, project_data: ProjectUpdateModel) -> Optional[dict]:
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
        for index, proj in enumerate(projects):
            if proj["id"] == project_id:
                if project_data.name is not None:
                    projects[index]["name"] = project_data.name
                if project_data.description is not None:
                    projects[index]["description"] = project_data.description
                return projects[index]
        return None
    
    async def delete_project(self, project_id: int) -> bool:
        """
        Delete a project by its ID.
        
        Args:
            project_id: The unique identifier of the project
            
        Returns:
            True if project was deleted successfully, False if not found
            
        Raises:
            Exception: If project deletion fails
        """
        global projects, tasks
        original_length = len(projects)
        projects[:] = [proj for proj in projects if proj["id"] != project_id]
        
        if len(projects) == original_length:
            return False
        
        # Delete associated tasks
        tasks[:] = [task for task in tasks if task["project_id"] != project_id]
        return True
    
    async def project_exists(self, project_id: int) -> bool:
        """
        Check if a project exists by its ID.
        
        Args:
            project_id: The unique identifier of the project
            
        Returns:
            True if project exists, False otherwise
        """
        return any(proj["id"] == project_id for proj in projects)
    
    async def get_projects_by_name(self, name: str) -> List[Project]:
        """
        Retrieve projects by name (exact or partial match).
        
        Args:
            name: The project name to search for
            
        Returns:
            List of projects matching the name criteria
        """
        # TODO: Implement project search by name logic
        pass
    
    async def count_projects(self) -> int:
        """
        Get the total count of projects.
        
        Returns:
            The total number of projects
        """
        return len(projects)
    
    async def create_task_for_project(self, project_id: int, task_data) -> dict:
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

        new_task = {
            "id": max([t["id"] for t in tasks], default=0) + 1,
            "project_id": project_id,
            "title": task_data.title,
            "priority": task_data.priority,
            "completed": task_data.completed,
            "due_date": task_data.due_date
        }
        
        tasks.append(new_task)
        return new_task
    
    async def get_tasks_for_project(self, project_id: int) -> List[dict]:
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

        project_tasks = [task for task in tasks if task["project_id"] == project_id]
        return project_tasks