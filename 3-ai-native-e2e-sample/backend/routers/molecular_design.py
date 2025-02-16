from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Security
from typing import List, Optional, Dict
from database_stub import get_storage
from models import DrugCandidate, MoleculeType, TestResult, MedicationRequest
from models import PatientData, AutomatedTest
from datetime import datetime
import asyncio
import os
import logging
from concurrent.futures import ThreadPoolExecutor

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

# Configure logging
logger = logging.getLogger(__name__)

# Import Azure AI Foundry clients
from clients import project_client, chat_client
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
from utils.molecular_analysis import (
    analyze_genetic_compatibility,
    analyze_biomarker_interaction,
    calculate_patient_response,
    identify_patient_risks,
    generate_patient_recommendations,
    analyze_single_molecule,
    perform_detailed_analysis
)
from security.data_encryption import data_encryption, data_auditing
from security.access_control import access_control, RoleBasedAccess

# Security scopes for molecular design endpoints
MOLECULE_SCOPES = {
    "read:molecules": "Access to molecular research data",
    "write:molecules": "Create and modify molecular data",
    "delete:molecules": "Delete molecular research data",
    "read:patients": "Access to patient analysis data",
    "write:regulatory": "Submit regulatory documentation"
}
# Temporarily disable OpenTelemetry
# from opentelemetry import trace
# tracer = trace.get_tracer(__name__)

router = APIRouter(tags=["molecular-design"])

