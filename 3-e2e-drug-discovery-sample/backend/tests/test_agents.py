import pytest
import numpy as np
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app
from models import DrugCandidate, ClinicalTrial, AutomatedTest, TestResult
import os
from fastapi import FastAPI
from typing import AsyncGenerator, Generator
from datetime import datetime, timedelta
from azure.ai.projects.models import BingGroundingTool, FunctionTool, CodeInterpreterTool, ToolSet

# Configure test environment
os.environ["TEST_MODE"] = "true"

@pytest.fixture(scope="module")
def test_app() -> FastAPI:
    """Create a test FastAPI app."""
    return app

@pytest.fixture(scope="module")
def client(test_app: FastAPI) -> Generator:
    """Create a test client."""
    test_client = TestClient(test_app)
    yield test_client

import pytest_asyncio

@pytest_asyncio.fixture(scope="module")
async def async_client(test_app: FastAPI) -> AsyncClient:
    """Create an async test client."""
    client = AsyncClient(app=test_app, base_url="http://test")
    yield client
    await client.aclose()
from clients import project_client, chat_client, toolset
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import json

# Mock message creator
def create_mock_message(content):
    """Create a mock message with the given content."""
    return Mock(
        message=Mock(
            content=content,
            role="assistant",
            tool_calls=[],
            function_calls=[]
        ),
        choices=[],
        model=os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4"),
        usage=Mock(total_tokens=100, prompt_tokens=50, completion_tokens=50)
    )

# Mock response generator factory
def create_mock_response_handler(mock_agents_dict, mock_conv):
    """Create a mock response handler with access to agents and conversation."""
    # Define agent IDs and names mapping
    endpoint_to_agent = {
        "literature-search": ("literature-search", "agent-1111"),
        "molecule-analysis": ("molecule-analysis", "agent-2222"),
        "trial-data-analysis": ("trial-data-analysis", "agent-3333"),
        "drug-repurpose": ("drug-repurpose", "agent-1122"),
        "manufacturing-opt": ("manufacturing-opt", "agent-2001"),
        "precision-med": ("precision-med", "agent-3002"),
        "digital-twin-sim": ("digital-twin-sim", "agent-5000")
    }
    
    def get_mock_response(message):
        """Generate mock responses based on agent type."""
        # Get agent ID from the conversation context
        agent_id = mock_conv.agent_id
        agent_name = next(
            (name for name, (_, id_val) in endpoint_to_agent.items() if id_val == agent_id),
            "unknown"
        )
        
        # Define response templates
        responses = {
            "literature-search": {
                "query": "EGFR inhibitors in lung cancer",
                "summary": "Recent research shows promising results...",
                "references": ["DOI:10.1234/..."]
            },
            "molecule-analysis": {
                "molecule": "CC1=CC=C(C=C1)NC(=O)C2=CC=C(Cl)C=C2",
                "analysis": {
                    "binding_predictions": {"EGFR": 0.85, "HER2": 0.76},
                    "drug_likeness": 0.92,
                    "safety_assessment": "Low toxicity profile"
                }
            },
            "trial-data-analysis": {
                "filename": "test_data.csv",
                "analysis": {
                    "correlations": {"age": 0.45, "biomarker_a": 0.78},
                    "summary": "Strong correlation found...",
                    "recommendations": ["Focus on biomarker_a", "Stratify by age"]
                }
            },
            "drug-repurpose": {
                "repurposing_opportunities": [{
                    "disease": "RareAutoimmuneXYZ",
                    "confidence": 0.89,
                    "supporting_sources": ["DOI:10.1234/..."]
                }]
            },
            "manufacturing-opt": {
                "optimized_schedule": {
                    "batch_size": 1000,
                    "line_allocation": "FactoryA",
                    "estimated_unit_cost": 2.45
                }
            },
            "precision-med": {
                "patient_id": "PAT-007",
                "custom_dosage": "120 mg daily",
                "predicted_outcome": 0.93,
                "recommended_followups": ["Monthly biomarker profiling"]
            },
            "digital-twin-sim": {
                "simulated_population_size": 10000,
                "mean_toxicity_score": 0.12,
                "average_survival_gain": "6 months"
            }
        }
        
        # Get response template or use default
        response_data = responses.get(agent_name, {"error": "Unknown agent type"})
        response_data["agent_id"] = agent_id
        
        return create_mock_message(json.dumps(response_data))
    return get_mock_response

