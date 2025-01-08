# Authentication Setup

Learn how to securely authenticate your applications with Azure AI Foundry services.

## Authentication Overview

Azure AI Foundry uses Azure Active Directory (Azure AD) for authentication, ensuring secure access to resources and services.

## Authentication Methods

1. **Interactive Browser Authentication**
   - Best for development
   - Uses Azure CLI
   - Browser-based login flow
   - Multi-factor authentication support

2. **Service Principal Authentication**
   - Recommended for production
   - Non-interactive scenarios
   - Application-level access
   - Role-based access control

3. **Managed Identity**
   - Azure-hosted applications
   - Automatic credential management
   - Enhanced security
   - Simplified configuration

## Setting Up Authentication

### 1. Interactive Authentication
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Set subscription
az account set --subscription <your-subscription-id>
```

### 2. Service Principal Authentication
```python
from azure.identity import ClientSecretCredential
from azure.ai.resources import AIProjectClient
import os

def get_ai_client():
    """Initialize AI Project client with service principal authentication."""
    try:
        # Initialize the credential with service principal details
        credential = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )
        
        # Create the AI Project client
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        return client
    except Exception as e:
        print(f"Error initializing AI client: {str(e)}")
        raise

# Example environment variable setup
"""
Required environment variables:
- AZURE_TENANT_ID: Your Azure AD tenant ID
- AZURE_CLIENT_ID: Your service principal client ID
- AZURE_CLIENT_SECRET: Your service principal secret
- AZURE_SUBSCRIPTION_ID: Your Azure subscription ID
- AZURE_RESOURCE_GROUP: Your resource group name
"""
```

### 3. Managed Identity Authentication
```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient

def get_ai_client_managed_identity():
    """Initialize AI Project client with managed identity authentication."""
    try:
        # DefaultAzureCredential will use managed identity when available
        credential = DefaultAzureCredential()
        
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        return client
    except Exception as e:
        print(f"Error initializing AI client with managed identity: {str(e)}")
        raise

## Security Best Practices

1. **Credential Management**
   ```python
   from azure.keyvault.secrets import SecretClient
   from azure.identity import DefaultAzureCredential
   
   def get_credentials_from_keyvault():
       """Retrieve credentials from Azure Key Vault."""
       try:
           # Initialize Key Vault client
           credential = DefaultAzureCredential()
           key_vault_url = os.getenv("AZURE_KEYVAULT_URL")
           secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
           
           # Retrieve secrets
           client_id = secret_client.get_secret("AI-CLIENT-ID").value
           client_secret = secret_client.get_secret("AI-CLIENT-SECRET").value
           
           return client_id, client_secret
       except Exception as e:
           print(f"Error retrieving credentials from Key Vault: {str(e)}")
           raise
   ```
   
   Best practices for credential management:
   - Store secrets in Azure Key Vault
   - Rotate secrets every 90 days
   - Implement proper error handling
   - Monitor access patterns using Azure Monitor

2. **Access Control**
   - Follow least privilege
   - Regular access reviews
   - Role-based permissions
   - Resource-level controls

3. **Environment Security**
   - Secure configuration storage
   - Environment separation
   - Audit logging
   - Monitoring and alerts

## Troubleshooting

1. **Common Issues and Solutions**
   ```python
   from azure.core.exceptions import ClientAuthenticationError
   
   def validate_authentication():
       """Validate authentication setup and troubleshoot common issues."""
       try:
           # Initialize client
           client = get_ai_client()
           
           # Test authentication by listing available models
           models = client.models.list()
           print("Authentication successful!")
           return True
           
       except ClientAuthenticationError as auth_error:
           print(f"Authentication failed: {str(auth_error)}")
           print("\nTroubleshooting steps:")
           print("1. Verify environment variables are set correctly")
           print("2. Check if service principal has required permissions")
           print("3. Ensure credentials haven't expired")
           return False
           
       except Exception as e:
           print(f"Unexpected error: {str(e)}")
           print("\nTroubleshooting steps:")
           print("1. Check network connectivity")
           print("2. Verify Azure subscription status")
           print("3. Review resource group access")
           return False
   ```

2. **Resolution Steps**
   ```bash
   # Verify environment variables
   echo $AZURE_TENANT_ID
   echo $AZURE_CLIENT_ID
   echo $AZURE_SUBSCRIPTION_ID
   
   # Check network access
   ping management.azure.com
   
   # Verify Azure CLI login
   az account show
   
   # Test resource group access
   az group show --name $AZURE_RESOURCE_GROUP
   ```

## Interactive Authentication Workshop

For hands-on practice with authentication setup and troubleshooting, try our interactive notebook:

[Launch Authentication Workshop](../building_agent/project_setup/project_setup.ipynb)

This notebook provides:
- Practical authentication setup examples
- Environment variable configuration
- Real-time authentication testing
- Interactive troubleshooting guide
- Best practices implementation

## Interactive Workshop

For hands-on practice with authentication setup and troubleshooting, try our interactive notebook:

[Launch Project Setup Workshop](../building_agent/project_setup/project_setup.ipynb)

This notebook provides:
- Practical authentication setup examples
- Environment variable configuration
- Real-time authentication testing
- Interactive troubleshooting guide
- Best practices implementation

Next: [Working with AIProjectClient](aiprojectclient.md)
