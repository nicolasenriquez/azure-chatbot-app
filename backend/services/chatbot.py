"""
Chatbot service - Main business logic for chat operations
"""

from datetime import datetime
from typing import Dict, List, Any
from services.azure_ai import get_openai_service, get_search_service
from services.storage import get_storage_service
from schemas.chat import ChatMessageRequest, ChatMessageResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class ChatbotService:
    """Main chatbot service handling message processing"""
    
    def __init__(self):
        self.openai_service = get_openai_service()
        self.search_service = get_search_service()
        self.storage = get_storage_service()
    
    async def process_message(self, request: ChatMessageRequest, user_id: int = 1) -> ChatMessageResponse:
        """Process a chat message and generate AI response"""
        
        try:
            conversation_id = request.conversation_id
            
            # Create new conversation if none provided
            if not conversation_id:
                conversation = await self.storage.create_conversation(
                    title=self._generate_conversation_title(request.message),
                    user_id=user_id
                )
                conversation_id = conversation["id"]
            
            # Store user message
            user_message = await self.storage.create_message(
                conversation_id=conversation_id,
                content=request.message,
                is_user=True
            )
            
            # Get conversation history for context
            conversation_history = await self._get_conversation_history(conversation_id)
            
            # Search knowledge base for relevant context
            context_results = await self.search_service.search_knowledge_base(request.message)
            context = "\n\n".join(context_results) if context_results else None
            
            # Generate AI response
            ai_response = await self.openai_service.chat_completion(
                message=request.message,
                conversation_history=conversation_history,
                context=context
            )
            
            # Store AI response
            bot_message = await self.storage.create_message(
                conversation_id=conversation_id,
                content=ai_response["response"],
                is_user=False
            )
            
            # Update conversation timestamp
            await self.storage.update_conversation(
                conversation_id=conversation_id,
                updated_at=datetime.utcnow()
            )
            
            logger.info(f"Processed message for conversation {conversation_id}")
            
            return ChatMessageResponse(
                message=ai_response["response"],
                conversation_id=conversation_id,
                message_id=bot_message["id"],
                timestamp=bot_message["timestamp"]
            )
            
        except Exception as e:
            logger.error(f"Error processing chatbot message: {e}")
            raise Exception("Failed to process message")
    
    async def get_conversations(self, user_id: int = 1) -> List[Dict[str, Any]]:
        """Get user conversations"""
        return await self.storage.get_user_conversations(user_id)
    
    async def get_conversation_messages(self, conversation_id: int) -> List[Dict[str, Any]]:
        """Get messages for a conversation"""
        return await self.storage.get_conversation_messages(conversation_id)
    
    async def _get_conversation_history(self, conversation_id: int) -> List[Dict[str, str]]:
        """Get conversation history for AI context"""
        messages = await self.storage.get_conversation_messages(conversation_id)
        
        # Get last 10 messages for context
        return [
            {
                "role": "user" if msg["is_user"] else "assistant",
                "content": msg["content"]
            }
            for msg in messages[-10:]
        ]
    
    def _generate_conversation_title(self, message: str) -> str:
        """Generate a title from the first message"""
        words = message.split()[:6]
        title = " ".join(words)
        
        if len(message) > len(title):
            title += "..."
        
        return title or "New Conversation"


# Global service instance
_chatbot_service = None


def get_chatbot_service() -> ChatbotService:
    """Get chatbot service singleton"""
    global _chatbot_service
    if _chatbot_service is None:
        _chatbot_service = ChatbotService()
    return _chatbot_service