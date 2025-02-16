"""
Common Type Definitions for AI Agents
----------------------------------
This module defines shared type definitions and interfaces used
across different agent implementations.
"""

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel

class AgentResponse(BaseModel):
    """Base model for agent responses."""
    agent_id: str
    content: str
    
class ToolResources(BaseModel):
    """Configuration for agent tool resources."""
    functions: List[str] = []
    file_ids: List[str] = []
    connection_id: Optional[str] = None

class AgentConfig(BaseModel):
    """Configuration for an AI agent."""
    model: str
    instructions: str
    tools: List[Dict[str, Any]]
    tool_resources: ToolResources
