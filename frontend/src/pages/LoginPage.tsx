import React, { useState } from 'react';
import { useNavigate, NavLink, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Mail, Lock, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { authService } from '../services/authService';
import { useAuthStore } from '../store/authStore';

// ─── Schema ────────────────────────────────────────────────────────────────────
const loginSchema = z.object({
  email: z.string().email('Enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});
type LoginForm = z.infer<typeof loginSchema>;

// ─── Login Page ────────────────────────────────────────────────────────────────
const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { setUser } = useAuthStore();
  const [serverError, setServerError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({ resolver: zodResolver(loginSchema) });

  const onSubmit = async (data: LoginForm) => {
    setServerError(null);
    try {
      await authService.login({ email: data.email, password: data.password });
      const me = await authService.me();
      setUser(me);
      // Redirect to originally requested page or default to /dashboard
      const from = (location.state as { from?: { pathname: string } })?.from?.pathname ?? '/dashboard';
      navigate(from, { replace: true });
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        'Invalid email or password. Please try again.';
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
        <div className="mb-12 flex flex-col items-center">
          <img 
            alt="FitnessRAG Logo" 
            className="w-32 h-32 object-cover rounded-xl shadow-[0_10px_30px_-10px_rgba(138,43,226,0.5)] mb-2" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuA4Pq-XD9BRYu-uGnIc_Pu7-o__-gq5tWCti2IBgyHrwwdmjXKJN_-eFhgKfhXTDzH-78DgPSQwJFyTUokcc29MzmmeTvBnRsKieDfPfzBSD2U2M65hCrWYi-zkkMUSOF8aYIizPPJkneXN4ATlP8CJbVtHLVSxrIS-dTqHCSq6acDPGK-4WSHIKCaDGchRbYkFuTO-aJqJGHEocA3P92-kIvvkEnh-IluogKVF-QTiPVz2Iue9IB3X"
          />
          <h1 className="font-heading text-4xl font-bold text-[var(--color-primary)] tracking-tight">FitnessRAG</h1>
        </div>

        {/* Glassmorphism Login Card */}
        <div className="w-full glass-panel rounded-xl p-8 border-t-2 border-t-[var(--color-secondary-container)] shadow-2xl relative overflow-hidden group">
          <div className="mb-6 text-center">
            <h2 className="font-heading text-2xl font-semibold text-[var(--color-on-surface)] mb-2">Welcome Back</h2>
            <p className="text-[var(--color-on-surface-variant)]">Access your AI-powered performance data.</p>
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
            aria-label="Login form"
          >
            {/* Email Input */}
            <div className="relative">
              <label htmlFor="login-email" className="sr-only">Email address</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Mail size={20} />
              </div>
              <input
                id="login-email"
                type="email"
                className={`input-field pl-10 ${errors.email ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Email address"
                autoComplete="email"
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? 'login-email-error' : undefined}
                {...register('email')}
              />
              {errors.email && (
                <span id="login-email-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.email.message}
                </span>
              )}
            </div>

            {/* Password Input */}
            <div className="relative">
              <label htmlFor="login-password" className="sr-only">Password</label>
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[var(--color-on-surface-variant)] group-focus-within:text-[var(--color-primary)]">
                <Lock size={20} />
              </div>
              <input
                id="login-password"
                type={showPassword ? 'text' : 'password'}
                className={`input-field pl-10 pr-10 ${errors.password ? 'border-[var(--color-error)] focus:border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}`}
                placeholder="Password"
                autoComplete="current-password"
                aria-invalid={!!errors.password}
                aria-describedby={errors.password ? 'login-password-error' : undefined}
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
                <span id="login-password-error" className="text-[var(--color-error)] text-sm mt-1 block" role="alert">
                  {errors.password.message}
                </span>
              )}
            </div>

            <div className="flex items-center justify-between mt-2">
              <div className="flex items-center">
                <input 
                  id="remember-me" 
                  name="remember-me" 
                  type="checkbox" 
                  className="h-4 w-4 text-[var(--color-primary)] focus:ring-[var(--color-primary)] border-[var(--color-outline-variant)] bg-[var(--color-surface-container-lowest)] rounded" 
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-[var(--color-on-surface-variant)]">Remember me</label>
              </div>
              <div className="text-sm">
                <a href="#" className="font-medium text-[var(--color-primary)] hover:text-[var(--color-primary-fixed)] transition-colors">Forgot password?</a>
              </div>
            </div>

            {/* Sign In Button */}
            <button
              type="submit"
              id="login-submit-btn"
              className="btn-primary w-full mt-2 flex justify-center items-center gap-2"
              disabled={isSubmitting}
              aria-busy={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" aria-hidden="true" />
                  Signing in…
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>
        </div>

        {/* Sign Up Link */}
        <p className="mt-6 text-center text-sm text-[var(--color-on-surface-variant)]">
          Don't have an account?{' '}
          <NavLink to="/register" id="login-register-link" className="font-medium text-[var(--color-primary)] hover:text-[var(--color-primary-fixed)] transition-colors">
            Sign up
          </NavLink>
        </p>
      </main>
    </div>
  );
};

export default LoginPage;
