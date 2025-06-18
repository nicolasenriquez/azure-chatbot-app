import type { Express } from "express";
import { createServer, type Server } from "http";
import { chatbotService } from "./services/chatbot.js";
import { chatRequestSchema } from "@shared/schema";
import { logger } from "./utils/logger.js";
import { validateSettings } from "./config/settings.js";

export async function registerRoutes(app: Express): Promise<Server> {
  // Validate environment variables on startup
  validateSettings();

  // Health check endpoint
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  // Chat endpoint
  app.post("/api/chat", async (req, res) => {
    try {
      const validatedData = chatRequestSchema.parse(req.body);
      
      logger.info("Processing chat request", {
        messageLength: validatedData.message.length,
        conversationId: validatedData.conversationId,
      });

      const response = await chatbotService.processMessage(validatedData);
      
      res.json({
        success: true,
        data: response,
      });
    } catch (error) {
      logger.error("Error in chat endpoint:", error);
      
      if (error instanceof Error) {
        res.status(400).json({
          success: false,
          error: error.message,
        });
      } else {
        res.status(500).json({
          success: false,
          error: "Internal server error",
        });
      }
    }
  });

  // Get conversations endpoint
  app.get("/api/conversations", async (req, res) => {
    try {
      const conversations = await chatbotService.getConversations();
      
      res.json({
        success: true,
        data: conversations,
      });
    } catch (error) {
      logger.error("Error fetching conversations:", error);
      res.status(500).json({
        success: false,
        error: "Failed to fetch conversations",
      });
    }
  });

  // Get conversation messages endpoint
  app.get("/api/conversations/:id/messages", async (req, res) => {
    try {
      const conversationId = parseInt(req.params.id);
      
      if (isNaN(conversationId)) {
        return res.status(400).json({
          success: false,
          error: "Invalid conversation ID",
        });
      }

      const messages = await chatbotService.getConversationMessages(conversationId);
      
      res.json({
        success: true,
        data: messages,
      });
    } catch (error) {
      logger.error("Error fetching conversation messages:", error);
      res.status(500).json({
        success: false,
        error: "Failed to fetch messages",
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
