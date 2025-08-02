"""
Knowledge Base update module, responsible for updateing
the knowledge base by loading documents from Blob Storage.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.app.knowledge_base.blob_storage import (
    create_blob_storage_document_loader
)
from backend.app.knowledge_base.embeddings import create_embeddings_client
from backend.app.knowledge_base.vector_store import create_vector_store


def update_knowledge_base(force_update: bool = False):
    """
    Update the knowledge base by loading documents from Azure Blob Storage,
    splitting them into segments, and uploading them to Azure AI Search.

    Args:
        forced_update (bool): If True, forces the update of knowledge base.
    """
    embeddings_client = create_embeddings_client()
    vector_store = create_vector_store(embeddings_client.embed_query)
    loader = create_blob_storage_document_loader()

    try:
        existing_documents = vector_store.similarity_search("test", k=1)
        if existing_documents and not force_update:
            print(
                "✅ The knowledge base is already populated"
                "No update needed."
            )
            return
    except Exception:
        pass

    print("⚠️ Processing documents to update the knowledge base...")
    documents: list = loader.load()

    if not documents:
        print(
            "❌ No documents found in Blob Storage,"
            "therefore no action will be taken."
        )
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    splitted_documents = text_splitter.split_documents(documents=documents)

    vector_store.add_documents(documents=splitted_documents)
    print("✅ Knowledge base updated successfully.")
