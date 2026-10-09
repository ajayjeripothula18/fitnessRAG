import api from './api';

export interface Citation {
  id: string;
  title: string;
  url?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  citations?: Citation[];
}

export interface Conversation {
  id: string;
  title?: string;
  created_at: string;
  messages: ChatMessage[];
}

// Backend citation shape from ChatResponse.citations
export interface BackendCitation {
  index: number;
  title: string;
  url: string;
  page?: number;
}

export interface SendMessagePayload {
  message: string;
  conversation_id?: number;
  history: Array<{ role: string; content: string }>;
}

export interface SendMessageResponse {
  conversation_id: number;
  message_id: number;
  response: string;
  citations: BackendCitation[];
  safety_tier: string;
}

export const chatService = {
  async sendMessage(payload: SendMessagePayload): Promise<SendMessageResponse> {
    const { data } = await api.post<SendMessageResponse>('/api/v1/chat/message', payload);
    return data;
  },

  async getHistory(conversationId: number): Promise<{ conversation_id: number; messages: Array<{ id: number; role: string; content: string; created_at: string }> }> {
    const { data } = await api.get(`/api/v1/chat/history/${conversationId}`);
    return data;
  },

  async getConversations(): Promise<Conversation[]> {
    const { data } = await api.get<Conversation[]>('/api/v1/chat/conversations');
    return data;
  },

  async getConversation(id: string): Promise<Conversation> {
    const { data } = await api.get<Conversation>(`/api/v1/chat/conversations/${id}`);
    return data;
  },
};
