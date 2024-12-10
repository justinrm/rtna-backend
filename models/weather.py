from sqlalchemy import Column, Integer, String, Float, DateTime
from app.utilities.database import Base
from datetime import datetime

class Weather(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)  # Adjusted for city-specific records
    temperature = Column(Float, nullable=False)
    condition = Column(String, nullable=False)  # e.g., Sunny, Cloudy
    wind_speed = Column(Float, nullable=True)  # Added for richer weather data
    humidity = Column(Float, nullable=True)  # Added for localized weather metrics
    timestamp = Column(DateTime, default=datetime.utcnow)

