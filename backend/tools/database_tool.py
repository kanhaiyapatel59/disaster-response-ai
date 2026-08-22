"""
Database Tool - Manages data for shelters, hospitals, and rescue teams with MongoDB Atlas integration and JSON fallback.
"""
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from math import radians, cos, sin, asin, sqrt

try:
    import pymongo
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

from config import config

class DatabaseTool:
    """Tool for accessing disaster response data from MongoDB Atlas with JSON fallback"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.mongo_client = None
        self.db = None
        self.mongo_connected = False
        
        self._init_mongo()
        self.reload_data()
        
        print(f"🏥 Database Tool initialized (MongoDB connected: {self.mongo_connected}) with "
              f"{len(self.shelters)} shelters, {len(self.hospitals)} hospitals, {len(self.rescue_teams)} rescue teams")
    
    def _init_mongo(self):
        """Initialize MongoDB Atlas connection if available"""
        if not PYMONGO_AVAILABLE:
            print("⚠️ pymongo not installed. Operating in local JSON fallback mode.")
            return
            
        mongo_uri = getattr(config, "MONGO_URI", "")
        if mongo_uri:
            try:
                self.mongo_client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
                # Quick server check
                self.mongo_client.admin.command('ping')
                self.db = self.mongo_client.get_default_database()
                if self.db is None:
                    self.db = self.mongo_client["disaster_db"]
                self.mongo_connected = True
                print("🟢 Connected successfully to MongoDB Atlas!")
            except Exception as e:
                print(f"⚠️ Could not connect to MongoDB Atlas ({e}). Falling back to local JSON files.")
                self.mongo_connected = False
    
    def reload_data(self):
        """Load data from MongoDB Atlas or local JSON fallback"""
        if self.mongo_connected and self.db is not None:
            try:
                shelters_cursor = list(self.db.shelters.find({}, {"_id": 0}))
                hospitals_cursor = list(self.db.hospitals.find({}, {"_id": 0}))
                teams_cursor = list(self.db.rescue_teams.find({}, {"_id": 0}))
                
                # Use MongoDB data if collections are populated
                if shelters_cursor or hospitals_cursor or teams_cursor:
                    self.shelters = shelters_cursor
                    self.hospitals = hospitals_cursor
                    self.rescue_teams = teams_cursor
                    return
            except Exception as e:
                print(f"⚠️ Error querying MongoDB collections: {e}")
        
        # Fallback to JSON files
        self.shelters = self._load_json_data("shelters.json")
        self.hospitals = self._load_json_data("hospitals.json")
        self.rescue_teams = self._load_json_data("rescue_teams.json")
    
    def _load_json_data(self, filename: str) -> List[Dict]:
        """Load data from local JSON file"""
        try:
            file_path = self.data_dir / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if filename == "shelters.json":
                        return data.get("shelters", [])
                    elif filename == "hospitals.json":
                        return data.get("hospitals", [])
                    elif filename == "rescue_teams.json":
                        return data.get("rescue_teams", [])
            return []
        except Exception as e:
            print(f"⚠️ Error loading {filename}: {e}")
            return []

    def seed_database(self) -> Dict[str, Any]:
        """
        Seed sample data from local JSON files into MongoDB Atlas database.
        Returns seeding status and document counts.
        """
        shelters_data = self._load_json_data("shelters.json")
        hospitals_data = self._load_json_data("hospitals.json")
        teams_data = self._load_json_data("rescue_teams.json")

        result = {
            "status": "success",
            "mongo_connected": self.mongo_connected,
            "counts": {
                "shelters": len(shelters_data),
                "hospitals": len(hospitals_data),
                "rescue_teams": len(teams_data)
            },
            "message": ""
        }

        # Try to reconnect if not connected yet
        if not self.mongo_connected:
            self._init_mongo()

        if self.mongo_connected and self.db is not None:
            try:
                # Seed Shelters
                if shelters_data:
                    self.db.shelters.delete_many({})
                    self.db.shelters.insert_many(shelters_data)
                
                # Seed Hospitals
                if hospitals_data:
                    self.db.hospitals.delete_many({})
                    self.db.hospitals.insert_many(hospitals_data)
                
                # Seed Rescue Teams
                if teams_data:
                    self.db.rescue_teams.delete_many({})
                    self.db.rescue_teams.insert_many(teams_data)

                self.reload_data()
                result["message"] = "Successfully populated sample disaster data into MongoDB Atlas!"
                result["db_name"] = self.db.name
            except Exception as e:
                result["status"] = "error"
                result["message"] = f"Failed to seed MongoDB Atlas: {str(e)}"
        else:
            # Local update
            self.shelters = shelters_data
            self.hospitals = hospitals_data
            self.rescue_teams = teams_data
            result["message"] = "Seeded local memory cache with sample data (MongoDB Atlas not connected)."

        return result
    
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
                    shelter_copy = dict(shelter)
                    shelter_copy["distance_km"] = round(distance, 2)
                    valid_shelters.append(shelter_copy)
        
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
                    hospital_copy = dict(hospital)
                    hospital_copy["distance_km"] = round(distance, 2)
                    valid_hospitals.append(hospital_copy)
        
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
                    team_copy = dict(team)
                    team_copy["distance_km"] = round(distance, 2)
                    valid_teams.append(team_copy)
        
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
            },
            "database_status": {
                "type": "MongoDB Atlas" if self.mongo_connected else "Local JSON Fallback",
                "connected": self.mongo_connected
            }
        }

# Create singleton instance
database_tool = DatabaseTool()