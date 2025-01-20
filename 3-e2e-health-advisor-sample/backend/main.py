from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_redoc_html
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Drug Development Platform API",
    description="AI-driven drug development platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/drugs")
async def get_drugs():
    try:
        # Mock drug data for demo
        drugs = [
            {
                "id": "DRUG-001",
                "molecule_type": "Small Molecule",
                "therapeutic_area": "Oncology",
                "predicted_efficacy": 0.85,
                "predicted_safety": 0.92,
                "development_stage": "Phase 1"
            },
            {
                "id": "DRUG-002",
                "molecule_type": "Antibody",
                "therapeutic_area": "Immunology",
                "predicted_efficacy": 0.78,
                "predicted_safety": 0.95,
                "development_stage": "Preclinical"
            }
        ]
        return drugs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Platform health check endpoint"""
    return {
        "status": "ok",
        "service": "drug-development-platform"
    }
