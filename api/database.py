from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL (Update with your actual credentials)
# DATABASE_URL = "postgresql://postgres:1475369@localhost:5432/weather_db"
# DATABASE_URL = "postgresql://postgres:your_password@127.0.0.1:5432/weather_db"
DATABASE_URL = "postgresql://postgres:1475369@127.0.0.1:5432/weather_db"



# SQLAlchemy Engine & Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Models
Base = declarative_base()

# Dependency to get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
