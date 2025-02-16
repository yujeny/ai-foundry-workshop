"""
Stub storage implementation using in-memory dictionaries.
Replaces SQLAlchemy-based database.py with a simpler storage solution.
"""
from typing import Dict, List, Optional
from datetime import datetime

class StorageException(Exception):
    """Base exception for storage operations."""
    pass

class Storage:
    """Storage class that provides both attribute and dict-style access."""
    def __init__(self):
        self._storage: Dict[str, List[dict]] = {
            "drug_candidates": [],
            "clinical_trials": [],
            "automated_tests": [],
            "patient_cohorts": [],
            "medication_analyses": []
        }
    
    def add_item(self, collection: str, item: dict) -> dict:
        """Add an item to a collection."""
        if collection not in self._storage:
            raise StorageException(f"Collection {collection} does not exist")
        
        # Add creation timestamp and ID if not present
        if "id" not in item:
            item["id"] = str(len(self._storage[collection]) + 1)
        if "created_at" not in item:
            item["created_at"] = datetime.utcnow().isoformat()
        
        self._storage[collection].append(item)
        return item

    def get_item(self, collection: str, item_id: str) -> Optional[dict]:
        """Get an item from a collection by ID."""
        if collection not in self._storage:
            raise StorageException(f"Collection {collection} does not exist")
        
        for item in self._storage[collection]:
            if item["id"] == item_id:
                return item
        return None

    def list_items(self, collection: str) -> List[dict]:
        """List all items in a collection."""
        if collection not in self._storage:
            raise StorageException(f"Collection {collection} does not exist")
        return self._storage[collection]

    def update_item(self, collection: str, item_id: str, updates: dict) -> Optional[dict]:
        """Update an item in a collection."""
        if collection not in self._storage:
            raise StorageException(f"Collection {collection} does not exist")
        
        for item in self._storage[collection]:
            if item["id"] == item_id:
                item.update(updates)
                return item
        return None

    def delete_item(self, collection: str, item_id: str) -> bool:
        """Delete an item from a collection."""
        if collection not in self._storage:
            raise StorageException(f"Collection {collection} does not exist")
        
        initial_length = len(self._storage[collection])
        self._storage[collection] = [item for item in self._storage[collection] if item["id"] != item_id]
        return len(self._storage[collection]) < initial_length

    def __getitem__(self, key):
        """Support dict-style access."""
        return getattr(self, key)

# Global storage instance
_storage = Storage()

# Dependency to get storage context (mimics FastAPI dependency injection)
def get_storage():
    """Dependency that provides access to storage operations."""
    from tests.mock_clients import MockStorage
    return MockStorage()
