import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure AI Agent Service."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure AI Agent Service Overview

This notebook introduces you to the Azure AI Agent Service and its capabilities. You'll learn:
1. What the AI Agent Service provides
2. Key service features and components
3. Service configuration options
4. Integration patterns
5. Best practices for service usage

## Prerequisites
- Completed Introduction to Agents
- Azure AI Foundry access
- Required Python packages installed"""))

    # Environment setup
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
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

    # Service Overview
    cells.append(new_markdown_cell("""## Azure AI Agent Service Overview

The Azure AI Agent Service provides:

1. **Agent Management**
   - Agent lifecycle management
   - Version control
   - Deployment options
   - Monitoring capabilities

2. **Integration Features**
   - API endpoints
   - SDK support
   - Event handling
   - Authentication

3. **Scalability**
   - Auto-scaling
   - Load balancing
   - Resource optimization
   - Performance monitoring

4. **Security**
   - Access control
   - Data protection
   - Audit logging
   - Compliance features"""))

    # Service Features
    cells.append(new_code_cell("""def explore_service_features():
    \"\"\"Demonstrate key features of the AI Agent Service.\"\"\"
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Example service configuration
        service_config = {
            "features": {
                "agent_management": {
                    "version_control": True,
                    "deployment_options": ["single", "distributed"],
                    "monitoring": ["metrics", "logs", "traces"]
                },
                "integration": {
                    "api_versions": ["v1", "v2"],
                    "protocols": ["REST", "gRPC"],
                    "event_handlers": ["webhook", "queue"]
                },
                "scaling": {
                    "auto_scale": True,
                    "min_instances": 1,
                    "max_instances": 10,
                    "scale_rules": ["cpu", "memory", "requests"]
                },
                "security": {
                    "authentication": ["OAuth", "API key"],
                    "authorization": ["RBAC", "scope-based"],
                    "audit_logging": True
                }
            }
        }
        
        print("Service Features:")
        print(json.dumps(service_config, indent=2))
        
        return service_config
    except Exception as e:
        print(f"× Error exploring service features: {str(e)}")
        return None

# Explore service features
service_features = explore_service_features()"""))

    # Service Configuration
    cells.append(new_code_cell("""def configure_agent_service():
    \"\"\"Demonstrate service configuration options.\"\"\"
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Example service configuration
        config = {
            "service": {
                "name": "customer-service-agent",
                "version": "1.0.0",
                "description": "Customer service agent handling support requests"
            },
            "compute": {
                "sku": "Standard_D2s_v3",
                "region": "eastus",
                "auto_scale": True
            },
            "networking": {
                "virtual_network": True,
                "private_endpoints": True,
                "outbound_access": ["allowed_endpoints"]
            },
            "monitoring": {
                "metrics_enabled": True,
                "logs_enabled": True,
                "application_insights": True
            },
            "security": {
                "managed_identity": True,
                "network_isolation": True,
                "key_rotation": True
            }
        }
        
        print("Service Configuration:")
        print(json.dumps(config, indent=2))
        
        return config
    except Exception as e:
        print(f"× Error configuring service: {str(e)}")
        return None

# Configure service
service_config = configure_agent_service()"""))

    # Integration Patterns
    cells.append(new_markdown_cell("""## Integration Patterns

Common patterns for integrating with the AI Agent Service:

1. **Direct API Integration**
   - REST API calls
   - SDK usage
   - Authentication handling
   - Error management

2. **Event-Driven Integration**
   - Webhook handlers
   - Message queues
   - Event subscriptions
   - Asynchronous processing

3. **Hybrid Integration**
   - Combined synchronous/asynchronous
   - Fallback mechanisms
   - Load distribution
   - High availability"""))

    cells.append(new_code_cell("""def demonstrate_integration_patterns():
    \"\"\"Show different integration patterns with the service.\"\"\"
    try:
        # Example integration patterns
        patterns = {
            "direct_api": {
                "pattern": "synchronous",
                "endpoint": "/api/v1/agents",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "authentication": {
                    "type": "OAuth2",
                    "scopes": ["agent.read", "agent.write"]
                },
                "example": {
                    "request": {
                        "method": "POST",
                        "path": "/api/v1/agents",
                        "headers": {
                            "Authorization": "Bearer ${token}",
                            "Content-Type": "application/json"
                        },
                        "body": {
                            "name": "customer-service-agent",
                            "model": "gpt-35-turbo",
                            "config": {}
                        }
                    }
                }
            },
            "event_driven": {
                "pattern": "asynchronous",
                "triggers": ["http", "queue", "timer"],
                "handlers": {
                    "webhook": {
                        "url": "/webhooks/agent-events",
                        "methods": ["POST"],
                        "retry": True
                    },
                    "queue": {
                        "type": "azure-storage-queue",
                        "name": "agent-events",
                        "visibility_timeout": 300
                    }
                }
            },
            "hybrid": {
                "patterns": ["sync", "async"],
                "load_balancing": True,
                "fallback": {
                    "enabled": True,
                    "strategy": "circuit-breaker"
                },
                "availability": {
                    "zones": ["1", "2", "3"],
                    "sla": "99.9%"
                }
            }
        }
        
        print("Integration Patterns:")
        print(json.dumps(patterns, indent=2))
        
        return patterns
    except Exception as e:
        print(f"× Error demonstrating integration patterns: {str(e)}")
        return None

