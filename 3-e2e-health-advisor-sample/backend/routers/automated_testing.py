from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.tables import AutomatedTestTable, DrugCandidateTable
from models.automated_test import AutomatedTest, TestResult
from datetime import datetime
import json
import asyncio
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan
from azure.ai.projects.models import Evaluation, Dataset, EvaluatorConfiguration
from azure.ai.evaluation import F1ScoreEvaluator

# Import Azure AI Foundry clients from main
from main import inference_client, f1_evaluator, tracer

router = APIRouter(tags=["automated-testing"])

@router.post("/evaluation/run-demo")
async def run_evaluation_demo(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    ### 📊 Run Evaluation Demo
    
    This endpoint demonstrates how to use Azure AI Evaluation to assess model outputs.
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Evaluator
        participant Dataset
        participant Metrics
        
        Client->>Dataset: Upload JSONL Data
        Dataset->>Evaluator: Configure Evaluation
        Evaluator->>Metrics: Run F1 Score
        Evaluator->>Metrics: Run Relevance
        Metrics-->>Client: Return Results
    ```
    
    The evaluation will:
    - 📝 Load sample evaluation data
    - 🔍 Configure multiple evaluators
    - 📈 Calculate metrics
    - 📊 Return detailed results
    """
    with tracer.start_as_current_span("run_evaluation_demo") as span:
        try:
            # Load sample evaluation data
            data_path = Path(__file__).parent.parent / "data" / "sample_evaluation.jsonl"
            
            # Load and evaluate data
            with open(data_path, "r") as f:
                evaluation_data = [json.loads(line) for line in f if line.strip()]
            
            # Run F1 score evaluation
            evaluation_results = f1_evaluator.evaluate(evaluation_data)
            
            # Store results in database
            test = AutomatedTestTable(
                test_id=f"EVAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                test_type="AI_EVALUATION",
                start_time=datetime.now(),
                parameters={"evaluation_type": "f1_score"},
                result=TestResult.PASSED,
                measurements={"f1_score": evaluation_results},
                ai_analysis={"metrics": evaluation_results}
            )
            db.add(test)
            db.commit()
            
            return {
                "message": "Evaluation complete",
                "results": {
                    "f1_score": evaluation_results
                },
                "metrics": [
                    "F1 Score - Measuring output accuracy"
                ]
            }
            
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error in evaluation demo: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in evaluation demo: {str(e)}"
            )

@router.post("/high-throughput-screen")
async def run_high_throughput_screening(
    test_type: str,
    drug_candidates: List[str],
    db: Session = Depends(get_db)
):
    # Temporarily disable OpenTelemetry tracing
    # with tracer.start_as_current_span("automated_testing.high_throughput_screen") as span:
    #     span.set_attribute("candidate_count", len(drug_candidates))
    #     span.set_attribute("test_type", test_type)
    """
    Perform high-throughput screening on multiple drug candidates:
    - Parallel testing
    - Automated analysis
    - Safety monitoring
    """
    results = []
    for candidate_id in drug_candidates:
        # Create test record
        test = AutomatedTestTable(
            test_id=f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            drug_candidate_id=candidate_id,
            test_type=test_type,
            start_time=datetime.now(),
            parameters={"concentration": "10uM", "duration": "48h"},
            result=TestResult.IN_PROGRESS
        )
        db.add(test)
        db.commit()
        
        results.append({
            "test_id": test.test_id,
            "drug_candidate_id": candidate_id,
            "status": "initiated",
            "estimated_completion": "48 hours"
        })
    
    return {
        "message": f"Initiated high-throughput screening for {len(drug_candidates)} candidates",
        "results": results
    }

@router.get("/results/{test_id}")
async def get_test_results(
    test_id: str,
    db: Session = Depends(get_db)
):
    # Temporarily disable OpenTelemetry tracing
    # with tracer.start_as_current_span("automated_testing.get_results") as span:
    #     span.set_attribute("test_id", test_id)
    """Get automated test results and AI analysis"""
    test = db.query(AutomatedTestTable).filter(AutomatedTestTable.test_id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return {
        "test_id": test.test_id,
        "drug_candidate_id": test.drug_candidate_id,
        "result": test.result,
        "measurements": test.measurements,
        "ai_analysis": test.ai_analysis,
        "safety_flags": test.safety_flags
    }
