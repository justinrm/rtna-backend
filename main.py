from fastapi import FastAPI, HTTPException
from app.modules.source_discovery import discover_sources, validate_sources
from app.modules.content_aggregation import aggregate_articles
from app.modules.feedback import analyze_feedback_trends
from app.modules.preferences import update_user_preferences
from app.modules.emergency_alerts import fetch_emergency_alerts
from app.utilities.logging import log_event, log_exception

app = FastAPI()

app.include_router(health_router)

@app.post("/sources/refresh")
async def refresh_sources():
    """
    Trigger source discovery and article aggregation.
    """
    try:
        log_event("API_CALL", "Triggering source discovery and article aggregation.")
        discover_sources()
        aggregate_articles()
        return {"status": "success", "message": "Sources and articles refreshed successfully."}
    except Exception as e:
        log_exception(e, "Error in source refresh process.")
        raise HTTPException(status_code=500, detail=f"Error refreshing sources: {str(e)}")

@app.post("/sources/validate")
async def validate_sources_endpoint():
    """
    Validate and update the status of all news sources.
    """
    try:
        log_event("API_CALL", "Validating sources.")
        validate_sources()
        return {"status": "success", "message": "Sources validated successfully."}
    except Exception as e:
        log_exception(e, "Error validating sources.")
        raise HTTPException(status_code=500, detail=f"Error validating sources: {str(e)}")

@app.put("/users/{user_id}/preferences")
async def update_user_preferences_endpoint(user_id: int, preferences: dict):
    """
    Update user preferences for personalized content.
    """
    try:
        log_event("API_CALL", f"Updating preferences for user {user_id}.")
        update_user_preferences(user_id, preferences)
        return {"status": "success", "message": "Preferences updated successfully."}
    except Exception as e:
        log_exception(e, f"Error updating preferences for user {user_id}.")
        raise HTTPException(status_code=500, detail=f"Error updating preferences: {str(e)}")

@app.get("/feedback/analysis")
async def get_feedback_analysis():
    """
    Fetch trends based on user feedback.
    """
    try:
        log_event("API_CALL", "Fetching feedback analysis.")
        trends = analyze_feedback_trends()
        return {"status": "success", "trends": trends}
    except Exception as e:
        log_exception(e, "Error analyzing feedback trends.")
        raise HTTPException(status_code=500, detail=f"Error analyzing feedback trends: {str(e)}")

@app.get("/alerts/{region}")
async def get_emergency_alerts_endpoint(region: str):
    """
    Fetch emergency alerts for a specific region.
    """
    try:
        log_event("API_CALL", f"Fetching alerts for region: {region}.")
        alerts = await fetch_emergency_alerts(region)
        return {"status": "success", "alerts": alerts}
    except Exception as e:
        log_exception(e, f"Error fetching alerts for region: {region}.")
        raise HTTPException(status_code=500, detail=f"Error fetching alerts: {str(e)}")

@app.get("/")
async def root():
    """
    Health check endpoint for the API.
    """
    log_event("HEALTH_CHECK", "Root endpoint accessed.")
    return {"status": "success", "message": "API is running."}