# Mock Azure clients
# Create mock message object

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock all external dependencies."""
    with patch("azure.ai.projects.AIProjectClient") as mock_project_client, \
         patch("azure.ai.inference.ChatCompletionsClient") as mock_chat_client, \
         patch("azure.identity.DefaultAzureCredential") as mock_credential, \
         patch("azure.ai.projects.models.BingGroundingTool") as mock_bing_tool, \
         patch("azure.ai.projects.models.FunctionTool") as mock_function_tool, \
         patch("azure.ai.projects.models.CodeInterpreterTool") as mock_code_tool, \
         patch("opentelemetry.trace") as mock_trace:
        
        # Setup mock agents for different endpoints with proper tool configurations
        endpoint_to_agent = {
            "literature-search": ("Literature Search Agent", "agent-1111"),
            "molecule-analysis": ("Molecule Analysis Agent", "agent-2222"),
            "trial-data-analysis": ("Trial Data Analysis Agent", "agent-3333"),
            "drug-repurpose": ("Drug Repurposing Agent", "agent-1122"),
            "manufacturing-opt": ("Manufacturing Optimization Agent", "agent-2001"),
            "precision-med": ("Precision Medicine Agent", "agent-3002"),
            "digital-twin-sim": ("Digital Twin Simulation Agent", "agent-5000")
        }
        
        mock_agents = {}
        for endpoint_type, (name, agent_id) in endpoint_to_agent.items():
            # Configure tools based on endpoint type
            tools = []
            tool_resources = {
                "connection_id": os.getenv("spn_4o_BING_API_KEY"),
                "functions": [],
                "file_ids": ["test-file-id"]
            }
            
            # Add Bing grounding for literature search and drug repurposing
            if endpoint_type in ["literature-search", "drug-repurpose", "precision-med"]:
                # Create mock BingGroundingTool with proper configuration
                mock_bing_tool = Mock(spec=BingGroundingTool)
                mock_bing_tool.connection_id = os.getenv("spn_4o_BING_API_KEY")
                mock_bing_tool.type = "bing-grounding"
                mock_bing_tool.name = "bing-grounding"
                # Create settings as a Mock object with proper attributes
                mock_settings = Mock()
                mock_settings.search_parameters = {
                    "count": 5,
                    "textDecorations": True,
                    "textFormat": "HTML"
                }
                mock_settings.file_search = {
                    "query": "",
                    "results": [],
                    "file_ids": [],
                    "search_mode": "semantic"
                }
                mock_bing_tool.settings = mock_settings
                tools.append(mock_bing_tool)
            
            # Add function calling for all endpoints
            mock_function_tool = Mock(spec=FunctionTool)
            mock_function_tool.type = "function"
            mock_function_tool.name = "function"
            # Create settings as a Mock object with proper attributes
            mock_settings = Mock()
            mock_settings.functions = []
            mock_settings.file_search = {
                "query": "",
                "results": [],
                "file_ids": [],
                "search_mode": "semantic"
            }
            mock_function_tool.settings = mock_settings
            tools.append(mock_function_tool)
            
            # Add code interpreter for manufacturing and digital twin
            if endpoint_type in ["manufacturing-opt", "digital-twin-sim"]:
                mock_code_tool = Mock(spec=CodeInterpreterTool)
                mock_code_tool.type = "code_interpreter"
                mock_code_tool.name = "code_interpreter"
                # Create settings as a Mock object with proper attributes
                mock_settings = Mock()
                mock_settings.file_ids = ["test-file-id"]
                mock_settings.allowed_modules = [
                    "numpy", "pandas", "scipy",
                    "matplotlib", "sklearn", "statsmodels"
                ]
                mock_settings.file_search = {
                    "query": "",
                    "results": [],
                    "file_ids": ["test-file-id"],
                    "search_mode": "semantic"
                }
                mock_code_tool.settings = mock_settings
                tools.append(mock_code_tool)
            
            mock_agents[agent_id] = Mock(
                id=agent_id,
                name=name,
                model=os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4"),
                system_prompt=f"You are an AI agent specialized in {name}.",
                tools=tools,
                tool_resources=tool_resources,
                status="ready"
            )
        
        # Setup mock conversation with realistic responses
        mock_conversation = Mock(
            id="test-conversation",
            agent_id=None,  # Will be set when conversation is created
            get_messages=Mock(return_value=[]),
            add_message=Mock(return_value=create_mock_message("Test message")),
            delete=Mock()
        )
        
        # Create response handler with access to agents and conversation
        get_mock_response = create_mock_response_handler(mock_agents, mock_conversation)
        mock_conversation.send_message = Mock(side_effect=get_mock_response)
        
        # Create a mock file object with comprehensive attributes
        mock_file = Mock(
            id="test-file-id",
            name="test-file",
            content_type="text/csv",
            size=1024,
            status="completed",
            purpose="AGENTS",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            download=Mock(return_value=b"test,data\n1,2\n3,4")
        )
        mock_file.wait_for_completion = Mock(return_value=mock_file)
        mock_file.download = Mock(return_value=b"test,data\n1,2\n3,4")
        
        # Create a mock files client with comprehensive methods
        mock_files_client = Mock(
            upload_and_poll=Mock(return_value=mock_file),
            upload=Mock(return_value=mock_file),
            get=Mock(return_value=mock_file),
            list=Mock(return_value=[mock_file]),
            delete=Mock(return_value=None),
            download=Mock(return_value=b"test,data\n1,2\n3,4"),
            wait_for_completion=Mock(return_value=mock_file),
            file_search={"query": "test", "results": [mock_file]}
        )
        # Add file_search as both method and attribute
        mock_files_client.file_search = Mock(return_value=[mock_file])
        setattr(mock_files_client, 'file_search', {"query": "test", "results": [mock_file]})
        
        def get_file_search_config(file_ids=None):
            """Helper to create consistent file_search configuration"""
            return {
                "query": "",
                "results": [],
                "file_ids": file_ids or [],
                "search_mode": "semantic"
            }

        # Create a mock agents client that returns the appropriate agent based on endpoint
        async def create_agent(model=None, name=None, instructions=None, tools=None, tool_resources=None, headers=None):
            # Add preview headers if not provided
            if not headers:
                headers = {
                    "x-ms-enable-preview": "true",
                    "x-ms-api-version": os.getenv("spn_4o_api_version", "2024-02-15-preview")
                }
            
            # Map endpoint names to agent IDs
            endpoint_to_agent = {
                "literature-search": "agent-1111",
                "molecule-analysis": "agent-2222",
                "trial-data-analysis": "agent-3333",
                "drug-repurpose": "agent-1122",
                "manufacturing-opt": "agent-2001",
                "precision-med": "agent-3002",
                "digital-twin-sim": "agent-5000"
            }
            
            # Ensure tools have proper file_search configuration
            if tools:
                for tool in tools:
                    if isinstance(tool, dict):
                        if "settings" not in tool:
                            tool["settings"] = {}
                        
                        # Add file_search configuration based on tool type
                        if tool.get("type") == "bing-grounding":
                            if "search_parameters" not in tool["settings"]:
                                tool["settings"]["search_parameters"] = {
                                    "count": 5,
                                    "textDecorations": True,
                                    "textFormat": "HTML"
                                }
                            tool["settings"]["file_search"] = get_file_search_config()
                        
                        elif tool.get("type") == "function-calling":
                            tool["settings"]["file_search"] = get_file_search_config()
                        
                        elif tool.get("type") == "code-interpreter":
                            if "allowed_modules" not in tool["settings"]:
                                tool["settings"]["allowed_modules"] = [
                                    "numpy", "pandas", "scipy",
                                    "matplotlib", "sklearn", "statsmodels"
                                ]
                            tool["settings"]["file_search"] = get_file_search_config(
                                tool["settings"].get("file_ids", [])
                            )
            
            # Get agent ID or use default
            agent_id = endpoint_to_agent.get(name, "agent-0000")
            
            # Create a new mock agent if it doesn't exist
            if agent_id not in mock_agents:
                mock_agents[agent_id] = Mock(
                    id=agent_id,
                    name=name or "default-agent",
                    model=model or os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o"),
                    instructions=instructions,
                    tools=tools or [],
                    tool_resources=tool_resources or {},
                    headers=headers,
                    status="completed"  # Add status to indicate agent is ready
                )
            
            # Return the existing or newly created agent
            agent = mock_agents[agent_id]
            # Update conversation mock for this agent
            if agent.id not in mock_conversations:
                mock_conversations[agent.id] = Mock(
                    id=f"conv-{agent.id}",
                    agent_id=agent.id,
                    send_message=Mock(side_effect=get_mock_response),
                    get_messages=Mock(return_value=[]),
                    add_message=Mock(return_value=create_mock_message(f"Test message for {agent.name}")),
                    delete=Mock(),
                    status="completed",  # Add status to indicate conversation is ready
                    wait_for_completion=Mock(return_value=Mock(
                        id=f"conv-{agent.id}",
                        agent_id=agent.id,
                        send_message=Mock(side_effect=get_mock_response),
                        get_messages=Mock(return_value=[]),
                        add_message=Mock(return_value=create_mock_message(f"Test message for {agent.name}")),
                        delete=Mock(),
                        status="completed"
                    ))
                )
            
            return agent

        # Create a mock agents client that properly handles agent creation and retrieval
        mock_agents_client = Mock(
            create_agent=Mock(side_effect=create_agent),  # Use create_agent to match SDK
            get=Mock(side_effect=lambda agent_id: next((agent for agent in mock_agents.values() if agent.id == agent_id), None)),
            list=Mock(return_value=list(mock_agents.values())),
            delete=Mock()  # Add delete method
        )
        
        # Create a mock connections client with proper Bing API key
        mock_connections_client = Mock(
            get_default=Mock(return_value=Mock(id=os.getenv("spn_4o_BING_API_KEY"))),
            get=Mock(return_value=Mock(id=os.getenv("spn_4o_BING_API_KEY"))),
            list=Mock(return_value=[Mock(id=os.getenv("spn_4o_BING_API_KEY"))])
        )
        
        # Configure the project client with proper file handling and agent management
        mock_project_instance = Mock(
            agents=mock_agents_client,
            connections=mock_connections_client,
            files=mock_files_client,  # Add files client directly in constructor
            endpoint=os.getenv("spn_4o_azure_endpoint"),
            subscription_id=os.getenv("spn_4o_AZURE_SUBSCRIPTION_ID", "test-subscription"),
            resource_group_name=os.getenv("AZURE_RESOURCE_GROUP", "test-resource-group"),
            project_name=os.getenv("AZURE_PROJECT_NAME", "drug-discovery")
        )
        
        # Configure the mock AIProjectClient to return our configured instance
        mock_project_client.return_value = mock_project_instance
        
        # Configure mock BingGroundingTool
        mock_bing_tool.return_value = Mock(
            connection_id=os.getenv("spn_4o_BING_API_KEY"),
            type="bing-grounding",
            name="bing-grounding",
            settings={
                "search_parameters": {
                    "count": 5,
                    "textDecorations": True,
                    "textFormat": "HTML"
                },
                "file_search": get_file_search_config()
            }
        )
        
        # Configure mock FunctionTool
        mock_function_tool.return_value = Mock(
            type="function",
            name="function",
            settings={
                "functions": [],
                "file_search": get_file_search_config()
            }
        )
        
        # Add file_search as a method directly
        mock_project_instance.file_search = Mock(return_value=[mock_file])
        
        # Add resource management methods
        mock_project_instance.create_resource = Mock(return_value=Mock(
            id="test-resource-id",
            name="test-resource",
            type="Microsoft.CognitiveServices/accounts",
            location="westus2"
        ))
        mock_project_instance.get_resource = Mock(return_value=Mock(
            id="test-resource-id",
            name="test-resource",
            type="Microsoft.CognitiveServices/accounts",
            location="westus2"
        ))
        mock_project_instance.list_resources = Mock(return_value=[Mock(
            id="test-resource-id",
            name="test-resource",
            type="Microsoft.CognitiveServices/accounts",
            location="westus2"
        )])
        
        # Set up mock agents for each endpoint
        endpoint_agents = {
            "literature-search": Mock(id="agent-1111"),
            "molecule-analysis": Mock(id="agent-2222"),
            "trial-data-analysis": Mock(id="agent-3333"),
            "drug-repurpose": Mock(id="agent-1122"),
            "manufacturing-opt": Mock(id="agent-2001"),
            "precision-med": Mock(id="agent-3002"),
            "digital-twin-sim": Mock(id="agent-5000")
        }
        
        # Update create_agent to return the appropriate mock agent with proper tools and response templates
        async def create_agent(model=None, name=None, instructions=None, tools=None, tool_resources=None):
            if name in endpoint_agents:
                agent_id = endpoint_agents[name].id
                
                # Ensure tools have proper file_search configuration
                if tools:
                    for tool in tools:
                        if isinstance(tool, dict):
                            if "settings" not in tool:
                                tool["settings"] = {}
                            if "file_search" not in tool["settings"]:
                                tool["settings"]["file_search"] = {
                                    "query": "",
                                    "results": [],
                                    "file_ids": [],
                                    "search_mode": "semantic"
                                }
                            
                            # Add specific settings based on tool type
                            if tool.get("type") == "bing-grounding":
                                if "search_parameters" not in tool["settings"]:
                                    tool["settings"]["search_parameters"] = {
                                        "count": 5,
                                        "textDecorations": True,
                                        "textFormat": "HTML"
                                    }
                            elif tool.get("type") == "function-calling":
                                if "functions" not in tool["settings"]:
                                    tool["settings"]["functions"] = []
                            elif tool.get("type") == "code-interpreter":
                                if "allowed_modules" not in tool["settings"]:
                                    tool["settings"]["allowed_modules"] = [
                                        "numpy",
                                        "pandas",
                                        "scipy",
                                        "matplotlib",
                                        "sklearn",
                                        "statsmodels"
                                    ]
                
                agent = Mock(
                    id=agent_id,
                    name=name,
                    model=model or os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4"),
                    instructions=instructions,
                    tools=tools or [],
                    tool_resources=tool_resources or {},
                    status="completed"
                )
                
                # Set up conversation for this agent
                if agent_id not in mock_conversations:
                    mock_conversations[agent_id] = Mock(
                        id=f"conv-{agent_id}",
                        agent_id=agent_id,
                        send_message=Mock(side_effect=lambda msg: create_mock_message(json.dumps({
                            "drug-repurpose": {
                                "repurposing_opportunities": [{
                                    "disease": "RareAutoimmuneXYZ",
                                    "confidence": 0.89,
                                    "supporting_sources": ["DOI:10.1234/..."]
                                }]
                            },
                            "manufacturing-opt": {
                                "optimized_schedule": {
                                    "batch_size": 1000,
                                    "line_allocation": "FactoryA",
                                    "estimated_unit_cost": 2.45
                                }
                            },
                            "precision-med": {
                                "patient_id": "PAT-007",
                                "custom_dosage": "120 mg daily",
                                "predicted_outcome": 0.93,
                                "recommended_followups": ["Monthly biomarker profiling"]
                            },
                            "digital-twin-sim": {
                                "simulated_population_size": 10000,
                                "mean_toxicity_score": 0.12,
                                "average_survival_gain": "6 months"
                            }
                        }.get(name, {"error": "Unknown agent type"})))),
                        get_messages=Mock(return_value=[]),
                        add_message=Mock(return_value=create_mock_message(f"Test message for {name}")),
                        delete=Mock(),
                        status="completed"
                    )
                return agent
            return Mock(id=f"agent-{name}")
        
        # Initialize mock_conversations dictionary at the module level
        global mock_conversations
        mock_conversations = {}
        
        # Update the agents client with the create_agent method
        mock_agents_client.create_agent = Mock(side_effect=create_agent)
        mock_project_instance.agents = mock_agents_client
        
        # Initialize conversations for existing agents
        for agent_id, agent in mock_agents.items():
            if agent_id not in mock_conversations:
                mock_conversations[agent_id] = Mock(
                    id=f"conv-{agent_id}",
                    agent_id=agent_id,
                    send_message=Mock(side_effect=get_mock_response),
                    get_messages=Mock(return_value=[]),
                    add_message=Mock(return_value=create_mock_message(f"Test message for {agent.name}")),
                    delete=Mock(),
                    status="completed"
                )
        
        # Set the return value for the project client
        mock_project_client.return_value = mock_project_instance
        
        # Create a mock message object
        # Use top-level create_mock_message function

        # Create a mock conversation object with proper methods
        # Use the first agent from our mock_agents dictionary
        default_agent_id = next(iter(mock_agents.values())).id
        mock_conversation = Mock(
            id="test-conversation-id",
            agent_id=default_agent_id,
            send_message=Mock(side_effect=get_mock_response),
            get_messages=Mock(return_value=[]),
            add_message=Mock(return_value=create_mock_message("Test message")),
            delete=Mock()
        )

        # Create mock conversations for each agent type with async support
        # Note: mock_conversations is already initialized at the module level
        for agent in mock_agents.values():
            mock_conv = Mock(
                id=f"conv-{agent.id}",
                agent_id=agent.id,
                get_messages=Mock(return_value=[]),
                add_message=Mock(return_value=create_mock_message(f"Test message for {agent.name}")),
                delete=Mock(),
                status="completed"  # Add status to indicate completion
            )
            
            # Create an async send_message function specific to this agent
            async def mock_send_message(message, agent_id=agent.id, agent_name=agent.name):
                agent_type = next(
                    (name for name, (_, id_val) in endpoint_to_agent.items() if id_val == agent_id),
                    agent_name
                )
                response_data = {
                    "drug-repurpose": {
                        "repurposing_opportunities": [{
                            "disease": "RareAutoimmuneXYZ",
                            "confidence": 0.89,
                            "supporting_sources": ["DOI:10.1234/..."]
                        }],
                        "agent_id": agent_id
                    },
                    "manufacturing-opt": {
                        "optimized_schedule": {
                            "batch_size": 1000,
                            "line_allocation": "FactoryA",
                            "estimated_unit_cost": 2.45
                        },
                        "agent_id": agent_id
                    },
                    "precision-med": {
                        "patient_id": "PAT-007",
                        "custom_dosage": "120 mg daily",
                        "predicted_outcome": 0.93,
                        "recommended_followups": ["Monthly biomarker profiling"],
                        "agent_id": agent_id
                    },
                    "digital-twin-sim": {
                        "simulated_population_size": 10000,
                        "mean_toxicity_score": 0.12,
                        "average_survival_gain": "6 months",
                        "agent_id": agent_id
                    }
                }
                return create_mock_message(json.dumps(response_data.get(agent_type, {"error": "Unknown agent type"})))
            
            # Bind the send_message function to this specific conversation
            mock_conv.send_message = Mock(side_effect=mock_send_message)
            mock_conversations[agent.id] = mock_conv

        # Configure the chat client with agent-specific conversations
        async def create_conversation(agent_id):
            if agent_id not in mock_agents:
                raise Exception("(404) Resource not found\nCode: 404\nMessage: Resource not found")
            
            conversation_id = f"conv-{agent_id}"
            if conversation_id not in mock_conversations:
                # Create a mock conversation with proper async methods
                mock_conv = Mock(
                    id=conversation_id,
                    agent_id=agent_id,
                    get_messages=Mock(return_value=[]),
                    add_message=Mock(return_value=create_mock_message(f"Test message for {mock_agents[agent_id].name}")),
                    delete=Mock(),
                    status="completed"
                )
                
                # Set up async send_message that returns proper JSON format
                async def mock_send_message(message):
                    agent_type = next(
                        (name for name, (_, id_val) in endpoint_to_agent.items() if id_val == agent_id),
                        "unknown"
                    )
                    response_data = {
                        "literature-search": {
                            "query": "EGFR inhibitors in lung cancer",
                            "summary": "Recent research shows promising results...",
                            "references": ["DOI:10.1234/..."],
                            "agent_id": agent_id
                        },
                        "molecule-analysis": {
                            "molecule": "CC1=CC=C(C=C1)NC(=O)C2=CC=C(Cl)C=C2",
                            "analysis": {
                                "binding_predictions": {"EGFR": 0.85, "HER2": 0.76},
                                "drug_likeness": 0.92,
                                "safety_assessment": "Low toxicity profile"
                            },
                            "agent_id": agent_id
                        },
                        "trial-data-analysis": {
                            "filename": "test_data.csv",
                            "analysis": {
                                "correlations": {"age": 0.45, "biomarker_a": 0.78},
                                "summary": "Strong correlation found...",
                                "recommendations": ["Focus on biomarker_a", "Stratify by age"]
                            },
                            "agent_id": agent_id
                        },
                        "drug-repurpose": {
                            "repurposing_opportunities": [{
                                "disease": "RareAutoimmuneXYZ",
                                "confidence": 0.89,
                                "supporting_sources": ["DOI:10.1234/..."]
                            }],
                            "agent_id": agent_id
                        },
                        "manufacturing-opt": {
                            "optimized_schedule": {
                                "batch_size": 1000,
                                "line_allocation": "FactoryA",
                                "estimated_unit_cost": 2.45
                            },
                            "agent_id": agent_id
                        },
                        "precision-med": {
                            "patient_id": "PAT-007",
                            "custom_dosage": "120 mg daily",
                            "predicted_outcome": 0.93,
                            "recommended_followups": ["Monthly biomarker profiling"],
                            "agent_id": agent_id
                        },
                        "digital-twin-sim": {
                            "simulated_population_size": 10000,
                            "mean_toxicity_score": 0.12,
                            "average_survival_gain": "6 months",
                            "agent_id": agent_id
                        }
                    }
                    return create_mock_message(json.dumps(response_data.get(agent_type, {"error": "Unknown agent type"})))
                
                mock_conv.send_message = Mock(side_effect=mock_send_message)
                mock_conv.wait_for_completion = Mock(return_value=mock_conv)
                mock_conversations[conversation_id] = mock_conv
            
            return mock_conversations[conversation_id]

        # Configure the chat client with proper async support
        async def async_create_conversation(agent_id):
            if agent_id not in mock_agents:
                raise Exception("(404) Resource not found\nCode: 404\nMessage: Resource not found")
            
            # Map agent IDs to their endpoint types
            agent_to_endpoint = {
                "agent-1111": "literature-search",
                "agent-2222": "molecule-analysis",
                "agent-3333": "trial-data-analysis",
                "agent-1122": "drug-repurpose",
                "agent-2001": "manufacturing-opt",
                "agent-3002": "precision-med",
                "agent-5000": "digital-twin-sim"
            }
            
            conversation_id = f"conv-{agent_id}"
            if conversation_id not in mock_conversations:
                # Create a mock conversation with proper async methods
                mock_conv = Mock(
                    id=conversation_id,
                    agent_id=agent_id,
                    get_messages=Mock(return_value=[]),
                    add_message=Mock(return_value=create_mock_message(f"Test message for {mock_agents[agent_id].name}")),
                    delete=Mock(),
                    status="completed"
                )
                
                # Set up async send_message that returns proper JSON format
                async def mock_send_message(message):
                    endpoint_type = agent_to_endpoint.get(agent_id, "unknown")
                    response_data = {
                        "literature-search": {
                            "query": "EGFR inhibitors in lung cancer",
                            "summary": "Recent research shows promising results...",
                            "references": ["DOI:10.1234/..."],
                            "agent_id": agent_id
                        },
                        "molecule-analysis": {
                            "molecule": "CC1=CC=C(C=C1)NC(=O)C2=CC=C(Cl)C=C2",
                            "analysis": {
                                "binding_predictions": {"EGFR": 0.85, "HER2": 0.76},
                                "drug_likeness": 0.92,
                                "safety_assessment": "Low toxicity profile"
                            },
                            "agent_id": agent_id
                        },
                        "trial-data-analysis": {
                            "filename": "test_data.csv",
                            "analysis": {
                                "correlations": {"age": 0.45, "biomarker_a": 0.78},
                                "summary": "Strong correlation found...",
                                "recommendations": ["Focus on biomarker_a", "Stratify by age"]
                            },
                            "agent_id": agent_id
                        },
                        "drug-repurpose": {
                            "repurposing_opportunities": [{
                                "disease": "RareAutoimmuneXYZ",
                                "confidence": 0.89,
                                "supporting_sources": ["DOI:10.1234/..."]
                            }],
                            "agent_id": agent_id
                        },
                        "manufacturing-opt": {
                            "optimized_schedule": {
                                "batch_size": 1000,
                                "line_allocation": "FactoryA",
                                "estimated_unit_cost": 2.45
                            },
                            "agent_id": agent_id
                        },
                        "precision-med": {
                            "patient_id": "PAT-007",
                            "custom_dosage": "120 mg daily",
                            "predicted_outcome": 0.93,
                            "recommended_followups": ["Monthly biomarker profiling"],
                            "agent_id": agent_id
                        },
                        "digital-twin-sim": {
                            "simulated_population_size": 10000,
                            "mean_toxicity_score": 0.12,
                            "average_survival_gain": "6 months",
                            "agent_id": agent_id
                        }
                    }
                    return create_mock_message(json.dumps(response_data.get(endpoint_type, {"error": "Unknown agent type"})))
                
                mock_conv.send_message = Mock(side_effect=mock_send_message)
                mock_conv.wait_for_completion = Mock(return_value=mock_conv)
                mock_conversations[conversation_id] = mock_conv
            
            return mock_conversations[conversation_id]

        # Configure chat client with proper async support
        mock_chat_instance = Mock(
            endpoint=os.getenv("spn_4o_azure_endpoint"),
            api_version=os.getenv("spn_4o_api_version", "2024-02-15-preview")
        )
        
        # Set up create_conversation to use async_create_conversation
        mock_chat_instance.create_conversation = Mock(side_effect=async_create_conversation)
        mock_chat_instance.get_conversation = Mock(side_effect=lambda conv_id: mock_conversations.get(conv_id))
        mock_chat_instance.list_conversations = Mock(return_value=list(mock_conversations.values()))
        
        mock_chat_client.return_value = mock_chat_instance
        
        # Mock tools and toolset with proper serialization
        mock_toolset = Mock()
        
        mock_toolset.definitions = [
            {
                "type": "bing-grounding",
                "name": "bing-grounding",
                "settings": {
                    "connection_id": os.getenv("spn_4o_BING_API_KEY"),
                    "search_parameters": {
                        "count": 5,
                        "textDecorations": True,
                        "textFormat": "HTML"
                    },
                    "file_search": get_file_search_config()
                }
            },
            {
                "type": "function-calling",
                "name": "function-tool",
                "settings": {
                    "functions": [],
                    "file_search": get_file_search_config()
                }
            },
            {
                "type": "code-interpreter",
                "name": "code-interpreter",
                "settings": {
                    "file_ids": ["test-file-id"],
                    "allowed_modules": [
                        "numpy",
                        "pandas",
                        "scipy",
                        "matplotlib",
                        "sklearn",
                        "statsmodels"
                    ],
                    "file_search": get_file_search_config(["test-file-id"])
                }
            }
        ]
        mock_toolset.resources = {
            "connection_id": os.getenv("spn_4o_BING_API_KEY"),
            "functions": [],
            "file_ids": ["test-file-id"]
        }
        mock_toolset.add = Mock()
        mock_toolset._tools = [
            Mock(
                type="bing-grounding",
                name="bing-grounding",
                settings={
                    "connection_id": os.getenv("spn_4o_BING_API_KEY"),
                    "search_parameters": {
                        "count": 5,
                        "textDecorations": True,
                        "textFormat": "HTML"
                    },
                    "file_search": {
                        "query": "",
                        "results": [],
                        "file_ids": [],
                        "search_mode": "semantic"
                    }
                }
            ),
            Mock(
                type="function-calling",
                name="function-tool",
                settings={
                    "functions": [],
                    "file_search": {
                        "query": "",
                        "results": [],
                        "file_ids": [],
                        "search_mode": "semantic"
                    }
                }
            ),
            Mock(
                type="code-interpreter",
                name="code-interpreter",
                settings={
                    "file_ids": ["test-file-id"],
                    "allowed_modules": [
                        "numpy",
                        "pandas",
                        "scipy",
                        "matplotlib",
                        "sklearn",
                        "statsmodels"
                    ],
                    "file_search": {
                        "query": "",
                        "results": [],
                        "file_ids": ["test-file-id"],
                        "search_mode": "semantic"
                    }
                }
            )
        ]
        
        # Mock OpenTelemetry
        mock_span = Mock()
        mock_span.set_attribute = Mock()
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_span)
        mock_context.__exit__ = Mock(return_value=None)
        mock_trace.get_tracer_provider = Mock()
        mock_trace.start_as_current_span = Mock(return_value=mock_context)
        
        # Patch the imported clients with properly configured mocks
        with patch("clients.project_client", mock_project_client.return_value), \
             patch("clients.chat_client", mock_chat_client.return_value), \
             patch("clients.toolset", mock_toolset), \
             patch("azure.ai.projects.models.BingGroundingTool", return_value=mock_toolset._tools[0]), \
             patch("azure.ai.projects.models.FunctionTool", return_value=mock_toolset._tools[1]), \
             patch("azure.ai.projects.models.CodeInterpreterTool", return_value=mock_toolset._tools[2]):
            yield

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "drug-discovery-platform"

@pytest.mark.asyncio
async def test_literature_search(async_client):
    """Test the literature search endpoint."""
    request_data = {
        "query": "EGFR inhibitors in lung cancer",
        "max_results": 5,
        "include_clinical_trials": True
    }
    response = await async_client.post("/agents/literature-search", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "summary" in data
    assert "agent_id" in data
    assert data["query"] == request_data["query"]

@pytest.mark.asyncio
async def test_molecule_analysis(async_client):
    """Test the molecule analysis endpoint."""
    molecule_data = {
        "smiles": "CC1=CC=C(C=C1)NC(=O)C2=CC=C(Cl)C=C2",
        "target_proteins": ["EGFR", "HER2"],
        "therapeutic_area": "Oncology"
    }
    response = await async_client.post("/agents/molecule-analysis", json=molecule_data)
    assert response.status_code == 200
    data = response.json()
    assert "molecule" in data
    assert "analysis" in data
    assert "agent_id" in data
    assert data["molecule"] == molecule_data["smiles"]

@pytest.mark.asyncio
async def test_data_analysis(async_client):
    """Test the clinical trial data analysis endpoint."""
    # Create a simple CSV file for testing
    test_data = "patient_id,age,response\n1,45,positive\n2,52,negative"
    files = {
        'file': ('test_data.csv', test_data, 'text/csv')
    }
    response = await async_client.post("/agents/data-analysis", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert "analysis" in data
    assert "agent_id" in data
    assert data["filename"] == "test_data.csv"

@pytest.mark.asyncio
async def test_invalid_literature_search(async_client):
    """Test error handling for literature search with invalid input."""
    response = await async_client.post("/agents/literature-search", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_invalid_molecule_analysis(async_client):
    """Test error handling for molecule analysis with invalid input."""
    response = await async_client.post("/agents/molecule-analysis", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_invalid_data_analysis(async_client):
    """Test error handling for data analysis without file."""
    response = await async_client.post("/agents/data-analysis")
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_drug_repurpose(async_client):
    """Test the drug repurposing endpoint."""
    request_data = {
        "molecule_id": "TEST-123",
        "new_indication": "RareDisease-XYZ",
        "current_indications": ["Arthritis"]
    }
    response = await async_client.post("/agents/drug-repurpose", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "repurposing_opportunities" in data
    assert "agent_id" in data
    assert len(data["repurposing_opportunities"]) > 0
    opportunity = data["repurposing_opportunities"][0]
    assert "disease" in opportunity
    assert "confidence" in opportunity
    assert "supporting_sources" in opportunity
    assert isinstance(opportunity["supporting_sources"], list)
    assert 0.5 <= opportunity["confidence"] <= 1.0  # Confidence should be between 0.5 and 1.0

@pytest.mark.asyncio
async def test_manufacturing_optimization(async_client):
    """Test the manufacturing optimization endpoint."""
    request_data = {
        "drug_candidate": "TEST-123",
        "batch_size_range": [1000, 2000, 5000],
        "raw_materials": {"API": 1000, "Excipient": 5000},
        "production_constraints": {"max_daily_batches": 3}
    }
    response = await async_client.post("/agents/manufacturing-opt", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "optimized_schedule" in data
    assert "agent_id" in data
    schedule = data["optimized_schedule"]
    assert "batch_size" in schedule
    assert "line_allocation" in schedule
    assert "estimated_unit_cost" in schedule
    assert isinstance(schedule["batch_size"], int)
    assert isinstance(schedule["estimated_unit_cost"], (int, float))
    assert schedule["batch_size"] in request_data["batch_size_range"]

@pytest.mark.asyncio
async def test_precision_medicine(async_client):
    """Test the precision medicine endpoint."""
    request_data = {
        "patient_id": "PAT-007",
        "genetic_markers": {"CYP2D6": "UM", "TPMT": "*1/*3"},
        "medical_history": {"conditions": ["Hypertension"]},
        "current_medications": ["Metoprolol"]
    }
    response = await async_client.post("/agents/precision-med", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "custom_dosage" in data
    assert "predicted_outcome" in data
    assert "recommended_followups" in data
    assert isinstance(data["recommended_followups"], list)
    assert len(data["recommended_followups"]) > 0
    assert "agent_id" in data
    assert 0.0 <= data["predicted_outcome"] <= 1.0  # Outcome should be a probability

@pytest.mark.asyncio
async def test_digital_twin_simulation(async_client):
    """Test the digital twin simulation endpoint."""
    request_data = {
        "molecule_parameters": {
            "half_life": "24h",
            "bioavailability": 0.85
        },
        "target_population": {
            "age_range": [18, 65],
            "conditions": ["Type2Diabetes"]
        },
        "simulation_config": {}
    }
    response = await async_client.post("/agents/digital-twin-sim", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "simulated_population_size" in data
    assert data["simulated_population_size"] == 10000  # Fixed size as per example
    assert "mean_toxicity_score" in data
    assert isinstance(data["mean_toxicity_score"], float)
    assert 0.1 <= data["mean_toxicity_score"] <= 0.15  # Range as per example
    assert "average_survival_gain" in data
    assert data["average_survival_gain"] == "6 months"  # Fixed value as per example
    assert "agent_id" in data

@pytest.mark.asyncio
async def test_invalid_drug_repurpose(async_client):
    """Test error handling for drug repurpose with invalid input."""
    response = await async_client.post("/agents/drug-repurpose", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_invalid_manufacturing_opt(async_client):
    """Test error handling for manufacturing optimization with invalid input."""
    response = await async_client.post("/agents/manufacturing-opt", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_invalid_precision_med(async_client):
    """Test error handling for precision medicine with invalid input."""
    response = await async_client.post("/agents/precision-med", json={})
    assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_invalid_digital_twin(async_client):
    """Test error handling for digital twin simulation with invalid input."""
    response = await async_client.post("/agents/digital-twin-sim", json={})
    assert response.status_code == 422  # Validation error
