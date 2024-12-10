from fastapi import APIRouter, HTTPException
from app.utilities.database import get_db
from app.utilities.cache import redis_cache
from sqlalchemy.exc import SQLAlchemyError
from aioredis.exceptions import RedisError
from app.utilities.logging import general_logger, log_event, log_exception

router = APIRouter()

@router.get("/health", summary="Check the health of backend services")
async def health_check():
    """
    Health check endpoint to ensure backend components are operational.

    Returns:
        dict: Health status of the backend components.
    """
    health_status = {
        "status": "healthy",
        "db": "unknown",
        "redis": "unknown",
    }

    # Check database connection
    try:
        with next(get_db()) as db:
            db.execute("SELECT 1")
        health_status["db"] = "connected"
        log_event(general_logger, "HEALTH_CHECK", "Database connection is healthy")
    except SQLAlchemyError as e:
        health_status["status"] = "unhealthy"
        health_status["db"] = "disconnected"
        log_exception(general_logger, e, "Database connection failed")

    # Check Redis connection
    try:
        await redis_cache.connect()
        await redis_cache.set("health_check", "ok", expire=1)
        redis_status = await redis_cache.get("health_check")
        await redis_cache.delete("health_check")
        if redis_status == "ok":
            health_status["redis"] = "connected"
            log_event(general_logger, "HEALTH_CHECK", "Redis connection is healthy")
        else:
            raise RedisError("Redis health check failed")
    except RedisError as e:
        health_status["status"] = "unhealthy"
        health_status["redis"] = "disconnected"
        log_exception(general_logger, e, "Redis connection failed")
    finally:
        await redis_cache.disconnect()

    # Return health status
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)

    return health_status

