import { http, HttpResponse } from 'msw';

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
