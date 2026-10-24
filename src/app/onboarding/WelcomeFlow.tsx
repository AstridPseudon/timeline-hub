import { lazy, Suspense, useCallback, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { TooltipProvider } from '@/shared/components/ui/tooltip.tsx';
import { BrowserTourEditor } from './BrowserTourEditor.tsx';
import { WelcomeRunMode, type WindowMode } from './WelcomeRunMode.tsx';
import { writeWelcomePhase, type WelcomeEntry } from './welcomeProgress.ts';

// Even module initialization for connection/identity stays outside the browser-only tour.
const WelcomeConnection = lazy(() => import('./WelcomeConnection.tsx'));
export function WelcomeFlow({ entry }: { entry: WelcomeEntry }) {
  const [queryClient] = useState(() => new QueryClient({ defaultOptions: { queries: { retry: false } } }));
  const [phase, setPhase] = useState<WelcomeEntry>(() => {
    if (entry !== 'editor') writeWelcomePhase(entry);
    return entry;
  });
  const [windowMode, setWindowMode] = useState<WindowMode>('app-window');
  const enter = useCallback((next: 'choose' | 'connection' | 'local') => {
    writeWelcomePhase(next);
    setPhase(next);
  }, []);
  const finishTour = useCallback(() => enter('choose'), [enter]);
  return <QueryClientProvider client={queryClient}><TooltipProvider><MemoryRouter>
    {phase === 'tour' && <BrowserTourEditor onFinish={finishTour} />}
    {phase === 'choose' && <WelcomeRunMode onContinue={enter} windowMode={windowMode} setWindowMode={setWindowMode} />}
    {phase === 'local' && <WelcomeRunMode local onBack={() => enter('choose')} windowMode={windowMode} setWindowMode={setWindowMode} />}
    {phase === 'connection' && <Suspense fallback={<div role="status">Connecting your machine…</div>}><WelcomeConnection windowMode={windowMode} /></Suspense>}
    {phase === 'editor' && null}
  </MemoryRouter></TooltipProvider></QueryClientProvider>;
}
