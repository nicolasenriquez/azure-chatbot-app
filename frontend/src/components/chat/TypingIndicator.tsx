import { Bot } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="flex justify-start animate-fade-in">
      <div className="max-w-lg">
        <div className="flex items-center space-x-2 mb-2">
          <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-green-500 rounded-full flex items-center justify-center">
            <Bot className="w-3 h-3 text-white" />
          </div>
          <span className="text-sm font-medium text-gray-200">AI Assistant</span>
        </div>
        <div className="bg-gray-800 border border-gray-700 rounded-2xl rounded-bl-md p-4 shadow-lg">
          <div className="flex items-center space-x-2">
            <div className="typing-indicator">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
            <span className="text-sm text-gray-400">Thinking...</span>
          </div>
        </div>
      </div>
    </div>
  );
}
