import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Navigation from './Navigation';

const MainLayout: React.FC = () => {
  return (
    <div className="flex flex-col h-[100dvh] w-full bg-surface-base overflow-hidden">
      <Header />
      
      <div className="flex flex-1 overflow-hidden md:flex-row flex-col">
        <Navigation />
        
        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto relative w-full h-full bg-surface-base">
          {/* A container inside main can use safe area if needed, though main itself could just have padding */}
          {/* Assuming mobile safari needs pb-safe if no bottom tab, but bottom tab handles it. 
              However, for chat UI or lists, we want standard padding plus whatever safe area exists. */}
          <div className="flex flex-col h-full w-full max-w-7xl mx-auto p-4 md:p-6 pb-[calc(env(safe-area-inset-bottom)+1rem)]">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
