"""
Shared Utilities for AI Agents
-----------------------------
This module provides common utilities and helper functions used across
different agent implementations in the drug discovery platform.

Key Components:
- Tool configuration helpers
- Response formatting utilities
- Common type definitions
"""

from typing import Dict, Any, List, Tuple, Optional, Callable, Union
from azure.ai.projects.models import ToolSet, BingGroundingTool, FunctionTool, CodeInterpreterTool
import os
import logging
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

def convert_numpy_types(obj: Any) -> Union[Dict, List, int, float, str, Any]:
    """Convert numpy types to Python native types.
    
    This function recursively converts numpy numeric types to their Python
    equivalents to ensure JSON serialization works correctly.
    
    Args:
        obj: Any Python or numpy object to convert
        
    Returns:
        The converted object with numpy types replaced by Python types
    """
    try:
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_numpy_types(x) for x in obj]
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, (int, float)):
            return obj
        elif obj is None:
            return None
        return str(obj)
    except Exception as e:
        logger.error(f"Error converting numpy types: {str(e)}")
        return str(obj)

def format_agent_response(
    response_content: str,
    agent_id: str,
    **additional_fields: Any
) -> Dict[str, Any]:
    """Format a standardized agent response.
    
    Args:
        response_content: The main content from the agent
        agent_id: The ID of the agent that generated the response
        **additional_fields: Any additional fields to include
        
    Returns:
        Dict[str, Any]: Formatted response with standard fields
    """
    return {
        "content": response_content,
        "agent_id": agent_id,
        **additional_fields
    }

def create_tool_config(
    bing_connection_id: Optional[str] = None,
    functions: Optional[List[Callable[..., Any]]] = None,
    code_interpreter: bool = False,
    file_ids: Optional[List[str]] = None
) -> Tuple[ToolSet, Dict[str, Any]]:
    """Create a standardized tool configuration for agents.
    
    This function creates a consistent tool configuration across different
    agent types, handling Bing grounding, function calling, and code
    interpreter capabilities.
    
    Args:
        bing_connection_id: Optional Bing API connection ID for grounding
        functions: Optional list of functions to expose to the agent
        code_interpreter: Whether to add code interpreter capability
        file_ids: Optional list of file IDs for code interpreter
        
    Returns:
        Tuple[ToolSet, Dict[str, Any]]: The configured toolset and resources
        
    Example:
        ```python
        def analyze_data(data: dict) -> dict:
            return {"result": "analysis"}
            
        toolset, resources = create_tool_config(
            bing_connection_id=os.getenv("BING_API_KEY"),
            functions=[analyze_data],
            code_interpreter=True
        )
        ```
    """
    logger.info("🔧 Creating tool configuration")
    toolset = ToolSet()
    resources = {
        "functions": [],
        "file_ids": file_ids or [],
        "connection_id": bing_connection_id
    }
    
    # Add Bing grounding if connection ID provided
    if bing_connection_id:
        logger.debug("Adding Bing grounding tool")
        bing_tool = BingGroundingTool(
            connection_id=bing_connection_id,
            settings={
                "search_parameters": {
                    "count": 5,
                    "textDecorations": True,
                    "textFormat": "HTML"
                }
            }
        )
        toolset.add(bing_tool)
        
    # Add function calling if functions provided
    if functions:
        logger.debug(f"Adding function tool with {len(functions)} functions")
        function_tool = FunctionTool(functions=functions)
        toolset.add(function_tool)
        resources["functions"].extend([f.__name__ for f in functions])
        
    # Add code interpreter if requested
    if code_interpreter:
        logger.debug("Adding code interpreter tool")
        code_tool = CodeInterpreterTool()
        toolset.add(code_tool)
        
    logger.info("✅ Tool configuration created successfully")
    return toolset, resources
