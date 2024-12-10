from app.utilities.database import execute_query
from app.utilities.logging import get_logger, log_event, log_exception
from app.utilities.general import handle_error

logger = get_logger(__name__)

@handle_error
def fetch_market_items(skip: int = 0, limit: int = 10, region: str = "Lewiston"):
    """
    Fetch local market items, paginated.

    Args:
        skip (int): Number of items to skip for pagination.
        limit (int): Maximum number of items to fetch.
        region (str): Region for which market data is fetched.

    Returns:
        list: Market items.
    """
    log_event(logger, "DATA_FETCH", "Fetching market items", region=region, skip=skip, limit=limit)
    query = """
        SELECT * FROM items
        WHERE region = %s AND available = 1
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    """
    try:
        items = execute_query(query, (region, limit, skip))["data"]
        log_event(logger, "DATA_FETCH", f"Fetched {len(items)} market items", region=region)
        return items
    except Exception as e:
        log_exception(logger, e, "Error fetching market items", region=region)
        raise

@handle_error
def add_market_item(title: str, description: str, price: int, region: str):
    """
    Add a new market item.

    Args:
        title (str): Title of the item.
        description (str): Description of the item.
        price (int): Price of the item.
        region (str): Region for the item.

    Returns:
        dict: Confirmation message.
    """
    log_event(logger, "DATA_INSERT", "Adding new market item", title=title, region=region)
    query = """
        INSERT INTO items (title, description, price, region, available)
        VALUES (%s, %s, %s, %s, 1)
    """
    try:
        execute_query(query, (title, description, price, region))
        log_event(logger, "DATA_INSERT", "Market item added successfully", title=title, region=region)
        return {"message": "Item added successfully."}
    except Exception as e:
        log_exception(logger, e, "Error adding market item", title=title, region=region)
        raise

