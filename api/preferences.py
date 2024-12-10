from fastapi import APIRouter, HTTPException
from app.modules.preferences import get_user_preferences, update_user_preferences
from app.utilities.validation import sanitize_input

router = APIRouter(prefix="/preferences", tags=["Preferences"])

@router.get("/{user_id}")
async def fetch_preferences(user_id: int):
    """
    Fetch user preferences by user ID.
    """
    try:
        preferences = get_user_preferences(user_id)
        return {"preferences": preferences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
async def update_preferences(user_id: int, preferences: dict):
    """
    Update user preferences.
    """
    try:
        sanitized_preferences = sanitize_input(preferences)
        result = update_user_preferences(user_id, sanitized_preferences)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

