from app.utilities.database import execute_query
from app.utilities.validation import is_valid_url
from app.utilities.logging import log_event, log_exception
from app.utilities.general import format_datetime, handle_error
import feedparser
from datetime import datetime

@handle_error
def aggregate_articles():
    """
    Aggregate articles from all active sources and save them to the database.
    Fetches RSS feeds for each source and parses articles for insertion.
    """
    log_event("AGGREGATION", "Starting article aggregation.")

    # Fetch all active sources
    query = "SELECT id, website FROM news_sources WHERE status = 'active'"
    sources = execute_query(query)["data"]

    if not sources:
        log_event("AGGREGATION", "No active sources available for aggregation.", level="INFO")
        return {"message": "No active sources to aggregate from."}

    total_articles = 0
    for source in sources:
        source_id = source["id"]
        rss_url = source["website"]

        if not is_valid_url(rss_url):
            log_event("VALIDATION", f"Skipping invalid RSS URL: {rss_url}", level="WARNING")
            continue

        # Fetch and parse the RSS feed
        articles = fetch_rss_feed(rss_url, source_id)
        if articles:
            save_articles_to_db(articles)
            total_articles += len(articles)

    log_event("AGGREGATION", f"Article aggregation completed. Total articles aggregated: {total_articles}")
    return {"message": "Article aggregation completed successfully.", "total_articles": total_articles}

@handle_error
def fetch_rss_feed(rss_url: str, source_id: int):
    """
    Fetch and parse articles from an RSS feed.
    
    Args:
        rss_url (str): The RSS feed URL.
        source_id (int): The ID of the source associated with the feed.

    Returns:
        list: A list of parsed articles with relevant metadata.
    """
    log_event("RSS_FETCH", f"Fetching RSS feed from {rss_url}.")
    try:
        feed = feedparser.parse(rss_url)

        if feed.bozo:
            log_event("RSS_ERROR", f"Malformed RSS feed from {rss_url}.", level="WARNING")
            return []

        articles = []
        for entry in feed.entries:
            published_at = format_datetime(entry.get("published_parsed")) if entry.get("published_parsed") else None
            article = {
                "title": entry.get("title", "No Title"),
                "content": entry.get("summary", ""),
                "url": entry.get("link", ""),
                "published_at": published_at,
                "source_id": source_id,
                "transparency_metadata": {
                    "source_name": feed.feed.get("title", "Unknown Source"),
                    "rss_url": rss_url,
                    "fetched_at": format_datetime(datetime.now())
                }
            }
            if is_valid_url(article["url"]):
                articles.append(article)
            else:
                log_event("DATA_VALIDATION", f"Skipping article with invalid URL: {article['url']}", level="WARNING")

        log_event("RSS_FETCH", f"Fetched {len(articles)} articles from {rss_url}.")
        return articles
    except Exception as e:
        log_exception(e, f"Failed to fetch RSS feed from {rss_url}.")
        return []

@handle_error
def save_articles_to_db(articles):
    """
    Save aggregated articles to the database.

    Args:
        articles (list): A list of articles to save, with metadata.

    Returns:
        None
    """
    if not articles:
        log_event("DATA_PROCESSING", "No articles to save.", level="INFO")
        return

    query = """
        INSERT INTO articles (title, content, url, published_at, fetched_at, source_id, transparency_metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
    """
    for article in articles:
        params = (
            article["title"],
            article["content"],
            article["url"],
            article["published_at"],
            article["transparency_metadata"]["fetched_at"],
            article["source_id"],
            article["transparency_metadata"]
        )
        try:
            execute_query(query, params)
            log_event("DATABASE", f"Article saved: {article['title']}")
        except Exception as e:
            log_exception(e, f"Error saving article: {article['url']}")

    log_event("DATABASE", f"{len(articles)} articles saved to the database.")

