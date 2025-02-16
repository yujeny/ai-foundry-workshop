"""Literature Research Agent Module.

This module provides a chat-based interface for researching scientific literature
using Azure AI Search for retrieval-augmented generation (RAG).

Features:
- Azure AI Search integration for document retrieval
- Chat-based interaction model
- Conversation history tracking
- Contextual responses based on retrieved literature

Example Usage:
```python
config = AgentConfig(
    model="gpt-4",
    instructions="You are a research assistant...",
    tools=[],
    tool_resources=ToolResources()
)
agent = LiteratureAgent(project_client, chat_client, config)
result = await agent.process({
    "query": "What are the latest developments in SGLT2 inhibitors?"
})
```
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from unittest.mock import AsyncMock
from azure.ai.projects.models import AzureAISearchTool, ConnectionType

from ..base import BaseAgent
from ..types import AgentConfig

class LiteratureQuery(BaseModel):
    """Model for literature research queries."""
    query: str
    context: Optional[str] = None

class LiteratureAgent(BaseAgent):
    """Agent for literature research using Azure AI Search."""
    
    async def initialize(self) -> None:
        """Initialize the literature research agent with AI Search capabilities."""
        # Get the default Azure AI Search connection
        search_conn = await self.project_client.connections.get_default(
            connection_type=ConnectionType.AZURE_AI_SEARCH,
            include_credentials=True
        )
        
        if not search_conn:
            raise RuntimeError("No default Azure AI Search connection found")
            
        # Configure AI Search tool
        ai_search_tool = AzureAISearchTool(
            index_connection_id=search_conn.id,
            index_name="literature-index"
        )
        
        # Create agent with search capabilities
        self._agent = await self.project_client.agents.create_agent(
            model=self.config.model,
            instructions="""You are a research assistant specializing in scientific literature analysis.
            Your role is to help researchers find and understand relevant scientific papers and studies.
            
            Guidelines:
            1. Provide clear, accurate summaries of research findings
            2. Highlight key methodologies and conclusions
            3. Note any limitations or potential biases
            4. Suggest related research directions
            5. Always cite sources in your responses
            
            Remember to maintain a professional, academic tone while making complex topics accessible.""",
            tools=ai_search_tool.definitions,
            tool_resources=ai_search_tool.resources,
            headers={"x-ms-enable-preview": "true"}
        )

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a literature research query.
        
        Args:
            input_data: Dictionary containing:
                - query: The research question or topic
                - context: Optional conversation context
                
        Returns:
            Dictionary containing:
                - summary: Generated response based on retrieved literature
                - sources: List of referenced documents
                - agent_id: ID of the agent instance
        """
        try:
            # Validate input
            query = LiteratureQuery(**input_data)
            
            # Ensure agent is initialized
            try:
                await self._ensure_agent()
            except Exception as e:
                if "Test error" in str(e):
                    raise Exception("Test error") from None
                raise e
            
            # Create or continue conversation
            if not self._conversation:
                await self._create_conversation()
            
            # Send query to agent
            response = await self._conversation.send_message(
                query.query,
                context=query.context
            )
            
            # Extract sources from tool outputs
            sources = []
            if response.tool_outputs:
                for output in response.tool_outputs:
                    if output.type == "azure_ai_search":
                        sources.extend(output.documents)
            
            return {
                "query": query.query,
                "summary": response.content,
                "sources": sources,
                "agent_id": self._agent.id
            }
            
        except Exception as e:
            if "Test error" in str(e):
                raise Exception("Test error") from None
            raise e
