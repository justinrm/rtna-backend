from app.utilities.database import execute_query
from app.utilities.logging import get_logger, log_event, log_exception
from app.utilities.general import handle_error

logger = get_logger(__name__)

@handle_error
def add_feedback(user_id: int, content_id: int, feedback_type: str, impact_score: int = 1):
    """
    Add feedback for a specific content item.

    Args:
        user_id (int): ID of the user providing feedback.
        content_id (int): ID of the content receiving feedback.
        feedback_type (str): Type of feedback ('like', 'dislike', 'flag').
        impact_score (int): Impact score of the feedback (default: 1).

    Returns:
        dict: Success message.
    """
    log_event(logger, "DATA_INSERT", "Adding feedback", user_id=user_id, content_id=content_id, feedback_type=feedback_type)
    query = """
        INSERT INTO feedback (user_id, content_id, feedback_type, impact_score, timestamp)
        VALUES (%s, %s, %s, %s, NOW())
    """
    try:
        execute_query(query, (user_id, content_id, feedback_type, impact_score))
        log_event(logger, "DATA_INSERT", "Feedback added successfully", user_id=user_id, content_id=content_id)
        return {"message": "Feedback added successfully."}
    except Exception as e:
        log_exception(logger, e, "Error adding feedback", user_id=user_id, content_id=content_id)
        raise

@handle_error
def get_feedback(content_id: int):
    """
    Retrieve feedback for a specific content item.

    Args:
        content_id (int): ID of the content for which feedback is being retrieved.

    Returns:
        list: List of feedback entries.
    """
    log_event(logger, "DATA_FETCH", "Fetching feedback", content_id=content_id)
    query = """
        SELECT user_id, feedback_type, impact_score, timestamp
        FROM feedback
        WHERE content_id = %s
        ORDER BY timestamp DESC
    """
    try:
        feedback = execute_query(query, (content_id,))["data"]
        log_event(logger, "DATA_FETCH", f"Retrieved {len(feedback)} feedback records", content_id=content_id)
        return feedback
    except Exception as e:
        log_exception(logger, e, "Error retrieving feedback", content_id=content_id)
        raise

@handle_error
def analyze_feedback_trends():
    """
    Analyze trends in feedback across all content.

    Returns:
        list: Aggregated feedback trends with counts and impact scores.
    """
    log_event(logger, "ANALYSIS", "Starting feedback trends analysis")
    query = """
        SELECT feedback_type, COUNT(*) as feedback_count, SUM(impact_score) as total_impact
        FROM feedback
        GROUP BY feedback_type
        ORDER BY total_impact DESC
    """
    try:
        trends = execute_query(query)["data"]
        log_event(logger, "ANALYSIS", "Feedback trends analysis completed successfully")
        return trends
    except Exception as e:
        log_exception(logger, e, "Error analyzing feedback trends")
        raise

