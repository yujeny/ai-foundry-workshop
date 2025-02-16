"""Trial Data Producer Module.

This module handles the generation and publishing of simulated clinical trial data
to Azure Event Hubs. It provides utilities for creating realistic trial events
with randomized patient data and vital signs.
"""

import json
import random
import asyncio
from typing import Optional, List
from datetime import datetime, timezone
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

from config import EVENT_HUBS_CONFIG

def generate_trial_event():
    """Generate a simulated trial event with random data."""
    return {
        "trialId": f"CTO{random.randint(1,1000):03d}",
        "patientId": f"P{random.randint(1,1000):03d}",
        "studyArm": random.choice(["Drug A", "Drug B", "Placebo"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "vitals": {
            "heartRate": random.randint(60, 100),
            "bloodPressure": f"{random.randint(110,140)}/{random.randint(60,90)}",
            "temperature": round(random.uniform(36.1, 37.2), 1),
            "respiratoryRate": random.randint(12, 20),
            "oxygenSaturation": random.randint(95, 100)
        },
        "adverseEvents": [
            {
                "type": random.choice(["Mild", "Moderate", "Severe"]),
                "description": random.choice([
                    "Headache",
                    "Nausea",
                    "Fatigue",
                    "Dizziness",
                    None,
                    None,
                    None
                ])
            }
        ] if random.random() < 0.3 else []
    }

async def simulate_trial_data(num_events: int = 1) -> list:
    """Generate and send simulated trial data to Event Hub.
    
    Args:
        num_events: Number of events to generate and send
        
    Returns:
        List of generated events
    """
    try:
        # Create producer client using connection string
        producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUBS_CONFIG["connection_string"]
        )
        
        # Generate events
        events = [generate_trial_event() for _ in range(num_events)]
        
        # Send events
        async with producer:
            event_data_batch = await producer.create_batch()
            
            for event in events:
                event_data = EventData(json.dumps(event))
                event_data_batch.add(event_data)
            
            await producer.send_batch(event_data_batch)
            
        return events
        
    except Exception as e:
        raise RuntimeError(f"Error simulating trial data: {str(e)}") from e

async def start_continuous_simulation(
    interval_seconds: float = 5.0,
    max_events: Optional[int] = None
) -> None:
    """Start continuous trial data simulation.
    
    Args:
        interval_seconds: Time between event batches
        max_events: Optional maximum number of events to generate
        
    This function runs indefinitely unless max_events is specified.
    """
    events_sent = 0
    try:
        while True:
            await simulate_trial_data()
            events_sent += 1
            
            if max_events and events_sent >= max_events:
                break
                
            await asyncio.sleep(interval_seconds)
            
    except asyncio.CancelledError:
        # Allow clean cancellation
        pass
    except Exception as e:
        raise RuntimeError(f"Error in continuous simulation: {str(e)}") from e
