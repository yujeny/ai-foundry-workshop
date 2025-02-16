"""Azure AI client initialization module for drug discovery platform."""
import os
import logging
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import BingGroundingTool, ToolSet
from azure.identity import DefaultAzureCredential
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Initialize Azure AI clients
project_client = None
chat_client = None
toolset = None

async def init_clients():
    """Initialize Azure AI Projects and Chat clients."""
    global project_client, chat_client, toolset
    logger.info("🔧 Initializing Azure AI clients")
    
    try:
        # Initialize Azure credentials using DefaultAzureCredential
        credential = DefaultAzureCredential()
        
        # Initialize project client with connection string
        logger.info("🔧 Initializing project client")
        project_client = AIProjectClient.from_connection_string(
            credential=credential,
            conn_str=os.getenv("PROJECT_CONNECTION_STRING")
        )
        
        # Get chat client from project client
        logger.info("🔧 Initializing chat client")
        chat_client = project_client.inference.get_chat_completions_client()
        
        # Initialize toolset
        logger.info("🔧 Initializing toolset")
        toolset = ToolSet()
        bing_tool = BingGroundingTool(
            connection_id=os.getenv("BING_API_KEY")
        )
        toolset.add(bing_tool)
        
        # Log successful initialization
        logger.info(f"""✨ Successfully initialized Azure AI clients:
        Project Client: {type(project_client).__name__}
        Chat Client: {type(chat_client).__name__}
        Tools: {[type(tool).__name__ for tool in toolset._tools]}""")
        
        return project_client, chat_client, toolset
        
    except Exception as e:
        logger.error(f"❌ Error initializing Azure AI clients: {str(e)}")
        raise

async def ensure_clients():
    """Ensure clients are initialized."""
    global project_client, chat_client, toolset
    if project_client is None or chat_client is None:
        project_client, chat_client, toolset = await init_clients()

__all__ = ['project_client', 'chat_client', 'toolset', 'tracer', 'ensure_clients']
