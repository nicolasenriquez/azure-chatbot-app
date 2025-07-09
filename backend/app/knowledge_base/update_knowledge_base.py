from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.app.knowledge_base.vector_store import create_vector_store
from backend.app.knowledge_base.embeddings import create_embeddings_client
from backend.app.knowledge_base.blob_storage import create_blob_storage_document_loader


def update_knowledge_base(force_update: bool = False):
    '''
    Actualiza la base de conocimientos cargando documentos desde Azure Blob Storage,
    dividiéndolos en segmentos y subiéndolos a Azure AI Search.

    Args:
        force_update (bool): Si es True, fuerza la actualización incluso si ya hay documentos.
    '''
    
    # Inicializar compónentes para base de conocimientos
    print("🔄 Inicializando componentes para la base de conocimientos...")
    embeddings_client = create_embeddings_client()
    vector_store = create_vector_store(embeddings_client.embed_query)
    loader = create_blob_storage_document_loader()

    # Verificar si ya hay documentos en el vector store
    try:
        existing_documents = vector_store.similarity_search("test", k=1)
        if existing_documents and not force_update:
            print("✅ La base de conocimientos ya tiene documentos. No se requiere actualización.")
            return
    except Exception:
        # Si el índice no existe, debemos cargar los documentos.
        pass

    # Si no hay documentos, cargar y procesar los nuevos
    print("⚠️  La base de conocimientos está vacía o se ha forzado la actualización. Cargando documentos desde Azure Blob Storage...")
    documents: list = loader.load()

    if not documents:
        print("❌ No se encontraron documentos en el contenedor de Azure Blob Storage. No se realizará ninguna acción.")
        return

    print(f"📄 Se encontraron {len(documents)} documentos. Procesando y dividiendo...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splitted_documents = text_splitter.split_documents(documents=documents)

    # Subir los documentos al vector store
    print(f"⬆️  Subiendo {len(splitted_documents)} segmentos de documentos a Azure AI Search...")
    vector_store.add_documents(documents=splitted_documents)
    print("✅ Base de conocimientos actualizada con éxito.")