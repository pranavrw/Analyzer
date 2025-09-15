"""
FastAPI main application entry point.
Registers routers and global exception handlers.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
import logging
from contextlib import asynccontextmanager
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.user_db import Base, engine
from api.auth import router as auth_router
from api.routes_dataset import router as dataset_router
from api.routes_analyzer import router as analyzer_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    try:
        # Create database tables on startup
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Cleanup code would go here
        logger.info("Application shutting down")

# Create FastAPI app
app = FastAPI(
    title="YOLO ML Training Platform",
    description="Platform for YOLO model training with dataset management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(dataset_router, prefix="/api/datasets", tags=["datasets"])
app.include_router(analyzer_router, prefix="/api/analyzer", tags=["analyzer"])

@app.get("/api/ping")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "YOLO ML Training Platform is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled error at {request.url}: {exc}")
    logger.error(traceback.format_exc())
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if app.debug else "Something went wrong"
        }
    )

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to YOLO ML Training Platform", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)