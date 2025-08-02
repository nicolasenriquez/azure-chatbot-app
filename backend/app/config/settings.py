"""
Configuration settings for the application,
managing environment variables for security
and functionality.
"""

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Application configuration settings.
    """

    APP_NAME: str = "Azure AI Chatbot"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://bda-chatbot-frontend-e4ddbvftcmcjbvd3.chilecentral-01.azurewebsites.net",
    ]

    AZURE_API_KEY: str = os.getenv("AZURE_API_KEY")
    AZURE_ENDPOINT: str = os.getenv("AZURE_ENDPOINT")
    AZURE_API_VERSION: str = os.getenv("AZURE_API_VERSION")
    AZURE_LLM_DEPLOYMENT: str = os.getenv("AZURE_LLM_DEPLOYMENT")
    AZURE_EMBEDDING_DEPLOYMENT: str = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    AZURE_DISPLAY_NAME: Optional[str] = os.getenv("AZURE_DISPLAY_NAME")

    AZURE_COGNITIVE_SEARCH_NAME: str = os.getenv("AZURE_COGNITIVE_SEARCH_NAME")
    AZURE_COGNITIVE_SEARCH_API_KEY: str = os.getenv(
        "AZURE_COGNITIVE_SEARCH_API_KEY"
    )
    AZURE_COGNITIVE_SEARCH_INDEX_NAME: str = os.getenv(
        "AZURE_COGNITIVE_SEARCH_INDEX_NAME"
    )

    AZURE_STORAGE_ACCOUNT_NAME: str = os.getenv(
        "AZURE_STORAGE_ACCOUNT_NAME"
    )
    AZURE_STORAGE_ACCOUNT_API_KEY: str = os.getenv(
        "AZURE_STORAGE_ACCOUNT_API_KEY"
    )
    AZURE_STORAGE_ACCOUNT_CONTAINER_NAME: str = os.getenv(
        "AZURE_STORAGE_ACCOUNT_CONTAINER_NAME"
    )
    AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX: str = os.getenv(
        "AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX"
    )
    AZURE_STORAGE_CONN_STRING: str = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={AZURE_STORAGE_ACCOUNT_NAME};"
        f"AccountKey={AZURE_STORAGE_ACCOUNT_API_KEY};"
        f"EndpointSuffix={AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX}"
    )

    TURSO_AUTH_TOKEN: str = os.getenv("TURSO_AUTH_TOKEN")
    TURSO_DATABASE_URL: str = os.getenv("TURSO_DATABASE_URL")

    AZURE_TENANT_ID: Optional[str] = os.getenv("AZURE_TENANT_ID")
    AZURE_CLIENT_ID: Optional[str] = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: Optional[str] = os.getenv("AZURE_CLIENT_SECRET")
    AZURE_KEY_VAULT_URL: Optional[str] = os.getenv("AZURE_KEY_VAULT_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False


_settings = None


def get_settings() -> Settings:
    """
    Obtains a global instance of the app configuration (Setttings).
    If the instance doesn't exist, it creates one.

    Returns:
        Settings: The instance of the app configuration
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def validate_get_settings():
    """
    Validates that all required environment variables are set correctly

    Raises:
        RuntimeError: If any required environment variable is missing

    Returns:
        bool: True all required environment variables are set
    """
    settings = get_settings()

    required_vars = [
        ("AZURE_API_KEY", settings.AZURE_API_KEY),
        ("AZURE_ENDPOINT", settings.AZURE_ENDPOINT),
        ("AZURE_API_VERSION", settings.AZURE_API_VERSION),
        ("AZURE_LLM_DEPLOYMENT", settings.AZURE_LLM_DEPLOYMENT),
        (
            "AZURE_EMBEDDING_DEPLOYMENT",
            settings.AZURE_EMBEDDING_DEPLOYMENT
        ),
        (
            "AZURE_COGNITIVE_SEARCH_NAME",
            settings.AZURE_COGNITIVE_SEARCH_NAME
        ),
        (
            "AZURE_COGNITIVE_SEARCH_API_KEY",
            settings.AZURE_COGNITIVE_SEARCH_API_KEY
        ),
        (
            "AZURE_COGNITIVE_SEARCH_INDEX_NAME",
            settings.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
        ),
        (
            "AZURE_STORAGE_ACCOUNT_NAME",
            settings.AZURE_STORAGE_ACCOUNT_NAME
        ),
        (
            "AZURE_STORAGE_ACCOUNT_API_KEY",
            settings.AZURE_STORAGE_ACCOUNT_API_KEY
        ),
        (
            "AZURE_STORAGE_ACCOUNT_CONTAINER_NAME",
            settings.AZURE_STORAGE_ACCOUNT_CONTAINER_NAME,
        ),
        (
            "AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX",
            settings.AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX,
        ),
        ("TURSO_AUTH_TOKEN", settings.TURSO_AUTH_TOKEN),
        ("TURSO_DATABASE_URL", settings.TURSO_DATABASE_URL),
    ]

    missing: list = [
        var_name for var_name, value in required_vars if not value
    ]

    if missing:
        missing_vars = ", ".join(missing)
        raise RuntimeError(
            f"⚠️ Missing the following environment variables: {missing_vars}."
            "Check the configuration before continuing."
        )

    print("All the environment variables are set correctly.")
    return True
