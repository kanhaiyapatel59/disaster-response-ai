"""
Resource Agent - Manages shelters, hospitals, and rescue team resources
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import math

from tools.database_tool import database_tool
from models import AgentResponse

class ResourceAgent:
    """
    Resource Agent responsible for:
    1. Finding nearest shelters with capacity
    2. Checking hospital bed availability
    3. Listing available rescue teams
    4. Allocating resources based on need
    5. Identifying resource gaps
    """
    
    def __init__(self):
        self.name = "Resource Agent"
    
    async def analyze(self, location: str, lat: float = None, lng: float = None,
                     people_affected: int = 0, severity: str = "MEDIUM") -> AgentResponse:
        """
        Analyze resource availability for a location
        
        Args:
            location: Location name
            lat: Latitude for geospatial search
            lng: Longitude for geospatial search
            people_affected: Number of people needing help
            severity: Incident severity level
            
        Returns:
            AgentResponse with resource data
        """
        try:
            # If no coordinates provided, use default Mumbai coordinates
            if lat is None or lng is None:
                # Simple geocoding for Indian cities
                lat, lng = self._geocode_location(location)
            
            # Find resources
            nearest_shelters = database_tool.find_nearest_shelters(lat, lng, limit=5)
            nearest_hospitals = database_tool.find_nearest_hospitals(lat, lng, limit=3)
            available_teams = database_tool.find_available_teams(lat, lng, limit=5)
            
            # Calculate resource allocation
            allocation = self._allocate_resources(
                people_affected,
                severity,
                nearest_shelters,
                nearest_hospitals,
                available_teams
            )
            
            # Identify resource gaps
            gaps = self._identify_gaps(
                people_affected,
                nearest_shelters,
                nearest_hospitals,
                available_teams
            )
            
            return AgentResponse(
                agent_name=self.name,
                status="success",
                data={
                    "location": location,
                    "coordinates": {"lat": lat, "lng": lng},
                    "nearest_shelters": nearest_shelters,
                    "nearest_hospitals": nearest_hospitals,
                    "available_teams": available_teams,
                    "resource_allocation": allocation,
                    "resource_gaps": gaps,
                    "resource_summary": database_tool.get_resource_summary(),
                    "timestamp": datetime.now().isoformat()
                },
                message=f"Resource analysis completed. Found {len(nearest_shelters)} shelters, "
                       f"{len(nearest_hospitals)} hospitals, {len(available_teams)} teams."
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                status="error",
                data={},
                message=f"Error analyzing resources: {str(e)}"
            )
    
    def _geocode_location(self, location: str) -> tuple:
        """Simple geocoding for demo locations"""
        # This is a simplified version - in production, use a real geocoding API
        locations = {
            "mumbai": (19.0760, 72.8777),
            "andheri": (19.1136, 72.8697),
            "bandra": (19.0556, 72.8401),
            "powai": (19.1176, 72.9064),
            "dadar": (19.0178, 72.8478),
            "chennai": (13.0827, 80.2707),
            "delhi": (28.6139, 77.2090),
            "kolkata": (22.5726, 88.3639)
        }
        
        location_lower = location.lower()
        for key, coords in locations.items():
            if key in location_lower:
                return coords
        
        # Default to Mumbai
        return (19.0760, 72.8777)
    
    def _allocate_resources(self, people_affected: int, severity: str,
                           shelters: List[Dict], hospitals: List[Dict],
                           teams: List[Dict]) -> Dict[str, Any]:
        """Allocate resources based on need"""
        
        # Determine resource intensity based on severity
        intensity_map = {
            "CRITICAL": 1.0,
            "HIGH": 0.8,
            "MEDIUM": 0.5,
            "LOW": 0.3
        }
        intensity = intensity_map.get(severity, 0.5)
        
        # Allocate shelter spaces
        shelter_allocation = 0
        for shelter in shelters[:3]:
            shelter_allocation += min(
                shelter.get("available_spaces", 0),
                int(people_affected * intensity / 3)
            )
        
        # Allocate medical resources
        medical_allocation = {
            "beds_needed": int(people_affected * intensity * 0.2),  # 20% may need medical care
            "beds_allocated": 0,
            "icu_beds_needed": int(people_affected * intensity * 0.05),  # 5% may need ICU
            "icu_beds_allocated": 0
        }
        
        for hospital in hospitals[:2]:
            medical_allocation["beds_allocated"] += min(
                hospital.get("beds_available", 0),
                int(medical_allocation["beds_needed"] / 2)
            )
            medical_allocation["icu_beds_allocated"] += min(
                hospital.get("icu_available", 0),
                int(medical_allocation["icu_beds_needed"] / 2)
            )
        
        # Allocate rescue teams
        teams_allocated = []
        for team in teams[:3]:
            if len(teams_allocated) < max(1, int(3 * intensity)):
                teams_allocated.append({
                    "team_id": team.get("id"),
                    "team_name": team.get("name"),
                    "members": team.get("members", 0),
                    "boats": team.get("boats", 0),
                    "vehicles": team.get("vehicles", 0),
                    "distance_km": team.get("distance_km", 0)
                })
        
        return {
            "shelter_capacity_allocated": shelter_allocation,
            "medical_resources": medical_allocation,
            "teams_allocated": teams_allocated,
            "total_teams_dispatched": len(teams_allocated),
            "resource_sufficiency": self._assess_sufficiency(
                people_affected,
                shelter_allocation,
                medical_allocation,
                len(teams_allocated)
            )
        }
    
    def _assess_sufficiency(self, people_affected: int, shelter_allocated: int,
                           medical_allocated: Dict, teams_count: int) -> str:
        """Assess if resources are sufficient"""
        
        # Check if we have enough shelter space
        shelter_sufficient = shelter_allocated >= people_affected * 0.5  # At least 50% can be sheltered
        
        # Check if we have enough medical beds
        beds_allocated = medical_allocated.get("beds_allocated", 0)
        beds_needed = medical_allocated.get("beds_needed", 0)
        medical_sufficient = beds_allocated >= beds_needed * 0.6  # At least 60% of needed beds
        
        # Check if we have enough teams
        teams_sufficient = teams_count >= 2  # At least 2 teams for medium incidents
        
        if shelter_sufficient and medical_sufficient and teams_sufficient:
            return "ADEQUATE"
        elif shelter_sufficient or medical_sufficient or teams_sufficient:
            return "PARTIAL"
        else:
            return "INADEQUATE"
    
    def _identify_gaps(self, people_affected: int, shelters: List[Dict],
                      hospitals: List[Dict], teams: List[Dict]) -> List[str]:
        """Identify resource gaps"""
        
        gaps = []
        
        # Check shelter capacity
        total_available = sum(s.get("available_spaces", 0) for s in shelters[:3])
        if total_available < people_affected * 0.5:
            gaps.append(f"🏠 Shelter capacity shortfall: Need space for {int(people_affected * 0.5)} people, "
                       f"only {total_available} available nearby")
        
        # Check hospital beds
        total_beds = sum(h.get("beds_available", 0) for h in hospitals[:2])
        beds_needed = int(people_affected * 0.2)  # 20% may need medical care
        if total_beds < beds_needed * 0.6:
            gaps.append(f"🏥 Medical bed shortage: Need {beds_needed} beds, "
                       f"only {total_beds} available nearby")
        
        # Check rescue teams
        available_teams = len([t for t in teams if t.get("distance_km", 999) < 20])
        if available_teams < 2:
            gaps.append(f"🚑 Insufficient rescue teams: Only {available_teams} teams within 20km")
        
        # Check boats
        total_boats = sum(t.get("boats", 0) for t in teams)
        if total_boats < 3 and people_affected > 20:
            gaps.append("🚤 Limited boat capacity for water rescue")
        
        return gaps

# Create singleton instance
resource_agent = ResourceAgent()