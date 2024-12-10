from fastapi import APIRouter, HTTPException
from app.modules.feedback import add_feedback, get_feedback, analyze_feedback_trends
from app.utilities.validation import sanitize_input

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/")
async def submit_feedback(user_id: int, content_id: int, feedback_type: str, impact_score: int = 1):
    """
    Submit feedback for a content item.
    """
    try:
        feedback_type = sanitize_input(feedback_type)
        result = add_feedback(user_id, content_id, feedback_type, impact_score)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{content_id}")
async def fetch_feedback(content_id: int):
    """
    Fetch all feedback for a specific content item.
    """
    try:
        feedback = get_feedback(content_id)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends")
async def fetch_feedback_trends():
    """
    Fetch aggregated feedback trends across all content.
    """
    try:
        trends = analyze_feedback_trends()
        return {"trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

