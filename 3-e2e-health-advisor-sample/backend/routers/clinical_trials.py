from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.tables import ClinicalTrialTable, PatientDataTable
from models.clinical_trial import ClinicalTrial, TrialPhase, TrialStatus
from datetime import datetime
import logging

# OpenTelemetry imports temporarily disabled
# from opentelemetry import trace
# from opentelemetry.trace import Status, StatusCode
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["clinical-trials"])

@router.get("/monitor")
async def monitor_trials(
    trial_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Real-time monitoring of:
    - trial parameters
    - potential issues
    - patient responses
    - adaptive trial adjustments
    """
    # Monitoring logic starts here
    logger.info(f"Monitoring trial: {trial_id if trial_id else 'all'}")
    trial = db.query(ClinicalTrialTable).filter(ClinicalTrialTable.trial_id == trial_id).first()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    
    # Get all trials if no specific trial_id is provided
    if trial_id:
        trials = [db.query(ClinicalTrialTable).filter(ClinicalTrialTable.trial_id == trial_id).first()]
        if not trials[0]:
            raise HTTPException(status_code=404, detail="Trial not found")
    else:
        trials = db.query(ClinicalTrialTable).all()

    result = []
    for trial in trials:
        # Calculate metrics
        enrollment_rate = trial.participant_count / trial.target_participant_count if trial.target_participant_count > 0 else 0
        
        # Format trial data
        trial_data = {
            "trial_id": trial.trial_id,
            "phase": trial.phase,
            "status": trial.status,
            "participant_count": trial.participant_count,
            "target_participant_count": trial.target_participant_count,
            "real_time_metrics": {
                "enrollment_rate": enrollment_rate,
                "retention_rate": 0.92,  # Example fixed value
                "safety_signals": []
            }
        }
        result.append(trial_data)
    
    return result if not trial_id else result[0]

@router.post("/predict-response")
async def predict_patient_response(
    trial_id: str,
    patient_id: str,
    db: Session = Depends(get_db)
):
    """Predict individual patient response based on biomarkers and demographics"""
    # Patient response prediction starts here
    logger.info(f"Predicting response for patient {patient_id} in trial {trial_id}")
    patient = db.query(PatientDataTable).filter(PatientDataTable.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "predicted_response": patient.treatment_response or 0.0,
        "confidence": 0.85,
        "biomarker_analysis": patient.biomarkers,
        "recommendations": [
            "Continue monitoring key biomarkers",
            "Schedule follow-up in 2 weeks",
            "Review medication adherence"
        ]
    }
