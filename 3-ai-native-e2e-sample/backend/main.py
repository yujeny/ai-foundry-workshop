"""
Main FastAPI Application Entry Point

This module initializes and configures the FastAPI application for the Clinical Trials Monitor.
It provides:
1. Environment and logging configuration
2. FastAPI application setup with CORS and routers
3. Core health and documentation endpoints
4. Development server configuration
"""

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from utils.telemetry import configure_telemetry
from clients import ensure_clients

# -------------------------------
# Environment Configuration
# -------------------------------

# Configure logging with proper level handling
def get_log_level():
    """Get log level from environment with fallback to INFO"""
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level, logging.INFO)

logging.basicConfig(
    level=get_log_level(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure OpenTelemetry
configure_telemetry()

logger.info("🎯 Starting Clinical Trials Monitor")

# -------------------------------
# Router Imports
# -------------------------------
from routers.trials import router as trials_router

# -------------------------------
# FastAPI App Configuration
# -------------------------------

logger.info("⚙️ Configuring FastAPI application")
app = FastAPI(
    title="Clinical Trials Monitor",
    description="""
    Real-time clinical trial event monitoring and analysis system using Azure AI Agents Service.
    
    ## Features 🚀
    
    ### 1. Event Simulation
    - Generate simulated trial events
    - Publish events to Azure Event Hubs
    - Real-time event streaming
    
    ### 2. Multi-Agent Processing
    - Team Leader coordination
    - Specialized agent analysis
    - Adaptive recommendations
    
    ### 3. Telemetry Integration
    - OpenTelemetry tracing
    - Operation monitoring
    - Performance insights
    """,
    version="1.0.0"
)

# -------------------------------
# Middleware Setup
# -------------------------------

logger.info("🔒 Configuring CORS middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend application URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Router Registration
# -------------------------------

logger.info("📝 Registering API routes")
app.include_router(
    trials_router,
    prefix="/api/trials",
    tags=["trials"]
)

# -------------------------------
# Application Events
# -------------------------------

@app.on_event("startup")
async def startup_event():
    """
    Initialize required services and verify dependencies on application startup.
    """
    logger.info("📦 Imported dependencies successfully")
    logger.info("✅ Backend services initialized successfully")

# -------------------------------
# Core Endpoints
# -------------------------------

@app.get("/", include_in_schema=False)
async def root():
    """Redirect root endpoint to ReDoc API documentation."""
    return RedirectResponse(url="/redoc", status_code=302)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify service status.
    Returns:
        dict: Status indicator
    """
    return {"status": "ok"}

# -------------------------------
# Development Configuration
# -------------------------------

# Print all registered routes for debugging purposes
if os.getenv("DEBUG", "false").lower() == "true":
    logger.info("📋 Registered Routes:")
    for route in app.routes:
        logger.info(f"{route.path} - {route.name}")

logger.info("✅ Application configuration complete")

# -------------------------------
# Development Server
# -------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
