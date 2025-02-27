from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List  # ✅ Import List for compatibility
from api import schemas, models, database

router = APIRouter(prefix="/venues", tags=["Venues"])  # ✅ Added prefix

# ✅ Get all venues
@router.get("/", response_model=List[schemas.VenueResponse])  # ✅ Fixed type hint
def get_venues(db: Session = Depends(database.get_db)):
    return db.query(models.Venues).all()

# ✅ Get weather for a specific venue
@router.get("/{venue_id}/weather", response_model=List[schemas.WeatherResponse])  # ✅ Fixed type hint
def get_weather(venue_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Weather).filter(models.Weather.venues_id == venue_id).all()
