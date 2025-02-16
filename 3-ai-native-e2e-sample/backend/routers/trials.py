from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
import logging
from utils.telemetry import tracer, Status, StatusCode

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/simulate")
async def simulate_trial_data():
    """Simulate clinical trial data."""
    with tracer.start_as_current_span("simulate_trial_data") as span:
        try:
            logger.info("🔄 Starting trial data simulation")
            logger.debug("Generating trial ID...")
            trial_id = f"CT-{uuid.uuid4().hex[:8]}"
            logger.debug("Generated trial ID: %s", trial_id)
            
            # Generate mock trial data
            trial_data = {
                "trials": [
                    {
                        "id": trial_id,
                        "phase": 2,
                        "status": "Recruiting",
                        "startDate": datetime.now().isoformat(),
                        "completionDate": None,
                        "participants": 250,
                        "conditions": ["Type 2 Diabetes", "Hypertension"],
                        "interventions": ["Drug A", "Placebo"]
                    }
                ],
                "totalTrials": 1,
                "page": 1,
                "pageSize": 10
            }
            
            logger.debug("Generated trial data: %s", trial_data)
            logger.info("✅ Trial data simulation completed for trial %s", trial_id)
            return trial_data
            
        except Exception as e:
            logger.error("❌ Error in trial data simulation: %s", str(e), exc_info=True)
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
