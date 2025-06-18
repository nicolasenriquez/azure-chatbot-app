import { Plus, MessageSquare, Settings, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { Conversation } from "@/hooks/useChat";

interface ChatSidebarProps {
  conversations: Conversation[];
  currentConversationId: number | null;
  onSelectConversation: (id: number) => void;
  onNewConversation: () => void;
  loading?: boolean;
}

export function ChatSidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  loading = false,
}: ChatSidebarProps) {
  const formatDate = (date: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffHours < 1) return "Just now";
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="w-80 chat-sidebar border-r flex flex-col h-full">
      {/* Sidebar Header */}
      <div className="p-6 border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-green-500 rounded-xl flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-200">AI Assistant</h1>
            <p className="text-sm text-gray-400">Azure-powered chatbot</p>
          </div>
        </div>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-hidden">
        <ScrollArea className="h-full p-4">
          <div className="space-y-2">
            <div className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-3">
              Recent Conversations
            </div>

            {loading ? (
              <div className="space-y-2">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="p-3 rounded-lg bg-gray-700/50 animate-pulse">
                    <div className="h-4 bg-gray-600 rounded mb-2"></div>
                    <div className="h-3 bg-gray-600 rounded w-2/3"></div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-2">
                {conversations.map((conversation) => (
                  <button
                    key={conversation.id}
                    onClick={() => onSelectConversation(conversation.id)}
                    className={`w-full p-3 rounded-lg text-left transition-colors ${
                      currentConversationId === conversation.id
                        ? "bg-purple-600/20 border border-purple-500/30"
                        : "hover:bg-gray-700/30"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-200 truncate">
                        {conversation.title}
                      </span>
                      <span className="text-xs text-gray-400 ml-2 flex-shrink-0">
                        {formatDate(conversation.updatedAt)}
                      </span>
                    </div>
                  </button>
                ))}
                
                {conversations.length === 0 && (
                  <div className="text-center py-8">
                    <MessageSquare className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                    <p className="text-gray-400 text-sm">No conversations yet</p>
                    <p className="text-gray-500 text-xs mt-1">Start a new chat to get started</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </ScrollArea>
      </div>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-gray-700 space-y-2">
        <Button
          onClick={onNewConversation}
          className="w-full flex items-center justify-center space-x-2 p-3 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded-lg transition-colors"
          variant="ghost"
        >
          <Plus className="w-4 h-4 text-green-400" />
          <span className="text-sm font-medium">New Conversation</span>
        </Button>
        
        <div className="flex space-x-2">
          <Button
            variant="ghost"
            size="sm"
            className="flex-1 text-gray-400 hover:text-gray-200 hover:bg-gray-700"
          >
            <Settings className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="flex-1 text-gray-400 hover:text-gray-200 hover:bg-gray-700"
          >
            <Download className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
