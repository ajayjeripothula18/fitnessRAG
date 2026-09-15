import React from 'react';
import { NavLink } from 'react-router-dom';
import { Zap } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const Header: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <header className="flex h-16 shrink-0 items-center justify-between px-4 bg-surface-base border-b border-surface-border shadow-sm pt-safe z-40" role="banner">
      <NavLink to="/" className="flex items-center gap-3 no-underline group" aria-label="FitnessRAG Home">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 shadow-lg shadow-primary-500/20 group-hover:scale-105 transition-transform" aria-hidden="true">
          <Zap size={18} className="text-white" />
        </div>
        <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
          FitnessRAG
        </span>
      </NavLink>

      <div className="flex items-center gap-4">
        {isAuthenticated ? (
          <>
            <span
              className="relative flex h-3 w-3"
              role="status"
              aria-label="API connected"
              title="Backend connected"
            >
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-success-500"></span>
            </span>
            <div
              className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 text-white font-semibold text-sm shadow-inner cursor-default"
              aria-label={`User: ${user?.email ?? 'Account'}`}
              title={user?.email}
            >
              {(user?.full_name ?? user?.email ?? 'U')[0].toUpperCase()}
            </div>
            <button
              className="px-3 py-1.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-surface-overlay rounded-md transition-colors"
              onClick={logout}
              aria-label="Log out"
              id="header-logout-btn"
            >
              Log out
            </button>
          </>
        ) : (
          <NavLink 
            to="/login" 
            className="px-4 py-2 text-sm font-semibold text-white bg-primary-600 hover:bg-primary-500 active:bg-primary-700 rounded-lg shadow-sm transition-all shadow-primary-500/20" 
            id="header-login-btn"
          >
            Sign in
          </NavLink>
        )}
      </div>
    </header>
  );
};

export default Header;
