#!/usr/bin/env python
# coding: utf-8

# # Basic Health Advisor Agent Tutorial
# 
# This notebook demonstrates how to create a basic health advisor agent using Azure AI Foundry. You'll learn:
# 1. Setting up a health advisor agent with proper medical disclaimers
# 2. Managing health-related conversations safely
# 3. Handling fitness and wellness queries
# 4. Implementing safety measures and professional referrals
# 
# ## Prerequisites
# - Azure subscription with AI services access
# - Python environment with required packages
# - Basic understanding of Azure AI concepts
# 
# ## Important Medical Disclaimer
# The health information provided by this agent is for general educational purposes only and is not intended as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or received from this agent.
# 
# ## Professional Consultation
# - Always consult healthcare professionals for medical advice
# - This agent provides general wellness information only
# - For specific medical conditions, consult your doctor
# - In case of emergency, contact emergency services immediately

# In[ ]:


# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageTextContent
import os
from dotenv import load_dotenv
import time
from pathlib import Path

# Load environment variables from parent directory's .env file
notebook_path = Path().absolute()  # Gets current working directory
parent_dir = notebook_path.parent
load_dotenv(parent_dir / '.env')

# Initialize client
try:
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.getenv("PROJECT_CONNECTION_STRING"),
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")


# ## Creating a Health Advisor Agent
# 
# Let's create an agent specialized in providing health and dietary advice:

# In[ ]:


def create_health_advisor():
    """Create a health advisor agent with appropriate instructions."""
    try:
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="health-advisor",
            instructions='''You are a knowledgeable health advisor focused on wellness and fitness. Important guidelines:
                        1. Always begin responses with appropriate medical disclaimers
                        2. Explicitly recommend consulting healthcare professionals for medical advice
                        3. Be specific about health conditions, allergies, and restrictions
                        4. Provide evidence-based nutritional and fitness guidance
                        5. Clearly explain health metrics (BMI, heart rate zones, etc.)
                        6. Emphasize the importance of professional medical consultation
                        7. Never provide specific medical diagnoses or treatment plans
                        8. Focus on general wellness, fitness, and healthy lifestyle choices
                        
                        Example responses should include:
                        Important Medical Disclaimer: This information is for educational purposes only.
                        Please consult your healthcare provider before starting any diet or exercise program.
                        
                        For BMI-related queries:
                        1. BMI Formula: weight(kg) / height(m)²
                        2. Categories: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (>30)
                        3. Important: BMI is just one metric and should be evaluated by healthcare professionals
                        
                        For all advice:
                        - Consult with healthcare professionals for personalized guidance
                        - Follow evidence-based nutritional and fitness guidelines
                        - Consider individual health conditions and restrictions'''
        )
        print(f"✓ Created health advisor agent, ID: {agent.id}")
        return agent
    except Exception as e:
        print(f"× Error creating agent: {str(e)}")
        return None

# Create the agent
agent = create_health_advisor()

# ## Example Health Queries
#                 
# The following examples demonstrate proper health and fitness guidance with appropriate disclaimers:
# 1. BMI Calculation and Interpretation
# 2. Nutritional Guidance for Active Lifestyle
# 3. Heart Rate Zone Training
#                 

# In[ ]:


# The following examples demonstrate proper health and fitness guidance:

# 1. BMI Calculation and Interpretation
# Example query: "How do I calculate my BMI and what does it mean for my fitness goals?"
# Response includes:
# - Medical disclaimer
# - BMI formula and categories
# - Professional consultation recommendation
# - Individual factors consideration

# 2. Nutritional Guidance for Active Lifestyle
# Example query: "What's a balanced meal plan for someone who exercises regularly?"
# Response includes:
# - Dietary disclaimer
# - Balanced nutrition principles
# - Pre/post workout considerations
# - Professional nutritionist consultation

# 3. Heart Rate Zone Training
# Example query: "How do I calculate my target heart rate zones for cardio?"
# Response includes:
# - Exercise safety disclaimer
# - Heart rate zone calculations
# - Individual fitness level considerations
# - Healthcare provider consultation

# ## Managing Conversations
# 
# Create a thread for health-related conversations:

# In[ ]:


def start_health_conversation():
    """Create a thread for health-related discussions."""
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
thread, message = start_health_conversation()


# ## Processing Health Queries
# 
# Process the health-related query and get agent's response:

# In[ ]:


def process_health_query(thread_id, assistant_id):
    """Process a health query and get agent's response."""
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
    run = process_health_query(thread.id, agent.id)


# ## Viewing Health Advice Responses
# 
# Review the agent's health advice responses:

# In[ ]:


def view_health_advice(thread_id):
    """View health advice responses in the conversation."""
    try:
        # List messages
        messages = project_client.agents.list_messages(thread_id=thread_id)
        
        print("Conversation History:")
        for data_point in reversed(messages.data):
            last_message_content = data_point.content[-1]
            if isinstance(last_message_content, MessageTextContent):
                print(f"{data_point.role}: {last_message_content.text.value}")
                
    except Exception as e:
        print(f"× Error viewing advice: {str(e)}")

# View the conversation if thread was created
if thread:
    view_health_advice(thread.id)


# ## Cleanup
# 
# Clean up resources when done:

# In[ ]:


def cleanup_resources():
    """Clean up the agent when done."""
    try:
        if agent:
            project_client.agents.delete_agent(agent.id)
            print("✓ Deleted health advisor agent")
    except Exception as e:
        print(f"× Error during cleanup: {str(e)}")

# Uncomment to clean up resources
# cleanup_resources()


# ## Best Practices
# 
# 1. **Health Advice Guidelines**
#    - Always include medical disclaimers
#    - Recommend professional consultation
#    - Be specific about restrictions
#    - Provide evidence-based information
# 
# 2. **Conversation Management**
#    - Handle sensitive topics appropriately
#    - Maintain context in conversations
#    - Implement proper error handling
#    - Monitor agent responses
# 
# 3. **Resource Management**
#    - Clean up unused resources
#    - Monitor usage and quotas
#    - Implement proper logging
#    - Regular performance reviews
