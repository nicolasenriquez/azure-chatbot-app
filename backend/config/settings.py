"""
Configuration settings for Azure AI Chatbot
"""

import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application Configuration
    app_name: str = "Azure AI Chatbot"
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://bda-chatbot-frontend-e4ddbvftcmcjbvd3.chilecentral-01.azurewebsites.net",
    ]
    
    # Azure OpenAI Configuration
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    # Azure AI Search Configuration
    azure_search_endpoint: str = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    azure_search_api_key: str = os.getenv("AZURE_SEARCH_API_KEY", "")
    azure_search_index_name: str = os.getenv("AZURE_SEARCH_INDEX_NAME", "knowledge-base")
    
    # Azure Storage Configuration
    azure_storage_connection_string: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    azure_storage_container_name: str = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "documents")
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get application settings singleton"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def validate_azure_settings():
    """Validate required Azure environment variables"""
    settings = get_settings()
    
    required_vars = [
        ("AZURE_OPENAI_API_KEY", settings.azure_openai_api_key),
        ("AZURE_OPENAI_ENDPOINT", settings.azure_openai_endpoint),
        ("AZURE_SEARCH_ENDPOINT", settings.azure_search_endpoint),
        ("AZURE_SEARCH_API_KEY", settings.azure_search_api_key),
    ]
    
    missing = [var_name for var_name, value in required_vars if not value]
    
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        print("   Some features may not work correctly.")
        return False
    
    print("✅ All Azure environment variables configured")
    return True