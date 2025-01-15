import nbformat as nbf
import os

def create_conclusion_notebook():
    """Create a Jupyter notebook for the workshop conclusion."""
    nb = nbf.v4.new_notebook()
    
    # Title and Overview
    nb.cells.append(nbf.v4.new_markdown_cell("""# Workshop Conclusion

Congratulations on completing the Azure AI Foundry Workshop! Let's review what you've learned and explore next steps for your AI development journey.

## Workshop Summary
Throughout this workshop, you've learned how to:
- Set up and authenticate with Azure AI Foundry
- Work with the AI Foundry SDK and AIProjectClient
- Deploy and test AI models
- Build and deploy an intelligent customer service agent
- Monitor and evaluate agent performance"""))

    # Key Takeaways
    nb.cells.append(nbf.v4.new_markdown_cell("""## Key Takeaways

1. **AI Foundry Basics**
   - Project setup and configuration
   - Authentication and security
   - Resource management

2. **Model Management**
   - Model deployment
   - Endpoint configuration
   - Testing and validation

3. **Agent Development**
   - Agent design principles
   - Implementation strategies
   - Testing and deployment

4. **Performance & Monitoring**
   - Evaluation metrics
   - Real-time monitoring
   - Performance optimization"""))

    # Review Exercise
    nb.cells.append(nbf.v4.new_markdown_cell("""## Review Exercise

Let's create a simple function to check your Azure AI Foundry setup and configuration:"""))

    nb.cells.append(nbf.v4.new_code_cell("""import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.evaluation import TextEvaluator
from azure.ai.contentsafety import ContentSafetyClient
import azure.monitor.opentelemetry._autoinstrument

def verify_setup():
    '''Verify Azure AI Foundry setup and configuration'''
    try:
        # Initialize credentials
        credential = DefaultAzureCredential()
        
        # Initialize project client
        project_client = AIProjectClient(
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
            credential=credential
        )
        
        # Check configuration
        config_status = {
            "credentials": "✓ Valid" if credential else "✗ Invalid",
            "project_client": "✓ Initialized" if project_client else "✗ Failed",
            "subscription_id": "✓ Set" if os.getenv("AZURE_SUBSCRIPTION_ID") else "✗ Missing",
            "resource_group": "✓ Set" if os.getenv("AZURE_RESOURCE_GROUP") else "✗ Missing"
        }
        
        print("Azure AI Foundry Configuration Status:")
        for key, value in config_status.items():
            print(f"{key}: {value}")
            
        return all("✓" in value for value in config_status.values())
    
    except Exception as e:
        print(f"Setup verification failed: {str(e)}")
        return False

# Run verification
setup_verified = verify_setup()
print(f"\nOverall Setup Status: {'✓ Ready' if setup_verified else '✗ Needs Attention'}"""))

    # Next Steps
    nb.cells.append(nbf.v4.new_markdown_cell("""## Next Steps

Now that you've completed the workshop, here are some suggested next steps:

1. **Expand Your Agent**
   - Add more capabilities
   - Implement additional use cases
   - Enhance error handling

2. **Optimize Performance**
   - Fine-tune model parameters
   - Implement caching strategies
   - Optimize resource usage

3. **Advanced Features**
   - Implement conversation history
   - Add context awareness
   - Integrate with external systems

4. **Production Deployment**
   - Set up CI/CD pipelines
   - Implement logging and monitoring
   - Configure scaling rules"""))

    # Resources
    nb.cells.append(nbf.v4.new_markdown_cell("""## Additional Resources

- [Azure AI Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [AI Projects SDK Reference](https://learn.microsoft.com/en-us/python/api/azure-ai-projects/)
- [AI Inference SDK Reference](https://learn.microsoft.com/en-us/python/api/azure-ai-inference/)
- [AI Evaluation SDK Reference](https://learn.microsoft.com/en-us/python/api/azure-ai-evaluation/)
- [AI Content Safety SDK Reference](https://learn.microsoft.com/en-us/python/api/azure-ai-contentsafety/)
- [Best Practices Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/best-practices)
- [Sample Projects](https://learn.microsoft.com/en-us/azure/ai-foundry/samples/)

Thank you for participating in this workshop! We hope you found it valuable for your AI development journey."""))

    # Save the notebook
    notebook_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "building_agent", "conclusion.ipynb")
    nbf.write(nb, notebook_path)
    print(f"\nCreated {notebook_path}")
    
    # Validate the notebook
    total_cells = len(nb.cells)
    has_markdown = any(cell.cell_type == "markdown" for cell in nb.cells)
    has_code = any(cell.cell_type == "code" for cell in nb.cells)
    has_imports = any("import" in cell.source for cell in nb.cells if cell.cell_type == "code")
    
    print(f"\nValidation Results for {notebook_path}:")
    print(f"Total Cells: {total_cells}")
    print(f"Has Markdown Documentation: {'✓' if has_markdown else '✗'}")
    print(f"Has Code Cells: {'✓' if has_code else '✗'}")
    print(f"Has Required Imports: {'✓' if has_imports else '✗'}")
    print(f"\nOverall Status: {'✓ Valid' if all([has_markdown, has_code, has_imports]) else '✗ Invalid'}")

if __name__ == "__main__":
    create_conclusion_notebook()
