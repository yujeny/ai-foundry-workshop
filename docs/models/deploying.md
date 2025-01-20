# 🚀 Deploying Your Customer Service Model

Let's deploy a GPT model optimized for customer service interactions. Get your health advisor ready to help users achieve their fitness goals! 🏃‍♀️ 💪 This will take about 15 minutes.

## Quick Model Deployment

### 1. Select the Model
```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os

def deploy_customer_service_model():
    """Deploy a GPT model for customer service."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Configure deployment
        deployment_config = {
            "model": {
                "name": "gpt-35-turbo",  # or your preferred model
                "version": "0301"
            },
            "compute": {
                "instance_type": "Standard_DS3_v2",
                "instance_count": 1
            },
            "settings": {
                "max_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.95
            }
        }
        
        # Create deployment
        deployment = client.models.deploy(
            model_name=deployment_config["model"]["name"],
            deployment_name="customer-service-v1",
            configuration=deployment_config
        )
        
        return deployment
    except Exception as e:
        print(f"Deployment error: {str(e)}")
        raise

## Deployment Process

### 1. Environment Setup
```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os

def setup_deployment_environment():
    """Set up the environment for model deployment."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Configure deployment environment
        environment_config = {
            "compute": {
                "vm_size": "Standard_DS3_v2",
                "min_nodes": 1,
                "max_nodes": 4
            },
            "network": {
                "virtual_network": "ai-vnet",
                "subnet": "model-subnet",
                "private_link_enabled": True
            },
            "security": {
                "encryption_type": "CustomerManaged",
                "key_vault_id": os.getenv("KEY_VAULT_ID"),
                "network_isolation": True
            },
            "monitoring": {
                "workspace_id": os.getenv("LOG_ANALYTICS_WORKSPACE_ID"),
                "metrics_enabled": True,
                "logs_enabled": True
            }
        }
        
        # Apply environment configuration
        client.deployments.configure_environment(
            environment_config=environment_config
        )
        
        return True
    except Exception as e:
        print(f"Error setting up deployment environment: {str(e)}")
        raise
```

### 2. Deployment Configuration
```python
def configure_model_deployment(model_name: str, version: str):
    """Configure model deployment settings."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Define deployment configuration
        deployment_config = {
            "compute": {
                "instance_type": "Standard_DS3_v2",
                "instance_count": 2,
                "autoscale_enabled": True,
                "min_replicas": 1,
                "max_replicas": 5
            },
            "endpoint": {
                "throughput_limit": 100,
                "max_concurrent_requests": 20,
                "request_timeout": 30
            },
            "performance": {
                "max_tokens": 2000,
                "temperature": 0.7,
                "top_p": 0.95,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        }
        
        # Apply deployment configuration
        deployment = client.models.create_deployment(
            model_name=model_name,
            version=version,
            deployment_name=f"{model_name}-deployment",
            configuration=deployment_config
        )
        
        return deployment
    except Exception as e:
        print(f"Error configuring model deployment: {str(e)}")
        raise
```

### 3. Deployment Methods
```python
def deploy_model_with_strategy(model_name: str, version: str, strategy: str):
    """Deploy model using specified deployment strategy."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        if strategy == "single":
            # Single model deployment
            deployment = client.models.deploy(
                model_name=model_name,
                version=version,
                deployment_name=f"{model_name}-prod"
            )
            
        elif strategy == "multi":
            # Multi-model deployment
            deployment = client.models.deploy_multi(
                models=[
                    {"name": model_name, "version": version},
                    {"name": f"{model_name}-backup", "version": "latest"}
                ],
                deployment_name=f"{model_name}-multi"
            )
            
        elif strategy == "ab":
            # A/B testing deployment
            deployment = client.models.deploy_ab_test(
                models=[
                    {
                        "name": model_name,
                        "version": version,
                        "traffic_percentage": 90
                    },
                    {
                        "name": model_name,
                        "version": "experimental",
                        "traffic_percentage": 10
                    }
                ],
                deployment_name=f"{model_name}-ab"
            )
            
        elif strategy == "staged":
            # Staged rollout
            deployment = client.models.deploy_staged(
                model_name=model_name,
                version=version,
                deployment_name=f"{model_name}-staged",
                stages=[
                    {"percentage": 10, "duration_hours": 24},
                    {"percentage": 50, "duration_hours": 24},
                    {"percentage": 100, "duration_hours": 24}
                ]
            )
        
        return deployment
    except Exception as e:
        print(f"Error deploying model: {str(e)}")
        raise
```

## Production Considerations

### 1. Performance Optimization
```python
def optimize_deployment_performance(deployment_name: str):
    """Optimize deployment performance settings."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Get current performance metrics
        metrics = client.deployments.get_metrics(
            deployment_name=deployment_name,
            metric_names=[
                "latency_p95",
                "requests_per_second",
                "token_utilization",
                "compute_utilization"
            ]
        )
        
        # Optimize based on metrics
        optimization_config = {
            "compute": {
                "instance_type": "Standard_DS4_v2" if metrics["compute_utilization"] > 80 else "Standard_DS3_v2",
                "instance_count": max(1, int(metrics["requests_per_second"] / 50))
            },
            "performance": {
                "cache_enabled": True,
                "batch_size": 32,
                "optimization_level": "memory_optimized" if metrics["token_utilization"] > 80 else "balanced"
            }
        }
        
        # Apply optimization
        client.deployments.update_configuration(
            deployment_name=deployment_name,
            configuration=optimization_config
        )
        
        return True
    except Exception as e:
        print(f"Error optimizing deployment performance: {str(e)}")
        raise
```

### 2. Monitoring and Logging
```python
def setup_deployment_monitoring(deployment_name: str):
    """Configure comprehensive monitoring and logging."""
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
            "metrics": {
                "latency": True,
                "throughput": True,
                "error_rate": True,
                "token_usage": True,
                "compute_usage": True
            },
            "logging": {
                "level": "Information",
                "request_logging": True,
                "response_logging": True,
                "error_logging": True
            },
            "alerts": [
                {
                    "metric": "error_rate",
                    "threshold": 0.01,
                    "window_minutes": 5,
                    "action": "notify"
                },
                {
                    "metric": "latency_p95",
                    "threshold": 1000,
                    "window_minutes": 5,
                    "action": "scale"
                }
            ]
        }
        
        # Apply monitoring configuration
        client.deployments.configure_monitoring(
            deployment_name=deployment_name,
            monitoring_config=monitoring_config
        )
        
        return True
    except Exception as e:
        print(f"Error setting up monitoring: {str(e)}")
        raise
