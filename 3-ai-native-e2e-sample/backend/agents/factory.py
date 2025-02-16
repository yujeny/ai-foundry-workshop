"""
Agent Factory Module
------------------
This module provides a factory class for creating and managing AI agents
in the drug discovery platform. It handles agent caching and initialization
to improve performance and resource utilization.

Key Components:
- AgentFactory: Main factory class for agent creation and caching
- Agent type management and validation
- Standardized agent configuration
"""

from typing import Dict, Any, Optional, List
import os
import logging
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from .types import AgentConfig, ToolResources
from .utils import create_tool_config
from azure.ai.projects.models import ToolSet

# Configure logging
logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory for creating and caching AI agents.
    
    This class manages the lifecycle of AI agents, including creation,
    caching, and configuration. It ensures consistent agent setup across
    different agent types.
    
    Attributes:
        _project_client: Azure AI Projects client
        _chat_client: Azure OpenAI chat client
        _cache: Dictionary storing agent instances
    """
    
    def __init__(
        self,
        project_client: AIProjectClient,
        chat_client: ChatCompletionsClient
    ):
        """Initialize the agent factory.
        
        Args:
            project_client: Azure AI Projects client
            chat_client: Azure OpenAI chat client
        """
        logger.info("🏭 Initializing AgentFactory")
        self._project_client = project_client
        self._chat_client = chat_client
        self._cache: Dict[str, Any] = {}
        logger.debug("Project client: %s", "initialized" if project_client else "not initialized")
        logger.debug("Chat client: %s", "initialized" if chat_client else "not initialized")
        
    async def get_or_create_agent(
        self,
        agent_type: str,
        config: AgentConfig
    ) -> Any:
        """Get an agent from cache or create a new one.
        
        This method first checks the cache for an existing agent of the
        specified type. If not found, it creates a new agent using the
        provided configuration.
        
        Args:
            agent_type: Type identifier for the agent
            config: Configuration for agent creation
            
        Returns:
            The agent instance
            
        Example:
            ```python
            config = AgentConfig(
                model="gpt-4",
                instructions="Analyze scientific literature",
                tools=[...],
                tool_resources=ToolResources(...)
            )
            agent = await factory.get_or_create_agent("literature", config)
            ```
        """
        logger.info(f"🔄 Getting or creating agent of type: {agent_type}")
        
        if agent_type not in self._cache:
            logger.debug(f"Creating new {agent_type} agent")
            try:
                agent = await self._project_client.agents.create_agent(
                    model=config.model,
                    instructions=config.instructions,
                    tools=config.tools,
                    tool_resources=config.tool_resources.dict(),
                    headers={"x-ms-enable-preview": "true"}
                )
                self._cache[agent_type] = agent
                logger.info(f"✅ Created new {agent_type} agent")
            except Exception as e:
                logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                raise
        
        return self._cache[agent_type]
    
    def get_chat_client(self) -> ChatCompletionsClient:
        """Get the chat completions client.
        
        Returns:
            The Azure OpenAI chat client
        """
        return self._chat_client
    
    async def create_conversation(self, agent: Any) -> Any:
        """Create a new conversation with an agent.
        
        Args:
            agent: The agent to create a conversation with
            
        Returns:
            The created conversation
        """
        logger.info("🗣️ Creating new conversation")
        return await self._chat_client.create_conversation(agent_id=agent.id)

    def get_tools(self) -> List[ToolSet]:
        """Get available tools for agents."""
        logger.debug("Getting tools from project client")
        try:
            tools = self._project_client.list_tools()
            logger.debug("Available tools: %s", tools)
            return tools
        except Exception as e:
            logger.error("Failed to get tools: %s", str(e), exc_info=True)
            raise
