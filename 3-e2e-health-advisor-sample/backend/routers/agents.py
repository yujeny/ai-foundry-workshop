from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.tables import DrugCandidateTable
from datetime import datetime
import logging
import os
from main import inference_client, tracer

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["agents"])

@router.post("/demo-agent")
async def demo_agent_interaction():
    """
    ### 🤖 Demo Agent Interaction

    👩‍🔬 This endpoint demonstrates how an Azure AI Foundry Agent can be used to perform
    advanced drug design tasks.

    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        Client->>Agent: Create Thread & Message
        Agent->>Agent: Process AI
        Agent-->>Client: Respond
    ```
    """
    with tracer.start_as_current_span("demo_agent_interaction") as span:
        try:
            span.set_attribute("operation", "agent_demo")
            logger.info("🚀 Starting agent demo interaction")

            # Create a chat completion request
            response = inference_client.chat.completions.create(
                model=os.getenv('MODEL_DEPLOYMENT_NAME'),
                messages=[
                    {"role": "system", "content": "You are an AI agent specialized in drug development analysis."},
                    {"role": "user", "content": "Analyze the potential of a new drug candidate for cancer treatment"}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Extract the response
            agent_response = response.choices[0].message.content
            
            logger.info("✅ Agent demo interaction complete")
            return {
                "message": "Agent interaction demo complete",
                "agent_id": "drug-analysis-agent",
                "response": agent_response
            }
            
        except Exception as e:
            logger.error(f"❌ Error in agent demo: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in agent demo: {str(e)}"
            )
