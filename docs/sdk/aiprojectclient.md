# Working with AIProjectClient

The AIProjectClient is your central interface for programmatic interaction with Azure AI Foundry. It provides comprehensive access to project management, model operations, and deployment capabilities.

## Project Management

### 1. Project Creation and Setup
```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os

def create_ai_project():
    """Create and configure a new AI project."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Create project
        project = client.projects.create(
            name="my-ai-project",
            description="AI project for development and testing",
            location="eastus",
            tags={
                "environment": "development",
                "team": "ai-research"
            }
        )
        
        # Configure project settings
        project_config = {
            "compute": {
                "vm_size": "Standard_DS3_v2",
                "min_nodes": 1,
                "max_nodes": 4
            },
            "security": {
                "network_isolation": True,
                "encryption_enabled": True
            },
            "monitoring": {
                "metrics_enabled": True,
                "logging_level": "Information"
            }
        }
        
        client.projects.update_configuration(
            project_name=project.name,
            configuration=project_config
        )
        
        return project
    except Exception as e:
        print(f"Error creating AI project: {str(e)}")
        raise
```

### 2. Resource Management
```python
def manage_project_resources(project_name: str):
    """Monitor and manage project resources."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Get resource usage
        usage = client.projects.get_resource_usage(project_name)
        
        # Monitor deployments
        deployments = client.deployments.list(project_name)
        
        # Get quota information
        quota = client.projects.get_quota(project_name)
        
        # Manage endpoints
        endpoints = client.endpoints.list(project_name)
        
        resource_status = {
            "compute_usage": usage.compute,
            "storage_usage": usage.storage,
            "active_deployments": len(deployments),
            "quota_remaining": quota,
            "endpoint_count": len(endpoints)
        }
        
        return resource_status
    except Exception as e:
        print(f"Error managing project resources: {str(e)}")
        raise
```

### 3. Project Configuration
```python
def configure_project_integrations(project_name: str):
    """Set up project integrations and monitoring."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Configure monitoring
        monitoring_config = {
            "workspace_id": os.getenv("LOG_ANALYTICS_WORKSPACE_ID"),
            "metrics_collection": True,
            "log_level": "Information",
            "custom_dimensions": {
                "environment": "production",
                "service": "ai-foundry"
            }
        }
        
        # Set up security
        security_config = {
            "network_isolation": True,
            "private_endpoints": True,
            "encryption_scope": "Microsoft.KeyVault",
            "key_rotation_days": 90
        }
        
        # Configure integrations
        integration_config = {
            "source_control": {
                "type": "GitHub",
                "repository": "org/repo",
                "branch": "main"
            },
            "container_registry": {
                "registry_name": "myacr",
                "resource_group": os.getenv("AZURE_RESOURCE_GROUP")
            }
        }
        
        # Apply configurations
        client.projects.update_configuration(
            project_name=project_name,
            monitoring=monitoring_config,
            security=security_config,
            integrations=integration_config
        )
        
        return True
    except Exception as e:
        print(f"Error configuring project: {str(e)}")
        raise
```

## Model Operations

### 1. Model Discovery
```python
def discover_models():
    """List and filter available models."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # List all available models
        all_models = client.models.list()
        
        # Filter models by capability
        text_models = [m for m in all_models if "text-generation" in m.capabilities]
        code_models = [m for m in all_models if "code-generation" in m.capabilities]
        
        # Get detailed information for specific model
        model_details = client.models.get(
            model_name="gpt-4",
            version="1"
        )
        
        # Compare model versions
        model_versions = client.models.list_versions(
            model_name="gpt-4"
        )
        
        return {
            "text_models": text_models,
            "code_models": code_models,
            "model_details": model_details,
            "versions": model_versions
        }
    except Exception as e:
        print(f"Error discovering models: {str(e)}")
        raise
```

### 2. Model Management
```python
def manage_model_deployment(model_name: str, version: str):
    """Deploy and manage model configurations."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Deploy model
        deployment = client.models.deploy(
            model_name=model_name,
            version=version,
            deployment_name=f"{model_name}-deployment",
            scale_settings={
                "scale_type": "Standard",
                "min_replicas": 1,
                "max_replicas": 3
            }
        )
        
        # Update configuration
        client.models.update_deployment(
            deployment_name=deployment.name,
            configuration={
                "request_timeout": 30,
                "max_tokens": 2000,
                "temperature": 0.7
            }
        )
        
        # Monitor performance
        metrics = client.models.get_deployment_metrics(
            deployment_name=deployment.name,
            metric_names=["requests", "latency", "tokens"]
        )
        
        return {
            "deployment": deployment,
            "metrics": metrics
        }
    except Exception as e:
        print(f"Error managing model deployment: {str(e)}")
        raise
```

