import api from './api';

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserResponse {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
}

// ── Auth Service ─────────────────────────────────────────────────────────────
export const authService = {
  async login(payload: LoginPayload): Promise<TokenResponse> {
    // Backend expects OAuth2 form data for token endpoint
    const formData = new URLSearchParams();
    formData.append('username', payload.email);
    formData.append('password', payload.password);
    const { data } = await api.post<TokenResponse>('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    return data;
  },

  async register(payload: RegisterPayload): Promise<UserResponse> {
    const { data } = await api.post<UserResponse>('/api/v1/auth/register', payload);
    return data;
  },

  async logout(): Promise<void> {
    try { await api.post('/api/v1/auth/logout'); } catch { /* ignore */ }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  async me(): Promise<UserResponse> {
    const { data } = await api.get<UserResponse>('/api/v1/users/me');
    return data;
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },
};
