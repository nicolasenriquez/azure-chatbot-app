from langchain_openai import AzureChatOpenAI
from langchain_community.retrievers import AzureCognitiveSearchRetriever
from backend.app.config.settings import get_settings


def get_model() -> AzureChatOpenAI:
    '''
    Obtiene y configura una instancia del modelo de lenguaje Azure OpenAI Chat.

    Returns:
        AzureChatOpenAI: Una instancia del modelo de chat configurado.
    '''
    settings = get_settings()
    
    return AzureChatOpenAI(
        api_key=settings.AZURE_API_KEY,
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.AZURE_LLM_DEPLOYMENT,
        deployment_name='chat'
    )


def get_retriever() -> AzureCognitiveSearchRetriever:
    '''
    Obtiene y configura un retriever para Azure Cognitive Search.

    Returns:
        AzureCognitiveSearchRetriever: Una instancia del retriever configurado.
    '''
    settings = get_settings()
    
    return AzureCognitiveSearchRetriever(
        api_key=settings.AZURE_COGNITIVE_SEARCH_API_KEY,
        service_name=settings.AZURE_COGNITIVE_SEARCH_NAME,
        index_name=settings.AZURE_COGNITIVE_SEARCH_INDEX_NAME,
        content_key='content',
        top_k=5
    )