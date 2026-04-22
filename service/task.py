from dataclasses import dataclass

from repository import TaskRepository, TaskCache
from schema.task import TaskSchema


@dataclass
class TaskService:
    # def __init__(self, task_repository: TaskRepository, task_cache: TaskCache):
    #     self.task_repository = task_repository
    #     self.task_cache = task_cache
    task_repository: TaskRepository
    task_cache: TaskCache
        
    def get_tasks(self):
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:    
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema