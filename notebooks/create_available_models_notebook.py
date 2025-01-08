import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for exploring available models in Azure AI Foundry."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Exploring Available Models in Azure AI Foundry

This notebook guides you through discovering and exploring available models in Azure AI Foundry. You'll learn:
1. Listing available models
2. Filtering models by capability
3. Getting model details
4. Comparing model versions
5. Understanding model capabilities

## Prerequisites
- Completed authentication setup
- Azure AI Foundry access
- Required Python packages installed"""))

    # Environment setup
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os
import pandas as pd
from tabulate import tabulate
import json

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

    # List models
    cells.append(new_markdown_cell("""## List Available Models
Let's explore what models are available in Azure AI Foundry:"""))

    cells.append(new_code_cell("""def list_models():
    \"\"\"List and display available models.\"\"\"
    try:
        # Get all models
        models = list(client.models.list())
        
        # Create a DataFrame for better visualization
        model_data = []
        for model in models:
            model_data.append({
                'Name': model.name,
                'Version': model.version,
                'Category': model.category,
                'Description': model.description,
                'Status': model.status
            })
        
        df = pd.DataFrame(model_data)
        print(f"Found {len(models)} models\\n")
        print(tabulate(df, headers='keys', tablefmt='pipe', showindex=False))
        return models
        
    except Exception as e:
        print(f"× Error listing models: {str(e)}")
        return []

# List all models
models = list_models()"""))

    # Filter models
    cells.append(new_markdown_cell("""## Filter Models by Capability
Let's explore how to filter models based on their capabilities:"""))

    cells.append(new_code_cell("""def filter_models_by_capability(models, capability):
    \"\"\"Filter models by specific capability.\"\"\"
    try:
        filtered_models = [
            model for model in models 
            if capability in model.capabilities
        ]
        
        # Create DataFrame for filtered models
        filtered_data = []
        for model in filtered_models:
            filtered_data.append({
                'Name': model.name,
                'Version': model.version,
                'Description': model.description,
                'Capabilities': ', '.join(model.capabilities)
            })
        
        df = pd.DataFrame(filtered_data)
        print(f"Found {len(filtered_models)} models with {capability} capability\\n")
        print(tabulate(df, headers='keys', tablefmt='pipe', showindex=False))
        return filtered_models
        
    except Exception as e:
        print(f"× Error filtering models: {str(e)}")
        return []

# Filter for text generation models
text_models = filter_models_by_capability(models, 'text-generation')

# Filter for code generation models
code_models = filter_models_by_capability(models, 'code-generation')"""))

    # Model details
    cells.append(new_markdown_cell("""## Get Model Details
Let's examine detailed information about specific models:"""))

    cells.append(new_code_cell("""def get_model_details(model_name, version=None):
    \"\"\"Get detailed information about a specific model.\"\"\"
    try:
        # Get model details
        model = client.models.get(
            model_name=model_name,
            version=version
        )
        
        # Format details for display
        details = {
            'Name': model.name,
            'Version': model.version,
            'Category': model.category,
            'Description': model.description,
            'Status': model.status,
            'Capabilities': model.capabilities,
            'Parameters': model.parameters,
            'Performance Metrics': model.performance_metrics
        }
        
        print(f"Details for {model_name} (version {version or 'latest'}):\\n")
        print(json.dumps(details, indent=2))
        return model
        
    except Exception as e:
        print(f"× Error getting model details: {str(e)}")
        return None

# Get details for GPT-4
model_details = get_model_details('gpt-4')"""))

    # Compare versions
    cells.append(new_markdown_cell("""## Compare Model Versions
Let's compare different versions of a model:"""))

    cells.append(new_code_cell("""def compare_model_versions(model_name):
    \"\"\"Compare different versions of a model.\"\"\"
    try:
        # List all versions
        versions = list(client.models.list_versions(model_name=model_name))
        
        # Create comparison data
        comparison_data = []
        for version in versions:
            comparison_data.append({
                'Version': version.version,
                'Status': version.status,
                'Release Date': version.release_date,
                'Performance Score': version.performance_metrics.get('score', 'N/A'),
                'Changes': version.release_notes
            })
        
        df = pd.DataFrame(comparison_data)
        print(f"Version comparison for {model_name}:\\n")
        print(tabulate(df, headers='keys', tablefmt='pipe', showindex=False))
        return versions
        
    except Exception as e:
        print(f"× Error comparing versions: {str(e)}")
        return []

# Compare GPT-4 versions
versions = compare_model_versions('gpt-4')"""))

    # Model capabilities
    cells.append(new_markdown_cell("""## Understanding Model Capabilities
Let's explore the different capabilities of models:"""))

    cells.append(new_code_cell("""def analyze_capabilities():
    \"\"\"Analyze and summarize model capabilities.\"\"\"
    try:
        # Get all models
        all_models = list(client.models.list())
        
        # Collect unique capabilities
        capabilities = set()
        for model in all_models:
            capabilities.update(model.capabilities)
        
        # Count models per capability
        capability_counts = {cap: 0 for cap in capabilities}
        for model in all_models:
            for cap in model.capabilities:
                capability_counts[cap] += 1
        
        # Create summary DataFrame
        summary_data = [
            {
                'Capability': cap,
                'Model Count': count,
                'Example Models': ', '.join(
                    [m.name for m in all_models if cap in m.capabilities][:3]
                )
            }
            for cap, count in capability_counts.items()
        ]
        
        df = pd.DataFrame(summary_data)
        print("Capability Analysis:\\n")
        print(tabulate(df, headers='keys', tablefmt='pipe', showindex=False))
        return capability_counts
        
    except Exception as e:
        print(f"× Error analyzing capabilities: {str(e)}")
        return {}

# Analyze model capabilities
capability_analysis = analyze_capabilities()"""))

    # Best practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Model Selection**
   - Consider model capabilities vs. requirements
   - Check model performance metrics
   - Review version history
   - Consider resource requirements

2. **Version Management**
   - Track version changes
   - Test new versions before deployment
   - Plan for version updates
   - Monitor version deprecation

3. **Performance Considerations**
   - Monitor model performance
   - Consider resource usage
   - Track costs
   - Implement caching when appropriate

4. **Security and Compliance**
   - Review data handling requirements
   - Check regional availability
   - Verify compliance certifications
   - Monitor usage patterns"""))

    # Cleanup
    cells.append(new_markdown_cell("""## Next Steps

1. Choose appropriate models for your use case
2. Deploy selected models
3. Monitor model performance
4. Plan for version updates

Remember to clean up any test resources when you're done!"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/available_models.ipynb"
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
