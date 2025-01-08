# Evaluating Agents

Learn how to comprehensively evaluate AI agents using Azure AI Evaluation's advanced capabilities and best practices.

## Evaluation Strategy

### 1. Performance Assessment
- Response accuracy
- Processing speed
- Resource efficiency
- Scalability metrics
- Error rates
- Recovery times

### 2. Behavioral Analysis
- Decision quality
- Adaptation capability
- Learning patterns
- Error handling
- Context awareness
- Task completion

### 3. User Experience
- Interaction quality
- Response relevance
- User satisfaction
- Task efficiency
- Error recovery
- Overall usability

## Evaluation Methods

### 1. Quantitative Analysis
```python
from azure.ai.evaluation import EvaluationClient
from azure.identity import DefaultAzureCredential
import pandas as pd
import numpy as np

def perform_quantitative_analysis(agent_id: str, test_cases: list):
    """Perform quantitative analysis of agent performance."""
    try:
        # Initialize evaluation client
        credential = DefaultAzureCredential()
        client = EvaluationClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Collect performance metrics
        metrics = []
        for test in test_cases:
            result = client.evaluate_agent(
                agent_id=agent_id,
                input_data=test["input"],
                expected_output=test["expected"],
                metrics=["response_time", "accuracy", "resource_usage"]
            )
            metrics.append(result)
        
        # Analyze results
        df = pd.DataFrame(metrics)
        analysis = {
            "avg_response_time": df["response_time"].mean(),
            "accuracy_rate": df["accuracy"].mean(),
            "avg_resource_usage": df["resource_usage"].mean(),
            "error_rate": 1 - df["success"].mean(),
            "p95_response_time": df["response_time"].quantile(0.95)
        }
        
        return analysis
    except Exception as e:
        print(f"Error in quantitative analysis: {str(e)}")
        raise
```

### 2. Qualitative Analysis
```python
def perform_qualitative_analysis(agent_id: str, test_cases: list):
    """Perform qualitative analysis of agent responses."""
    try:
        # Initialize evaluation client
        credential = DefaultAzureCredential()
        client = EvaluationClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Evaluate response quality
        quality_metrics = []
        for test in test_cases:
            result = client.evaluate_response_quality(
                agent_id=agent_id,
                input_data=test["input"],
                response=test["response"],
                evaluation_criteria={
                    "relevance": True,
                    "coherence": True,
                    "completeness": True,
                    "correctness": True
                }
            )
            quality_metrics.append(result)
        
        # Analyze quality results
        quality_analysis = {
            "avg_relevance": np.mean([m["relevance"] for m in quality_metrics]),
            "avg_coherence": np.mean([m["coherence"] for m in quality_metrics]),
            "avg_completeness": np.mean([m["completeness"] for m in quality_metrics]),
            "avg_correctness": np.mean([m["correctness"] for m in quality_metrics])
        }
        
        return quality_analysis
    except Exception as e:
        print(f"Error in qualitative analysis: {str(e)}")
        raise
```

### 3. Comparative Analysis
```python
def perform_comparative_analysis(agent_ids: list, benchmark_data: dict):
    """Compare multiple agent versions or implementations."""
    try:
        # Initialize evaluation client
        credential = DefaultAzureCredential()
        client = EvaluationClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Compare agents
        comparison_results = []
        for agent_id in agent_ids:
            # Evaluate against benchmark
            result = client.evaluate_agent_benchmark(
                agent_id=agent_id,
                benchmark_data=benchmark_data,
                metrics=["accuracy", "response_time", "resource_usage"]
            )
            
            # Calculate performance score
            performance_score = calculate_performance_score(result)
            comparison_results.append({
                "agent_id": agent_id,
                "performance_score": performance_score,
                "metrics": result
            })
        
        return comparison_results
    except Exception as e:
        print(f"Error in comparative analysis: {str(e)}")
        raise

def calculate_performance_score(result: dict) -> float:
    """Calculate overall performance score based on multiple metrics."""
    weights = {
        "accuracy": 0.4,
        "response_time": 0.3,
        "resource_usage": 0.3
    }
    
    score = (
        result["accuracy"] * weights["accuracy"] +
        (1 / result["response_time"]) * weights["response_time"] +
        (1 / result["resource_usage"]) * weights["resource_usage"]
    )
    
    return score

## Evaluation Scenarios

### 1. Functional Testing
```python
def perform_functional_testing(agent_id: str):
    """Execute functional tests for core agent capabilities."""
    try:
        # Initialize evaluation client
        credential = DefaultAzureCredential()
        client = EvaluationClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Define test cases
        test_cases = [
            {
                "name": "Basic Response",
                "input": "Hello, how are you?",
                "expected": "greeting"
            },
            {
                "name": "Task Completion",
                "input": "Schedule a meeting for tomorrow",
                "expected": "task_scheduling"
            },
            {
                "name": "Error Handling",
                "input": "Invalid request format",
                "expected": "error_response"
            }
        ]
        
        # Execute tests
        results = []
        for test in test_cases:
            result = client.test_agent_function(
                agent_id=agent_id,
                test_case=test,
                validation_rules={
                    "response_format": True,
                    "error_handling": True,
                    "completion_check": True
                }
            )
            results.append(result)
        
        return results
    except Exception as e:
        print(f"Error in functional testing: {str(e)}")
        raise
