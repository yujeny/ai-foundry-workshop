# Quick Setup Guide

Welcome to the Customer Service AI Agent workshop! Let's get your environment ready for development.

## Prerequisites Check (5 minutes)

1. **Azure Account Setup**
   ```bash
   # Login to Azure
   az login
   
   # Set subscription
   az account set --subscription <your-subscription-id>
   ```

2. **Python Environment**
   ```bash
   # Check Python version (3.8 or later required)
   python --version
   
   # Install required packages
   pip install azure-identity azure-ai-projects azure-ai-inference azure-ai-evaluation azure-ai-contentsafety azure-monitor-opentelemetry
   ```

## Project Setup (10 minutes)

1. **Create AI Foundry Project**
   ```python
   from azure.identity import DefaultAzureCredential
   from azure.ai.resources import AIProjectClient
   
   # Initialize client
   credential = DefaultAzureCredential()
   client = AIProjectClient(
       subscription_id="your-subscription-id",
       resource_group="your-resource-group",
       credential=credential
   )
   
   # Create project
   project = client.projects.create(
       name="customer-service-agent",
       description="AI-powered customer service agent"
   )
   ```

2. **Verify Access**
   ```python
   # Test connection
   models = client.models.list()
   print("Available models:", len(models))
   ```

## Environment Variables

Set these required variables:
```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="your-resource-group"
```

## Interactive Setup Notebook

For a hands-on environment setup experience, you can use our interactive Jupyter notebook:

[Launch Environment Setup Notebook](../building_agent/project_setup/project_setup.ipynb)

This notebook will guide you through:
- Installing required packages
- Setting up Azure authentication
- Initializing the AI Project client
- Verifying access to models

## What's Next?

In this workshop, you'll:
1. Deploy a GPT model for customer service
2. Create an intelligent support agent
3. Evaluate and monitor performance

Let's start by [accessing AI Foundry](ai-foundry.md) to deploy our model!
