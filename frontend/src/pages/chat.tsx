import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { useChat } from "@/hooks/useChat";

export default function Chat() {
  const {
    conversations,
    currentConversationId,
    conversationsLoading,
    selectConversation,
    startNewConversation,
  } = useChat();

  return (
    <div className="min-h-screen chat-container flex">
      <ChatSidebar
        conversations={conversations}
        currentConversationId={currentConversationId}
        onSelectConversation={selectConversation}
        onNewConversation={startNewConversation}
        loading={conversationsLoading}
      />
      <ChatInterface />
    </div>
  );
}
