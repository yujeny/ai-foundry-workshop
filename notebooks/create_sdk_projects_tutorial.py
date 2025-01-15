import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure AI Projects SDK tutorial."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure AI Projects SDK Tutorial

This notebook demonstrates how to use the Azure AI Projects SDK for health and dietary applications.

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## What You'll Learn
- Creating and managing AI projects
- Configuring project settings
- Managing resources
- Best practices for health applications"""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os
import json
from datetime import datetime

# Check environment setup
try:
    # Initialize credentials
    credential = DefaultAzureCredential()
    
    # Create client
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Project Creation
    cells.append(new_markdown_cell("""## Creating a Health Advisor Project

Let's create a project for health and dietary advice:"""))

    cells.append(new_code_cell("""def create_health_project():
    \"\"\"Create a new health advisor project.\"\"\"
    try:
        # Create project
        project = client.projects.create(
            name=f"health-advisor-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            description="AI-powered health and dietary advice project",
            tags={
                "domain": "healthcare",
                "features": "dietary-planning,health-advice",
                "environment": "development"
            }
        )
        print(f"✓ Created project: {project.name}")
        return project
    except Exception as e:
        print(f"× Error creating project: {str(e)}")
        return None

# Create the project
project = create_health_project()"""))

    # Project Configuration
    cells.append(new_markdown_cell("""## Configuring Project Settings

Configure the project with health-specific settings:"""))

    cells.append(new_code_cell("""def configure_health_project(project):
    \"\"\"Configure health project settings.\"\"\"
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
                },
                "safety": {
                    "content_filtering": True,
                    "medical_disclaimer_required": True
                }
            }
        )
        print("✓ Successfully configured project settings")
    except Exception as e:
        print(f"× Error configuring project: {str(e)}")

# Configure the project
if project:
    configure_health_project(project)"""))

    # Resource Management
    cells.append(new_markdown_cell("""## Managing Project Resources

View and manage resources in your health advisor project:"""))

    cells.append(new_code_cell("""def list_project_resources(project_name):
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
    list_project_resources(project.name)"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Project Organization**
   - Use descriptive names
   - Implement proper tagging
   - Regular resource cleanup
   - Monitor usage

2. **Security**
   - Implement role-based access
   - Regular security reviews
   - Monitor access patterns

3. **Health Data Handling**
   - Include medical disclaimers
   - Implement content safety
   - Regular compliance checks"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/sdk_projects_tutorial.ipynb"
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
