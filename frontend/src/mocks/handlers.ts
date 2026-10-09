import { http, HttpResponse } from 'msw';
import type { SendMessagePayload } from '../services/chatService';

export const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Mock profile data
const mockProfile = {
  full_name: 'Test User',
  age_range: '25-34',
  sex: 'male',
  height_cm: 180,
  weight_kg: 75,
  fitness_level: 'intermediate',
  primary_goal: 'muscle_gain',
  dietary_preference: 'omnivore',
  allergies: 'none',
  available_equipment: 'dumbbells, yoga mat',
  workout_location: 'home',
  days_per_week: 3,
  session_duration_min: 45,
  food_preferences: 'high protein',
  food_dislikes: 'none',
  experience_exercises: 'squats, push-ups, running'
};

export const handlers = [
  http.post(`${baseURL}/api/v1/chat/message`, async ({ request }) => {
    // We can simulate a delay to show typing indicator
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Get the conversation_id from request if present, otherwise simulate a new conversation
    const { conversation_id } = await request.json() as SendMessagePayload;
    // For simplicity, we'll always return conversation_id 1 and increment message_id based on a static counter?
    // But we want to simulate persistence: if conversation_id is provided, we return the same conversation_id.
    // We'll use a static map for message IDs per conversation? For mock, we'll just return a fixed message_id.
    // However, to test history, we need to return different messages for the same conversation.
    // We'll simplify: for now, we'll return a fixed conversation_id and message_id, and for history we'll return a fixed set.
    // We'll adjust the history mock to return messages based on the conversation_id.

    return HttpResponse.json({
      conversation_id: conversation_id ?? 1, // If not provided, use 1 (new conversation)
      message_id: 1, // In a real test, we might want to increment, but for simplicity we keep it fixed.
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

  // Mock for fetching conversation history
  http.get(`${baseURL}/api/v1/chat/history/:conversationId`, ({ params }) => {
    const conversationId = Number(params.conversationId);
    // If the conversationId is not a positive integer, return an error to simulate failure
    if (!Number.isInteger(conversationId) || conversationId <= 0) {
      return new HttpResponse(
        JSON.stringify({ error: 'Invalid conversation ID' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }
    // Return a fixed set of messages for any valid conversationId for simplicity
    // In a real test, we might want to vary based on conversationId, but we'll keep it simple.
    return HttpResponse.json({
      conversation_id: conversationId,
      messages: [
        {
          id: 1,
          role: 'user',
          content: 'Hello, AI!',
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          role: 'assistant',
          content: 'Hello human! How can I help you today?',
          created_at: new Date(Date.now() - 10000).toISOString(), // slightly earlier
        },
      ],
    });
  }),

  // Profile endpoints
  http.get(`${baseURL}/api/v1/users/me/profile`, () => {
    return HttpResponse.json(mockProfile);
  }),

  http.put(`${baseURL}/api/v1/users/me/profile`, async ({ request }) => {
    const profileUpdate = await request.json() as Partial<typeof mockProfile>;
    // Merge the update with the mock profile (simulating partial update)
    const updatedProfile = { ...mockProfile, ...profileUpdate };
    return HttpResponse.json(updatedProfile);
  }),
];