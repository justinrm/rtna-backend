from sqlalchemy import Column, Integer, String, Text
from app.utilities.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    price = Column(Integer, default=0)
    region = Column(String, nullable=True)  # Added for location-based item filtering
    available = Column(Integer, default=1)  # 1 for available, 0 for unavailable

