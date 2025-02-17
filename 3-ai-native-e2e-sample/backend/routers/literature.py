from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AzureAISearchTool
from azure.identity import DefaultAzureCredential
from ..agents.literature import LiteratureChatHandler
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/agents/literature-chat")
async def chat_literature(message: str):
    """
    Stream chat responses about literature using AI Search.
    
    Args:
        message: The user's chat message
        
    Returns:
        StreamingResponse: Server-sent events stream of chat responses
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        # Initialize AI Project client
        project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=os.environ["PROJECT_CONNECTION_STRING"]
        )
        
        # Get AI Search connection
        search_conn = project_client.connections.get_default(
            connection_type="AZURE_AI_SEARCH",
            include_credentials=True
        )
        if not search_conn:
            raise ValueError("No default Azure AI Search connection found")
        
        # Configure AI Search tool
        ai_search_tool = AzureAISearchTool(
            index_connection_id=search_conn.id,
            index_name="literature-index"
        )
        
        # Create chat agent
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="literature-chat",
            instructions="""You are a Literature Research Assistant. Help users find and understand scientific literature.
            Use the search tool to find relevant papers and provide evidence-based responses.
            Always cite your sources and provide context for your answers.""",
            tools=ai_search_tool.definitions,
            tool_resources=ai_search_tool.resources,
            headers={"x-ms-enable-preview": "true"}
        )
        logger.info(f"Created agent with ID: {agent.id}")
        
        # Create thread and message
        thread = project_client.agents.create_thread()
        logger.info(f"Created thread with ID: {thread.id}")
        
        message_obj = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=message
        )
        logger.info(f"Created message with ID: {message_obj.id}")
        
        # Create streaming response
        stream = project_client.agents.create_stream(
            thread_id=thread.id,
            assistant_id=agent.id,
            event_handler=LiteratureChatHandler()
        )
        
        return StreamingResponse(
            stream,
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Error in literature chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process literature chat: {str(e)}"
        )
