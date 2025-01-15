import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for Azure AI Evaluation SDK tutorial."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Azure AI Evaluation SDK Tutorial

This notebook demonstrates how to evaluate health and dietary advice using the Azure AI Evaluation SDK.

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## What You'll Learn
- Initializing the evaluation client
- Evaluating health recommendations
- Analyzing evaluation results
- Best practices for health advice evaluation"""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import TextEvaluator
import os
import json

# Initialize evaluator
try:
    evaluator = TextEvaluator(credential=DefaultAzureCredential())
    print("✓ Successfully initialized TextEvaluator")
except Exception as e:
    print(f"× Error initializing evaluator: {str(e)}")"""))

    # Basic Evaluation
    cells.append(new_markdown_cell("""## Evaluating Health Advice

Let's evaluate some health recommendations:"""))

    cells.append(new_code_cell("""async def evaluate_health_advice(text: str):
    \"\"\"Evaluate health-related advice.\"\"\"
    try:
        evaluation = await evaluator.evaluate_text(
            text=text,
            criteria={
                "medical_accuracy": "Advice should be accurate and evidence-based",
                "safety": "Advice should include appropriate disclaimers",
                "clarity": "Explanations should be clear and easy to understand"
            }
        )
        return evaluation
    except Exception as e:
        return f"Error evaluating advice: {str(e)}"

# Test health advice evaluation
sample_advice = [
    "To manage type 2 diabetes, maintain a balanced diet low in refined carbohydrates. Always consult your healthcare provider before making significant dietary changes.",
    "For weight management, combine regular exercise with a balanced diet. Monitor your progress and adjust as needed.",
    "When dealing with food allergies, carefully read ingredient labels and avoid cross-contamination."
]

for advice in sample_advice:
    print(f"\nEvaluating advice: {advice}")
    result = await evaluate_health_advice(advice)
    print(f"Evaluation result: {result}")"""))

    # Custom Evaluation
    cells.append(new_markdown_cell("""## Custom Evaluation Criteria

Create custom evaluation criteria for specific health scenarios:"""))

    cells.append(new_code_cell("""async def evaluate_dietary_plan(meal_plan: str):
    \"\"\"Evaluate a dietary plan.\"\"\"
    try:
        evaluation = await evaluator.evaluate_text(
            text=meal_plan,
            criteria={
                "nutritional_balance": "Plan includes all essential food groups",
                "portion_control": "Appropriate portion sizes are specified",
                "dietary_restrictions": "Accounts for common allergies and restrictions",
                "practicality": "Meals are practical to prepare"
            }
        )
        return evaluation
    except Exception as e:
        return f"Error evaluating meal plan: {str(e)}"

# Test meal plan evaluation
sample_plan = \"\"\"
Breakfast: Oatmeal with berries and nuts (1 cup oats, 1/2 cup berries)
Lunch: Grilled chicken salad with olive oil dressing
Dinner: Baked salmon with quinoa and steamed vegetables
Snacks: Apple slices with almond butter, Greek yogurt
\"\"\"

result = await evaluate_dietary_plan(sample_plan)
print(f"Meal Plan Evaluation: {result}")"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Evaluation Criteria**
   - Use specific, measurable criteria
   - Include safety considerations
   - Consider medical accuracy
   - Evaluate clarity and practicality

2. **Result Analysis**
   - Review all evaluation metrics
   - Consider context
   - Look for patterns
   - Document findings

3. **Continuous Improvement**
   - Use feedback to improve advice
   - Update evaluation criteria
   - Monitor trends
   - Maintain quality standards"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/sdk_evaluation_tutorial.ipynb"
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
