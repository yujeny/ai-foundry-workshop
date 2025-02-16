"""
Main FastAPI Application Entry Point

This module initializes and configures the FastAPI application for the AI-native Drug Discovery Platform.
It sets up middleware, routers, and core endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
import logging
from dotenv import load_dotenv
from utils.logging_config import setup_logging
from clients import ensure_clients

# Initialize logging first
setup_logging()
logger = logging.getLogger(__name__)

logger.info("🎯 Starting AI-native Drug Discovery Platform")

# Initialize environment and logging
# -------------------------------

# Load environment variables from .env file
load_dotenv()

# Configure logging with level from environment (defaults to INFO)
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import application routers
# ------------------------
from routers.trials import router as trials_router
from routers.agents import router as agents_router

# FastAPI App Configuration
# -----------------------

logger.info("⚙️ Configuring FastAPI application")
app = FastAPI(
    title="AI-native Drug Discovery Platform (Sample)",
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
    version="1.0.0"
)

# Middleware Configuration
# ----------------------

logger.info("🔒 Configuring CORS middleware")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Registration
# -----------------

logger.info("📝 Registering API routes")
app.include_router(trials_router, prefix="/api/trials", tags=["trials"])
app.include_router(agents_router, prefix="/api/agents", tags=["agents"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("📦 Imported dependencies successfully")
    
    # Initialize clients before serving requests
    logger.info("🔌 Initializing backend services")
    try:
        ensure_clients()  # No need for await since it's not async anymore
        logger.info("✅ Backend services initialized successfully")
    except Exception as e:
        logger.error("❌ Failed to initialize backend services: %s", str(e), exc_info=True)
        raise

# Core Endpoints
# ------------

@app.get("/", include_in_schema=False)
async def root():
    """Redirect root endpoint to ReDoc API documentation."""
    return RedirectResponse(url="/redoc", status_code=302)

@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify service status."""
    return {"status": "ok"}

# Debug Information
# --------------
# Print all registered routes for debugging purposes
for route in app.routes:
    print(route.path, route.name)

# Development Server
# ---------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

logger.info("✅ Application configuration complete")
