from fastapi import APIRouter, HTTPException, Query
from app.modules.market_data import fetch_market_items, add_market_item
from app.utilities.validation import sanitize_input

router = APIRouter(prefix="/market", tags=["Market Data"])

@router.get("/")
async def list_market_items(skip: int = Query(default=0), limit: int = Query(default=10), region: str = Query(default="Lewiston")):
    """
    List market items for a specific region, paginated.
    """
    try:
        items = fetch_market_items(skip=skip, limit=limit, region=region)
        return {"region": region, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def add_market_item(title: str, description: str, price: int, region: str = "Lewiston"):
    """
    Add a new market item.
    """
    try:
        sanitized_title = sanitize_input(title)
        sanitized_description = sanitize_input(description)
        result = add_market_item(sanitized_title, sanitized_description, price, region)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

