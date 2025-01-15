import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

# Create notebooks directory if it doesn't exist
os.makedirs("introduction", exist_ok=True)

# Create a new notebook
nb = new_notebook()

# Add cells to the notebook
nb["cells"] = [
    new_markdown_cell("""# Environment Setup for Azure AI Foundry Workshop

This notebook will guide you through setting up your environment for the Azure AI Foundry workshop.

## Prerequisites
- Python 3.8 or later
- Azure subscription with AI services access
- Basic Python knowledge"""),
    
    new_code_cell("""# Install required packages
!pip install azure-identity azure-ai-projects azure-ai-inference azure-ai-evaluation azure-ai-contentsafety azure-monitor-opentelemetry"""),
    
    new_markdown_cell("""## Azure Authentication Setup
First, we'll verify our Azure credentials and setup."""),
    
    new_code_cell("""from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.evaluation import TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument
import os

# Initialize Azure credentials
try:
    credential = DefaultAzureCredential()
    print("✓ Successfully initialized DefaultAzureCredential")
except Exception as e:
    print(f"× Error initializing credentials: {str(e)}")"""),
    
    new_markdown_cell("""## Initialize AI Project Client
Now we'll create an AI Project client to interact with Azure AI services."""),
    
    new_code_cell("""# Initialize AI Project Client
try:
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""),
    
    new_markdown_cell("""## Verify Access to Models
Finally, let's verify we can access the available models."""),
    
    new_code_cell("""# List available models
try:
    models = client.models.list()
    print(f"✓ Successfully retrieved {len(list(models))} models")
except Exception as e:
    print(f"× Error listing models: {str(e)}")""")
]

# Write the notebook
nbf.write(nb, "introduction/environment_setup.ipynb")
print("Created environment_setup.ipynb in introduction directory")
