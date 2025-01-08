import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook introducing AI agents in Azure AI Foundry."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Introduction to AI Agents in Azure AI Foundry

This notebook introduces you to AI agents and their capabilities in Azure AI Foundry. You'll learn:
1. What AI agents are
2. Key components of an agent
3. Agent capabilities and limitations
4. Basic agent interactions
5. Best practices for agent design

## Prerequisites
- Completed model deployment and testing
- Azure AI Foundry access
- Required Python packages installed"""))

    # Environment setup
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.resources import AIProjectClient
import os
import json
from datetime import datetime

# Check environment variables
required_vars = {
    "AZURE_SUBSCRIPTION_ID": os.getenv("AZURE_SUBSCRIPTION_ID"),
    "AZURE_RESOURCE_GROUP": os.getenv("AZURE_RESOURCE_GROUP")
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    print("× Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
else:
    print("✓ All required environment variables are set")"""))

    # What are AI Agents
    cells.append(new_markdown_cell("""## What are AI Agents?

AI agents are autonomous software entities that can:
1. Perceive their environment
2. Make decisions
3. Take actions
4. Learn from experience

Key characteristics:
- Autonomy
- Goal-oriented behavior
- Adaptability
- Interaction capabilities

In Azure AI Foundry, agents are built on top of foundation models and can be:
- Specialized for specific tasks
- Integrated with various services
- Monitored and evaluated
- Deployed at scale"""))

    # Agent Components
    cells.append(new_code_cell("""def explore_agent_components():
    \"\"\"Demonstrate the key components of an AI agent.\"\"\"
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Example agent configuration
        agent_config = {
            "components": {
                "language_model": {
                    "type": "gpt-35-turbo",
                    "role": "core_reasoning"
                },
                "memory": {
                    "type": "conversation_buffer",
                    "capacity": 10
                },
                "tools": [
                    {
                        "name": "search",
                        "type": "web_search",
                        "config": {"max_results": 3}
                    },
                    {
                        "name": "calculator",
                        "type": "basic_math",
                        "config": {}
                    }
                ],
                "capabilities": [
                    "conversation",
                    "task_planning",
                    "information_retrieval"
                ]
            }
        }
        
        print("Agent Components:")
        print(json.dumps(agent_config, indent=2))
        
        return agent_config
    except Exception as e:
        print(f"× Error exploring agent components: {str(e)}")
        return None

# Explore agent components
agent_components = explore_agent_components()"""))

    # Agent Capabilities
    cells.append(new_markdown_cell("""## Agent Capabilities

AI agents in Azure AI Foundry can:

1. **Process Natural Language**
   - Understand user queries
   - Generate human-like responses
   - Maintain context in conversations

2. **Use Tools and APIs**
   - Access external services
   - Perform calculations
   - Search for information

3. **Learn and Adapt**
   - Improve from feedback
   - Adjust to user preferences
   - Learn new patterns

4. **Make Decisions**
   - Evaluate options
   - Follow business rules
   - Handle uncertainty

5. **Manage State**
   - Track conversations
   - Remember context
   - Maintain history"""))

    # Basic Agent Interaction
    cells.append(new_code_cell("""def demonstrate_agent_interaction():
    \"\"\"Demonstrate basic interaction with an AI agent.\"\"\"
    try:
        # Initialize client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Example conversation
        conversation = [
            {
                "role": "user",
                "content": "I need help with a customer service issue."
            },
            {
                "role": "agent",
                "content": "I'll be happy to help. Could you please describe the issue?"
            },
            {
                "role": "user",
                "content": "My subscription was charged twice this month."
            }
        ]
        
        # Process conversation
        def process_interaction(message):
            \"\"\"Process a single interaction with the agent.\"\"\"
            try:
                # Add message to conversation
                conversation.append({
                    "role": "user",
                    "content": message
                })
                
                # Get agent response
                response = client.agents.generate_response(
                    agent_name="customer-service-agent",
                    conversation=conversation,
                    max_tokens=150
                )
                
                # Add response to conversation
                conversation.append({
                    "role": "agent",
                    "content": response
                })
                
                return response
            except Exception as e:
                return f"Error processing interaction: {str(e)}"
        
        # Example interactions
        test_messages = [
            "Can you help me understand why I was charged twice?",
            "How can I get a refund?",
            "Thank you for your help."
        ]
        
        print("Agent Interaction Demo:\\n")
        for message in test_messages:
            print(f"User: {message}")
            response = process_interaction(message)
            print(f"Agent: {response}\\n")
            
        return conversation
    except Exception as e:
        print(f"× Error demonstrating agent interaction: {str(e)}")
        return None

# Demonstrate agent interaction
conversation_history = demonstrate_agent_interaction()"""))

    # Agent Limitations
    cells.append(new_markdown_cell("""## Agent Limitations

Important considerations when working with AI agents:

1. **Knowledge Limitations**
   - Based on training data
   - May not have real-time information
   - Can't access private data without configuration

2. **Reasoning Constraints**
   - May not understand complex context
   - Limited by model capabilities
   - Needs clear instructions

3. **Technical Boundaries**
   - API rate limits
   - Token limitations
   - Resource constraints

4. **Security Considerations**
   - Access control needed
   - Data privacy concerns
   - Authentication requirements"""))

    # Best Practices
    cells.append(new_code_cell("""def demonstrate_best_practices():
    \"\"\"Demonstrate best practices for working with AI agents.\"\"\"
    try:
        # Example best practices implementation
        best_practices = {
            "agent_design": {
                "clear_purpose": "Define specific agent goals and scope",
                "modular_components": "Break down functionality into reusable parts",
                "error_handling": "Implement robust error handling",
                "logging": "Enable comprehensive logging for monitoring"
            },
            "interaction_patterns": {
                "clear_instructions": "Provide explicit instructions to the agent",
                "context_management": "Maintain relevant conversation context",
                "feedback_loop": "Implement mechanism for continuous improvement",
                "fallback_handling": "Define behavior for edge cases"
            },
            "security_measures": {
                "authentication": "Implement proper authentication",
                "authorization": "Define clear access controls",
                "data_protection": "Ensure sensitive data handling",
                "audit_logging": "Track all agent actions"
            },
            "monitoring": {
                "performance_metrics": "Track response times and quality",
                "usage_patterns": "Monitor interaction patterns",
                "error_rates": "Track and analyze failures",
                "user_satisfaction": "Collect and analyze feedback"
            }
        }
        
        print("Best Practices for AI Agents:")
        print(json.dumps(best_practices, indent=2))
        
        return best_practices
    except Exception as e:
        print(f"× Error demonstrating best practices: {str(e)}")
        return None

# Demonstrate best practices
agent_best_practices = demonstrate_best_practices()"""))

    # Practical Exercise
    cells.append(new_markdown_cell("""## Practical Exercise

Now that you understand the basics of AI agents, try these exercises:

1. **Design an Agent**
   - Define its purpose
   - List required capabilities
   - Identify necessary tools
   - Plan interaction patterns

2. **Configure Components**
   - Select appropriate model
   - Define memory requirements
   - Choose necessary tools
   - Set up skills

3. **Test Interactions**
   - Write test conversations
   - Verify responses
   - Check error handling
   - Evaluate performance"""))

    cells.append(new_code_cell("""def complete_practical_exercise():
    \"\"\"Complete the practical exercise for agent design.\"\"\"
    try:
        # Your agent design
        my_agent_design = {
            "purpose": "Customer service support",
            "capabilities": [
                "Answer product questions",
                "Handle billing inquiries",
                "Process refund requests",
                "Escalate complex issues"
            ],
            "tools": [
                "Knowledge base search",
                "Order lookup",
                "Payment processing",
                "Ticket creation"
            ],
            "interaction_patterns": [
                "Greeting and identification",
                "Issue classification",
                "Resolution steps",
                "Satisfaction confirmation"
            ]
        }
        
        # Your component configuration
        my_agent_config = {
            "model": {
                "name": "gpt-35-turbo",
                "temperature": 0.7,
                "max_tokens": 150
            },
            "memory": {
                "type": "conversation_buffer",
                "max_turns": 10
            },
            "tools": [
                {
                    "name": "kb_search",
                    "type": "vector_search",
                    "config": {"index_name": "customer_support"}
                },
                {
                    "name": "order_lookup",
                    "type": "api_call",
                    "config": {"endpoint": "orders/search"}
                }
            ]
        }
        
        print("Agent Design:")
        print(json.dumps(my_agent_design, indent=2))
        print("\\nComponent Configuration:")
        print(json.dumps(my_agent_config, indent=2))
        
        return my_agent_design, my_agent_config
    except Exception as e:
        print(f"× Error in practical exercise: {str(e)}")
        return None, None

# Complete the exercise
agent_design, agent_config = complete_practical_exercise()"""))

    # Next Steps
    cells.append(new_markdown_cell("""## Next Steps

Now that you understand AI agents, you can:
1. Explore the AI Agent Service
2. Build your first agent
3. Deploy and test agents
4. Monitor agent performance

Continue to the next notebook to learn about the Azure AI Agent Service."""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_introduction.ipynb"
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
