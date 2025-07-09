# Azure AI Chatbot Agent 🤖

Un asistente de chatbot inteligente con un pipeline RAG (Retrieval-Augmented Generation) y un agente supervisor, construido con FastAPI, LangGraph y la potencia de los servicios de Azure AI.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-blueviolet?style=for-the-badge)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-orange?style=for-the-badge)](https://python.langchain.com/docs/langgraph/)
[![Azure](https://img.shields.io/badge/Azure-blue?style=for-the-badge&logo=microsoftazure)](https://azure.microsoft.com/)

---

## 🚀 Demostración Visual

Aquí puedes ver al chatbot en acción. La interfaz es limpia, responsive y ofrece una experiencia de usuario fluida.

*(Aquí se puede insertar un GIF grabado de la pantalla mostrando la interacción con el chatbot)*
`[GIF de la interfaz de usuario]`

## 🎯 Descripción General

Este proyecto es una implementación completa de un chatbot de IA diseñado para un propósito específico: servir como asistente para estudiantes de una fundación que forma a profesionales y emprendedores de pequeños negocios. El chatbot está especializado en temas de **logística, gestión de inventario, bodegaje y reabastecimiento**.

Utiliza un patrón de **Generación Aumentada por Recuperación (RAG)** para basar sus respuestas en una base de conocimientos de documentos PDF, garantizando que la información sea precisa y relevante. Para asegurar la calidad y coherencia de las respuestas, se ha implementado un **agente supervisor con LangGraph** que evalúa, refina y, si es necesario, enriquece las respuestas antes de entregarlas al usuario.

## ✨ Características Principales

### Backend (FastAPI)
- ✅ **API Robusta:** Construida con FastAPI, ofreciendo alto rendimiento y documentación automática de endpoints.
- ✅ **Pipeline RAG:** Utiliza Azure AI Search como un vector store para recuperar información relevante de documentos.
- ✅ **Agente Supervisor (LangGraph):** Un grafo de estados que orquesta un flujo de control de calidad:
    - **Evaluación:** Decide si la respuesta del RAG es adecuada.
    - **Refinamiento:** Corrige y mejora el estilo o la claridad de la respuesta.
    - **Enriquecimiento:** Puede consultar fuentes externas (como Wikipedia) para añadir contexto adicional.
- ✅ **Integración Nativa con Azure:** Utiliza `AzureChatOpenAI` para los modelos de lenguaje y `AzureOpenAIEmbeddings` para la generación de embeddings.
- ✅ **Gestión de Conversación:** Mantiene el historial del chat para dar respuestas contextuales.
- ✅ **Configuración Centralizada:** Manejo de secretos y configuraciones a través de variables de entorno con Pydantic.

### Frontend (HTML, CSS, JS)
- ✅ **Interfaz Moderna:** Diseño *dark-mode* con acentos de color y una estética profesional.
- ✅ **Totalmente Responsive:** Adaptable a dispositivos de escritorio, tabletas y móviles.
- ✅ **Experiencia de Usuario Mejorada:** Indicador de "escribiendo...", auto-ajuste del área de texto y animaciones suaves.
- ✅ **Renderizado de Markdown:** Las respuestas del chatbot se renderizan como Markdown, permitiendo formato de texto, listas y más.
- ✅ **PWA Ready:** Incluye un Service Worker para capacidades offline básicas.

## 🛠️ Tech Stack

| Área | Tecnología/Servicio | Propósito |
| :--- | :--- | :--- |
| **Backend** | Python, FastAPI, Uvicorn | Creación de la API y servidor web |
| | LangChain, LangGraph | Orquestación del pipeline RAG y lógica de agentes |
| **IA & Datos** | Azure OpenAI | Modelos de Lenguaje (GPT-4) y Embeddings |
| | Azure AI Search | Vector Store para la base de conocimientos |
| | Azure Blob Storage | Almacenamiento de los documentos fuente (PDFs) |
| **Frontend** | HTML5, CSS3, JavaScript | Estructura, estilo y lógica de la interfaz |
| | Marked.js | Renderizado de respuestas en formato Markdown |

## 🏗️ Arquitectura y Flujo de Datos

El sistema sigue un flujo de datos claro desde que el usuario envía un mensaje hasta que recibe una respuesta de alta calidad.

<details>
<summary>Haz clic aquí para ver el diagrama de arquitectura (código Mermaid)</summary>

```mermaid
graph TD
    subgraph "🌐 Usuario Final"
        A[📱 Interfaz de Usuario Frontend]
    end

    subgraph "⚙️ Backend (FastAPI)"
        B[API Endpoint: /api/chat]
        C{🤖 Grafo Supervisor (LangGraph)}
    end

    subgraph "🧠 Lógica del Agente Cíclico"
        D[1. Nodo RAG: Generar Respuesta Inicial]
        E[2. Nodo Supervisor: Evaluar Calidad]
        F[3a. Nodo Refinador: Corregir y Mejorar]
        G[3b. Nodo de Búsqueda Web: Enriquecer]
    end

    subgraph "☁️ Servicios de Azure AI"
        H[LLM: Azure OpenAI]
        I[Vector Store: Azure AI Search]
    end

    A -- "POST /api/chat\n{ message: '...' }" --> B
    B -- "Inicia el grafo con la pregunta" --> C
    
    C -- "Comienza el ciclo" --> D
    D -- "Consulta con query reformulada" --> I
    I -- "Retorna documentos relevantes" --> D
    D -- "Pregunta + Contexto" --> H
    H -- "Respuesta inicial" --> D
    D -- "Respuesta generada" --> E

    E -- "Evalúa la respuesta" --> H
    H -- "Decisión: Final, Refinar o Wikipedia" --> E
    
    E -- "Decisión" --> C

    C -- route_decision --> F
    C -- route_decision --> G
    C -- route_decision --> Z[🏁 Fin del Grafo]

    F -- "Respuesta refinada" --> Z
    G -- "Respuesta enriquecida" --> Z

    Z -- "Respuesta final y pulida" --> B
    B -- "JSON: { response: '...' }" --> A

    style A fill:#D6EAF8,stroke:#3498DB
    style B fill:#D1F2EB,stroke:#1ABC9C
    style C fill:#FCF3CF,stroke:#F1C40F
    style H fill:#FDEDEC,stroke:#E74C3C
    style I fill:#FDEDEC,stroke:#E74C3C
```
</details>

*(Aquí se puede insertar una imagen generada a partir del código Mermaid anterior para mayor portabilidad)*
`[Diagrama de Arquitectura]`

### Conceptos Clave de la Arquitectura

Para entender cómo el chatbot logra respuestas coherentes y de alta calidad, es importante conocer tres componentes fundamentales:

#### 1. RAG Contextual y con Memoria
A diferencia de un RAG simple, este sistema tiene **memoria conversacional**.
- **Uso de Memoria:** Cada conversación utiliza una instancia de `ConversationBufferMemory` que almacena las interacciones pasadas.
- **Reformulación de Preguntas:** Antes de buscar en la base de conocimientos, el sistema utiliza un prompt específico (`contextualize_retriever_system_prompt`) para reformular la pregunta del usuario a la luz del historial de la conversación. Por ejemplo, si el usuario pregunta "¿Y sobre las estanterías?", el sistema lo convierte en una pregunta autónoma como "¿Qué tipos de estanterías son mejores para la gestión de inventario en un almacén?". Esto hace que la búsqueda en el vector store sea mucho más precisa y relevante.

#### 2. Agente Supervisor y Grafo de Estados (LangGraph)
Aquí reside la inteligencia principal del chatbot para el control de calidad.
- **Grafo de Estados:** `LangGraph` se utiliza para definir un flujo de trabajo cíclico y condicional, no una simple secuencia lineal. Cada nodo en el grafo representa una acción (llamar al RAG, evaluar, refinar).
- **Agente Supervisor:** Es un LLM con un rol definido: actuar como un supervisor de calidad. Después de que el RAG genera una respuesta, este agente la inspecciona y decide el siguiente paso.
- **Decisiones Estructuradas:** El agente no solo responde, sino que emite una decisión estructurada (usando Pydantic models como `FinalAnswer`, `CorrectAndRefine`, `ComplementWithWikipedia`). Esta decisión determina qué camino tomar en el grafo, permitiendo un proceso de refinamiento iterativo hasta que la respuesta cumple con los estándares de calidad.

#### 3. Gestión de la Memoria Conversacional
- **Aislamiento:** La memoria se gestiona por sesión, lo que garantiza que las conversaciones de diferentes usuarios no se mezclen.
- **Componente Clave:** La memoria es el pilar del "RAG Contextual". Sin ella, el chatbot no podría entender preguntas de seguimiento y cada interacción sería tratada como si fuera la primera vez.

**Flujo detallado:**
1.  **Petición del Usuario:** El usuario escribe un mensaje en el frontend y lo envía. Se realiza una llamada POST al endpoint `/api/chat` del backend FastAPI.
2.  **Inicio del Grafo:** La API recibe la petición e invoca al grafo de LangGraph, pasando la pregunta del usuario.
3.  **Generación RAG:** El primer nodo del grafo (`call_rag_agent`) utiliza Azure AI Search para encontrar los fragmentos de texto más relevantes en la base de conocimientos. Luego, envía estos fragmentos junto con la pregunta original al modelo de Azure OpenAI para generar una respuesta inicial.
4.  **Supervisión y Evaluación:** La respuesta generada por el RAG pasa al `call_supervisor_agent`. Este agente (un LLM con instrucciones específicas) evalúa la calidad de la respuesta.
5.  **Enrutamiento Condicional:** Basado en la evaluación, el supervisor decide una de tres rutas:
    *   **FinalAnswer:** La respuesta es excelente y se envía directamente al final del flujo.
    *   **CorrectAndRefine:** La respuesta es conceptualmente correcta pero necesita mejoras. El supervisor la reescribe para mejorar su claridad y estilo.
    *   **ComplementWithWikipedia:** La respuesta es buena pero incompleta. Se realiza una búsqueda en Wikipedia para obtener más contexto y se combina con la respuesta original.
6.  **Respuesta Final:** La respuesta final, ya sea aprobada, refinada o enriquecida, se devuelve como JSON al frontend.
7.  **Visualización:** El frontend recibe la respuesta, la renderiza desde Markdown a HTML y la muestra en el chat.

## ⚙️ Guía de Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto en tu entorno local.

### Prerrequisitos
- Git
- Python 3.10+
- Una cuenta de Azure con acceso a los servicios mencionados (OpenAI, AI Search, Blob Storage).

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### 2. Configuración del Backend
a. **Crear y activar un entorno virtual:**
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

b. **Instalar dependencias:**
```bash
pip install -r backend/requirements.txt
```

c. **Configurar variables de entorno:**
Crea un archivo llamado `.env` en la raíz del proyecto. Copia el contenido de `.env.example` (si existe) o usa la siguiente plantilla y rellena los valores con tus credenciales de Azure.

```ini
# .env

# Azure OpenAI
AZURE_API_KEY="TU_API_KEY_DE_AZURE_OPENAI"
AZURE_ENDPOINT="https://TU_ENDPOINT.openai.azure.com/"
AZURE_API_VERSION="2024-02-01"
AZURE_LLM_DEPLOYMENT="NOMBRE_DEL_DEPLOYMENT_CHAT"
AZURE_EMBEDDING_DEPLOYMENT="NOMBRE_DEL_DEPLOYMENT_EMBEDDING"

# Azure AI Search
AZURE_COGNITIVE_SEARCH_NAME="NOMBRE_DE_TU_SERVICIO_AI_SEARCH"
AZURE_COGNITIVE_SEARCH_API_KEY="API_KEY_DE_AI_SEARCH"
AZURE_COGNITIVE_SEARCH_INDEX_NAME="NOMBRE_DEL_INDICE"

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT_NAME="NOMBRE_DE_LA_CUENTA_DE_STORAGE"
AZURE_STORAGE_ACCOUNT_API_KEY="API_KEY_DE_LA_CUENTA_DE_STORAGE"
AZURE_STORAGE_ACCOUNT_CONTAINER_NAME="NOMBRE_DEL_CONTENEDOR"
AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX=""

# Turso DB (Opcional, si se usa para logs)
TURSO_AUTH_TOKEN=""
TURSO_DATABASE_URL=""
```

d. **Poblar la Base de Conocimientos:**
Asegúrate de haber subido tus archivos PDF al contenedor de Azure Blob Storage. Luego, puedes ejecutar el script para procesarlos y cargarlos en Azure AI Search. (Este paso podría requerir un script de inicialización).

### 3. Ejecutar la Aplicación

a. **Iniciar el servidor del backend:**
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
La API estará disponible en `http://localhost:8000`.

b. **Iniciar el servidor del frontend:**
Abre otra terminal y ejecuta un servidor web simple desde la carpeta `frontend`.
```bash
# Navega a la carpeta del frontend
cd frontend

# Ejecuta el servidor
python -m http.server 8001
```
La interfaz de usuario estará disponible en `http://localhost:8001`.

## 📖 Uso

1.  Abre tu navegador y ve a `http://localhost:8001`.
2.  Haz clic en "Empezar conversación".
3.  Escribe tus preguntas sobre logística, inventario o temas relacionados en el campo de texto.
4.  Presiona Enter o haz clic en el botón de enviar para recibir una respuesta del Ingenierín AI Assistant.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---
*Creado para potenciar y democratizar el aprendizaje a través de la IA.*