"""
Creates and configures an embeddings client
from Azure OpenAI.
"""

from langchain_openai import AzureOpenAIEmbeddings

from backend.app.config.settings import get_settings


def create_embeddings_client() -> AzureOpenAIEmbeddings:
    """
    Create and configure an embedding client.

    Returns:
        AzureOpenAIEmbeddings: Embeddings instance.
    """
    settings = get_settings()

    return AzureOpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.AZURE_API_KEY,
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.AZURE_EMBEDDING_DEPLOYMENT,
    )
