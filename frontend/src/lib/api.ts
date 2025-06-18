const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ChatResponse {
  success: boolean;
  data?: {
    message: string;
    conversation_id: number;
    message_id: number;
    timestamp: string;
  };
  error?: string;
}

export interface ConversationsResponse {
  success: boolean;
  data?: Array<{
    id: number;
    title: string;
    updated_at: string;
  }>;
  error?: string;
}

export interface MessagesResponse {
  success: boolean;
  data?: Array<{
    id: number;
    content: string;
    is_user: boolean;
    timestamp: string;
  }>;
  error?: string;
}

async function apiRequest(method: string, endpoint: string, body?: any) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response;
}

export const chatAPI = {
  sendMessage: async (message: string, conversation_id?: number): Promise<ChatResponse> => {
    const response = await apiRequest("POST", "/api/chat", {
      message,
      conversation_id,
    });
    return await response.json();
  },

  getConversations: async (): Promise<ConversationsResponse> => {
    const response = await apiRequest("GET", "/api/conversations");
    return await response.json();
  },

  getConversationMessages: async (conversationId: number): Promise<MessagesResponse> => {
    const response = await apiRequest("GET", `/api/conversations/${conversationId}/messages`);
    return await response.json();
  },

  checkHealth: async (): Promise<{ status: string; timestamp: string }> => {
    const response = await apiRequest("GET", "/api/health");
    return await response.json();
  },
};