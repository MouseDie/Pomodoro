from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tasks, Categories
from app.infra.database import get_db_session
from app.schema import TaskCreateSchema, TaskSchema

class TaskRepository:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
        
    async def get_task(self, id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == id)
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(query)).scalar_one_or_none()
        return task
    
    
    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task
    
    
    async def get_tasks(self):
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(select(Tasks))).scalars().all()
        return task
    
    
    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(name=task.name, 
                     pomodoro_count=task.pomodoro_count,
                     category_id=task.category_id,
                     user_id=user_id
                     )
        async with self.db_session as session:
            session.add(task_model)
            await session.commit()
            return task_model.id
    
    
    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
            
            
    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name ==category_name)
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(query)).scalars().all()
            return task
        
        
    async def update_task_name(self, task_id: int, name: str):
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            await session.flush()
            return await self.get_task(task_id)
        
