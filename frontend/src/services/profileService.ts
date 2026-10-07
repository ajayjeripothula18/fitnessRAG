import api from './api';

export interface Profile {
  full_name?: string | null;
  age_range?: string | null;
  sex?: string | null;
  height_cm?: number | null;
  weight_kg?: number | null;
  fitness_level?: string | null;
  primary_goal?: string | null;
  dietary_preference?: string | null;
  allergies?: string | null;
  available_equipment?: string | null;
  workout_location?: string | null;
  days_per_week?: number | null;
  session_duration_min?: number | null;
  food_preferences?: string | null;
  food_dislikes?: string | null;
  experience_exercises?: string | null;
}

export const profileService = {
  async getProfile(): Promise<Profile> {
    const { data } = await api.get<Profile>('/api/v1/users/me/profile');
    return data;
  },

  async updateProfile(profileData: Partial<Profile>): Promise<Profile> {
    const { data } = await api.put<Profile>('/api/v1/users/me/profile', profileData);
    return data;
  },
};