"""
FastAPI main application file for AI Chatbot
Configures the FastAPI app, middleware, and routes
"""

from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from azure.core.exceptions import AzureError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.config.settings import get_settings, validate_get_settings
from backend.app.routers.chatbot_router import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management
    Handles startup and shutdown events
    """
    # Startup
    print(" Starting AI Chatbot Backend...")
    try:
        validate_get_settings()
    except RuntimeError as e:
        print(f"Configuration error while initializing: {e}")
        raise

    yield

    print(" Shutting down AI Chatbot Backend...")


app = FastAPI(
    title=settings.APP_NAME,
    description="API interact with a RAG-based Agentic Chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["chatbot"])


@app.get("/")
async def root():
    """
    Root endpoint
    Returns basic API information
    """
    return {
        "message": "AI Chatbot API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    Used for monitoring and deployment verification
    """
    try:
        if not settings.TURSO_DATABASE_URL:
            raise HTTPException(
                status_code=503, detail="Database configuration is incomplete"
            )
        return {
            "status": "healthy",
            "service": "ai-chatbot-backend",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    Catches unhandled exceptions and returns structured error responses

    Args:
        request: The incoming request object
        exc: The exception that was raised

    Returns:
        JSONResponse: A structured error response with status code 500
    """
    if isinstance(exc, AzureError):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Azure Error",
                "message": "An error ocurred while interacting with Azure",
                "detail": str(exc),
            },
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "detail": str(exc),
            },
        )


if __name__ == "__main__":
    try:
        validate_get_settings()
    except RuntimeError as e:
        print(str(e))
        exit(1)

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
