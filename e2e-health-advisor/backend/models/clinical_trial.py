from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class TrialPhase(str, Enum):
    PRECLINICAL = "preclinical"
    PHASE_1 = "phase_1"
    PHASE_2 = "phase_2"
    PHASE_3 = "phase_3"
    PHASE_4 = "phase_4"

class TrialStatus(str, Enum):
    PLANNED = "planned"
    RECRUITING = "recruiting"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    TERMINATED = "terminated"

class ClinicalTrial(BaseModel):
    """Model for clinical trial management and real-time monitoring."""
    trial_id: str = Field(..., description="Unique identifier for the trial")
    drug_candidate_id: str = Field(..., description="Reference to the drug candidate")
    phase: TrialPhase
    status: TrialStatus
    start_date: datetime
    estimated_completion_date: datetime
    actual_completion_date: Optional[datetime] = None
    participant_count: int = Field(..., ge=0)
    target_participant_count: int = Field(..., ge=0)
    locations: List[str] = Field(default_factory=list)
    primary_endpoint: str
    secondary_endpoints: List[str] = Field(default_factory=list)
    inclusion_criteria: List[str] = Field(default_factory=list)
    exclusion_criteria: List[str] = Field(default_factory=list)
    adverse_events: List[Dict] = Field(default_factory=list)
    interim_analyses: List[Dict] = Field(default_factory=list)
    real_time_metrics: Dict = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "trial_id": "CT-2024-001",
                "drug_candidate_id": "DRUG-2024-001",
                "phase": "phase_2",
                "status": "active",
                "start_date": "2024-01-15T00:00:00",
                "estimated_completion_date": "2025-01-15T00:00:00",
                "participant_count": 120,
                "target_participant_count": 200,
                "locations": ["Site A", "Site B"],
                "primary_endpoint": "Overall survival rate",
                "secondary_endpoints": ["Progression-free survival"],
                "real_time_metrics": {
                    "enrollment_rate": 0.85,
                    "retention_rate": 0.92,
                    "safety_signals": []
                }
            }
        }
