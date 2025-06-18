import { Bot, User, ThumbsUp, ThumbsDown, Copy, Check } from "lucide-react";
import { useState } from "react";
import type { ChatMessage } from "@/hooks/useChat";

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error("Failed to copy text:", error);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("en-US", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  };

  if (message.isUser) {
    return (
      <div className="flex justify-end animate-fade-in">
        <div className="max-w-lg">
          <div className="chat-message-user rounded-2xl rounded-br-md p-4 shadow-lg">
            <p className="text-white leading-relaxed">{message.content}</p>
          </div>
          <div className="flex items-center justify-end mt-2 space-x-2">
            <span className="text-xs text-gray-400">{formatTime(message.timestamp)}</span>
            <Check className="w-3 h-3 text-green-400" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start animate-fade-in">
      <div className="max-w-lg">
        <div className="flex items-center space-x-2 mb-2">
          <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-green-500 rounded-full flex items-center justify-center">
            <Bot className="w-3 h-3 text-white" />
          </div>
          <span className="text-sm font-medium text-gray-200">AI Assistant</span>
        </div>
        <div className="chat-message-bot border rounded-2xl rounded-bl-md p-4 shadow-lg">
          <p className="leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>
        <div className="flex items-center mt-2 space-x-2">
          <span className="text-xs text-gray-400">{formatTime(message.timestamp)}</span>
          <div className="flex items-center space-x-1">
            <button className="text-gray-400 hover:text-green-400 transition-colors p-1">
              <ThumbsUp className="w-3 h-3" />
            </button>
            <button className="text-gray-400 hover:text-red-400 transition-colors p-1">
              <ThumbsDown className="w-3 h-3" />
            </button>
            <button
              onClick={copyToClipboard}
              className="text-gray-400 hover:text-purple-400 transition-colors p-1"
            >
              {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
