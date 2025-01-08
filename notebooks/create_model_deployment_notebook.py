import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for model deployment in Azure AI Foundry."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Deploying Models in Azure AI Foundry

This notebook guides you through the process of deploying models in Azure AI Foundry. You'll learn:
1. Creating deployment configurations
2. Deploying models to endpoints
3. Managing deployments
4. Monitoring deployment status
5. Best practices for production deployments

## Prerequisites
- Completed authentication setup
- Azure AI Foundry access
- Required Python packages installed
- Selected model from Available Models section"""))

    # Environment setup
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os
import json
from datetime import datetime
import time

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

    # Create deployment configuration
    cells.append(new_markdown_cell("""## Create Deployment Configuration
Let's create a configuration for our model deployment:"""))

    cells.append(new_code_cell("""def create_deployment_config(model_name, endpoint_name):
    \"\"\"Create a deployment configuration for a model.\"\"\"
    try:
        # Define deployment configuration
        deployment_config = {
            "name": f"deployment-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "model": {
                "name": model_name,
                "version": "latest"  # You can specify a specific version if needed
            },
            "endpoint_name": endpoint_name,
            "scale_settings": {
                "scale_type": "standard",
                "min_instances": 1,
                "max_instances": 2
            },
            "compute": {
                "machine_type": "Standard_DS3_v2",  # Adjust based on your needs
                "instance_count": 1
            }
        }
        
        print("Deployment Configuration:")
        print(json.dumps(deployment_config, indent=2))
        return deployment_config
        
    except Exception as e:
        print(f"× Error creating deployment configuration: {str(e)}")
        return None

# Create deployment config for GPT-4
deployment_config = create_deployment_config(
    model_name="gpt-4",
    endpoint_name="customer-service-endpoint"
)"""))

    # Deploy model
    cells.append(new_markdown_cell("""## Deploy Model
Now let's deploy the model using our configuration:"""))

    cells.append(new_code_cell("""def deploy_model(deployment_config):
    \"\"\"Deploy a model using the provided configuration.\"\"\"
    try:
        # Create deployment
        deployment = client.deployments.create(
            deployment_name=deployment_config["name"],
            model_name=deployment_config["model"]["name"],
            model_version=deployment_config["model"]["version"],
            endpoint_name=deployment_config["endpoint_name"],
            scale_settings=deployment_config["scale_settings"],
            compute=deployment_config["compute"]
        )
        
        print(f"✓ Deployment {deployment.name} created successfully")
        return deployment
        
    except Exception as e:
        print(f"× Error deploying model: {str(e)}")
        return None

# Deploy the model
deployment = deploy_model(deployment_config)"""))

    # Monitor deployment
    cells.append(new_markdown_cell("""## Monitor Deployment Status
Let's monitor the status of our deployment:"""))

    cells.append(new_code_cell("""def monitor_deployment(deployment_name, endpoint_name, timeout_minutes=10):
    \"\"\"Monitor the status of a deployment until it's ready or timeout.\"\"\"
    try:
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        
        while True:
            # Get current status
            deployment = client.deployments.get(
                deployment_name=deployment_name,
                endpoint_name=endpoint_name
            )
            
            print(f"Status: {deployment.status}")
            
            if deployment.status == "Succeeded":
                print("✓ Deployment completed successfully!")
                return deployment
            elif deployment.status == "Failed":
                print(f"× Deployment failed: {deployment.status_message}")
                return None
            
            # Check timeout
            if time.time() - start_time > timeout_seconds:
                print(f"× Deployment monitoring timed out after {timeout_minutes} minutes")
                return None
            
            # Wait before next check
            time.sleep(30)
            
    except Exception as e:
        print(f"× Error monitoring deployment: {str(e)}")
        return None

# Monitor our deployment
if deployment:
    final_deployment = monitor_deployment(
        deployment_name=deployment.name,
        endpoint_name=deployment_config["endpoint_name"]
    )"""))

    # Manage deployments
    cells.append(new_markdown_cell("""## Manage Deployments
Let's explore how to manage existing deployments:"""))

    cells.append(new_code_cell("""def list_deployments(endpoint_name):
    \"\"\"List all deployments for an endpoint.\"\"\"
    try:
        deployments = list(client.deployments.list(endpoint_name=endpoint_name))
        
        print(f"Deployments for endpoint {endpoint_name}:")
        for d in deployments:
            print(f"\\nDeployment: {d.name}")
            print(f"Status: {d.status}")
            print(f"Model: {d.model.name} (version {d.model.version})")
            print(f"Created: {d.created_time}")
            print(f"Last Modified: {d.last_modified_time}")
        
        return deployments
        
    except Exception as e:
        print(f"× Error listing deployments: {str(e)}")
        return []

# List deployments
deployments = list_deployments(deployment_config["endpoint_name"])"""))

    # Update deployment
    cells.append(new_markdown_cell("""## Update Deployment
Let's see how to update an existing deployment:"""))

    cells.append(new_code_cell("""def update_deployment(deployment_name, endpoint_name, scale_settings=None):
    \"\"\"Update an existing deployment's configuration.\"\"\"
    try:
        # Get current deployment
        deployment = client.deployments.get(
            deployment_name=deployment_name,
            endpoint_name=endpoint_name
        )
        
        # Update scale settings if provided
        if scale_settings:
            deployment.scale_settings = scale_settings
        
        # Apply updates
        updated_deployment = client.deployments.update(
            deployment_name=deployment_name,
            endpoint_name=endpoint_name,
            scale_settings=deployment.scale_settings
        )
        
        print(f"✓ Deployment {deployment_name} updated successfully")
        return updated_deployment
        
    except Exception as e:
        print(f"× Error updating deployment: {str(e)}")
        return None

# Update deployment scale settings
if deployment:
    new_scale_settings = {
        "scale_type": "standard",
        "min_instances": 2,
        "max_instances": 4
    }
    
    updated_deployment = update_deployment(
        deployment_name=deployment.name,
        endpoint_name=deployment_config["endpoint_name"],
        scale_settings=new_scale_settings
    )"""))

    # Cleanup
    cells.append(new_markdown_cell("""## Cleanup
When you're done testing, you can clean up your deployments:"""))

    cells.append(new_code_cell("""def cleanup_deployment(deployment_name, endpoint_name):
    \"\"\"Delete a deployment.\"\"\"
    try:
        client.deployments.delete(
            deployment_name=deployment_name,
            endpoint_name=endpoint_name
        )
        print(f"✓ Deployment {deployment_name} deleted successfully")
        
    except Exception as e:
        print(f"× Error deleting deployment: {str(e)}")

# Uncomment to clean up the deployment
# if deployment:
#     cleanup_deployment(
#         deployment_name=deployment.name,
#         endpoint_name=deployment_config["endpoint_name"]
#     )"""))

    # Best practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Deployment Planning**
   - Start with minimal instances and scale based on usage
   - Use appropriate machine types for your workload
   - Consider costs and performance requirements
   - Plan for high availability if needed

2. **Monitoring and Maintenance**
   - Monitor deployment status regularly
   - Set up alerts for deployment issues
   - Keep track of resource usage
   - Plan for version updates

3. **Resource Management**
   - Clean up unused deployments
   - Optimize instance counts
   - Monitor costs
   - Use tags for better organization

4. **Security**
   - Use proper authentication
   - Implement network security
   - Monitor access patterns
   - Regular security reviews

5. **Production Considerations**
   - Test thoroughly before production
   - Implement proper error handling
   - Plan for scaling
   - Document deployment configurations"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/model_deployment.ipynb"
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
