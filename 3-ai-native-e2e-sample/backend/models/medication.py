from pydantic import BaseModel
from typing import Optional, List

class MedicationRequest(BaseModel):
    name: str
    notes: Optional[str] = None
