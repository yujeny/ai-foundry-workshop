from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_redoc_html
from openai import AzureOpenAI
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

# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OpenTelemetry exporter
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Initialize Azure OpenAI client
try:
    api_key = os.getenv("AZURE_CLIENT_SECRET")  # Using client secret as API key
    deployment_name = os.getenv('MODEL_DEPLOYMENT_NAME')
    if not api_key:
        raise ValueError("Azure OpenAI API key not found")
    if not deployment_name:
        raise ValueError("Azure OpenAI deployment name not found")

    # Initialize Azure credentials with proper scope
    credential = DefaultAzureCredential()
    
    # Get token with correct audience
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    
    # Initialize the client with Azure AD token
    inference_client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,  # Using the connection string
        api_version="2024-02-15-preview",
        api_key=os.getenv("AZURE_CLIENT_SECRET"),  # Using client secret as API key
        azure_ad_token_provider=lambda: credential.get_token("https://cognitiveservices.azure.com/.default").token
    )
    
    logger.info(f"""✨ Successfully initialized Azure OpenAI client:
    Endpoint: {AZURE_ENDPOINT}
    API Version: 2024-02-15-preview
    Deployment: {deployment_name}""")
    
    # Initialize evaluators
    f1_evaluator = F1ScoreEvaluator()
    
    # Test the client configuration
    try:
        # Simple test completion to verify configuration
        deployment_name = os.getenv('MODEL_DEPLOYMENT_NAME')
        test_response = inference_client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        logger.info(f"✅ Successfully connected to Azure OpenAI using deployment: {deployment_name}")
    except Exception as e:
        logger.warning(f"⚠️ Could not test connection, but continuing anyway: {str(e)}")
    # Initialize evaluators
    f1_evaluator = F1ScoreEvaluator()  # F1Score doesn't need model config
    logger.info("✨ Successfully initialized Azure AI Foundry clients")
except Exception as e:
    logger.error(f"❌ Error initializing Azure AI Foundry clients: {str(e)}")
    raise

# Import routers
from routers import molecular_design, clinical_trials, automated_testing, supply_chain, agents, evaluation

# Initialize FastAPI app
app = FastAPI(
    title="Drug Development Platform API",
    description="AI-driven drug development platform with Azure AI Foundry integration",
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
    with tracer.start_as_current_span("health_check") as span:
        span.set_attribute("service.name", OTEL_SERVICE_NAME)
        return {
            "status": "ok",
            "service": "drug-development-platform",
            "ai_foundry": {
                "inference_client": inference_client is not None,
                "evaluators": {
                    "f1_score": f1_evaluator is not None
                }
            }
        }

# Register routers
app.include_router(molecular_design.router, prefix="/molecular-design", tags=["molecular-design"])
app.include_router(clinical_trials.router, prefix="/clinical-trials", tags=["clinical-trials"])
app.include_router(automated_testing.router, prefix="/automated-testing", tags=["automated-testing"])
app.include_router(supply_chain.router, prefix="/supply-chain", tags=["supply-chain"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])

# Initialize OpenTelemetry instrumentation for FastAPI
FastAPIInstrumentor.instrument_app(app)
