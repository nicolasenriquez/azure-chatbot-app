"""
Creates and configures a document loader
for Azure Blob Storage.
"""

from langchain_community.document_loaders import (
    AzureBlobStorageContainerLoader
)

from backend.app.config.settings import get_settings


def create_blob_storage_document_loader() -> AzureBlobStorageContainerLoader:
    """
    Create and configure a document loader for Azure Blob Storage service.
    This function retrieves the necessary setting for the configuration of
    the service connection.

    Returns:
        AzureBlobStorageContainerLoader: Document loader instance.
    """
    settings = get_settings()

    return AzureBlobStorageContainerLoader(
        conn_str=settings.AZURE_STORAGE_CONN_STRING,
        container=settings.AZURE_STORAGE_ACCOUNT_CONTAINER_NAME,
    )
