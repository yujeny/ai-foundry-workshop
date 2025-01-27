"""
Stub storage implementation using in-memory dictionaries.
Replaces SQLAlchemy-based database.py with a simpler storage solution.
"""
from typing import Dict, List, Optional
from datetime import datetime

# In-memory storage
storage: Dict[str, List[dict]] = {
    "drug_candidates": [],
    "clinical_trials": [],
    "automated_tests": [],
    "patient_cohorts": []
}

class StorageException(Exception):
    """Base exception for storage operations."""
    pass

def add_item(collection: str, item: dict) -> dict:
    """Add an item to a collection."""
    if collection not in storage:
        raise StorageException(f"Collection {collection} does not exist")
    
    # Add creation timestamp and ID if not present
    if "id" not in item:
        item["id"] = str(len(storage[collection]) + 1)
    if "created_at" not in item:
        item["created_at"] = datetime.utcnow().isoformat()
    
    storage[collection].append(item)
    return item

def get_item(collection: str, item_id: str) -> Optional[dict]:
    """Get an item from a collection by ID."""
    if collection not in storage:
        raise StorageException(f"Collection {collection} does not exist")
    
    for item in storage[collection]:
        if item["id"] == item_id:
            return item
    return None

def list_items(collection: str) -> List[dict]:
    """List all items in a collection."""
    if collection not in storage:
        raise StorageException(f"Collection {collection} does not exist")
    return storage[collection]

def update_item(collection: str, item_id: str, updates: dict) -> Optional[dict]:
    """Update an item in a collection."""
    if collection not in storage:
        raise StorageException(f"Collection {collection} does not exist")
    
    for item in storage[collection]:
        if item["id"] == item_id:
            item.update(updates)
            return item
    return None

def delete_item(collection: str, item_id: str) -> bool:
    """Delete an item from a collection."""
    if collection not in storage:
        raise StorageException(f"Collection {collection} does not exist")
    
    initial_length = len(storage[collection])
    storage[collection] = [item for item in storage[collection] if item["id"] != item_id]
    return len(storage[collection]) < initial_length

# Dependency to get storage context (mimics FastAPI dependency injection)
def get_storage():
    """Dependency that provides access to storage operations."""
    return {
        "add_item": add_item,
        "get_item": get_item,
        "list_items": list_items,
        "update_item": update_item,
        "delete_item": delete_item
    }
