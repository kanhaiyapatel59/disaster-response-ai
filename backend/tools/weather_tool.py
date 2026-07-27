"""
Weather Tool - Fetches real-time weather data from OpenWeatherMap API
"""
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json

from config import config

class WeatherTool:
    """Tool for fetching weather data with flood risk assessment"""
    
    def __init__(self):
        self.api_key = config.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.use_simulation = not bool(self.api_key)
        
        if self.use_simulation:
            print("⚠️  Weather Agent: No API key found. Using simulation mode.")
    
    async def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Fetch current weather for a location
        
        Args:
            location: City name (e.g., "Mumbai", "Kerala")
            
        Returns:
            Dict with weather data and flood risk assessment
        """
        if self.use_simulation:
            return self._simulate_weather(location)
        
        try:
            # First, geocode location to get coordinates
            geo_url = "http://api.openweathermap.org/geo/1.0/direct"
            geo_params = {
                "q": location,
                "limit": 1,
                "appid": self.api_key
            }
            
            async with httpx.AsyncClient() as client:
                # Get coordinates
                geo_response = await client.get(geo_url, params=geo_params)
                geo_response.raise_for_status()
                geo_data = geo_response.json()
                
                if not geo_data:
                    return self._simulate_weather(location)
                
                lat = geo_data[0]["lat"]
                lon = geo_data[0]["lon"]
                
                # Get weather data
                weather_url = f"{self.base_url}/weather"
                weather_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric"  # Celsius
                }
                
                weather_response = await client.get(weather_url, params=weather_params)
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                
                # Get forecast for rainfall prediction
                forecast_url = f"{self.base_url}/forecast"
                forecast_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": 8  # 8 * 3-hour = 24 hours
                }
                
                forecast_response = await client.get(forecast_url, params=forecast_params)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()
                
                # Process and combine data
                return self._process_weather_data(weather_data, forecast_data, location)
                
        except Exception as e:
            print(f"⚠️  Weather API error: {e}. Using simulation.")
            return self._simulate_weather(location)
    
    def _process_weather_data(self, weather: Dict, forecast: Dict, location: str) -> Dict[str, Any]:
        """Process raw API data into our format"""
        
        # Current conditions
        current = {
            "temperature": weather["main"]["temp"],
            "feels_like": weather["main"]["feels_like"],
            "humidity": weather["main"]["humidity"],
            "pressure": weather["main"]["pressure"],
            "condition": weather["weather"][0]["description"],
            "wind_speed": weather["wind"]["speed"],
            "rainfall": weather.get("rain", {}).get("1h", 0),  # Rain in last hour
            "clouds": weather["clouds"]["all"]
        }
        
        # Get rainfall prediction for next 4-6 hours
        rainfall_predictions = []
        current_time = datetime.now()
        
        for item in forecast["list"][:4]:  # Next 12 hours
            forecast_time = datetime.fromtimestamp(item["dt"])
            rain = item.get("rain", {}).get("3h", 0)
            rainfall_predictions.append({
                "time": forecast_time.strftime("%H:%M"),
                "rain_mm": rain,
                "condition": item["weather"][0]["description"]
            })
        
        # Calculate flood risk score (0-100)
        risk_score = self._calculate_flood_risk(current, rainfall_predictions)
        
        return {
            "location": location,
            "current": current,
            "forecast": rainfall_predictions,
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_flood_risk(self, current: Dict, forecast: List) -> float:
        """Calculate flood risk score based on multiple factors"""
        score = 0
        
        # Factor 1: Current rainfall (0-30 points)
        if current["rainfall"] > 0:
            score += min(current["rainfall"] * 10, 30)
        
        # Factor 2: Humidity (0-20 points)
        if current["humidity"] > 70:
            score += (current["humidity"] - 70) * 0.67
        score = min(score, 20)
        
        # Factor 3: Pressure trend (0-20 points)
        if current["pressure"] < 1000:  # Low pressure = more rain
            score += 20
        elif current["pressure"] < 1010:
            score += 10
        
        # Factor 4: Forecasted rain next 6 hours (0-30 points)
        total_forecast_rain = sum(item["rain_mm"] for item in forecast[:2])  # Next 6 hours
        if total_forecast_rain > 0:
            score += min(total_forecast_rain * 5, 30)
        
        return min(score, 100)
    
    def _get_risk_level(self, score: float) -> str:
        """Convert numeric score to risk level"""
        if score >= 75:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _simulate_weather(self, location: str) -> Dict[str, Any]:
        """Generate realistic simulated weather data for demos"""
        import random
        
        # Simulate different weather patterns based on location
        coastal_cities = ["Mumbai", "Chennai", "Kolkata", "Kochi"]
        is_coastal = any(city in location for city in coastal_cities)
        
        if is_coastal:
            # Tropical coastal weather
            rainfall = random.uniform(2, 15)
            humidity = random.randint(75, 95)
            temp = random.uniform(25, 35)
            condition = random.choice(["heavy rain", "moderate rain", "thunderstorm", "light rain"])
        else:
            # Inland weather
            rainfall = random.uniform(0, 8)
            humidity = random.randint(50, 80)
            temp = random.uniform(20, 30)
            condition = random.choice(["clear", "partly cloudy", "light rain", "overcast"])
        
        # Generate forecast
        forecast = []
        current_hour = datetime.now().hour
        for i in range(4):
            forecast_hour = (current_hour + i + 2) % 24
            forecast.append({
                "time": f"{forecast_hour:02d}:00",
                "rain_mm": rainfall * random.uniform(0.5, 1.5),
                "condition": random.choice(["rain", "cloudy", "clear"])
            })
        
        risk_score = self._calculate_flood_risk({
            "rainfall": rainfall,
            "humidity": humidity,
            "pressure": random.randint(990, 1020)
        }, forecast)
        
        return {
            "location": location,
            "current": {
                "temperature": temp,
                "feels_like": temp - 1,
                "humidity": humidity,
                "pressure": random.randint(990, 1020),
                "condition": condition,
                "wind_speed": random.uniform(0, 20),
                "rainfall": rainfall,
                "clouds": random.randint(20, 100)
            },
            "forecast": forecast,
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "timestamp": datetime.now().isoformat(),
            "simulated": True
        }