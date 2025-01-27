import pytest
import asyncio
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
from main import app
import json
from unittest.mock import patch, AsyncMock, MagicMock
from azure.ai.projects.models import ToolSet
from .mocks import (
    MockProjectClient,
    MockChatClient,
    MockToolSet,
    mock_drug_repurpose_response,
    mock_manufacturing_opt_response,
    mock_precision_med_response,
    mock_digital_twin_response
)

# Import request models
from routers.agents import (
    DrugRepurposeRequest,
    ManufacturingOptRequest,
    PrecisionMedRequest,
    DigitalTwinRequest
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def mock_clients():
    """Mock Azure AI clients for testing."""
    mock_project_client = MockProjectClient()
    mock_chat_client = MockChatClient()
    
    with patch('clients.init_clients', AsyncMock(return_value=(mock_project_client, mock_chat_client, None))), \
         patch('clients.project_client', mock_project_client), \
         patch('clients.chat_client', mock_chat_client), \
         patch('routers.agents.project_client', mock_project_client), \
         patch('routers.agents.chat_client', mock_chat_client), \
         patch('routers.agents.agent_cache', {}), \
         patch.dict(os.environ, {
             'MODEL_DEPLOYMENT_NAME': 'gpt-4',
             'spn_4o_BING_API_KEY': 'mock-bing-key',
             'spn_4o_model': 'gpt-4'
         }, clear=True):
        yield

@pytest.fixture(scope="session")
def test_app():
    """Create a test application instance."""
    return app

@pytest.fixture(scope="session")
def client(test_app):
    """Create a test client."""
    with TestClient(test_app) as client:
        yield client

@pytest.mark.asyncio
async def test_drug_repurpose(client):
    """Test the drug repurposing endpoint."""
    request_data = {
        "molecule_id": "DRUG123",
        "new_indication": "RareAutoimmuneXYZ",
        "current_indications": ["Arthritis", "Lupus"]
    }
    
    response = client.post("/agents/drug-repurpose", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "repurposing_opportunities" in data
    assert isinstance(data["repurposing_opportunities"], list)
    assert len(data["repurposing_opportunities"]) > 0
    
    opportunity = data["repurposing_opportunities"][0]
    assert "disease" in opportunity
    assert "confidence" in opportunity
    assert "supporting_sources" in opportunity
    assert isinstance(opportunity["confidence"], float)
    assert 0 <= opportunity["confidence"] <= 1

@pytest.mark.asyncio
async def test_manufacturing_optimization(client):
    """Test the manufacturing optimization endpoint."""
    request_data = {
        "drug_candidate": "DRUG123",
        "batch_size_range": [1000, 2000, 5000],
        "raw_materials": {"API": 1000, "Excipient": 5000},
        "production_constraints": {"max_daily_batches": 3}
    }
    
    response = client.post("/agents/manufacturing-opt", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "optimized_schedule" in data
    schedule = data["optimized_schedule"]
    
    assert "batch_size" in schedule
    assert "line_allocation" in schedule
    assert "estimated_unit_cost" in schedule
    assert isinstance(schedule["batch_size"], int)
    assert isinstance(schedule["estimated_unit_cost"], float)

@pytest.mark.asyncio
async def test_precision_medicine(client):
    """Test the precision medicine endpoint."""
    request_data = {
        "patient_id": "PAT007",
        "genetic_markers": {"CYP2D6": "UM", "TPMT": "*1/*3"},
        "medical_history": {"conditions": ["Hypertension"]},
        "current_medications": ["Metoprolol"]
    }
    
    response = client.post("/agents/precision-med", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "patient_id" in data
    assert "custom_dosage" in data
    assert "predicted_outcome" in data
    assert "recommended_followups" in data
    
    assert isinstance(data["predicted_outcome"], float)
    assert 0 <= data["predicted_outcome"] <= 1
    assert isinstance(data["recommended_followups"], list)

@pytest.mark.asyncio
async def test_digital_twin_simulation(client):
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
    
    response = client.post("/agents/digital-twin-sim", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "simulated_population_size" in data
    assert "mean_toxicity_score" in data
    assert "average_survival_gain" in data
    
    assert isinstance(data["simulated_population_size"], int)
    assert isinstance(data["mean_toxicity_score"], float)
    assert 0 <= data["mean_toxicity_score"] <= 1
    assert isinstance(data["average_survival_gain"], str)
    assert "months" in data["average_survival_gain"]

@pytest.mark.asyncio
async def test_invalid_requests(client):
    """Test error handling for invalid requests."""
    # Test drug repurpose with missing required field
    response = client.post("/agents/drug-repurpose", json={})
    assert response.status_code == 422
    
    # Test manufacturing optimization with invalid batch size
    response = client.post("/agents/manufacturing-opt", json={
        "drug_candidate": "DRUG123",
        "batch_size_range": "invalid",
        "raw_materials": {}
    })
    assert response.status_code == 422
    
    # Test precision medicine with invalid genetic markers
    response = client.post("/agents/precision-med", json={
        "patient_id": "PAT007",
        "genetic_markers": "invalid",
        "medical_history": {}
    })
    assert response.status_code == 422
    
    # Test digital twin simulation with missing required fields
    response = client.post("/agents/digital-twin-sim", json={})
    assert response.status_code == 422
