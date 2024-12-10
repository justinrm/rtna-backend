from fastapi import APIRouter, HTTPException
from app.utilities.cache import redis_cache

router = APIRouter(prefix="/cache", tags=["Cache"])

@router.on_event("startup")
async def startup_event():
    """Connect to Redis during app startup."""
    await redis_cache.connect()

@router.on_event("shutdown")
async def shutdown_event():
    """Disconnect from Redis during app shutdown."""
    await redis_cache.disconnect()

@router.get("/{key}")
async def read_cache(key: str):
    """Retrieve a value from the cache by key."""
    try:
        value = await redis_cache.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found.")
        return {"key": key, "value": value}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def write_cache(key: str, value: str, expire: int = None):
    """Write a key-value pair to the cache."""
    try:
        await redis_cache.set(key, value, expire)
        return {"message": "Key-Value pair added to cache", "key": key, "value": value, "expire": expire}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

