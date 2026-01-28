"""
FastAPI main application setup and configuration.
Initializes the API with middleware, routes, and lifecycle management.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import os

from app.routes.analyze import router as analyze_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Lifecycle event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.
    Ensures proper resource cleanup.
    """
    
    # Startup
    logger.info("🚀 Starting AI Resume-JD Matcher API...")
    
    # Verify OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        logger.warning("⚠️ OPENAI_API_KEY not set - API calls will fail")
    else:
        logger.info("✓ OpenAI API key configured")
    
    logger.info("✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    logger.info("✅ Application shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title="AI Resume-JD Matcher",
    description="Compare resumes against job descriptions using LLM-based analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://localhost:3002",
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"✓ CORS enabled for: {origins}")


# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests and responses.
    Useful for debugging and monitoring.
    """
    
    start_time = time.time()
    
    # Log request
    logger.debug(f"📨 {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"❌ Request failed: {str(e)}")
        raise
    
    # Calculate processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.debug(f"📤 {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
    
    return response


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected errors with consistent response format.
    """
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "detail": "An unexpected error occurred"
        }
    )


# Include API routes
app.include_router(analyze_router)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Verifies API is running.
    """
    return {
        "status": "healthy",
        "message": "AI Resume-JD Matcher API is running"
    }


# Root endpoint with API information
@app.get("/", tags=["info"])
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "name": "AI Resume-JD Matcher",
        "version": "1.0.0",
        "description": "Compare resumes against job descriptions using LLM-based analysis",
        "docs": "/api/docs",
        "endpoints": {
            "analyze": "/api/v1/analyze (POST)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run development server
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    logger.info(f"🌐 Starting server on {host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
