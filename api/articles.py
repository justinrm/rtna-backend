from fastapi import APIRouter, HTTPException
from app.utilities.database import execute_query
from app.utilities.validation import sanitize_input

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/")
async def list_articles(skip: int = 0, limit: int = 10):
    """
    List recent articles, paginated.
    """
    query = f"SELECT * FROM articles ORDER BY published_at DESC LIMIT {limit} OFFSET {skip}"
    try:
        result = execute_query(query)
        return {"articles": result["data"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing articles: {str(e)}")

@router.get("/{article_id}")
async def get_article(article_id: int):
    """
    Retrieve a specific article by ID.
    """
    query = "SELECT * FROM articles WHERE id = %s"
    try:
        result = execute_query(query, (article_id,))
        if not result["data"]:
            raise HTTPException(status_code=404, detail="Article not found.")
        return {"article": result["data"][0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving article: {str(e)}")

@router.post("/")
async def add_article(title: str, content: str, url: str, source_id: int, published_at: str):
    """
    Add a new article to the database.
    """
    query = """
        INSERT INTO articles (title, content, url, source_id, published_at, fetched_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """
    try:
        execute_query(query, (sanitize_input(title), sanitize_input(content), sanitize_input(url), source_id, published_at))
        return {"message": "Article added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding article: {str(e)}")

