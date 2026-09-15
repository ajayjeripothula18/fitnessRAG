import React from 'react';
import { LayoutDashboard, TrendingUp, Zap, MessageSquare } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

/**
 * DashboardPage — landing screen after login.
 * Shows a welcome banner, quick stats (placeholders for Sprint 2 data),
 * and entry points to the main features.
 */
const DashboardPage: React.FC = () => {
  const user = useAuthStore((s) => s.user);
  const displayName = user?.full_name ?? user?.email ?? 'Athlete';

  const quickActions = [
    {
      id: 'qa-chat',
      to: '/chat',
      icon: MessageSquare,
      label: 'Ask AI Coach',
      description: 'Get personalised fitness guidance',
      color: 'var(--color-primary)',
    },
    {
      id: 'qa-plans',
      to: '/plans',
      icon: LayoutDashboard,
      label: 'View Plans',
      description: 'Your active workout programmes',
      color: 'var(--color-success)',
    },
    {
      id: 'qa-progress',
      to: '/progress',
      icon: TrendingUp,
      label: 'Track Progress',
      description: 'Charts and milestone history',
      color: 'var(--color-warning)',
    },
  ];

  return (
    <main className="dashboard-page" aria-label="Dashboard">
      {/* Welcome banner */}
      <section className="dashboard-hero" aria-labelledby="dashboard-heading">
        <div className="dashboard-hero-content">
          <div className="dashboard-hero-icon" aria-hidden="true">
            <Zap size={28} />
          </div>
          <div>
            <h1 id="dashboard-heading" className="dashboard-heading">
              Welcome back, {displayName}!
            </h1>
            <p className="dashboard-subheading">
              Your AI fitness coach is ready. What are we working on today?
            </p>
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="dashboard-section" aria-labelledby="quick-actions-heading">
        <h2 id="quick-actions-heading" className="section-title">
          Quick Actions
        </h2>
        <div className="quick-actions-grid">
          {quickActions.map(({ id, to, icon: Icon, label, description, color }) => (
            <NavLink
              key={id}
              id={id}
              to={to}
              className="quick-action-card card"
              aria-label={label}
            >
              <div className="quick-action-icon" style={{ color }} aria-hidden="true">
                <Icon size={24} />
              </div>
              <h3 className="quick-action-label">{label}</h3>
              <p className="quick-action-desc">{description}</p>
            </NavLink>
          ))}
        </div>
      </section>

      {/* Stats row — placeholder for Sprint 2 real data */}
      <section className="dashboard-section" aria-labelledby="stats-heading">
        <h2 id="stats-heading" className="section-title">
          This Week
        </h2>
        <div className="stats-grid" role="list">
          {[
            { label: 'Sessions Logged', value: '—', id: 'stat-sessions' },
            { label: 'Messages with Coach', value: '—', id: 'stat-messages' },
            { label: 'Active Plan', value: '—', id: 'stat-plan' },
          ].map(({ label, value, id }) => (
            <div key={id} id={id} className="stat-card card" role="listitem">
              <span className="stat-value">{value}</span>
              <span className="stat-label">{label}</span>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
};

export default DashboardPage;
