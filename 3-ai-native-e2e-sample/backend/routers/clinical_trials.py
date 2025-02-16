from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from database_stub import get_storage
from models import ClinicalTrial, TrialPhase, TrialStatus, PatientData
from datetime import datetime
import logging
import os

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

# Import Azure AI Foundry clients from main
from clients import project_client, tracer, chat_client

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["clinical-trials"])

@router.post("/check-eligibility")
async def check_eligibility(
    request: PatientData,
    storage = Depends(get_storage)
):
    """
    Check patient eligibility for clinical trials.
    
    This endpoint provides:
    - 🎯 Eligibility classification
    - 💊 Trial matching
    - 📋 AI-powered analysis
    - ⚠️ Medical disclaimers
    """
    with tracer.start_as_current_span("check_eligibility") as span:
        try:
            span.set_attribute("patient_age", request.age)
            logger.info(f"🔍 Checking eligibility for patient")

            # Get AI explanation first since this can fail
            prompt = f"""Analyze this patient's clinical trial eligibility:
            Age: {request.age}
            Gender: {request.gender}
            Medical Conditions: {request.conditions}
            Current Medications: {request.medications}
            
            Provide a comprehensive analysis including:
            1. Eligibility assessment
            2. Key considerations
            3. Potential risks
            4. Recommendations
            
            Format as a medical eligibility summary, including appropriate disclaimers.
            """
            
            # Get AI explanation first since this can fail
            try:
                response = await chat_client.complete(
                    model=os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4"),
                    messages=[{
                        "role": "system",
                        "content": "You are a medical eligibility assistant. Always include appropriate medical disclaimers."
                    }, {
                        "role": "user",
                        "content": prompt
                    }]
                )
                ai_explanation = response.choices[0].message.content
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                logger.error(f"❌ Error in chat completion: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error in chat completion: {str(e)}"
                )

            # Basic eligibility rules
            is_eligible = True
            if int(request.age) < 18:
                is_eligible = False

            # Get matching trials
            trials = storage.list_items("clinical_trials")
            logger.info(f"Found trials: {trials}")
            matched_trials = []
            if is_eligible:
                matched_trials = [
                    trial["id"] for trial in trials 
                    if trial["status"] == "Recruiting"
                ]
                logger.info(f"Matched trials: {matched_trials}")

            return {
                "classification": {
                    "status": "Likely Eligible" if is_eligible else "Ineligible",
                    "confidence": 0.85,
                    "matched_trials": matched_trials
                },
                "ai_explanation": ai_explanation,
                "disclaimer": "This eligibility check is for educational purposes only. Final eligibility determination must be made by healthcare professionals."
            }
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error in eligibility check: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in eligibility check: {str(e)}"
            )
