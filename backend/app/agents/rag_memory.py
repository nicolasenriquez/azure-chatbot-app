"""
This module provides functionality for a retrieval-augmented generation (RAG)
conversational agent. It initializes a conversational chain with memory,
generates responses based on user questions.
"""

from datetime import datetime, timezone

import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback

from backend.app.config.settings import get_settings
from backend.app.utils import get_model, get_retriever

settings = get_settings()


def initialize_rag_chat_chain(memory: ConversationBufferMemory):
    """
    Initialize a custome retrieval-augmented generation (RAG)
    conversational chain for a virtual assistant.

    Args:
        memory (ConversationBufferMemory): Object to save conversation history

    Returns:
        ConversationalRetrievalChain: The RAG chain configured and ready to use
    """
    template: str = """
        Eres un asistente llamado "Ingenierin", diseñado para atender las
        consultas de estudiantes de una fundación dedicada a la formación
        de profesionales emprendedores en tiendas, minimarkets
        y pequeños negocios.

        Tu propósito es brindar orientación clara, útil y específica sobre
        temas de logística, gestión de inventario, bodegaje y reabastecimiento,
        **utilizando la información proporcionada en el contexto para
        fundamentar tus respuestas.**

        Ten en cuenta estas instrucciones para responder:
        1.  Utiliza un lenguaje formal pero cercano y amigable, adecuado para
            un entorno educativo y práctico.
        2.  **Incluye emojis relevantes y variados** para hacer las respuestas
            más visuales, atractivas y comprensibles. No abuses, pero úsalos
            estratégicamente.
        3.  **Formatea tu respuesta de manera clara y organizada, utilizando
            Markdown** (negritas, cursivas, listas numeradas o con guiones,
            encabezados si es necesario) para mejorar la legibilidad y
            priorizar la utilidad práctica para el estudiante.
        4.  **Añade saltos de línea y espacios** para que el texto no se vea
            "apelmazado" y sea fácil de escanear.
        5.  **Siempre explica brevemente cómo la información del contexto te
            ayudó a formular la respuesta, si es aplicable.**
        6.  **Nunca pidas aclaraciones sobre la pregunta del usuario.**
            Si la información en el contexto no es suficiente para una
            respuesta completa, utiliza tu mejor juicio para proporcionar la
            orientación más útil posible basada en lo que sí tienes,
            **sin inventar datos.**
        7.  Limita tus respuestas exclusivamente a temas relacionados con
            logística, finanzas, inventario, bodegaje y reabastecimiento.
            Si la consulta está fuera de estos temas, informa amablemente
            que no puedes responderla, pero sé breve.

        {context}

        Pregunta: {question}
        Respuesta:
    """

    prompt: PromptTemplate = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    llm = get_model()

    retriever = get_retriever()

    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

    return rag_chain


async def generate_response(
    rag_chain,
    user_question: str,
    session_id: str
) -> str:
    """
    Generate the model's respionse based on the user's question.

    Args:
        rag_chain (ConversationalRetrievalChain): RAG chain.
        user_question (str): User's message.
        session_id (str): Session ID.

    Returns:
        str: The model's response to the user's question.

    Raises:
        Exception: If an error occurs while communicating with the
                   OpenAI API or generating the response.
    """
    try:
        response = await rag_chain.ainvoke(
            input={"question": user_question}
        )
        return response.get("answer")
    except openai.APIError as e:
        print(
            f"Error generating response for session {session_id}: {e}"
        )
        raise Exception(f"Error communicating with OpenAI API: {e.args[0]}")
    except Exception as e:
        print(
            f"Error generating response for session {session_id}: {e}"
        )
        raise Exception(f"Error al generar la respuesta: {str(e)}")


async def generate_logs(
    rag_chain,
    user_question: str,
    session_id: str
) -> dict:
    """
    Generate logs related to the interaction.

    Args:
        rag_chain (ConversationalRetrievalChain): RAG chain.
        user_question (str): User's message.
        session_id (str): Session ID.

    Returns:
        dict: Dictionary containing logs with session ID,
        token usage, cost, user question, model's answer,
        and date processed.
    """
    try:
        with get_openai_callback() as cb:
            response = await rag_chain.ainvoke(
                input={"question": user_question}
            )

            logs = {
                "session_id": session_id,
                "total_tokens": cb.total_tokens,
                "prompt_tokens": cb.prompt_tokens,
                "completion_tokens": cb.completion_tokens,
                "total_cost_usd": cb.total_cost,
                "user_question": user_question,
                "llm_answer": response,
                "date_processed": datetime.now(timezone.utc).isoformat(),
            }
        return logs
    except openai.APIError as e:
        print(
            f"Error generating logs for session {session_id}: {e}"
        )
        raise Exception(f"Error communicating with OpenAI API: {e.args[0]}")
    except Exception as e:
        print(
            f"Error generating logs for session {session_id}: {e}"
        )
        raise Exception(f"Error al generar los logs: {str(e)}")
