# 📋 Listing Available Models 🤖

Learn how to discover, explore, and select models in Azure AI Foundry for your specific use cases. Find the perfect AI companion for your health and fitness journey! 🏋️‍♀️ 🎯

## Model Discovery

### 1. Model Categories
- Text Generation
- Code Generation
- Image Generation
- Speech Processing
- Custom Models

```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from typing import Dict, List

class ModelExplorer:
    def __init__(self):
        """Initialize the ModelExplorer with Azure credentials."""
        try:
            self.credential = DefaultAzureCredential()
            self.client = AIProjectClient(
                subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
                resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
                credential=self.credential
            )
        except Exception as e:
            print(f"Error initializing ModelExplorer: {str(e)}")
            raise

    def list_models_by_category(self) -> Dict[str, List[dict]]:
        """List all available models grouped by category."""
        try:
            # Get all available models
            models = self.client.models.list()
            
            # Group models by category
            categorized_models = {}
            for model in models:
                category = model.category
                if category not in categorized_models:
                    categorized_models[category] = []
                
                model_info = {
                    'name': model.name,
                    'version': model.version,
                    'description': model.description,
                    'capabilities': model.capabilities
                }
                categorized_models[category].append(model_info)
            
            return categorized_models
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            raise

    def display_models(self):
        """Display available models in a formatted way."""
        try:
            models = self.list_models_by_category()
            
            for category, model_list in models.items():
                print(f"\n=== {category} Models ===")
                for model in model_list:
                    print(f"\nName: {model['name']}")
                    print(f"Version: {model['version']}")
                    print(f"Description: {model['description']}")
                    print(f"Capabilities: {', '.join(model['capabilities'])}")
        except Exception as e:
            print(f"Error displaying models: {str(e)}")

# Example usage
if __name__ == "__main__":
    explorer = ModelExplorer()
    explorer.display_models()

### 2. Model Providers
- Azure OpenAI
- Third-party providers
- Custom providers
- Community models

### 3. Model Capabilities
- Task specialization
- Language support
- Performance characteristics
- Resource requirements

## Model Selection

### 1. Selection Criteria
- Use case requirements
- Performance needs
- Resource constraints
- Cost considerations

### 2. Comparison Factors
- Model capabilities
- Version differences
- Resource usage
- Pricing tiers

### 3. Evaluation Methods
- Performance metrics
- Quality assessment
- Resource efficiency
- Cost analysis

## Model Information

### 1. Technical Details
- Model architecture
- Version history
- Input/output formats
- Resource specifications

### 2. Usage Guidelines
- Best practices
- Limitations
- Performance tips
- Security considerations

### 3. Deployment Requirements
- Resource needs
- Scaling considerations
- Integration requirements
- Monitoring setup

## Best Practices

### 1. Model Selection
- Define clear requirements
- Compare alternatives
- Test performance
- Consider costs

### 2. Resource Planning
- Capacity planning
- Usage monitoring
- Cost optimization
- Performance tuning

### 3. Documentation
- Track decisions
- Document configurations
- Monitor changes
- Share knowledge

## Interactive Workshop

For hands-on practice with exploring available models in Azure AI Foundry, try our interactive notebook:

[Launch Available Models Workshop](../2-notebooks/1-chat_completion/4-phi-4.ipynb)

This notebook provides:
- Comprehensive model listing and filtering
- Detailed model information retrieval
- Version comparison capabilities
- Best practices for model selection
- Interactive examples with real-time output

Next: [Deploying Models](deploying.md)
