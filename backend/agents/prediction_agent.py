"""
Prediction Agent - Combines weather and detection data for flood predictions
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import math

from models import AgentResponse

class PredictionAgent:
    """
    Prediction Agent responsible for:
    1. Combining weather and detection data
    2. Predicting water level rise
    3. Assessing road accessibility
    4. Determining urgency level
    5. Recommending specific actions
    """
    
    def __init__(self):
        self.name = "Prediction Agent"
    
    def _extract_data(self, agent_result: Dict, key: str) -> Dict:
        """
        Extract data from agent result, handling both wrapped and flat formats
        """
        # If it has 'data' wrapper, use that
        if isinstance(agent_result, dict) and 'data' in agent_result:
            return agent_result.get('data', {})
        
        # If it has 'additionalProp1' (Swagger artifact), handle it
        if isinstance(agent_result, dict) and 'additionalProp1' in agent_result:
            return {}
        
        # Otherwise, assume it's already the data
        return agent_result
    
    def _get_risk_level_from_score(self, score: float) -> str:
        """Convert risk score to level"""
        if score >= 75:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_severity_from_people(self, people: int) -> str:
        """Convert people count to severity level"""
        if people > 50:
            return "CRITICAL"
        elif people > 30:
            return "HIGH"
        elif people > 10:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def predict(self, weather_data: Dict, detection_data: Dict) -> AgentResponse:
        """
        Generate predictions based on weather and detection data
        """
        try:
            # Extract data from both formats
            weather_info = self._extract_data(weather_data, 'weather')
            detection_info = self._extract_data(detection_data, 'detection')
            
            # If weather_info is empty, try to extract from flat structure
            if not weather_info:
                if 'weather_risk' in weather_data:
                    weather_info = {
                        'risk_score': weather_data.get('weather_risk', 0),
                        'risk_level': self._get_risk_level_from_score(weather_data.get('weather_risk', 0)),
                        'current': {
                            'rainfall': weather_data.get('rainfall', 0),
                            'humidity': weather_data.get('humidity', 70)
                        }
                    }
                elif 'risk_score' in weather_data:
                    weather_info = weather_data
            
            # If detection_info is empty, try to extract from flat structure
            if not detection_info:
                if 'people' in detection_data:
                    people = detection_data.get('people', 0)
                    flood_percent = detection_data.get('flood_percentage', 0)
                    detection_info = {
                        'analysis': {
                            'people_detected': people,
                            'flood_area_percent': flood_percent,
                            'severity_level': self._get_severity_from_people(people)
                        }
                    }
                elif 'people_detected' in detection_data:
                    detection_info = {'analysis': detection_data}
            
            # Get detection analysis
            analysis = detection_info.get('analysis', {})
            people_detected = analysis.get('people_detected', 0)
            current_flood_area = analysis.get('flood_area_percent', 0)
            
            # Get weather data
            current_rainfall = weather_info.get('current', {}).get('rainfall', 0)
            weather_risk = weather_info.get('risk_score', 0)
            forecast = weather_info.get('forecast', [])
            
            # Calculate predictions
            water_rise_prediction = self._predict_water_rise(
                current_flood_area,
                current_rainfall,
                forecast
            )
            
            road_accessibility = self._assess_roads(
                current_flood_area,
                water_rise_prediction
            )
            
            urgency_level = self._calculate_urgency(
                people_detected,
                current_flood_area,
                weather_risk,
                water_rise_prediction
            )
            
            recommended_actions = self._generate_actions(
                urgency_level,
                people_detected,
                current_flood_area,
                water_rise_prediction,
                road_accessibility
            )
            
            overall_risk = self._calculate_overall_risk(
                people_detected,
                current_flood_area,
                weather_risk,
                water_rise_prediction
            )
            
            return AgentResponse(
                agent_name=self.name,
                status="success",
                data={
                    "predictions": {
                        "water_level_rise": water_rise_prediction,
                        "road_accessibility": road_accessibility,
                        "urgency_level": urgency_level,
                        "urgency_score": self._urgency_to_score(urgency_level),
                        "overall_risk_score": overall_risk
                    },
                    "recommended_actions": recommended_actions,
                    "risk_factors": self._get_risk_factors(
                        weather_info,
                        detection_info,
                        water_rise_prediction
                    ),
                    "timestamp": datetime.now().isoformat()
                },
                message=f"Prediction completed. Urgency: {urgency_level}"
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                status="error",
                data={},
                message=f"Error generating predictions: {str(e)}"
            )
    
    def _predict_water_rise(self, current_flood_area: float, 
                           current_rainfall: float, 
                           forecast: List[Dict]) -> Dict[str, Any]:
        """Predict water level rise over next 4-6 hours"""
        
        # Calculate expected rainfall in next 6 hours
        forecast_rain = sum(item.get("rain_mm", 0) for item in forecast[:2])
        
        # Base rise from current conditions
        base_rise = current_flood_area * 0.02
        
        # Additional rise from rainfall
        rain_rise = forecast_rain * 0.5
        
        # Total predicted rise
        predicted_rise = base_rise + rain_rise
        
        if predicted_rise > 30:
            level_category = "SEVERE FLOODING"
            description = "Water levels expected to rise significantly. Immediate evacuation required."
        elif predicted_rise > 20:
            level_category = "HIGH FLOODING"
            description = "Significant water rise expected. Prepare for evacuation."
        elif predicted_rise > 10:
            level_category = "MODERATE FLOODING"
            description = "Water levels rising. Monitor situation closely."
        else:
            level_category = "MILD FLOODING"
            description = "Minor water level increase expected."
        
        return {
            "current_rise_percent": round(current_flood_area, 1),
            "predicted_rise_percent": round(predicted_rise, 1),
            "rise_increase": round(predicted_rise - current_flood_area, 1),
            "category": level_category,
            "description": description,
            "forecast_rainfall_mm": round(forecast_rain, 1),
            "timeframe": "Next 4-6 hours"
        }
    
    def _assess_roads(self, current_flood_area: float, water_rise: Dict) -> Dict[str, Any]:
        """Assess road accessibility based on flood predictions"""
        
        predicted_rise = water_rise.get("predicted_rise_percent", 0)
        
        if predicted_rise > 30:
            score = 20
            status = "IMPASSABLE"
            description = "Major roads flooded. Only boat access possible."
        elif predicted_rise > 20:
            score = 40
            status = "SEVERE RESTRICTIONS"
            description = "Most roads flooded. Use high-clearance vehicles only."
        elif predicted_rise > 10:
            score = 60
            status = "PARTIAL ACCESS"
            description = "Some roads accessible. Avoid low-lying areas."
        else:
            score = 85
            status = "MOSTLY ACCESSIBLE"
            description = "Most roads accessible. Exercise caution in flood-prone areas."
        
        return {
            "accessibility_score": score,
            "status": status,
            "description": description,
            "recommended_vehicles": self._get_recommended_vehicles(status),
            "evacuation_routes_available": score > 50
        }
    
    def _get_recommended_vehicles(self, road_status: str) -> List[str]:
        """Get vehicle recommendations based on road conditions"""
        if road_status == "IMPASSABLE":
            return ["🚤 Boats", "🚁 Helicopters"]
        elif road_status == "SEVERE RESTRICTIONS":
            return ["🚛 High-clearance trucks", "🚤 Boats for deep water areas"]
        elif road_status == "PARTIAL ACCESS":
            return ["🚗 SUVs", "🚛 Utility vehicles"]
        else:
            return ["🚗 Standard vehicles", "🚑 Ambulances"]
    
    def _calculate_urgency(self, people: int, flood_area: float, 
                          weather_risk: float, water_rise: Dict) -> str:
        """Calculate urgency level based on multiple factors"""
        
        predicted_rise = water_rise.get("predicted_rise_percent", 0)
        
        score = 0
        
        # Factor 1: People at risk (0-40 points)
        if people > 50:
            score += 40
        elif people > 30:
            score += 30
        elif people > 15:
            score += 20
        elif people > 5:
            score += 10
        
        # Factor 2: Flood severity (0-30 points)
        score += min(flood_area * 0.3, 30)
        
        # Factor 3: Weather risk (0-20 points)
        score += min(weather_risk * 0.2, 20)
        
        # Factor 4: Water rise prediction (0-10 points)
        score += min(predicted_rise * 0.1, 10)
        
        # Determine urgency level
        if score >= 70:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _urgency_to_score(self, urgency: str) -> int:
        """Convert urgency level to numeric score"""
        mapping = {
            "CRITICAL": 90,
            "HIGH": 70,
            "MEDIUM": 50,
            "LOW": 30
        }
        return mapping.get(urgency, 50)
    
    def _generate_actions(self, urgency: str, people: int, 
                         flood_area: float, water_rise: Dict,
                         road_accessibility: Dict) -> List[str]:
        """Generate recommended actions based on predictions"""
        
        actions = []
        predicted_rise = water_rise.get("predicted_rise_percent", 0)
        
        if urgency == "CRITICAL":
            actions.append("🚨 IMMEDIATE: Full evacuation order required")
            actions.append("🚁 Deploy all available rescue helicopters")
            actions.append("🚤 Mobilize all boats for water rescue")
        elif urgency == "HIGH":
            actions.append("⚠️  Prepare evacuation plan")
            actions.append("🚑 Deploy medical teams to shelters")
            actions.append("📢 Issue public alert for 4-6 hour window")
        
        if people > 30:
            actions.append(f"👥 {people} people require rescue - prioritize high-density areas")
        
        if flood_area > 50:
            actions.append("🌊 Deploy flood barriers where possible")
        
        if predicted_rise > 20:
            actions.append("⬆️  Water rising - relocate equipment to higher ground")
        
        if not road_accessibility.get("evacuation_routes_available", True):
            actions.append("🛤️  Evacuation routes compromised - use alternative routes")
        
        actions.append("📡 Continue monitoring with drone surveillance")
        
        # Return top 5 most important actions
        return actions[:5]
    
    def _calculate_overall_risk(self, people: int, flood_area: float, 
                               weather_risk: float, water_rise: Dict) -> float:
        """Calculate overall risk score (0-100)"""
        
        predicted_rise = water_rise.get("predicted_rise_percent", 0)
        
        people_factor = min(people / 50, 1.0) * 30
        flood_factor = min(flood_area / 100, 1.0) * 30
        weather_factor = min(weather_risk / 100, 1.0) * 20
        rise_factor = min(predicted_rise / 50, 1.0) * 20
        
        overall = people_factor + flood_factor + weather_factor + rise_factor
        
        return round(min(overall, 100), 1)
    
    def _get_risk_factors(self, weather_info: Dict, detection_info: Dict, 
                         water_rise: Dict) -> List[str]:
        """List key risk factors"""
        
        factors = []
        
        rainfall = weather_info.get('current', {}).get('rainfall', 0)
        if rainfall > 5:
            factors.append(f"🌧️  Heavy rainfall ({rainfall}mm in last hour)")
        
        humidity = weather_info.get('current', {}).get('humidity', 0)
        if humidity > 80:
            factors.append(f"💧  High humidity ({humidity}%) - conducive to continued rain")
        
        people = detection_info.get('analysis', {}).get('people_detected', 0)
        if people > 20:
            factors.append(f"👥  High population density in affected area ({people} people)")
        
        flood_area = detection_info.get('analysis', {}).get('flood_area_percent', 0)
        if flood_area > 40:
            factors.append(f"🌊  Extensive flooding detected ({flood_area}% of area)")
        
        predicted_rise = water_rise.get('predicted_rise_percent', 0)
        if predicted_rise > 20:
            factors.append(f"⬆️  Water level predicted to rise by {predicted_rise}%")
        
        return factors

# Create singleton instance
prediction_agent = PredictionAgent()