import nbformat as nbf
import os

def create_evaluation_intro_notebook():
    """Create a Jupyter notebook for introduction to Azure AI Evaluation."""
    nb = nbf.v4.new_notebook()
    
    # Title and Overview
    nb.cells.append(nbf.v4.new_markdown_cell("""# Introduction to Azure AI Evaluation
    
This notebook provides a hands-on introduction to evaluating AI models and agents using Azure AI Evaluation.

## Prerequisites
- Azure subscription with access to Azure AI Foundry
- Python environment with required packages installed
- Basic understanding of AI models and agents

## Learning Objectives
- Understand Azure AI Evaluation capabilities
- Learn to set up evaluation metrics
- Practice basic evaluation scenarios
- Analyze evaluation results
"""))

    # Setup and Authentication
    nb.cells.append(nbf.v4.new_code_cell("""# Import required libraries
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import InferenceClient, ChatCompletionsClient
from azure.ai.evaluation import EvaluationClient, TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument

# Initialize credentials and clients
credential = DefaultAzureCredential()
project_client = AIProjectClient(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    credential=credential
)

evaluation_client = EvaluationClient(credential=credential)
"""))

    # Basic Evaluation Setup
    nb.cells.append(nbf.v4.new_markdown_cell("""## Basic Evaluation Setup

Let's start with a simple evaluation scenario for our customer service agent."""))

    nb.cells.append(nbf.v4.new_code_cell("""# Define evaluation metrics
evaluation_metrics = {
    "response_relevance": {
        "type": "relevance",
        "weight": 0.4
    },
    "response_accuracy": {
        "type": "exact_match",
        "weight": 0.3
    },
    "response_time": {
        "type": "latency",
        "weight": 0.3
    }
}

# Create test cases
test_cases = [
    {
        "input": "How do I reset my password?",
        "expected_output": "To reset your password, click the 'Forgot Password' link, enter your email, and follow the instructions sent to your inbox."
    },
    {
        "input": "What are the product features?",
        "expected_output": "Our product includes cloud storage, synchronization capabilities, sharing features, and administrative controls."
    }
]"""))

    # Running Evaluations
    nb.cells.append(nbf.v4.new_markdown_cell("""## Running Evaluations

Now let's run some basic evaluations using our metrics and test cases."""))

    nb.cells.append(nbf.v4.new_code_cell("""async def run_evaluation():
    try:
        # Create evaluation run
        evaluation = await evaluation_client.create_evaluation(
            name="customer-service-basic-eval",
            metrics=evaluation_metrics,
            test_cases=test_cases
        )
        
        # Run evaluation
        results = await evaluation.run()
        
        # Print results
        print("Evaluation Results:")
        print(f"Overall Score: {results.overall_score}")
        print("\nMetric Scores:")
        for metric, score in results.metric_scores.items():
            print(f"{metric}: {score}")
            
        return results
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        return None

# Run evaluation
await run_evaluation()"""))

    # Analyzing Results
    nb.cells.append(nbf.v4.new_markdown_cell("""## Analyzing Results

Let's look at how to interpret and analyze the evaluation results."""))

    nb.cells.append(nbf.v4.new_code_cell("""def analyze_results(results):
    if not results:
        print("No results to analyze")
        return
    
    # Calculate performance metrics
    performance_summary = {
        "total_tests": len(test_cases),
        "successful_tests": sum(1 for score in results.test_scores if score > 0.8),
        "average_response_time": sum(results.response_times) / len(results.response_times)
    }
    
    # Print analysis
    print("Performance Summary:")
    print(f"Total Tests: {performance_summary['total_tests']}")
    print(f"Successful Tests: {performance_summary['successful_tests']}")
    print(f"Success Rate: {(performance_summary['successful_tests'] / performance_summary['total_tests']) * 100:.2f}%")
    print(f"Average Response Time: {performance_summary['average_response_time']:.2f}ms")

# Analyze the results
analyze_results(await run_evaluation())"""))

    # Error Handling and Best Practices
    # Add error handling section
    error_handling_md = """## Error Handling and Best Practices

Important considerations when working with Azure AI Evaluation:

1. Always validate your metrics configuration
2. Use appropriate test case sizes
3. Monitor evaluation performance
4. Handle timeouts and errors gracefully
5. Store and version your evaluation results"""
    
    nb.cells.append(nbf.v4.new_markdown_cell(error_handling_md))

    validation_code = """def validate_evaluation_config(metrics, test_cases):
    '''Validate evaluation configuration.'''
    try:
        # Check metric weights sum to 1
        total_weight = sum(metric["weight"] for metric in metrics.values())
        assert abs(total_weight - 1.0) < 0.001, "Metric weights must sum to 1"
        
        # Validate test cases
        for test_case in test_cases:
            assert "input" in test_case, "Test case missing input"
            assert "expected_output" in test_case, "Test case missing expected output"
        
        print("✓ Evaluation configuration is valid")
        return True
    except Exception as e:
        print(f"Configuration error: {str(e)}")
        return False

# Validate our configuration
validate_evaluation_config(evaluation_metrics, test_cases)"""
    nb.cells.append(nbf.v4.new_code_cell(validation_code))

    # Next Steps
    nb.cells.append(nbf.v4.new_markdown_cell("""## Next Steps

Now that you understand the basics of Azure AI Evaluation, you can:
1. Create more comprehensive evaluation metrics
2. Design larger test case sets
3. Implement continuous evaluation
4. Set up automated evaluation pipelines
5. Track evaluation results over time"""))

    # Save the notebook
    notebook_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "building_agent", "evaluation_intro.ipynb")
    nbf.write(nb, notebook_path)
    print(f"\nCreated {notebook_path}")
    
    # Validate the notebook
    total_cells = len(nb.cells)
    has_markdown = any(cell.cell_type == "markdown" for cell in nb.cells)
    has_code = any(cell.cell_type == "code" for cell in nb.cells)
    has_imports = any("import" in cell.source for cell in nb.cells if cell.cell_type == "code")
    has_error_handling = any("try:" in cell.source for cell in nb.cells if cell.cell_type == "code")
    
    print(f"\nValidation Results for {notebook_path}:")
    print(f"Total Cells: {total_cells}")
    print(f"Has Markdown Documentation: {'✓' if has_markdown else '✗'}")
    print(f"Has Code Cells: {'✓' if has_code else '✗'}")
    print(f"Has Required Imports: {'✓' if has_imports else '✗'}")
    print(f"Has Error Handling: {'✓' if has_error_handling else '✗'}")
    print(f"\nOverall Status: {'✓ Valid' if all([has_markdown, has_code, has_imports, has_error_handling]) else '✗ Invalid'}")

if __name__ == "__main__":
    create_evaluation_intro_notebook()
