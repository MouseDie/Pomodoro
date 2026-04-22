from typing import Annotated
from fastapi import FastAPI, APIRouter, status, Depends
from pydantic import BaseModel
#from dependency import get_tasks_repository, get_tasks_cache_repository
from dependency import get_task_service, get_tasks_repository
from fixtures import tasks as fixtures_tasks
from schema.task import TaskSchema
from database.database import get_db_session
from repository import TaskRepository, TaskCache
from service.task import TaskService

router = APIRouter(prefix="/task", tags=["task"])



@router.get(
    "/all",
    response_model=list[TaskSchema]
)
async def get_tasks(
    # task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    # task_cache: Annotated[TaskCache, Depends(get_tasks_cache_repository)],
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_tasks()


@router.post(
    "/",
    response_model=TaskSchema,
)
async def create_task(
    task: TaskSchema,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
)
async def patch_task(
    task_id: int,
    name: str,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    return task_repository.update_task_name(task_id, name)
    # for task in fixtures_tasks:
    #     if task["id"] == task_id:
    #         task["name"] = name
    #         return task
        
        
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    task_repository.delete_task(task_id)
    return {"message": "task deleted succesfully"}
    # for index, task in enumerate(fixtures_tasks):
    #     if task["id"] == task_id:
    #         del fixtures_tasks[index]
    #         return {"message": "task deleted"}
    # return {"message": "task not found"}