"""
Test script for Commander Agent
"""
import asyncio
import sys
import os

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.commander_agent import commander_agent

async def test_commander():
    """Test the full commander workflow"""
    
    print("🚀 Testing Commander Agent...")
    print("="*60)
    
    # Test 1: Basic incident analysis
    result = await commander_agent.analyze_incident(
        location="Mumbai",
        people_affected_estimate=50
    )
    
    print("\n📊 RESULTS:")
    print(f"   Status: {result.get('status')}")
    print(f"   Urgency: {result.get('urgency')}")
    print(f"   Risk Score: {result.get('risk_score')}")
    print(f"   Steps Executed: {result.get('execution_order')}")
    
    if result.get('report'):
        report = result['report']
        print(f"\n📋 Report Generated: {report.get('incident_id')}")
        print(f"   Title: {report.get('title')}")
    
    print("\n" + "="*60)
    print("✅ Commander Agent test complete!")

if __name__ == "__main__":
    asyncio.run(test_commander())