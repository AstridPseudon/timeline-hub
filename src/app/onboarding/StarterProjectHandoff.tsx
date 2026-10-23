import { useEffect, useRef, useState } from 'react';
import { Button } from '@/shared/components/ui/button.tsx';
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
export function StarterProjectHandoff({ onReady }: { onReady: (selection: StarterProjectSelection) => void }) {
  const [intentId] = useState(projectIntent);
  const [attempt, setAttempt] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const onReadyRef = useRef(onReady);
  onReadyRef.current = onReady;
  const pending = useRef<Promise<StarterProjectSelection> | null>(null);
  useEffect(() => {
    let active = true;
    pending.current ??= prepareStarterProject({ intentId, preferredProjectId: preferredProject() });
    void pending.current.then(selection => {
      if (!active) return;
      onReadyRef.current(selection);
      finishIntent(intentId);
    }, reason => {
      if (active) setError(reason instanceof Error ? reason.message : 'Please retry project setup.');
    });
    return () => { active = false; };
  }, [attempt, intentId]);
  const retry = () => {
    pending.current = null;
    setError(null);
    setAttempt(value => value + 1);
  };
  return <main className="flex min-h-screen items-center justify-center px-6">
    <div className="max-w-md space-y-4 text-center">
      <h1 className="text-2xl font-semibold">{error ? 'Couldn’t open your project' : 'Opening your project…'}</h1>
      {error ? <>
        <p role="alert" className="text-sm text-muted-foreground">{error}</p>
        <Button onClick={retry}>Retry project setup</Button>
      </> : <p role="status" className="text-sm text-muted-foreground">Your Runtime is connected. We’re getting your project ready.</p>}
    </div>
  </main>;
}
