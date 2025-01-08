import nbformat as nbf
import os

def create_testing_notebook():
    nb = nbf.v4.new_notebook()
    
    # Title and Introduction
    nb.cells.append(nbf.v4.new_markdown_cell("""# Testing and Deploying Your AI Agent
    
This notebook guides you through the process of testing and deploying your AI agent in Azure AI Foundry.

## Prerequisites
- Azure AI Foundry SDK installed
- Azure credentials configured
- A developed AI agent (from previous notebooks)

## What You'll Learn
- How to test your AI agent
- How to deploy your agent to Azure
- How to monitor agent performance
- How to handle errors and edge cases
"""))

    # Setup and Authentication
    nb.cells.append(nbf.v4.new_markdown_cell("""## Setup and Authentication

First, let's import the required libraries and authenticate with Azure."""))
    
    nb.cells.append(nbf.v4.new_code_cell("""import os
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from azure.ai.inference import InferenceClient
from azure.ai.evaluation import EvaluationClient
import asyncio
import json
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Azure credentials
try:
    credential = DefaultAzureCredential()
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    print("✓ Successfully authenticated with Azure")
except Exception as e:
    print(f"× Authentication failed: {str(e)}")
    raise"""))

    # Agent Testing Suite
    nb.cells.append(nbf.v4.new_markdown_cell("""## Agent Testing Suite

Let's create a testing suite for evaluating our AI agent's functionality using Azure AI Evaluation."""))
    
    nb.cells.append(nbf.v4.new_code_cell("""from typing import Dict, List, Optional
import asyncio

class AgentTester:
    def __init__(self, agent):
        \"\"\"Initialize the AgentTester with an AI agent.\"\"\"
        self.agent = agent
        self.test_cases = []
        self.results = []
        
        # Initialize Azure evaluation client
        credential = DefaultAzureCredential()
        self.evaluation_client = EvaluationClient(credential=credential)
    
    def add_test_case(self, input_text: str, expected_topics: List[str]):
        \"\"\"Add a test case with input and expected topics.\"\"\"
        self.test_cases.append({
            "input": input_text,
            "expected_topics": expected_topics
        })
    
    async def run_tests(self):
        \"\"\"Run all test cases and collect results using Azure AI Evaluation.\"\"\"
        for test in self.test_cases:
            try:
                # Get agent response
                response = await self.agent.process_input(test["input"])
                
                # Evaluate response using Azure AI Evaluation
                evaluation = await self.evaluation_client.evaluate_completion(
                    completion=response,
                    reference=test["expected_topics"],
                    metrics=["relevance", "toxicity", "fluency"]
                )
                
                # Check if response meets quality criteria
                topics_found = evaluation.metrics["relevance"] > 0.7
                
                self.results.append({
                    "input": test["input"],
                    "response": response,
                    "topics_found": topics_found,
                    "evaluation": evaluation.metrics,
                    "status": "success"
                })
            except Exception as e:
                self.results.append({
                    "input": test["input"],
                    "error": str(e),
                    "status": "error"
                })
        
        return self.results

    def print_results(self):
        \"\"\"Display test results in a formatted way.\"\"\"
        print("\\nTest Results:")
        print("-" * 50)
        
        success_count = sum(1 for r in self.results if r["status"] == "success")
        total_count = len(self.results)
        
        for i, result in enumerate(self.results, 1):
            print(f"\\nTest Case {i}:")
            print(f"Input: {result['input']}")
            if result['status'] == 'success':
                print(f"Response: {result['response']}")
                print(f"Topics Found: {'✓' if result['topics_found'] else '×'}")
            else:
                print(f"Error: {result['error']}")
            print("-" * 30)
        
        print(f"\\nOverall: {success_count}/{total_count} tests passed")"""))

    # Testing Examples
    nb.cells.append(nbf.v4.new_markdown_cell("""## Running Tests

Let's test our agent with some common customer service scenarios."""))
    
    nb.cells.append(nbf.v4.new_code_cell("""# Initialize your agent
from typing import Dict, List
import asyncio
from your_agent_module import CustomerServiceAgent  # You should have this from previous notebooks

async def test_agent():
    \"\"\"Test the customer service agent with various scenarios.\"\"\"
    try:
        # Create agent instance
        agent = CustomerServiceAgent()
        await agent.initialize()
        
        # Create tester
        tester = AgentTester(agent)
        
        # Add test cases
        test_cases = [
            {
                "input": "How do I reset my password?",
                "expected_topics": ["password", "reset", "account"]
            },
            {
                "input": "What are your business hours?",
                "expected_topics": ["hours", "business", "time"]
            },
            {
                "input": "I need to cancel my subscription",
                "expected_topics": ["cancel", "subscription", "account"]
            }
        ]
        
        for test in test_cases:
            tester.add_test_case(test["input"], test["expected_topics"])
        
        # Run tests
        results = await tester.run_tests()
        
        # Display results
        tester.print_results()
        
        return results
    except Exception as e:
        print(f"× Error during testing: {str(e)}")
        raise

# Run the tests
await test_agent()"""))

    # Deployment
    nb.cells.append(nbf.v4.new_markdown_cell("""## Deploying Your Agent

Now that we've tested our agent, let's deploy it to Azure AI Foundry."""))
    
    nb.cells.append(nbf.v4.new_code_cell("""from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from typing import Dict, Optional
import asyncio

class AgentDeployer:
    def __init__(self, client: AIProjectClient):
        \"\"\"Initialize the AgentDeployer with an AIProjectClient.\"\"\"
        self.client = client
    
    async def deploy_agent(self, 
                          agent_name: str,
                          deployment_name: str,
                          model_name: str = "gpt-35-turbo",
                          instance_count: int = 1):
        \"\"\"Deploy an agent to Azure AI Foundry.\"\"\"
        try:
            # Create deployment configuration
            deployment_config = {
                "name": deployment_name,
                "model": model_name,
                "instance_count": instance_count,
                "agent_configuration": {
                    "name": agent_name,
                    "description": "Customer service agent deployment",
                    "capabilities": ["chat", "task_completion"]
                }
            }
            
            # Deploy the agent
            deployment = await self.client.deployments.create_or_update(
                deployment_name,
                deployment_config
            )
            
            print(f"✓ Agent '{agent_name}' deployed successfully")
            print(f"Deployment name: {deployment.name}")
            print(f"Endpoint: {deployment.endpoint}")
            
            return deployment
        except Exception as e:
            print(f"× Deployment failed: {str(e)}")
            raise

# Deploy the agent
deployer = AgentDeployer(client)
deployment = await deployer.deploy_agent(
    agent_name="customer-service-agent",
    deployment_name="customer-service-v1"
)"""))

    # Monitoring
    nb.cells.append(nbf.v4.new_markdown_cell("""## Monitoring Your Deployment

Let us set up basic monitoring for your deployed agent."""))
    
    nb.cells.append(nbf.v4.new_code_cell("""from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from typing import Dict, Optional
import asyncio

class AgentMonitor:
    def __init__(self, client: AIProjectClient):
        \"\"\"Initialize the AgentMonitor with an AIProjectClient.\"\"\"
        self.client = client
    
    async def get_deployment_status(self, deployment_name: str) -> Dict[str, str]:
        \"\"\"Get the current status of a deployment.\"\"\"
        try:
            deployment = await self.client.deployments.get(deployment_name)
            return {
                "status": deployment.status,
                "last_updated": deployment.last_updated,
                "endpoint": deployment.endpoint
            }
        except Exception as e:
            print(f"× Error getting deployment status: {str(e)}")
            raise
    
    async def get_deployment_metrics(self, deployment_name: str) -> Dict[str, float]:
        \"\"\"Get basic metrics for a deployment.\"\"\"
        try:
            metrics = await self.client.deployments.get_metrics(deployment_name)
            return {
                "requests_per_minute": metrics.get("requests_per_minute", 0),
                "average_latency": metrics.get("average_latency", 0),
                "error_rate": metrics.get("error_rate", 0)
            }
        except Exception as e:
            print(f"× Error getting metrics: {str(e)}")
            raise

# Monitor the deployment
monitor = AgentMonitor(client)
status = await monitor.get_deployment_status("customer-service-v1")
metrics = await monitor.get_deployment_metrics("customer-service-v1")

print("\\nDeployment Status:")
print(json.dumps(status, indent=2))
print("\\nDeployment Metrics:")
print(json.dumps(metrics, indent=2))"""))

    # Cleanup
    nb.cells.append(nbf.v4.new_markdown_cell("""## Cleanup

Don't forget to clean up resources when you're done testing."""))
    
    nb.cells.append(nbf.v4.new_code_cell("""async def cleanup_deployment(client: AIProjectClient, deployment_name: str):
    \"\"\"Clean up a deployment when no longer needed.\"\"\"
    try:
        await client.deployments.delete(deployment_name)
        print(f"✓ Deployment '{deployment_name}' deleted successfully")
    except Exception as e:
        print(f"× Error during cleanup: {str(e)}")
        raise

# Uncomment to cleanup
# await cleanup_deployment(client, "customer-service-v1")"""))

    # Save the notebook
    os.makedirs("building_agent", exist_ok=True)
    notebook_path = "building_agent/agent_testing.ipynb"
    with open(notebook_path, "w") as f:
        nbf.write(nb, f)
    
    print(f"\nCreated {notebook_path}")
    
    # Validate the notebook
    total_cells = len(nb.cells)
    has_markdown = any(cell.cell_type == "markdown" for cell in nb.cells)
    has_code = any(cell.cell_type == "code" for cell in nb.cells)
    has_imports = any("import" in cell.source for cell in nb.cells if cell.cell_type == "code")
    has_error_handling = any("try:" in cell.source for cell in nb.cells if cell.cell_type == "code")
    
    print(f"\nValidation Results for {notebook_path}:")
    print(f"Total Cells: {total_cells}")
    print(f"Has Markdown Documentation: {'✓' if has_markdown else '×'}")
    print(f"Has Code Cells: {'✓' if has_code else '×'}")
    print(f"Has Required Imports: {'✓' if has_imports else '×'}")
    print(f"Has Error Handling: {'✓' if has_error_handling else '×'}")
    
    all_valid = all([has_markdown, has_code, has_imports, has_error_handling])
    print(f"\nOverall Status: {'✓ Valid' if all_valid else '× Invalid'}")

if __name__ == "__main__":
    create_testing_notebook()
