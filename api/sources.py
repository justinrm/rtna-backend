from fastapi import APIRouter, HTTPException
from app.utilities.database import execute_query
from app.utilities.validation import is_valid_url, sanitize_input

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.get("/")
async def list_sources():
    """
    List all active sources, ordered by reliability score.
    """
    query = "SELECT * FROM news_sources WHERE status = 'active' ORDER BY reliability_score DESC"
    try:
        result = execute_query(query)
        return {"sources": result["data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing sources: {str(e)}")

@router.post("/")
async def add_source(name: str, website: str):
    """
    Add a new news source.
    """
    if not is_valid_url(website):
        raise HTTPException(status_code=400, detail="Invalid website URL.")

    query = """
        INSERT INTO news_sources (name, website, status, reliability_score, discovered_by, discovery_timestamp)
        VALUES (%s, %s, 'pending', 0, 'Manual', NOW())
    """
    try:
        execute_query(query, (
            sanitize_input(name),
            sanitize_input(website)
        ))
        return {"message": "Source added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding source: {str(e)}")

