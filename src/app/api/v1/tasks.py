from fastapi import APIRouter, Depends, HTTPException
from app.schemas.tasks import TaskModel, TaskUpdateModel
from app.test.mock_tasks import tasks
from app.test.mock_projects import projects


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.put(
        "/{task_id}",
        summary="Update a task by ID",
        status_code=200,
        response_model=TaskModel)
async def update_task(
    task_id: int,
    updated_task: TaskUpdateModel
):
    # Find the task
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            # Validate project exists if project_id is being updated
            if updated_task.project_id is not None:
                project = next((proj for proj in projects if proj["id"] == updated_task.project_id), None)
                if not project:
                    raise HTTPException(status_code=404, detail="Project not found")
                tasks[index]["project_id"] = updated_task.project_id
            
            # Update other fields that were provided
            if updated_task.title is not None:
                tasks[index]["title"] = updated_task.title
            if updated_task.priority is not None:
                tasks[index]["priority"] = updated_task.priority
            if updated_task.completed is not None:
                tasks[index]["completed"] = updated_task.completed
            if updated_task.due_date is not None:
                tasks[index]["due_date"] = updated_task.due_date
            
            return tasks[index]
    
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete(
        "/{task_id}",
        summary="Delete a task by ID",
        status_code=204)
async def delete_task(task_id: int):
    global tasks
    original_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(tasks) == original_length:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return None
