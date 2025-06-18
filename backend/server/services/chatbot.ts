import { storage } from '../storage.js';
import { azureAIService } from './azure-ai.js';
import { logger } from '../utils/logger.js';
import type { ChatRequest, Message } from '@shared/schema';

export interface ChatbotResponse {
  message: string;
  conversationId: number;
  messageId: number;
  timestamp: Date;
}

export class ChatbotService {
  async processMessage(request: ChatRequest, userId: number = 1): Promise<ChatbotResponse> {
    try {
      let conversationId = request.conversationId;
      
      // Create new conversation if none provided
      if (!conversationId) {
        const conversation = await storage.createConversation({
          title: this.generateConversationTitle(request.message),
          userId,
        });
        conversationId = conversation.id;
      }

      // Store user message
      const userMessage = await storage.createMessage({
        conversationId,
        content: request.message,
        isUser: true,
      });

      // Get conversation history for context
      const conversationHistory = await this.getConversationHistory(conversationId);
      
      // Search knowledge base for relevant context
      const contextResults = await azureAIService.searchKnowledgeBase(request.message);
      const context = contextResults.length > 0 ? contextResults.join('\n\n') : undefined;

      // Generate AI response
      const aiResponse = await azureAIService.chatCompletion({
        message: request.message,
        conversationHistory,
        context,
      });

      // Store AI response
      const botMessage = await storage.createMessage({
        conversationId,
        content: aiResponse.response,
        isUser: false,
      });

      // Update conversation timestamp
      await storage.updateConversation(conversationId, {
        updatedAt: new Date(),
      });

      logger.info(`Processed message for conversation ${conversationId}`, {
        userId,
        messageLength: request.message.length,
        responseLength: aiResponse.response.length,
      });

      return {
        message: aiResponse.response,
        conversationId,
        messageId: botMessage.id,
        timestamp: botMessage.timestamp,
      };
    } catch (error) {
      logger.error('Error processing chatbot message:', error);
      throw new Error('Failed to process message');
    }
  }

  private async getConversationHistory(conversationId: number): Promise<Array<{ role: 'user' | 'assistant'; content: string }>> {
    const messages = await storage.getConversationMessages(conversationId);
    
    // Get last 10 messages for context (excluding the current message)
    return messages
      .slice(-10)
      .map((msg) => ({
        role: msg.isUser ? 'user' as const : 'assistant' as const,
        content: msg.content,
      }));
  }

  private generateConversationTitle(message: string): string {
    // Generate a title from the first message
    const words = message.split(' ').slice(0, 6);
    let title = words.join(' ');
    
    if (message.length > title.length) {
      title += '...';
    }
    
    return title || 'New Conversation';
  }

  async getConversations(userId: number = 1): Promise<Array<{ id: number; title: string; updatedAt: Date }>> {
    const conversations = await storage.getUserConversations(userId);
    return conversations
      .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())
      .map(conv => ({
        id: conv.id,
        title: conv.title,
        updatedAt: conv.updatedAt,
      }));
  }

  async getConversationMessages(conversationId: number): Promise<Message[]> {
    return await storage.getConversationMessages(conversationId);
  }
}

export const chatbotService = new ChatbotService();
