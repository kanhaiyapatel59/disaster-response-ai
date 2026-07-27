"""
Communication Agent - Generates reports, alerts, and messages from agent data
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

from models import AgentResponse

class CommunicationAgent:
    """
    Communication Agent responsible for:
    1. Generating official incident reports
    2. Creating SMS/email templates
    3. Formatting alerts for control room
    4. Synthesizing data from all agents
    """
    
    def __init__(self):
        self.name = "Communication Agent"
        self.incident_counter = 0
    
    async def generate_report(self, 
                             weather_data: Dict,
                             detection_data: Dict,
                             prediction_data: Dict,
                             resource_data: Dict,
                             incident_location: str = "Unknown",
                             include_timestamp: bool = True) -> AgentResponse:
        """
        Generate a comprehensive incident report
        
        Args:
            weather_data: Data from Weather Agent
            detection_data: Data from Detection Agent
            prediction_data: Data from Prediction Agent
            resource_data: Data from Resource Agent
            incident_location: Location of incident
            include_timestamp: Include timestamp in report
            
        Returns:
            AgentResponse with complete incident report
        """
        try:
            # Increment incident counter
            self.incident_counter += 1
            incident_id = f"DIS-{datetime.now().strftime('%Y%m%d')}-{str(self.incident_counter).zfill(4)}"
            
            # Extract key information
            weather_info = weather_data.get("data", {})
            detection_info = detection_data.get("data", {})
            prediction_info = prediction_data.get("data", {})
            resource_info = resource_data.get("data", {})
            
            # Generate report components
            executive_summary = self._generate_executive_summary(
                incident_location,
                weather_info,
                detection_info,
                prediction_info
            )
            
            situation_report = self._generate_situation_report(
                weather_info,
                detection_info,
                prediction_info,
                resource_info
            )
            
            resource_status = self._generate_resource_status(resource_info)
            
            recommended_actions = self._generate_action_summary(
                prediction_info,
                resource_info
            )
            
            # Prepare alert messages
            alerts = self._generate_alerts(
                incident_location,
                prediction_info,
                resource_info
            )
            
            # Generate the full report
            report = {
                "incident_id": incident_id,
                "title": f"Flood Incident Report - {incident_location}",
                "location": incident_location,
                "timestamp": datetime.now().isoformat(),
                "status": self._determine_incident_status(prediction_info),
                
                "executive_summary": executive_summary,
                "situation_report": situation_report,
                "resource_status": resource_status,
                "recommended_actions": recommended_actions,
                "alerts": alerts,
                
                "key_figures": self._extract_key_figures(
                    detection_info,
                    prediction_info,
                    resource_info
                ),
                
                "full_data": {
                    "weather": weather_info,
                    "detection": detection_info,
                    "prediction": prediction_info,
                    "resources": resource_info
                }
            }
            
            return AgentResponse(
                agent_name=self.name,
                status="success",
                data=report,
                message=f"Incident report {incident_id} generated successfully"
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                status="error",
                data={},
                message=f"Error generating report: {str(e)}"
            )
    
    def _generate_executive_summary(self, location: str, weather: Dict, 
                                   detection: Dict, prediction: Dict) -> str:
        """Generate executive summary for decision makers"""
        
        # Extract data
        risk_level = prediction.get("predictions", {}).get("urgency_level", "Unknown")
        people = detection.get("analysis", {}).get("people_detected", 0)
        water_rise = prediction.get("predictions", {}).get("water_level_rise", {})
        flood_category = water_rise.get("category", "Unknown")
        
        # Build summary
        summary_parts = [
            f"🔴 INCIDENT STATUS: {risk_level}",
            f"📍 Location: {location}",
            f"👥 People Affected: {people} detected",
            f"🌊 Flood Status: {flood_category}",
        ]
        
        if risk_level in ["CRITICAL", "HIGH"]:
            summary_parts.append("⚠️  IMMEDIATE ACTION REQUIRED")
            summary_parts.append("🚨 Full evacuation and rescue deployment recommended")
        
        return "\n".join(summary_parts)
    
    def _generate_situation_report(self, weather: Dict, detection: Dict,
                                  prediction: Dict, resources: Dict) -> str:
        """Generate detailed situation report"""
        
        sections = []
        
        # Weather section
        current_weather = weather.get("current", {})
        weather_text = f"""
