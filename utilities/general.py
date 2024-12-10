import os
import functools
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(level=logging.INFO)

def handle_error(func):
    """
    Decorator to handle errors gracefully in functions.
    Logs the exception and prevents the application from crashing.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            return {"error": f"An unexpected error occurred in {func.__name__}"}
    return wrapper

def format_datetime(dt: datetime) -> str:
    """
    Format a datetime object into a string.
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def load_env_variable(key: str, default: str = None) -> str:
    """
    Load an environment variable, with an optional default value.
    Raises an exception if the variable is not set and no default is provided.
    """
    value = os.getenv(key)
    if value is None and default is None:
        raise EnvironmentError(f"Environment variable {key} not set.")
    return value or default