# Demonstrate integration patterns
integration_patterns = demonstrate_integration_patterns()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

Key considerations when working with the AI Agent Service:

1. **Service Configuration**
   - Right-size compute resources
   - Enable appropriate monitoring
   - Configure proper security
   - Plan for scaling

2. **Integration Design**
   - Choose appropriate patterns
   - Implement proper error handling
   - Consider performance impact
   - Plan for resilience

3. **Security Setup**
   - Use managed identities
   - Implement least privilege
   - Enable audit logging
   - Regular security reviews

4. **Monitoring**
   - Track key metrics
   - Set up alerts
   - Review logs regularly
   - Monitor costs"""))

    cells.append(new_code_cell("""def implement_best_practices():
    \"\"\"Demonstrate implementation of best practices.\"\"\"
    try:
        # Example best practices implementation
        practices = {
            "service_configuration": {
                "compute_sizing": {
                    "strategy": "start_small_scale_up",
                    "monitoring_period": "2_weeks",
                    "metrics": ["cpu", "memory", "requests"]
                },
                "monitoring_setup": {
                    "metrics": True,
                    "logs": True,
                    "alerts": True,
                    "dashboard": True
                }
            },
            "integration": {
                "error_handling": {
                    "retry_policy": True,
                    "circuit_breaker": True,
                    "fallback_logic": True
                },
                "performance": {
                    "caching": True,
                    "connection_pooling": True,
                    "async_operations": True
                }
            },
            "security": {
                "identity": "managed_identity",
                "network": "private_endpoints",
                "encryption": "at_rest_and_transit",
                "monitoring": "security_center"
            },
            "operations": {
                "backup": True,
                "disaster_recovery": True,
                "cost_management": True,
                "compliance": True
            }
        }
        
        print("Best Practices Implementation:")
        print(json.dumps(practices, indent=2))
        
        return practices
    except Exception as e:
        print(f"× Error implementing best practices: {str(e)}")
        return None

# Implement best practices
best_practices = implement_best_practices()"""))

    # Practical Exercise
    cells.append(new_markdown_cell("""## Practical Exercise

Now that you understand the AI Agent Service, try these exercises:

1. **Service Configuration**
   - Configure basic service settings
   - Set up monitoring
   - Enable security features
   - Configure scaling

2. **Integration Setup**
   - Choose integration pattern
   - Implement basic integration
   - Add error handling
   - Test connectivity

3. **Best Practices Implementation**
   - Apply security best practices
   - Set up monitoring
   - Implement error handling
   - Configure scaling"""))

    cells.append(new_code_cell("""def complete_practical_exercise():
    \"\"\"Complete the practical exercise for service configuration.\"\"\"
    try:
        # Your service configuration
        my_service_config = {
            "name": "customer-support-agent",
            "version": "1.0.0",
            "compute": {
                "sku": "Standard_D2s_v3",
                "auto_scale": True,
                "min_instances": 1,
                "max_instances": 3
            },
            "security": {
                "managed_identity": True,
                "private_endpoints": True,
                "audit_logging": True
            },
            "monitoring": {
                "metrics": True,
                "logs": True,
                "alerts": [
                    {
                        "name": "high_latency",
                        "threshold": 1000,
                        "window": "5m"
                    }
                ]
            },
            "integration": {
                "pattern": "hybrid",
                "endpoints": {
                    "sync": "/api/v1/agents",
                    "async": "/api/v1/agent-events"
                },
                "error_handling": {
                    "retries": 3,
                    "timeout": 30,
                    "circuit_breaker": True
                }
            }
        }
        
        print("Your Service Configuration:")
        print(json.dumps(my_service_config, indent=2))
        
        return my_service_config
    except Exception as e:
        print(f"× Error in practical exercise: {str(e)}")
        return None

# Complete the exercise
my_config = complete_practical_exercise()"""))

    # Next Steps
    cells.append(new_markdown_cell("""## Next Steps

Now that you understand the AI Agent Service, you can:
1. Implement your agent
2. Configure the service
3. Set up integrations
4. Monitor operations

Continue to the next notebook to learn about implementing your AI agent."""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_service.ipynb"
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
