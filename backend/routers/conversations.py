"""
Conversations router - Handles conversation management
"""

from fastapi import APIRouter, HTTPException
from typing import List
from schemas.chat import ConversationResponse, MessageResponse, APIResponse
from services.chatbot import get_chatbot_service
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/conversations", response_model=APIResponse)
async def get_conversations():
    """Get all conversations for the user"""
    try:
        chatbot_service = get_chatbot_service()
        conversations = await chatbot_service.get_conversations()
        
        return APIResponse(
            success=True,
            data=[
                {
                    "id": conv["id"],
                    "title": conv["title"],
                    "updated_at": conv["updated_at"].isoformat()
                }
                for conv in conversations
            ]
        )
        
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Failed to fetch conversations"}
        )


@router.get("/conversations/{conversation_id}/messages", response_model=APIResponse)
async def get_conversation_messages(conversation_id: int):
    """Get all messages for a specific conversation"""
    try:
        chatbot_service = get_chatbot_service()
        messages = await chatbot_service.get_conversation_messages(conversation_id)
        
        return APIResponse(
            success=True,
            data=[
                {
                    "id": msg["id"],
                    "content": msg["content"],
                    "is_user": msg["is_user"],
                    "timestamp": msg["timestamp"].isoformat()
                }
                for msg in messages
            ]
        )
        
    except Exception as e:
        logger.error(f"Error fetching conversation messages: {e}")
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Failed to fetch messages"}
        )