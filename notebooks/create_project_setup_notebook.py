import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for the Project Setup section.
    
    This notebook guides users through:
    1. Setting up environment variables
    2. Authenticating with Azure
    3. Creating and configuring an AI project
    4. Managing project resources
    5. Applying best practices
    
    Returns:
        str: Path to the created notebook
    """
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Create cells list
    cells = []
    
    # Add introduction
    cells.append(new_markdown_cell("""# Project Setup for Azure AI Foundry

This notebook guides you through setting up an AI project in Azure AI Foundry. You'll learn:
1. Creating a new AI project
2. Configuring project settings
3. Managing project resources
4. Best practices for project organization

## Prerequisites
- Completed authentication setup from previous notebook
- Azure AI Foundry access
- Required Python packages installed"""))

    # Add import cell
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os
import json

# Initialize credentials
try:
    credential = DefaultAzureCredential()
    print("✓ Successfully initialized DefaultAzureCredential")
except Exception as e:
    print(f"× Error initializing credentials: {str(e)}")"""))

    # Add client initialization
    cells.append(new_markdown_cell("""## Initialize AI Project Client
First, let's create our client instance using the credentials we set up:"""))

    cells.append(new_code_cell("""# Create AI Project client
try:
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Add project creation
    cells.append(new_markdown_cell("""## Create a New Project
Let's create a customer service AI project:"""))

    project_code = """def create_project(name="customer-service-agent", description="AI-powered customer service agent"):
    \"\"\"Create a new AI Foundry project.\"\"\"
    try:
        project = client.projects.create(
            name=name,
            description=description,
            tags={
                "environment": "development",
                "purpose": "customer-service",
                "workshop": "true"
            }
        )
        print(f"✓ Successfully created project: {project.name}")
        return project
    except Exception as e:
        print(f"× Error creating project: {str(e)}")
        return None

# Create the project
project = create_project()"""
    cells.append(new_code_cell(project_code))

    # Add project configuration
    config_md = """## Project Configuration
Configure project settings and resources:"""
    cells.append(new_markdown_cell(config_md))

    config_code = """def configure_project(project):
    \"\"\"Configure project settings.\"\"\"
    if not project:
        print("× No project to configure")
        return
    
    try:
        # Update project settings
        project = client.projects.update(
            project_name=project.name,
            settings={
                "deployment": {
                    "environment": "development",
                    "region": "eastus",
                    "sku": "standard"
                },
                "monitoring": {
                    "metrics_enabled": True,
                    "logging_level": "INFO"
                }
            }
        )
        print("✓ Successfully configured project settings")
    except Exception as e:
        print(f"× Error configuring project: {str(e)}")

# Configure the project
configure_project(project)"""
    cells.append(new_code_cell(config_code))

    # Add resource listing
    cells.append(new_markdown_cell("""## List Project Resources
View the resources associated with your project:"""))

    resources_code = """def list_project_resources(project_name):
    \"\"\"List resources in the project.\"\"\"
    try:
        resources = client.projects.list_resources(project_name=project_name)
        print("\nProject Resources:")
        for resource in resources:
            print(f"- {resource.name} ({resource.type})")
    except Exception as e:
        print(f"× Error listing resources: {str(e)}")

# List resources if project was created
if project:
    list_project_resources(project.name)"""
    cells.append(new_code_cell(resources_code))

    # Add best practices
    cells.append(new_markdown_cell("""## Project Organization Best Practices

1. **Naming Conventions**
   - Use descriptive, lowercase names
   - Include environment indicator
   - Add purpose/function identifier

2. **Resource Management**
   - Group related resources
   - Use consistent tagging
   - Regular cleanup of unused resources

3. **Access Control**
   - Implement role-based access
   - Regular permission reviews
   - Audit access logs"""))

    best_practices_code = """def apply_best_practices(project):
    \"\"\"Apply best practices to project.\"\"\"
    if not project:
        print("× No project to configure")
        return
    
    try:
        # Update project with best practice configurations
        project = client.projects.update(
            project_name=project.name,
            tags={
                "owner": "workshop-participant",
                "cost-center": "training",
                "environment": "development",
                "purpose": "customer-service",
                "created-date": "2024-01",
                "cleanup-after": "2024-02"
            }
        )
        print("✓ Successfully applied best practices")
        
        # Display project details
        print("\nProject Configuration:")
        print(f"Name: {project.name}")
        print(f"Description: {project.description}")
        print("Tags:")
        for key, value in project.tags.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"× Error applying best practices: {str(e)}")

# Apply best practices
if project:
    apply_best_practices(project)"""
    cells.append(new_code_cell(best_practices_code))

    # Add cleanup section
    cells.append(new_markdown_cell("""## Cleanup (Optional)
If you want to remove the project:"""))

    cleanup_code = """def cleanup_project(project_name):
    \"\"\"Delete the project and associated resources.\"\"\"
    try:
        client.projects.delete(project_name=project_name)
        print(f"✓ Successfully deleted project: {project_name}")
    except Exception as e:
        print(f"× Error deleting project: {str(e)}")

# Uncomment to cleanup (careful!)
# if project:
#     cleanup_project(project.name)"""
    cells.append(new_code_cell(cleanup_code))

    # Add next steps
    cells.append(new_markdown_cell("""## Next Steps
- Deploy models to your project
- Configure endpoints
- Set up monitoring
- Implement the customer service agent

Remember to clean up resources if you're done with the workshop!"""))

    # Add environment variable setup cell at the beginning
    cells.insert(1, new_code_cell("""# Set up environment variables for local testing
import os

# Check for required environment variables
required_vars = {
    "AZURE_SUBSCRIPTION_ID": os.getenv("AZURE_SUBSCRIPTION_ID"),
    "AZURE_RESOURCE_GROUP": os.getenv("AZURE_RESOURCE_GROUP"),
    "AZURE_TENANT_ID": os.getenv("AZURE_TENANT_ID"),
    "AZURE_CLIENT_ID": os.getenv("AZURE_CLIENT_ID"),
    "AZURE_CLIENT_SECRET": os.getenv("AZURE_CLIENT_SECRET")
}

# Check which variables are missing
missing_vars = [var for var, value in required_vars.items() if not value]

if missing_vars:
    print("× Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
    print("\\nPlease set these variables before running the notebook:")
    print("```bash")
    print("export AZURE_SUBSCRIPTION_ID='your-subscription-id'")
    print("export AZURE_RESOURCE_GROUP='your-resource-group'")
    print("export AZURE_TENANT_ID='your-tenant-id'")
    print("export AZURE_CLIENT_ID='your-client-id'")
    print("export AZURE_CLIENT_SECRET='your-client-secret'")
    print("```")
else:
    print("✓ All required environment variables are set")"""))

    # Set the notebook cells
    nb['cells'] = cells

    # Write the notebook
    notebook_path = "building_agent/project_setup.ipynb"
    nbf.write(nb, notebook_path)
    print(f"Created {notebook_path}")
    return notebook_path

if __name__ == "__main__":
    # Create the notebook
    notebook_path = create_notebook()
    
    # Run validation
    import sys
    sys.path.append('..')
    from validate_notebook import validate_notebook
    validate_notebook(notebook_path)
