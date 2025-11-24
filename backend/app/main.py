from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import (
    RadicException,
    radic_exception_handler,
    general_exception_handler
)

# Initialize logging
logger.info("Starting Radic Backend API")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add exception handlers
app.add_exception_handler(RadicException, radic_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Set all CORS enabled origins - MUST be added before other middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )
    logger.info(f"CORS enabled for origins: {settings.BACKEND_CORS_ORIGINS}")

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    """Root endpoint - API welcome message."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Radic Backend API", "version": "0.1.0"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "radic-backend"
    }


