from app.utilities.database import execute_query
from app.utilities.validation import is_valid_url
from app.utilities.logging import log_event, log_exception
from app.utilities.general import handle_error
from datetime import datetime

# Define a list of local news sources for discovery
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
    This function saves valid sources into the database.
    """
    log_event("DISCOVERY", "Starting source discovery process.")

    for source in LOCAL_SOURCES:
        if is_valid_url(source["website"]):
            query = """
                INSERT INTO news_sources (name, website, status, discovery_timestamp)
                VALUES (%s, %s, 'active', %s)
                ON CONFLICT (website) DO NOTHING
            """
            params = (source["name"], source["website"], datetime.now())
            execute_query(query, params)
            log_event("DISCOVERY", f"Source discovered and added: {source['name']}")
        else:
            log_event("VALIDATION", f"Invalid URL skipped: {source['website']}", level="WARNING")

    log_event("DISCOVERY", "Source discovery process completed successfully.")

@handle_error
def validate_sources():
    """
    Validate the availability of all sources in the database.
    Updates the source status to 'active' if valid or 'inactive' if unreachable.
    """
    log_event("VALIDATION", "Starting source validation process.")

    query = "SELECT id, website FROM news_sources"
    update_query = "UPDATE news_sources SET status = %s WHERE id = %s"
    sources = execute_query(query)["data"]

    for source in sources:
        source_id = source["id"]
        website = source["website"]

        status = "active" if is_valid_url(website) else "inactive"
        execute_query(update_query, (status, source_id))
        log_event("VALIDATION", f"Source {website} validated and updated to status: {status}")

    log_event("VALIDATION", "Source validation process completed successfully.")

@handle_error
def discover_sources_from_external_api(api_url: str, api_key: str):
    """
    Discover sources dynamically using an external API.
    Fetches potential news sources and registers them into the database.

    Args:
        api_url (str): The base URL of the external API.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of new sources discovered from the API.
    """
    import requests

    log_event("API_CALL", "Fetching sources from external API.")
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
                log_event("DISCOVERY", f"External source added: {source['name']}")

        log_event("API_CALL", f"Discovered {len(new_sources)} new sources from the external API.")
        return new_sources
    except requests.RequestException as e:
        log_exception(e, "Failed to fetch sources from external API.")
        raise

@handle_error
def save_sources_to_db(sources):
    """
    Save a list of sources to the database.

    Args:
        sources (list): A list of sources to save, each as a dictionary with keys 'name' and 'website'.
    """
    log_event("DATABASE", "Saving discovered sources to the database.")

    query = """
        INSERT INTO news_sources (name, website, status, discovery_timestamp)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (website) DO NOTHING
    """
    for source in sources:
        if not is_valid_url(source["website"]):
            log_event("VALIDATION", f"Invalid source URL skipped: {source['website']}", level="WARNING")
            continue

        params = (source["name"], source["website"], "active", datetime.now())
        execute_query(query, params)
        log_event("DATABASE", f"Source saved: {source['name']}")

    log_event("DATABASE", "All sources processed and saved.")

