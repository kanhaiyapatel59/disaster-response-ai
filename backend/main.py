"""
Main FastAPI application for AI Disaster Command Center
"""
import json
import os
import shutil
from typing import Any, Dict, Optional
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from config import config
from models import IncidentReport
from agents.weather_agent import weather_agent
from agents.detection_agent import detection_agent
from agents.prediction_agent import prediction_agent
from agents.resource_agent import resource_agent, database_tool
from agents.communication_agent import communication_agent
from agents.commander_agent import commander_agent

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="Multi-Agent Disaster Response Command Center"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs("uploads", exist_ok=True)


# --- Request/Response Models ---
class WeatherRequest(BaseModel):
    location: str
    use_cache: bool = True


class AgentStatusResponse(BaseModel):
    agent_name: str
    status: str
    data: dict
    message: str


class PredictionRequest(BaseModel):
    weather_data: Dict[str, Any]
    detection_data: Dict[str, Any]


class ResourceRequest(BaseModel):
    location: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    people_affected: int = 0
    severity: str = "MEDIUM"


class CommunicationRequest(BaseModel):
    weather_data: Dict[str, Any]
    detection_data: Dict[str, Any]
    prediction_data: Dict[str, Any]
    resource_data: Dict[str, Any]
    incident_location: str = "Unknown"


class CommanderRequest(BaseModel):
    location: str
    people_affected_estimate: Optional[int] = None


# --- Weather Agent Endpoints ---
@app.post("/api/weather/analyze")
async def analyze_weather(request: WeatherRequest):
    """
    Analyze weather for a location
    """
    try:
        result = await weather_agent.analyze(
            location=request.location,
            use_cache=request.use_cache
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/weather/status")
async def weather_status():
    """
    Get weather agent status
    """
    return {
        "agent": "Weather Agent",
        "status": "operational",
        "simulation_mode": weather_agent.weather_tool.use_simulation,
        "cache_size": len(weather_agent.cache)
    }


# --- Detection Agent Endpoints ---
@app.post("/api/detection/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    location: str = Form("Unknown")
):
    """
    Analyze a drone/CCTV image for disaster assessment
    """
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {image.content_type} not supported. Use JPEG, PNG, or WEBP."
            )

        # Analyze image
        result = await detection_agent.analyze_image(image, location=location)

        if getattr(result, "status", None) == "error":
            raise HTTPException(status_code=500, detail=result.message)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/detection/status")
async def detection_status():
    """
    Get detection agent status
    """
    return {
        "agent": "Detection Agent",
        "status": "operational",
        "mode": "simulation",
        "upload_dir": str(detection_agent.upload_dir)
    }


# --- Prediction Agent Endpoints ---
@app.post("/api/prediction/analyze")
async def analyze_prediction(request: PredictionRequest):
    """
    Generate predictions based on weather and detection data
    """
    try:
        result = await prediction_agent.predict(
            weather_data=request.weather_data,
            detection_data=request.detection_data
        )

        if getattr(result, "status", None) == "error":
            raise HTTPException(status_code=500, detail=result.message)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/prediction/status")
async def prediction_status():
    """
    Get prediction agent status
    """
    return {
        "agent": "Prediction Agent",
        "status": "operational"
    }


# --- Resource Agent Endpoints ---
@app.post("/api/resources/analyze")
async def analyze_resources(request: ResourceRequest):
    """
    Analyze resource availability for a location
    """
    try:
        result = await resource_agent.analyze(
            location=request.location,
            lat=request.lat,
            lng=request.lng,
            people_affected=request.people_affected,
            severity=request.severity
        )

        if getattr(result, "status", None) == "error":
            raise HTTPException(status_code=500, detail=result.message)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/resources/status")
async def resource_status():
    """
    Get resource agent status
    """
    return {
        "agent": "Resource Agent",
        "status": "operational",
        "data_sources": {
            "shelters": len(database_tool.shelters),
            "hospitals": len(database_tool.hospitals),
            "rescue_teams": len(database_tool.rescue_teams)
        }
    }


@app.get("/api/resources/summary")
async def resource_summary():
    """
    Get overall resource summary
    """
    return database_tool.get_resource_summary()


# --- Communication Agent Endpoints ---
@app.post("/api/communication/generate")
async def generate_report(request: CommunicationRequest):
    """
    Generate complete incident report from all agent data
    """
    try:
        result = await communication_agent.generate_report(
            weather_data=request.weather_data,
            detection_data=request.detection_data,
            prediction_data=request.prediction_data,
            resource_data=request.resource_data,
            incident_location=request.incident_location
        )

        if getattr(result, "status", None) == "error":
            raise HTTPException(status_code=500, detail=result.message)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/communication/status")
async def communication_status():
    """
    Get communication agent status
    """
    return {
        "agent": "Communication Agent",
        "status": "operational",
        "reports_generated": communication_agent.incident_counter
    }


# --- Commander Agent Endpoints ---
@app.post("/api/incident/analyze")
async def analyze_incident(
    location: str = Form(...),
    image: Optional[UploadFile] = File(None),
    people_affected_estimate: Optional[int] = Form(None)
):
    """
    Full incident analysis using the Commander Agent.
    Orchestrates all 5 agents in the correct order.
    """
    try:
        image_path = None

        # Save image if provided
        if image and image.filename:
            file_id = str(uuid.uuid4())[:8]
            file_ext = os.path.splitext(image.filename)[1]
            save_path = config.UPLOAD_DIR / f"incident_{file_id}{file_ext}"

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            image_path = str(save_path)

        # Run commander agent
        result = await commander_agent.analyze_incident(
            location=location,
            image_path=image_path,
            people_affected_estimate=people_affected_estimate
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/incident/status")
async def incident_status():
    """
    Get commander agent status
    """
    return {
        "agent": "Commander Agent",
        "status": "operational",
        "workflow": "LangGraph Orchestration",
        "agents": ["weather", "detection", "prediction", "resource", "communication"]
    }


# --- Health Check Endpoints ---
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": config.APP_NAME,
        "version": config.APP_VERSION,
        "status": "operational",
        "message": "🆘 AI Disaster Command Center is ready"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_keys": {
            "groq": bool(config.GROQ_API_KEY),
            "openweather": bool(config.OPENWEATHER_API_KEY),
            "google": bool(config.GOOGLE_API_KEY)
        },
        "services": {
            "database": "sqlite",
            "upload_dir": str(config.UPLOAD_DIR)
        }
    }


# --- Main Entry Point ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.DEBUG
    )