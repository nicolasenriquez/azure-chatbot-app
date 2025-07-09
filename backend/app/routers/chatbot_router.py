from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.agents.agent import process_user_question

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint para interactuar con el chatbot.
    Recibe un mensaje del usuario y devuelve la respuesta del chatbot.
    """
    try:
        chatbot_response = await process_user_question(request.message)
        return ChatResponse(response=chatbot_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")
