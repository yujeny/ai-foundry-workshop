# Azure AI Projects SDK Tutorial

This tutorial demonstrates how to use the Azure AI Projects SDK for health and dietary applications.

## Prerequisites
```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
```

## Getting Started
Learn how to create and manage AI projects for health applications:
```python
# Initialize the client
client = AIProjectClient(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    credential=DefaultAzureCredential()
)
```

## Health Advisor Project Example
Create a project for health and dietary advice:
```python
project = client.projects.create(
    name="health-advisor",
    description="AI-powered health and dietary advice project",
    tags={
        "domain": "healthcare",
        "features": "dietary-planning,health-advice"
    }
)
```

## Next Steps
- Try the [Projects Tutorial Notebook](../building_agent/sdk_projects_tutorial/sdk_projects_tutorial.ipynb)
- Learn about [Azure AI Inference](inference.md)
- Explore [Content Safety](contentsafety.md)

!!! note "Notebook Tutorial"
    The complete tutorial notebook is available in the Notebooks section under SDK Tutorials.
