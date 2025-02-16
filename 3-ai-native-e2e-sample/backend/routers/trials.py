from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import logging
from opentelemetry import trace
from agents.trials.event_producer.producer import simulate_trial_data

# Configure logging and tracing
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()

@router.post("/simulate")
async def simulate_trial_events(num_events: int = Query(default=1, ge=1, le=100)):
    """
    Simulate clinical trial events.
    
    Args:
        num_events: Number of events to generate (1-100)
        
    Returns:
        List of generated trial events
    """
    with tracer.start_as_current_span("simulate_trial_events") as span:
        try:
            logger.info("🔄 Starting trial event simulation for %d events", num_events)
            span.set_attribute("trial.num_events", num_events)
            
            # Generate and publish events
            events = await simulate_trial_data(num_events)
            
            logger.info("✅ Trial event simulation completed")
            span.set_attribute("trial.events_generated", len(events))
            return {
                "status": "success",
                "message": f"Generated and published {len(events)} trial events",
                "events": events
            }
            
        except Exception as e:
            logger.error("❌ Error in trial event simulation: %s", str(e), exc_info=True)
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            span.record_exception(e)
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