🌤️ CURRENT WEATHER:
- Temperature: {current_weather.get('temperature', 'N/A')}°C
- Conditions: {current_weather.get('condition', 'Unknown')}
- Rainfall: {current_weather.get('rainfall', 0)}mm (last hour)
- Humidity: {current_weather.get('humidity', 0)}%
- Wind Speed: {current_weather.get('wind_speed', 0)} km/h
- Risk Level: {weather.get('risk_level', 'Unknown')}
"""
        sections.append(weather_text)
        
        # Detection section
        analysis = detection.get("analysis", {})
        detection_text = f"""
📸 DRONE/CCTV ANALYSIS:
- People Detected: {analysis.get('people_detected', 0)}
- Flood Area: {analysis.get('flood_area_percent', 0)}% of surveyed area
- Water Level: {analysis.get('water_level', 'Unknown')}
- Severity: {analysis.get('severity_level', 'Unknown')}
"""
        sections.append(detection_text)
        
        # Prediction section
        predictions = prediction.get("predictions", {})
        water_rise = predictions.get("water_level_rise", {})
        roads = predictions.get("road_accessibility", {})
        prediction_text = f"""
🔮 PREDICTIONS:
- Water Level Rise: {water_rise.get('predicted_rise_percent', 0)}% (Current: {water_rise.get('current_rise_percent', 0)}%)
- Flood Category: {water_rise.get('category', 'Unknown')}
- Road Accessibility: {roads.get('status', 'Unknown')} ({roads.get('accessibility_score', 0)}%)
- Urgency Level: {predictions.get('urgency_level', 'Unknown')}
"""
        sections.append(prediction_text)
        
        # Resource section
        resource_allocation = resources.get("resource_allocation", {})
        resource_text = f"""
🏥 RESOURCE STATUS:
- Shelter Capacity Allocated: {resource_allocation.get('shelter_capacity_allocated', 0)} spaces
- Medical Beds Allocated: {resource_allocation.get('medical_resources', {}).get('beds_allocated', 0)}
- Teams Dispatched: {resource_allocation.get('total_teams_dispatched', 0)}
- Resource Sufficiency: {resource_allocation.get('resource_sufficiency', 'Unknown')}
"""
        sections.append(resource_text)
        
        return "\n".join(sections)
    
    def _generate_resource_status(self, resource_data: Dict) -> str:
        """Generate resource status summary"""
        
        resource_summary = resource_data.get("resource_summary", {})
        allocation = resource_data.get("resource_allocation", {})
        
        status_parts = [
            "📊 RESOURCE STATUS SUMMARY",
            "-" * 30,
            "",
            "🏠 SHELTERS:",
            f"  Total Open: {resource_summary.get('shelters', {}).get('open', 0)}",
            f"  Available Spaces: {resource_summary.get('shelters', {}).get('available_spaces', 0)}",
            f"  Occupancy Rate: {resource_summary.get('shelters', {}).get('occupancy_rate', 0)}%",
            "",
            "🏥 MEDICAL:",
            f"  Available Beds: {resource_summary.get('hospitals', {}).get('available_beds', 0)}",
            f"  Total Ambulances: {resource_summary.get('hospitals', {}).get('total_ambulances', 0)}",
            "",
            "🚑 RESCUE TEAMS:",
            f"  Teams Available: {resource_summary.get('rescue_teams', {}).get('available', 0)}",
            f"  Total Boats: {resource_summary.get('rescue_teams', {}).get('total_boats', 0)}",
            "",
            f"✅ Resource Sufficiency: {allocation.get('resource_sufficiency', 'UNKNOWN')}"
        ]
        
        return "\n".join(status_parts)
    
    def _generate_action_summary(self, prediction: Dict, resources: Dict) -> List[str]:
        """Generate summary of recommended actions"""
        
        actions = []
        
        # Get actions from prediction
        pred_actions = prediction.get("recommended_actions", [])
        if pred_actions:
            actions.extend(pred_actions[:3])  # Top 3 actions
        
        # Add resource-based actions
        allocation = resources.get("resource_allocation", {})
        if allocation.get("resource_sufficiency") == "INADEQUATE":
            actions.append("⚠️  Resource shortage detected - request additional resources")
        
        gaps = resources.get("resource_gaps", [])
        for gap in gaps[:2]:  # Top 2 gaps
            actions.append(f"🔧 Address gap: {gap}")
        
        # Add always-recommended actions
        actions.append("📡 Continue monitoring and updating situation assessment")
        actions.append("🔄 Coordinate with state disaster management authority")
        
        # Remove duplicates and limit
        seen = set()
        unique_actions = []
        for action in actions:
            if action not in seen:
                seen.add(action)
                unique_actions.append(action)
        
        return unique_actions[:7]  # Return top 7 actions
    
    def _generate_alerts(self, location: str, prediction: Dict, 
                        resources: Dict) -> Dict[str, Any]:
        """Generate alert messages for different channels"""
        
        urgency = prediction.get("predictions", {}).get("urgency_level", "MEDIUM")
        people = prediction.get("people_affected", 0)
        
        # Control room alert
        control_room_alert = f"""
