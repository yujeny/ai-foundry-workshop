from sqlalchemy import create_engine, Index
import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from database import Base, engine
from models.tables import (
    DrugCandidateTable,
    ClinicalTrialTable,
    AutomatedTestTable,
    PatientCohortTable,
    PatientDataTable
)

def init_database():
    """Initialize the database with all required tables and indexes."""
    print("Creating database tables and indexes...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create indexes for high-throughput screening queries
    Index(
        'idx_drug_candidate_therapeutic',
        DrugCandidateTable.therapeutic_area,
        DrugCandidateTable.predicted_efficacy,
        DrugCandidateTable.predicted_safety
    ).create(bind=engine)
    
    Index(
        'idx_clinical_trial_status',
        ClinicalTrialTable.status,
        ClinicalTrialTable.phase
    ).create(bind=engine)
    
    Index(
        'idx_automated_test_results',
        AutomatedTestTable.drug_candidate_id,
        AutomatedTestTable.result
    ).create(bind=engine)
    
    Index(
        'idx_patient_biomarkers',
        PatientDataTable.cohort_id,
        PatientDataTable.treatment_response
    ).create(bind=engine)
    
    # Initialize sample data for testing
    from sqlalchemy.orm import Session
    from datetime import datetime, timedelta
    from models.clinical_trial import TrialPhase, TrialStatus
    
    with Session(engine) as db:
        # Add sample drug candidate
        drug = DrugCandidateTable(
            id="DRUG-2024-001",
            molecule_type="small_molecule",
            molecular_weight=342.4,
            therapeutic_area="oncology",
            predicted_efficacy=0.85,
            predicted_safety=0.92,
            creation_date=datetime.now(),
            target_proteins=["EGFR", "HER2"],
            side_effects=["mild_headache"],
            development_stage="preclinical",
            ai_confidence=0.89,
            properties={}
        )
        db.add(drug)
        
        # Add sample clinical trial
        trial = ClinicalTrialTable(
            trial_id="CT-2024-001",
            drug_candidate_id="DRUG-2024-001",
            phase=TrialPhase.PHASE_2,
            status=TrialStatus.ACTIVE,
            start_date=datetime.now(),
            estimated_completion_date=datetime.now() + timedelta(days=365),
            participant_count=120,
            target_participant_count=200,
            locations=["Site A", "Site B"],
            primary_endpoint="Overall survival rate",
            secondary_endpoints=["Progression-free survival"],
            inclusion_criteria=["Age > 18", "ECOG status 0-1"],
            exclusion_criteria=["Prior treatment", "Active infection"],
            adverse_events=[],
            interim_analyses=[],
            real_time_metrics={
                "enrollment_rate": 0.85,
                "retention_rate": 0.92,
                "safety_signals": []
            }
        )
        db.add(trial)
        db.commit()
    
    print("Database tables, indexes, and sample data created successfully!")

if __name__ == "__main__":
    init_database()
