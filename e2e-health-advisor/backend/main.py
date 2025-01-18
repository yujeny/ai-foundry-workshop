from fastapi import FastAPI, Request, Security, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader, SecurityScopes
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_redoc_html
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from datetime import datetime
import hashlib
import hmac
import logging
from logging.handlers import RotatingFileHandler
import os

from security.data_encryption import DataEncryption, DataAuditing, DataAnonymization
from security.access_control import AccessControl, RoleBasedAccess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize security components
data_encryption = DataEncryption()
data_auditing = DataAuditing()
access_control = AccessControl(os.getenv("JWT_SECRET_KEY", "your-secret-key"))
# Temporarily comment out OpenTelemetry imports until packages are installed
# from azure.core.tracing.opentelemetry import AzureSDKRegisteredTraceExporter
# from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
import os
from dotenv import load_dotenv
from routers.molecular_design import router as molecular_router
from routers.clinical_trials import router as trials_router
from routers.automated_testing import router as testing_router
from routers.supply_chain import router as supply_router

# Load environment variables
load_dotenv()

# Temporarily comment out OpenTelemetry initialization
# provider = TracerProvider(resource=Resource.create({"service.name": "drug-development-platform"}))
# processor = BatchSpanProcessor(OTLPSpanExporter())
# provider.add_span_processor(processor)
# trace.set_tracer_provider(provider)
# AzureSDKRegisteredTraceExporter.register_tracer_provider(provider)

# Initialize FastAPI app with security documentation
app = FastAPI(
    title="Drug Development Platform API",
    description="""
    AI-driven drug development platform supporting:
    - Molecular Design and Analysis
    - Automated Preclinical Testing
    - Real-time Clinical Trial Monitoring
    - Supply Chain Optimization
    
    Security Features:
    - End-to-end data encryption with Fernet
    - Role-based access control with JWT
    - Comprehensive audit logging
    - Data anonymization for research
    - HIPAA and GDPR compliance measures
    """,
    version="1.0.0",
    openapi_tags=[
        {"name": "Security", "description": "Authentication and authorization endpoints"},
        {"name": "Molecular Design", "description": "Drug candidate design and analysis"},
        {"name": "Clinical Trials", "description": "Trial management and monitoring"},
        {"name": "Automated Testing", "description": "High-throughput screening"},
        {"name": "Supply Chain", "description": "Supply chain optimization"}
    ]
)

# Configure security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Type"]
)

# Ensure proper JSON response handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Add security middleware for request auditing and headers
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Security middleware for request auditing and headers."""
    start_time = datetime.now()
    
    # Add security headers
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Audit logging
    data_auditing.log_access(
        user_id=request.headers.get("X-API-Key", "anonymous"),
        data_type="api_request",
        action=f"{request.method} {request.url.path}",
        resource_id=request.url.path,
        success=response.status_code < 400
    )
    
    # Log response time for monitoring
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Request processed in {duration:.2f}s")
    
    return response

# Initialize Azure AI client and security components
try:
    # Initialize Azure AI client
    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.getenv("PROJECT_CONNECTION_STRING"),
    )
    logger.info("✓ Successfully initialized AIProjectClient")
    
    # Verify security components
    if not os.getenv("JWT_SECRET_KEY"):
        logger.warning("No JWT_SECRET_KEY found. Using default key (not recommended for production)")
    if not os.getenv("ENCRYPTION_KEY"):
        logger.warning("No ENCRYPTION_KEY found. Generated new key")
    
    logger.info("✓ Security components initialized successfully")
except Exception as e:
    logger.error(f"× Initialization error: {str(e)}")
    raise

# Temporarily disable OpenTelemetry tracing
# tracer = trace.get_tracer(__name__)

# Include routers
app.include_router(
    molecular_router,
    prefix="/api/v1/molecular-design",  # Match frontend URL
    tags=["Molecular Design"]
)
app.include_router(
    trials_router,
    prefix="/api/v1/clinical-trials",  # Match frontend URL
    tags=["Clinical Trials"]
)
app.include_router(
    testing_router,
    prefix="/api/automated-testing",
    tags=["Automated Testing"]
)
app.include_router(
    supply_router,
    prefix="/api/supply-chain",
    tags=["Supply Chain"]
)

@app.get("/", include_in_schema=False)
async def root():
    """API Documentation"""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Drug Development Platform API",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

@app.get("/health")
async def health_check():
    """Platform health check endpoint for container readiness"""
    # Temporarily disable OpenTelemetry tracing
    # with tracer.start_as_current_span("platform.health_check") as span:
    return {
            "status": "ok",
            "service": "drug-development-platform",
            "components": {
                "molecular_design": "active",
                "clinical_trials": "active",
                "automated_testing": "active",
                "supply_chain": "active"
            }
        }
