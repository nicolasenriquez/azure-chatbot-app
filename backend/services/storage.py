"""
In-memory storage service for chatbot data
Production deployments should use a proper database
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class MemoryStorageService:
    """In-memory storage implementation"""
    
    def __init__(self):
        self.users: Dict[int, Dict[str, Any]] = {}
        self.conversations: Dict[int, Dict[str, Any]] = {}
        self.messages: Dict[int, Dict[str, Any]] = {}
        
        self.current_user_id = 1
        self.current_conversation_id = 1
        self.current_message_id = 1
        
        # Create default user
        self.users[1] = {
            "id": 1,
            "username": "default_user",
            "created_at": datetime.utcnow()
        }
    
    async def create_conversation(self, title: str, user_id: int) -> Dict[str, Any]:
        """Create a new conversation"""
        conversation_id = self.current_conversation_id
        self.current_conversation_id += 1
        
        now = datetime.utcnow()
        conversation = {
            "id": conversation_id,
            "title": title,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now
        }
        
        self.conversations[conversation_id] = conversation
        logger.info(f"Created conversation {conversation_id}: {title}")
        
        return conversation
    
    async def update_conversation(self, conversation_id: int, updated_at: datetime) -> Optional[Dict[str, Any]]:
        """Update conversation timestamp"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id]["updated_at"] = updated_at
            return self.conversations[conversation_id]
        return None
    
    async def get_user_conversations(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all conversations for a user"""
        conversations = [
            conv for conv in self.conversations.values()
            if conv["user_id"] == user_id
        ]
        
        # Sort by updated_at descending
        conversations.sort(key=lambda x: x["updated_at"], reverse=True)
        
        return conversations
    
    async def create_message(self, conversation_id: int, content: str, is_user: bool) -> Dict[str, Any]:
        """Create a new message"""
        message_id = self.current_message_id
        self.current_message_id += 1
        
        message = {
            "id": message_id,
            "conversation_id": conversation_id,
            "content": content,
            "is_user": is_user,
            "timestamp": datetime.utcnow()
        }
        
        self.messages[message_id] = message
        logger.debug(f"Created message {message_id} in conversation {conversation_id}")
        
        return message
    
    async def get_conversation_messages(self, conversation_id: int) -> List[Dict[str, Any]]:
        """Get all messages for a conversation"""
        messages = [
            msg for msg in self.messages.values()
            if msg["conversation_id"] == conversation_id
        ]
        
        # Sort by timestamp ascending
        messages.sort(key=lambda x: x["timestamp"])
        
        return messages


# Global storage instance
_storage_service = None


def get_storage_service() -> MemoryStorageService:
    """Get storage service singleton"""
    global _storage_service
    if _storage_service is None:
        _storage_service = MemoryStorageService()
    return _storage_service