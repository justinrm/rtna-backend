from app.utilities.cache import redis_cache
from app.utilities.logging import log_event, log_exception
from app.utilities.general import handle_error
import requests

# Define the region-specific API endpoint and other constants
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
        log_event("ALERT_FETCH", f"Region '{region}' is unsupported. Defaulting to 'Lewiston'.", level="WARNING")
        region = "Lewiston"

    log_event("ALERT_FETCH", f"Fetching emergency alerts for region: {region}.")
    cache_key = f"emergency_alerts:{region.lower()}"
    cached_data = await redis_cache.get(cache_key)

    # Serve from cache if available
    if cached_data:
        log_event("CACHE_HIT", f"Cache hit for alerts in region: {region}.")
        return cached_data

    # If no cached data, fetch from regional API
    try:
        api_url = LEWISTON_API_URL  # Use the specific API for Lewiston, Idaho
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        alerts = response.json()
        if not alerts:
            log_event("ALERT_FETCH", f"No alerts found for region: {region}.", level="INFO")
            return []

        # Cache the fetched alerts
        await redis_cache.set(cache_key, alerts, expire=CACHE_EXPIRY_SECONDS)
        log_event("ALERT_FETCH", f"Fetched and cached {len(alerts)} alerts for region: {region}.")
        return alerts

    except requests.RequestException as e:
        log_exception(e, f"Error fetching alerts for region: {region}.")
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
    if region.lower() != "lewiston":
        log_event("CACHE_CLEAR", f"Region '{region}' is unsupported. Defaulting to 'Lewiston'.", level="WARNING")
        region = "Lewiston"

    cache_key = f"emergency_alerts:{region.lower()}"
    try:
        result = await redis_cache.delete(cache_key)
        if result:
            log_event("CACHE_CLEAR", f"Cache cleared for alerts in region: {region}.")
            return {"message": f"Cache cleared for region: {region}."}
        else:
            log_event("CACHE_CLEAR", f"No cache to clear for region: {region}.", level="INFO")
            return {"message": f"No cache found for region: {region}."}
    except Exception as e:
        log_exception(e, f"Error clearing cache for region: {region}.")
        raise

@handle_error
async def get_cached_alerts(region: str = "Lewiston"):
    """
    Retrieve cached alerts for Lewiston, Idaho.

    Args:
        region (str): The region to retrieve cached alerts for (default: Lewiston).

    Returns:
        list: Cached alerts if available, or an empty list.
    """
    if region.lower() != "lewiston":
        log_event("CACHE_MISS", f"Region '{region}' is unsupported. Defaulting to 'Lewiston'.", level="WARNING")
        region = "Lewiston"

    cache_key = f"emergency_alerts:{region.lower()}"
    try:
        cached_data = await redis_cache.get(cache_key)
        if cached_data:
            log_event("CACHE_HIT", f"Retrieved cached alerts for region: {region}.")
            return cached_data
        else:
            log_event("CACHE_MISS", f"No cached alerts for region: {region}.")
            return []
    except Exception as e:
        log_exception(e, f"Error retrieving cached alerts for region: {region}.")
        raise

