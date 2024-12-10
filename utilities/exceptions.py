from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from aioredis.exceptions import RedisError

class AppException(HTTPException):
    """Base exception class for application-specific errors."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class DatabaseException(SQLAlchemyError):
    """Exception class for database-related errors."""
    pass

class CacheException(RedisError):
    """Exception class for Redis-related errors."""
    pass

def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler for SQLAlchemy errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database Error",
            "message": "An unexpected error occurred while interacting with the database.",
            "details": str(exc),
        },
    )

def redis_exception_handler(request: Request, exc: RedisError):
    """Handler for Redis errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Cache Error",
            "message": "An unexpected error occurred while interacting with the cache.",
            "details": str(exc),
        },
    )

