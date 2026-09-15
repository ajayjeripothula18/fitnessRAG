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

export interface SendMessagePayload {
  message: string;
  conversation_id?: string;
}

export interface SendMessageResponse {
  conversation_id: string;
  message: ChatMessage;
  response: ChatMessage;
  safety_tier?: string;
}

export const chatService = {
  async sendMessage(payload: SendMessagePayload): Promise<SendMessageResponse> {
    const { data } = await api.post<SendMessageResponse>('/api/v1/chat', payload);
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
