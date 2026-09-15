import React, { useState } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, User, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { authService } from '../services/authService';
import { useAuthStore } from '../store/authStore';

// ─── Schema ────────────────────────────────────────────────────────────────────
const registerSchema = z.object({
  email: z.string().email('Enter a valid email address'),
  full_name: z.string().min(2, 'Name must be at least 2 characters').optional().or(z.literal('')),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});
type RegisterForm = z.infer<typeof registerSchema>;

// ─── Register Page ─────────────────────────────────────────────────────────────
const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { setUser } = useAuthStore();
  const [serverError, setServerError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterForm>({ resolver: zodResolver(registerSchema) });

  const onSubmit = async (data: RegisterForm) => {
    setServerError(null);
    try {
      // 1. Register
      await authService.register({
        email: data.email,
        password: data.password,
        full_name: data.full_name || undefined,
      });
      // 2. Automatically log in after registration
      await authService.login({ email: data.email, password: data.password });
      const me = await authService.me();
      setUser(me);
      // 3. Navigate to dashboard
      navigate('/dashboard', { replace: true });
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        'An error occurred during registration. Please try again.';
      setServerError(msg);
    }
  };

  return (
    <div className="bg-[var(--color-background)] text-[var(--color-on-background)] min-h-screen flex flex-col items-center justify-center p-6 md:p-12 font-sans overflow-hidden relative">
      {/* Ambient glow behind the card */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-30">
        <div className="w-[300px] h-[300px] bg-[var(--color-primary-container)] rounded-full blur-[100px]"></div>
      </div>

      <main className="w-full max-w-md relative z-10 flex flex-col items-center">
        {/* Branding Logo */}
        <div className="mb-10 flex flex-col items-center">
          <img 
            alt="FitnessRAG Logo" 
            className="w-24 h-24 object-cover rounded-xl shadow-[0_10px_30px_-10px_rgba(138,43,226,0.5)] mb-2" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuA4Pq-XD9BRYu-uGnIc_Pu7-o__-gq5tWCti2IBgyHrwwdmjXKJN_-eFhgKfhXTDzH-78DgPSQwJFyTUokcc29MzmmeTvBnRsKieDfPfzBSD2U2M65hCrWYi-zkkMUSOF8aYIizPPJkneXN4ATlP8CJbVtHLVSxrIS-dTqHCSq6acDPGK-4WSHIKCaDGchRbYkFuTO-aJqJGHEocA3P92-kIvvkEnh-IluogKVF-QTiPVz2Iue9IB3X"
          />
          <h1 className="font-heading text-3xl font-bold text-[var(--color-primary)] tracking-tight">FitnessRAG</h1>
        </div>

        {/* Glassmorphism Register Card */}
        <div className="w-full glass-panel rounded-xl p-8 border-t-2 border-t-[var(--color-secondary-container)] shadow-2xl relative overflow-hidden group">
          <div className="mb-6 text-center">
            <h2 className="font-heading text-2xl font-semibold text-[var(--color-on-surface)] mb-2">Create Account</h2>
            <p className="text-[var(--color-on-surface-variant)]">Join us to power up your fitness journey.</p>
          </div>

          {/* Error alert */}
          {serverError && (
            <div className="mb-6 p-4 rounded-lg bg-[var(--color-error-container)] text-[var(--color-on-error-container)] flex items-center gap-2" role="alert" aria-live="assertive">
              <AlertCircle size={16} aria-hidden="true" />
              <span>{serverError}</span>
            </div>
          )}

          <form
            className="flex flex-col gap-4"
            onSubmit={handleSubmit(onSubmit)}
            noValidate
            aria-label="Registration form"
          >
            {/* Full Name Input */}
            <div className="relative">
              <label htmlFor="register-name" className="sr-only">Full Name</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <User size={20} />
              </div>
              <input
                id="register-name"
                type="text"
                className={`input-field pl-10 ${errors.full_name ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Full Name (Optional)"
                autoComplete="name"
                aria-invalid={!!errors.full_name}
                aria-describedby={errors.full_name ? 'register-name-error' : undefined}
                {...register('full_name')}
              />
              {errors.full_name && (
                <span id="register-name-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.full_name.message}
                </span>
              )}
            </div>

            {/* Email Input */}
            <div className="relative">
              <label htmlFor="register-email" className="sr-only">Email address</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Mail size={20} />
              </div>
              <input
                id="register-email"
                type="email"
                className={`input-field pl-10 ${errors.email ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Email address"
                autoComplete="email"
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? 'register-email-error' : undefined}
                {...register('email')}
              />
              {errors.email && (
                <span id="register-email-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.email.message}
                </span>
              )}
            </div>

            {/* Password Input */}
            <div className="relative">
              <label htmlFor="register-password" className="sr-only">Password</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Lock size={20} />
              </div>
              <input
                id="register-password"
                type={showPassword ? 'text' : 'password'}
                className={`input-field pl-10 pr-10 ${errors.password ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Password"
                autoComplete="new-password"
                aria-invalid={!!errors.password}
                aria-describedby={errors.password ? 'register-password-error' : undefined}
                {...register('password')}
              />
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-on-surface-variant)] hover:text-[var(--color-on-surface)] transition-colors"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
              {errors.password && (
                <span id="register-password-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.password.message}
                </span>
              )}
            </div>

            {/* Sign Up Button */}
            <button
              type="submit"
              id="register-submit-btn"
              className="btn-primary w-full mt-4 flex justify-center items-center gap-2"
              disabled={isSubmitting}
              aria-busy={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" aria-hidden="true" />
                  Creating account…
                </>
              ) : (
                'Sign Up'
              )}
            </button>
          </form>
        </div>

        {/* Sign In Link */}
        <p className="mt-6 text-center text-sm text-[var(--color-on-surface-variant)]">
          Already have an account?{' '}
          <NavLink to="/login" id="register-login-link" className="font-medium text-[var(--color-primary)] hover:text-[var(--color-primary-fixed)] transition-colors">
            Sign in
          </NavLink>
        </p>
      </main>
    </div>
  );
};

export default RegisterPage;
