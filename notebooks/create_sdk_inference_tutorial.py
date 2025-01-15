import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure AI Inference SDK tutorial."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure AI Inference SDK Tutorial

This notebook demonstrates how to use the Azure AI Inference SDK for generating health and dietary advice.

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## What You'll Learn
- Initializing the inference client
- Generating health recommendations
- Handling responses
- Best practices for health advice"""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.inference import ChatCompletionsClient
import os
import json

# Initialize client
try:
    client = ChatCompletionsClient(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        credential=DefaultAzureCredential()
    )
    print("✓ Successfully initialized ChatCompletionsClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Basic Completion
    cells.append(new_markdown_cell("""## Generating Health Advice

Let's generate some basic health recommendations:"""))

    cells.append(new_code_cell("""async def generate_health_advice(query: str):
    \"\"\"Generate health-related advice.\"\"\"
    try:
        response = await client.complete(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a health advisor providing evidence-based advice. Important guidelines: 1. Always include appropriate health disclaimers 2. Recommend consulting healthcare professionals 3. Be specific about food allergies and restrictions 4. Provide evidence-based guidance"
                },
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating advice: {str(e)}"

# Test health advice generation
queries = [
    "Create a balanced meal plan for someone with type 2 diabetes",
    "What exercises are safe for someone with lower back pain?",
    "List common food allergens and their alternatives"
]

for query in queries:
    print(f"\nQuery: {query}")
    response = await generate_health_advice(query)
    print(f"Response: {response}")"""))

    # Function Calling
    cells.append(new_markdown_cell("""## Using Function Calling

Implement BMI calculation using function calling:"""))

    cells.append(new_code_cell("""async def calculate_bmi(height_inches: float, weight_pounds: float):
    \"\"\"Calculate BMI with function calling.\"\"\"
    try:
        response = await client.complete(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"Calculate BMI for height {height_inches} inches and weight {weight_pounds} pounds"}
            ],
            tools=[{
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
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calculating BMI: {str(e)}"

# Test BMI calculation
height = 69  # 5'9"
weight = 150
bmi_result = await calculate_bmi(height, weight)
print(f"BMI Calculation Result: {bmi_result}")"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Response Handling**
   - Validate responses
   - Include error handling
   - Implement retry logic
   - Monitor performance

2. **Health Advice**
   - Include disclaimers
   - Be specific and clear
   - Reference reliable sources
   - Consider user context

3. **Safety**
   - Implement content filtering
   - Validate medical advice
   - Monitor for misuse"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/sdk_inference_tutorial.ipynb"
    nbf.write(nb, notebook_path)
    print(f"Created {notebook_path}")
    return notebook_path

if __name__ == "__main__":
    notebook_path = create_notebook()
    
    # Run validation
    import sys
    sys.path.append('..')
    from validate_notebook import validate_notebook
    validate_notebook(notebook_path)
