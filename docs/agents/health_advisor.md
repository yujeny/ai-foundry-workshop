# Health Advisor Agent Example

This guide demonstrates how to create a health advisor agent using Azure AI Foundry SDKs. The agent provides dietary advice, BMI calculations, and nutritional guidance while ensuring content safety.

## Prerequisites

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.evaluation import TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument
```

## Creating the Health Advisor Agent

The health advisor agent combines multiple Azure AI capabilities:
- Content safety checks for medical advice
- BMI calculation using code interpreter
- Nutritional guidance with proper disclaimers
- Dietary restriction handling

### Basic Implementation

```python
class HealthAdvisorAgent:
    def __init__(self):
        credential = DefaultAzureCredential()
        self.client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        self.inference_client = ChatCompletionsClient(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            credential=credential
        )
        self.safety_client = ContentSafetyClient(
            endpoint=os.getenv("AZURE_CONTENTSAFETY_ENDPOINT"),
            credential=credential
        )

    async def process_request(self, user_input: str) -> str:
        # Content safety check
        safety_result = await self.safety_client.analyze_text(
            text=user_input,
            categories=["Hate", "SelfHarm", "Violence"]
        )
        
        if any(category.severity > 2 for category in safety_result.categories):
            return "I apologize, but I cannot provide advice on that topic. Please consult a healthcare professional."
        
        # Process health-related query
        response = await self.inference_client.complete(
            deployment_name="health-advisor-v1",
            messages=[
                {"role": "system", "content": """You are a knowledgeable health advisor. Important guidelines:
                1. Always include appropriate health disclaimers
                2. Recommend consulting healthcare professionals for medical advice
                3. Be specific about food allergies and restrictions
                4. Provide evidence-based nutritional guidance
                5. Clearly explain BMI calculations and interpretations"""},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
```

### BMI Calculator Implementation

```python
def setup_bmi_calculator():
    return {
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

# Usage example
agent = HealthAdvisorAgent()
bmi_calculator = setup_bmi_calculator()

response = await agent.inference_client.complete(
    deployment_name="health-advisor-v1",
    messages=[
        {"role": "system", "content": "You are a health advisor."},
        {"role": "user", "content": "Calculate BMI for someone 5'9\" and 198 pounds"}
    ],
    tools=[bmi_calculator]
)
```

## Safety and Evaluation

The agent includes multiple safety measures:

1. Content Safety Checks
```python
safety_result = await safety_client.analyze_text(
    text=user_input,
    categories=["Hate", "SelfHarm", "Violence"]
)
```

2. Response Quality Evaluation
```python
evaluation = await evaluation_client.evaluate_text(
    text=response.choices[0].message.content,
    criteria={
        "medical_accuracy": "Advice should be accurate and evidence-based",
        "safety": "Advice should prioritize user safety and include disclaimers",
        "clarity": "Explanations should be clear and easy to understand"
    }
)
```

## Example Usage

Here are some example interactions:

1. BMI Calculation
```python
response = await agent.process_request(
    "Calculate BMI for someone who is 5'9\" and 198 pounds"
)
```

2. Dietary Restrictions
```python
response = await agent.process_request(
    "I have a peanut allergy, what foods should I avoid?"
)
```

3. Meal Planning
```python
response = await agent.process_request(
    "Create a weekly meal plan for someone with type 2 diabetes"
)
```

!!! note "Important"
    Always include appropriate medical disclaimers and recommend consulting healthcare professionals for medical advice.

!!! warning "Content Safety"
    The agent includes content safety checks to ensure responsible health advice.

For more information, see the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/).
