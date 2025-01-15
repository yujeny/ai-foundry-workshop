import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure Identity SDK tutorial."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure Identity SDK Tutorial

This notebook demonstrates how to use Azure Identity for authentication in health applications.

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## What You'll Learn
- Using DefaultAzureCredential
- Managing authentication
- Securing health applications
- Best practices for identity"""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential, ClientSecretCredential
import os
import json

# Initialize credentials
try:
    credential = DefaultAzureCredential()
    print("✓ Successfully initialized DefaultAzureCredential")
except Exception as e:
    print(f"× Error initializing credentials: {str(e)}")"""))

    # Authentication Methods
    cells.append(new_markdown_cell("""## Authentication Methods

Explore different authentication methods:"""))

    cells.append(new_code_cell("""def demonstrate_auth_methods():
    \"\"\"Demonstrate different authentication methods.\"\"\"
    try:
        # Default credential
        default_cred = DefaultAzureCredential()
        print("✓ DefaultAzureCredential initialized")
        
        # Client secret credential
        client_secret_cred = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )
        print("✓ ClientSecretCredential initialized")
        
        return {
            "default": default_cred,
            "client_secret": client_secret_cred
        }
    except Exception as e:
        print(f"× Error demonstrating auth methods: {str(e)}")
        return None

# Try different auth methods
credentials = demonstrate_auth_methods()"""))

    # Token Management
    cells.append(new_markdown_cell("""## Token Management

Manage access tokens for health applications:"""))

    cells.append(new_code_cell("""async def manage_tokens():
    \"\"\"Demonstrate token management.\"\"\"
    try:
        # Get token for Azure services
        scope = "https://management.azure.com/.default"
        token = await credential.get_token(scope)
        
        print("✓ Successfully acquired token")
        print(f"Token expires in: {token.expires_on}")
        
        return token
    except Exception as e:
        print(f"× Error managing tokens: {str(e)}")
        return None

# Get and manage tokens
token = await manage_tokens()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Authentication**
   - Use DefaultAzureCredential
   - Implement proper error handling
   - Secure credential storage
   - Regular token rotation

2. **Security**
   - Follow least privilege
   - Monitor access patterns
   - Implement logging
   - Regular audits

3. **Health Applications**
   - Secure patient data
   - Implement RBAC
   - Monitor access
   - Regular reviews"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/sdk_identity_tutorial.ipynb"
    nbf.write(nb, notebook_path)
    print(f"Created {notebook_path}")
    return notebook_path

if __name__ == "__main__":
    notebook_path = create_notebook()
    
    # Run validation
    import sys
    sys.path.append('..')
    from validate_notebook import validate_notebook
    validate_notebook(notebook_path)
