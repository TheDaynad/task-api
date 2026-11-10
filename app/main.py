from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.core.redis import create_redis_client
from app.api.users import user_router
from app.api.tasks import task_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = create_redis_client()
    app.state.redis = redis_client

    try:
        await redis_client.ping()
        print("Redis connection successfully")

        yield

    finally:
        await redis_client.aclose()
        print("Redis connection closed")


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(task_router)



