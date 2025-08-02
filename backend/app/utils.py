"""
Utilities for configuring and retrieving instances
of Azure OpenAI and Azure Cognitive Search retriever.
"""

from langchain_community.retrievers import AzureCognitiveSearchRetriever
from langchain_openai import AzureChatOpenAI

from backend.app.config.settings import get_settings


def get_model() -> AzureChatOpenAI:
    """
    Create and configure an Azure OpenAI completion model instance.

    Returns:
        AzureChatOpenAI: Azure OpenAI completion model instance.
    """
    settings = get_settings()

    return AzureChatOpenAI(
        api_key=settings.AZURE_API_KEY,
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.AZURE_LLM_DEPLOYMENT,
        deployment_name="chat",
    )


def get_retriever() -> AzureCognitiveSearchRetriever:
    """
    Create and configure a retriever for Azure Cognitive Search, retrieving
    the top 5 relevant documents based on the query.

    Returns:
        AzureCognitiveSearchRetriever: Cognitive Search Retriever instance.
    """
    settings = get_settings()

    return AzureCognitiveSearchRetriever(
        api_key=settings.AZURE_COGNITIVE_SEARCH_API_KEY,
        service_name=settings.AZURE_COGNITIVE_SEARCH_NAME,
        index_name=settings.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
        content_key="content",
        top_k=5,
    )
