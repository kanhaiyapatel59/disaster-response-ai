"""
Weather Agent - Provides weather data and flood risk assessment
"""
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

from tools.weather_tool import WeatherTool
from models import AgentResponse

class WeatherAgent:
    """
    Weather Agent responsible for:
    1. Fetching current weather for a location
    2. Predicting rainfall for next 4-6 hours
    3. Calculating flood risk score
    """
    
    def __init__(self):
        self.name = "Weather Agent"
        self.weather_tool = WeatherTool()
        self.cache = {}  # Simple cache to reduce API calls
    
    async def analyze(self, location: str, use_cache: bool = True) -> AgentResponse:
        """
        Analyze weather for a given location
        
        Args:
            location: City/region name
            use_cache: Use cached data if available
            
        Returns:
            AgentResponse with weather data
        """
        try:
            # Check cache first (5 minute TTL)
            cache_key = location.lower()
            if use_cache and cache_key in self.cache:
                cached_data = self.cache[cache_key]
                cache_age = (datetime.now() - cached_data["timestamp"]).seconds
                if cache_age < 300:  # 5 minutes
                    return AgentResponse(
                        agent_name=self.name,
                        status="success",
                        data=cached_data["data"],
                        message="Weather data retrieved from cache"
                    )
            
            # Fetch fresh weather data
            weather_data = await self.weather_tool.get_current_weather(location)
            
            # Update cache
            self.cache[cache_key] = {
                "data": weather_data,
                "timestamp": datetime.now()
            }
            
            return AgentResponse(
                agent_name=self.name,
                status="success",
                data=weather_data,
                message=f"Weather analysis completed for {location}"
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                status="error",
                data={},
                message=f"Error analyzing weather: {str(e)}"
            )
    
    def get_risk_summary(self, weather_data: Dict) -> Dict[str, Any]:
        """
        Extract key risk information from weather data
        """
        return {
            "risk_level": weather_data.get("risk_level", "UNKNOWN"),
            "risk_score": weather_data.get("risk_score", 0),
            "conditions": {
                "rainfall": weather_data.get("current", {}).get("rainfall", 0),
                "humidity": weather_data.get("current", {}).get("humidity", 0)
            },
            "forecast": weather_data.get("forecast", [])[:2]  # Next 4-6 hours
        }

# Create singleton instance
weather_agent = WeatherAgent()