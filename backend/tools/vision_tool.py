"""
Vision Tool - Simulates computer vision analysis of drone/CCTV images
For hackathon demo - generates realistic detection data
"""
import os
import random
from datetime import datetime
from typing import Dict, Any, Optional, List
from PIL import Image
import json

class VisionTool:
    """Simulated vision analysis tool"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
        print("📸 Vision Tool initialized (SIMULATION MODE)")
    
    def analyze_image(self, image_path: str, location: str = "Unknown") -> Dict[str, Any]:
        """
        Analyze an image and simulate detection results
        
        Args:
            image_path: Path to uploaded image
            location: Location description
            
        Returns:
            Dict with detection results
        """
        try:
            # Open image to get dimensions (for realism)
            img = Image.open(image_path)
            width, height = img.size
            
            # Simulate detection based on image properties
            # Larger images = more "detected" objects
            area_factor = (width * height) / (1920 * 1080)  # Relative to HD
            base_count = int(area_factor * random.randint(5, 20))
            
            # Simulate realistic detection data
            people_detected = random.randint(5, 50) + base_count
            flood_area_percent = random.uniform(15, 85)
            
            # Determine severity based on people count + flood area
            severity_score = min(100, 
                (people_detected / 50) * 60 +  # People factor (60%)
                (flood_area_percent / 100) * 40  # Flood factor (40%)
            )
            
            # Generate random coordinates for "detected" people
            detections = self._generate_detections(people_detected, width, height)
            
            return {
                "image_path": image_path,
                "location": location,
                "analysis": {
                    "people_detected": people_detected,
                    "flood_area_percent": round(flood_area_percent, 2),
                    "water_level": self._estimate_water_level(flood_area_percent),
                    "severity_score": round(severity_score, 2),
                    "severity_level": self._get_severity_level(severity_score),
                    "detections": detections[:20],  # Return top 20 for display
                    "image_dimensions": {"width": width, "height": height}
                },
                "recommendations": self._generate_recommendations(
                    people_detected, flood_area_percent, severity_score
                ),
                "timestamp": datetime.now().isoformat(),
                "simulated": True
            }
            
        except Exception as e:
            print(f"⚠️  Vision analysis error: {e}")
            return self._simulate_fallback(location)
    
    def _generate_detections(self, count: int, width: int, height: int) -> List[Dict]:
        """Generate random detection coordinates"""
        detections = []
        for i in range(min(count, 50)):  # Max 50 detections for display
            detections.append({
                "id": f"person_{i+1}",
                "type": random.choice(["person", "vehicle", "animal"]),
                "confidence": round(random.uniform(0.65, 0.98), 2),
                "bbox": {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "width": random.randint(20, 80),
                    "height": random.randint(40, 120)
                }
            })
        return detections
    
    def _estimate_water_level(self, flood_percent: float) -> str:
        """Estimate water level based on flood area"""
        if flood_percent > 70:
            return "SEVERE (> 2 meters)"
        elif flood_percent > 40:
            return "MODERATE (1-2 meters)"
        elif flood_percent > 20:
            return "MILD (0.5-1 meters)"
        else:
            return "LOW (< 0.5 meters)"
    
    def _get_severity_level(self, score: float) -> str:
        """Convert severity score to level"""
        if score >= 75:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendations(self, people: int, flood_area: float, severity: float) -> List[str]:
        """Generate realistic recommendations"""
        recommendations = []
        
        if people > 30:
            recommendations.append("🚨 High population density detected - prioritize rescue")
        if flood_area > 50:
            recommendations.append("🌊 Extensive flooding - boats required for rescue")
        if severity > 60:
            recommendations.append("⚡ Immediate evacuation recommended")
        
        if people > 10 and flood_area > 30:
            recommendations.append("🚑 Medical teams needed on site")
        
        recommendations.append("📡 Continue drone surveillance")
        
        return recommendations[:4]  # Return top 4
    
    def _simulate_fallback(self, location: str) -> Dict[str, Any]:
        """Fallback when image analysis fails"""
        return {
            "image_path": "simulated",
            "location": location,
            "analysis": {
                "people_detected": random.randint(5, 25),
                "flood_area_percent": round(random.uniform(20, 60), 2),
                "water_level": "MODERATE (1-2 meters)",
                "severity_score": round(random.uniform(30, 70), 2),
                "severity_level": "HIGH",
                "detections": [],
                "image_dimensions": {"width": 1920, "height": 1080}
            },
            "recommendations": [
                "⚠️  Simulated analysis - verify with ground data",
                "🚑 Deploy rescue teams to location",
                "📡 Request additional drone coverage"
            ],
            "timestamp": datetime.now().isoformat(),
            "simulated": True,
            "fallback": True
        }

# Create singleton instance
vision_tool = VisionTool()