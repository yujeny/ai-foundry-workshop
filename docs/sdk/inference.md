# 🤖 Azure AI Inference SDK Tutorial

This tutorial demonstrates how to use the Azure AI Inference SDK for generating health and dietary advice. Let's build some intelligent health recommendations! 🏃‍♂️ 🥗

## Process Flow

```mermaid
sequenceDiagram
    participant Client
    participant Inference as AI Inference
    participant Safety as Content Safety
    participant Model as AI Model
    
    Client->>Inference: Initialize client
    activate Inference
    
    rect rgb(200, 220, 255)
        note right of Inference: Health Advice Request
        Client->>Inference: Request completion
        Inference->>Safety: Check content
        Safety-->>Inference: Content approved
        Inference->>Model: Generate response
        Model-->>Inference: Raw completion
        Inference->>Inference: Add health disclaimers
        Inference-->>Client: Safe health advice
    end
    
    deactivate Inference
    
    note over Client,Model: All health-related responses<br/>include appropriate disclaimers
```

## Prerequisites
```python
from azure.identity import DefaultAzureCredential
from azure.ai.inference import ChatCompletionsClient
```

## Getting Started
Initialize the chat client for health advice:
```python
client = ChatCompletionsClient(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    credential=DefaultAzureCredential()
)
```

## Health Advice Example
Generate personalized health recommendations:
```python
response = await client.complete(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a health advisor providing evidence-based advice."},
        {"role": "user", "content": "Create a balanced meal plan for diabetes"}
    ],
    temperature=0.7
)
print(response.choices[0].message.content)
```

## Next Steps
- Try the [Inference Tutorial Notebook](../2-notebooks/1-chat_completion/2-embeddings.ipynb)
- Learn about [Azure AI Evaluation](evaluation.md)
- Explore [Azure Monitor](monitoring.md)

!!! note "Notebook Tutorial"
    The complete tutorial notebook is available in the Notebooks section under SDK Tutorials.
