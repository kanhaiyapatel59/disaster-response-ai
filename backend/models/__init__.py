"""
Pydantic models for data validation
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentReport(BaseModel):
    """Main incident report model"""
    incident_id: str
    location: str
    severity: SeverityLevel
    timestamp: datetime
    description: str
    status: str = "active"

class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    agent_name: str
    status: str  # "success" or "error"
    data: Dict[str, Any]
    message: Optional[str] = None
    timestamp: datetime = datetime.now()