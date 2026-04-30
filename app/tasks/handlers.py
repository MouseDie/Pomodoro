from typing import Annotated
from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
#from dependency import get_tasks_repository, get_tasks_cache_repository
from app.dependency import get_task_service, get_tasks_repository, get_request_user_id
from app.exception import TaskNotFound
from fixtures import tasks as fixtures_tasks
from app.tasks.schema import TaskCreateSchema, TaskSchema
from app.infra.database import get_db_session
from app.tasks.repository import TaskRepository, TaskCache
from app.tasks.service import TaskService

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
    tasks = await task_service.get_tasks()
    return tasks


# Если разложить это по шагам, то происходит следующее:
# Запрос прилетает в FastAPI: Кто-то вызвал POST-запрос на ваш эндпоинт.
# FastAPI видит зависимость: Он замечает Depends(get_tasks_repository) и ставит выполнение функции create_task на паузу.
# Вызов функции-провайдера: FastAPI запускает get_tasks_repository().
# Получение объекта: Эта функция создает и возвращает объект (экземпляр класса) TaskRepository.
# Инъекция (внедрение): FastAPI берет этот созданный объект и сам подставляет его в вашу переменную task_repository внутри функции create_task.
# Выполнение функции: Теперь, когда у create_task есть всё необходимое (и данные из JSON, и готовый репозиторий), она начинает работать.
# Важный нюанс:
# TaskRepository — это не просто «формат данных» (как JSON), а живой объект класса, у которого есть методы. Именно поэтому вы можете сразу вызвать у него функцию:
# task_repository.create_task(task).

@router.post(
    "/",
    response_model=TaskSchema,
)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
    
    # task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    # user_id: int = Depends(get_request_user_id)
):
    # task_id = task_repository.create_task(task)
    # task.id = task_id
    task = await task_service.create_task(body, user_id)
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
)
async def patch_task(
    task_id: int,
    name: str,
   # task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
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
    #task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    #return {"message": "task deleted succesfully"}
    # for index, task in enumerate(fixtures_tasks):
    #     if task["id"] == task_id:
    #         del fixtures_tasks[index]
    #         return {"message": "task deleted"}
    # return {"message": "task not found"}