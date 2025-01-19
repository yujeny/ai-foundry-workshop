from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class TestResult(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    INCONCLUSIVE = "inconclusive"
    IN_PROGRESS = "in_progress"

class AutomatedTest(BaseModel):
    """Model for automated preclinical testing and high-throughput screening."""
    test_id: str = Field(..., description="Unique identifier for the test")
    drug_candidate_id: str = Field(..., description="Reference to the drug candidate")
    test_type: str = Field(..., description="Type of automated test")
    start_time: datetime = Field(default_factory=datetime.now)
    completion_time: Optional[datetime] = None
    result: TestResult = Field(default=TestResult.IN_PROGRESS)
    parameters: Dict = Field(..., description="Test parameters and conditions")
    measurements: List[Dict] = Field(default_factory=list)
    ai_analysis: Dict = Field(default_factory=dict)
    safety_flags: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "test_id": "TEST-2024-001",
                "drug_candidate_id": "DRUG-2024-001",
                "test_type": "cytotoxicity",
                "start_time": "2024-01-15T10:00:00",
                "result": "passed",
                "parameters": {
                    "concentration": "10uM",
                    "duration": "48h"
                },
                "measurements": [
                    {"timepoint": "24h", "cell_viability": 0.95}
                ],
                "ai_analysis": {
                    "prediction": "low_toxicity",
                    "confidence": 0.88
                }
            }
        }
