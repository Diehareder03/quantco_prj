from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base
from datetime import datetime

class Venues(Base):  
    __tablename__ = "venues"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # ✅ Fixed Relationship to Weather
    weather_data = relationship("Weather", back_populates="venue")

# ✅ Fixed Weather Table
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    venues_id = Column(Integer, ForeignKey("venues.id"), nullable=False)  # ✅ Fixed ForeignKey
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    dewpoint = Column(Float, nullable=True)
    apparent_temp = Column(Float, nullable=True)
    precipitation_prob = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    rain = Column(Float, nullable=True)
    showers = Column(Float, nullable=True)
    snowfall = Column(Float, nullable=True)
    snow_depth = Column(Float, nullable=True)

    # ✅ Fixed Relationship (Was "venues", should be "Venues")
    venue = relationship("Venues", back_populates="weather_data")
