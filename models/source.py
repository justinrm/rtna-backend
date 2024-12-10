from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.utilities.database import Base
from datetime import datetime

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    website = Column(String, unique=True, nullable=False)
    latitude = Column(String)  # Lat/Long for location-based news aggregation
    longitude = Column(String)
    reliability_score = Column(Integer, default=0)
    discovered_by = Column(String, nullable=False)  # E.g., "Manual", "Crawler"
    discovery_timestamp = Column(DateTime, default=datetime.utcnow)
    last_validated = Column(DateTime, nullable=True)  # New field for validation tracking
    articles = relationship("Article", back_populates="source")

