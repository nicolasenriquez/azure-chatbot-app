"""
Create and configure a vector store
using Azure AI Search.
"""

from typing import Callable

from langchain_community.vectorstores import AzureSearch

from backend.app.config.settings import get_settings


def create_vector_store(embedding_function: Callable) -> AzureSearch:
    """
    Create and configure a vector store using AI Search to create the index
    that will store the knowledge base.

    Args:
        embedding_function (Callable): The embbedings function used to
                                       vectorize the text.

    Returns:
        AzureSearch: Vector store instance.
    """
    settings = get_settings()

    vector_store_address: str = (
        f"https://{settings.AZURE_COGNITIVE_SEARCH_NAME}.search.windows.net"
    )
    return AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=settings.AZURE_COGNITIVE_SEARCH_API_KEY,
        index_name=settings.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
        embedding_function=embedding_function,
    )
