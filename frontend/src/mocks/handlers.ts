import { http, HttpResponse } from 'msw';

export const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const handlers = [
  http.post(`${baseURL}/api/v1/chat`, async () => {
    // We can simulate a delay to show typing indicator
    await new Promise(resolve => setTimeout(resolve, 1500));

    return HttpResponse.json({
      conversation_id: 'mock-conv-id',
      message: {
        id: crypto.randomUUID(),
        role: 'user',
        content: 'Mock user message',
        created_at: new Date().toISOString()
      },
      response: {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'Here is a mock response from the AI coach. Based on my sources, you should make sure to lift heavy and eat protein.',
        created_at: new Date().toISOString(),
        citations: [
          {
            id: 'cit-1',
            title: 'Fitness Fundamentals Book',
            url: 'https://example.com/fitness-fundamentals'
          },
          {
            id: 'cit-2',
            title: 'Nutrition Guide'
          }
        ]
      },
      safety_tier: 'Safe'
    });
  }),
];
