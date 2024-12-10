from app.utilities.cache import redis_cache
from app.utilities.logging import get_logger, log_event, log_exception
from app.utilities.general import handle_error
import requests
from datetime import datetime

logger = get_logger(__name__)

@handle_error
async def fetch_weather(location: str):
    """
    Fetch and cache weather data for a specific location.

    Args:
        location (str): City or region to fetch weather for.

    Returns:
        dict: Weather data.
    """
    log_event(logger, "API_CALL", "Fetching weather data", location=location)
    cache_key = f"weather:{location.lower()}"
    cached_data = await redis_cache.get(cache_key)
    if cached_data:
        log_event(logger, "CACHE_HIT", "Cache hit for weather data", location=location)
        return cached_data

    try:
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=imperial"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        await redis_cache.set(cache_key, data, expire=3600)  # Cache for 1 hour
        log_event(logger, "API_CALL", "Weather data fetched and cached", location=location)
        return data
    except requests.RequestException as e:
        log_exception(logger, e, "Error fetching weather data", location=location)
        raise

