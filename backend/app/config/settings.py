"""Configurattion settings for the application, managing environment variables for security and functionality."""

from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

import os
from typing import List, Optional
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Volver a probar mas tarde, para acceder a secretos Azure KV
# credential = ClientSecretCredential(
#     tenant_id=os.getenv("AZURE_TENANT_ID"),
#     client_id=os.getenv("AZURE_CLIENT_ID"),
#     client_secret=os.getenv("AZURE_CLIENT_SECRET")
# )

# client = SecretClient(
#     vault_url=os.getenv("AZURE_KEY_VAULT_URL"),
#     credential=credential
# )

# print(client.get_secret('azure-api-key').value)


class Settings(BaseSettings):
    
    # App configuration
    APP_NAME: str = 'Azure AI Chatbot'
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    PORT: int = int(os.getenv('PORT', 8000))
    
    # CORS configuration
    CORS_ORIGINS: List[str] = ['*']
    
    # Azure OpenAI configuration
    AZURE_API_KEY: str = os.getenv('AZURE_API_KEY')
    AZURE_ENDPOINT: str = os.getenv('AZURE_ENDPOINT')
    AZURE_API_VERSION: str = os.getenv('AZURE_API_VERSION')
    AZURE_LLM_DEPLOYMENT: str = os.getenv('AZURE_LLM_DEPLOYMENT')
    AZURE_EMBEDDING_DEPLOYMENT: str = os.getenv('AZURE_EMBEDDING_DEPLOYMENT')
    AZURE_DISPLAY_NAME: Optional[str] = os.getenv('AZURE_DISPLAY_NAME')
    
    # Azure AI Search configuration
    AZURE_COGNITIVE_SEARCH_NAME: str = os.getenv('AZURE_COGNITIVE_SEARCH_NAME')
    AZURE_COGNITIVE_SEARCH_API_KEY: str = os.getenv('AZURE_COGNITIVE_SEARCH_API_KEY')
    AZURE_COGNITIVE_SEARCH_INDEX_NAME: str = os.getenv('AZURE_COGNITIVE_SEARCH_INDEX_NAME')
    
    # Azure Blob Storage configuration
    AZURE_STORAGE_ACCOUNT_NAME: str = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    AZURE_STORAGE_ACCOUNT_API_KEY: str = os.getenv('AZURE_STORAGE_ACCOUNT_API_KEY')
    AZURE_STORAGE_ACCOUNT_CONTAINER_NAME: str = os.getenv('AZURE_STORAGE_ACCOUNT_CONTAINER_NAME')
    AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX: str = os.getenv('AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX')
    AZURE_STORAGE_CONN_STRING: str = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_API_KEY};EndpointSuffix={AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX}"
    
    # Turso Database configuration
    TURSO_AUTH_TOKEN: str = os.getenv('TURSO_AUTH_TOKEN')
    TURSO_DATABASE_URL: str = os.getenv('TURSO_DATABASE_URL')

    # Azure Key Vault configuration (if used)
    AZURE_TENANT_ID: Optional[str] = os.getenv('AZURE_TENANT_ID')
    AZURE_CLIENT_ID: Optional[str] = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET: Optional[str] = os.getenv('AZURE_CLIENT_SECRET')
    AZURE_KEY_VAULT_URL: Optional[str] = os.getenv('AZURE_KEY_VAULT_URL')
    
    # Metaconfiguracion de Pydantic para modificar comportamiento de BaseSettings
    class Config:
        env_file = ".env"         # indica de donde se cargan las variables si esta disponible
        case_sensitive = False    # las variable de entorno no son sensibles a mayusculas y minusculas


# Global settings
_settings = None

def get_settings() -> Settings:
    '''
    Obtiene una instancia global de la configuración de la aplicación (Settings).
    Si la instancia no existe, la crea.

    Returns:
        Settings: La instancia de configuración de la aplicación.
    '''
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def validate_get_settings():
    '''
    Valida que todas las variables de entorno requeridas para la aplicación estén configuradas.

    Raises:
        RuntimeError: Si alguna variable de entorno requerida no está configurada.

    Returns:
        bool: True si todas las variables de entorno están configuradas correctamente.
    '''
    settings = get_settings()

    required_vars = [
         ('AZURE_API_KEY', settings.AZURE_API_KEY),
         ('AZURE_ENDPOINT', settings.AZURE_ENDPOINT),
         ('AZURE_API_VERSION', settings.AZURE_API_VERSION),
         ('AZURE_LLM_DEPLOYMENT', settings.AZURE_LLM_DEPLOYMENT),
         ('AZURE_EMBEDDING_DEPLOYMENT', settings.AZURE_EMBEDDING_DEPLOYMENT),
         
         ('AZURE_COGNITIVE_SEARCH_NAME', settings.AZURE_COGNITIVE_SEARCH_NAME),
         ('AZURE_COGNITIVE_SEARCH_API_KEY', settings.AZURE_COGNITIVE_SEARCH_API_KEY),
         ('AZURE_COGNITIVE_SEARCH_INDEX_NAME', settings.AZURE_COGNITIVE_SEARCH_INDEX_NAME),
         
         ('AZURE_STORAGE_ACCOUNT_NAME', settings.AZURE_STORAGE_ACCOUNT_NAME),
         ('AZURE_STORAGE_ACCOUNT_API_KEY', settings.AZURE_STORAGE_ACCOUNT_API_KEY),
         ('AZURE_STORAGE_ACCOUNT_CONTAINER_NAME', settings.AZURE_STORAGE_ACCOUNT_CONTAINER_NAME),
         ('AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX', settings.AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX),
         
         ('TURSO_AUTH_TOKEN', settings.TURSO_AUTH_TOKEN),
         ('TURSO_DATABASE_URL', settings.TURSO_DATABASE_URL)
    ]

    # Check if all required variables are set
    missing = [ var_name for var_name, value in required_vars if not value ]
 
    if missing:
        missing_vars = ", ".join(missing)
        raise RuntimeError(
            f"⚠️ Faltan las siguientes variables de entorno requeridas: {missing_vars}. "
            "Verifica la configuración antes de continuar."
        )

    print("Todas las variables de entorno de Azure están configuradas correctamente.")
    return True