from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_redoc_html
from clients import project_client, chat_client, toolset, ensure_clients
from azure.ai.evaluation import F1ScoreEvaluator
from azure.identity import DefaultAzureCredential
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan
from datetime import datetime
import logging
import os
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables
load_dotenv()

# Azure Configuration
# Set environment variables for DefaultAzureCredential
os.environ["AZURE_CLIENT_ID"] = os.getenv("AZURE_CLIENT_ID", "")
os.environ["AZURE_CLIENT_SECRET"] = os.getenv("AZURE_CLIENT_SECRET", "")
os.environ["AZURE_TENANT_ID"] = os.getenv("AZURE_TENANT_ID", "")

# Update Azure endpoint and model variables
AZURE_ENDPOINT = os.getenv("PROJECT_CONNECTION_STRING")  # Using the connection string from .env
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

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
    "MODEL_DEPLOYMENT_NAME"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
    logger.error(error_msg)
    raise ValueError(error_msg)

# Import tracer from clients
from clients import tracer

# Configure OpenTelemetry exporter if not in test mode
if not os.getenv("TEST_MODE"):
    otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    logger.info("OpenTelemetry exporter configured for production")
else:
    logger.info("Running in test mode - OpenTelemetry exporter disabled")

# Initialize evaluators
f1_evaluator = F1ScoreEvaluator()

# Import routers
from routers import molecular_design, clinical_trials, automated_testing, supply_chain, agents, evaluation

# Initialize FastAPI app
app = FastAPI(
    title="Drug Discovery Platform",
    description="""
    AI-powered drug discovery platform leveraging Azure AI Agents Service capabilities.
    
    ## Features 🚀
    
    ### 1. Literature Search with Bing Grounding
    - Search and analyze scientific literature
    - Ground responses in recent publications
    - Track research developments
    
    ### 2. Molecule Analysis with Function Calling
    - Analyze molecular properties
    - Predict protein interactions
    - Assess drug-like characteristics
    
    ### 3. Clinical Trial Data Analysis with Code Interpreter
    - Process trial data
    - Generate visualizations
    - Extract insights
    """,
    version="1.0.0",
    docs_url=None,  # Disable Swagger UI
    redoc_url=None  # We'll serve Redoc at root
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

@app.get("/", include_in_schema=False)
async def root():
    """Serve Redoc documentation at root."""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Drug Discovery Platform API Documentation",
        redoc_favicon_url="/favicon.ico"
    )

@app.get("/health", tags=["system"])
async def health_check():
    """
    Platform health check endpoint.
    
    Returns:
        dict: Health status information including version and timestamp
    """
    with tracer.start_as_current_span("health_check") as span:
        span.set_attribute("service.name", OTEL_SERVICE_NAME)
        return {
            "status": "ok",
            "service": "drug-discovery-platform",
            "ai_foundry": {
                "project_client": project_client is not None,
                "chat_client": chat_client is not None,
                "evaluators": {
                    "f1_score": f1_evaluator is not None
                }
            }
        }

# Initialize clients on startup
@app.on_event("startup")
async def startup_event():
    """Initialize clients on startup."""
    await ensure_clients()

# Register routers
app.include_router(molecular_design.router, prefix="/molecular-design", tags=["molecular-design"])
app.include_router(clinical_trials.router, prefix="/clinical-trials", tags=["clinical-trials"])
app.include_router(automated_testing.router, prefix="/automated-testing", tags=["automated-testing"])
app.include_router(supply_chain.router, prefix="/supply-chain", tags=["supply-chain"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])

# Initialize OpenTelemetry instrumentation for FastAPI if not in test mode
if not os.getenv("TEST_MODE"):
    FastAPIInstrumentor.instrument_app(app)
    logger.info("FastAPI OpenTelemetry instrumentation enabled")
else:
    logger.info("Running in test mode - FastAPI OpenTelemetry instrumentation disabled")
