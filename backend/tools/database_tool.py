"""
Database Tool - Manages mock data for shelters, hospitals, and rescue teams
"""
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

class DatabaseTool:
    """Tool for accessing mock disaster response data"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.shelters = self._load_data("shelters.json")
        self.hospitals = self._load_data("hospitals.json")
        self.rescue_teams = self._load_data("rescue_teams.json")
        print(f"🏥 Database Tool initialized with {len(self.shelters)} shelters, "
              f"{len(self.hospitals)} hospitals, {len(self.rescue_teams)} teams")
    
    def _load_data(self, filename: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            file_path = self.data_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Handle different file structures
                    if filename == "shelters.json":
                        return data.get("shelters", [])
                    elif filename == "hospitals.json":
                        return data.get("hospitals", [])
                    elif filename == "rescue_teams.json":
                        return data.get("rescue_teams", [])
            return []
        except Exception as e:
            print(f"⚠️  Error loading {filename}: {e}")
            return []
    
    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        if None in [lat1, lon1, lat2, lon2]:
            return 999  # Return large distance for invalid coordinates
        
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        return R * c
    
    def find_nearest_shelters(self, lat: float, lng: float, 
                              limit: int = 3) -> List[Dict]:
        """Find nearest shelters with available capacity"""
        
        valid_shelters = []
        for shelter in self.shelters:
            if shelter.get("status") == "open" and shelter.get("available_spaces", 0) > 10:
                shelter_lat = shelter.get("lat")
                shelter_lng = shelter.get("lng")
                
                if shelter_lat and shelter_lng:
                    distance = self.haversine_distance(lat, lng, shelter_lat, shelter_lng)
                    shelter["distance_km"] = round(distance, 2)
                    valid_shelters.append(shelter)
        
        # Sort by distance
        valid_shelters.sort(key=lambda x: x.get("distance_km", 999))
        
        return valid_shelters[:limit]
    
    def find_nearest_hospitals(self, lat: float, lng: float, 
                               limit: int = 3) -> List[Dict]:
        """Find nearest hospitals with bed availability"""
        
        valid_hospitals = []
        for hospital in self.hospitals:
            if hospital.get("beds_available", 0) > 5:
                hospital_lat = hospital.get("lat")
                hospital_lng = hospital.get("lng")
                
                if hospital_lat and hospital_lng:
                    distance = self.haversine_distance(lat, lng, hospital_lat, hospital_lng)
                    hospital["distance_km"] = round(distance, 2)
                    valid_hospitals.append(hospital)
        
        # Sort by distance
        valid_hospitals.sort(key=lambda x: x.get("distance_km", 999))
        
        return valid_hospitals[:limit]
    
    def find_available_teams(self, lat: float, lng: float, 
                            team_type: Optional[str] = None,
                            limit: int = 3) -> List[Dict]:
        """Find available rescue teams near location"""
        
        valid_teams = []
        for team in self.rescue_teams:
            if team.get("status") == "available":
                if team_type and team.get("type") != team_type:
                    continue
                
                team_lat = team.get("lat")
                team_lng = team.get("lng")
                
                if team_lat and team_lng:
                    distance = self.haversine_distance(lat, lng, team_lat, team_lng)
                    team["distance_km"] = round(distance, 2)
                    valid_teams.append(team)
        
        # Sort by distance
        valid_teams.sort(key=lambda x: x.get("distance_km", 999))
        
        return valid_teams[:limit]
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get summary of all available resources"""
        
        total_shelters = len(self.shelters)
        open_shelters = len([s for s in self.shelters if s.get("status") == "open"])
        total_capacity = sum(s.get("capacity", 0) for s in self.shelters)
        total_available = sum(s.get("available_spaces", 0) for s in self.shelters)
        
        total_beds = sum(h.get("beds_total", 0) for h in self.hospitals)
        available_beds = sum(h.get("beds_available", 0) for h in self.hospitals)
        total_ambulances = sum(h.get("ambulances", 0) for h in self.hospitals)
        
        available_teams = len([t for t in self.rescue_teams if t.get("status") == "available"])
        total_boats = sum(t.get("boats", 0) for t in self.rescue_teams)
        
        return {
            "shelters": {
                "total": total_shelters,
                "open": open_shelters,
                "total_capacity": total_capacity,
                "available_spaces": total_available,
                "occupancy_rate": round((1 - total_available/total_capacity) * 100, 1) if total_capacity > 0 else 0
            },
            "hospitals": {
                "total": len(self.hospitals),
                "total_beds": total_beds,
                "available_beds": available_beds,
                "bed_availability_rate": round((available_beds/total_beds) * 100, 1) if total_beds > 0 else 0,
                "total_ambulances": total_ambulances
            },
            "rescue_teams": {
                "total": len(self.rescue_teams),
                "available": available_teams,
                "total_boats": total_boats,
                "availability_rate": round((available_teams/len(self.rescue_teams)) * 100, 1) if self.rescue_teams else 0
            }
        }

# Create singleton instance
database_tool = DatabaseTool()