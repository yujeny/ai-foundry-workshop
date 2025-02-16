"""
Trial Events Consumer
------------------
This module handles consuming and processing trial events from Azure Event Hubs.
It coordinates with other agents to process trial data and generate insights.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional
from azure.eventhub.aio import EventHubConsumerClient
from ...telemetry import tracer
import os
from .coordinator import TrialAgentCoordinator

class TrialEventsConsumer:
    def __init__(self, coordinator: TrialAgentCoordinator):
        self.coordinator = coordinator
        self.consumer = EventHubConsumerClient.from_connection_string(
            conn_str=os.getenv("EVENTHUB_CONNECTION_STRING"),
            consumer_group=os.getenv("CONSUMER_GROUP", "$Default"),
            eventhub_name=os.getenv("EVENTHUB_NAME")
        )
    
    async def process_event(self, event: Dict[str, Any]) -> None:
        """Process a single trial event using the multi-agent system."""
        with tracer.start_as_current_span("process_trial_event") as span:
            try:
                trial_id = event.get("trial_id")
                span.set_attribute("trial.id", trial_id)
                
                # Process event through multi-agent system
                analysis = await self.coordinator.process_trial_event(event)
                
                # Store or broadcast results as needed
                # This could integrate with a WebSocket for real-time updates
                
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise
    
    async def start_receiving(self) -> None:
        """Start receiving events from Event Hub."""
        with tracer.start_as_current_span("receive_trial_events") as span:
            try:
                async with self.consumer:
                    async def on_event(partition_context, event):
                        # Extract event data
                        event_data = json.loads(event.body_as_str())
                        await self.process_event(event_data)
                        await partition_context.update_checkpoint(event)
                    
                    await self.consumer.receive(
                        on_event=on_event,
                        starting_position="-1"  # Start from end
                    )
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise

    def close(self) -> None:
        """Close the consumer client."""
        if self.consumer:
            self.consumer.close()
