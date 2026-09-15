import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Send, Bot, Zap, Dumbbell } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { chatService } from '../../services/chatService';

import { ChatMessage, type MessageData } from './ChatMessage';
// ─── Typing Indicator ─────────────────────────────────────────────────────────
const TypingIndicator: React.FC = () => (
  <div className="chat-message assistant-message" role="status" aria-label="Assistant is typing">
    <div className="avatar avatar-sm avatar-gradient" aria-hidden="true">
      <Bot size={14} />
    </div>
    <div className="typing-indicator" aria-live="polite">
      <span className="typing-dot" />
      <span className="typing-dot" />
      <span className="typing-dot" />
    </div>
  </div>
);


// ─── Empty Chat State ──────────────────────────────────────────────────────────
const EmptyChat: React.FC = () => (
  <div className="empty-state">
    <div className="empty-state-icon">
      <Zap size={28} />
    </div>
    <h2 className="empty-state-title">Your AI Fitness Coach</h2>
    <p className="empty-state-desc">
      Ask me anything about workouts, nutrition, form tips, or to build a personalised training plan.
    </p>
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--sp-2)', justifyContent: 'center', marginTop: 'var(--sp-2)' }}>
      {[
        'Build me a 4-day workout plan',
        'How do I improve my squat form?',
        'What should I eat for muscle gain?',
        'Create a beginner running program',
      ].map((prompt) => (
        <button
          key={prompt}
          className="btn btn-secondary btn-sm"
          onClick={() => {
            const event = new CustomEvent('chat:prefill', { detail: prompt });
            window.dispatchEvent(event);
          }}
          id={`quick-prompt-${prompt.replace(/\s+/g, '-').toLowerCase().slice(0, 20)}`}
        >
          <Dumbbell size={12} aria-hidden="true" />
          {prompt}
        </button>
      ))}
    </div>
  </div>
);

// ─── Chat Container ────────────────────────────────────────────────────────────
const ChatContainer: React.FC = () => {
  const { user } = useAuthStore();
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const userInitial = (user?.full_name || user?.email || 'U')[0].toUpperCase();

  // ── Scroll to bottom on new messages ──────────────────────────────────────
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // ── Prefill from quick prompts ─────────────────────────────────────────────
  useEffect(() => {
    const handler = (e: Event) => {
      const text = (e as CustomEvent<string>).detail;
      setInput(text);
      textareaRef.current?.focus();
    };
    window.addEventListener('chat:prefill', handler);
    return () => window.removeEventListener('chat:prefill', handler);
  }, []);

  // ── Auto-resize textarea ───────────────────────────────────────────────────
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
  };

  // ── Send message ───────────────────────────────────────────────────────────
  const sendMessage = useCallback(async () => {
    const text = input.trim();
    if (!text || isTyping) return;

    const userMsg: MessageData = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    try {
      const result = await chatService.sendMessage({
        message: text,
        conversation_id: conversationId,
      });

      // Persist conversation_id so the backend threads messages together
      if (!conversationId) setConversationId(result.conversation_id);

      const assistantMsg: MessageData = {
        id: result.response.id,
        role: 'assistant',
        content: result.response.content,
        timestamp: new Date(result.response.created_at),
        citations: result.response.citations,
        safety_tier: result.safety_tier,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      const errMsg: MessageData = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content:
          'I could not reach the AI service right now. Please check that the backend is running and try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsTyping(false);
    }
  }, [input, isTyping, conversationId]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <section className="chat-layout" aria-label="AI Coach Chat">
      {/* Messages */}
      <div
        className="chat-messages"
        role="log"
        aria-label="Chat messages"
        aria-live="polite"
        aria-relevant="additions"
      >
        {messages.length === 0 ? (
          <EmptyChat />
        ) : (
          messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} userInitial={userInitial} />
          ))
        )}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} aria-hidden="true" />
      </div>

      {/* Input area */}
      <div className="chat-input-area">
        <div className="chat-input-wrapper" role="form" aria-label="Send a message">
          <textarea
            ref={textareaRef}
            id="chat-input"
            className="chat-textarea"
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask your AI fitness coach anything… (Shift+Enter for new line)"
            rows={1}
            aria-label="Message input"
            aria-multiline="true"
            disabled={isTyping}
          />
          <button
            className="chat-send-btn"
            onClick={sendMessage}
            disabled={!input.trim() || isTyping}
            aria-label="Send message"
            id="chat-send-btn"
            type="button"
          >
            {isTyping ? (
              <span className="btn-spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
            ) : (
              <Send size={16} aria-hidden="true" />
            )}
          </button>
        </div>
        <p
          style={{ textAlign: 'center', marginTop: 'var(--sp-2)', fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}
          aria-live="polite"
        >
          AI-generated content. Always consult a professional for medical or injury-related advice.
        </p>
      </div>
    </section>
  );
};

export default ChatContainer;
