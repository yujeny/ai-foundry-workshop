from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
import json
import logging
from azure.eventhub import EventHubProducerClient, EventData
from config import EVENT_HUBS_CONFIG

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["trials"])

def generate_mock_trial_data():
    """Generate mock trial data for simulation."""
    return {
        "phase": 2,
        "status": "active",
        "participants": 250,
        "conditions": ["Type 2 Diabetes", "Hypertension"],
        "interventions": ["Drug A", "Placebo"],
        "metrics": {
            "efficacy": 0.75,
            "safety": 0.92,
            "adherence": 0.88
        }
    }

@router.post("/simulate")
async def simulate_trial_data():
    """
    ### 📊 Simulate Clinical Trial Data
    
    Generates simulated trial data and sends it to Azure Event Hubs
    for real-time processing and analysis.
    
    #### Process Flow
    1. Generate mock trial data
    2. Send event to Azure Event Hubs
    3. Return simulation status
    
    Returns:
        dict: Status and message indicating simulation started
    """
    try:
        logger.info("🔄 Starting trial data simulation")
        
        # Create Event Hubs producer
        producer = EventHubProducerClient(
            fully_qualified_namespace=EVENT_HUBS_CONFIG["fully_qualified_namespace"],
            eventhub_name=EVENT_HUBS_CONFIG["eventhub_name"],
            credential=EVENT_HUBS_CONFIG["credential"]
        )
        
        # Generate and send event
        async with producer:
            event_data_batch = await producer.create_batch()
            
            # Create event with mock data
            event = {
                "trial_id": f"TRIAL_{uuid.uuid4()}",
                "timestamp": datetime.now().isoformat(),
                "data": generate_mock_trial_data()
            }
            
            # Add event to batch
            event_data_batch.add(EventData(json.dumps(event)))
            
            # Send batch to Event Hubs
            await producer.send_batch(event_data_batch)
            
            logger.info("✅ Trial data simulation event sent successfully")
            return {
                "status": "success",
                "message": "Trial data simulation started",
                "trial_id": event["trial_id"]
            }
            
    except Exception as e:
        logger.error(f"❌ Error in trial data simulation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error simulating trial data: {str(e)}"
        )
