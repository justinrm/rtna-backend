from app.utilities.database import execute_query
from app.utilities.logging import log_event, log_exception
from app.utilities.general import handle_error

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
    query = """
        SELECT * FROM items
        WHERE region = %s AND available = 1
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    """
    try:
        items = execute_query(query, (region, limit, skip))["data"]
        log_event("DATA_FETCH", f"Fetched {len(items)} market items for region: {region}")
        return items
    except Exception as e:
        log_exception(e, "Error fetching market items.")
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
    query = """
        INSERT INTO items (title, description, price, region, available)
        VALUES (%s, %s, %s, %s, 1)
    """
    try:
        execute_query(query, (title, description, price, region))
        log_event("DATA_INSERT", f"Added new market item: {title}")
        return {"message": "Item added successfully."}
    except Exception as e:
        log_exception(e, "Error adding market item.")
        raise

