## Medication Analysis Agent

This agent provides medication analysis capabilities including:
- Common uses and indications
- Mechanism of action analysis
- Side effect assessment
- Drug interaction warnings
- Special population considerations

### Usage

```python
from agents.medication import MedicationAgent

agent = MedicationAgent(project_client, chat_client, config)
result = await agent.process({
    "name": "Medication Name",
    "notes": "Optional additional context"
})
```

### Response Format

The agent returns structured information and an AI-generated explanation:

```python
{
    "structured_info": {
        "common_uses": str,
        "mechanism": str,
        "side_effects": str,
        "interactions": str,
        "contraindications": str,
        "special_populations": str
    },
    "ai_explanation": str,
    "disclaimer": str
}
```

### OpenTelemetry Integration

The agent includes OpenTelemetry tracing for monitoring and debugging:
- Span: "medication_analysis"
- Attributes: medication.name
- Error tracking with full stack traces
