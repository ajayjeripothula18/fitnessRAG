import React from 'react';
import { Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Citation } from '../../services/chatService';

// ─── Types ────────────────────────────────────────────────────────────────────
export type { Citation };

export interface MessageData {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: Citation[];
  safety_tier?: string;
}

export interface ChatMessageProps {
  message: MessageData;
  userInitial: string;
}

import { CitationBadge } from './CitationBadge';
import { ShieldAlert } from 'lucide-react';

// ─── Chat Message ─────────────────────────────────────────────────────────────
export const ChatMessage: React.FC<ChatMessageProps> = ({ message, userInitial }) => {
  const isUser = message.role === 'user';
  const timeStr = message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <article
      className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}
      aria-label={`${isUser ? 'You' : 'AI Coach'} at ${timeStr}`}
    >
      <div
        className={`avatar avatar-sm ${isUser ? 'avatar-gradient' : ''}`}
        style={!isUser ? { background: 'var(--color-surface-variant)', border: '1px solid var(--color-outline-variant)', color: 'var(--color-primary)' } : {}}
        aria-hidden="true"
      >
        {isUser ? userInitial : <Bot size={14} />}
      </div>
      <div className="flex-1 max-w-[calc(100%-40px)]">
        <div className={`message-bubble ${isUser ? 'text-white' : 'text-[var(--color-on-surface)]'}`}>
          {isUser ? (
            <p className="whitespace-pre-wrap m-0">{message.content}</p>
          ) : (
            <div className="markdown-body prose prose-sm max-w-none dark:prose-invert">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>
          )}
          {message.citations && message.citations.length > 0 && (
            <div className="mt-3 pt-2 border-t border-[var(--color-outline-variant)]/30 flex flex-wrap gap-2 items-center">
              <span className="text-xs text-[var(--color-on-surface-variant)]">Sources:</span>
              {message.citations.map((c, i) => (
                <CitationBadge key={c.id} citation={c} index={i + 1} />
              ))}
            </div>
          )}
        </div>
        <div className="flex items-center gap-2 mt-1 opacity-70">
          <time className="message-timestamp text-xs block" dateTime={message.timestamp.toISOString()}>
            {timeStr}
          </time>
          {message.safety_tier && (
            <span className="text-[10px] uppercase font-semibold flex items-center gap-1 text-[var(--color-warning)]" title={`Safety Tier: ${message.safety_tier}`}>
              <ShieldAlert size={10} /> {message.safety_tier}
            </span>
          )}
        </div>
      </div>
    </article>
  );
};
