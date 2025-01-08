import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for testing deployed models in Azure AI Foundry."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Testing Deployed Models in Azure AI Foundry

This notebook guides you through testing your deployed customer service AI model. You'll learn:
1. Basic model testing
2. Performance evaluation
3. Load testing
4. Error handling and validation
5. Best practices for model testing

## Prerequisites
- Completed model deployment
- Azure AI Foundry access
- Required Python packages installed
- Active model endpoint"""))

    # Environment setup
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os
import json
import time
import pandas as pd
from datetime import datetime
import requests
import asyncio
import aiohttp

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
    cells.append(new_markdown_cell("""## Initialize Testing Environment
First, let's set up our testing environment:"""))

    cells.append(new_code_cell("""def initialize_test_environment():
    \"\"\"Initialize the testing environment and client.\"\"\"
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
        print(f"× Error initializing test environment: {str(e)}")
        return None

# Initialize client
client = initialize_test_environment()"""))

    # Basic model testing
    cells.append(new_markdown_cell("""## Basic Model Testing
Let's start with basic functionality tests:"""))

    cells.append(new_code_cell("""def test_basic_functionality(deployment_name: str, test_cases: list):
    \"\"\"Run basic functionality tests on the deployed model.\"\"\"
    try:
        results = []
        for test_case in test_cases:
            # Send request to model
            response = client.deployments.invoke(
                deployment_name=deployment_name,
                input_data=test_case["input"]
            )
            
            # Validate response
            success = validate_response(response, test_case["expected"])
            
            # Store result
            results.append({
                "test_case": test_case["name"],
                "input": test_case["input"],
                "output": response,
                "expected": test_case["expected"],
                "success": success
            })
        
        # Display results
        df = pd.DataFrame(results)
        print("\\nTest Results:")
        print(df[["test_case", "success"]].to_string())
        
        return results
    except Exception as e:
        print(f"× Error in basic testing: {str(e)}")
        return None

# Example test cases
test_cases = [
    {
        "name": "Basic greeting",
        "input": "Hello, how can you help me today?",
        "expected": {"type": "greeting"}
    },
    {
        "name": "Product inquiry",
        "input": "What's the price of your basic plan?",
        "expected": {"type": "product_info"}
    },
    {
        "name": "Support request",
        "input": "I'm having trouble logging in",
        "expected": {"type": "support"}
    }
]

# Run basic tests
results = test_basic_functionality("customer-service-v1", test_cases)"""))

    # Performance testing
    cells.append(new_markdown_cell("""## Performance Testing
Now let's evaluate the model's performance:"""))

    cells.append(new_code_cell("""async def run_performance_test(deployment_name: str, requests_per_second: int, duration_seconds: int):
    \"\"\"Run performance tests on the deployed model.\"\"\"
    try:
        start_time = time.time()
        end_time = start_time + duration_seconds
        total_requests = requests_per_second * duration_seconds
        
        async def make_request():
            try:
                response = await client.deployments.invoke_async(
                    deployment_name=deployment_name,
                    input_data="Test request for performance evaluation"
                )
                return {
                    "success": True,
                    "latency": response.get("latency", 0),
                    "timestamp": time.time()
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "timestamp": time.time()
                }
        
        # Create tasks for concurrent requests
        tasks = []
        for _ in range(total_requests):
            tasks.append(make_request())
        
        # Run requests
        results = await asyncio.gather(*tasks)
        
        # Analyze results
        df = pd.DataFrame(results)
        
        print("\\nPerformance Test Results:")
        print(f"Total Requests: {len(results)}")
        print(f"Successful Requests: {df['success'].sum()}")
        print(f"Failed Requests: {len(results) - df['success'].sum()}")
        print(f"Average Latency: {df[df['success']]['latency'].mean():.2f}ms")
        print(f"95th Percentile Latency: {df[df['success']]['latency'].quantile(0.95):.2f}ms")
        
        return results
    except Exception as e:
        print(f"× Error in performance testing: {str(e)}")
        return None

# Run performance test
asyncio.run(run_performance_test(
    deployment_name="customer-service-v1",
    requests_per_second=10,
    duration_seconds=30
))"""))

    # Load testing
    cells.append(new_markdown_cell("""## Load Testing
Let's test how the model handles increasing load:"""))

    cells.append(new_code_cell("""def run_load_test(deployment_name: str, max_concurrent_requests: int):
    \"\"\"Run load tests with increasing concurrent requests.\"\"\"
    try:
        results = []
        
        for concurrent_requests in range(1, max_concurrent_requests + 1, 5):
            print(f"\\nTesting with {concurrent_requests} concurrent requests...")
            
            # Run concurrent requests
            test_results = asyncio.run(run_performance_test(
                deployment_name=deployment_name,
                requests_per_second=concurrent_requests,
                duration_seconds=10
            ))
            
            # Analyze results
            df = pd.DataFrame(test_results)
            results.append({
                "concurrent_requests": concurrent_requests,
                "success_rate": df['success'].mean() * 100,
                "avg_latency": df[df['success']]['latency'].mean(),
                "p95_latency": df[df['success']]['latency'].quantile(0.95)
            })
        
        # Display results
        results_df = pd.DataFrame(results)
        print("\\nLoad Test Results:")
        print(results_df.to_string())
        
        return results
    except Exception as e:
        print(f"× Error in load testing: {str(e)}")
        return None

# Run load test
load_results = run_load_test(
    deployment_name="customer-service-v1",
    max_concurrent_requests=50
)"""))

    # Error handling testing
    cells.append(new_markdown_cell("""## Error Handling Testing
Test how the model handles various error conditions:"""))

    cells.append(new_code_cell("""def test_error_handling(deployment_name: str):
    \"\"\"Test model's error handling capabilities.\"\"\"
    try:
        error_test_cases = [
            {
                "name": "Empty input",
                "input": "",
                "expected_error": True
            },
            {
                "name": "Very long input",
                "input": "a" * 10000,
                "expected_error": True
            },
            {
                "name": "Invalid JSON",
                "input": "{invalid_json:",
                "expected_error": True
            },
            {
                "name": "Special characters",
                "input": "!@#$%^&*()",
                "expected_error": False
            }
        ]
        
        results = []
        for test_case in error_test_cases:
            try:
                response = client.deployments.invoke(
                    deployment_name=deployment_name,
                    input_data=test_case["input"]
                )
                
                results.append({
                    "test_case": test_case["name"],
                    "expected_error": test_case["expected_error"],
                    "actual_error": False,
                    "handled_correctly": not test_case["expected_error"],
                    "response": response
                })
            except Exception as e:
                results.append({
                    "test_case": test_case["name"],
                    "expected_error": test_case["expected_error"],
                    "actual_error": True,
                    "handled_correctly": test_case["expected_error"],
                    "error": str(e)
                })
        
        # Display results
        df = pd.DataFrame(results)
        print("\\nError Handling Test Results:")
        print(df[["test_case", "handled_correctly"]].to_string())
        
        return results
    except Exception as e:
        print(f"× Error in error handling testing: {str(e)}")
        return None

# Run error handling tests
error_results = test_error_handling("customer-service-v1")"""))

    # Validation testing
    cells.append(new_markdown_cell("""## Response Validation
Test the model's response format and content:"""))

    cells.append(new_code_cell("""def validate_model_responses(deployment_name: str):
    \"\"\"Validate model responses for format and content.\"\"\"
    try:
        validation_test_cases = [
            {
                "name": "Response format",
                "input": "What are your business hours?",
                "validations": [
                    "response_type",
                    "confidence_score",
                    "response_text"
                ]
            },
            {
                "name": "Response content",
                "input": "I need technical support",
                "validations": [
                    "relevant_keywords",
                    "sentiment_analysis",
                    "action_items"
                ]
            }
        ]
        
        results = []
        for test_case in validation_test_cases:
            response = client.deployments.invoke(
                deployment_name=deployment_name,
                input_data=test_case["input"]
            )
            
            # Validate response
            validation_results = {}
            for validation in test_case["validations"]:
                validation_results[validation] = validate_field(response, validation)
            
            results.append({
                "test_case": test_case["name"],
                "input": test_case["input"],
                "validations": validation_results,
                "success": all(validation_results.values())
            })
        
        # Display results
        print("\\nValidation Test Results:")
        for result in results:
            print(f"\\nTest Case: {result['test_case']}")
            print(f"Success: {'✓' if result['success'] else '×'}")
            print("Validation Results:")
            for validation, passed in result['validations'].items():
                print(f"  - {validation}: {'✓' if passed else '×'}")
        
        return results
    except Exception as e:
        print(f"× Error in validation testing: {str(e)}")
        return None

def validate_field(response, field_type):
    \"\"\"Validate specific fields in the response.\"\"\"
    try:
        if field_type == "response_type":
            return isinstance(response.get("type"), str)
        elif field_type == "confidence_score":
            score = response.get("confidence")
            return isinstance(score, (int, float)) and 0 <= score <= 1
        elif field_type == "response_text":
            return isinstance(response.get("text"), str)
        elif field_type == "relevant_keywords":
            keywords = response.get("keywords", [])
            return isinstance(keywords, list) and len(keywords) > 0
        elif field_type == "sentiment_analysis":
            sentiment = response.get("sentiment")
            return isinstance(sentiment, (str, float))
        elif field_type == "action_items":
            actions = response.get("actions", [])
            return isinstance(actions, list)
        return False
    except Exception:
        return False

# Run validation tests
validation_results = validate_model_responses("customer-service-v1")"""))

    # Best practices
    cells.append(new_markdown_cell("""## Best Practices for Model Testing

1. **Comprehensive Testing Strategy**
   - Unit tests for basic functionality
   - Integration tests for end-to-end workflows
   - Performance tests for scalability
   - Load tests for stability
   - Error handling tests for robustness

2. **Test Data Management**
   - Use diverse test cases
   - Include edge cases
   - Maintain test data versioning
   - Regular test data updates

3. **Performance Monitoring**
   - Track response times
   - Monitor error rates
   - Analyze throughput
   - Set up alerts

4. **Documentation**
   - Document test cases
   - Record test results
   - Maintain testing procedures
   - Update documentation regularly

5. **Continuous Testing**
   - Automated testing pipeline
   - Regular test execution
   - Results tracking
   - Continuous improvement"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/model_testing.ipynb"
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
