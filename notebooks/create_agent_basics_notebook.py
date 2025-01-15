import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for basic health advisor agent operations."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Basic Health Advisor Agent Tutorial

This notebook demonstrates how to create a basic health advisor agent using Azure AI Foundry. You'll learn:
1. Setting up a health advisor agent
2. Managing agent conversations
3. Handling health-related queries
4. Implementing safety measures

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts

## Important Note
Always include appropriate medical disclaimers and recommend consulting healthcare professionals for medical advice."""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageTextContent
import os
import time

# Initialize client
try:
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Create Health Advisor Agent
    cells.append(new_markdown_cell("""## Creating a Health Advisor Agent

Let's create an agent specialized in providing health and dietary advice:"""))

    cells.append(new_code_cell("""def create_health_advisor():
    \"\"\"Create a health advisor agent with appropriate instructions.\"\"\"
    try:
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="health-advisor",
            instructions='''You are a knowledgeable health advisor. Important guidelines:
            1. Always include appropriate health disclaimers
            2. Recommend consulting healthcare professionals for medical advice
            3. Be specific about food allergies and restrictions
            4. Provide evidence-based nutritional guidance
            5. Clearly explain BMI calculations and interpretations'''
        )
        print(f"✓ Created health advisor agent, ID: {agent.id}")
        return agent
    except Exception as e:
        print(f"× Error creating agent: {str(e)}")
        return None

# Create the agent
agent = create_health_advisor()"""))

    # Create Conversation Thread
    cells.append(new_markdown_cell("""## Managing Conversations

Create a thread for health-related conversations:"""))

    cells.append(new_code_cell("""def start_health_conversation():
    \"\"\"Create a thread for health-related discussions.\"\"\"
    try:
        # Create thread
        thread = project_client.agents.create_thread()
        print(f"✓ Created conversation thread, ID: {thread.id}")
        
        # Example health query
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content="What are some healthy breakfast options for someone with diabetes?"
        )
        print(f"✓ Created message, ID: {message.id}")
        
        return thread, message
    except Exception as e:
        print(f"× Error starting conversation: {str(e)}")
        return None, None

# Start a conversation
thread, message = start_health_conversation()"""))

    # Process Health Query
    cells.append(new_markdown_cell("""## Processing Health Queries

Process the health-related query and get agent's response:"""))

    cells.append(new_code_cell("""def process_health_query(thread_id, assistant_id):
    \"\"\"Process a health query and get agent's response.\"\"\"
    try:
        # Create and process run
        run = project_client.agents.create_run(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        # Poll the run status
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = project_client.agents.get_run(
                thread_id=thread_id,
                run_id=run.id
            )
            print(f"Run status: {run.status}")
        
        return run
    except Exception as e:
        print(f"× Error processing query: {str(e)}")
        return None

# Process the query if thread and agent were created successfully
if thread and agent:
    run = process_health_query(thread.id, agent.id)"""))

    # View Responses
    cells.append(new_markdown_cell("""## Viewing Health Advice Responses

Review the agent's health advice responses:"""))

    cells.append(new_code_cell("""def view_health_advice(thread_id):
    \"\"\"View health advice responses in the conversation.\"\"\"
    try:
        # List messages
        messages = project_client.agents.list_messages(thread_id=thread_id)
        
        print("\nConversation History:")
        for data_point in reversed(messages.data):
            last_message_content = data_point.content[-1]
            if isinstance(last_message_content, MessageTextContent):
                print(f"{data_point.role}: {last_message_content.text.value}")
                
    except Exception as e:
        print(f"× Error viewing advice: {str(e)}")

# View the conversation if thread was created
if thread:
    view_health_advice(thread.id)"""))

    # Cleanup
    cells.append(new_markdown_cell("""## Cleanup

Clean up resources when done:"""))

    cells.append(new_code_cell("""def cleanup_resources():
    \"\"\"Clean up the agent when done.\"\"\"
    try:
        if agent:
            project_client.agents.delete_agent(agent.id)
            print("✓ Deleted health advisor agent")
    except Exception as e:
        print(f"× Error during cleanup: {str(e)}")

# Uncomment to clean up resources
# cleanup_resources()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Health Advice Guidelines**
   - Always include medical disclaimers
   - Recommend professional consultation
   - Be specific about restrictions
   - Provide evidence-based information

2. **Conversation Management**
   - Handle sensitive topics appropriately
   - Maintain context in conversations
   - Implement proper error handling
   - Monitor agent responses

3. **Resource Management**
   - Clean up unused resources
   - Monitor usage and quotas
   - Implement proper logging
   - Regular performance reviews"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_basics_tutorial.ipynb"
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
