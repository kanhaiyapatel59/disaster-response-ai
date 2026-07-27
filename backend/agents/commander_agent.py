"""
Commander Agent - Orchestrates all agents using LangGraph
The brain of the Disaster Command Center
"""
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from datetime import datetime
import json
import operator

from langgraph.graph import StateGraph, END
# Fix: MemorySaver is now in langgraph.checkpoint.memory
from langgraph.checkpoint.memory import MemorySaver

from agents.weather_agent import weather_agent
from agents.detection_agent import detection_agent
from agents.prediction_agent import prediction_agent
from agents.resource_agent import resource_agent
from agents.communication_agent import communication_agent
from models import AgentResponse


# --- State Definition ---
class DisasterState(TypedDict):
    """State that flows through the LangGraph workflow"""
    
    # Input
    location: str
    image_path: Optional[str]
    people_affected_estimate: Optional[int]
    
    # Agent Results
    weather_result: Optional[Dict[str, Any]]
    detection_result: Optional[Dict[str, Any]]
    prediction_result: Optional[Dict[str, Any]]
    resource_result: Optional[Dict[str, Any]]
    communication_result: Optional[Dict[str, Any]]
    
    # Aggregated Data
    combined_risk_score: Optional[float]
    final_urgency: Optional[str]
    final_report: Optional[Dict[str, Any]]
    
    # Workflow Control
    current_step: str
    errors: List[str]
    execution_order: List[str]
    completed_steps: Annotated[List[str], operator.add]


