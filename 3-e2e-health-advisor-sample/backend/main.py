from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_redoc_html
# Temporarily disable Azure imports
# from azure.identity import DefaultAzureCredential
# from azure.ai.projects import AIProjectClient
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables
load_dotenv()

# Azure Configuration
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# OpenTelemetry Configuration
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "drug-development-platform")
OTEL_RESOURCE_ATTRIBUTES = os.getenv("OTEL_RESOURCE_ATTRIBUTES", "deployment.environment=development")

# Audit Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "/var/log/drugdev/data_access.log")

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate required environment variables
required_vars = [
    "AZURE_CLIENT_ID",
    "AZURE_CLIENT_SECRET",
    "AZURE_TENANT_ID",
    "PROJECT_CONNECTION_STRING",
    "MODEL_DEPLOYMENT_NAME",
    "DATABASE_URL"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
    logger.error(error_msg)
    raise ValueError(error_msg)

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
