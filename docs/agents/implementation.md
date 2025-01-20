# Building Your Health Advisor Agent 🏥

Let's create a health advisor agent that can provide personalized fitness and nutrition guidance. This will take about 30 minutes.

!!! warning "⚠️ Important Medical Disclaimer ⚠️"
    The health information provided by this guide is for general educational and entertainment purposes only and is not intended as a substitute for professional medical advice, diagnosis, or treatment.

## Quick Implementation

```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from azure.ai.inference import InferenceClient
import asyncio
import os

class HealthAdvisorAgent:
    def __init__(self):
        """Initialize the health advisor agent."""
        self.client = None
        self.inference_client = None
        self.product_docs = {
            "password_reset": "To reset password: 1) Click 'Forgot Password' 2) Enter email 3) Follow link",
            "billing": "Billing cycle runs monthly. Payment processed on 1st of each month.",
            "features": "Product includes: cloud storage, sync, sharing, and admin controls."
        }
    
    async def initialize(self):
        """Set up the agent with Azure AI."""
        try:
            # Initialize credentials
            credential = DefaultAzureCredential()
            
            # Create AI Project client
            self.client = AIProjectClient(
                subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
                resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
                credential=credential
            )
            
            # Create inference client
            self.inference_client = InferenceClient(
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                credential=credential
            )
            
            return True
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            return False
    
    async def handle_inquiry(self, user_input: str) -> str:
        """Handle a customer inquiry."""
        try:
            # Create context
            context = f"""
            You are a helpful health and fitness advisor.
            Available health resources:
            {self.product_docs}
            
            User inquiry: {user_input}
            
            Provide a clear, helpful response using the available documentation.
            """
            
            # Generate response using Azure AI inference
            response = await self.inference_client.chat_completion(
                deployment_name="health-advisor-v1",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

# Usage example
async def main():
    agent = CustomerServiceAgent()
    if await agent.initialize():
        response = await agent.handle_inquiry("How do I reset my password?")
        print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())

#### Key Components
- Azure AI Project client
- Azure AI Inference client
- Context management
- Error handling
- Response generation
- State tracking

#### Best Practices
- Project organization
- Resource management
- Error handling
- Testing patterns
- Documentation
- Performance optimization
- Security best practices
- Monitoring setup

## Common Implementation Patterns

### 1. Conversation Management
- Turn handling
- Context tracking
- State management
- History storage
- Response generation
- Error recovery

### 2. Azure AI SDK Integration
- AIProjectClient setup
- InferenceClient configuration
- Error handling with Azure SDK
- Retry policies
- Circuit breakers
- Fallback strategies

### 3. Operational Implementation
- Monitoring setup
- Logging system
- Performance tracking
- Security controls
- Backup procedures
- Recovery processes

## Development Best Practices

### 1. Code Organization
- Project structure
- Module design
- Interface definitions
- Error handling
- Documentation
- Testing strategy

### 2. Quality Assurance
- Unit testing
- Integration testing
- Performance testing
- Security testing
- Documentation review
- Code review

### 3. Performance Optimization
- Resource management
- Memory optimization
- Response time
- Error handling
- Caching strategy
- Scaling considerations

## Interactive Workshop

For hands-on practice with implementing AI agents in Azure AI Foundry, try our interactive notebook:

[Launch Agent Implementation Workshop](../2-notebooks/2-agent_service/1-basics.ipynb)

This notebook provides:
- Complete health advisor agent implementation
- Error handling and best practices with medical disclaimers
- Context management examples
- Testing and validation
- Enhancement exercises

Next: [Deploying and Testing](deploy-test.md)
