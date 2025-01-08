import nbformat
import sys
from pathlib import Path

def validate_notebook(notebook_path):
    """Validate a Jupyter notebook's structure and content."""
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Initialize validation results
        results = {
            'has_markdown_cells': False,
            'has_code_cells': False,
            'has_imports': False,
            'has_error_handling': False,
            'cell_count': len(nb.cells)
        }
        
        required_imports = ['azure.identity', 'azure.ai.resources', 'azure.ai.evaluation']
        import_found = set()
        
        # Analyze cells
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                results['has_markdown_cells'] = True
            elif cell.cell_type == 'code':
                results['has_code_cells'] = True
                
                # Check for imports
                if any(f"import {pkg}" in cell.source or f"from {pkg}" in cell.source 
                      for pkg in required_imports):
                    results['has_imports'] = True
                    
                # Check for error handling
                if 'try:' in cell.source and 'except' in cell.source:
                    results['has_error_handling'] = True
        
        # Print validation results
        print(f"\nValidation Results for {notebook_path}:")
        print(f"Total Cells: {results['cell_count']}")
        print(f"Has Markdown Documentation: {'✓' if results['has_markdown_cells'] else '×'}")
        print(f"Has Code Cells: {'✓' if results['has_code_cells'] else '×'}")
        print(f"Has Required Imports: {'✓' if results['has_imports'] else '×'}")
        print(f"Has Error Handling: {'✓' if results['has_error_handling'] else '×'}")
        
        # Overall validation
        is_valid = all(results.values())
        print(f"\nOverall Status: {'✓ Valid' if is_valid else '× Needs Improvement'}")
        
        return is_valid
        
    except Exception as e:
        print(f"Error validating notebook: {str(e)}")
        return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        notebook_path = Path(sys.argv[1])
        if notebook_path.exists():
            validate_notebook(notebook_path)
        else:
            print(f"Error: Notebook not found at {notebook_path}")
    else:
        print("Error: Please provide notebook path as argument")
