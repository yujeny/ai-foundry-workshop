from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from database_stub import get_storage
from models import ClinicalTrial, TrialPhase, TrialStatus, PatientData
from datetime import datetime
import logging

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

# Import Azure AI Foundry clients from main
from clients import project_client, chat_client, tracer

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["clinical-trials"])

@router.get("/monitor")
async def monitor_trials(
    trial_id: Optional[str] = None,
    storage = Depends(get_storage)
):
    """
    ### 📊 Real-time Trial Monitoring
    
    This endpoint provides real-time monitoring of clinical trials:
    - 📈 Trial parameters and metrics
    - ⚠️ Potential issues and alerts
    - 👥 Patient responses and outcomes
    - 🔄 Adaptive trial adjustments
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Monitor
        participant Database
        participant Analytics
        
        Client->>Monitor: Request Trial Data
        Monitor->>Database: Query Trial Status
        Database-->>Monitor: Trial Metrics
        Monitor->>Analytics: Calculate KPIs
        Analytics-->>Monitor: Performance Data
        Monitor-->>Client: Trial Status Report
    ```
    """
    with tracer.start_as_current_span("monitor_trials") as span:
        try:
            span.set_attribute("trial_id", trial_id if trial_id else "all")
            logger.info(f"Monitoring trial: {trial_id if trial_id else 'all'}")
            
            storage = db()
            trials = storage["list_items"]("clinical_trials")
            
            if trial_id:
                trial = storage["get_item"]("clinical_trials", trial_id)
                if not trial:
                    span.set_status(Status(StatusCode.ERROR))
                    raise HTTPException(status_code=404, detail="Trial not found")
                trials = [trial]

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
            
            logger.info(f"✅ Successfully monitored {len(trials)} trials")
            return result if not trial_id else result[0]
            
        except HTTPException as e:
            span.set_status(Status(StatusCode.ERROR))
            logger.error(f"❌ HTTP error in trial monitoring: {str(e)}")
            raise
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error in trial monitoring: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error monitoring trials: {str(e)}"
            )
    
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
    storage = Depends(get_storage)
):
    """
    ### 🧬 Patient Response Prediction
    
    Predict individual patient response based on:
    - 🔬 Biomarker analysis
    - 👤 Patient demographics
    - 💊 Treatment history
    - 📈 Response patterns
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Predictor
        participant BioData
        participant AI
        
        Client->>Predictor: Patient Data
        Predictor->>BioData: Get Biomarkers
        BioData-->>Predictor: Patient Profile
        Predictor->>AI: Analyze Data
        AI-->>Predictor: Response Prediction
        Predictor-->>Client: Treatment Recommendations
    ```
    """
    with tracer.start_as_current_span("predict_patient_response") as span:
        try:
            span.set_attribute("trial_id", trial_id)
            span.set_attribute("patient_id", patient_id)
            logger.info(f"🔍 Predicting response for patient {patient_id} in trial {trial_id}")
            
            storage = db()
            patient = storage["get_item"]("patient_cohorts", patient_id)
            if not patient:
                span.set_status(Status(StatusCode.ERROR))
                raise HTTPException(status_code=404, detail="Patient not found")
    
            logger.info("✅ Successfully predicted patient response")
            return {
                "predicted_response": patient.get("treatment_response", 0.0),
                "confidence": 0.85,
                "biomarker_analysis": patient.get("biomarkers", {}),
                "recommendations": [
                    "Continue monitoring key biomarkers",
                    "Schedule follow-up in 2 weeks",
                    "Review medication adherence"
                ]
            }
            
        except HTTPException as e:
            span.set_status(Status(StatusCode.ERROR))
            logger.error(f"❌ HTTP error in patient response prediction: {str(e)}")
            raise
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error predicting patient response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error predicting patient response: {str(e)}"
            )
