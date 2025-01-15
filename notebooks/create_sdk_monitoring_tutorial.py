import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure Monitor OpenTelemetry tutorial."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure Monitor OpenTelemetry Tutorial

This notebook demonstrates how to monitor health advice applications using Azure Monitor OpenTelemetry.

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## What You'll Learn
- Setting up OpenTelemetry instrumentation
- Monitoring health advice operations
- Analyzing telemetry data
- Best practices for monitoring"""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
import azure.monitor.opentelemetry._autoinstrument
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os
import json

# Initialize client
try:
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=DefaultAzureCredential()
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Basic Monitoring
    cells.append(new_markdown_cell("""## Monitoring Health Advice Operations

Monitor operations in your health advice application:"""))

    cells.append(new_code_cell("""async def monitor_health_operations():
    \"\"\"Monitor health advice operations.\"\"\"
    try:
        # OpenTelemetry is automatically instrumenting operations
        
        # Perform some operations to monitor
        project = await client.projects.create(
            name=f"health-monitor-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            description="Health monitoring example",
            tags={
                "domain": "healthcare",
                "purpose": "monitoring"
            }
        )
        
        # List resources
        resources = await client.projects.list_resources(
            project_name=project.name
        )
        
        print("✓ Operations completed successfully")
        print("Check Azure Monitor for telemetry data")
        
        return {
            "project": project.name,
            "resource_count": len(list(resources))
        }
    except Exception as e:
        print(f"× Error in operations: {str(e)}")
        return None

# Run monitored operations
result = await monitor_health_operations()
print(f"Operation result: {result}")"""))

    # Custom Metrics
    cells.append(new_markdown_cell("""## Custom Health Metrics

Add custom metrics for health-specific monitoring:"""))

    cells.append(new_code_cell("""from opentelemetry import metrics
from datetime import datetime

# Get meter
meter = metrics.get_meter(__name__)

# Create counters
advice_requests = meter.create_counter(
    name="health_advice_requests",
    description="Number of health advice requests"
)

dietary_plans = meter.create_counter(
    name="dietary_plans_generated",
    description="Number of dietary plans generated"
)

async def track_health_metrics():
    \"\"\"Track custom health metrics.\"\"\"
    try:
        # Simulate some health advice operations
        advice_requests.add(1, {"type": "dietary"})
        dietary_plans.add(1, {"plan_type": "diabetes"})
        
        print("✓ Metrics recorded successfully")
        print("Check Azure Monitor for custom metrics")
        
    except Exception as e:
        print(f"× Error recording metrics: {str(e)}")

# Record custom metrics
await track_health_metrics()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Instrumentation**
   - Enable automatic instrumentation
   - Add custom metrics where needed
   - Monitor key operations
   - Track performance metrics

2. **Health Metrics**
   - Track advice requests
   - Monitor response times
   - Record success rates
   - Track user interactions

3. **Analysis**
   - Review telemetry data
   - Analyze patterns
   - Set up alerts
   - Monitor trends"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/sdk_monitoring_tutorial.ipynb"
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
