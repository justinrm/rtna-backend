from fastapi import APIRouter, HTTPException, Query
from app.modules.weather import fetch_weather

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/")
async def get_weather(location: str = Query(default="Lewiston")):
    """
    Get weather data for a specific location (default: Lewiston, Idaho).
    """
    try:
        weather = await fetch_weather(location)
        return {"location": location, "weather": weather}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

