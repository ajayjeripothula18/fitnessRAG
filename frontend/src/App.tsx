import React, { Suspense, lazy } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import MainLayout from './components/layout/MainLayout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import './styles/tokens.css';
import './styles/globals.css';
import './styles/components.css';
import './styles/layout.css';

// ─── Lazy-loaded pages (code-split per route) ─────────────────────────────────
const LoginPage     = lazy(() => import('./pages/LoginPage'));
const RegisterPage  = lazy(() => import('./pages/RegisterPage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const ChatPage      = lazy(() => import('./pages/ChatPage'));

// ─── Query Client ─────────────────────────────────────────────────────────────
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000, // 30 s
    },
  },
});

// ─── Skeleton fallback shown during lazy loading ──────────────────────────────
const PageSkeleton: React.FC = () => (
  <div className="w-full h-full flex flex-col gap-4 animate-pulse p-4">
    <div className="bg-surface-overlay h-8 w-2/5 rounded-md" />
    <div className="bg-surface-overlay h-64 w-full rounded-md" />
    <div className="bg-surface-overlay h-6 w-3/5 rounded-md" />
  </div>
);

// ─── App Shell ────────────────────────────────────────────────────────────────
const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Suspense fallback={<PageSkeleton />}>
          <Routes>
            {/* Wrap all routes inside MainLayout to maintain standard layout structure */}
            <Route element={<MainLayout />}>
              {/* Public routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Protected routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/chat"
                element={
                  <ProtectedRoute>
                    <ChatPage />
                  </ProtectedRoute>
                }
              />

              {/* Stub routes — components will be built in Sprint 2 */}
              <Route
                path="/plans"
                element={
                  <ProtectedRoute>
                    <PlaceholderPage title="My Plans" />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/progress"
                element={
                  <ProtectedRoute>
                    <PlaceholderPage title="Progress" />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/library"
                element={
                  <ProtectedRoute>
                    <PlaceholderPage title="Exercise Library" />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/settings"
                element={
                  <ProtectedRoute>
                    <PlaceholderPage title="Settings" />
                  </ProtectedRoute>
                }
              />

              {/* Default redirect */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Route>
          </Routes>
        </Suspense>
      </Router>
    </QueryClientProvider>
  );
};

// ─── Inline placeholder for Sprint-2 pages ────────────────────────────────────
const PlaceholderPage: React.FC<{ title: string }> = ({ title }) => (
  <div className="flex flex-col items-center justify-center h-full w-full">
    <div className="p-8 bg-surface-raised border border-surface-border rounded-xl shadow-sm text-center max-w-md w-full">
      <h1 className="text-2xl font-bold text-text-primary mb-2">{title}</h1>
      <p className="text-text-secondary">
        This page is coming in Sprint 2. Use the AI Coach to get started!
      </p>
    </div>
  </div>
);

export default App;
