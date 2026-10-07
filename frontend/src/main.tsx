import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { worker } from './mocks/browser';
import { http, HttpResponse } from 'msw';

async function enableMocking() {
  if (import.meta.env.PROD) {
    return;
  }

  await worker.start({
    onUnhandledRequest: 'bypass',
  });

  // Expose MSW utilities for Cypress testing
  // @ts-ignore: Cypress is not typed in the global scope
  if ((window as any).Cypress) {
    // @ts-ignore: Cypress is not typed in the global scope
    window.__MSW__ = {
      worker,
      http,
      HttpResponse,
    };
  }
}

enableMocking().then(() => {
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
});
