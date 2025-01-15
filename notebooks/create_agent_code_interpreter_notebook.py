import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for health calculations using code interpreter."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Health Calculator Agent Tutorial

This notebook demonstrates how to create an AI agent that performs health-related calculations using the code interpreter. You'll learn:
1. Setting up a code interpreter agent
2. Implementing BMI calculations
3. Analyzing nutritional data
4. Generating health insights

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts
- Sample health/nutrition data files

## Important Note
The calculations provided are for educational purposes. Always consult healthcare professionals for medical advice."""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose
import os
import pandas as pd
import matplotlib.pyplot as plt

# Initialize client
try:
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Create Sample Data
    cells.append(new_markdown_cell("""## Prepare Sample Data

First, let's create a sample nutrition dataset:"""))

    cells.append(new_code_cell("""# Create sample nutrition data
import pandas as pd

def create_sample_data():
    \"\"\"Create a sample nutrition dataset.\"\"\"
    try:
        # Create sample data
        data = {
            'Date': pd.date_range(start='2024-01-01', periods=7),
            'Calories': [2100, 1950, 2300, 2050, 1900, 2200, 2150],
            'Protein_g': [80, 75, 85, 78, 72, 82, 79],
            'Carbs_g': [250, 230, 270, 245, 225, 260, 255],
            'Fat_g': [70, 65, 75, 68, 63, 73, 71],
            'Fiber_g': [25, 22, 28, 24, 21, 26, 23]
        }
        df = pd.DataFrame(data)
        
        # Save to CSV
        filename = "nutrition_data.csv"
        df.to_csv(filename, index=False)
        print(f"✓ Created sample data file: {filename}")
        return filename
    except Exception as e:
        print(f"× Error creating sample data: {str(e)}")
        return None

# Create sample data file
sample_file = create_sample_data()"""))

    # Upload File and Create Agent
    cells.append(new_markdown_cell("""## Create Health Calculator Agent

Create an agent with code interpreter capabilities:"""))

    cells.append(new_code_cell("""def create_health_calculator(file_path):
    \"\"\"Create an agent with code interpreter for health calculations.\"\"\"
    try:
        # Upload file
        file = project_client.agents.upload_file_and_poll(
            file_path=file_path,
            purpose=FilePurpose.AGENTS
        )
        print(f"✓ Uploaded file, ID: {file.id}")
        
        # Create code interpreter tool
        code_interpreter = CodeInterpreterTool(file_ids=[file.id])
        
        # Create agent
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="health-calculator",
            instructions='''You are a health calculator agent that can:
            1. Calculate and interpret BMI
            2. Analyze nutritional data
            3. Generate health insights
            4. Create visualizations
            Always include appropriate disclaimers and explanations.''',
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"✓ Created health calculator agent, ID: {agent.id}")
        return agent, file
    except Exception as e:
        print(f"× Error creating calculator: {str(e)}")
        return None, None

# Create the agent if sample file was created
if sample_file:
    agent, uploaded_file = create_health_calculator(sample_file)"""))

    # BMI Calculation
    cells.append(new_markdown_cell("""## BMI Calculator Implementation

Implement BMI calculation functionality:"""))

    cells.append(new_code_cell("""def calculate_bmi(thread_id, height_inches, weight_pounds):
    \"\"\"Calculate BMI using the agent.\"\"\"
    try:
        # Create message with BMI calculation request
        message = project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=f'''Calculate BMI for:
            Height: {height_inches} inches
            Weight: {weight_pounds} pounds
            
            Please:
            1. Show the calculation
            2. Interpret the result
            3. Include a health disclaimer'''
        )
        print(f"✓ Created BMI calculation request")
        
        # Process the request
        run = project_client.agents.create_and_process_run(
            thread_id=thread_id,
            assistant_id=agent.id
        )
        print(f"Run status: {run.status}")
        
        return run
    except Exception as e:
        print(f"× Error calculating BMI: {str(e)}")
        return None

# Create thread for BMI calculation
if agent:
    thread = project_client.agents.create_thread()
    print(f"✓ Created thread, ID: {thread.id}")
    
    # Example BMI calculation
    run = calculate_bmi(thread.id, 69, 150)  # 5'9", 150 lbs"""))

    # Nutrition Analysis
    cells.append(new_markdown_cell("""## Nutritional Data Analysis

Analyze the uploaded nutrition data:"""))

    cells.append(new_code_cell("""def analyze_nutrition(thread_id):
    \"\"\"Analyze nutrition data using the agent.\"\"\"
    try:
        # Create message requesting nutrition analysis
        message = project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content='''Please analyze the nutrition data:
            1. Calculate average daily intake
            2. Create a bar chart of macronutrients
            3. Identify trends
            4. Provide recommendations'''
        )
        print(f"✓ Created nutrition analysis request")
        
        # Process the request
        run = project_client.agents.create_and_process_run(
            thread_id=thread_id,
            assistant_id=agent.id
        )
        print(f"Run status: {run.status}")
        
        return run
    except Exception as e:
        print(f"× Error analyzing nutrition: {str(e)}")
        return None

# Create thread for nutrition analysis
if agent:
    nutrition_thread = project_client.agents.create_thread()
    print(f"✓ Created nutrition thread, ID: {nutrition_thread.id}")
    
    # Analyze nutrition data
    nutrition_run = analyze_nutrition(nutrition_thread.id)"""))

    # View Results
    cells.append(new_markdown_cell("""## View Analysis Results

Review the agent's calculations and analysis:"""))

    cells.append(new_code_cell("""def view_results(thread_id):
    \"\"\"View the agent's analysis results.\"\"\"
    try:
        # List messages
        messages = project_client.agents.list_messages(thread_id=thread_id)
        print("\nAnalysis Results:")
        
        # Process text messages
        for message in messages.data:
            if message.role == "assistant":
                for content in message.content:
                    if hasattr(content, "text"):
                        print(f"Analysis: {content.text.value}")
        
        # Save any generated images
        for image_content in messages.image_contents:
            file_id = image_content.image_file.file_id
            file_name = f"{file_id}_analysis.png"
            project_client.agents.save_file(
                file_id=file_id,
                file_name=file_name
            )
            print(f"✓ Saved visualization: {file_name}")
            
    except Exception as e:
        print(f"× Error viewing results: {str(e)}")

# View results if runs were successful
if 'run' in locals() and run:
    print("\nBMI Calculation Results:")
    view_results(thread.id)

if 'nutrition_run' in locals() and nutrition_run:
    print("\nNutrition Analysis Results:")
    view_results(nutrition_thread.id)"""))

    # Cleanup
    cells.append(new_markdown_cell("""## Cleanup

Clean up resources when done:"""))

    cells.append(new_code_cell("""def cleanup_resources():
    \"\"\"Clean up all resources.\"\"\"
    try:
        # Delete uploaded file
        if 'uploaded_file' in locals() and uploaded_file:
            project_client.agents.delete_file(uploaded_file.id)
            print("✓ Deleted uploaded file")
        
        # Delete agent
        if 'agent' in locals() and agent:
            project_client.agents.delete_agent(agent.id)
            print("✓ Deleted health calculator agent")
            
        # Delete sample data file
        if 'sample_file' in locals() and sample_file:
            os.remove(sample_file)
            print("✓ Deleted sample data file")
            
    except Exception as e:
        print(f"× Error during cleanup: {str(e)}")

# Uncomment to clean up resources
# cleanup_resources()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Data Handling**
   - Validate input data
   - Handle missing values
   - Use appropriate data types
   - Implement error checking

2. **Calculations**
   - Show calculation steps
   - Include unit conversions
   - Validate results
   - Provide interpretations

3. **Visualizations**
   - Use clear labels
   - Include legends
   - Choose appropriate charts
   - Add context

4. **Health Advice**
   - Include disclaimers
   - Recommend professional consultation
   - Provide evidence-based information
   - Consider individual factors"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_code_interpreter_tutorial.ipynb"
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
