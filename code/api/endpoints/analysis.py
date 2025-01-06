from fastapi import APIRouter, HTTPException, Depends
from services.earthquake_service import EarthquakeService
from services.analysis_service import AnalysisService
from typing import Optional, List
from datetime import datetime
import os
from pydantic import BaseModel

router = APIRouter()
earthquake_service = EarthquakeService()
analysis_service = AnalysisService(api_key=os.getenv("ANTHROPIC_API_KEY"))

class AnalysisResponse(BaseModel):
    geographic_trends: List[str]
    magnitude_distribution: List[str]
    temporal_patterns: List[str]

@router.get("/earthquake-analysis", response_model=AnalysisResponse)
async def get_earthquake_analysis(days: int = 1, min_magnitude: float = 2.5, limit: int = 10):
    try:
        earthquakes = earthquake_service.get_earthquakes(days, min_magnitude)
        
        recent_earthquakes = sorted(
            earthquakes, 
            key=lambda x: datetime.fromisoformat(x['time']), 
            reverse=True
        )[:limit]
        
        analysis = analysis_service.analyze_earthquakes(recent_earthquakes)
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
