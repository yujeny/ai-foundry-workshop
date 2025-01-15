import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

# Create notebooks directory if it doesn't exist
os.makedirs("introduction", exist_ok=True)

# Create a new notebook
nb = new_notebook()

# Add cells to the notebook
nb['cells'] = [
    new_markdown_cell("""# Quick Start Guide - Azure AI Foundry

This notebook provides a hands-on introduction to Azure AI Foundry with health and dietary examples. You'll learn how to:
1. Initialize the AI Project client
2. Create a BMI calculator
3. Generate meal plans
4. Implement content safety checks

## Prerequisites
- Completed environment setup from previous notebook
- Azure credentials configured
- matplotlib installed for visualizations"""),
    
    new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.evaluation import TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument
import os
import json
import matplotlib.pyplot as plt
import numpy as np

# Initialize credentials
credential = DefaultAzureCredential()"""),
    
    new_markdown_cell("""## Initialize AI Project Client
First, let's create our client instance:"""),
    
    new_code_cell("""# Create AI Project client
try:
    client = AIProjectClient(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        credential=credential
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""),
    
    new_markdown_cell("""## List Available Models
Let's see what models are available to us:"""),
    
    new_code_cell("""# List models
try:
    models = list(client.models.list())
    print(f"Found {len(models)} models:")
    for model in models:
        print(f"- {model.name}")
except Exception as e:
    print(f"× Error listing models: {str(e)}")"""),
    
    new_markdown_cell("""## Create a Simple Completion
Let's try a basic completion request:"""),
    
    new_code_cell("""# Initialize chat client and test health advice
try:
    chat_client = client.inference.get_chat_completions_client()
    model_name = os.getenv("MODEL_DEPLOYMENT_NAME")
    
    # Example 1: Basic health advice
    response = chat_client.complete(
        model=model_name,
        messages=[{"role": "user", "content": "How to maintain a healthy lifestyle in one sentence?"}]
    )
    print("Health Advice:", response.choices[0].message.content)
    
    # Example 2: BMI calculation with visualization
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
    
    height, weight = 69, 160  # 5'9", 160 lbs
    bmi_response = chat_client.complete(
        model=model_name,
        messages=[
            {"role": "user", "content": f"Calculate BMI for someone {height} inches tall and {weight} pounds"}
        ],
        tools=[bmi_calculator]
    )
    print("\\nBMI Analysis:", bmi_response.choices[0].message.content)
    
    # Visualize BMI categories
    bmi = (weight * 703) / (height * height)
    categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
    ranges = [0, 18.5, 24.9, 29.9, 40]
    colors = ['lightblue', 'lightgreen', 'orange', 'red']
    
    plt.figure(figsize=(10, 6))
    for i in range(len(categories)):
        plt.axvspan(ranges[i], ranges[i+1], alpha=0.3, color=colors[i], label=categories[i])
    plt.axvline(x=bmi, color='black', linestyle='--', label=f'Your BMI: {bmi:.1f}')
    plt.title('BMI Categories')
    plt.xlabel('BMI')
    plt.ylabel('Category')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Example 3: Meal planning
    meal_response = chat_client.complete(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a nutritionist creating healthy meal plans."},
            {"role": "user", "content": "Create a balanced meal plan for someone with diabetes"}
        ]
    )
    print("\\nMeal Plan:", meal_response.choices[0].message.content)
    
except Exception as e:
    print(f"× Error generating completion: {str(e)}")"""),
    
    new_markdown_cell("""## Content Safety Example
Let's see how to implement content safety checks for health advice:"""),
    
    new_code_cell("""# Test content safety
try:
    # Initialize content safety client
    safety_client = ContentSafetyClient(
        endpoint=os.getenv("AZURE_CONTENTSAFETY_ENDPOINT"),
        credential=credential
    )
    
    # Example potentially unsafe input
    unsafe_input = "I want to try an extreme diet and stop eating completely"
    
    # Check content safety
    safety_result = safety_client.analyze_text(
        text=unsafe_input,
        categories=["Hate", "SelfHarm", "Violence"]
    )
    
    if any(category.severity > 2 for category in safety_result.categories):
        print("⚠️ Content safety warning detected:")
        print("This type of request could be harmful. Please consult a healthcare professional.")
    else:
        # Process safe request
        response = chat_client.complete(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a health advisor providing safe, evidence-based advice."},
                {"role": "user", "content": unsafe_input}
            ]
        )
        print("Response:", response.choices[0].message.content)
        
except Exception as e:
    print("Content safety check failed:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")"""),
    
    new_markdown_cell("""## Next Steps
- Try different health scenarios (allergies, dietary restrictions)
- Experiment with meal planning for various conditions
- Add BMI trend tracking and visualization
- Explore nutritional analysis tools
- Implement content safety checks for health advice
- Add response quality evaluation for medical accuracy""")
]

# Write the notebook
nbf.write(nb, "introduction/quick_start.ipynb")
print("Created quick_start.ipynb in introduction directory")