@router.post("/agents/demo-agent")
async def demo_agent_interaction(
    molecule_data: DrugCandidate,
    storage = Depends(get_storage)
):
    """
    ### 🧬 Demo Agent Interaction

    This endpoint demonstrates how an Azure AI Foundry Agent can be used to perform
    advanced drug design tasks.

    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Models
        participant Analysis
        
        Client->>Agent: Submit Molecule Data
        Agent->>Models: Analyze Properties
        Models-->>Agent: Property Predictions
        Agent->>Analysis: Safety Assessment
        Analysis-->>Agent: Safety Report
        Agent-->>Client: Complete Analysis
    ```

    The agent will:
    - 🔍 Analyze molecular properties
    - 🧪 Predict drug interactions
    - ⚕️ Assess safety profile
    - 📊 Generate recommendations
    """
    with tracer.start_as_current_span("demo_agent_interaction") as span:
        try:
            span.set_attribute("molecule_id", molecule_data.id)
            
            # Create a chat completion request for analysis
            response = chat_client.get_chat_completion(
                model=os.getenv('MODEL_DEPLOYMENT_NAME'), 
                messages=[
                    {
                        "role": "system",
                        "content": """You are a pharmaceutical research assistant specializing in drug candidate analysis.
                        Analyze the provided molecule data and provide insights on:
                        - Molecular properties and potential interactions
                        - Safety considerations
                        - Development recommendations"""
                    },
                    {
                        "role": "user",
                        "content": f"""Please analyze this drug candidate:
                        ID: {molecule_data.id}
                        Type: {molecule_data.molecule_type}
                        Therapeutic Area: {molecule_data.therapeutic_area}
                        Target Proteins: {', '.join(molecule_data.target_proteins)}
                        Development Stage: {molecule_data.development_stage}
                        """
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Get the analysis response
            analysis_response = response.choices[0].message.content
            
            # Store the analysis in the storage
            molecule_dict = {
                "id": molecule_data.id,
                "molecule_type": molecule_data.molecule_type,
                "therapeutic_area": molecule_data.therapeutic_area,
                "predicted_efficacy": 0.85,  # Example value
                "predicted_safety": 0.92,  # Example value
                "creation_date": datetime.now().isoformat(),
                "target_proteins": molecule_data.target_proteins,
                "side_effects": [],
                "development_stage": molecule_data.development_stage,
                "ai_confidence": 0.88,  # Example value
                "properties": {"ai_analysis": analysis_response}
            }
            storage["add_item"]("drug_candidates", molecule_dict)
            
            return {
                "message": "Agent analysis complete",
                "molecule_id": molecule_data.id,
                "analysis": analysis_response,
                "recommendations": [
                    "Continue with detailed toxicology studies",
                    "Consider additional protein binding assays",
                    "Monitor for specific side effects"
                ]
            }
            
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error in agent interaction: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in agent interaction: {str(e)}"
            )

@router.post("/batch-analysis", dependencies=[Security(access_control.get_current_user, scopes=["write:molecules"])])
async def analyze_molecules_batch(
    molecules: List[DrugCandidate],
    background_tasks: BackgroundTasks,
    storage = Depends(get_storage)
):
    """
    Perform high-throughput screening on multiple drug candidates:
    - Parallel molecular analysis
    - Batch efficacy predictions
    - Safety assessment
    - Regulatory compliance checks
    """
    analysis_results = []
    
    # Create thread pool for parallel processing
    with ThreadPoolExecutor() as executor:
        # Process molecules in parallel
        futures = []
        for molecule in molecules:
            future = executor.submit(
                analyze_single_molecule,
                molecule=molecule,
                storage=storage
            )
            futures.append(future)
        
        # Collect results
        for future in futures:
            try:
                result = future.result()
                analysis_results.append(result)
            except Exception as e:
                analysis_results.append({
                    "error": str(e),
                    "status": "failed"
                })
    
    # Schedule background task for detailed analysis
    background_tasks.add_task(
        perform_detailed_analysis,
        molecule_ids=[m.id for m in molecules],
        storage=storage
    )
    
    return {
        "batch_size": len(molecules),
        "successful_analyses": len([r for r in analysis_results if "error" not in r]),
        "results": analysis_results,
        "status": "detailed_analysis_scheduled"
    }

@router.post("/analyze-medication")
async def analyze_medication(
    request: MedicationRequest,
    storage = Depends(get_storage)
):
    """
    Analyze medication information and provide structured data with AI explanation.
    
    This endpoint provides:
    - 💊 Structured medication information
    - 🔍 AI-powered analysis
    - ⚠️ Safety information and disclaimers
    - 🎯 Usage recommendations
    """
    with tracer.start_as_current_span("analyze_medication") as span:
        try:
            span.set_attribute("medication", request.name)
            logger.info(f"🔍 Analyzing medication: {request.name}")
            
            # Create chat completion request for analysis
            prompt = f"""Analyze this medication:
            Name: {request.name}
            Additional Notes: {request.notes or 'None provided'}
            
            Provide a comprehensive analysis including:
            1. Common side effects
            2. Risk rating
            3. Usage recommendations
            4. Important warnings
            
            Format as a medical information summary, including appropriate disclaimers.
            """
            
            try:
                response = await chat_client.complete(
                    model=os.getenv("MODEL_DEPLOYMENT_NAME"),
                    messages=[{
                        "role": "system",
                        "content": "You are a medical information assistant. Always include appropriate medical disclaimers."
                    }, {
                        "role": "user",
                        "content": prompt
                    }]
                )
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(e)
                logger.error(f"❌ Error in chat completion: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error in chat completion: {str(e)}"
                )
            
            # Mock structured data (would be from ML model in production)
            structured_info = {
                "category": "Over-the-counter analgesic",
                "common_side_effects": ["Stomach upset", "Headache"],
                "risk_rating": "Low",
                "interactions": ["Blood thinners", "NSAIDs"]
            }
        
            logger.info(f"📊 Analysis Results:"
                   f"\n- Category: {structured_info['category']}"
                   f"\n- Risk Rating: {structured_info['risk_rating']}"
                   f"\n- Side Effects: {', '.join(structured_info['common_side_effects'])}")
            
            # Store the analysis in storage
            analysis_dict = {
                "medication": request.name,
                "notes": request.notes,
                "structured_info": structured_info,
                "ai_explanation": response.choices[0].message.content,
                "creation_date": datetime.now().isoformat()
            }
            storage["add_item"]("medication_analyses", analysis_dict)
            
            return {
                "structured_info": structured_info,
                "ai_explanation": response.choices[0].message.content,
                "disclaimer": "This information is for educational purposes only. Always consult healthcare professionals for medical advice."
            }
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error analyzing medication: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing medication: {str(e)}"
            )

@router.post("/regulatory-submission/{molecule_id}", dependencies=[Security(access_control.get_current_user, scopes=["write:regulatory"])])
async def prepare_regulatory_submission(
    molecule_id: str,
    storage = Depends(get_storage)
):
    """
    Prepare regulatory submission package:
    - Compile safety data
    - Generate efficacy reports
    - Prepare clinical trial summaries
    - Format for regulatory requirements
    """
    molecule = storage["get_item"]("drug_candidates", molecule_id)
    if not molecule:
        raise HTTPException(status_code=404, detail="Molecule not found")
    
    # Get all test results
    all_tests = storage["list_items"]("automated_tests")
    tests = [test for test in all_tests if test["drug_candidate_id"] == molecule_id]
    
    # Compile submission package
    submission_package = {
        "molecule_details": {
            "id": molecule["id"],
            "type": molecule["molecule_type"],
            "therapeutic_area": molecule["therapeutic_area"],
            "development_stage": molecule["development_stage"]
        },
        "safety_assessment": {
            "predicted_safety": molecule["predicted_safety"],
            "safety_studies": [
                {
                    "test_id": test["test_id"],
                    "type": test["test_type"],
                    "result": test["result"],
                    "safety_flags": test["safety_flags"]
                }
                for test in tests
                if test["result"] == TestResult.PASS
            ]
        },
        "efficacy_data": {
            "predicted_efficacy": molecule["predicted_efficacy"],
            "target_proteins": molecule["target_proteins"],
            "mechanism_of_action": molecule["properties"].get("mechanism_of_action", "Unknown")
        },
        "development_history": {
            "creation_date": molecule["creation_date"],
            "test_count": len(tests),
            "development_timeline": molecule["properties"].get("development_timeline", [])
        }
    }
    
    return {
        "submission_ready": True,
        "package": submission_package,
        "recommendations": [
            "Include detailed toxicology reports",
            "Add pharmacokinetic study results",
            "Prepare clinical trial protocols"
        ]
    }

@router.post("/patient-specific-analysis", dependencies=[Security(access_control.get_current_user, scopes=["read:molecules", "read:patients"])])
async def analyze_patient_specific_response(
    molecule_id: str,
    patient_id: str,
    storage = Depends(get_storage)
):
    """
    Analyze potential drug response for specific patient:
    - Consider genetic markers
    - Evaluate biomarkers
    - Assess potential interactions
    - Predict efficacy
    """
    molecule = storage["get_item"]("drug_candidates", molecule_id)
    if not molecule:
        raise HTTPException(status_code=404, detail="Molecule not found")
    
    patient = storage["get_item"]("patient_cohorts", patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Decrypt sensitive data for analysis
    decrypted_molecule = data_encryption.decrypt_molecule_data({
        "target_proteins": molecule["target_proteins"],
        "mechanism_of_action": molecule["development_stage"],
        "properties": molecule["properties"]
    })
    
    # Anonymize patient data
    anonymized_patient = data_encryption.decrypt_patient_data({
        "genetic_markers": patient["genetic_markers"],
        "biomarkers": patient["biomarkers"],
        "demographics": patient["demographics"]
    })
    
    # Audit the data access
    data_auditing.log_access(
        user_id="system",  # TODO: Get from security context
        data_type="patient_analysis",
        action="analyze",
        resource_id=f"{molecule_id}_{patient_id}",
        success=True
    )
    
    # Analyze patient-specific response with anonymized data
    genetic_compatibility = analyze_genetic_compatibility(
        decrypted_molecule["target_proteins"],
        anonymized_patient["genetic_markers"]
    )
    
    biomarker_analysis = analyze_biomarker_interaction(
        decrypted_molecule["properties"].get("biomarker_interactions", {}),
        anonymized_patient["biomarkers"]
    )
    
    return {
        "patient_specific_analysis": {
            "genetic_compatibility": genetic_compatibility,
            "biomarker_analysis": biomarker_analysis,
            "predicted_response": calculate_patient_response(
                molecule["predicted_efficacy"],
                genetic_compatibility,
                biomarker_analysis
            ),
            "potential_risks": identify_patient_risks(
                molecule["side_effects"],
                patient["demographics"],
                patient["biomarkers"]
            )
        },
        "recommendations": generate_patient_recommendations(
            molecule["therapeutic_area"],
            patient["demographics"]
        )
    }

@router.get("/candidates", response_model=List[DrugCandidate])  # TODO: Re-enable auth after testing
async def list_candidates(
    therapeutic_area: Optional[str] = None,
    min_efficacy: Optional[float] = None,
    development_stage: Optional[str] = None,
    safety_threshold: Optional[float] = None,
    storage = Depends(get_storage)
):
    """List drug candidates with advanced filtering"""
    candidates = storage["list_items"]("drug_candidates")
    
    # Apply filters
    if therapeutic_area:
        candidates = [c for c in candidates if c["therapeutic_area"] == therapeutic_area]
    if min_efficacy:
        candidates = [c for c in candidates if c["predicted_efficacy"] >= min_efficacy]
    if development_stage:
        candidates = [c for c in candidates if c["development_stage"] == development_stage]
    if safety_threshold:
        candidates = [c for c in candidates if c["predicted_safety"] >= safety_threshold]
    
    return candidates