### 3. Deployment Control
```python
def control_deployment(deployment_name: str):
    """Manage deployment endpoints and scaling."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Get endpoint information
        endpoint = client.endpoints.get(deployment_name)
        
        # Update scaling settings
        client.endpoints.update_scale_settings(
            deployment_name=deployment_name,
            scale_settings={
                "scale_type": "Standard",
                "min_replicas": 2,
                "max_replicas": 5,
                "target_utilization": 70
            }
        )
        
        # Configure auto-scaling
        client.endpoints.configure_autoscaling(
            deployment_name=deployment_name,
            rules=[
                {
                    "metric": "RequestsPerSecond",
                    "threshold": 100,
                    "operator": "GreaterThan",
                    "scale_increment": 1
                }
            ]
        )
        
        # Monitor performance
        performance = client.endpoints.get_performance_metrics(
            deployment_name=deployment_name,
            time_range="1h"
        )
        
        return {
            "endpoint": endpoint,
            "performance": performance
        }
    except Exception as e:
        print(f"Error controlling deployment: {str(e)}")
        raise
```

## Agent Operations

### 1. Agent Lifecycle
```python
def manage_agent_lifecycle(agent_name: str):
    """Create and manage AI agents."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Create new agent
        agent = client.agents.create(
            name=agent_name,
            description="Customer service agent",
            model_name="gpt-4",
            deployment_name="customer-service-v1",
            configuration={
                "max_tokens": 1000,
                "temperature": 0.7,
                "capabilities": ["conversation", "task-management"]
            }
        )
        
        # Update agent configuration
        client.agents.update_configuration(
            agent_name=agent_name,
            configuration={
                "context_window": 4000,
                "response_format": "markdown",
                "custom_data": {
                    "knowledge_base": "customer-service-kb"
                }
            }
        )
        
        # Monitor agent status
        status = client.agents.get_status(agent_name)
        
        # Manage versions
        versions = client.agents.list_versions(agent_name)
        
        return {
            "agent": agent,
            "status": status,
            "versions": versions
        }
    except Exception as e:
        print(f"Error managing agent lifecycle: {str(e)}")
        raise
```

### 2. Integration
```python
def setup_agent_integrations(agent_name: str):
    """Configure agent integrations and connections."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Set up service connections
        service_connections = {
            "knowledge_base": {
                "type": "cognitive-search",
                "endpoint": os.getenv("SEARCH_ENDPOINT"),
                "key": os.getenv("SEARCH_KEY"),
                "index_name": "customer-kb"
            },
            "storage": {
                "type": "blob-storage",
                "connection_string": os.getenv("STORAGE_CONNECTION")
            }
        }
        
        # Configure data handling
        data_config = {
            "input_validation": True,
            "output_formatting": True,
            "data_retention_days": 30,
            "privacy_level": "high"
        }
        
        # Apply configurations
        client.agents.configure_integrations(
            agent_name=agent_name,
            configuration=integration_config,
            services=service_connections,
            data_handling=data_config
        )
        
        return True
    except Exception as e:
        print(f"Error setting up agent integrations: {str(e)}")
        raise
```

## Best Practices

### 1. Error Handling
- Implement retry logic
- Handle rate limits
- Log errors properly
- Monitor operations

### 2. Performance Optimization
- Resource efficiency
- Batch operations
- Caching strategies
- Connection management

### 3. Security Considerations
- Access control
- Credential management
- Audit logging
- Compliance monitoring

## Common Patterns

### 1. Project Setup
- Initialize client
- Configure settings
- Validate access
- Set up monitoring

### 2. Resource Management
- Track usage
- Handle quotas
- Monitor costs
- Optimize resources

### 3. Operational Maintenance
- Regular health checks
- Performance monitoring
- Security updates
- Backup strategies

## Interactive Workshop

For hands-on practice with AIProjectClient, try our interactive notebook:

[Launch AIProjectClient Workshop](../building_agent/aiprojectclient/aiprojectclient.ipynb)

This notebook provides:
- Practical examples of AIProjectClient usage
- Project management operations
- Resource management examples
- Error handling and best practices
- Interactive troubleshooting guide

Next: [Listing Models](../models/listing.md)
