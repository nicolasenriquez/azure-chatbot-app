import { useState, useCallback } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { chatAPI } from "@/lib/api";

interface APIMessage {  
  id: number;  
  content: string;  
  is_user: boolean;  
  timestamp: string;  
  conversation_id?: number; // Hacer que conversation_id sea opcional  
} 

export interface ChatMessage {  
  id: number;  
  content: string;  
  isUser: boolean;  
  timestamp: Date;  
  conversationId: number; // Asegúrate de usar `conversationId` aquí  
  conversation_id?: number; // Agrega esta propiedad opcional para evitar conflictos  
}

export interface Conversation {
  id: number;
  title: string;
  updatedAt: Date;
}

export function useChat() {
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const queryClient = useQueryClient();

  // Fetch conversations
  const {
    data: conversations = [],
    isLoading: conversationsLoading,
    error: conversationsError,
  } = useQuery({
    queryKey: ["/api/conversations"],
    queryFn: async () => {
      const response = await chatAPI.getConversations();
      if (!response.success) {
        throw new Error(response.error || "Failed to fetch conversations");
      }
      return response.data?.map(conv => ({
        ...conv,
        updatedAt: new Date(conv.updated_at),
      })) || [];
    },
  });

  // Fetch messages for current conversation
  const {
    data: messages = [],
    isLoading: messagesLoading,
    error: messagesError,
  } = useQuery({
    queryKey: ["/api/conversations", currentConversationId, "messages"],
    queryFn: async () => {
      if (!currentConversationId) return [];
      const response = await chatAPI.getConversationMessages(currentConversationId);
      if (!response.success) {
        throw new Error(response.error || "Failed to fetch messages");
      }
      return response.data?.map(msg => ({
        ...msg,
        isUser: msg.is_user, // Mapea `is_user` a `isUser`
        conversationId: msg.conversation_id ?? null, // Si `conversation_id` es undefined, asigna null
        timestamp: new Date(msg.timestamp), // Convierte el timestamp a un objeto Date
      })) || [];
    },
    enabled: !!currentConversationId,
  });

  // Send message mutation
  const sendMessageMutation = useMutation({
    mutationFn: async ({ message, conversationId }: { message: string; conversationId?: number }) => {
      const response = await chatAPI.sendMessage(message, conversationId);
      if (!response.success) {
        throw new Error(response.error || "Failed to send message");
      }
      return {  
        ...response.data,  
        conversationId: response.data?.conversation_id ?? null, // Usa encadenamiento opcional  
      }; 
    },
    onSuccess: (data) => {
      // Update current conversation ID if it's a new conversation
      if (!currentConversationId) {
        setCurrentConversationId(data.conversationId);
      }
      
      // Invalidate and refetch conversations and messages
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      queryClient.invalidateQueries({ 
        queryKey: ["/api/conversations", data.conversationId, "messages"] 
      });
    },
  });

  const sendMessage = useCallback((message: string) => {
    sendMessageMutation.mutate({ message, conversationId: currentConversationId || undefined });
  }, [currentConversationId, sendMessageMutation]);

  const startNewConversation = useCallback(() => {
    setCurrentConversationId(null);
  }, []);

  const selectConversation = useCallback((conversationId: number) => {
    setCurrentConversationId(conversationId);
  }, []);

  return {
    // Data
    conversations,
    messages,
    currentConversationId,
    
    // Loading states
    conversationsLoading,
    messagesLoading,
    isSendingMessage: sendMessageMutation.isPending,
    
    // Error states
    conversationsError,
    messagesError,
    sendError: sendMessageMutation.error,
    
    // Actions
    sendMessage,
    startNewConversation,
    selectConversation,
  };
}
