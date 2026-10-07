import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { Profile } from '../services/profileService';
import { profileService } from '../services/profileService';
import { User, Info, AlertCircle, AlertTriangle, CheckCircle } from 'lucide-react';

// ─── Schema ────────────────────────────────────────────────────────────────────────
const profileSchema = z.object({
  full_name: z.string().min(2, 'Name must be at least 2 characters').optional().or(z.literal('')),
  age_range: z.string().optional(),
  sex: z.enum(['male', 'female', 'other']).optional(),
  height_cm: z.number().int().positive().optional(),
  weight_kg: z.number().int().positive().optional(),
  fitness_level: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
  primary_goal: z.string().optional(),
  dietary_preference: z.string().optional(),
  allergies: z.string().optional(),
  available_equipment: z.string().optional(),
  workout_location: z.enum(['home', 'gym', 'outdoors']).optional(),
  days_per_week: z.number().int().min(1).max(7).optional(),
  session_duration_min: z.number().int().min(5).optional(),
  food_preferences: z.string().optional(),
  food_dislikes: z.string().optional(),
  experience_exercises: z.string().optional(),
});
type ProfileForm = z.infer<typeof profileSchema>;

// ─── Profile Page ──────────────────────────────────────────────────────────────────
const ProfilePage: React.FC = () => {
  const queryClient = useQueryClient();

  const {
    data: profile,
    isLoading: isProfileLoading,
    isError: isProfileError,
    error: profileError,
  } = useQuery<Profile, Error>({
    queryKey: ['profile'],
    queryFn: profileService.getProfile,
    staleTime: Infinity, // We'll refetch on mutation success
  });

  const {
    mutate: updateProfile,
    isPending: isSaving,
    isError: isSaveError,
    error: saveError,
    isSuccess: isSaveSuccess,
  } = useMutation({
    mutationFn: profileService.updateProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<ProfileForm>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      full_name: '',
      age_range: undefined,
      sex: undefined,
      height_cm: undefined,
      weight_kg: undefined,
      fitness_level: undefined,
      primary_goal: undefined,
      dietary_preference: undefined,
      allergies: undefined,
      available_equipment: undefined,
      workout_location: undefined,
      days_per_week: undefined,
      session_duration_min: undefined,
      food_preferences: undefined,
      food_dislikes: undefined,
      experience_exercises: undefined,
    },
  });

  const onSubmit = (data: ProfileForm) => {
    // Convert empty strings to undefined for optional fields
    const profileData = Object.entries(data).reduce((acc, [key, value]) => {
      if (value === '') {
        return acc;
      }
      return { ...acc, [key]: value };
    }, {} as Partial<ProfileForm>);

    updateProfile(profileData);
  };

  // Reset form when profile data changes
  React.useEffect(() => {
    if (profile) {
      reset(profile as ProfileForm);
    }
  }, [profile, reset]);

  if (isProfileLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-full w-full">
        <div className="w-full h-16 w-64 bg-surface-overlay rounded-md animate-pulse" />
      </div>
    );
  }

  if (isProfileError) {
    return (
      <div className="flex flex-col items-center justify-center h-full w-full p-6">
        <AlertTriangle size={24} className="mb-4 text-[var(--color-error)]" />
        <h2 className="text-xl font-semibold text-[var(--color-on-surface)] mb-2">
          Failed to load profile
        </h2>
        <p className="text-[var(--color-on-surface-variant)] text-center max-w-md">
          {(profileError as Error)?.message ?? 'An unknown error occurred'}
        </p>
        <button
          onClick={() => window.location.reload()}
          className="mt-6 btn-secondary"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-[var(--color-background)] text-[var(--color-on-background)] flex flex-col items-center p-6 md:p-12 font-sans relative">
      {/* Ambient glow behind the card */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-30">
        <div className="w-[300px] h-[300px] bg-[var(--color-primary-container)] rounded-full blur-[100px]"></div>
      </div>

      <div className="w-full max-w-md relative z-10 flex flex-col items-center">
        {/* Branding Logo */}
        <div className="mb-10 flex flex-col items-center">
          <img
            alt="FitnessRAG Logo"
            className="w-24 h-24 object-cover rounded-xl shadow-[0_10px_30px_-10px_rgba(138,43,226,0.5)] mb-2"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuA4Pq-XD9BRYu-uGnIc_Pu7-o__-gq5tWCti2IBgyHrwwdmjXKJN_-eFhgKfhXTDzH-78DgPSQwJFyTUokcc29MzmmeTvBnRsKieDfPfzBSD2U2M65hCrWYi-zkkMUSOF8aYIizPPJkneXN4ATlP8CJbVtHLVSxrIS-dTqHCSq6acDPGK-4WSHIKCaDGchRbYkFuTO-aJqJGHEocA3P92-kIvvkEnh-IluogKVF-QTiPVz2Iue9IB3X"
          />
          <h1 className="font-heading text-3xl font-bold text-[var(--color-primary)] tracking-tight">FitnessRAG</h1>
        </div>

        {/* Glassmorphism Profile Card */}
        <div className="w-full glass-panel rounded-xl p-8 border-t-2 border-t-[var(--color-secondary-container)] shadow-2xl relative overflow-hidden group">
          <div className="mb-6 text-center">
            <h2 className="font-heading text-2xl font-semibold text-[var(--color-on-surface)] mb-2">My Profile</h2>
            <p className="text-[var(--color-on-surface-variant)]">
              Update your fitness and nutrition preferences to get personalized advice.
            </p>
          </div>

          {/* Save Status */}
          {isSaveSuccess && (
            <div className="mb-4 p-3 rounded-lg bg-[var(--color-success-container)] text-[var(--color-on-success-container)] flex items-center gap-2" role="status">
              <CheckCircle size={16} aria-hidden="true" />
              <span>Profile saved successfully!</span>
            </div>
          )}

          {/* Save Error */}
          {isSaveError && (
            <div className="mb-4 p-3 rounded-lg bg-[var(--color-error-container)] text-[var(--color-on-error-container)] flex items-center gap-2" role="alert">
              <AlertCircle size={16} aria-hidden="true" />
              <span>
                {(saveError as Error)?.message ?? 'Failed to save profile'}
              </span>
            </div>
          )}

          <form
            className="flex flex-col gap-4"
            onSubmit={handleSubmit(onSubmit)}
            noValidate
            aria-label="Profile form"
          >
            {/* Full Name Input */}
            <div className="relative">
              <label htmlFor="profile-name" className="sr-only">Full Name</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <User size={20} />
              </div>
              <input
                id="profile-name"
                type="text"
                className={`input-field pl-10 ${errors.full_name ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Full Name (Optional)"
                autoComplete="name"
                aria-invalid={!!errors.full_name}
                aria-describedby={errors.full_name ? 'profile-name-error' : undefined}
                {...register('full_name')}
              />
              {errors.full_name && (
                <span id="profile-name-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.full_name.message}
                </span>
              )}
            </div>

            {/* Age Range Input */}
            <div className="relative">
              <label htmlFor="profile-age-range" className="sr-only">Age Range</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-age-range"
                type="text"
                className={`input-field pl-10 ${errors.age_range ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Age Range (e.g., 25-34)"
                autoComplete="off"
                aria-invalid={!!errors.age_range}
                aria-describedby={errors.age_range ? 'profile-age-range-error' : undefined}
                {...register('age_range')}
              />
              {errors.age_range && (
                <span id="profile-age-range-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.age_range.message}
                </span>
              )}
            </div>

            {/* Sex Input */}
            <div className="relative">
              <label htmlFor="profile-sex" className="sr-only">Sex</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <select
                id="profile-sex"
                className={`select-field pl-10 pr-10 ${errors.sex ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                aria-invalid={!!errors.sex}
                aria-describedby={errors.sex ? 'profile-sex-error' : undefined}
                {...register('sex')}
              >
                <option value="">Select sex (optional)</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              {errors.sex && (
                <span id="profile-sex-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.sex.message}
                </span>
              )}
            </div>

            {/* Height Input */}
            <div className="relative">
              <label htmlFor="profile-height" className="sr-only">Height (cm)</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-height"
                type="number"
                className={`input-field pl-10 ${errors.height_cm ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Height in cm"
                autoComplete="off"
                aria-invalid={!!errors.height_cm}
                aria-describedby={errors.height_cm ? 'profile-height-error' : undefined}
                {...register('height_cm', {
                  valueAsNumber: true,
                  setValueAs: (value) => {
                    if (value === '' || value === null) {
                      return undefined;
                    }
                    return Number(value);
                  }
                })}
              />
              {errors.height_cm && (
                <span id="profile-height-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.height_cm.message}
                </span>
              )}
            </div>

            {/* Weight Input */}
            <div className="relative">
              <label htmlFor="profile-weight" className="sr-only">Weight (kg)</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-weight"
                type="number"
                className={`input-field pl-10 ${errors.weight_kg ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Weight in kg"
                autoComplete="off"
                aria-invalid={!!errors.weight_kg}
                aria-describedby={errors.weight_kg ? 'profile-weight-error' : undefined}
                {...register('weight_kg', {
                  valueAsNumber: true,
                  setValueAs: (value) => {
                    if (value === '' || value === null) {
                      return undefined;
                    }
                    return Number(value);
                  }
                })}
              />
              {errors.weight_kg && (
                <span id="profile-weight-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.weight_kg.message}
                </span>
              )}
            </div>

            {/* Fitness Level Input */}
            <div className="relative">
              <label htmlFor="profile-fitness-level" className="sr-only">Fitness Level</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <select
                id="profile-fitness-level"
                className={`select-field pl-10 pr-10 ${errors.fitness_level ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                aria-invalid={!!errors.fitness_level}
                aria-describedby={errors.fitness_level ? 'profile-fitness-level-error' : undefined}
                {...register('fitness_level')}
              >
                <option value="">Select fitness level (optional)</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
              {errors.fitness_level && (
                <span id="profile-fitness-level-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.fitness_level.message}
                </span>
              )}
            </div>

            {/* Primary Goal Input */}
            <div className="relative">
              <label htmlFor="profile-primary-goal" className="sr-only">Primary Goal</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-primary-goal"
                type="text"
                className={`input-field pl-10 ${errors.primary_goal ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Primary Goal (e.g., weight_loss, muscle_gain)"
                autoComplete="off"
                aria-invalid={!!errors.primary_goal}
                aria-describedby={errors.primary_goal ? 'profile-primary-goal-error' : undefined}
                {...register('primary_goal')}
              />
              {errors.primary_goal && (
                <span id="profile-primary-goal-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.primary_goal.message}
                </span>
              )}
            </div>

            {/* Dietary Preference Input */}
            <div className="relative">
              <label htmlFor="profile-dietary-preference" className="sr-only">Dietary Preference</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-dietary-preference"
                type="text"
                className={`input-field pl-10 ${errors.dietary_preference ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Dietary Preference (e.g., vegetarian, vegan)"
                autoComplete="off"
                aria-invalid={!!errors.dietary_preference}
                aria-describedby={errors.dietary_preference ? 'profile-dietary-preference-error' : undefined}
                {...register('dietary_preference')}
              />
              {errors.dietary_preference && (
                <span id="profile-dietary-preference-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.dietary_preference.message}
                </span>
              )}
            </div>

            {/* Allergies Input */}
            <div className="relative">
              <label htmlFor="profile-allergies" className="sr-only">Allergies</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <textarea
                id="profile-allergies"
                className={`textarea-field pl-10 ${errors.allergies ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="List any allergies"
                aria-invalid={!!errors.allergies}
                aria-describedby={errors.allergies ? 'profile-allergies-error' : undefined}
                {...register('allergies')}
              />
              {errors.allergies && (
                <span id="profile-allergies-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.allergies.message}
                </span>
              )}
            </div>

            {/* Available Equipment Input */}
            <div className="relative">
              <label htmlFor="profile-available-equipment" className="sr-only">Available Equipment</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <textarea
                id="profile-available-equipment"
                className={`textarea-field pl-10 ${errors.available_equipment ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="List available equipment (e.g., dumbbells, yoga mat)"
                aria-invalid={!!errors.available_equipment}
                aria-describedby={errors.available_equipment ? 'profile-available-equipment-error' : undefined}
                {...register('available_equipment')}
              />
              {errors.available_equipment && (
                <span id="profile-available-equipment-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.available_equipment.message}
                </span>
              )}
            </div>

            {/* Workout Location Input */}
            <div className="relative">
              <label htmlFor="profile-workout-location" className="sr-only">Workout Location</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <select
                id="profile-workout-location"
                className={`select-field pl-10 pr-10 ${errors.workout_location ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                aria-invalid={!!errors.workout_location}
                aria-describedby={errors.workout_location ? 'profile-workout-location-error' : undefined}
                {...register('workout_location')}
              >
                <option value="">Select workout location (optional)</option>
                <option value="home">Home</option>
                <option value="gym">Gym</option>
                <option value="outdoors">Outdoors</option>
              </select>
              {errors.workout_location && (
                <span id="profile-workout-location-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.workout_location.message}
                </span>
              )}
            </div>

            {/* Days Per Week Input */}
            <div className="relative">
              <label htmlFor="profile-days-per-week" className="sr-only">Days per Week</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-days-per-week"
                type="number"
                className={`input-field pl-10 ${errors.days_per_week ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Days per week (1-7)"
                autoComplete="off"
                aria-invalid={!!errors.days_per_week}
                aria-describedby={errors.days_per_week ? 'profile-days-per-week-error' : undefined}
                {...register('days_per_week', {
                  valueAsNumber: true,
                  setValueAs: (value) => {
                    if (value === '' || value === null) {
                      return undefined;
                    }
                    return Number(value);
                  }
                })}
              />
              {errors.days_per_week && (
                <span id="profile-days-per-week-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.days_per_week.message}
                </span>
              )}
            </div>

            {/* Session Duration Input */}
            <div className="relative">
              <label htmlFor="profile-session-duration" className="sr-only">Session Duration (min)</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <input
                id="profile-session-duration"
                type="number"
                className={`input-field pl-10 ${errors.session_duration_min ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Session duration in minutes"
                autoComplete="off"
                aria-invalid={!!errors.session_duration_min}
                aria-describedby={errors.session_duration_min ? 'profile-session-duration-error' : undefined}
                {...register('session_duration_min', {
                  valueAsNumber: true,
                  setValueAs: (value) => {
                    if (value === '' || value === null) {
                      return undefined;
                    }
                    return Number(value);
                  }
                })}
              />
              {errors.session_duration_min && (
                <span id="profile-session-duration-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.session_duration_min.message}
                </span>
              )}
            </div>

            {/* Food Preferences Input */}
            <div className="relative">
              <label htmlFor="profile-food-preferences" className="sr-only">Food Preferences</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <textarea
                id="profile-food-preferences"
                className={`textarea-field pl-10 ${errors.food_preferences ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Describe your food preferences"
                aria-invalid={!!errors.food_preferences}
                aria-describedby={errors.food_preferences ? 'profile-food-preferences-error' : undefined}
                {...register('food_preferences')}
              />
              {errors.food_preferences && (
                <span id="profile-food-preferences-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.food_preferences.message}
                </span>
              )}
            </div>

            {/* Food Dislikes Input */}
            <div className="relative">
              <label htmlFor="profile-food-dislikes" className="sr-only">Food Dislikes</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <textarea
                id="profile-food-dislikes"
                className={`textarea-field pl-10 ${errors.food_dislikes ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="List foods you dislike"
                aria-invalid={!!errors.food_dislikes}
                aria-describedby={errors.food_dislikes ? 'profile-food-dislikes-error' : undefined}
                {...register('food_dislikes')}
              />
              {errors.food_dislikes && (
                <span id="profile-food-dislikes-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.food_dislikes.message}
                </span>
              )}
            </div>

            {/* Experience Exercises Input */}
            <div className="relative">
              <label htmlFor="profile-experience-exercises" className="sr-only">Experience Exercises</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Info size={20} />
              </div>
              <textarea
                id="profile-experience-exercises"
                className={`textarea-field pl-10 ${errors.experience_exercises ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="List exercises you have experience with"
                aria-invalid={!!errors.experience_exercises}
                aria-describedby={errors.experience_exercises ? 'profile-experience-exercises-error' : undefined}
                {...register('experience_exercises')}
              />
              {errors.experience_exercises && (
                <span id="profile-experience-exercises-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.experience_exercises.message}
                </span>
              )}
            </div>

            {/* Save Button */}
            <button
              type="submit"
              id="profile-save-btn"
              className="btn-primary w-full mt-4 flex justify-center items-center gap-2"
              disabled={isSubmitting || isSaving}
              aria-busy={isSubmitting || isSaving}
            >
              {isSubmitting || isSaving ? (
                <>
                  <span className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" aria-hidden="true" />
                  Saving…
                </>
              ) : (
                'Save Profile'
              )}
            </button>
          </form>
        </div>

        {/* Sign Out Link */}
        <div className="mt-6 text-center text-sm text-[var(--color-on-surface-variant)]">
          <button
            onClick={() => {
              // TODO: Implement logout via authService
              window.location.href = '/login';
            }}
            className="font-medium text-[var(--color-primary)] hover:text-[var(--color-primary-fixed)] transition-colors"
          >
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;