from sqlalchemy import Column, Integer, String, Text, DateTime
from app.utilities.database import Base
from datetime import datetime

class Alerts(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, nullable=False)  # Adjusted for localized region usage
    alert_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String, nullable=False)  # Includes the source of the alert (e.g., NWS or local agency)

