"""
Trial Events Consumer
------------------
This module handles consuming and processing trial events from Azure Event Hubs.
It coordinates with the multi-agent system to analyze trial data and generate insights.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from azure.eventhub.aio import EventHubConsumerClient
from opentelemetry import trace
from utils.telemetry import tracer
import os
from .coordinator import TrialAgentCoordinator
from config import EVENT_HUBS_CONFIG

logger = logging.getLogger(__name__)

class TrialEventsConsumer:
    """Consumes trial events and processes them through the multi-agent system."""
    
    def __init__(self, coordinator: TrialAgentCoordinator):
        """Initialize the consumer with a coordinator.
        
        Args:
            coordinator: The multi-agent coordinator for processing events
        """
        self.coordinator = coordinator
        self.consumer = EventHubConsumerClient.from_connection_string(
            conn_str=EVENT_HUBS_CONFIG["connection_string"],
            consumer_group=EVENT_HUBS_CONFIG["consumer_group"],
            eventhub_name=EVENT_HUBS_CONFIG["eventhub_name"]
        )
        logger.info("✅ Trial events consumer initialized")
    
    async def process_event(self, event: Dict[str, Any]) -> None:
        """Process a single trial event using the multi-agent system.
        
        Args:
            event: The trial event data to process
        """
        with tracer.start_as_current_span("process_trial_event") as span:
            try:
                trial_id = event.get("trialId")
                span.set_attribute("trial.id", trial_id)
                logger.info("🔄 Processing trial event: %s", trial_id)
                
                # Process event through multi-agent system
                analysis = await self.coordinator.process_trial_event(event)
                
                # Log analysis results
                logger.info("✅ Analysis completed for trial: %s", trial_id)
                logger.debug("Analysis results: %s", analysis)
                span.set_attribute("analysis.completed", True)
                
            except Exception as e:
                logger.error("❌ Error processing trial event: %s", str(e), exc_info=True)
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise
    
    async def start_receiving(self) -> None:
        """Start receiving events from Event Hub."""
        with tracer.start_as_current_span("receive_trial_events") as span:
            try:
                logger.info("🎯 Starting trial event consumer")
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
                logger.error("❌ Error in event consumer: %s", str(e), exc_info=True)
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise

    def close(self) -> None:
        """Close the consumer client."""
        if self.consumer:
            logger.info("🛑 Closing trial event consumer")
            self.consumer.close()
