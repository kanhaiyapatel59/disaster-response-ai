"""
Detection Agent - Analyzes drone/CCTV images for disaster assessment
"""
import os
import shutil
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from tools.vision_tool import vision_tool
from models import AgentResponse
from config import config

class DetectionAgent:
    """
    Detection Agent responsible for:
    1. Analyzing uploaded images (drone/CCTV)
    2. Detecting people in distress
    3. Estimating flood area
    4. Providing severity assessment
    """
    
    def __init__(self):
        self.name = "Detection Agent"
        self.upload_dir = config.UPLOAD_DIR
        
        # Ensure upload directory exists
        self.upload_dir.mkdir(exist_ok=True)
    
    async def analyze_image(self, image_file, location: str = "Unknown") -> AgentResponse:
        """
        Analyze an uploaded image
        
        Args:
            image_file: Uploaded image file (FastAPI UploadFile)
            location: Location description
            
        Returns:
            AgentResponse with detection results
        """
        try:
            # Save uploaded image
            file_id = str(uuid.uuid4())[:8]
            file_ext = os.path.splitext(image_file.filename)[1]
            save_path = self.upload_dir / f"detection_{file_id}{file_ext}"
            
            # Save the file
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
            
            # Analyze image
            results = vision_tool.analyze_image(
                str(save_path),
                location=location
            )
            
            return AgentResponse(
                agent_name=self.name,
                status="success",
                data={
                    "image_id": file_id,
                    "image_path": str(save_path),
                    "analysis": results["analysis"],
                    "recommendations": results.get("recommendations", []),
                    "location": location
                },
                message=f"Image analysis completed. Detected {results['analysis']['people_detected']} people."
            )
            
        except Exception as e:
            return AgentResponse(
                agent_name=self.name,
                status="error",
                data={},
                message=f"Error analyzing image: {str(e)}"
            )
    
    def get_severity_summary(self, detection_data: Dict) -> Dict[str, Any]:
        """
        Extract key severity information from detection results
        """
        analysis = detection_data.get("analysis", {})
        return {
            "severity_level": analysis.get("severity_level", "UNKNOWN"),
            "severity_score": analysis.get("severity_score", 0),
            "people_detected": analysis.get("people_detected", 0),
            "flood_area_percent": analysis.get("flood_area_percent", 0),
            "water_level": analysis.get("water_level", "Unknown"),
            "needs_immediate_action": analysis.get("severity_score", 0) > 50
        }

# Create singleton instance
detection_agent = DetectionAgent()