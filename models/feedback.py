from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.utilities.database import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, nullable=False)  # ID of the related article or source
    feedback_type = Column(String, nullable=False)  # "like", "dislike", "flag", etc.
    user_id = Column(Integer, ForeignKey("users.id"))
    impact_score = Column(Integer, nullable=False, default=1)  # Adjusted to include default
    timestamp = Column(DateTime, default=datetime.utcnow)

