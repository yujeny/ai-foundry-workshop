# Testing Your Health Advisor Model 🧪

Let's verify that your deployed model works correctly for health and fitness scenarios. This will take about 15 minutes. Remember to validate medical disclaimers and safety checks! ⚕️

## Quick Test

```python
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os

def test_health_advisor_model():
    """Test the deployed health advisor model."""
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Test cases
        test_cases = [
            {
                "input": "How do I reset my password?",
                "expected_topics": ["password", "reset", "account"]
            },
            {
                "input": "When is my next billing date?",
                "expected_topics": ["billing", "payment", "date"]
            },
            {
                "input": "What features are included?",
                "expected_topics": ["features", "product", "capabilities"]
            }
        ]
        
        # Run tests
        results = []
        for test in test_cases:
            response = client.models.generate(
                deployment_name="health-advisor-v1",
                prompt=test["input"],
                max_tokens=100
            )
            
            # Simple topic check
            topics_found = any(
                topic in response.lower() 
                for topic in test["expected_topics"]
            )
            
            results.append({
                "input": test["input"],
                "response": response,
                "topics_found": topics_found
            })
        
        return results
    except Exception as e:
        print(f"Testing error: {str(e)}")
        raise

# Usage example
if __name__ == "__main__":
    results = test_customer_service_model()
    for result in results:
        print(f"\nTest: {result['input']}")
        print(f"Response: {result['response']}")
        print(f"Topics found: {result['topics_found']}")
```

## What to Check

1. **Response Relevance**
   - Does the model understand customer queries?
   - Are responses on-topic and helpful?
   - Is the context maintained?

2. **Response Quality**
   - Clear and concise answers
   - Professional tone
   - Accurate information

3. **Error Handling**
   - Graceful handling of unclear queries
   - Appropriate error messages
   - Fallback responses

## Interactive Workshop

For hands-on practice with model testing in Azure AI Foundry, try our interactive notebook:

[Launch Model Testing Workshop](../2-notebooks/2-agent_service/4-bing_grounding.ipynb)

This notebook provides:
- Basic model testing examples
- Performance evaluation techniques
- Load testing scenarios
- Error handling and validation
- Best practices for comprehensive testing

Next: [Creating Your Agent](../agents/implementation.md)
