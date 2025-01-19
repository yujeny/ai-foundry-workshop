from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MoleculeType(str, Enum):
    SMALL_MOLECULE = "small_molecule"
    BIOLOGIC = "biologic"
    PEPTIDE = "peptide"
    ANTIBODY = "antibody"

class DrugCandidate(BaseModel):
    """Model for AI-generated drug candidates and molecular designs."""
    id: str = Field(..., description="Unique identifier for the drug candidate")
    molecule_type: MoleculeType
    molecular_weight: float = Field(..., description="Molecular weight in g/mol")
    therapeutic_area: str = Field(..., description="Target therapeutic area")
    predicted_efficacy: float = Field(..., ge=0, le=1, description="AI-predicted efficacy score")
    predicted_safety: float = Field(..., ge=0, le=1, description="AI-predicted safety score")
    creation_date: datetime = Field(default_factory=datetime.now)
    target_proteins: List[str] = Field(default_factory=list)
    side_effects: List[str] = Field(default_factory=list)
    development_stage: str = Field(..., description="Current development stage")
    ai_confidence: float = Field(..., ge=0, le=1, description="AI confidence in predictions")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "DRUG-2024-001",
                "molecule_type": "small_molecule",
                "molecular_weight": 342.4,
                "therapeutic_area": "oncology",
                "predicted_efficacy": 0.85,
                "predicted_safety": 0.92,
                "target_proteins": ["EGFR", "HER2"],
                "side_effects": ["mild_headache"],
                "development_stage": "preclinical",
                "ai_confidence": 0.89
            }
        }
