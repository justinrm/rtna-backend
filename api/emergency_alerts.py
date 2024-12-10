from fastapi import APIRouter, HTTPException
from app.utilities.cache import redis_cache
from app.utilities.logging import log_event, log_exception
from app.utilities.general import handle_error
import requests

router = APIRouter(prefix="/alerts", tags=["Emergency Alerts"])

@router.get("/{region}")
async def get_emergency_alerts(region: str):
    """
    Fetch and cache emergency alerts for a specific region.
    """
    cache_key = f"emergency_alerts:{region.lower()}"
    cached_data = await redis_cache.get(cache_key)
    if cached_data:
        log_event("CACHE_HIT", f"Cache hit for alerts in region {region}")
        return cached_data

    try:
        api_url = f"https://alerts.idaho.gov/{region}/alerts"  # Replace with actual regional API
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Cache the results
        await redis_cache.set(cache_key, data, expire=600)
        log_event("API_CALL", f"Fetched alerts for region {region}")
        return data
    except requests.RequestException as e:
        log_exception(e, f"Error fetching alerts for region {region}")
        raise HTTPException(status_code=500, detail=f"Error fetching alerts: {str(e)}")

