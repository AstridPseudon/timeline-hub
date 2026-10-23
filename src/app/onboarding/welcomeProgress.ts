import { APP_ENTRY_PATH } from '@/app/entryClassification.ts';

export const WELCOME_PROGRESS_KEY = 'astrid:welcome-v1';
export type WelcomePhase = 'tour' | 'connection' | 'complete';
let memoryPhase: WelcomePhase | null = null;

export function readWelcomePhase(): WelcomePhase | null {
  try {
    const value = localStorage.getItem(WELCOME_PROGRESS_KEY);
    return value === 'tour' || value === 'connection' || value === 'complete' ? value : null;
  } catch { return memoryPhase; }
}
export function writeWelcomePhase(phase: WelcomePhase): void {
  memoryPhase = phase;
  try { localStorage.setItem(WELCOME_PROGRESS_KEY, phase); } catch { /* This visit still progresses. */ }
}

/** Only an unselected editor entry belongs to welcome. Explicit work links always win. */
export function shouldShowWelcome(url: URL): boolean {
  if (url.pathname !== APP_ENTRY_PATH) return false;
  if ([...url.searchParams.keys()].some(key => key !== 'connect')) return false;
  const phase = readWelcomePhase();
  if (phase === 'complete') return false;
  if (phase) return true;
  try {
    return localStorage.getItem('astrid.runtime.connectedBefore') !== '1'
      && localStorage.getItem('astrid-setup-complete') !== 'true'
      && localStorage.getItem('astrid-editor-tour-v1') === null
      && localStorage.getItem('astrid:lastOpenedLocalProjectSlug') === null;
  } catch { return false; } // Don't trap storage-blocked returning visits.
}

export function welcomeEntryPhase(url: URL): 'tour' | 'connection' {
  return readWelcomePhase() === 'connection' || url.searchParams.get('connect') === '1' ? 'connection' : 'tour';
}

export function completeWelcome(selection?: {projectId: string; timelineId: string | null}): string {
  writeWelcomePhase('complete');
  try {
    localStorage.setItem('astrid-setup-complete', 'true');
    localStorage.setItem('astrid-editor-tour-v1', '1');
  } catch { /* The explicit destination below also bypasses welcome. */ }
  const params = new URLSearchParams();
  if (selection) {
    params.set('project', selection.projectId);
    if (selection.timelineId) params.set('timeline', selection.timelineId);
  }
  return `${APP_ENTRY_PATH}${params.size ? `?${params}` : ''}`;
}
