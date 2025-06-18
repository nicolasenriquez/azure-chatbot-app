import { settings } from '../config/settings.js';
import { logger } from '../utils/logger.js';

export interface ChatCompletionRequest {
  message: string;
  conversationHistory?: Array<{ role: 'user' | 'assistant'; content: string }>;
  context?: string;
}

export interface ChatCompletionResponse {
  response: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}

export class AzureAIService {
  private openaiEndpoint: string;
  private openaiApiKey: string;
  private deploymentName: string;
  private apiVersion: string;

  constructor() {
    this.openaiEndpoint = settings.azureOpenaiEndpoint;
    this.openaiApiKey = settings.azureOpenaiApiKey;
    this.deploymentName = settings.azureOpenaiDeploymentName;
    this.apiVersion = settings.azureOpenaiApiVersion;
  }

  async chatCompletion(request: ChatCompletionRequest): Promise<ChatCompletionResponse> {
    try {
      const url = `${this.openaiEndpoint}/openai/deployments/${this.deploymentName}/chat/completions?api-version=${this.apiVersion}`;
      
      const messages = [
        {
          role: 'system',
          content: `You are a helpful AI assistant. You provide accurate, concise, and helpful responses. ${request.context ? `Context: ${request.context}` : ''}`
        },
        ...(request.conversationHistory || []),
        {
          role: 'user',
          content: request.message
        }
      ];

      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'api-key': this.openaiApiKey,
        },
        body: JSON.stringify({
          messages,
          max_tokens: 1000,
          temperature: 0.7,
          top_p: 0.95,
          frequency_penalty: 0,
          presence_penalty: 0,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        logger.error(`Azure OpenAI API error: ${response.status} - ${errorText}`);
        throw new Error(`Azure OpenAI API error: ${response.status}`);
      }

      const data = await response.json();
      
      return {
        response: data.choices[0]?.message?.content || 'I apologize, but I could not generate a response.',
        usage: {
          promptTokens: data.usage?.prompt_tokens || 0,
          completionTokens: data.usage?.completion_tokens || 0,
          totalTokens: data.usage?.total_tokens || 0,
        }
      };
    } catch (error) {
      logger.error('Error in Azure AI chat completion:', error);
      throw new Error('Failed to generate AI response');
    }
  }

  async searchKnowledgeBase(query: string): Promise<string[]> {
    try {
      if (!settings.azureSearchEndpoint || !settings.azureSearchApiKey) {
        logger.warn('Azure Search not configured, skipping knowledge base search');
        return [];
      }

      const url = `${settings.azureSearchEndpoint}/indexes/${settings.azureSearchIndexName}/docs/search?api-version=2023-11-01`;
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'api-key': settings.azureSearchApiKey,
        },
        body: JSON.stringify({
          search: query,
          top: 5,
          select: 'content',
          searchMode: 'any',
          queryType: 'semantic',
        }),
      });

      if (!response.ok) {
        logger.error(`Azure Search API error: ${response.status}`);
        return [];
      }

      const data = await response.json();
      return data.value?.map((item: any) => item.content) || [];
    } catch (error) {
      logger.error('Error searching knowledge base:', error);
      return [];
    }
  }
}

export const azureAIService = new AzureAIService();
