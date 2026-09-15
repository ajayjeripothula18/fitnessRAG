import api from './api';

export interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  version: string;
  database: string;
  timestamp: string;
}

export const healthService = {
  async check(): Promise<HealthResponse> {
    const { data } = await api.get<HealthResponse>('/health');
    return data;
  },
};
