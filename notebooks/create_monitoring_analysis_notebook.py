import nbformat as nbf
import os

def create_monitoring_analysis_notebook():
    """Create a Jupyter notebook for monitoring and analysis of AI agent evaluation."""
    nb = nbf.v4.new_notebook()
    
    # Title and Overview
    title_cell = """# Monitoring and Analysis in Azure AI Evaluation
    
This notebook demonstrates how to set up monitoring and analyze evaluation results for your customer service AI agent.

## Prerequisites
- Azure subscription with access to Azure AI Foundry
- Python environment with required packages installed
- Completed the Performance Metrics notebook
- Working customer service agent implementation

## Learning Objectives
- Set up real-time monitoring
- Configure alerts and notifications
- Analyze evaluation trends
- Create performance dashboards
- Implement continuous improvement
"""
    nb.cells.append(nbf.v4.new_markdown_cell(title_cell))

    # Setup and Imports
    setup_code = """import os
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
from azure.ai.evaluation import EvaluationClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import asyncio

# Initialize Azure clients
credential = DefaultAzureCredential()
project_client = AIProjectClient(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    credential=credential
)
evaluation_client = EvaluationClient(credential=credential)"""
    nb.cells.append(nbf.v4.new_code_cell(setup_code))

    # Monitoring Setup
    monitoring_md = """## Setting Up Monitoring

Let's configure real-time monitoring for our customer service agent."""
    nb.cells.append(nbf.v4.new_markdown_cell(monitoring_md))

    monitoring_code = """async def setup_monitoring():
    '''Configure monitoring settings for the evaluation system.'''
    try:
        monitoring_config = {
            "metrics": {
                "collection_interval": "1m",
                "retention_days": 30,
                "metrics_to_track": [
                    "response_time",
                    "accuracy_score",
                    "user_satisfaction",
                    "error_rate",
                    "completion_rate"
                ]
            },
            "alerts": {
                "error_rate_threshold": 0.2,
                "response_time_threshold_ms": 2000,
                "accuracy_threshold": 0.8,
                "notification_channels": ["email"]
            },
            "dashboard": {
                "refresh_interval": "5m",
                "widgets": [
                    "performance_metrics",
                    "error_tracking",
                    "user_satisfaction"
                ]
            }
        }
        
        # Apply monitoring configuration
        await evaluation_client.configure_monitoring(monitoring_config)
        print("✓ Monitoring configuration applied successfully")
        return monitoring_config
    except Exception as e:
        print(f"Error setting up monitoring: {str(e)}")
        return None

# Set up monitoring
monitoring_config = await setup_monitoring()"""
    nb.cells.append(nbf.v4.new_code_cell(monitoring_code))

    # Real-time Monitoring
    realtime_md = """## Real-time Monitoring

Now let's implement real-time monitoring of our agent's performance."""
    nb.cells.append(nbf.v4.new_markdown_cell(realtime_md))

    realtime_code = """async def monitor_performance(duration_minutes=5):
    '''Monitor agent performance in real-time.'''
    try:
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        metrics_data = []
        
        print(f"Starting performance monitoring for {duration_minutes} minutes...")
        
        while datetime.now() < end_time:
            # Collect current metrics
            current_metrics = await evaluation_client.get_current_metrics()
            
            metrics_data.append({
                'timestamp': datetime.now(),
                'response_time': current_metrics.get('response_time', 0),
                'accuracy': current_metrics.get('accuracy_score', 0),
                'error_rate': current_metrics.get('error_rate', 0),
                'satisfaction': current_metrics.get('user_satisfaction', 0)
            })
            
            # Check for alerts
            if current_metrics.get('error_rate', 0) > monitoring_config['alerts']['error_rate_threshold']:
                print(f"⚠️ Alert: High error rate detected: {current_metrics['error_rate']:.2f}")
            
            await asyncio.sleep(60)  # Wait for 1 minute
            
        return pd.DataFrame(metrics_data)
    except Exception as e:
        print(f"Monitoring error: {str(e)}")
        return None

# Run monitoring for 5 minutes
metrics_df = await monitor_performance(duration_minutes=5)"""
    nb.cells.append(nbf.v4.new_code_cell(realtime_code))

    # Analysis
    analysis_md = """## Performance Analysis

Let's analyze the collected metrics and create visualizations."""
    nb.cells.append(nbf.v4.new_markdown_cell(analysis_md))

    analysis_code = """def analyze_performance(metrics_df):
    '''Analyze and visualize performance metrics.'''
    if metrics_df is None or len(metrics_df) == 0:
        print("No data available for analysis")
        return
    
    # Create performance dashboard
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Response Time Trend
    sns.lineplot(data=metrics_df, x='timestamp', y='response_time', ax=axes[0,0])
    axes[0,0].set_title('Response Time Trend')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Accuracy Trend
    sns.lineplot(data=metrics_df, x='timestamp', y='accuracy', ax=axes[0,1])
    axes[0,1].set_title('Accuracy Trend')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Error Rate
    sns.lineplot(data=metrics_df, x='timestamp', y='error_rate', ax=axes[1,0])
    axes[1,0].set_title('Error Rate Trend')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # User Satisfaction
    sns.lineplot(data=metrics_df, x='timestamp', y='satisfaction', ax=axes[1,1])
    axes[1,1].set_title('User Satisfaction Trend')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate summary statistics
    summary = {
        'avg_response_time': metrics_df['response_time'].mean(),
        'avg_accuracy': metrics_df['accuracy'].mean(),
        'avg_error_rate': metrics_df['error_rate'].mean(),
        'avg_satisfaction': metrics_df['satisfaction'].mean()
    }
    
    print("\nPerformance Summary:")
    for metric, value in summary.items():
        print(f"{metric}: {value:.2f}")

# Analyze collected metrics
analyze_performance(metrics_df)"""
    nb.cells.append(nbf.v4.new_code_cell(analysis_code))

    # Continuous Improvement
    improvement_md = """## Continuous Improvement

Based on the monitoring and analysis results, let's implement some improvements."""
    nb.cells.append(nbf.v4.new_markdown_cell(improvement_md))

    improvement_code = """def generate_improvement_recommendations(metrics_df):
    '''Generate recommendations based on performance analysis.'''
    if metrics_df is None or len(metrics_df) == 0:
        return "No data available for recommendations"
    
    recommendations = []
    
    # Analyze response time
    avg_response_time = metrics_df['response_time'].mean()
    if avg_response_time > 1000:  # If average response time > 1 second
        recommendations.append(
            "Response Time: Consider implementing caching or optimizing model inference"
        )
    
    # Analyze accuracy
    avg_accuracy = metrics_df['accuracy'].mean()
    if avg_accuracy < 0.9:
        recommendations.append(
            "Accuracy: Review training data and consider model fine-tuning"
        )
    
    # Analyze error rate
    avg_error_rate = metrics_df['error_rate'].mean()
    if avg_error_rate > 0.1:
        recommendations.append(
            "Error Rate: Implement better error handling and edge case detection"
        )
    
    # Analyze user satisfaction
    avg_satisfaction = metrics_df['satisfaction'].mean()
    if avg_satisfaction < 4.0:
        recommendations.append(
            "User Satisfaction: Review user feedback and improve response quality"
        )
    
    return recommendations

# Generate improvement recommendations
recommendations = generate_improvement_recommendations(metrics_df)
print("Improvement Recommendations:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")"""
    nb.cells.append(nbf.v4.new_code_cell(improvement_code))

    # Save the notebook
    notebook_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "building_agent", "monitoring_analysis.ipynb")
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
    create_monitoring_analysis_notebook()
