from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class PatientData(BaseModel):
    """Model for individual patient data in a trial."""
    patient_id: str = Field(..., description="Unique identifier for the patient")
    enrollment_date: datetime
    demographics: Dict = Field(..., description="Patient demographic information")
    genetic_markers: List[str] = Field(default_factory=list)
    biomarkers: Dict = Field(default_factory=dict)
    adverse_events: List[Dict] = Field(default_factory=list)
    treatment_response: Optional[float] = None
    withdrawal_date: Optional[datetime] = None
    withdrawal_reason: Optional[str] = None

class PatientCohort(BaseModel):
    """Model for managing patient cohorts in personalized medicine trials."""
    cohort_id: str = Field(..., description="Unique identifier for the cohort")
    trial_id: str = Field(..., description="Reference to the clinical trial")
    creation_date: datetime = Field(default_factory=datetime.now)
    stratification_factors: List[str] = Field(default_factory=list)
    inclusion_criteria: List[str] = Field(default_factory=list)
    patients: List[PatientData] = Field(default_factory=list)
    biomarker_analysis: Dict = Field(default_factory=dict)
    efficacy_metrics: Dict = Field(default_factory=dict)
    safety_metrics: Dict = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "cohort_id": "COHORT-2024-001",
                "trial_id": "CT-2024-001",
                "stratification_factors": ["biomarker_status", "prior_treatment"],
                "inclusion_criteria": ["EGFR mutation positive"],
                "biomarker_analysis": {
                    "response_rate": 0.75,
                    "biomarker_correlation": 0.82
                }
            }
        }
