import api from './api';

export interface IngestionResponse {
  message: string;
  chunks_ingested?: number;
}

export interface IngestionService {
  uploadFile: (file: File) => Promise<IngestionResponse>;
}

export const ingestionService: IngestionService = {
  uploadFile: async (file: File): Promise<IngestionResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const { data } = await api.post<IngestionResponse>(
      '/api/v1/ingestion/file',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return data;
  },
};