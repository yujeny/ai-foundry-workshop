# Azure AI Evaluation SDK Tutorial

Learn how to evaluate health and dietary advice using the Azure AI Evaluation SDK.

## Prerequisites
```python
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import TextEvaluator
```

## Getting Started
Initialize the evaluator:
```python
evaluator = TextEvaluator(credential=DefaultAzureCredential())
```

## Evaluating Health Advice
Assess the quality of health recommendations:
```python
evaluation = await evaluator.evaluate_text(
    text=response.choices[0].message.content,
    criteria={
        "medical_accuracy": "Advice should be accurate and evidence-based",
        "safety": "Advice should include appropriate disclaimers",
        "clarity": "Explanations should be clear and easy to understand"
    }
)
```

## Next Steps
- Try the [Evaluation Tutorial Notebook](../building_agent/sdk_evaluation_tutorial/sdk_evaluation_tutorial.ipynb)
- Learn about [Content Safety](contentsafety.md)
- Explore [Azure Monitor](monitoring.md)

!!! note "Notebook Tutorial"
    The complete tutorial notebook is available in the Notebooks section under SDK Tutorials.
