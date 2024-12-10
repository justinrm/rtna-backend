from fastapi import APIRouter, HTTPException, Query
from app.modules.weather import fetch_weather
from app.modules.emergency_alerts import fetch_emergency_alerts
from app.modules.source_discovery import validate_sources
from app.modules.feedback import analyze_feedback_trends
from app.modules.market_data import fetch_market_items
from app.modules.content_aggregation import aggregate_articles
from app.utilities.logging import log_event, log_exception
from app.config import settings

router = APIRouter(prefix="/transparency", tags=["Transparency Panel"])

@router.get("/weather")
async def transparency_weather(location: str = Query(default="Lewiston")):
    """
    Get weather data for transparency panel.
    """
    try:
        weather = await fetch_weather(location)
        log_event("TRANSPARENCY", f"Weather data fetched for location: {location}")
        return {"location": location, "weather": weather}
    except Exception as e:
        log_exception(e, f"Error fetching weather for location: {location}")
        raise HTTPException(status_code=500, detail="Error fetching weather data.")

@router.get("/alerts")
async def transparency_alerts(region: str = Query(default="Lewiston")):
    """
    Get emergency alerts for transparency panel.
    """
    try:
        alerts = await fetch_emergency_alerts(region)
        log_event("TRANSPARENCY", f"Emergency alerts fetched for region: {region}")
        return {"region": region, "alerts": alerts}
    except Exception as e:
        log_exception(e, f"Error fetching alerts for region: {region}")
        raise HTTPException(status_code=500, detail="Error fetching alerts.")

@router.get("/sources/validate")
async def transparency_validate_sources():
    """
    Validate sources and report results.
    """
    try:
        validate_sources()
        log_event("TRANSPARENCY", "Source validation completed successfully.")
        return {"message": "Source validation completed successfully."}
    except Exception as e:
        log_exception(e, "Error during source validation.")
        raise HTTPException(status_code=500, detail="Error validating sources.")

@router.get("/feedback/trends")
async def transparency_feedback_trends():
    """
    Fetch feedback trends for transparency panel.
    """
    try:
        trends = analyze_feedback_trends()
        log_event("TRANSPARENCY", "Feedback trends fetched successfully.")
        return {"trends": trends}
    except Exception as e:
        log_exception(e, "Error fetching feedback trends.")
        raise HTTPException(status_code=500, detail="Error fetching feedback trends.")

@router.get("/market-data")
async def transparency_market_data(skip: int = Query(default=0), limit: int = Query(default=10), region: str = Query(default="Lewiston")):
    """
    Fetch market data (e.g., classifieds, items for sale) for transparency panel.
    """
    try:
        items = fetch_market_items(skip=skip, limit=limit, region=region)
        log_event("TRANSPARENCY", f"Market data fetched for region: {region}")
        return {"region": region, "items": items}
    except Exception as e:
        log_exception(e, f"Error fetching market data for region: {region}")
        raise HTTPException(status_code=500, detail="Error fetching market data.")

@router.get("/articles")
async def transparency_articles():
    """
    Trigger article aggregation for transparency panel.
    """
    try:
        aggregate_articles()
        log_event("TRANSPARENCY", "Articles aggregated successfully.")
        return {"message": "Articles aggregated successfully."}
    except Exception as e:
        log_exception(e, "Error aggregating articles.")
        raise HTTPException(status_code=500, detail="Error aggregating articles.")

@router.get("/config")
async def transparency_config():
    """
    Fetch current configuration settings for transparency purposes.
    """
    try:
        config_data = {
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
            "database_url": settings.DATABASE_URL,
            "redis_url": settings.REDIS_URL,
            "allowed_origins": settings.ALLOWED_ORIGINS,
        }
        log_event("TRANSPARENCY", "Configuration fetched successfully.")
        return {"config": config_data}
    except Exception as e:
        log_exception(e, "Error fetching configuration settings.")
        raise HTTPException(status_code=500, detail="Error fetching configuration.")

