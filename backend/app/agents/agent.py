"""
Este módulo define el Agente Supervisor y su flujo de ejecución utilizando LangGraph.
El grafo controla la evaluación y refinamiento de las respuestas generadas por el sistema RAG.
"""

import asyncio
import operator
import json
from typing import TypedDict, Annotated, Union

from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field, ValidationError

# Importaciones del proyecto
from backend.app.agents.rag_memory import initialize_rag_chat_chain, generate_response
from backend.app.utils import get_model

# --- 1. MODELOS DE DECISIÓN (PYDANTIC) ---

class FinalAnswer(BaseModel):
    '''Decisión final: La respuesta es de alta calidad y está lista para el usuario.'''
    answer: str = Field(..., description="La respuesta final, clara y bien formada, para ser mostrada directamente al usuario.")

class CorrectAndRefine(BaseModel):
    '''Decisión: La respuesta es conceptualmente correcta pero necesita ser mejorada.'''
    reasoning: str = Field(..., description="Explicación concisa de por qué la respuesta necesita ser refinada.")
    corrected_answer: str = Field(..., description="La versión mejorada y corregida de la respuesta.")

class ComplementWithWikipedia(BaseModel):
    '''Decisión: La respuesta se beneficiaría de contexto adicional de Wikipedia.'''
    reasoning: str = Field(..., description="Explicación de por qué se necesita contexto adicional.")
    search_query: str = Field(..., description="La consulta de búsqueda optimizada para Wikipedia.")

# La unión de todos los posibles modelos de decisión.
SupervisorDecision = Union[FinalAnswer, CorrectAndRefine, ComplementWithWikipedia]

# --- 2. DEFINICIÓN DEL ESTADO DEL GRAFO ---

class GraphState(TypedDict):
    '''
    Define el estado que fluye a través del grafo LangGraph.
    '''
    user_question: str
    rag_answer: str
    supervisor_decision: SupervisorDecision
    final_answer: str
    revision_count: Annotated[int, operator.add]

# --- 3. HERRAMIENTAS Y AGENTE SUPERVISOR ---

