import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

class EarthquakeService:
    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def get_earthquakes(self, days: int = 2, min_magnitude: float = 2.5) -> List[Dict[str, Any]]:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        params = {
            'format': 'geojson',
            'starttime': start_date.strftime('%Y-%m-%d'),
            'endtime': end_date.strftime('%Y-%m-%d'),
            'minmagnitude': str(min_magnitude),
            'limit': 100 
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            transformed_data = []
            for feature in data['features']:
                timestamp_ms = feature['properties']['time']
                time_iso = datetime.fromtimestamp(timestamp_ms / 1000.0).isoformat()
                
                transformed_data.append({
                    'id': feature['id'],
                    'location': feature['properties']['place'],
                    'magnitude': feature['properties']['mag'],
                    'time': time_iso
                })
            
            return transformed_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching earthquake data: {str(e)}")
