from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Item  # Assuming models are refactored into app/models
from app.utilities.database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["Items"])

class ItemCreate(BaseModel):
    title: str
    description: str

@router.get("/", response_model=list[ItemCreate])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List items with pagination.
    """
    return db.query(Item).offset(skip).limit(limit).all()

@router.post("/", response_model=ItemCreate)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Add a new item.
    """
    db_item = Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

