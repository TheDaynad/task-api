from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from redis.exceptions import RedisError
import json

from app.shemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskPatch
from app.db.database import get_db
from app.CRUD.task import create_task,get_tasks,get_task,update_task,patch_task,get_user_tasks,delete_task
from app.CRUD.user import get_user
from app.core.redis import get_redis

task_router = APIRouter()

@task_router.post("/tasks", response_model=TaskResponse)
async def create_task_endpoint(task: TaskCreate, session: AsyncSession = Depends(get_db),redis: Redis = Depends(get_redis)):
    created_task = await create_task(session, task)

    if created_task is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        await redis.delete("tasks:list")
    except RedisError:
        pass

    return created_task

@task_router.get("/tasks",response_model=list[TaskResponse])
async def get_tasks_endpoint(session: AsyncSession = Depends(get_db),redis: Redis = Depends(get_redis)):
    try:
        cached_tasks = await redis.get("tasks:list")
    except RedisError:
        cached_tasks = None

    if cached_tasks is not None:
        return json.loads(cached_tasks)

    tasks = await get_tasks(session)

    tasks_data = [
        TaskResponse.model_validate(task).model_dump()
        for task in tasks
    ]

    tasks_json =json.dumps(tasks_data)

    try:
        await redis.setex(f"tasks:list",300,tasks_json)
    except RedisError:
        pass

    return tasks

@task_router.get("/tasks/{task_id}",response_model=TaskResponse)
async def get_tasks_endpoint(task_id: int,session: AsyncSession = Depends(get_db),redis: Redis = Depends(get_redis)):
    try:
        cached_task = await redis.get(f"task:{task_id}")
    except RedisError:
        cached_task = None

    if cached_task is not None:
        return json.loads(cached_task)

    task = await get_task(session, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = TaskResponse.model_validate(task).model_dump_json()

    try:
        await redis.setex(f'task:{task_id}',300,task_data)
    except RedisError:
        pass

    return task

@task_router.put("/tasks/{task_id}",response_model=TaskResponse)
async def update_task_endpoint(task: TaskUpdate, task_id : int,session: AsyncSession = Depends(get_db),redis: Redis = Depends(get_redis)):
    updated_task = await update_task(session, task_id, task)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        await redis.delete(f"task:{task_id}",f"tasks:list")
    except RedisError:
        pass
    return updated_task


@task_router.patch("/tasks/{task_id}",response_model=TaskResponse)
async def patch_task_endpoint(task: TaskPatch, task_id : int, session: AsyncSession = Depends(get_db),redis: Redis = Depends(get_redis)):
    patched_task = await patch_task(session, task_id, task)

    if patched_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        await redis.delete(f"task:{task_id}",f"tasks:list")
    except RedisError:
        pass
    return patched_task

@task_router.get("/users/{user_id}/tasks",response_model=list[TaskResponse])
async def get_user_tasks_endpoint(user_id : int, session: AsyncSession = Depends(get_db)):
    user = await get_user(session, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    tasks = await get_user_tasks(session, user_id)

    return tasks

@task_router.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: int,session: AsyncSession = Depends(get_db),redis: Redis = Depends(get_redis)):
    deleted_task = await delete_task(session, task_id)
    if deleted_task == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        await redis.delete(f"task:{task_id}",f"tasks:list")
    except RedisError:
        pass
    return