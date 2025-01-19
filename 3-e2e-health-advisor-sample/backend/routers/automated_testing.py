from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.tables import AutomatedTestTable, DrugCandidateTable
from models.automated_test import AutomatedTest, TestResult
from datetime import datetime
# Temporarily disable OpenTelemetry
# from opentelemetry import trace
# tracer = trace.get_tracer(__name__)

router = APIRouter(tags=["automated-testing"])

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
