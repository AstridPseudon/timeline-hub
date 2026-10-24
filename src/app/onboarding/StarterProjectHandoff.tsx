import { useEffect, useRef, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
import { useRuntimeRequestWait } from '@/integrations/runtime/useRuntimeRequestWait.ts';
import { prepareStarterProject, type StarterProjectSelection } from './prepareStarterProject.ts';

export const PENDING_STARTER_PROJECT_KEY = 'astrid:onboarding:pending-project-v1';
const LAST_PROJECT_KEY = 'astrid:lastOpenedLocalProjectSlug';
let memoryIntent: string | undefined;

function projectIntent(): string {
  try {
    const previous = localStorage.getItem(PENDING_STARTER_PROJECT_KEY);
    if (previous && /^[a-zA-Z0-9-]{1,80}$/.test(previous)) return previous;
    const id = crypto.randomUUID();
    localStorage.setItem(PENDING_STARTER_PROJECT_KEY, id);
    return id;
  } catch {
    return memoryIntent ??= crypto.randomUUID();
  }
}

function finishIntent(intentId: string): void {
  try {
    if (localStorage.getItem(PENDING_STARTER_PROJECT_KEY) === intentId) localStorage.removeItem(PENDING_STARTER_PROJECT_KEY);
  } catch { /* Runtime discovery still recovers a completed project without browser storage. */ }
  if (memoryIntent === intentId) memoryIntent = undefined;
}

function preferredProject(): string | null {
  try { return localStorage.getItem(LAST_PROJECT_KEY); } catch { return null; }
}

/** Mount only inside the connected Runtime gate. The intent is a retry token, never a project ID. */
export function StarterProjectHandoff({ onReady, onContinueWithoutProject }: {
  onReady: (selection: StarterProjectSelection) => void;
  onContinueWithoutProject?: () => void;
}) {
  const [intentId] = useState(projectIntent);
  const [attempt, setAttempt] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const onReadyRef = useRef(onReady);
  onReadyRef.current = onReady;
  const pending = useRef<{ controller: AbortController; result: Promise<StarterProjectSelection> } | null>(null);
  const stillWaiting = useRuntimeRequestWait(!error, attempt);
  useEffect(() => {
    let active = true;
    if (!pending.current) {
      const controller = new AbortController();
      pending.current = { controller, result: prepareStarterProject({
        intentId, preferredProjectId: preferredProject(), signal: controller.signal,
      }) };
    }
    const current = pending.current;
    void current.result.then(selection => {
      if (!active || pending.current !== current) return;
      onReadyRef.current(selection);
      finishIntent(intentId);
    }, reason => {
      if (active && pending.current === current) setError(reason instanceof Error ? reason.message : 'Please retry project setup.');
    });
    return () => { active = false; };
  }, [attempt, intentId]);
  const cancelAttempt = () => {
    pending.current?.controller.abort();
    pending.current = null;
  };
  const retry = () => {
    cancelAttempt();
    setError(null);
    setAttempt(value => value + 1);
  };
  return <main className="flex min-h-screen items-center justify-center px-6">
    <div className="max-w-md space-y-4 text-center">
      <h1 className="text-2xl font-semibold">{error ? 'Couldn’t open your project' : stillWaiting ? 'Still getting your project ready' : 'Opening your project…'}</h1>
      {error || stillWaiting ? <>
        <p role={error ? 'alert' : 'status'} className="text-sm text-muted-foreground">{error ?? 'Astrid is taking longer than usual to answer. You can keep waiting or retry.'}</p>
        <div className="flex flex-wrap justify-center gap-3">
          <Button onClick={retry}>Retry project setup</Button>
          {onContinueWithoutProject && <Button variant="outline" onClick={() => { cancelAttempt(); onContinueWithoutProject(); }}>Open editor</Button>}
        </div>
      </> : <p role="status" className="text-sm text-muted-foreground">Your Runtime is connected. We’re getting your project ready.</p>}
    </div>
  </main>;
}
