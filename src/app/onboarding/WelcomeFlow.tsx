import { lazy, Suspense, useCallback, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { TooltipProvider } from '@/shared/components/ui/tooltip.tsx';
import { BrowserTourEditor } from './BrowserTourEditor.tsx';
import { EditorBackdrop } from '@/shared/components/RuntimeConnection/EditorCardLayer.tsx';
import { WelcomeRunMode, type RunMode, type WindowMode } from './WelcomeRunMode.tsx';
import { WelcomeLocalSetup } from './WelcomeLocalSetup.tsx';
import { writeWelcomePhase, type WelcomeEntry } from './welcomeProgress.ts';
import { detectInstallScenario } from '@/pages/Home/installScenario.ts';

// Even module initialization for connection/identity stays outside the browser-only tour.
const WelcomeConnection = lazy(() => import('./WelcomeConnection.tsx'));
export function WelcomeFlow({ entry, localBuild = false }: { entry: WelcomeEntry; localBuild?: boolean }) {
  const [queryClient] = useState(() => new QueryClient({ defaultOptions: { queries: { retry: false } } }));
  const [phase, setPhase] = useState<WelcomeEntry>(() => {
    if (entry !== 'editor') writeWelcomePhase(entry);
    return entry;
  });
  const [windowMode, setWindowMode] = useState<WindowMode>('app-window');
  const [runMode, setRunMode] = useState<RunMode>(entry === 'local' ? 'local' : 'hosted');
  const enter = useCallback((next: 'choose' | 'connection' | 'local') => {
    writeWelcomePhase(next);
    setPhase(next);
  }, []);
  const finishTour = useCallback(() => enter(localBuild || detectInstallScenario() === 'mobile' ? 'connection' : 'choose'), [enter, localBuild]);
  return <QueryClientProvider client={queryClient}><TooltipProvider><MemoryRouter>
    {phase === 'tour' && <BrowserTourEditor onFinish={finishTour} />}
    {phase === 'choose' && <WelcomeRunMode onContinue={enter} windowMode={windowMode} setWindowMode={setWindowMode} runMode={runMode} setRunMode={setRunMode} />}
    {phase === 'local' && <WelcomeLocalSetup onBack={() => enter('choose')} />}
    {phase === 'connection' && <Suspense fallback={<><EditorBackdrop /><p role="status" className="sr-only">Connecting to Astrid…</p></>}><WelcomeConnection windowMode={windowMode} /></Suspense>}
    {phase === 'editor' && null}
  </MemoryRouter></TooltipProvider></QueryClientProvider>;
}
