from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.utilities.database import Base
from datetime import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    published_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    source = relationship("Source", back_populates="articles")
    keywords = Column(String, nullable=True)  # Added for SEO and search functionality

