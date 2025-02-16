from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PatientData(BaseModel):
    age: str
    gender: str
    conditions: str = Field(default="None")
    medications: str = Field(default="None")

class PatientCohort(BaseModel):
    id: str = Field(..., description="Unique identifier for the cohort")
    trial_id: str = Field(..., description="Associated clinical trial ID")
    patients: List[PatientData]
    creation_date: datetime = Field(default_factory=datetime.now)
    target_size: int
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "COHORT001",
                "trial_id": "CT001",
                "target_size": 100,
                "inclusion_criteria": ["Age > 18", "No prior treatment"],
                "exclusion_criteria": ["Pregnancy", "Heart conditions"],
                "patients": [
                    {
                        "patient_id": "P001",
                        "age": 45,
                        "gender": "F",
                        "medical_history": ["hypertension"],
                        "current_medications": ["lisinopril"],
                        "biomarkers": {"blood_pressure": "120/80"}
                    }
                ]
            }
        }
