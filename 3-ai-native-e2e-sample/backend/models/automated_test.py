from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TestResult(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    IN_PROGRESS = "in_progress"

class AutomatedTest(BaseModel):
    id: str = Field(..., description="Unique identifier for the test")
    drug_id: str = Field(..., description="ID of the drug candidate being tested")
    test_type: str = Field(..., description="Type of automated test performed")
    result: TestResult
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    metrics: dict = Field(default_factory=dict)
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "TEST001",
                "drug_id": "DRUG001",
                "test_type": "toxicity_screening",
                "result": "pass",
                "metrics": {
                    "toxicity_score": 0.12,
                    "confidence": 0.95
                }
            }
        }