```

### 2. Load Testing
```python
async def perform_load_testing(agent_id: str, concurrent_users: int):
    """Execute load tests to assess agent performance under stress."""
    try:
        # Initialize evaluation client
        credential = DefaultAzureCredential()
        client = EvaluationClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Configure load test
        load_config = {
            "concurrent_users": concurrent_users,
            "duration_seconds": 300,
            "ramp_up_seconds": 60,
            "test_scenarios": [
                {
                    "weight": 0.7,
                    "input": "Standard request",
                },
                {
                    "weight": 0.3,
                    "input": "Complex request",
                }
            ]
        }
        
        # Execute load test
        result = await client.execute_load_test(
            agent_id=agent_id,
            load_config=load_config,
            metrics=["response_time", "error_rate", "throughput"]
        )
        
        return result
    except Exception as e:
        print(f"Error in load testing: {str(e)}")
        raise
```

### 3. Endurance Testing
```python
async def perform_endurance_testing(agent_id: str, duration_hours: int):
    """Execute long-running tests to assess agent stability."""
    try:
        # Initialize evaluation client
        credential = DefaultAzureCredential()
        client = EvaluationClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Configure endurance test
        test_config = {
            "duration_hours": duration_hours,
            "monitoring_interval_minutes": 5,
            "test_scenarios": [
                "basic_interaction",
                "complex_task",
                "error_scenario"
            ],
            "metrics": [
                "memory_usage",
                "response_time",
                "error_rate",
                "resource_utilization"
            ]
        }
        
        # Execute endurance test
        result = await client.execute_endurance_test(
            agent_id=agent_id,
            test_config=test_config
        )
        
        # Analyze stability metrics
        stability_analysis = analyze_stability_metrics(result)
        
        return stability_analysis
    except Exception as e:
        print(f"Error in endurance testing: {str(e)}")
        raise

def analyze_stability_metrics(result: dict) -> dict:
    """Analyze stability metrics from endurance test results."""
    return {
        "memory_leak_detected": check_memory_growth(result["memory_usage"]),
        "performance_degradation": calculate_degradation(result["response_time"]),
        "error_accumulation": analyze_error_pattern(result["error_rate"]),
        "resource_efficiency": calculate_resource_efficiency(result["resource_utilization"])
    }

## Analysis and Reporting

### 1. Data Collection
- Metric gathering
- Log analysis
- User feedback
- System metrics
- Cost data
- Performance data

### 2. Analysis Methods
- Statistical analysis
- Pattern recognition
- Trend analysis
- Anomaly detection
- Root cause analysis
- Impact assessment

### 3. Report Generation
- Performance reports
- Quality metrics
- Resource usage
- Cost analysis
- Improvement recommendations
- Action plans

## Continuous Improvement

### 1. Performance Optimization
- Resource tuning
- Response optimization
- Error reduction
- Cost efficiency
- Quality improvement
- Process refinement

### 2. Feature Enhancement
- Capability expansion
- Integration improvement
- Security enhancement
- User experience
- Documentation updates
- Training materials

### 3. Process Improvement
- Workflow optimization
- Tool enhancement
- Documentation updates
- Team training
- Knowledge sharing
- Best practices

Next: [Workshop Conclusion](../conclusion.md)
