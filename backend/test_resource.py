"""
Test script for Resource Agent
"""
import asyncio
from agents.resource_agent import resource_agent

async def test_resource():
    """Test the Resource Agent"""
    
    print("🏥 Testing Resource Agent...")
    print("-" * 50)
    
    # Test 1: Basic resource lookup
    print("\n📍 Test 1: Resources in Mumbai")
    print("-" * 40)
    
    result = await resource_agent.analyze(
        location="Mumbai",
        people_affected=100,
        severity="HIGH"
    )
    
    if result.status == "success":
        data = result.data
        print(f"\n📍 Location: {data.get('location')}")
        
        print("\n🏠 Nearest Shelters:")
        for shelter in data.get("nearest_shelters", [])[:3]:
            print(f"   • {shelter.get('name')}: {shelter.get('available_spaces')} spaces available "
                  f"({shelter.get('distance_km')}km away)")
        
        print("\n🏥 Nearest Hospitals:")
        for hospital in data.get("nearest_hospitals", [])[:3]:
            print(f"   • {hospital.get('name')}: {hospital.get('beds_available')} beds available "
                  f"({hospital.get('distance_km')}km away)")
        
        print("\n🚑 Available Teams:")
        for team in data.get("available_teams", [])[:3]:
            print(f"   • {team.get('name')}: {team.get('members')} members, {team.get('boats')} boats "
                  f"({team.get('distance_km')}km away)")
        
        print("\n📊 Resource Allocation:")
        allocation = data.get("resource_allocation", {})
        print(f"   Shelter capacity allocated: {allocation.get('shelter_capacity_allocated')} spaces")
        print(f"   Medical beds allocated: {allocation.get('medical_resources', {}).get('beds_allocated')} beds")
        print(f"   Teams dispatched: {allocation.get('total_teams_dispatched')} teams")
        print(f"   Resource sufficiency: {allocation.get('resource_sufficiency', 'UNKNOWN')}")
        
        print("\n⚠️  Resource Gaps:")
        for gap in data.get("resource_gaps", []):
            print(f"   • {gap}")
    
    # Test 2: Different location
    print("\n\n📍 Test 2: Resources in Andheri")
    print("-" * 40)
    
    result2 = await resource_agent.analyze(
        location="Andheri",
        people_affected=50,
        severity="MEDIUM"
    )
    
    if result2.status == "success":
        data = result2.data
        print(f"\n📍 Location: {data.get('location')}")
        allocation = data.get("resource_allocation", {})
        print(f"   Shelter capacity: {allocation.get('shelter_capacity_allocated')} spaces")
        print(f"   Resource sufficiency: {allocation.get('resource_sufficiency')}")
    
    # Test 3: Resource summary
    print("\n\n📊 Global Resource Summary")
    print("-" * 40)
    
    summary = await resource_agent.analyze(
        location="Mumbai",
        people_affected=10,
        severity="LOW"
    )
    
    if summary.status == "success":
        summary_data = summary.data.get("resource_summary", {})
        
        print("\n🏠 Shelters:")
        for key, value in summary_data.get("shelters", {}).items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print("\n🏥 Hospitals:")
        for key, value in summary_data.get("hospitals", {}).items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print("\n🚑 Rescue Teams:")
        for key, value in summary_data.get("rescue_teams", {}).items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "-" * 50)
    print("✅ Resource Agent tests complete!")

if __name__ == "__main__":
    asyncio.run(test_resource())