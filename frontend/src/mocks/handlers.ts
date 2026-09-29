import { http, HttpResponse } from 'msw';

export const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const handlers = [
  http.post(`${baseURL}/api/v1/chat/message`, async () => {
    // We can simulate a delay to show typing indicator
    await new Promise(resolve => setTimeout(resolve, 1500));

    return HttpResponse.json({
      conversation_id: 1,
      message_id: 1,
      response: 'Here is a mock response from the AI coach. Based on my sources, you should make sure to lift heavy and eat protein.',
      citations: [
        {
          index: 1,
          title: 'Fitness Fundamentals Book',
          url: 'https://example.com/fitness-fundamentals'
        },
        {
          index: 2,
          title: 'Nutrition Guide',
          url: 'https://example.com/nutrition-guide'
        }
      ],
      safety_tier: 'Safe'
    });
  }),
];
