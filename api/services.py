import requests
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Open-Meteo API Base URL
WEATHER_API_URL = "https://archive-api.open-meteo.com/v1/archive"

def fetch_weather_data(venues: models.Venues, start_date: datetime, end_date: datetime):
    """Fetch weather data from Open-Meteo API."""
    params = {
        "latitude": venues.latitude,
        "longitude": venues.longitude,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": ",".join([
            "temperature_2m", "relative_humidity_2m", "dewpoint_2m",
            "apparent_temperature", "precipitation_probability",
            "precipitation", "rain", "showers", "snowfall", "snow_depth"
        ])
    }
    
    logger.info(f"Fetching weather data: {params}")
    response = requests.get(WEATHER_API_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to fetch weather data: {response.status_code}, {response.text}")
        return None

def save_weather_data(db: Session, venues_id: int, weather_data: dict):
    """Process and save weather data into the database."""
    hourly_data = weather_data.get("hourly", {})
    timestamps = hourly_data.get("time", [])

    if not timestamps:
        logger.warning("No weather data available to save.")
        return None
    
    saved_entries = []
    for i, timestamp in enumerate(timestamps):
        weather_entry = models.Weather(
            venues_id=venues_id,
            timestamp=datetime.fromisoformat(timestamp),
            temperature=hourly_data.get("temperature_2m", [None])[i],
            humidity=hourly_data.get("relative_humidity_2m", [None])[i],
            dewpoint=hourly_data.get("dewpoint_2m", [None])[i],
            apparent_temp=hourly_data.get("apparent_temperature", [None])[i],
            precipitation_prob=hourly_data.get("precipitation_probability", [None])[i],
            precipitation=hourly_data.get("precipitation", [None])[i],
            rain=hourly_data.get("rain", [None])[i],
            showers=hourly_data.get("showers", [None])[i],
            snowfall=hourly_data.get("snowfall", [None])[i],
            snow_depth=hourly_data.get("snow_depth", [None])[i]
        )
        db.add(weather_entry)
        saved_entries.append(weather_entry)

    db.commit()
    logger.info(f"Successfully saved {len(saved_entries)} weather entries.")
    
    return saved_entries[-1] if saved_entries else None