class RefinementAgent:
    '''
    Agente que evalúa y refina respuestas. Contiene la lógica de supervisión y combinación.
    '''
    def __init__(self):
        '''
        Inicializa el RefinementAgent cargando el modelo de lenguaje (LLM).
        '''
        self.llm = get_model()

    def _create_supervisor_prompt(self, user_question: str, rag_answer: str) -> str:
        '''
        Crea el prompt para el LLM supervisor, instruyéndolo a devolver una decisión estructurada en formato JSON.

        Args:
            user_question (str): La pregunta original del usuario.
            rag_answer (str): La respuesta generada por el agente RAG.

        Returns:
            str: El prompt formateado para el LLM.
        '''
        return f'''
        Tu rol es ser un Supervisor de Calidad de IA. Analiza la respuesta del RAG y decide el siguiente paso.
        Debes responder **SOLO** con un objeto JSON que contenga dos campos: "type" y "data".

        El campo "type" debe ser uno de los siguientes strings:
        - "FinalAnswer" (si la respuesta del RAG es excelente y está lista para el usuario)
        - "CorrectAndRefine" (si la respuesta del RAG es correcta pero necesita mejoras de estilo o claridad)
        - "ComplementWithWikipedia" (si la respuesta del RAG es buena pero se beneficiaría de contexto adicional de Wikipedia)

        El campo "data" debe ser un objeto JSON que corresponda al tipo elegido:

        Si "type" es "FinalAnswer":
        {{
            "answer": "La respuesta final, clara y bien formada, para ser mostrada directamente al usuario."
        }}

        Si "type" es "CorrectAndRefine":
        {{
            "reasoning": "Explicación concisa de por qué la respuesta necesita ser refinada.",
            "corrected_answer": "La versión mejorada y corregida de la respuesta."
        }}

        Si "type" es "ComplementWithWikipedia":
        {{
            "reasoning": "Explicación de por qué se necesita contexto adicional y qué se va a buscar.",
            "search_query": "La consulta de búsqueda optimizada para Wikipedia (ej. 'Economic Order Quantity')."
        }}

        **Ejemplo de respuesta JSON:**
        ```json
        {{
            "type": "FinalAnswer",
            "data": {{
                "answer": "El Just-in-Time es una filosofía de producción que busca eliminar el desperdicio..."
            }}
        }}
        ```

        **Pregunta Original:** "{user_question}"
        **Respuesta del RAG:** "{rag_answer}"

        Tu respuesta JSON:
        '''

    async def review_answer(self, user_question: str, rag_answer: str) -> SupervisorDecision:
        '''
        Revisa la respuesta generada por el agente RAG y decide la acción a tomar (aprobar, refinar o complementar).

        Args:
            user_question (str): La pregunta original del usuario.
            rag_answer (str): La respuesta generada por el agente RAG.

        Returns:
            SupervisorDecision: Una instancia de FinalAnswer, CorrectAndRefine o ComplementWithWikipedia.
        '''
        prompt = self._create_supervisor_prompt(user_question, rag_answer)
        
        # Invocamos el LLM para obtener la respuesta en formato JSON (como string)
        llm_response = await self.llm.ainvoke(prompt)
        response_content = llm_response.content.strip()
        
        # Eliminar los delimitadores de bloque de código Markdown si existen
        if response_content.startswith('```json') and response_content.endswith('```'):
            response_content = response_content[len('```json'):-len('```')].strip()

        try:
            # Intentamos parsear la respuesta como JSON
            parsed_json = json.loads(response_content)
            
            # Validamos el tipo y los datos contra los modelos Pydantic
            response_type = parsed_json.get("type")
            response_data = parsed_json.get("data")

            if response_type == "FinalAnswer":
                return FinalAnswer(**response_data)
            elif response_type == "CorrectAndRefine":
                return CorrectAndRefine(**response_data)
            elif response_type == "ComplementWithWikipedia":
                return ComplementWithWikipedia(**response_data)
            else:
                # Si el tipo no es reconocido, devolvemos una FinalAnswer con un mensaje de error
                print(f"Advertencia: Tipo de decisión no reconocido: {response_type}. Devolviendo respuesta original.")
                return FinalAnswer(answer=f"Lo siento, hubo un problema al procesar la respuesta. Tipo de decisión no reconocido: {response_type}. Respuesta original: {rag_answer}")

        except json.JSONDecodeError:
            print(f"Error: La respuesta del LLM no es un JSON válido. Respuesta: {response_content}")
            return FinalAnswer(answer=f"Lo siento, hubo un problema al procesar la respuesta. El LLM no devolvió un JSON válido. Respuesta original: {rag_answer}")
        except ValidationError as e:
            print(f"Error de validación Pydantic: {e}. Respuesta: {response_content}")
            return FinalAnswer(answer=f"Lo siento, hubo un problema al procesar la respuesta. Error de validación: {e}. Respuesta original: {rag_answer}")
        except Exception as e:
            print(f"Error inesperado al procesar la respuesta del LLM: {e}. Respuesta: {response_content}")
            return FinalAnswer(answer=f"Lo siento, hubo un problema inesperado al procesar la respuesta. Error: {e}. Respuesta original: {rag_answer}")


    async def combine_with_wikipedia(self, original_answer: str, wiki_context: str) -> str:
        '''
        Combina la respuesta original del agente RAG con información adicional obtenida de Wikipedia.

        Args:
            original_answer (str): La respuesta inicial generada por el agente RAG.
            wiki_context (str): El texto de contexto obtenido de Wikipedia.

        Returns:
            str: La respuesta final combinada y enriquecida.
        '''
        prompt = f'''
        Combina la respuesta original con el contexto de Wikipedia de forma natural.
        Respuesta Original: "{original_answer}"
        Contexto Wikipedia: "{wiki_context}"
        Respuesta Combinada:
        '''
        response = await self.llm.ainvoke(prompt)
        return response.content

# --- 4. NODOS DEL GRAFO LANGGRAPH ---

refinement_agent = RefinementAgent()

async def call_rag_agent(state: GraphState) -> dict:
    '''Nodo que invoca al agente RAG para obtener la respuesta inicial.'''
    print("--- Nodo: Call RAG Agent ---")
    user_question = state["user_question"]
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    rag_chain = initialize_rag_chat_chain(memory)
    response = await generate_response(rag_chain, user_question, "langgraph_session")
    return {"rag_answer": response, "revision_count": 1}

