"""
Medication Analysis Agent
----------------------
This agent handles medication analysis and provides structured information
along with AI-generated explanations.

Features:
- Medication property analysis
- Side effect assessment
- Drug interaction warnings
- Medical disclaimers
"""

from typing import Dict, Any
import os
from ..base import BaseAgent
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class MedicationAgent(BaseAgent):
    """Agent for medication analysis and information retrieval."""
    
    async def initialize(self) -> None:
        """Initialize the medication agent."""
        self._agent = await self.project_client.agents.create_agent(
            model=self.config.model,
            instructions=self.config.instructions,
            tools=self.config.tools,
            tool_resources=self.config.tool_resources
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process medication analysis request.
        
        Args:
            input_data: Dict containing medication name and optional notes
            
        Returns:
            Dict containing structured info and AI-generated explanation
        """
        with tracer.start_as_current_span("medication_analysis") as span:
            try:
                await self._ensure_agent()
                await self._create_conversation()
                
                span.set_attribute("medication.name", input_data["name"])
                
                prompt = f"""Analyze this medication:
                Name: {input_data["name"]}
                Notes: {input_data.get("notes", "None provided")}
                
                Provide a comprehensive analysis including:
                1. Common uses and indications
                2. Mechanism of action
                3. Side effects (common and serious)
                4. Drug interactions
                5. Contraindications
                6. Special populations (elderly, pregnant, etc.)
                
                Format as a structured medical summary with appropriate disclaimers.
                """
                
                await self._ensure_agent()
                await self._create_conversation()
                if self._conversation:
                    response = await self._conversation.send_message(prompt)
                else:
                    raise Exception("Failed to create conversation")
                
                # Parse the response into structured sections
                # This is a simplified example - in production we'd use more robust parsing
                sections = response.content.split("\n\n")
                
                return {
                    "structured_info": {
                        "common_uses": sections[0] if len(sections) > 0 else "",
                        "mechanism": sections[1] if len(sections) > 1 else "",
                        "side_effects": sections[2] if len(sections) > 2 else "",
                        "interactions": sections[3] if len(sections) > 3 else "",
                        "contraindications": sections[4] if len(sections) > 4 else "",
                        "special_populations": sections[5] if len(sections) > 5 else ""
                    },
                    "ai_explanation": response.content,
                    "disclaimer": "This medication information is for educational purposes only. Always consult healthcare professionals for medical advice."
                }
            except Exception as e:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                span.record_exception(e)
                raise
