from redis.asyncio import Redis
from fastapi import Request

from app.core.config import settings

def create_redis_client() -> Redis:
    return Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )

def get_redis(request: Request) -> Redis:
    return request.app.state.redis
