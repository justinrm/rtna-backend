import aioredis
from aioredis import Redis
from app.config import settings

class RedisCache:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis_url = redis_url
        self.redis: Redis = None

    async def connect(self):
        """Establish connection to the Redis server."""
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        """Close the connection to the Redis server."""
        if self.redis:
            await self.redis.close()

    async def set(self, key: str, value: str, expire: int = None):
        """Set a key-value pair with an optional expiration time."""
        try:
            await self.redis.set(key, value, ex=expire)
        except Exception as e:
            raise RuntimeError(f"Failed to set key '{key}': {e}")

    async def get(self, key: str):
        """Get the value for a key."""
        try:
            value = await self.redis.get(key)
            return value.decode("utf-8") if value else None
        except Exception as e:
            raise RuntimeError(f"Failed to get key '{key}': {e}")

    async def delete(self, key: str):
        """Delete a key."""
        try:
            await self.redis.delete(key)
        except Exception as e:
            raise RuntimeError(f"Failed to delete key '{key}': {e}")

# Instantiate a shared cache instance
redis_cache = RedisCache()
