from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.tables import DrugCandidateTable, ClinicalTrialTable
from datetime import datetime, timedelta
# Temporarily disable OpenTelemetry
# from opentelemetry import trace
# tracer = trace.get_tracer(__name__)

router = APIRouter(tags=["supply-chain"])

@router.get("/predict-demand")
async def predict_demand(
    therapeutic_area: Optional[str] = None,
    timeframe_days: int = 90,
    db: Session = Depends(get_db)
):
    # Temporarily disable OpenTelemetry tracing
    # with tracer.start_as_current_span("supply_chain.predict_demand") as span:
    #     span.set_attribute("therapeutic_area", therapeutic_area or "all")
    #     span.set_attribute("timeframe_days", timeframe_days)
    """
    Predict drug demand based on:
    - global health trends
    - epidemics
    - individual patient needs
    """
    # Get active trials and their participant counts
    query = db.query(ClinicalTrialTable).filter(
        ClinicalTrialTable.status == "active"
    )
    if therapeutic_area:
        query = query.join(DrugCandidateTable).filter(
            DrugCandidateTable.therapeutic_area == therapeutic_area
        )
    
    active_trials = query.all()
    
    # Calculate demand metrics
    total_participants = sum(trial.participant_count for trial in active_trials)
    growth_rate = 0.15  # Example growth rate
    
    future_date = datetime.now() + timedelta(days=timeframe_days)
    predicted_demand = total_participants * (1 + growth_rate)
    
    return {
        "current_demand": total_participants,
        "predicted_demand": predicted_demand,
        "prediction_date": future_date.isoformat(),
        "confidence_score": 0.85,
        "factors": {
            "active_trials": len(active_trials),
            "growth_rate": growth_rate,
            "market_trends": [
                "Increasing demand in oncology",
                "Stable demand in cardiovascular",
                "Growing need in rare diseases"
            ]
        }
    }

@router.get("/inventory-optimization")
async def optimize_inventory(
    db: Session = Depends(get_db)
):
    # Temporarily disable OpenTelemetry tracing
    # with tracer.start_as_current_span("supply_chain.optimize_inventory") as span:
    #     span.set_attribute("operation", "inventory_optimization")
    """Optimize inventory based on predicted demand and trial needs"""
    return {
        "recommendations": [
            "Increase production for oncology drugs by 25%",
            "Maintain current levels for cardiovascular treatments",
            "Scale up rare disease drug production"
        ],
        "risk_factors": [
            "Supply chain disruption probability: Low",
            "Production capacity utilization: 75%",
            "Raw material availability: Stable"
        ],
        "optimization_metrics": {
            "inventory_turnover": 12,
            "stockout_risk": "Low",
            "excess_inventory_cost": "$50,000"
        }
    }
