from app.utilities.cache import redis_cache
from app.utilities.logging import log_event, log_exception
from app.utilities.general import handle_error
import requests
from datetime import datetime

@handle_error
async def fetch_weather(location: str):
    """
    Fetch and cache weather data for a specific location.

    Args:
        location (str): City or region to fetch weather for.

    Returns:
        dict: Weather data.
    """
    cache_key = f"weather:{location.lower()}"
    cached_data = await redis_cache.get(cache_key)
    if cached_data:
        log_event("CACHE_HIT", f"Cache hit for weather in location: {location}")
        return cached_data

    try:
        # Replace with an actual weather API URL and key
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=YOUR_API_KEY&units=imperial"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Cache the results
        await redis_cache.set(cache_key, data, expire=3600)  # Cache for 1 hour
        log_event("API_CALL", f"Fetched weather for location: {location}")
        return data
    except requests.RequestException as e:
        log_exception(e, f"Error fetching weather for location: {location}")
        raise

