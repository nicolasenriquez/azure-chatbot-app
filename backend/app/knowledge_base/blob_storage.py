from langchain_community.document_loaders import AzureBlobStorageContainerLoader
from backend.app.config.settings import get_settings


def create_blob_storage_document_loader() -> AzureBlobStorageContainerLoader:
    '''
    Crea y configura un cargador de documentos para Azure Blob Storage.

    Returns:
        AzureBlobStorageContainerLoader: Una instancia del cargador de documentos.
    '''

    settings = get_settings()

    return AzureBlobStorageContainerLoader(
        conn_str=settings.AZURE_STORAGE_CONN_STRING,
        container=settings.AZURE_STORAGE_ACCOUNT_CONTAINER_NAME
    ) 