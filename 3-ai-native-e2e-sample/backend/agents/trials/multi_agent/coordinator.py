from typing import Dict, Any, List
from azure.ai.projects import AIProjectClient
from azure.ai.inference import InferenceClient
from opentelemetry import trace
from utils.telemetry import tracer

class TrialAgentCoordinator:
    def __init__(self, project_client: AIProjectClient, inference_client: InferenceClient):
        self.project_client = project_client
        self.inference_client = inference_client
        self.agents = {}

    async def initialize_agents(self):
        """Initialize the team of specialized agents."""
        with tracer.start_as_current_span("initialize_trial_agents") as span:
            try:
                # Create Team Leader
                self.agents["team_leader"] = await self.project_client.agents.create_agent(
                    model="gpt-4o",
                    instructions="""You are the Team Leader agent coordinating trial analysis.
                    Analyze incoming trial events and delegate tasks to specialized agents."""
                )

                # Create specialized agents
                agent_specs = {
                    "vitals": "Analyze patient vital signs and identify anomalies",
                    "adverse_events": "Monitor and assess adverse events",
                    "data_summary": "Aggregate and summarize trial data trends"
                }

                for agent_id, instructions in agent_specs.items():
                    self.agents[agent_id] = await self.project_client.agents.create_agent(
                        model="gpt-4o",
                        instructions=instructions
                    )

                span.set_attribute("agents.initialized", len(self.agents))
                return True

            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise

    async def process_trial_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Process a trial event through the multi-agent system."""
        with tracer.start_as_current_span("process_trial_event") as span:
            try:
                # Team Leader analyzes event
                leader_response = await self._delegate_tasks(event)
                
                # Aggregate responses
                analysis = {
                    "event_id": event.get("id"),
                    "timestamp": event.get("timestamp"),
                    "analysis": leader_response,
                    "recommendations": []
                }

                span.set_attribute("event.processed", True)
                return analysis

            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise

    async def _delegate_tasks(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Team Leader delegates tasks to specialized agents."""
        with tracer.start_as_current_span("delegate_trial_tasks") as span:
            try:
                # Collect responses from specialized agents
                responses = {}
                
                # Process vitals
                if "vitals" in event:
                    vitals_response = await self.agents["vitals"].process_message(
                        f"Analyze these vital signs: {event['vitals']}"
                    )
                    responses["vitals_analysis"] = vitals_response
                
                # Process adverse events
                if "adverseEvents" in event and event["adverseEvents"]:
                    adverse_response = await self.agents["adverse_events"].process_message(
                        f"Assess these adverse events: {event['adverseEvents']}"
                    )
                    responses["adverse_events_analysis"] = adverse_response
                
                # Generate summary
                summary_response = await self.agents["data_summary"].process_message(
                    f"Summarize this trial event data: {event}"
                )
                responses["summary"] = summary_response
                
                span.set_attribute("tasks.completed", len(responses))
                return responses
                
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise   