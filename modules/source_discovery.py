from app.utilities.database import execute_query
from app.utilities.validation import is_valid_url
from app.utilities.logging import get_logger, log_event, log_exception
from app.utilities.general import handle_error
from datetime import datetime

logger = get_logger(__name__)

LOCAL_SOURCES = [
    {"name": "Lewiston Tribune", "website": "https://lmtribune.com/rss"},
    {"name": "Idaho Statesman", "website": "https://idahostatesman.com/local/rss"},
    {"name": "KLEW TV", "website": "https://klewtv.com/rss"},
    {"name": "The Moscow-Pullman Daily News", "website": "https://dnews.com/rss"},
    {"name": "Idaho County Free Press", "website": "https://idahocountyfreepress.com/rss"},
]

@handle_error
def discover_sources():
    """
    Discover and register new sources from predefined local sources.
    """
    log_event(logger, "DISCOVERY", "Starting source discovery process")

    for source in LOCAL_SOURCES:
        if is_valid_url(source["website"]):
            query = """
                INSERT INTO news_sources (name, website, status, discovery_timestamp)
                VALUES (%s, %s, 'active', %s)
                ON CONFLICT (website) DO NOTHING
            """
            params = (source["name"], source["website"], datetime.now())
            execute_query(query, params)
            log_event(logger, "DISCOVERY", "Source added", source_name=source["name"], website=source["website"])
        else:
            log_event(logger, "VALIDATION", "Invalid source URL skipped", website=source["website"], level="WARNING")

    log_event(logger, "DISCOVERY", "Source discovery process completed successfully")

@handle_error
def validate_sources():
    """
    Validate the availability of all sources in the database.
    Updates the source status to 'active' if valid or 'inactive' if unreachable.
    """
    log_event(logger, "VALIDATION", "Starting source validation process")

    query = "SELECT id, website FROM news_sources"
    update_query = "UPDATE news_sources SET status = %s WHERE id = %s"
    sources = execute_query(query)["data"]

    for source in sources:
        source_id = source["id"]
        website = source["website"]

        status = "active" if is_valid_url(website) else "inactive"
        execute_query(update_query, (status, source_id))
        log_event(logger, "VALIDATION", "Source validated", source_id=source_id, website=website, status=status)

    log_event(logger, "VALIDATION", "Source validation process completed successfully")

@handle_error
def discover_sources_from_external_api(api_url: str, api_key: str):
    """
    Discover sources dynamically using an external API.

    Args:
        api_url (str): The base URL of the external API.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of new sources discovered from the API.
    """
    import requests

    log_event(logger, "API_CALL", "Fetching sources from external API")
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        sources = response.json().get("sources", [])

        new_sources = []
        for source in sources:
            if is_valid_url(source["url"]):
                query = """
                    INSERT INTO news_sources (name, website, status, discovery_timestamp)
                    VALUES (%s, %s, 'pending', %s)
                    ON CONFLICT (website) DO NOTHING
                """
                params = (source["name"], source["url"], datetime.now())
                execute_query(query, params)
                new_sources.append(source["name"])
                log_event(logger, "DISCOVERY", "External source added", source_name=source["name"])

        log_event(logger, "API_CALL", f"Discovered {len(new_sources)} new sources from the external API")
        return new_sources
    except requests.RequestException as e:
        log_exception(logger, e, "Failed to fetch sources from external API")
        raise

