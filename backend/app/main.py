"""
FastAPI main application file for AI Chatbot
Configures the FastAPI app, middleware, and routes
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
from azure.core.exceptions import AzureError
from backend.app.routers.chatbot_router import router
from backend.app.config.settings import get_settings, validate_get_settings


# Obtener configuraciones globales
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
        print(f"Error de configuración al iniciar: {e}")
        raise

    yield  # Aquí se ejecuta la aplicación

    # Shutdown
    print(" Shutting down AI Chatbot Backend...")

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para interactuar con un chatbot basado en RAG y almacenar logs en Turso.",
    version="1.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluir el router de chatbot_api
app.include_router(router, prefix="/api", tags=["chatbot"])

# Endpoint raíz
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
        "docs": "/docs"
    }

# Endpoint de verificación de salud
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    Used for monitoring and deployment verification
    """
    try:
        # Simular una verificación básica de conectividad con la base de datos
        if not settings.TURSO_DATABASE_URL:
            raise HTTPException(status_code=503, detail="La configuración de la base de datos es incompleta.")
        return {
            "status": "healthy",
            "service": "ai-chatbot-backend",
            "version": "1.0.1",
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# Manejador global de excepciones
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    Catches unhandled exceptions and returns structured error responses
    """
    if isinstance(exc, AzureError):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Azure Error",
                "message": "Ocurrió un error al interactuar con Azure.",
                "detail": str(exc) # Removed settings.log_level check
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Ocurrió un error inesperado.",
                "detail": str(exc) # Removed settings.log_level check
            }
        )


# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":

    # Validar las variables de entorno antes de iniciar la aplicación
    try:
        validate_get_settings()
    except RuntimeError as e:
        print(str(e))
        exit(1)            # Salir del programa con un código de error

    uvicorn.run(
        "backend.app.main:app",                         # Nombre del archivo y la instancia de la aplicación
        host="0.0.0.0",                                 # Escuchar en todas las interfaces de red
        port=settings.PORT,                             # Usar configuración de settings
        reload=settings.ENVIRONMENT == "development",   # Recarga automática en modo desarrollo
        # log_level=settings.log_level.lower()            # Removed as log_level is not in Settings
    )
    
    
# Punto de entrada backend: python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
# Punto de entrada frontend: python -m http.server 8001