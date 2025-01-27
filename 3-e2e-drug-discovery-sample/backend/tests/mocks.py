"""Mock implementations for Azure AI clients and tools."""
from unittest.mock import MagicMock, AsyncMock
import random
import uuid
import json
from azure.ai.projects.models import BingGroundingTool, FunctionTool, CodeInterpreterTool, ToolSet

class MockAgent:
    def __init__(self, id=None, model=None, instructions=None, tools=None, toolset=None):
        self.id = id or f"agent-{uuid.uuid4().hex[:8]}"
        self.model = model
        self.instructions = instructions
        self.tools = tools
        self.toolset = toolset
        self.definitions = []
        self.resources = {}
        
        if toolset and hasattr(toolset, '_tools'):
            for tool in toolset._tools:
                if isinstance(tool, BingGroundingTool):
                    self.definitions.append({
                        "type": "bing_search",
                        "name": "bing_search"
                    })
                elif isinstance(tool, FunctionTool):
                    self.definitions.append({
                        "type": "function",
                        "name": "function"
                    })
                elif isinstance(tool, CodeInterpreterTool):
                    self.definitions.append({
                        "type": "code_interpreter",
                        "name": "code_interpreter"
                    })

class MockMessage:
    def __init__(self, content):
        self.content = content
        self.message = self

class MockConversation:
    def __init__(self, agent_id):
        self.agent_id = agent_id
    
    async def send_message(self, content):
        # Return different responses based on the content
        if "drug repurpose" in content.lower():
            response = {
                "repurposing_opportunities": [{
                    "disease": "RareAutoimmuneXYZ",
                    "confidence": 0.89,
                    "supporting_sources": ["DOI:10.1234/..."]
                }],
                "agent_id": self.agent_id
            }
        elif "manufacturing" in content.lower():
            response = {
                "optimized_schedule": {
                    "batch_size": 1000,
                    "line_allocation": "FactoryA",
                    "estimated_unit_cost": 2.45
                },
                "agent_id": self.agent_id
            }
        elif "precision medicine" in content.lower():
            response = {
                "patient_id": "PAT-007",
                "custom_dosage": "120 mg daily",
                "predicted_outcome": 0.93,
                "recommended_followups": ["Monthly biomarker profiling"],
                "agent_id": self.agent_id
            }
        else:  # Digital twin simulation
            response = {
                "simulated_population_size": 10000,
                "mean_toxicity_score": 0.12,
                "average_survival_gain": "6 months",
                "agent_id": self.agent_id
            }
        return MockMessage(json.dumps(response))

class MockToolSet:
    def __init__(self):
        self._tools = []
        self.definitions = []
        self.resources = {}

    def add(self, tool):
        self._tools.append(tool)
        self.definitions.append({
            "type": tool.__class__.__name__,
            "name": f"tool_{len(self._tools)}"
        })
        self.resources[f"tool_{len(self._tools)}"] = {"config": {}}

class MockAgentsOperations:
    async def create_agent(self, model=None, instructions=None, tools=None, toolset=None, headers=None, tool_resources=None):
        """Mock create_agent that accepts all possible arguments."""
        return MockAgent(
            model=model,
            instructions=instructions,
            tools=tools,
            toolset=toolset
        )

class MockProjectClient:
    def __init__(self):
        self.agents = MockAgentsOperations()

class MockChatClient:
    async def create_conversation(self, agent_id):
        return MockConversation(agent_id)

    async def get_conversation(self, conversation_id):
        return MockConversation(conversation_id)

def mock_drug_repurpose_response():
    """Generate mock response for drug repurposing endpoint."""
    return {
        "repurposing_opportunities": [
            {
                "disease": "RareAutoimmuneXYZ",
                "confidence": round(random.uniform(0.7, 0.95), 2),
                "supporting_sources": [f"DOI:10.{random.randint(1000,9999)}/..."]
            }
        ],
        "agent_id": f"agent-{random.randint(1000,9999)}"
    }

def mock_manufacturing_opt_response():
    """Generate mock response for manufacturing optimization endpoint."""
    return {
        "optimized_schedule": {
            "batch_size": random.choice([1000, 2000, 5000]),
            "line_allocation": f"Factory{random.choice(['A','B','C'])}",
            "estimated_unit_cost": round(random.uniform(1.5, 5.0), 2)
        },
        "agent_id": f"agent-{random.randint(1000,9999)}"
    }

def mock_precision_med_response():
    """Generate mock response for precision medicine endpoint."""
    return {
        "patient_id": f"PAT-{random.randint(1,999):03d}",
        "custom_dosage": f"{random.randint(50,200)} mg daily",
        "predicted_outcome": round(random.uniform(0.7, 0.98), 2),
        "recommended_followups": [
            "Monthly biomarker profiling",
            "Quarterly genetic screening"
        ],
        "agent_id": f"agent-{random.randint(1000,9999)}"
    }

def mock_digital_twin_response():
    """Generate mock response for digital twin simulation endpoint."""
    return {
        "simulated_population_size": random.randint(5000, 15000),
        "mean_toxicity_score": round(random.uniform(0.05, 0.3), 2),
        "average_survival_gain": f"{random.randint(3,12)} months",
        "agent_id": f"agent-{random.randint(1000,9999)}"
    }
