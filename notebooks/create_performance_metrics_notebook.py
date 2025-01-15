import nbformat as nbf
import os

def create_performance_metrics_notebook():
    """Create a Jupyter notebook for performance metrics evaluation."""
    nb = nbf.v4.new_notebook()
    
    # Title and Overview
    nb.cells.append(nbf.v4.new_markdown_cell("""# Performance Metrics in Azure AI Evaluation
    
This notebook demonstrates how to set up and measure performance metrics for your customer service AI agent using Azure AI Evaluation.

## Prerequisites
- Azure subscription with access to Azure AI Foundry
- Python environment with required packages installed
- Completed the Introduction to Evaluation notebook
- Working customer service agent implementation

## Learning Objectives
- Define custom evaluation metrics
- Set up performance monitoring
- Collect and analyze metrics
- Optimize agent performance
"""))

    # Setup and Imports
    nb.cells.append(nbf.v4.new_code_cell("""import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import InferenceClient, ChatCompletionsClient
from azure.ai.evaluation import EvaluationClient, TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument
import pandas as pd
from datetime import datetime, timedelta
import asyncio

# Initialize Azure clients
credential = DefaultAzureCredential()
project_client = AIProjectClient(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    credential=credential
)
evaluation_client = EvaluationClient(credential=credential)"""))

    # Define Metrics
    nb.cells.append(nbf.v4.new_markdown_cell("""## Defining Performance Metrics

Let's define key metrics for evaluating our customer service agent:
1. Response Accuracy
2. Response Time
3. Task Completion Rate
4. User Satisfaction Score
5. Error Rate"""))

    nb.cells.append(nbf.v4.new_code_cell("""# Define evaluation metrics
performance_metrics = {
    "response_accuracy": {
        "type": "relevance",
        "weight": 0.3,
        "threshold": 0.8
    },
    "response_time": {
        "type": "latency",
        "weight": 0.2,
        "threshold": 2000  # milliseconds
    },
    "task_completion": {
        "type": "binary",
        "weight": 0.2
    },
    "user_satisfaction": {
        "type": "rating",
        "weight": 0.2,
        "scale": [1, 5]
    },
    "error_rate": {
        "type": "error_count",
        "weight": 0.1
    }
}"""))

    # Test Cases
    nb.cells.append(nbf.v4.new_markdown_cell("""## Creating Test Cases

We'll create a comprehensive set of test cases to evaluate our agent's performance across different scenarios."""))

    nb.cells.append(nbf.v4.new_code_cell("""# Define test cases
test_cases = [
    {
        "scenario": "Password Reset",
        "input": "How do I reset my password?",
        "expected_output": "To reset your password, click the 'Forgot Password' link, enter your email, and follow the instructions sent to your inbox.",
        "expected_completion": True
    },
    {
        "scenario": "Billing Inquiry",
        "input": "When will I be charged for my subscription?",
        "expected_output": "Billing occurs on the 1st of each month for your subscription.",
        "expected_completion": True
    },
    {
        "scenario": "Feature Information",
        "input": "What features are included in the product?",
        "expected_output": "The product includes cloud storage, synchronization capabilities, sharing features, and administrative controls.",
        "expected_completion": True
    }
]"""))

    # Performance Evaluation
    nb.cells.append(nbf.v4.new_markdown_cell("""## Running Performance Evaluation

Now let's create and run a performance evaluation using our defined metrics and test cases."""))

    nb.cells.append(nbf.v4.new_code_cell("""async def evaluate_performance():
    try:
        # Create evaluation run
        evaluation = await evaluation_client.create_evaluation(
            name=f"customer-service-perf-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            metrics=performance_metrics,
            test_cases=test_cases
        )
        
        # Run evaluation
        results = await evaluation.run()
        
        # Create performance report
        report = {
            "overall_score": results.overall_score,
            "metric_scores": results.metric_scores,
            "response_times": results.response_times,
            "error_count": len(results.errors) if results.errors else 0
        }
        
        return report
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        return None

# Run evaluation
report = await evaluate_performance()

# Display results
if report:
    print("Performance Evaluation Results:")
    print(f"Overall Score: {report['overall_score']:.2f}")
    print("\nMetric Scores:")
    for metric, score in report['metric_scores'].items():
        print(f"{metric}: {score:.2f}")
    print(f"\nAverage Response Time: {sum(report['response_times'])/len(report['response_times']):.2f}ms")
    print(f"Total Errors: {report['error_count']}")"""))

    # Analysis and Visualization
    nb.cells.append(nbf.v4.new_markdown_cell("""## Analyzing Results

Let's create some visualizations to better understand our agent's performance."""))

    nb.cells.append(nbf.v4.new_code_cell("""import matplotlib.pyplot as plt
import seaborn as sns

def visualize_results(report):
    if not report:
        print("No data to visualize")
        return
    
    # Prepare data for plotting
    metrics_df = pd.DataFrame([
        {"metric": metric, "score": score}
        for metric, score in report['metric_scores'].items()
    ])
    
    # Create bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=metrics_df, x='metric', y='score')
    plt.title('Performance Metrics Scores')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Visualize results
visualize_results(report)"""))

    # Recommendations
    nb.cells.append(nbf.v4.new_markdown_cell("""## Performance Optimization Recommendations

Based on the evaluation results, here are some recommendations for improving agent performance:

1. If response accuracy is low:
   - Review and update training data
   - Refine prompt engineering
   - Consider using a more capable model

2. If response times are high:
   - Optimize code execution
   - Consider caching frequent responses
   - Review resource allocation

3. If task completion rate is low:
   - Analyze failed scenarios
   - Implement better error handling
   - Add support for edge cases

4. If user satisfaction is low:
   - Improve response quality
   - Add more context awareness
   - Implement feedback loop

5. If error rate is high:
   - Implement robust error handling
   - Add input validation
   - Improve edge case handling"""))

    # Save the notebook
    notebook_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "building_agent", "performance_metrics.ipynb")
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
    create_performance_metrics_notebook()
