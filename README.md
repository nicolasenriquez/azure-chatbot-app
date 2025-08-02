# Azure AI Chatbot Agent 🤖

An intelligent chatbot assistant with a Retrieval-Augmented Generation (RAG) pipeline and a supervisor agent, built with FastAPI, LangGraph, and the power of Azure AI services.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-blueviolet?style=for-the-badge)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-orange?style=for-the-badge)](https://python.langchain.com/docs/langgraph/)
[![Azure](https://img.shields.io/badge/Azure-blue?style=for-the-badge&logo=microsoftazure)](https://azure.microsoft.com/)

---

## 🎯 Overview

This project is a complete implementation of an AI chatbot designed for a specific purpose: to serve as an assistant for students of a foundation that trains professionals and small business entrepreneurs. The chatbot specializes in topics of **logistics, inventory management, warehousing, and restocking**.

It uses a **Retrieval-Augmented Generation (RAG)** pattern to base its answers on a knowledge base of PDF documents, ensuring that the information is accurate and relevant. To ensure the quality and consistency of the answers, a **supervisor agent with LangGraph** has been implemented to evaluate, refine, and, if necessary, enrich the answers before delivering them to the user.

## ✨ Key Features

### Backend (FastAPI)
- ✅ **Robust API:** Built with FastAPI, offering high performance and automatic endpoint documentation.
- ✅ **RAG Pipeline:** Uses Azure AI Search as a vector store to retrieve relevant information from documents.
- ✅ **Supervisor Agent (LangGraph):** A state graph that orchestrates a quality control flow:
    - **Evaluation:** Decides if the RAG's response is appropriate.
    - **Refinement:** Corrects and improves the style or clarity of the response.
    - **Enrichment:** Can consult external sources (like Wikipedia) to add additional context.
- ✅ **Native Integration with Azure:** Uses `AzureChatOpenAI` for language models and `AzureOpenAIEmbeddings` for generating embeddings.
- ✅ **Conversation Management:** Maintains chat history to provide contextual responses.
- ✅ **Centralized Configuration:** Manages secrets and configurations through environment variables with Pydantic.

### Frontend (HTML, CSS, JS)
- ✅ **Modern Interface:** *Dark-mode* design with color accents and a professional aesthetic.
- ✅ **Fully Responsive:** Adaptable to desktop, tablet, and mobile devices.
- ✅ **Enhanced User Experience:** "Typing..." indicator, auto-adjusting text area, and smooth animations.
- ✅ **Markdown Rendering:** The chatbot's responses are rendered as Markdown, allowing for text formatting, lists, and more.
- ✅ **PWA Ready:** Includes a Service Worker for basic offline capabilities.

## 🛠️ Tech Stack

| Area          | Technology/Service      | Purpose                                           |
| :------------ | :---------------------- | :------------------------------------------------ |
| **Backend**   | Python, FastAPI, Uvicorn| API creation and web server                       |
|               | LangChain, LangGraph    | Orchestration of the RAG pipeline and agent logic |
| **AI & Data** | Azure OpenAI            | Language Models (GPT-4) and Embeddings            |
|               | Azure AI Search         | Vector Store for the knowledge base               |
|               | Azure Blob Storage      | Storage of source documents (PDFs)                |
| **Frontend**  | HTML5, CSS3, JavaScript | Structure, style, and logic of the interface      |
|               | Marked.js               | Rendering of responses in Markdown format         |

### Key Architecture Concepts

To understand how the chatbot achieves coherent and high-quality responses, it is important to know three fundamental components:

#### 1. Contextual RAG with Memory
Unlike a simple RAG, this system has **conversational memory**.
- **Memory Usage:** Each conversation uses an instance of `ConversationBufferMemory` that stores past interactions.

#### 2. Supervisor Agent and State Graph (LangGraph)
This is where the main intelligence of the chatbot for quality control resides.
- **State Graph:** `LangGraph` is used to define a cyclical and conditional workflow, not a simple linear sequence. Each node in the graph represents an action (calling the RAG, evaluating, refining).
- **Supervisor Agent:** It is an LLM with a defined role: to act as a quality supervisor. After the RAG generates a response, this agent inspects it and decides the next step.
- **Structured Decisions:** The agent not only responds but also issues a structured decision (using Pydantic models like `FinalAnswer`, `CorrectAndRefine`, `ComplementWithWikipedia`). This decision determines which path to take in the graph, allowing for an iterative refinement process until the response meets quality standards.

#### 3. Conversational Memory Management
- **Isolation:** Memory is managed per session, ensuring that conversations from different users do not mix.
- **Key Component:** Memory is the pillar of "Contextual RAG." Without it, the chatbot could not understand follow-up questions, and each interaction would be treated as if it were the first time.

**Detailed Flow:**
1.  **User Request:** The user types a message in the frontend and sends it. A POST call is made to the `/api/chat` endpoint of the FastAPI backend.
2.  **Graph Start:** The API receives the request and invokes the LangGraph graph, passing the user's question.
3.  **RAG Generation:** The first node of the graph (`call_rag_agent`) uses Azure AI Search to find the most relevant text fragments in the knowledge base. Then, it sends these fragments along with the original question to the Azure OpenAI model to generate an initial response.
4.  **Supervision and Evaluation:** The response generated by the RAG passes to the `call_supervisor_agent`. This agent (an LLM with specific instructions) evaluates the quality of the response.
5.  **Conditional Routing:** Based on the evaluation, the supervisor decides on one of three routes:
    *   **FinalAnswer:** The response is excellent and is sent directly to the end of the flow.
    *   **CorrectAndRefine:** The response is conceptually correct but needs improvement. The supervisor rewrites it to improve its clarity and style.
    *   **ComplementWithWikipedia:** The response is good but incomplete. A search is performed on Wikipedia to get more context and is combined with the original response.
6.  **Final Response:** The final response, whether approved, refined, or enriched, is returned as JSON to the frontend.
7.  **Visualization:** The frontend receives the response, renders it from Markdown to HTML, and displays it in the chat.

## ⚙️ Installation and Execution Guide

Follow these steps to get the project up and running in your local environment.

### Prerequisites
- Git
- Python 3.10+
- An Azure account with access to the mentioned services (OpenAI, AI Search, Blob Storage).

### 1. Clone the Repository
```bash
git clone https://github.com/your-user/your-repository.git
cd your-repository
```

### 2. Backend Configuration
a. **Create and activate a virtual environment:**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

b. **Install dependencies:**
```bash
pip install -r backend/requirements.txt
```

c. **Configure environment variables:**
Create a file named `.env` in the root of the project. Copy the content of `.env.example` (if it exists) or use the following template and fill in the values with your Azure credentials.

```ini
# .env

# Azure OpenAI
AZURE_API_KEY="YOUR_AZURE_OPENAI_API_KEY"
AZURE_ENDPOINT="https://YOUR_ENDPOINT.openai.azure.com/"
AZURE_API_VERSION="2024-02-01"
AZURE_LLM_DEPLOYMENT="CHAT_DEPLOYMENT_NAME"
AZURE_EMBEDDING_DEPLOYMENT="EMBEDDING_DEPLOYMENT_NAME"

# Azure AI Search
AZURE_COGNITIVE_SEARCH_NAME="YOUR_AI_SEARCH_SERVICE_NAME"
AZURE_COGNITIVE_SEARCH_API_KEY="AI_SEARCH_API_KEY"
AZURE_COGNITIVE_SEARCH_INDEX_NAME="INDEX_NAME"

# Azure Blob Storage
AZURE_STORAGE_ACCOUNT_NAME="STORAGE_ACCOUNT_NAME"
AZURE_STORAGE_ACCOUNT_API_KEY="STORAGE_ACCOUNT_API_KEY"
AZURE_STORAGE_ACCOUNT_CONTAINER_NAME="CONTAINER_NAME"
AZURE_STORAGE_ACCOUNT_ENDPOINT_SUFFIX=""

# Turso DB (Optional, if used for logs)
TURSO_AUTH_TOKEN=""
TURSO_DATABASE_URL=""
```

d. **Populate the Knowledge Base:**
Make sure you have uploaded your PDF files to the Azure Blob Storage container. Then, you can run the script to process them and load them into Azure AI Search. (This step might require an initialization script).

### 3. Run the Application

a. **Start the backend server:**
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at `http://localhost:8000`.

b. **Start the frontend server:**
Open another terminal and run a simple web server from the `frontend` folder.
```bash
# Navigate to the frontend folder
cd frontend

# Run the server
python -m http.server 8001
```
The user interface will be available at `http://localhost:8001`.

## 📖 Usage

1.  Open your browser and go to `http://localhost:8001`.
2.  Click on "Start conversation".
3.  Type your questions about logistics, inventory, or related topics in the text field.
4.  Press Enter or click the send button to receive a response from the Ingenierín AI Assistant.

## 📄 License

This project is under the MIT License. See the `LICENSE` file for more details.

---
*Created to empower and democratize learning through AI.*
