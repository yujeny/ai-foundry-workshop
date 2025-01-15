---
markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - admonition
  - def_list
  - pymdownx.details
---

# Dietary Planning with Azure AI

This guide demonstrates how to implement dietary planning scenarios using Azure AI Foundry's latest SDKs.

!!! note "SDK Updates"
    This guide uses the latest Azure AI SDKs:
    ```python
    from azure.ai.projects import AIProjectClient
    from azure.ai.inference import ChatCompletionsClient
    ```

## Quick Start Example

Here's a simple example of getting dietary advice:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient

# Initialize clients
credential = DefaultAzureCredential()
project_client = AIProjectClient(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    credential=credential
)

chat_client = project_client.inference.get_chat_completions_client()
response = chat_client.complete(
    model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    messages=[{"role": "user", "content": "How to be healthy in one sentence?"}]
)
print(response.choices[0].message.content)
```

## Dietary Planning Scenarios

??? example "BMI Calculation"
    ```python
    bmi_calculator = {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "Calculate BMI given height and weight",
            "parameters": {
                "type": "object",
                "properties": {
                    "height_inches": {"type": "number"},
                    "weight_pounds": {"type": "number"}
                }
            }
        }
    }

    response = chat_client.complete(
        model=model_name,
        messages=[
            {"role": "user", "content": "Calculate BMI for 5'9\" and 160 pounds"}
        ],
        tools=[bmi_calculator]
    )
    ```

??? example "Meal Planning"
    ```python
    response = chat_client.complete(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a nutritionist creating healthy meal plans."},
            {"role": "user", "content": "Create a balanced meal plan for diabetes"}
        ]
    )
    ```

??? example "Dietary Restrictions"
    ```python
    response = chat_client.complete(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a dietary advisor."},
            {"role": "user", "content": "What foods should I avoid with celiac disease?"}
        ]
    )
    ```

## Content Safety

!!! warning "Medical Advice"
    Always include content safety checks when providing health-related advice:
    ```python
    from azure.ai.contentsafety import ContentSafetyClient
    
    safety_client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENTSAFETY_ENDPOINT"),
        credential=credential
    )
    
    safety_result = await safety_client.analyze_text(
        text=user_input,
        categories=["Hate", "SelfHarm", "Violence"]
    )
    ```

## Response Evaluation

Use the TextEvaluator to assess dietary advice quality:

```python
from azure.ai.evaluation import TextEvaluator

evaluator = TextEvaluator(credential=credential)
evaluation = await evaluator.evaluate_text(
    text=response.choices[0].message.content,
    criteria={
        "medical_accuracy": "Advice should be accurate and evidence-based",
        "safety": "Advice should include appropriate disclaimers",
        "clarity": "Explanations should be clear and easy to understand"
    }
)
```

## Best Practices

1. Always include health disclaimers
2. Validate nutritional information
3. Consider dietary restrictions
4. Monitor response quality
5. Implement safety checks

!!! tip "Monitoring"
    Use Azure Monitor OpenTelemetry for tracking:
    ```python
    import azure.monitor.opentelemetry._autoinstrument
    ```

For more examples and detailed documentation, see the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/).
