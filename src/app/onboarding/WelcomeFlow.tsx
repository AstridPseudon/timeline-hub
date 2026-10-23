import { lazy, Suspense, useCallback, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { TooltipProvider } from '@/shared/components/ui/tooltip.tsx';
import { BrowserTourEditor } from './BrowserTourEditor.tsx';
import { welcomeEntryPhase, writeWelcomePhase } from './welcomeProgress.ts';

// Even module initialization for connection/identity stays outside the browser-only tour.
const WelcomeConnection = lazy(() => import('./WelcomeConnection.tsx'));
export function WelcomeFlow() {
  const [queryClient] = useState(() => new QueryClient({ defaultOptions: { queries: { retry: false } } }));
  const [phase, setPhase] = useState(() => {
    const initial = welcomeEntryPhase(new URL(window.location.href));
    writeWelcomePhase(initial);
    return initial;
  });
  const finish = useCallback(() => {
    writeWelcomePhase('connection');
    setPhase('connection');
  }, []);
  return <QueryClientProvider client={queryClient}><TooltipProvider><MemoryRouter>
    {phase === 'tour' ? <BrowserTourEditor onFinish={finish} /> : <Suspense fallback={<div role="status">Connecting your machine…</div>}><WelcomeConnection /></Suspense>}
  </MemoryRouter></TooltipProvider></QueryClientProvider>;
}
