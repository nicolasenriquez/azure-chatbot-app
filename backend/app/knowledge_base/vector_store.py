from langchain_community.vectorstores import AzureSearch
from backend.app.config.settings import get_settings
from typing import Callable

def create_vector_store(embedding_function: Callable) -> AzureSearch:
    '''
    Crea y configura un vector store utilizando Azure AI Search.

    Args:
        embedding_function (Callable): La función de embedding a utilizar para vectorizar el texto.

    Returns:
        AzureSearch: Una instancia del vector store configurado.
    '''
    settings = get_settings()
    
    vector_store_address: str = f"https://{settings.AZURE_COGNITIVE_SEARCH_NAME}.search.windows.net"
    return AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=settings.AZURE_COGNITIVE_SEARCH_API_KEY,
        index_name=settings.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
        embedding_function=embedding_function
    )