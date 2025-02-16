from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import os
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from agents.medication import MedicationAgent
from clients import project_client, chat_client, tracer
from agents.types import AgentConfig
from agents.types import AgentConfig

class MedicationRequest(BaseModel):
    name: str
    notes: Optional[str] = None

router = APIRouter(tags=["medications"])

@router.post("/analyze")
async def analyze_medication(request: MedicationRequest):
    """
    Analyze medication properties and provide structured information.
    
    This endpoint provides:
    - 💊 Common uses and indications
    - 🔬 Mechanism of action
    - ⚠️ Side effects and interactions
    - 👥 Special population considerations
    - 📋 Medical disclaimers
    """
    with tracer.start_as_current_span("analyze_medication") as span:
        try:
            span.set_attribute("medication.name", request.name)
            
            config = AgentConfig(
                model=os.getenv("MODEL_DEPLOYMENT_NAME"),
                instructions="You are a medical information assistant. Provide accurate, structured information about medications with appropriate medical disclaimers.",
                tools=[],
                tool_resources=None
            )
            
            agent = MedicationAgent(project_client, chat_client, config)
            result = await agent.process({
                "name": request.name,
                "notes": request.notes
            })
            
            return result
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing medication: {str(e)}"
            )
