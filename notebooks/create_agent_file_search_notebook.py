import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

def create_notebook():
    """Create a Jupyter notebook for searching health and dietary resources."""
    # Create notebooks directory if it doesn't exist
    os.makedirs("building_agent", exist_ok=True)

    # Create a new notebook
    nb = new_notebook()

    # Add cells
    cells = []
    
    # Introduction
    cells.append(new_markdown_cell("""# Health Resource Search Agent Tutorial

This notebook demonstrates how to create an AI agent that can search and retrieve health and dietary information. You'll learn:
1. Setting up a file search agent
2. Creating and managing vector stores
3. Searching health and dietary resources
4. Handling recipe queries

## Prerequisites
- Azure subscription with AI services access
- Python environment with required packages
- Basic understanding of Azure AI concepts
- Sample health and recipe files

## Important Note
Always verify health information with qualified healthcare professionals."""))
    
    # Setup and Imports
    cells.append(new_code_cell("""# Import required libraries
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool
import os

# Initialize client
try:
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )
    print("✓ Successfully initialized AIProjectClient")
except Exception as e:
    print(f"× Error initializing client: {str(e)}")"""))

    # Create Sample Resources
    cells.append(new_markdown_cell("""## Prepare Sample Resources

Create sample health and recipe resources:"""))

    cells.append(new_code_cell("""def create_sample_resources():
    \"\"\"Create sample health and recipe files.\"\"\"
    try:
        # Create sample recipe file
        recipes = '''# Healthy Recipes Database

## Gluten-Free Recipes
1. Quinoa Bowl
   - Ingredients: quinoa, vegetables, olive oil
   - Instructions: Cook quinoa, add vegetables

2. Rice Pasta with Vegetables
   - Ingredients: rice pasta, mixed vegetables
   - Instructions: Boil pasta, sauté vegetables

## Diabetic-Friendly Recipes
1. Low-Carb Stir Fry
   - Ingredients: chicken, vegetables, tamari sauce
   - Instructions: Cook chicken, add vegetables

2. Greek Salad
   - Ingredients: cucumber, tomatoes, feta, olives
   - Instructions: Chop vegetables, combine

## Heart-Healthy Recipes
1. Baked Salmon
   - Ingredients: salmon, lemon, herbs
   - Instructions: Season salmon, bake

2. Mediterranean Bowl
   - Ingredients: chickpeas, vegetables, tahini
   - Instructions: Combine ingredients'''
        
        # Create sample dietary guidelines
        guidelines = '''# Dietary Guidelines

## General Guidelines
- Eat a variety of foods
- Control portion sizes
- Stay hydrated

## Special Diets
1. Gluten-Free Diet
   - Avoid wheat, barley, rye
   - Focus on naturally gluten-free foods

2. Diabetic Diet
   - Monitor carbohydrate intake
   - Choose low glycemic foods

3. Heart-Healthy Diet
   - Limit saturated fats
   - Choose lean proteins'''
        
        # Save files
        with open("recipes.md", "w") as f:
            f.write(recipes)
        with open("guidelines.md", "w") as f:
            f.write(guidelines)
            
        print("✓ Created sample resource files")
        return ["recipes.md", "guidelines.md"]
    except Exception as e:
        print(f"× Error creating resources: {str(e)}")
        return None

# Create sample resources
resource_files = create_sample_resources()"""))

    # Upload Files and Create Vector Store
    cells.append(new_markdown_cell("""## Create Vector Store

Upload files and create a vector store for efficient searching:"""))

    cells.append(new_code_cell("""def setup_vector_store(file_paths):
    \"\"\"Upload files and create vector store.\"\"\"
    try:
        # Upload files
        file_ids = []
        for file_path in file_paths:
            file = project_client.agents.upload_file_and_poll(
                file_path=file_path,
                purpose="assistants"
            )
            file_ids.append(file.id)
            print(f"✓ Uploaded file: {file_path}, ID: {file.id}")
        
        # Create vector store
        vector_store = project_client.agents.create_vector_store_and_poll(
            file_ids=file_ids,
            name="health_resources"
        )
        print(f"✓ Created vector store, ID: {vector_store.id}")
        
        return vector_store, file_ids
    except Exception as e:
        print(f"× Error setting up vector store: {str(e)}")
        return None, None

# Setup vector store if resources were created
if resource_files:
    vector_store, file_ids = setup_vector_store(resource_files)"""))

    # Create Search Agent
    cells.append(new_markdown_cell("""## Create Health Resource Agent

Create an agent with file search capabilities:"""))

    cells.append(new_code_cell("""def create_resource_agent(vector_store_id):
    \"\"\"Create an agent for searching health resources.\"\"\"
    try:
        # Create file search tool
        file_search = FileSearchTool(vector_store_ids=[vector_store_id])
        
        # Create agent
        agent = project_client.agents.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="health-resource-advisor",
            instructions='''You are a health resource advisor that can:
            1. Search and retrieve dietary guidelines
            2. Find recipes for specific dietary needs
            3. Provide evidence-based health information
            4. Answer questions about special diets
            Always include appropriate health disclaimers.''',
            tools=file_search.definitions,
            tool_resources=file_search.resources,
        )
        print(f"✓ Created health resource agent, ID: {agent.id}")
        return agent
    except Exception as e:
        print(f"× Error creating agent: {str(e)}")
        return None

# Create agent if vector store was created
if vector_store:
    agent = create_resource_agent(vector_store.id)"""))

    # Search Examples
    cells.append(new_markdown_cell("""## Search Health Resources

Try different search queries:"""))

    cells.append(new_code_cell("""def search_resources(thread_id, query):
    \"\"\"Search health resources using the agent.\"\"\"
    try:
        # Create message with search query
        message = project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=query
        )
        print(f"✓ Created search query: {query}")
        
        # Process the query
        run = project_client.agents.create_and_process_run(
            thread_id=thread_id,
            assistant_id=agent.id
        )
        print(f"Run status: {run.status}")
        
        return run
    except Exception as e:
        print(f"× Error searching resources: {str(e)}")
        return None

# Create thread for searches
if agent:
    thread = project_client.agents.create_thread()
    print(f"✓ Created thread, ID: {thread.id}")
    
    # Example searches
    queries = [
        "What recipes are suitable for someone with celiac disease?",
        "Show me heart-healthy meal options",
        "What are the guidelines for a diabetic diet?"
    ]
    
    for query in queries:
        print(f"\nSearching: {query}")
        run = search_resources(thread.id, query)"""))

    # View Search Results
    cells.append(new_markdown_cell("""## View Search Results

Review the agent's responses and citations:"""))

    cells.append(new_code_cell("""def view_search_results(thread_id):
    \"\"\"View search results and citations.\"\"\"
    try:
        # List messages
        messages = project_client.agents.list_messages(thread_id=thread_id)
        
        print("\nSearch Results:")
        # Process messages
        for message in messages.data:
            if message.role == "assistant":
                for content in message.content:
                    if hasattr(content, "text"):
                        print(f"\nResponse: {content.text.value}")
        
        # Print citations
        print("\nCitations:")
        for citation in messages.file_citation_annotations:
            print(f"- Cited from: {citation.text}")
            print(f"  File ID: {citation.file_path.file_id}")
            
    except Exception as e:
        print(f"× Error viewing results: {str(e)}")

# View results if searches were performed
if 'thread' in locals() and thread:
    view_search_results(thread.id)"""))

    # Cleanup
    cells.append(new_markdown_cell("""## Cleanup

Clean up resources when done:"""))

    cells.append(new_code_cell("""def cleanup_resources():
    \"\"\"Clean up all resources.\"\"\"
    try:
        # Delete vector store
        if 'vector_store' in locals() and vector_store:
            project_client.agents.delete_vector_store(vector_store.id)
            print("✓ Deleted vector store")
        
        # Delete uploaded files
        if 'file_ids' in locals() and file_ids:
            for file_id in file_ids:
                project_client.agents.delete_file(file_id)
            print("✓ Deleted uploaded files")
        
        # Delete agent
        if 'agent' in locals() and agent:
            project_client.agents.delete_agent(agent.id)
            print("✓ Deleted health resource agent")
            
        # Delete sample files
        if 'resource_files' in locals() and resource_files:
            for file in resource_files:
                os.remove(file)
            print("✓ Deleted sample resource files")
            
    except Exception as e:
        print(f"× Error during cleanup: {str(e)}")

# Uncomment to clean up resources
# cleanup_resources()"""))

    # Best Practices
    cells.append(new_markdown_cell("""## Best Practices

1. **Resource Management**
   - Organize files by topic
   - Use clear file naming
   - Regular vector store updates
   - Clean up unused resources

2. **Search Queries**
   - Be specific in queries
   - Consider variations
   - Handle multiple topics
   - Validate results

3. **Health Information**
   - Include disclaimers
   - Cite sources
   - Verify accuracy
   - Consider context

4. **Vector Store**
   - Monitor store size
   - Regular maintenance
   - Optimize search
   - Backup important data"""))

    # Set notebook cells
    nb['cells'] = cells

    # Write notebook
    notebook_path = "building_agent/agent_file_search_tutorial.ipynb"
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
