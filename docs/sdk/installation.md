# Installing the AI Foundry SDK

This guide will walk you through the process of installing and setting up the Azure AI Foundry development environment.

## Prerequisites

- Python 3.8 or later
- pip (Python package manager)
- Azure subscription with access to Azure AI services
- Azure CLI (recommended for authentication)

## Required Components

1. **Core SDKs**
   - Azure AI Resources SDK for project and model management
   - Azure AI Evaluation SDK for performance assessment
   - Azure Identity package for authentication

2. **Optional Components**
   - Azure Storage SDK for data management
   - Azure KeyVault SDK for secure credential storage
   - Azure AI Inference SDK with OpenTelemetry for model interaction and tracing

## Environment Setup

1. **Create a Virtual Environment** (Recommended)

```bash
# Create a new virtual environment
python -m venv .venv

# Activate the virtual environment (Linux/Mac)
source .venv/bin/activate

# Activate the virtual environment (Windows)
.\.venv\Scripts\activate
```

2. **Install Required Packages**

```bash
# Install core Azure AI Foundry packages
pip install azure-ai-projects
pip install azure-ai-inference
pip install azure-ai-evaluation
pip install azure-ai-contentsafety
pip install azure-monitor-opentelemetry
pip install azure-identity

# Optional but recommended packages
pip install azure-storage-blob  # For data storage
pip install azure-keyvault-secrets  # For secure credential management
```

3. **Configure Development Environment**

```python
# config.py
import os
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient

def setup_environment():
    """Configure the development environment with required settings."""
    try:
        # Initialize Azure credentials
        credential = DefaultAzureCredential()
        
        # Create AI Project client
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        return client
    except Exception as e:
        print(f"Error setting up environment: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    # Set required environment variables
    os.environ["AZURE_SUBSCRIPTION_ID"] = "your-subscription-id"
    os.environ["AZURE_RESOURCE_GROUP"] = "your-resource-group"
    
    # Initialize the client
    client = setup_environment()
    print("Environment setup completed successfully")

## Development Tools Integration

1. **IDE Support**
   - Visual Studio Code
   - PyCharm
   - Jupyter Notebooks

2. **Version Control**
   - Git integration
   - Project structure
   - Dependency management

## Best Practices

- Use virtual environments
- Keep dependencies updated
- Follow security guidelines
- Implement proper error handling

## Troubleshooting Guide

1. **Common Issues**
   - Package version conflicts
   - Authentication failures
   - Environment configuration

2. **Resolution Steps**
   - Verify Python version
   - Check package compatibility
   - Validate credentials
   - Review environment setup

Next: [Setting up Authentication](authentication.md)
