import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for agent design patterns."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from azure.ai.inference import InferenceClient
from azure.ai.evaluation import EvaluationClient
from typing import Dict, List, Optional
import asyncio
import json
import os

# Check environment setup
required_vars = {
    "AZURE_SUBSCRIPTION_ID": os.getenv("AZURE_SUBSCRIPTION_ID"),
    "AZURE_RESOURCE_GROUP": os.getenv("AZURE_RESOURCE_GROUP"),
    "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT")
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    print("× Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
else:
    print("✓ All required environment variables are set")"""))
    
    # Introduction
    cells.append(new_markdown_cell("""# Agent Design Patterns in Azure AI Foundry

This notebook explores design patterns for building effective AI agents. You'll learn:
1. Core design principles
2. Pattern implementation
3. Best practices
4. Common pitfalls
5. Testing strategies

## Prerequisites
- Completed agent implementation
- Azure AI Foundry access
- Required Python packages installed"""))

    # Azure AI Design Principles
    cells.append(new_markdown_cell("""## Azure AI Design Principles

1. **Project Management**
   - Resource organization
   - Model deployment
   - Environment configuration
   - Access control

2. **Inference Management**
   - Model interaction
   - Response generation
   - Context handling
   - Error recovery

3. **Evaluation Strategy**
   - Performance monitoring
   - Quality assessment
   - Metrics tracking
   - Continuous improvement

4. **Integration Patterns**
   - Service connections
   - Data management
   - Security controls
   - Monitoring setup"""))

    # Basic Azure AI Implementation
    cells.append(new_code_cell("""from typing import Dict, List, Optional
import json

class CustomerServiceAgent:
    def __init__(self):
        \"\"\"Initialize the customer service agent with Azure AI clients.\"\"\"
        self.conversations: List[Dict] = []
        self.max_history = 10
        self.error_count = 0
        
        # Initialize Azure AI clients
        credential = DefaultAzureCredential()
        self.project_client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        self.inference_client = InferenceClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            credential=credential
        )
        self.evaluation_client = EvaluationClient(
            credential=credential
        )
        
    def add_conversation(self, interaction: Dict):
        \"\"\"Add a conversation interaction to history.\"\"\"
        self.conversations.append(interaction)
        if len(self.conversations) > self.max_history:
            self.conversations.pop(0)
            
    def get_recent_conversations(self, count: Optional[int] = None) -> List[Dict]:
        \"\"\"Get recent conversation history.\"\"\"
        if count is None:
            return self.conversations
        return self.conversations[-count:]
        
    def clear_history(self):
        \"\"\"Clear conversation history.\"\"\"
        self.conversations = []
    
    def _validate_input(self, user_input: str) -> bool:
        \"\"\"Validate user input.\"\"\"
        return bool(user_input and user_input.strip())
    
    def _format_response(self, response: str) -> str:
        \"\"\"Format agent response.\"\"\"
        return f"{self.config.name}: {response}"
    
    def _handle_error(self, error: Exception) -> str:
        \"\"\"Handle errors gracefully.\"\"\"
        self.error_count += 1
        if self.error_count > self.max_retries:
            return "I'm having trouble processing requests. Please try again later."
        
        return f"I encountered an error: {str(error)}. Retrying... ({self.error_count}/{self.max_retries})"
    
    def process_input(self, user_input: str) -> str:
        \"\"\"Process user input and generate response.\"\"\"
        try:
            # Validate input
            if not self._validate_input(user_input):
                raise ValueError("Invalid input")
            
            # Process input (to be implemented by subclasses)
            response = self._process(user_input)
            
            # Add to conversation history
            self.add_conversation({
                "user_input": user_input,
                "response": response
            })
            
            # Request completed successfully
            self.error_count = 0
            
            return self._format_response(response)
            
        except Exception as e:
            return self._handle_error(e)
    
    def _process(self, user_input: str) -> str:
        \"\"\"To be implemented by subclasses.\"\"\"
        raise NotImplementedError"""))

    # Specialized Agent Implementation
    cells.append(new_code_cell("""class CustomerServiceAgent:
    def __init__(self):
        self.client = None
        self.inference_client = None
        
        # Initialize Azure clients
        credential = DefaultAzureCredential()
        self.client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        self.inference_client = InferenceClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            credential=credential
        )
        
        # Knowledge base for context
        self.knowledge_base = {
            "account": {
                "password_reset": "To reset your password, visit the account settings page.",
                "login_issues": "Make sure you're using the correct email and password.",
                "security": "We use industry-standard encryption for all data."
            },
            "billing": {
                "payment": "We accept all major credit cards and PayPal.",
                "refunds": "Refund requests are processed within 5-7 business days.",
                "subscription": "Subscriptions are billed monthly on the same date."
            },
            "product": {
                "features": "Our product includes cloud storage, sync, and sharing.",
                "limits": "Free accounts have 5GB storage, paid accounts have unlimited.",
                "support": "24/7 support is available for premium accounts."
            }
        }
    
    async def _process(self, user_input: str) -> str:
        \"\"\"Process user input using Azure AI inference.\"\"\"
        try:
            # Create context from knowledge base
            context = f\"\"\"You are a helpful customer service agent. 
            Available product documentation:
            {json.dumps(self.knowledge_base, indent=2)}
            
            User inquiry: {user_input}
            
            Provide a clear, helpful response using the available documentation.\"\"\"
            
            # Generate response using Azure AI inference
            response = await self.inference_client.chat_completion(
                deployment_name="customer-service-v1",
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
"""))

    # Testing Azure AI Implementation
    cells.append(new_code_cell("""async def test_agent():
    \"\"\"Test the customer service agent implementation with Azure AI.\"\"\"
    # Create agent
    agent = CustomerServiceAgent()
    
    # Test cases
    test_cases = [
        "How do I reset my password?",
        "What payment methods do you accept?",
        "Tell me about your product features"
    ]
    
    # Run tests
    print("Running Azure AI agent tests...")
    print("-" * 50)
    
    for test_input in test_cases:
        try:
            print(f"User: {test_input}")
            
            # Generate response using Azure AI inference
            response = await agent.inference_client.chat_completion(
                deployment_name="customer-service-v1",
                messages=[
                    {"role": "system", "content": "You are a helpful customer service agent."},
                    {"role": "user", "content": test_input}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            # Add to conversation history
            agent.add_conversation({
                "user_input": test_input,
                "response": response.choices[0].message.content
            })
            
            print(f"Agent: {response.choices[0].message.content}\\n")
            
            # Evaluate response
            evaluation = await agent.evaluation_client.evaluate(
                responses=[response.choices[0].message.content],
                expected=["A helpful customer service response"],
                metrics=["relevance", "fluency"]
            )
            print(f"Response evaluation: {evaluation}\\n")
            
        except Exception as e:
            print(f"Error processing request: {str(e)}\\n")
    
    # Check conversation history
    print("Recent conversations:")
    for interaction in agent.get_recent_conversations():
        print(json.dumps(interaction, indent=2))

# Run tests
await test_agent()"""))

    # Design Patterns
    cells.append(new_markdown_cell('''## Azure AI Design Patterns

1. **Azure AI Project Pattern**
   - Manage AI resources
   - Configure deployments
   - Handle authentication

2. **Azure AI Inference Pattern**
   - Model deployment
   - Response generation
   - Error handling

3. **Azure AI Evaluation Pattern**
   - Performance monitoring
   - Quality assessment
   - Metrics tracking

4. **Azure AI Pipeline Pattern**
   - Input preprocessing
   - Azure AI inference
   - Response post-processing'''))

    # Azure AI Pattern Implementation
    pattern_implementation = '''from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from azure.ai.inference import InferenceClient
from azure.ai.evaluation import EvaluationClient
import os
import asyncio
from typing import Dict, List, Optional

# Azure AI Project Pattern
class AIProjectManager:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=self.credential
        )
    
    async def deploy_model(self, model_name: str, deployment_name: str) -> Dict:
        """Deploy an AI model."""
        try:
            deployment = await self.client.models.deploy(
                model_name=model_name,
                deployment_name=deployment_name,
                configuration={
                    "instance_type": "Standard_DS3_v2",
                    "instance_count": 1
                }
            )
            return deployment
        except Exception as e:
            print(f"Error deploying model: {str(e)}")
            return None

# Azure AI Inference Pattern
class InferenceManager:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.client = InferenceClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            credential=self.credential
        )
    
    async def generate_response(self, prompt: str, deployment_name: str) -> str:
        """Generate response using Azure AI inference."""
        try:
            response = await self.client.chat_completion(
                deployment_name=deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful customer service agent."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

# Azure AI Evaluation Pattern
class EvaluationManager:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.client = EvaluationClient(
            credential=self.credential
        )
    
    async def evaluate_response(self, response: str, expected: str) -> Dict:
        """Evaluate response quality."""
        try:
            result = await self.client.evaluate(
                responses=[response],
                expected=[expected],
                metrics=["relevance", "fluency", "coherence"]
            )
            return result
        except Exception as e:
            print(f"Error evaluating response: {str(e)}")
            return None

# Azure AI Pipeline Pattern
class AIPipeline:
    def __init__(self):
        self.project_manager = AIProjectManager()
        self.inference_manager = InferenceManager()
        self.evaluation_manager = EvaluationManager()
    
    async def process_request(self, input_text: str, deployment_name: str) -> Dict:
        """Process request through the Azure AI pipeline."""
        try:
            # Generate response
            response = await self.inference_manager.generate_response(
                input_text, 
                deployment_name
            )
            
            # Evaluate response
            evaluation = await self.evaluation_manager.evaluate_response(
                response,
                "Expected response template"
            )
            
            return {
                "response": response,
                "evaluation": evaluation
            }
        except Exception as e:
            return {
                "error": f"Pipeline error: {str(e)}"
            }'''
    cells.append(new_code_cell(pattern_implementation))

    enhanced_agent_code = '''# Enhanced Agent with Patterns
class EnhancedAgent:
    def __init__(self):
        # Initialize Azure AI clients
        credential = DefaultAzureCredential()
        self.inference_client = InferenceClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            credential=credential
        )
        self.evaluation_client = EvaluationClient(credential=credential)
    
    async def _process(self, user_input: str) -> str:
        try:
            # Generate response using Azure AI inference
            response = await self.inference_client.chat_completion(
                deployment_name="customer-service-v1",
                messages=[
                    {"role": "system", "content": "You are a helpful customer service agent."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing request: {str(e)}"'''
    cells.append(new_code_cell(enhanced_agent_code))

    # Testing Patterns
    test_patterns_code = '''# Test Azure AI patterns
async def test_azure_patterns():
    """Test the implementation of Azure AI patterns."""
    try:
        # Initialize pipeline
        pipeline = AIPipeline()
        
        # Test input
        test_input = "How do I reset my password?"
        
        print("Testing Azure AI Pipeline...")
        result = await pipeline.process_request(
            test_input,
            deployment_name="customer-service-v1"
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("Response:", result["response"])
            print("\nEvaluation:", result["evaluation"])
        
        # Test individual components
        print("\nTesting Azure AI Project Manager...")
        project_manager = AIProjectManager()
        deployment = await project_manager.deploy_model(
            model_name="gpt-4",
            deployment_name="test-deployment"
        )
        print("Deployment:", deployment)
        
        print("\nTesting Azure AI Inference...")
        inference_manager = InferenceManager()
        response = await inference_manager.generate_response(
            test_input,
            deployment_name="customer-service-v1"
        )
        print("Response:", response)
        
        print("\nTesting Azure AI Evaluation...")
        evaluation_manager = EvaluationManager()
        evaluation = await evaluation_manager.evaluate_response(
            response,
            "A clear explanation of password reset process"
        )
        print("Evaluation:", evaluation)
        
        return "Azure AI pattern tests completed successfully"
    except Exception as e:
        return f"Error in Azure AI pattern tests: {str(e)}"

# Run Azure AI pattern tests
await test_azure_patterns()'''
    cells.append(new_code_cell(test_patterns_code))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Code Organization**
   - Clear class hierarchy
   - Separation of concerns
   - Interface-based design
   - Proper encapsulation

2. **Error Handling**
   - Comprehensive error checking
   - Graceful degradation
   - Clear error messages
   - Recovery mechanisms

3. **Testing**
   - Unit tests for components
   - Integration tests
   - Error case testing
   - Performance testing

4. **Documentation**
   - Clear code comments
   - API documentation
   - Usage examples
   - Design decisions

5. **Maintenance**
   - Regular code reviews
   - Performance monitoring
   - Error tracking
   - Version control"""))

    # Practical Exercise
    cells.append(new_markdown_cell("""## Practical Exercise

Try these exercises to reinforce your understanding:

1. **Enhance Azure AI Project**
   - Add model deployment configuration
   - Implement resource monitoring
   - Configure access controls
   - Add usage tracking

2. **Improve Inference**
   - Implement retry logic
   - Add response streaming
   - Enhance context management
   - Optimize token usage

3. **Expand Evaluation**
   - Add custom metrics
   - Implement A/B testing
   - Track performance trends
   - Generate quality reports"""))

    cells.append(new_code_cell("""async def exercise_template():
    \"\"\"Template for practical exercises using Azure AI SDKs.\"\"\"
    # Initialize clients
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    inference_client = InferenceClient(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        credential=credential
    )
    evaluation_client = EvaluationClient(
        credential=credential
    )
    
    # Example: Deploy and test a model
    try:
        # Deploy model
        deployment = await project_client.models.deploy(
            model_name="gpt-4",
            deployment_name="exercise-deployment",
            configuration={
                "instance_type": "Standard_DS3_v2",
                "instance_count": 1
            }
        )
        
        # Test inference
        response = await inference_client.chat_completion(
            deployment_name="exercise-deployment",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
        )
        
        # Evaluate response
        evaluation = await evaluation_client.evaluate(
            responses=[response.choices[0].message.content],
            expected=["A friendly greeting"],
            metrics=["relevance", "fluency"]
        )
        
        return {
            "deployment": deployment,
            "response": response,
            "evaluation": evaluation
        }
    except Exception as e:
        return f"Error in exercise: {str(e)}"

# Try implementing more Azure AI patterns!"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_design.ipynb"
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
