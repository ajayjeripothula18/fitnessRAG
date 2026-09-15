import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  MessageSquare,
  LayoutDashboard,
  Dumbbell,
  TrendingUp,
  BookOpen,
  Settings,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const Navigation: React.FC = () => {
  const { isAuthenticated } = useAuthStore();
  if (!isAuthenticated) return null;

  const sections = [
    {
      title: 'Main',
      items: [
        { to: '/chat', label: 'AI Coach', icon: MessageSquare, id: 'nav-chat' },
        { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, id: 'nav-dashboard' },
      ],
    },
    {
      title: 'Training',
      items: [
        { to: '/plans', label: 'My Plans', icon: Dumbbell, id: 'nav-plans' },
        { to: '/progress', label: 'Progress', icon: TrendingUp, id: 'nav-progress' },
        { to: '/library', label: 'Exercise Library', icon: BookOpen, id: 'nav-library' },
      ],
    },
    {
      title: 'Account',
      items: [
        { to: '/settings', label: 'Settings', icon: Settings, id: 'nav-settings' },
      ],
    },
  ];

  // Flatten items for mobile bottom nav
  const mobileItems = sections.flatMap(s => s.items).filter(item => 
    // Maybe we only want the most important ones on mobile to save space?
    // Let's just show top 5 on mobile
    ['nav-dashboard', 'nav-chat', 'nav-plans', 'nav-progress', 'nav-settings'].includes(item.id)
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex w-64 flex-shrink-0 bg-surface-raised border-r border-surface-border flex-col overflow-y-auto transition-all pl-safe" role="complementary" aria-label="App sidebar">
        {sections.map((section) => (
          <div className="p-4 border-b border-surface-border" key={section.title}>
            <p className="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">{section.title}</p>
            <nav className="flex flex-col gap-1" aria-label={section.title}>
              {section.items.map(({ to, label, icon: Icon, id }) => (
                <NavLink
                  key={to}
                  to={to}
                  id={id}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md w-full transition-colors ${
                      isActive 
                        ? 'text-primary-400 bg-primary-400/10 font-semibold' 
                        : 'text-text-secondary hover:text-text-primary hover:bg-surface-overlay'
                    }`
                  }
                  aria-label={label}
                >
                  <Icon className="w-[18px] h-[18px] shrink-0" aria-hidden="true" />
                  {label}
                </NavLink>
              ))}
            </nav>
          </div>
        ))}
      </aside>

      {/* Mobile Bottom Tab Bar */}
      <nav className="md:hidden flex flex-row items-center justify-around bg-surface-raised border-t border-surface-border pb-safe pt-2 px-2 shrink-0 z-50">
        {mobileItems.map(({ to, label, icon: Icon, id }) => (
          <NavLink
            key={to}
            to={to}
            id={`${id}-mobile`}
            className={({ isActive }) =>
              `flex flex-col items-center justify-center p-2 rounded-lg min-w-[64px] transition-colors ${
                isActive 
                  ? 'text-primary-400' 
                  : 'text-text-secondary hover:text-text-primary'
              }`
            }
            aria-label={label}
          >
            <Icon className={`w-6 h-6 mb-1 ${/* isActive check isn't directly available for icon props without a wrapper, so color inherits */ ''}`} aria-hidden="true" />
            <span className="text-[10px] font-medium leading-none">{label}</span>
          </NavLink>
        ))}
      </nav>
    </>
  );
};

export default Navigation;