```

### 3. Security Management
```python
def configure_deployment_security(deployment_name: str):
    """Configure security settings for deployment."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Configure security settings
        security_config = {
            "authentication": {
                "type": "aad",
                "required_roles": ["AI.User", "AI.Admin"],
                "token_expiration_hours": 24
            },
            "network": {
                "private_endpoint_enabled": True,
                "allowed_ip_ranges": ["10.0.0.0/24"],
                "virtual_network_rules": [
                    {
                        "subnet_id": "/subscriptions/.../resourceGroups/.../providers/Microsoft.Network/virtualNetworks/vnet/subnets/subnet",
                        "ignore_missing_endpoint": False
                    }
                ]
            },
            "data": {
                "encryption_type": "CustomerManaged",
                "key_vault_key_id": os.getenv("KEY_VAULT_KEY_ID"),
                "double_encryption_enabled": True
            },
            "compliance": {
                "audit_logging_enabled": True,
                "diagnostic_settings_enabled": True,
                "retention_days": 90
            }
        }
        
        # Apply security configuration
        client.deployments.configure_security(
            deployment_name=deployment_name,
            security_config=security_config
        )
        
        return True
    except Exception as e:
        print(f"Error configuring security: {str(e)}")
        raise
```

## Scaling Strategies

### 1. Horizontal Scaling
- Instance management
- Load balancing
- Traffic distribution
- Resource allocation

### 2. Vertical Scaling
- Resource adjustment
- Performance tuning
- Capacity planning
- Cost management

### 3. Auto-scaling
- Scaling rules
- Trigger conditions
- Resource limits
- Performance targets

## Best Practices

### 1. Deployment Strategy
- Gradual rollout
- Version control
- Rollback planning
- Documentation

### 2. Performance Management
- Regular monitoring
- Performance tuning
- Resource optimization
- Cost tracking

### 3. Maintenance Planning
- Update strategy
- Backup procedures
- Disaster recovery
- Support processes

## Interactive Workshop

For hands-on practice with model deployment in Azure AI Foundry, try our interactive notebook:

[Launch Model Deployment Workshop](../2-notebooks/2-agent_service/6-agents-az-functions.ipynb)

This notebook provides:
- Step-by-step deployment configuration
- Model deployment process walkthrough
- Deployment monitoring and management
- Scaling and updating deployments
- Best practices for production deployments

Next: [Testing Deployments](testing.md)
