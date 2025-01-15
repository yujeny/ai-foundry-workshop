import nbformat as nbf

# Create a new notebook
nb = nbf.v4.new_notebook()

# Create markdown cell content
text = '''# Test Notebook
This is a test notebook to verify the Jupyter environment.

## Testing Azure Packages
```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.evaluation import EvaluationClient

print('Azure packages imported successfully!')
```
'''

# Add markdown cell to notebook
nb['cells'] = [nbf.v4.new_markdown_cell(text)]

# Write the notebook to file
nbf.write(nb, 'test.ipynb')
print("Test notebook created successfully!")
