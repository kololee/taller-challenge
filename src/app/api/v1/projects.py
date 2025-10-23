from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.schemas.projects import ProjectModel, ProjectCreateModel, ProjectUpdateModel
from app.schemas.tasks import TaskCreateModel
from app.test.mock_projects import projects
from app.test.mock_tasks import tasks


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
        "/",
        summary="Create a new project",
        status_code=201,
        response_model=ProjectModel)
async def create_project(project: ProjectCreateModel):
    new_id = max([p["id"] for p in projects], default=0) + 1
    new_project = {
        "id": new_id,
        "name": project.name,
        "description": project.description,
        "created_at": datetime.now().isoformat() + "Z"
    }
    projects.append(new_project)
    return new_project


@router.get(
        "/{project_id}",
        summary="Get project details by ID",
        status_code=200,
        response_model=ProjectModel)
async def get_project_details(
    project_id: int,
    # db: Session = Depends(get_db)
):
    project = next((proj for proj in projects if proj["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put(
        "/{project_id}",
        summary="Update project information by ID",
        status_code=200,
        response_model=ProjectModel)
async def update_project_info(
    project_id: int,
    updated_project: ProjectUpdateModel,
    # db: Session = Depends(get_db)
):
    for index, proj in enumerate(projects):
        if proj["id"] == project_id:
            if updated_project.name is not None:
                projects[index]["name"] = updated_project.name
            if updated_project.description is not None:
                projects[index]["description"] = updated_project.description
            return projects[index]
    raise HTTPException(status_code=404, detail="Project not found")


@router.delete(
        "/{project_id}",
        summary="Delete a project by ID",
        status_code=204)
async def delete_project(
    project_id: int,
    # db: Session = Depends(get_db)
):
    global projects, tasks
    original_length = len(projects)
    projects = [proj for proj in projects if proj["id"] != project_id]
    
    if len(projects) == original_length:
        raise HTTPException(status_code=404, detail="Project not found")
    
    tasks[:] = [task for task in tasks if task["project_id"] != project_id]
    
    return None


@router.post(
        "/{project_id}/tasks/",
        summary="Create a new task under a specific project",
        status_code=201,
        response_model=dict)
async def create_task_for_project(project_id: int, task: TaskCreateModel):
    project = next((proj for proj in projects if proj["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "project_id": project_id,
        "title": task.title,
        "priority": task.priority,
        "completed": task.completed,
        "due_date": task.due_date
    }
    
    tasks.append(new_task)
    
    return new_task


@router.get(
        "/{project_id}/tasks/",
        summary="Get all tasks under a specific project",
        status_code=200,
        response_model=list[dict])
async def get_tasks_for_project(project_id: int):
    project = next((proj for proj in projects if proj["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_tasks = [task for task in tasks if task["project_id"] == project_id]
    return project_tasks
