import os
import sys
import nbformat
from pathlib import Path

def validate_notebooks():
    """Validate all notebooks in the building_agent directory."""
    print("=== Testing Notebook Environment ===")
    
    # Check building_agent directory exists
    building_agent_dir = Path("building_agent")
    if not building_agent_dir.exists():
        print("❌ building_agent directory not found")
        return False
        
    # Validate all notebooks
    notebooks = list(building_agent_dir.glob("*.ipynb"))
    if not notebooks:
        print("❌ No notebooks found in building_agent directory")
        return False
        
    print(f"\nFound {len(notebooks)} notebooks:")
    for nb_path in notebooks:
        print(f"- {nb_path.name}")
        
    # Validate notebook format
    print("\n=== Validating Notebook Format ===")
    for nb_path in notebooks:
        try:
            nb = nbformat.read(nb_path, as_version=4)
            print(f"✓ {nb_path.name}: Valid format")
        except Exception as e:
            print(f"❌ {nb_path.name}: Invalid format - {str(e)}")
            return False
    
    print("\n=== All Verification Steps Complete ===")
    print("✓ All notebooks validated successfully")
    return True

if __name__ == "__main__":
    success = validate_notebooks()
    sys.exit(0 if success else 1)
