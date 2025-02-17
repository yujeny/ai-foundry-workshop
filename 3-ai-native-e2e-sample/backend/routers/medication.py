from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import BingGroundingTool, FunctionTool, RunStatus, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput
from azure.identity import DefaultAzureCredential
from agents.medication import MedicationChatHandler
from agents.medication_functions import medication_functions
import os
import logging
import json
import time
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agents", tags=["medication"])

class MedicationInfo(BaseModel):
    name: str
    notes: Optional[str] = None

class MedicationAnalysis(BaseModel):
    analysis: str
    interactions: list[str]
    warnings: list[str]
    recommendations: list[str]

@router.post("/medication/analyze")
async def analyze_medication(info: MedicationInfo):
    """
    Analyze medication information using AI agents with Bing grounding.
    """
    try:
        logger.info(f"Starting medication analysis for: {info.name}")
        
        # Initialize AI Project client
        project_client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=os.environ["PROJECT_CONNECTION_STRING"]
        )
        logger.info("AI Project client initialized")
        
        # Get Bing connection
        bing_conn = project_client.connections.get(
            connection_name=os.environ["BING_CONNECTION_NAME"]
        )
        if not bing_conn:
            raise ValueError("No Bing connection found with specified name")
        logger.info(f"Got Bing connection with ID: {bing_conn.id}")
        
        # Configure tools
        bing_tool = BingGroundingTool(connection_id=bing_conn.id)
        functions = FunctionTool(functions=medication_functions)
        
        # Create agent with both tools
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="medication-analysis",
            instructions="""You are a medication information assistant.
            Use Bing to find accurate, up-to-date information about medications.
            ALWAYS use the analyze_medication_info function to structure your responses.
            The function will return a JSON string that you should return directly without modification.
            Do not format the response as markdown or add any additional text.""",
            tools=[*bing_tool.definitions, *functions.definitions],
            headers={"x-ms-enable-preview": "true"}
        )
        logger.info(f"Created agent with ID: {agent.id}")
        
        # Create thread and message
        thread = project_client.agents.create_thread()
        logger.info(f"Created thread with ID: {thread.id}")
        
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"Analyze the medication: {info.name}. Return the analysis using the analyze_medication_info function. {info.notes if info.notes else ''}"
        )
        logger.info(f"Created message with ID: {message.id}")

        # Create run
        run = project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)
        logger.info(f"Created run with ID: {run.id}")

        # Poll for run completion
        max_retries = 60
        retry_count = 0
        
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)
            logger.info(f"Current run status: {run.status}")

            if run.status == "requires_action" and isinstance(run.required_action, SubmitToolOutputsAction):
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    logger.error("No tool calls provided")
                    break

                tool_outputs = []
                for tool_call in tool_calls:
                    if isinstance(tool_call, RequiredFunctionToolCall):
                        try:
                            logger.info(f"Executing tool call: {tool_call.function.name}")
                            output = functions.execute(tool_call)
                            tool_outputs.append(
                                ToolOutput(
                                    tool_call_id=tool_call.id,
                                    output=output
                                )
                            )
                            logger.info(f"Tool output: {output}")
                        except Exception as e:
                            logger.error(f"Error executing tool call: {e}")

                if tool_outputs:
                    run = project_client.agents.submit_tool_outputs_to_run(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    continue

            retry_count += 1
            if retry_count >= max_retries:
                raise HTTPException(status_code=500, detail="Run timed out")

        if run.status == "failed":
            logger.error(f"Run failed: {run.last_error}")
            raise HTTPException(status_code=500, detail=str(run.last_error))

        # Get messages after run completion
        messages = project_client.agents.list_messages(thread_id=thread.id)
        logger.info(f"Got {len(messages.data)} messages")
        
        # Get the latest assistant message
        for msg in reversed(messages.data):
            logger.info(f"Processing message with role: {msg.role}")
            if msg.role == "assistant":
                for content in msg.content:
                    logger.info(f"Content type: {type(content)}")
                    if hasattr(content, 'text') and content.text:
                        logger.info(f"Message content: {content.text.value}")
                        try:
                            # Try to extract JSON from the message
                            text = content.text.value
                            # If the response is markdown, try to find JSON in it
                            if text.startswith('```json'):
                                text = text.split('```json')[1].split('```')[0].strip()
                            elif text.startswith('{'):
                                text = text.strip()
                            
                            result = json.loads(text)
                            return MedicationAnalysis(
                                analysis=result.get("analysis", ""),
                                interactions=result.get("interactions", []),
                                warnings=result.get("warnings", []),
                                recommendations=result.get("recommendations", [])
                            )
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse JSON: {e}")
                            logger.error(f"Raw text: {text}")
                            continue

        raise HTTPException(status_code=500, detail="No valid response received from AI")
        
    except Exception as e:
        logger.error(f"Error in medication analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze medication: {str(e)}"
        )
