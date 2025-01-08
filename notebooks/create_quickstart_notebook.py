import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

# Create notebooks directory if it doesn't exist
os.makedirs("introduction", exist_ok=True)

# Create a new notebook
nb = new_notebook()

# Add cells to the notebook
nb['cells'] = [
    new_markdown_cell("""# Quick Start Guide - Azure AI Foundry

This notebook provides a hands-on introduction to Azure AI Foundry. You'll learn how to:
1. Initialize the AI Project client
2. List available models
3. Create a simple completion request
4. Handle basic error scenarios

## Prerequisites
- Completed environment setup from previous notebook
- Azure credentials configured"""),
    
    new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os
import json

# Initialize credentials
credential = DefaultAzureCredential()"""),
    
    new_markdown_cell("""## Initialize AI Project Client
First, let's create our client instance:"""),
    
    new_code_cell("""# Create AI Project client
try:
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""),
    
    new_markdown_cell("""## List Available Models
Let's see what models are available to us:"""),
    
    new_code_cell("""# List models
try:
    models = list(client.models.list())
    print(f"Found {len(models)} models:")
    for model in models:
        print(f"- {model.name}")
except Exception as e:
    print(f"× Error listing models: {str(e)}")"""),
    
    new_markdown_cell("""## Create a Simple Completion
Let's try a basic completion request:"""),
    
    new_code_cell("""# Test completion
try:
    response = client.models.generate(
        deployment_name="customer-service-v1",  # Update with your deployment name
        prompt="How can I help you with your account today?",
        max_tokens=100
    )
    print("Response:", response)
except Exception as e:
    print(f"× Error generating completion: {str(e)}")"""),
    
    new_markdown_cell("""## Error Handling Example
Let's see how to handle a common error scenario:"""),
    
    new_code_cell("""# Test error handling
try:
    # Intentionally use invalid deployment name
    response = client.models.generate(
        deployment_name="non-existent-model",
        prompt="This should fail gracefully",
        max_tokens=100
    )
except Exception as e:
    print("Expected error caught successfully:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")"""),
    
    new_markdown_cell("""## Next Steps
- Explore more advanced model configurations
- Try different prompt types
- Implement retry logic for robustness
- Add logging for production use""")
]

# Write the notebook
nbf.write(nb, "introduction/quick_start.ipynb")
print("Created quick_start.ipynb in introduction directory")
