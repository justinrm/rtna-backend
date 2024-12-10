from app.utilities.cache import redis_cache
from app.utilities.logging import get_logger, log_event, log_exception
from app.utilities.general import handle_error
import requests

logger = get_logger(__name__)

LEWISTON_API_URL = "https://alerts.idaho.gov/lewiston/alerts"
CACHE_EXPIRY_SECONDS = 300  # Cache alerts for 5 minutes

@handle_error
async def fetch_emergency_alerts(region: str = "Lewiston"):
    """
    Fetch and cache emergency alerts for Lewiston, Idaho.

    Args:
        region (str): The region to fetch alerts for (default: Lewiston).

    Returns:
        list: A list of emergency alerts for the specified region.
    """
    if region.lower() != "lewiston":
        log_event(logger, "ALERT_FETCH", f"Region '{region}' is unsupported. Defaulting to 'Lewiston'.", level="WARNING")
        region = "Lewiston"

    log_event(logger, "ALERT_FETCH", f"Fetching emergency alerts for region: {region}.")
    cache_key = f"emergency_alerts:{region.lower()}"
    cached_data = await redis_cache.get(cache_key)

    if cached_data:
        log_event(logger, "CACHE_HIT", f"Cache hit for alerts in region: {region}.")
        return cached_data

    try:
        api_url = LEWISTON_API_URL
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        alerts = response.json()
        if not alerts:
            log_event(logger, "ALERT_FETCH", f"No alerts found for region: {region}.", level="INFO")
            return []

        await redis_cache.set(cache_key, alerts, expire=CACHE_EXPIRY_SECONDS)
        log_event(logger, "ALERT_FETCH", f"Fetched and cached {len(alerts)} alerts for region: {region}.")
        return alerts

    except requests.RequestException as e:
        log_exception(logger, e, f"Error fetching alerts for region: {region}.")
        raise

@handle_error
async def clear_cached_alerts(region: str = "Lewiston"):
    """
    Clear cached emergency alerts for Lewiston, Idaho.

    Args:
        region (str): The region to clear the cache for (default: Lewiston).

    Returns:
        dict: Success message indicating the cache was cleared.
    """
    cache_key = f"emergency_alerts:{region.lower()}"
    try:
        result = await redis_cache.delete(cache_key)
        if result:
            log_event(logger, "CACHE_CLEAR", f"Cache cleared for alerts in region: {region}.")
            return {"message": f"Cache cleared for region: {region}."}
        else:
            log_event(logger, "CACHE_CLEAR", f"No cache to clear for region: {region}.", level="INFO")
            return {"message": f"No cache found for region: {region}."}
    except Exception as e:
        log_exception(logger, e, f"Error clearing cache for region: {region}.")
        raise

