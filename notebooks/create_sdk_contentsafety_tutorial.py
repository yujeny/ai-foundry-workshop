import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure AI Content Safety SDK tutorial."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure AI Content Safety SDK Tutorial

This notebook demonstrates how to implement content safety checks for health and medical advice.

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## What You'll Learn
- Initializing the content safety client
- Analyzing text for safety concerns
- Handling safety check results
- Best practices for health content"""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.contentsafety import ContentSafetyClient
import os
import json

# Initialize client
try:
    client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENTSAFETY_ENDPOINT"),
        credential=DefaultAzureCredential()
    )
    print("✓ Successfully initialized ContentSafetyClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Basic Safety Check
    cells.append(new_markdown_cell("""## Content Safety Analysis

Let's analyze some health-related content:"""))

    cells.append(new_code_cell("""async def check_content_safety(text: str):
    \"\"\"Analyze text for safety concerns.\"\"\"
    try:
        result = await client.analyze_text(
            text=text,
            categories=["Hate", "SelfHarm", "Violence"]
        )
        
        # Check severity levels
        concerns = []
        for category in result.categories:
            if category.severity > 2:
                concerns.append(f"{category.category}: {category.severity}")
        
        return {
            "safe": len(concerns) == 0,
            "concerns": concerns,
            "result": result
        }
    except Exception as e:
        return f"Error checking content: {str(e)}"

# Test content safety
sample_content = [
    "Maintain a balanced diet and exercise regularly for good health.",
    "Consult your doctor before starting any new diet or exercise program.",
    "Some health conditions require special dietary considerations."
]

for content in sample_content:
    print(f"\nAnalyzing content: {content}")
    result = await check_content_safety(content)
    print(f"Safety check result: {result}")"""))

    # Health Content Guidelines
    cells.append(new_markdown_cell("""## Health Content Guidelines

Implement specific checks for health-related content:"""))

    cells.append(new_code_cell("""async def validate_health_content(content: str):
    \"\"\"Validate health-related content.\"\"\"
    try:
        # Check content safety
        safety_result = await check_content_safety(content)
        
        if not safety_result["safe"]:
            return {
                "valid": False,
                "reason": f"Safety concerns: {safety_result['concerns']}"
            }
        
        # Additional health-specific checks
        required_disclaimers = [
            "consult",
            "healthcare",
            "professional",
            "medical"
        ]
        
        has_disclaimer = any(term in content.lower() for term in required_disclaimers)
        
        return {
            "valid": has_disclaimer,
            "reason": "Missing medical disclaimer" if not has_disclaimer else "Content approved"
        }
    except Exception as e:
        return f"Error validating content: {str(e)}"

# Test health content validation
health_advice = [
    "For weight management, consult your healthcare provider about appropriate diet and exercise.",
    "Try this new miracle diet for instant results!",
    "Discuss any dietary changes with your medical professional."
]

for advice in health_advice:
    print(f"\nValidating advice: {advice}")
    result = await validate_health_content(advice)
    print(f"Validation result: {result}")"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Content Analysis**
   - Check all relevant categories
   - Consider context
   - Implement appropriate thresholds
   - Monitor false positives

2. **Health Content**
   - Require medical disclaimers
   - Validate professional references
   - Check for misleading claims
   - Monitor user feedback

3. **Safety Measures**
   - Regular content reviews
   - Update safety criteria
   - Document decisions
   - Maintain audit trails"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/sdk_contentsafety_tutorial.ipynb"
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
