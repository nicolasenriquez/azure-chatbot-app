from langchain_community.retrievers import AzureCognitiveSearchRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.callbacks.manager import get_openai_callback
from datetime import datetime, timezone
from backend.app.config.settings import get_settings
from backend.app.utils import get_model, get_retriever
import logging
import openai


# logging configuration
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Get settings  
settings = get_settings()


def initialize_rag_chat_chain(memory: ConversationBufferMemory):
    """
    Inicializa una cadena conversacional RAG (Retrieval-Augmented Generation) personalizada
    para un asistente virtual llamado "Ingenierin".

    Args:
        memory (ConversationBufferMemory): La memoria de conversación para mantener el historial del chat.

    Returns:
        ConversationalRetrievalChain: La cadena RAG configurada y lista para usar.
    """
    # Template para reformular preguntas con historial de chat  
    contextualize_retriever_system_prompt: str = ''' 
        Tu tarea es **optimizar la recuperación de información** en un sistema RAG. Para ello, reformula la última pregunta del usuario, considerando el
        historial de conversación, para que sea una consulta **completamente independiente, clara y altamente efectiva para la búsqueda.**

        **Instrucciones clave:**
        1.  Si la pregunta del usuario ya es autónoma y no requiere contexto adicional del historial, devuélvela **exactamente sin cambios.**
        2.  Si la pregunta depende del contexto previo, integra la información necesaria del historial de forma **concisa y coherente** en la reformulación.
        3.  **Siempre produce una reformulación.** Incluso si el historial es limitado o ambiguo, haz tu mejor esfuerzo para capturar la intención del
            usuario en una consulta de búsqueda.
        4.  **Bajo ninguna circunstancia respondas la pregunta original.** Tu única función es reformularla para la búsqueda.
        5.  No añadas información que no sea estrictamente necesaria para la reformulación de la consulta.
    '''  
    contextualized_retriever_prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([  
        ('system', contextualize_retriever_system_prompt),  
        MessagesPlaceholder('chat_history'),  
        ('human', '{input}')  
    ])  
  
    # Prompt del asistente con personalidad definida 
    template: str ='''
        Eres un asistente llamado "Ingenierin", diseñado para atender las consultas de estudiantes de una fundación dedicada a la formación de profesionales
        emprendedores en tiendas, minimarkets y pequeños negocios.
        
        Tu propósito es brindar orientación clara, útil y específica sobre temas de logística, gestión de inventario, bodegaje y reabastecimiento,
        **utilizando la información proporcionada en el contexto para fundamentar tus respuestas.**
        
        Ten en cuenta estas instrucciones para responder:
        1.  Utiliza un lenguaje formal pero cercano y amigable, adecuado para un entorno educativo y práctico.
        2.  **Incluye emojis relevantes y variados** para hacer las respuestas más visuales, atractivas y comprensibles. No abuses, pero úsalos estratégicamente.
        3.  **Formatea tu respuesta de manera clara y organizada, utilizando Markdown** (negritas, cursivas, listas numeradas o con guiones, encabezados si es necesario) para mejorar la legibilidad y priorizar la utilidad práctica para el estudiante.
        4.  **Añade saltos de línea y espacios** para que el texto no se vea "apelmazado" y sea fácil de escanear.
        5.  **Siempre explica brevemente cómo la información del contexto te ayudó a formular la respuesta, si es aplicable.**
        6.  **Nunca pidas aclaraciones sobre la pregunta del usuario.** Si la información en el contexto no es suficiente para una respuesta completa,
        utiliza tu mejor juicio para proporcionar la orientación más útil posible basada en lo que sí tienes, **sin inventar datos.**
        7.  Limita tus respuestas exclusivamente a temas relacionados con logística, finanzas, inventario, bodegaje y reabastecimiento. Si la consulta está
            fuera de estos temas, informa amablemente que no puedes responderla, pero sé breve.
    
        {context}
    
        Pregunta: {question}
        Respuesta:
    '''

    prompt: PromptTemplate = PromptTemplate(template=template, input_variables=['context', 'question'])  
  
    # Inicializar llm 
    llm = get_model()
  
    # Inicializar el retriever 
    retriever = get_retriever()  
  
    # Cadena conversacional RAG  
    rag_chain: ConversationalRetrievalChain = ConversationalRetrievalChain.from_llm(  
        llm=llm,  
        memory=memory,  
        retriever=retriever,  
        combine_docs_chain_kwargs={'prompt': prompt}  
    )

    return rag_chain  
  

async def generate_response(rag_chain, user_question: str, session_id: str) -> str:
    """
    Genera la respuesta del modelo basada en la pregunta del usuario.

    Args:
        rag_chain (ConversationalRetrievalChain): La cadena RAG configurada.
        user_question (str): La pregunta del usuario.
        session_id (str): El ID de la sesión actual.

    Returns:
        str: La respuesta generada por el modelo.

    Raises:
        Exception: Si ocurre un error al comunicarse con la API de OpenAI o al generar la respuesta.
    """
    try:  
        # Ejecutar la cadena conversacional para obtener la respuesta  
        response = await rag_chain.ainvoke(input={"question": user_question})
        return response.get('answer')
    except openai.APIError as e:
        logging.error(f"OpenAI API Error generating response for session {session_id}: {e}", exc_info=True)
        raise Exception(f"Error communicating with OpenAI API: {e.args[0]}")
    except Exception as e:  
        logging.error(f"Error generating response for session {session_id}: {e}", exc_info=True)
        raise Exception(f"Error al generar la respuesta: {str(e)}")  


async def generate_logs(rag_chain, user_question: str, session_id: str) -> dict:
    """
    Genera los logs relacionados con la interacción.
    """
    try:  
        # Ejecutar la cadena conversacional con registro de costos  
        with get_openai_callback() as cb:  
            response = await rag_chain.ainvoke(input={"question": user_question})  
  
            # Diccionario de logs  
            logs = {  
                "session_id": session_id,  
                "total_tokens": cb.total_tokens,  
                "prompt_tokens": cb.prompt_tokens,  
                "completion_tokens": cb.completion_tokens,  
                "total_cost_usd": cb.total_cost,  
                "user_question": user_question,  
                "llm_answer": response,  
                "date_processed": datetime.now(timezone.utc).isoformat()  
            }  
        return logs  
    except openai.APIError as e:
        logging.error(f"OpenAI API Error generating logs for session {session_id}: {e}", exc_info=True)
        raise Exception(f"Error communicating with OpenAI API: {e.args[0]}")
    except Exception as e:  
        logging.error(f"Error generating logs for session {session_id}: {e}", exc_info=True)
        raise Exception(f"Error al generar los logs: {str(e)}")