class CommanderAgent:
    """
    Commander Agent using LangGraph to orchestrate all agents
    
    Workflow:
    1. Detect (if image provided) or use defaults
    2. Get Weather
    3. Predict (combines detection + weather)
    4. Get Resources (based on prediction)
    5. Generate Communication (final report)
    """
    
    def __init__(self):
        self.name = "Commander Agent"
        self.workflow = None
        self.memory = MemorySaver()
        self._build_workflow()
    
    def _build_workflow(self):
        """Build the LangGraph workflow"""
        
        # Create graph
        workflow = StateGraph(DisasterState)
        
        # Add nodes (each node is a step in the workflow)
        workflow.add_node("detect", self._detect_node)
        workflow.add_node("weather", self._weather_node)
        workflow.add_node("predict", self._predict_node)
        workflow.add_node("resource", self._resource_node)
        workflow.add_node("communicate", self._communicate_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Define edges (workflow flow)
        workflow.set_entry_point("weather")  # Start with weather
        
        # Weather → Detect (parallel or sequential?)
        workflow.add_edge("weather", "detect")
        
        # Detect → Predict
        workflow.add_edge("detect", "predict")
        
        # Predict → Resource
        workflow.add_edge("predict", "resource")
        
        # Resource → Communicate
        workflow.add_edge("resource", "communicate")
        
        # Communicate → Finalize
        workflow.add_edge("communicate", "finalize")
        
        # Finalize → END
        workflow.add_edge("finalize", END)
        
        # Compile workflow with checkpointer
        self.workflow = workflow.compile(checkpointer=self.memory)
    
    async def _detect_node(self, state: DisasterState) -> Dict[str, Any]:
        """Node: Run Detection Agent"""
        try:
            print(f"🔍 [Commander] Running Detection Agent...")
            
            # If we have an image path, use it
            if state.get("image_path"):
                # In a real scenario, we'd load the image file
                # For demo, we'll simulate with the state
                result = AgentResponse(
                    agent_name="Detection Agent",
                    status="success",
                    data={
                        "analysis": {
                            "people_detected": 35,
                            "flood_area_percent": 65.5,
                            "severity_level": "HIGH",
                            "water_level": "SEVERE (> 2 meters)"
                        }
                    }
                )
            else:
                # Use estimated people count if provided
                people = state.get("people_affected_estimate", 20)
                result = AgentResponse(
                    agent_name="Detection Agent",
                    status="success",
                    data={
                        "analysis": {
                            "people_detected": people,
                            "flood_area_percent": 40.0,
                            "severity_level": "MEDIUM",
                            "water_level": "MODERATE"
                        }
                    }
                )
            
            return {
                "detection_result": result.dict(),
                "completed_steps": ["detect"],
                "current_step": "detect"
            }
            
        except Exception as e:
            return {
                "errors": [f"Detection failed: {str(e)}"],
                "completed_steps": ["detect"]
            }
    
    async def _weather_node(self, state: DisasterState) -> Dict[str, Any]:
        """Node: Run Weather Agent"""
        try:
            print(f"🌤️ [Commander] Running Weather Agent for {state.get('location')}...")
            
            location = state.get("location", "Mumbai")
            result = await weather_agent.analyze(location, use_cache=True)
            
            return {
                "weather_result": result.dict(),
                "completed_steps": ["weather"],
                "current_step": "weather"
            }
            
        except Exception as e:
            return {
                "errors": [f"Weather failed: {str(e)}"],
                "completed_steps": ["weather"]
            }
    
    async def _predict_node(self, state: DisasterState) -> Dict[str, Any]:
        """Node: Run Prediction Agent"""
        try:
            print(f"🔮 [Commander] Running Prediction Agent...")
            
            weather_data = state.get("weather_result", {})
            detection_data = state.get("detection_result", {})
            
            result = await prediction_agent.predict(weather_data, detection_data)
            
            # Handle both dict and AgentResponse
            if hasattr(result, 'dict'):
                result_dict = result.dict()
            else:
                result_dict = result
            
            return {
                "prediction_result": result_dict,
                "combined_risk_score": result_dict.get("data", {}).get("predictions", {}).get("overall_risk_score", 0),
                "final_urgency": result_dict.get("data", {}).get("predictions", {}).get("urgency_level", "MEDIUM"),
                "completed_steps": ["predict"],
                "current_step": "predict"
            }
            
        except Exception as e:
            return {
                "errors": [f"Prediction failed: {str(e)}"],
                "completed_steps": ["predict"]
            }
    
    async def _resource_node(self, state: DisasterState) -> Dict[str, Any]:
        """Node: Run Resource Agent"""
        try:
            print(f"🏥 [Commander] Running Resource Agent...")
            
            # Get people affected from detection or estimate
            detection = state.get("detection_result", {})
            people = detection.get("data", {}).get("analysis", {}).get("people_detected", 0)
            
            if people == 0:
                people = state.get("people_affected_estimate", 20)
            
            # Get urgency from prediction
            prediction = state.get("prediction_result", {})
            urgency = prediction.get("data", {}).get("predictions", {}).get("urgency_level", "MEDIUM")
            
            result = await resource_agent.analyze(
                location=state.get("location", "Mumbai"),
                people_affected=people,
                severity=urgency
            )
            
            # Handle both dict and AgentResponse
            if hasattr(result, 'dict'):
                result_dict = result.dict()
            else:
                result_dict = result
            
            return {
                "resource_result": result_dict,
                "completed_steps": ["resource"],
                "current_step": "resource"
            }
            
        except Exception as e:
            return {
                "errors": [f"Resource failed: {str(e)}"],
                "completed_steps": ["resource"]
            }
    
    async def _communicate_node(self, state: DisasterState) -> Dict[str, Any]:
        """Node: Run Communication Agent"""
        try:
            print(f"📢 [Commander] Running Communication Agent...")
            
            result = await communication_agent.generate_report(
                weather_data=state.get("weather_result", {}),
                detection_data=state.get("detection_result", {}),
                prediction_data=state.get("prediction_result", {}),
                resource_data=state.get("resource_result", {}),
                incident_location=state.get("location", "Unknown")
            )
            
            # Handle both dict and AgentResponse
            if hasattr(result, 'dict'):
                result_dict = result.dict()
            else:
                result_dict = result
            
            return {
                "communication_result": result_dict,
                "final_report": result_dict.get("data", {}),
                "completed_steps": ["communicate"],
                "current_step": "communicate"
            }
            
        except Exception as e:
            return {
                "errors": [f"Communication failed: {str(e)}"],
                "completed_steps": ["communicate"]
            }
    
    async def _finalize_node(self, state: DisasterState) -> Dict[str, Any]:
        """Node: Finalize and summarize results"""
        print(f"✅ [Commander] Finalizing results...")
        
        # Calculate overall status
        errors = state.get("errors", [])
        completed = state.get("completed_steps", [])
        total_steps = ["weather", "detect", "predict", "resource", "communicate"]
        
        status = "COMPLETE" if len(completed) >= len(total_steps) else "PARTIAL"
        
        if errors:
            status = "ERROR"
        
        return {
            "current_step": "finalize",
            "execution_order": completed,
            "status": status,
            "errors": errors
        }
    
    async def analyze_incident(self, 
                               location: str,
                               image_path: Optional[str] = None,
                               people_affected_estimate: Optional[int] = None) -> Dict[str, Any]:
        """
        Main entry point - analyze a complete incident
        
        Args:
            location: Location of the incident
            image_path: Optional path to uploaded image
            people_affected_estimate: Optional manual estimate of people affected
            
        Returns:
            Complete incident analysis with report
        """
        print("\n" + "="*60)
        print(f"🚀 COMMANDER AGENT - Analyzing Incident at {location}")
        print("="*60 + "\n")
        
        # Initialize state
        initial_state: DisasterState = {
            "location": location,
            "image_path": image_path,
            "people_affected_estimate": people_affected_estimate,
            "weather_result": None,
            "detection_result": None,
            "prediction_result": None,
            "resource_result": None,
            "communication_result": None,
            "combined_risk_score": 0,
            "final_urgency": "MEDIUM",
            "final_report": None,
            "current_step": "init",
            "errors": [],
            "execution_order": [],
            "completed_steps": []
        }
        
        # Create config for LangGraph
        config = {"configurable": {"thread_id": f"incident_{datetime.now().timestamp()}"}}
        
        try:
            # Run the workflow
            final_state = await self.workflow.ainvoke(initial_state, config)
            
            # Extract results
            result = {
                "status": final_state.get("status", "COMPLETE"),
                "location": location,
                "urgency": final_state.get("final_urgency", "MEDIUM"),
                "risk_score": final_state.get("combined_risk_score", 0),
                "execution_order": final_state.get("execution_order", []),
                "errors": final_state.get("errors", []),
                "report": final_state.get("final_report", {}),
                "raw_data": {
                    "weather": final_state.get("weather_result", {}),
                    "detection": final_state.get("detection_result", {}),
                    "prediction": final_state.get("prediction_result", {}),
                    "resource": final_state.get("resource_result", {}),
                    "communication": final_state.get("communication_result", {})
                },
                "timestamp": datetime.now().isoformat()
            }
            
            print("\n" + "="*60)
            print("✅ INCIDENT ANALYSIS COMPLETE")
            print("="*60)
            print(f"📍 Location: {location}")
            print(f"🚨 Urgency: {result['urgency']}")
            print(f"📊 Risk Score: {result['risk_score']}")
            print(f"📋 Steps Executed: {len(result['execution_order'])}/5")
            print("="*60 + "\n")
            
            return result
            
        except Exception as e:
            print(f"❌ Commander Agent Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "status": "ERROR",
                "location": location,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Create singleton instance
commander_agent = CommanderAgent()