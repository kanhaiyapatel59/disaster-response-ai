"""
Test script for Communication Agent
"""
import asyncio
import json
from datetime import datetime
from agents.communication_agent import communication_agent

async def test_communication():
    """Test the Communication Agent"""
    
    print("📢 Testing Communication Agent...")
    print("-" * 60)
    
    # Sample data from all agents
    weather_data = {
        "data": {
            "location": "Mumbai",
            "risk_score": 65,
            "risk_level": "HIGH",
            "current": {
                "temperature": 28.5,
                "condition": "moderate rain",
                "rainfall": 8.5,
                "humidity": 92,
                "wind_speed": 12.5,
                "pressure": 1005
            },
            "forecast": [
                {"time": "14:00", "rain_mm": 5.2},
                {"time": "17:00", "rain_mm": 3.8}
            ]
        }
    }
    
    detection_data = {
        "data": {
            "analysis": {
                "people_detected": 35,
                "flood_area_percent": 65.5,
                "water_level": "SEVERE (> 2 meters)",
                "severity_score": 72.3,
                "severity_level": "HIGH"
            }
        }
    }
    
    prediction_data = {
        "data": {
            "predictions": {
                "water_level_rise": {
                    "current_rise_percent": 65.5,
                    "predicted_rise_percent": 78.3,
                    "category": "SEVERE FLOODING",
                    "description": "Water levels expected to rise significantly.",
                    "timeframe": "Next 4-6 hours"
                },
                "road_accessibility": {
                    "accessibility_score": 40,
                    "status": "SEVERE RESTRICTIONS",
                    "evacuation_routes_available": False,
                    "recommended_vehicles": ["Boats", "Helicopters"]
                },
                "urgency_level": "CRITICAL",
                "urgency_score": 90,
                "overall_risk_score": 85.6
            },
            "recommended_actions": [
                "🚨 IMMEDIATE: Full evacuation order required",
                "🚁 Deploy all available rescue helicopters",
                "🚤 Mobilize all boats for water rescue"
            ]
        }
    }
    
    resource_data = {
        "data": {
            "resource_summary": {
                "shelters": {
                    "total": 5,
                    "open": 4,
                    "total_capacity": 2250,
                    "available_spaces": 1100,
                    "occupancy_rate": 51.1
                },
                "hospitals": {
                    "total": 3,
                    "total_beds": 450,
                    "available_beds": 80,
                    "bed_availability_rate": 17.8,
                    "total_ambulances": 20
                },
                "rescue_teams": {
                    "total": 4,
                    "available": 3,
                    "total_boats": 9,
                    "availability_rate": 75.0
                }
            },
            "resource_allocation": {
                "shelter_capacity_allocated": 150,
                "medical_resources": {
                    "beds_needed": 20,
                    "beds_allocated": 12,
                    "icu_beds_needed": 5,
                    "icu_beds_allocated": 3
                },
                "total_teams_dispatched": 2,
                "resource_sufficiency": "PARTIAL"
            },
            "resource_gaps": [
                "🏥 Medical bed shortage: Need 20 beds, only 12 available nearby"
            ]
        }
    }
    
    # Generate report
    print("📝 Generating incident report...\n")
    
    result = await communication_agent.generate_report(
        weather_data=weather_data,
        detection_data=detection_data,
        prediction_data=prediction_data,
        resource_data=resource_data,
        incident_location="Mumbai Flood Zone"
    )
    
    if result.status == "success":
        report = result.data
        
        print("=" * 60)
        print(f"📋 INCIDENT REPORT: {report.get('incident_id')}")
        print("=" * 60)
        
        print(f"\n📌 {report.get('title')}")
        print(f"📍 Location: {report.get('location')}")
        print(f"⏰ Timestamp: {report.get('timestamp')}")
        print(f"📊 Status: {report.get('status')}")
        
        print("\n" + "=" * 60)
        print("📝 EXECUTIVE SUMMARY")
        print("=" * 60)
        print(report.get('executive_summary', 'N/A'))
        
        print("\n" + "=" * 60)
        print("📊 KEY FIGURES")
        print("=" * 60)
        for key, value in report.get('key_figures', {}).items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print("\n" + "=" * 60)
        print("✅ RECOMMENDED ACTIONS")
        print("=" * 60)
        for i, action in enumerate(report.get('recommended_actions', []), 1):
            print(f"   {i}. {action}")
        
        print("\n" + "=" * 60)
        print("📢 ALERTS")
        print("=" * 60)
        
        alerts = report.get('alerts', {})
        print("\n🚨 CONTROL ROOM ALERT:")
        print("-" * 40)
        print(alerts.get('control_room', 'N/A')[:200] + "...")
        
        print("\n📱 SMS ALERT:")
        print("-" * 40)
        print(alerts.get('sms', 'N/A'))
        
        print("\n" + "=" * 60)
        print(f"✅ Report generation complete! (ID: {report.get('incident_id')})")
        
    else:
        print(f"❌ Error: {result.message}")

if __name__ == "__main__":
    asyncio.run(test_communication())