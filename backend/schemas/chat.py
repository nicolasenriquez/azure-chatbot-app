"""
Pydantic schemas for chat-related operations
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """Request model for sending a chat message"""
    message: str = Field(..., min_length=1, max_length=10000, description="The chat message content")
    conversation_id: Optional[int] = Field(None, description="ID of the conversation (optional for new conversations)")


class ChatMessageResponse(BaseModel):
    """Response model for chat message"""
    message: str
    conversation_id: int
    message_id: int
    timestamp: datetime


class ConversationResponse(BaseModel):
    """Response model for conversation"""
    id: int
    title: str
    updated_at: datetime


class MessageResponse(BaseModel):
    """Response model for individual message"""
    id: int
    content: str
    is_user: bool
    timestamp: datetime


class APIResponse(BaseModel):
    """Generic API response wrapper"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"