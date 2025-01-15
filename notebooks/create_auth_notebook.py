import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

# Create notebooks directory if it doesn't exist
os.makedirs("introduction", exist_ok=True)

# Create a new notebook
nb = new_notebook()

# Add cells to the notebook
nb['cells'] = [
    new_markdown_cell("""# Azure Authentication for AI Foundry

This notebook guides you through setting up authentication for Azure AI Foundry. You'll learn:
1. Different authentication methods
2. Setting up environment variables
3. Using DefaultAzureCredential
4. Testing your authentication
5. Common troubleshooting steps

## Prerequisites
- Azure subscription
- Azure CLI installed (optional)
- Python environment from setup notebook"""),
    
    new_markdown_cell("""## Authentication Methods

Azure AI Foundry supports several authentication methods:
1. DefaultAzureCredential (recommended)
2. Environment Variables
3. Service Principal
4. Managed Identity

We'll focus on DefaultAzureCredential as it provides the most flexible approach."""),
    
    new_code_cell("""# First, let's check if we have the required packages
try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.evaluation import TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument
    print("✓ Required packages are installed")
except ImportError as e:
    print(f"× Missing package: {str(e)}")
    print("Install required packages with:")
    print("pip install azure-identity azure-ai-projects azure-ai-inference azure-ai-evaluation azure-ai-contentsafety azure-monitor-opentelemetry")"""),
    
    new_markdown_cell("""## Environment Variables

DefaultAzureCredential looks for these environment variables:
- AZURE_SUBSCRIPTION_ID
- AZURE_RESOURCE_GROUP
- AZURE_CLIENT_ID (for service principals)
- AZURE_CLIENT_SECRET (for service principals)
- AZURE_TENANT_ID

Let's check if they're set:"""),
    
    new_code_cell("""import os

required_vars = [
    "AZURE_SUBSCRIPTION_ID",
    "AZURE_RESOURCE_GROUP"
]

optional_vars = [
    "AZURE_CLIENT_ID",
    "AZURE_CLIENT_SECRET",
    "AZURE_TENANT_ID"
]

print("Required Variables:")
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✓ {var} is set")
    else:
        print(f"× {var} is not set")

print("\nOptional Variables (for service principals):")
for var in optional_vars:
    value = os.getenv(var)
    if value:
        print(f"✓ {var} is set")
    else:
        print(f"× {var} is not set")"""),
    
    new_markdown_cell("""## Testing Authentication

Let's try to authenticate and create an AI Project client:"""),
    
    new_code_cell("""def test_authentication():
    try:
        # Initialize credentials
        credential = DefaultAzureCredential()
        print("✓ Successfully created DefaultAzureCredential")
        
        # Create client
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        print("✓ Successfully created AIProjectClient")
        
        # Test authentication by listing models
        models = list(client.models.list())
        print(f"✓ Successfully authenticated! Found {len(models)} models")
        return True
        
    except Exception as e:
        print(f"× Authentication failed: {str(e)}")
        return False

test_authentication()"""),
    
    new_markdown_cell("""## Troubleshooting

If authentication fails, try these steps:

1. Check environment variables:
   ```bash
   export AZURE_SUBSCRIPTION_ID="your-subscription-id"
   export AZURE_RESOURCE_GROUP="your-resource-group"
   ```

2. Login with Azure CLI:
   ```bash
   az login
   az account set --subscription <subscription-id>
   ```

3. Check access permissions in Azure Portal:
   - Verify subscription access
   - Check resource group permissions
   - Ensure AI Foundry access is granted"""),
    
    new_code_cell("""# Helper function to diagnose common issues
def diagnose_auth_issues():
    print("Running authentication diagnostics...")
    
    # Check Python version
    import sys
    print(f"\nPython version: {sys.version}")
    
    # Check package versions
    import pkg_resources
    for package in ['azure-identity', 'azure-ai-projects', 'azure-ai-inference', 'azure-ai-evaluation', 'azure-ai-contentsafety']:
        try:
            version = pkg_resources.get_distribution(package).version
            print(f"{package} version: {version}")
        except pkg_resources.DistributionNotFound:
            print(f"× {package} not installed")
    
    # Check environment
    print("\nEnvironment variables:")
    for var in required_vars + optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var} is set to: {'*' * len(value)}")  # Hide actual values
        else:
            print(f"× {var} is not set")

diagnose_auth_issues()"""),
    
    new_markdown_cell("""## Next Steps

Once authenticated, you can:
1. Create and manage AI projects
2. Deploy models
3. Create agents
4. Monitor performance

For more details, see the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/).""")
]

# Write the notebook
nbf.write(nb, "introduction/authentication.ipynb")
print("Created authentication.ipynb in introduction directory")
