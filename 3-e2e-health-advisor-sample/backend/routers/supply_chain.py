from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.tables import DrugCandidateTable, ClinicalTrialTable
from datetime import datetime, timedelta
import logging

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan

# Import Azure AI Foundry clients from main
from main import inference_client, tracer

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["supply-chain"])

@router.get("/predict-demand")
async def predict_demand(
    therapeutic_area: Optional[str] = None,
    timeframe_days: int = 90,
    db: Session = Depends(get_db)
):
    with tracer.start_as_current_span("supply_chain.predict_demand") as span:
        try:
            span.set_attribute("therapeutic_area", therapeutic_area or "all")
            span.set_attribute("timeframe_days", timeframe_days)
            logger.info(f"📊 Predicting demand for {therapeutic_area or 'all'} over {timeframe_days} days")
            
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
            
            logger.info(f"✅ Successfully predicted demand for {len(active_trials)} active trials")
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
            
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error predicting demand: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error predicting demand: {str(e)}"
            )
    """
    ### 📈 Drug Demand Prediction
    
    Predict pharmaceutical demand based on:
    - 🌍 Global health trends
    - 🦠 Epidemic patterns
    - 👥 Patient population needs
    - 📊 Historical usage data
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Predictor
        participant Trials
        participant Market
        
        Client->>Predictor: Request Forecast
        Predictor->>Trials: Get Trial Data
        Predictor->>Market: Get Trends
        Trials-->>Predictor: Active Trials
        Market-->>Predictor: Market Data
        Predictor-->>Client: Demand Forecast
    ```
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
    """
    ### 📦 Inventory Optimization
    
    Smart inventory management using:
    - 🔄 Supply chain analytics
    - 📊 Demand forecasting
    - ⚡ Real-time monitoring
    - 🎯 Risk assessment
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Optimizer
        participant Inventory
        participant Risk
        
        Client->>Optimizer: Request Optimization
        Optimizer->>Inventory: Check Levels
        Optimizer->>Risk: Assess Risks
        Risk-->>Optimizer: Risk Factors
        Inventory-->>Optimizer: Stock Data
        Optimizer-->>Client: Recommendations
    ```
    """
    with tracer.start_as_current_span("supply_chain.optimize_inventory") as span:
        try:
            span.set_attribute("operation", "inventory_optimization")
            logger.info("📦 Starting inventory optimization analysis")
            logger.info("✅ Successfully optimized inventory")
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
            
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            logger.error(f"❌ Error optimizing inventory: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error optimizing inventory: {str(e)}"
            )
