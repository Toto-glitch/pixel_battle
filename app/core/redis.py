from redis.asyncio import from_url

from .config import settings

redis = from_url(settings.redis.url, decode_responses=True)

async def close_redis_connection() -> None:
    await redis.close()
