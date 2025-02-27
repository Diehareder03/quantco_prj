from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# ✅ Venue Schema
class VenueBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class VenueCreate(VenueBase):
    pass

class VenueResponse(VenueBase):
    id: int

    class Config:
        from_attributes = True

# ✅ Weather Schema
class WeatherBase(BaseModel):
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    dewpoint: Optional[float] = None
    apparent_temp: Optional[float] = None
    precipitation_prob: Optional[float] = None
    precipitation: Optional[float] = None
    rain: Optional[float] = None
    showers: Optional[float] = None
    snowfall: Optional[float] = None
    snow_depth: Optional[float] = None

class WeatherCreate(WeatherBase):
    venues_id: int

class WeatherResponse(WeatherBase):
    id: int
    venues_id: int

    class Config:
        from_attributes = True

# ✅ Fixed Request Schema for Fetching Weather
class WeatherRequest(BaseModel):
    venues_id: int
    start_date: date  # Changed to date since it's not a datetime
    end_date: date    # Changed to date
