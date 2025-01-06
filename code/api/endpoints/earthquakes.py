from fastapi import APIRouter, HTTPException
from services.earthquake_service import EarthquakeService
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
earthquake_service = EarthquakeService()

class Earthquake(BaseModel):
    id: str
    location: str
    magnitude: float
    time: str  # ISO format timestamp

@router.get("/earthquakes", response_model=List[Earthquake])
async def get_earthquakes(days: int = 2, min_magnitude: float = 2.5):
    try:
        earthquakes = earthquake_service.get_earthquakes(days, min_magnitude)
        return earthquakes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
