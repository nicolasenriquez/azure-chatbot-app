"""
Router for the chatbot functionality
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.agents.agent import process_user_question

router = APIRouter()


class ChatRequest(BaseModel):
    """Model representing a user message request"""

    message: str


class ChatResponse(BaseModel):
    """Model containing the chatbot's response"""

    response: str


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint for interacting with the chatbott.
    Recieves a user message and returns the chatbot's response.
    """
    try:
        chatbot_response = await process_user_question(request.message)
        return ChatResponse(response=chatbot_response)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {e}"
        )
