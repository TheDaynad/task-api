from sqlalchemy.ext.asyncio import AsyncSession
from app.CRUD.user import get_user
from app.models.task import Task
from app.shemas.task import TaskCreate, TaskUpdate, TaskPatch
from sqlalchemy import select,delete


async def create_task(session: AsyncSession, task_data: TaskCreate):

    user = await get_user(session, task_data.user_id)

    if user is None:
        return None

    task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        user_id=task_data.user_id)

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_tasks(session: AsyncSession):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return tasks

async def get_task(session: AsyncSession, task_id: int):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    return task

async def update_task(session: AsyncSession, task_id : int,task_data: TaskUpdate):

    task = await get_task(session, task_id)

    if task is None:
        return None

    task.title = task_data.title
    task.description = task_data.description
    task.is_completed = task_data.is_completed

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def patch_task(session: AsyncSession, task_id : int, task_data: TaskPatch):
    task = await get_task(session, task_id)

    if task is None:
        return None

    data = task_data.model_dump(exclude_none=True)

    for key, value in data.items():
        setattr(task, key, value)


    await session.commit()
    await session.refresh(task)
    return task


async def get_user_tasks(session: AsyncSession,user_id: int):
    result = await session.execute(select(Task).where(Task.user_id == user_id))
    tasks = result.scalars().all()
    return tasks

async def delete_task(session: AsyncSession, task_id: int):
    result = await session.execute(delete(Task).where(Task.id == task_id))

    await session.commit()

    return result.rowcount















