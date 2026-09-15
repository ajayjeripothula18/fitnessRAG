import React from 'react';
import ChatContainer from '../components/chat/ChatContainer';

/**
 * ChatPage — full-viewport AI Coach chat screen.
 * The ChatContainer component handles all message state and API calls.
 */
const ChatPage: React.FC = () => {
  return (
    <div className="chat-page h-full w-full">
      <h1 className="sr-only">AI Fitness Coach Chat</h1>
      <ChatContainer />
    </div>
  );
};

export default ChatPage;
