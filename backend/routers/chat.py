"""
Chat router - Handles chat message operations
"""

from fastapi import APIRouter, HTTPException
from schemas.chat import ChatMessageRequest, ChatMessageResponse, APIResponse
from services.chatbot import get_chatbot_service
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/chat", response_model=APIResponse)
async def send_message(request: ChatMessageRequest):
    """Send a chat message and get AI response"""
    try:
        chatbot_service = get_chatbot_service()
        response = await chatbot_service.process_message(request)
        
        return APIResponse(
            success=True,
            data={
                "message": response.message,
                "conversation_id": response.conversation_id,
                "message_id": response.message_id,
                "timestamp": response.timestamp.isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Failed to process message"}
        )