async def call_supervisor_agent(state: GraphState) -> dict:
    '''Nodo que invoca al agente supervisor para evaluar la respuesta del RAG.'''
    print("--- Nodo: Call Supervisor Agent ---")
    user_question = state["user_question"]
    rag_answer = state["rag_answer"]
    decision = await refinement_agent.review_answer(user_question, rag_answer)
    print(f"   -> Decisión: {type(decision).__name__}")
    return {"supervisor_decision": decision}

async def enrich_with_wikipedia(state: GraphState) -> dict:
    '''Nodo que enriquece la respuesta con información de Wikipedia.'''
    print("--- Nodo: Enrich with Wikipedia ---")
    decision = state["supervisor_decision"]
    rag_answer = state["rag_answer"]
    
    print(f"   -> Buscando en Wikipedia: '{decision.search_query}'")
    wiki_tool = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=2500)
    wiki_context = await asyncio.to_thread(wiki_tool.run, decision.search_query)
    
    print("   -> Combinando respuestas...")
    final_answer = await refinement_agent.combine_with_wikipedia(rag_answer, wiki_context)
    return {"final_answer": final_answer}

async def prepare_final_response(state: GraphState) -> dict:
    '''Nodo que prepara la respuesta final cuando no se necesita Wikipedia.'''
    print("--- Nodo: Prepare Final Response ---")
    decision = state["supervisor_decision"]
    if isinstance(decision, FinalAnswer):
        print("   -> Acción: Aprobar respuesta.")
        return {"final_answer": decision.answer}
    elif isinstance(decision, CorrectAndRefine):
        print(f"   -> Acción: Aplicar refinamiento. Razón: {decision.reasoning}")
        return {"final_answer": decision.corrected_answer}
    return {}

# --- 5. LÓGICA DE ENRUTAMIENTO CONDICIONAL ---

def route_decision(state: GraphState) -> str:
    '''Función de enrutamiento que decide el siguiente paso basado en la decisión del supervisor.'''
    print("--- Router: Route Decision ---")
    decision = state["supervisor_decision"]
    if isinstance(decision, ComplementWithWikipedia):
        print("   -> Ruta: a enrich_with_wikipedia")
        return "enrich_with_wikipedia"
    else:
        print("   -> Ruta: a prepare_final_response")
        return "prepare_final_response"

# --- 6. CONSTRUCCIÓN Y EJECUCIÓN DEL GRAFO ---

def build_graph():
    '''Construye y compila el grafo LangGraph.'''
    workflow = StateGraph(GraphState)

    workflow.add_node("call_rag_agent", call_rag_agent)
    workflow.add_node("call_supervisor_agent", call_supervisor_agent)
    workflow.add_node("enrich_with_wikipedia", enrich_with_wikipedia)
    workflow.add_node("prepare_final_response", prepare_final_response)

    workflow.set_entry_point("call_rag_agent")
    workflow.add_edge("call_rag_agent", "call_supervisor_agent")
    workflow.add_conditional_edges(
        "call_supervisor_agent",
        route_decision,
        {
            "enrich_with_wikipedia": "enrich_with_wikipedia",
            "prepare_final_response": "prepare_final_response"
        }
    )
    workflow.add_edge("enrich_with_wikipedia", END)
    workflow.add_edge("prepare_final_response", END)

    return workflow.compile()

async def process_user_question(user_question: str) -> str:
    '''
    Procesa la pregunta del usuario a través del flujo de LangGraph y devuelve la respuesta final.

    Args:
        user_question (str): La pregunta del usuario.

    Returns:
        str: La respuesta final generada por el chatbot.
    '''
    print("🚀 Iniciando el flujo con LangGraph...")
    app = build_graph()
    
    inputs = {"user_question": user_question}
    
    final_state = await app.ainvoke(inputs)
    
    return final_state['final_answer']

if __name__ == "__main__":
    # Este bloque solo se ejecuta si el script es llamado directamente
    asyncio.run(process_user_question("¿Qué es el Just-in-Time y cómo impacta en el inventario?"))