from anthropic import Anthropic
from typing import Dict, Any, List
from datetime import datetime
import json

class AnalysisService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError("Anthropic API key required")
            
        try:
            self.client = Anthropic(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Anthropic client: {str(e)}")
        
        
    def analyze_earthquakes(self, earthquakes: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not self.client:
            return {"error": "Anthropic client not initialized"}
    
        earthquake_text = "\n".join([
            f"Location: {eq['location']}, Magnitude: {eq['magnitude']}, Time: {eq['time']}"
            for eq in earthquakes
        ])
        
        prompt = f"""Analyze the following earthquake data:

{earthquake_text}

Analyze the text for: Give four sentences description for each category:
- Geographic Trend Clustering
- Magnitude Distribution
- Temporal Patterns

Return the data in the following JSON format:
{{
    "geographic_trends": ["sentence1", "sentence2", "sentence3", "sentence4"],
    "magnitude_distribution": ["sentence1", "sentence2", "sentence3", "sentence4"],
    "temporal_patterns": ["sentence1", "sentence2", "sentence3", "sentence4"]
}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis_text = response.content[0].text
            try:
                return json.loads(analysis_text)
            except json.JSONDecodeError:
                return {
                    "error": "Failed to parse",
                    "raw_response": analysis_text
                }
                
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}"
            }
