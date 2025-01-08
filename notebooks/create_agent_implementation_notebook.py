import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for implementing an AI agent."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Implementing an AI Agent

This notebook guides you through implementing a customer service AI agent using Azure AI Foundry. You'll learn:
1. Setting up the agent environment
2. Implementing core agent functionality
3. Adding specialized capabilities
4. Testing and debugging
5. Best practices for agent implementation

## Prerequisites
- Completed AI Agent Service overview
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

    # Agent Class Definition
    cells.append(new_markdown_cell("""## Customer Service Agent Implementation

Let's implement a customer service agent that can:
1. Handle common customer inquiries
2. Process support tickets
3. Escalate complex issues
4. Maintain conversation context
5. Follow company policies"""))

    cells.append(new_code_cell("""class CustomerServiceAgent:
    def __init__(self, client):
        \"\"\"Initialize the customer service agent.\"\"\"
        self.client = client
        self.conversation_history = []
        self.knowledge_base = {}
        self.policies = {
            "escalation_threshold": 0.7,
            "max_conversation_turns": 10,
            "required_fields": ["customer_id", "issue_type", "description"]
        }
    
    def validate_ticket(self, ticket):
        \"\"\"Validate support ticket fields.\"\"\"
        missing_fields = [
            field for field in self.policies["required_fields"]
            if field not in ticket or not ticket[field]
        ]
        return len(missing_fields) == 0, missing_fields
    
    def process_ticket(self, ticket):
        \"\"\"Process a support ticket.\"\"\"
        try:
            # Validate ticket
            is_valid, missing_fields = self.validate_ticket(ticket)
            if not is_valid:
                return {
                    "status": "invalid",
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }
            
            # Add to conversation history
            self.conversation_history.append({
                "type": "ticket",
                "content": ticket,
                "timestamp": datetime.now().isoformat()
            })
            
            # Process ticket
            response = self.generate_response(ticket)
            
            return {
                "status": "processed",
                "response": response,
                "ticket_id": f"TICKET-{len(self.conversation_history)}"
            }
        except Exception as e:
            print(f"× Error processing ticket: {str(e)}")
            return {
                "status": "error",
                "message": "Error processing ticket"
            }
    
    def generate_response(self, ticket):
        \"\"\"Generate a response using the AI model.\"\"\"
        try:
            # Prepare prompt
            prompt = self._create_prompt(ticket)
            
            # Generate response
            response = self.client.models.generate(
                deployment_name="customer-service-v1",
                prompt=prompt,
                max_tokens=200,
                temperature=0.7
            )
            
            return response
        except Exception as e:
            print(f"× Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request."
    
    def _create_prompt(self, ticket):
        \"\"\"Create a prompt for the AI model.\"\"\"
        try:
            # Basic prompt template
            prompt = f'''You are a helpful customer service agent. 
            Please assist with the following issue:
            
            Customer ID: {ticket.get('customer_id')}
            Issue Type: {ticket.get('issue_type')}
            Description: {ticket.get('description')}
            
            Previous conversation context:
            {self._format_history()}
            
            Please provide a helpful response:'''
            
            return prompt
        except Exception as e:
            print(f"× Error creating prompt: {str(e)}")
            return ""
    
    def _format_history(self):
        \"\"\"Format conversation history for context.\"\"\"
        try:
            formatted_history = []
            for entry in self.conversation_history[-3:]:  # Last 3 interactions
                if entry["type"] == "ticket":
                    formatted_history.append(
                        f"Customer ({entry['timestamp']}): {entry['content']['description']}"
                    )
            return "\\n".join(formatted_history)
        except Exception as e:
            print(f"× Error formatting history: {str(e)}")
            return ""
    
    def needs_escalation(self, ticket, response):
        \"\"\"Determine if the ticket needs escalation.\"\"\"
        try:
            # Check escalation criteria
            criteria = {
                "complex_issue": any(
                    word in ticket["description"].lower()
                    for word in ["urgent", "emergency", "critical"]
                ),
                "multiple_interactions": len(self.conversation_history) > 3,
                "unclear_resolution": len(response) < 50
            }
            
            # Calculate escalation score
            score = sum(criteria.values()) / len(criteria)
            
            return score >= self.policies["escalation_threshold"]
        except Exception as e:
            print(f"× Error checking escalation: {str(e)}")
            return True  # Escalate on error to be safe"""))

    # Initialize Agent
    cells.append(new_markdown_cell("""## Initialize the Agent

Let's create an instance of our customer service agent:"""))

    cells.append(new_code_cell("""def initialize_agent():
    \"\"\"Initialize the customer service agent.\"\"\"
    try:
        # Initialize Azure client
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Create agent
        agent = CustomerServiceAgent(client)
        print("✓ Agent initialized successfully")
        
        return agent
    except Exception as e:
        print(f"× Error initializing agent: {str(e)}")
        return None

# Initialize agent
agent = initialize_agent()"""))

    # Test Agent
    cells.append(new_markdown_cell("""## Test the Agent

Let's test our agent with some sample support tickets:"""))

    cells.append(new_code_cell("""def test_agent():
    \"\"\"Test the customer service agent with sample tickets.\"\"\"
    try:
        # Sample tickets
        test_tickets = [
            {
                "customer_id": "CUST001",
                "issue_type": "login",
                "description": "I can't log into my account. Password reset not working."
            },
            {
                "customer_id": "CUST002",
                "issue_type": "billing",
                "description": "Urgent: Double charged on my last invoice!"
            },
            {
                "customer_id": "CUST003",
                "issue_type": "feature",
                "description": "How do I enable two-factor authentication?"
            }
        ]
        
        # Process tickets
        for ticket in test_tickets:
            print(f"\\nProcessing ticket for {ticket['customer_id']}:")
            print(f"Issue: {ticket['issue_type']}")
            print(f"Description: {ticket['description']}")
            
            # Process ticket
            result = agent.process_ticket(ticket)
            print(f"Status: {result['status']}")
            
            if result['status'] == 'processed':
                print(f"Response: {result['response']}")
                
                # Check escalation
                if agent.needs_escalation(ticket, result['response']):
                    print("⚠ Ticket needs escalation")
            else:
                print(f"Error: {result.get('message', 'Unknown error')}")
            
            print("-" * 50)
        
        return "Testing completed"
    except Exception as e:
        print(f"× Error testing agent: {str(e)}")
        return None

# Test the agent
if agent:
    test_result = test_agent()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Error Handling**
   - Implement comprehensive error handling
   - Log errors appropriately
   - Provide meaningful error messages
   - Have fallback responses

2. **Context Management**
   - Maintain conversation history
   - Use relevant context in responses
   - Clear old context periodically
   - Handle context limits

3. **Response Generation**
   - Use appropriate temperature settings
   - Implement response validation
   - Handle token limits
   - Maintain consistent tone

4. **Security**
   - Validate input data
   - Handle sensitive information
   - Implement rate limiting
   - Follow security policies

5. **Performance**
   - Optimize prompt length
   - Cache common responses
   - Monitor response times
   - Handle concurrent requests"""))

    # Practical Exercise
    cells.append(new_markdown_cell("""## Practical Exercise

Now it's your turn! Try these exercises:

1. **Add New Functionality**
   - Add support for new issue types
   - Implement response templates
   - Add priority handling
   - Enhance escalation logic

2. **Improve Error Handling**
   - Add more validation checks
   - Implement retry logic
   - Add logging
   - Enhance error messages

3. **Enhance Context Management**
   - Implement better history tracking
   - Add context summarization
   - Improve prompt creation
   - Add context cleanup"""))

    cells.append(new_code_cell("""def enhance_agent():
    \"\"\"Enhance the agent with new functionality.\"\"\"
    try:
        # Add new issue type
        new_ticket = {
            "customer_id": "CUST004",
            "issue_type": "technical",
            "description": "Need help configuring API integration",
            "priority": "high"
        }
        
        # Process with enhanced functionality
        result = agent.process_ticket(new_ticket)
        
        print("Enhanced Agent Test:")
        print(f"Ticket Status: {result['status']}")
        if result['status'] == 'processed':
            print(f"Response: {result['response']}")
            print(f"Ticket ID: {result['ticket_id']}")
        
        return "Enhancement completed"
    except Exception as e:
        print(f"× Error enhancing agent: {str(e)}")
        return None

# Try the enhancement
if agent:
    enhancement_result = enhance_agent()"""))

    # Next Steps
    cells.append(new_markdown_cell("""## Next Steps

Now that you've implemented a basic customer service agent, you can:
1. Add more sophisticated features
2. Implement advanced error handling
3. Enhance context management
4. Add monitoring and logging
5. Deploy your agent

Continue to the next notebook to learn about agent design patterns."""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_implementation.ipynb"
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
