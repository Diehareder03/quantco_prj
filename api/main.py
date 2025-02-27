from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Venues, Weather  # Ensure Weather model is imported
from api.schemas import WeatherRequest, WeatherResponse
from api.services import fetch_weather_data, save_weather_data
from api.routers import venues  
import logging

# Define FastAPI instance
app = FastAPI(title="Weather Data API", version="1.0")

# Include the venues router
app.include_router(venues.router, prefix="/api")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/fetch-weather/", response_model=WeatherResponse)
def fetch_and_store_weather(request: WeatherRequest, db: Session = Depends(get_db)):
    """Fetch and store weather data for a venue."""
    logger.info(f"Fetching weather for Venue ID: {request.venues_id}")
    
    venue = db.query(Venues).filter(Venues.id == request.venues_id).first()
    if not venue:
        logger.error("Venue not found!")
        raise HTTPException(status_code=404, detail="Venue not found")
    
    weather_data = fetch_weather_data(venue, request.start_date, request.end_date)
    if not weather_data:
        logger.error("Failed to fetch weather data")
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")
    
    saved_weather = save_weather_data(db, request.venues_id, weather_data)
    
    if not saved_weather:
        logger.error("Failed to save weather data!")
        raise HTTPException(status_code=500, detail="Failed to save weather data to the database.")
    
    logger.info("Weather data saved successfully!")
    
    return WeatherResponse(
        id=saved_weather.id,
        venues_id=saved_weather.venues_id,
        timestamp=saved_weather.timestamp,
        temperature=saved_weather.temperature,
        humidity=saved_weather.humidity,
        dewpoint=saved_weather.dewpoint,
        apparent_temp=saved_weather.apparent_temp,
        precipitation_prob=saved_weather.precipitation_prob,
        precipitation=saved_weather.precipitation,
        rain=saved_weather.rain,
        showers=saved_weather.showers,
        snowfall=saved_weather.snowfall,
        snow_depth=saved_weather.snow_depth
    )
