"""
Azure AI Services integration
Handles OpenAI and Azure AI Search operations
"""

import json
from typing import List, Dict, Any, Optional
import httpx
from config.settings import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)


class AzureOpenAIService:
    """Azure OpenAI API integration"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def chat_completion(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate chat completion using Azure OpenAI"""
        
        try:
            url = f"{self.settings.azure_openai_endpoint}/openai/deployments/{self.settings.azure_openai_deployment_name}/chat/completions"
            
            # Build messages array
            messages = [
                {
                    "role": "system",
                    "content": f"You are a helpful AI assistant. You provide accurate, concise, and helpful responses. {f'Context: {context}' if context else ''}"
                }
            ]
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # API request
            response = await self.client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "api-key": self.settings.azure_openai_api_key,
                },
                params={"api-version": self.settings.azure_openai_api_version},
                json={
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "frequency_penalty": 0,
                    "presence_penalty": 0,
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Azure OpenAI API error: {response.status_code} - {response.text}")
                raise Exception(f"Azure OpenAI API error: {response.status_code}")
            
            data = response.json()
            
            return {
                "response": data["choices"][0]["message"]["content"],
                "usage": {
                    "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": data.get("usage", {}).get("completion_tokens", 0),
                    "total_tokens": data.get("usage", {}).get("total_tokens", 0),
                }
            }
            
        except Exception as e:
            logger.error(f"Error in Azure OpenAI chat completion: {e}")
            raise Exception("Failed to generate AI response")
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class AzureSearchService:
    """Azure AI Search integration"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_knowledge_base(self, query: str, top_k: int = 5) -> List[str]:
        """Search knowledge base using Azure AI Search"""
        
        try:
            if not self.settings.azure_search_endpoint or not self.settings.azure_search_api_key:
                logger.warning("Azure Search not configured, skipping knowledge base search")
                return []
            
            url = f"{self.settings.azure_search_endpoint}/indexes/{self.settings.azure_search_index_name}/docs/search"
            
            response = await self.client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "api-key": self.settings.azure_search_api_key,
                },
                params={"api-version": "2023-11-01"},
                json={
                    "search": query,
                    "top": top_k,
                    "select": "content",
                    "searchMode": "any",
                    "queryType": "semantic",
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Azure Search API error: {response.status_code}")
                return []
            
            data = response.json()
            return [item.get("content", "") for item in data.get("value", [])]
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global service instances
_openai_service = None
_search_service = None


def get_openai_service() -> AzureOpenAIService:
    """Get Azure OpenAI service singleton"""
    global _openai_service
    if _openai_service is None:
        _openai_service = AzureOpenAIService()
    return _openai_service


def get_search_service() -> AzureSearchService:
    """Get Azure Search service singleton"""
    global _search_service
    if _search_service is None:
        _search_service = AzureSearchService()
    return _search_service