🚨 CONTROL ROOM ALERT
📍 Location: {location}
⚠️  Urgency: {urgency}
📋 Action Required: Immediate Deployment

Based on AI analysis, {people} people have been detected in flood-affected areas.
{self._get_urgency_message(urgency)}

Resources Status: {resources.get('resource_allocation', {}).get('resource_sufficiency', 'Unknown')}

Please activate emergency response protocol for {urgency} level incidents.
"""
        
        # SMS alert for responders
        sms_alert = f"""
🚨 FLOOD RESPONSE ALERT
Location: {location}
Urgency: {urgency}
People Affected: {people}
Deploy rescue teams immediately. Response code: {urgency}
"""
        
        # Email template for situation report
        email_template = f"""
Subject: URGENT: Flood Incident Report - {location}

Dear Disaster Management Team,

This is an automated alert from the AI Disaster Command Center.

INCIDENT DETAILS:
- Location: {location}
- Urgency Level: {urgency}
- People Affected: {people}
- Incident ID: DIS-{datetime.now().strftime('%Y%m%d')}-001

SITUATION SUMMARY:
{self._generate_executive_summary(location, {}, {}, prediction)}

RECOMMENDED ACTIONS:
{self._generate_action_summary(prediction, resources)}

Please review the full incident report for detailed information.

This is an AI-generated alert. Please verify all information with ground teams.

Regards,
AI Disaster Command Center
"""
        
        return {
            "control_room": control_room_alert,
            "sms": sms_alert,
            "email": email_template,
            "priority": "HIGH" if urgency in ["CRITICAL", "HIGH"] else "NORMAL"
        }
    
    def _get_urgency_message(self, urgency: str) -> str:
        """Get urgency-specific message"""
        messages = {
            "CRITICAL": "This is a CRITICAL situation. Immediate evacuation and rescue required.",
            "HIGH": "This is a HIGH risk situation. Deploy all available resources.",
            "MEDIUM": "This is a MEDIUM risk situation. Monitor and prepare for deployment.",
            "LOW": "This is a LOW risk situation. Continue monitoring."
        }
        return messages.get(urgency, "Monitor situation closely.")
    
    def _determine_incident_status(self, prediction: Dict) -> str:
        """Determine overall incident status"""
        urgency = prediction.get("predictions", {}).get("urgency_level", "MEDIUM")
        status_map = {
            "CRITICAL": "ACTIVE - CRITICAL",
            "HIGH": "ACTIVE - HIGH PRIORITY",
            "MEDIUM": "ACTIVE - MONITORING",
            "LOW": "MONITORING"
        }
        return status_map.get(urgency, "UNDER ASSESSMENT")
    
    def _extract_key_figures(self, detection: Dict, prediction: Dict, 
                           resources: Dict) -> Dict[str, Any]:
        """Extract key metrics for dashboard display"""
        
        return {
            "people_affected": detection.get("analysis", {}).get("people_detected", 0),
            "flood_area": detection.get("analysis", {}).get("flood_area_percent", 0),
            "urgency_score": prediction.get("predictions", {}).get("urgency_score", 0),
            "resource_sufficiency": resources.get("resource_allocation", {}).get("resource_sufficiency", "UNKNOWN"),
            "teams_deployed": resources.get("resource_allocation", {}).get("total_teams_dispatched", 0),
            "shelter_capacity": resources.get("resource_allocation", {}).get("shelter_capacity_allocated", 0),
            "incident_status": self._determine_incident_status(prediction)
        }

# Create singleton instance
communication_agent = CommunicationAgent()