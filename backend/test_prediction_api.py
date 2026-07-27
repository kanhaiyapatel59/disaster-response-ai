"""
Quick test script for Prediction Agent
"""
import asyncio
import httpx
import json

async def test_prediction():
    """Test the prediction endpoint with valid data"""
    
    url = "http://localhost:8000/api/prediction/analyze"
    
    # Test with properly formatted data
    payload = {
        "weather_data": {
            "data": {
                "location": "Mumbai",
                "risk_score": 65,
                "risk_level": "HIGH",
                "current": {
                    "temperature": 28.5,
                    "rainfall": 8.5,
                    "humidity": 92
                },
                "forecast": [
                    {"rain_mm": 5.2},
                    {"rain_mm": 3.8}
                ]
            }
        },
        "detection_data": {
            "data": {
                "analysis": {
                    "people_detected": 35,
                    "flood_area_percent": 65.5,
                    "severity_level": "HIGH"
                }
            }
        }
    }
    
    print("📤 Sending prediction request...")
    print(json.dumps(payload, indent=2))
    print("\n" + "="*50)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=30.0)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS!")
            print(f"Agent: {data.get('agent_name')}")
            print(f"Status: {data.get('status')}")
            
            prediction_data = data.get('data', {})
            predictions = prediction_data.get('predictions', {})
            
            print(f"\n📊 Predictions:")
            print(f"   Urgency Level: {predictions.get('urgency_level', 'N/A')}")
            print(f"   Urgency Score: {predictions.get('urgency_score', 0)}")
            print(f"   Overall Risk: {predictions.get('overall_risk_score', 0)}%")
            
            water_rise = predictions.get('water_level_rise', {})
            print(f"\n🌊 Water Level Rise:")
            print(f"   Current: {water_rise.get('current_rise_percent', 0)}%")
            print(f"   Predicted: {water_rise.get('predicted_rise_percent', 0)}%")
            print(f"   Category: {water_rise.get('category', 'N/A')}")
            
            roads = predictions.get('road_accessibility', {})
            print(f"\n🛤️  Roads:")
            print(f"   Status: {roads.get('status', 'N/A')}")
            print(f"   Score: {roads.get('accessibility_score', 0)}%")
            
            print(f"\n✅ Recommended Actions:")
            for i, action in enumerate(prediction_data.get('recommended_actions', []), 1):
                print(f"   {i}. {action}")
        else:
            print(f"\n❌ ERROR: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_prediction())