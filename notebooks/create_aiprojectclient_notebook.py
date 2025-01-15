import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for working with AIProjectClient."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Working with AIProjectClient

This notebook demonstrates how to use the AIProjectClient to manage AI projects and resources in Azure AI Foundry. You'll learn:
1. Initializing AIProjectClient
2. Managing AI Projects
3. Working with Resources
4. Error Handling and Best Practices

## Prerequisites
- Completed authentication setup
- Azure AI Foundry access
- Required Python packages installed"""))

    # Environment setup
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.evaluation import TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument
import os
import json
from datetime import datetime

# Check environment variables
required_vars = {
    "AZURE_SUBSCRIPTION_ID": os.getenv("AZURE_SUBSCRIPTION_ID"),
    "AZURE_RESOURCE_GROUP": os.getenv("AZURE_RESOURCE_GROUP")
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    print("× Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
else:
    print("✓ All required environment variables are set")"""))

    # Client initialization
    cells.append(new_markdown_cell("""## Initialize AIProjectClient
First, let's create an instance of AIProjectClient:"""))

    cells.append(new_code_cell("""def initialize_client():
    \"\"\"Initialize AIProjectClient with error handling.\"\"\"
    try:
        # Initialize credentials
        credential = DefaultAzureCredential()
        print("✓ Successfully initialized DefaultAzureCredential")
        
        # Create client
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        print("✓ Successfully initialized AIProjectClient")
        return client
        
    except Exception as e:
        print(f"× Error initializing client: {str(e)}")
        return None

# Initialize client
client = initialize_client()"""))

    # Project management
    cells.append(new_markdown_cell("""## Project Management
Let's explore common project management operations:"""))

    cells.append(new_code_cell("""def list_projects():
    \"\"\"List all AI projects in the resource group.\"\"\"
    try:
        projects = list(client.projects.list())
        print(f"Found {len(projects)} projects:")
        for project in projects:
            print(f"- {project.name}")
            print(f"  Description: {project.description}")
            print(f"  Status: {project.status}")
            print()
        return projects
    except Exception as e:
        print(f"× Error listing projects: {str(e)}")
        return []

# List existing projects
projects = list_projects()"""))

    # Resource management
    cells.append(new_markdown_cell("""## Resource Management
Now let's look at managing resources within a project:"""))

    cells.append(new_code_cell("""def manage_resources(project_name):
    \"\"\"Demonstrate resource management operations.\"\"\"
    try:
        # List resources
        resources = list(client.projects.list_resources(project_name=project_name))
        print(f"\nResources in project {project_name}:")
        for resource in resources:
            print(f"- {resource.name} ({resource.type})")
            print(f"  Status: {resource.status}")
            print(f"  Region: {resource.region}")
            print()
        return resources
    except Exception as e:
        print(f"× Error managing resources: {str(e)}")
        return []

# If we have projects, examine resources in the first one
if projects:
    resources = manage_resources(projects[0].name)"""))

    # Project operations
    cells.append(new_markdown_cell("""## Common Project Operations
Let's explore some common operations you might perform on projects:"""))

    cells.append(new_code_cell("""def project_operations():
    \"\"\"Demonstrate common project operations.\"\"\"
    try:
        # Create a new health advisor project
        project_name = f"health-advisor-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        new_project = client.projects.create(
            name=project_name,
            description="Health and dietary advice AI project",
            tags={
                "environment": "development",
                "purpose": "health-advisor",
                "domain": "healthcare",
                "features": "bmi-calculator,meal-planning,diet-restrictions",
                "created-by": "workshop"
            }
        )
        print(f"✓ Created project: {new_project.name}")
        
        # Update project
        updated_project = client.projects.update(
            project_name=project_name,
            description="Updated demo project description",
            tags={
                "environment": "development",
                "purpose": "demo",
                "created-by": "workshop",
                "last-modified": datetime.now().isoformat()
            }
        )
        print(f"✓ Updated project: {updated_project.name}")
        
        # Get project details
        project_details = client.projects.get(project_name=project_name)
        print("\nProject Details:")
        print(f"Name: {project_details.name}")
        print(f"Description: {project_details.description}")
        print("Tags:")
        for key, value in project_details.tags.items():
            print(f"  {key}: {value}")
        
        return project_details
        
    except Exception as e:
        print(f"× Error in project operations: {str(e)}")
        return None

# Perform project operations
project_details = project_operations()"""))

    # Error handling
    cells.append(new_markdown_cell("""## Error Handling and Best Practices
Let's look at some common errors and how to handle them:"""))

    cells.append(new_code_cell("""def demonstrate_error_handling():
    \"\"\"Show common errors and how to handle them.\"\"\"
    try:
        # Try to get a non-existent health advisor project
        print("Attempting to get non-existent project...")
        client.projects.get(project_name="health-advisor-non-existent")
    except Exception as e:
        print("✓ Successfully caught error:")
        print(f"  {str(e)}")
        print("  This is expected when the project doesn't exist")
    
    try:
        # Try to create a project with invalid characters
        print("\nAttempting to create project with invalid name...")
        client.projects.create(
            name="Invalid Project Name!",
            description="This should fail"
        )
    except Exception as e:
        print("✓ Successfully caught error:")
        print(f"  {str(e)}")
        print("  Project names must be lowercase alphanumeric with hyphens")

# Demonstrate error handling
demonstrate_error_handling()"""))

    # Cleanup
    cells.append(new_markdown_cell("""## Cleanup
If you created any demo projects, you can clean them up:"""))

    cells.append(new_code_cell("""def cleanup_demo_projects():
    \"\"\"Clean up any projects created during this demo.\"\"\"
    try:
        # List all projects
        projects = list(client.projects.list())
        
        # Find and delete health advisor projects
        for project in projects:
            if project.name.startswith("health-advisor-"):
                print(f"Cleaning up project: {project.name}")
                client.projects.delete(project_name=project.name)
                print(f"✓ Deleted project: {project.name}")
    
    except Exception as e:
        print(f"× Error during cleanup: {str(e)}")

# Uncomment to clean up demo projects
# cleanup_demo_projects()"""))

    # Best practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Error Handling**
   - Always wrap API calls in try-except blocks
   - Log errors appropriately
   - Handle specific exceptions when possible

2. **Resource Management**
   - Clean up unused resources
   - Use meaningful names and tags
   - Monitor resource usage

3. **Security**
   - Use environment variables for credentials
   - Implement proper access control
   - Regular security reviews

4. **Performance**
   - Batch operations when possible
   - Implement retry logic for transient failures
   - Monitor API usage limits"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/aiprojectclient.ipynb"
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
