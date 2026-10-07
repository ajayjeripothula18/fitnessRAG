import axios, { AxiosError } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';

// ── Base API client ─────────────────────────────────────────────────────────
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30_000,
});

// ── Request interceptor: attach JWT ─────────────────────────────────────────
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('access_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ── Response interceptor: handle 401 ───────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    // If we have a response and it contains a detail in the body, use that as the message
    if (error.response && error.response.data && typeof error.response.data === 'object' && 'detail' in error.response.data) {
      // Assuming the detail is a string
      error.message = String(error.response.data.detail);
    }
    return Promise.reject(error);
  }
);

export default api;