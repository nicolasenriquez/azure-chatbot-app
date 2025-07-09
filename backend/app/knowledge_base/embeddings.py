from langchain_openai import AzureOpenAIEmbeddings
from backend.app.config.settings import get_settings


def create_embeddings_client() -> AzureOpenAIEmbeddings:
    '''
    Crea y configura un cliente para generar embeddings utilizando Azure OpenAI.

    Returns:
        AzureOpenAIEmbeddings: Una instancia del cliente de embeddings.
    '''
    settings = get_settings()
    
    return AzureOpenAIEmbeddings(
        model='text-embedding-3-small',
        api_key=settings.AZURE_API_KEY,
        api_version=settings.AZURE_API_VERSION,
        azure_endpoint=settings.AZURE_ENDPOINT,
        azure_deployment=settings.AZURE_EMBEDDING_DEPLOYMENT
    )