import logging
import logging.handlers
from datetime import datetime
import os
import json

# Create log directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Define log file paths
GENERAL_LOG_FILE = os.path.join(LOG_DIR, "general.log")
MEDIA_METADATA_LOG_FILE = os.path.join(LOG_DIR, "media_metadata.log")
USER_METADATA_LOG_FILE = os.path.join(LOG_DIR, "user_metadata.log")

# Configure log rotation (max 10 MB per file, keep 10 backups)
log_rotation_handler = lambda log_file: logging.handlers.RotatingFileHandler(
    log_file, maxBytes=10 * 1024 * 1024, backupCount=10
)

# General logger
general_logger = logging.getLogger("general")
general_logger.setLevel(logging.INFO)
general_handler = log_rotation_handler(GENERAL_LOG_FILE)
general_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
general_logger.addHandler(general_handler)

# Media metadata logger
media_logger = logging.getLogger("media_metadata")
media_logger.setLevel(logging.INFO)
media_handler = log_rotation_handler(MEDIA_METADATA_LOG_FILE)
media_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
media_logger.addHandler(media_handler)

# User metadata logger
user_logger = logging.getLogger("user_metadata")
user_logger.setLevel(logging.INFO)
user_handler = log_rotation_handler(USER_METADATA_LOG_FILE)
user_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
user_logger.addHandler(user_handler)

def log_event(category: str, message: str, level: str = "INFO"):
    """
    Logs a general event in the application.
    Args:
        category (str): Event category (e.g., SCHEDULER, API_CALL).
        message (str): Message describing the event.
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR).
    """
    log_message = f"[{category}] {message}"
    if level.upper() == "DEBUG":
        general_logger.debug(log_message)
    elif level.upper() == "INFO":
        general_logger.info(log_message)
    elif level.upper() == "WARNING":
        general_logger.warning(log_message)
    elif level.upper() == "ERROR":
        general_logger.error(log_message)

def log_exception(exception: Exception, context: str = ""):
    """
    Logs exceptions with detailed stack traces.
    Args:
        exception (Exception): The exception instance to log.
        context (str): Context or message describing where the exception occurred.
    """
    log_message = f"{context}: {str(exception)}"
    general_logger.error(log_message, exc_info=True)

def log_user_metadata(user_id: int, metadata: dict):
    """
    Logs aggregated user metadata for analytics.
    Args:
        user_id (int): The ID of the user.
        metadata (dict): Aggregated metadata related to the user's actions.
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "metadata": metadata,
    }
    user_logger.info(json.dumps(log_data))

def log_media_metadata(content_id: int, metadata: dict):
    """
    Logs detailed media metadata for ML training.
    Args:
        content_id (int): The ID of the content.
        metadata (dict): Metadata about the content.
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "content_id": content_id,
        "metadata": metadata,
    }
    media_logger.info(json.dumps(log_data))

