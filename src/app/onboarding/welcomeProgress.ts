import { APP_ENTRY_PATH } from '@/app/entryClassification.ts';
import { isWorkspaceRoute } from '@/app/runtime/runtimeDocument.ts';

export const WELCOME_PROGRESS_KEY = 'astrid:welcome-v1';
export type WelcomePhase = 'tour' | 'choose' | 'connection' | 'local' | 'complete';
export type WelcomeEntry = WelcomePhase | 'editor';
const LEGACY_KEYS = [
  'astrid.runtime.connectedBefore',
  'astrid-setup-complete',
  'astrid-editor-tour-v1',
  'astrid:lastOpenedLocalProjectSlug',
] as const;
let memoryPhase: WelcomePhase | null = null;

/** Fill in the durable record once for an existing browser profile. */
export function readWelcomePhase(): WelcomePhase | null {
  try {
    const value = localStorage.getItem(WELCOME_PROGRESS_KEY);
    if (value === 'tour' || value === 'choose' || value === 'connection' || value === 'local' || value === 'complete') return value;
    if (value !== null) return null;
    const returning = LEGACY_KEYS.some(key => localStorage.getItem(key) !== null);
    if (returning) {
      localStorage.setItem(WELCOME_PROGRESS_KEY, 'complete');
      memoryPhase = 'complete';
      return 'complete';
    }
    return memoryPhase;
  } catch { return memoryPhase; }
}

export function writeWelcomePhase(phase: WelcomePhase | null): void {
  memoryPhase = phase;
  try {
    if (phase === null) localStorage.removeItem(WELCOME_PROGRESS_KEY);
    else localStorage.setItem(WELCOME_PROGRESS_KEY, phase);
  } catch { /* This visit still progresses. */ }
}

/** Pick the only owner for this URL and phase. Work links take precedence over onboarding. */
export function entryFor(url: URL, phase: WelcomePhase | null, localBuild = false): WelcomeEntry {
  if (url.pathname !== APP_ENTRY_PATH) return 'editor';
  if (['project', 'timeline', 'localProject', 'localTimeline'].some(key => url.searchParams.has(key))) return 'editor';
  // The tour's explicit Open editor link can still work when browser storage is blocked.
  // The editor's normal Runtime gate remains responsible for connecting before workspace data loads.
  if (url.searchParams.get('entry') === 'editor') return 'editor';
  if (phase === 'local') return 'local';
  if (url.searchParams.get('connect') === '1') return 'connection';
  if (localBuild && phase === 'choose') return 'connection';
  return phase === 'complete' ? 'editor' : phase ?? 'tour';
}

export function completeWelcome(selection?: {projectId: string; timelineId: string | null}): string {
  writeWelcomePhase('complete');
  const params = new URLSearchParams();
  if (selection) {
    params.set('project', selection.projectId);
    if (selection.timelineId) params.set('timeline', selection.timelineId);
  } else params.set('entry', 'editor');
  return `${APP_ENTRY_PATH}${params.size ? `?${params}` : ''}`;
}

const RETURN_PARAM = 'return';

/**
 * The onboarding connection step for an editor page that cannot reach Astrid, carrying the page (project and timeline
 * deep link included) to come back to. `connect=1` is what `entryFor` resumes at connection; the one-shot `connect`
 * flag is dropped from the return address so it cannot start a second prompt on the way back.
 */
export function connectionStepFor(current: Pick<Location, 'pathname' | 'search' | 'hash'>): string {
  const back = new URLSearchParams(current.search);
  back.delete('connect');
  const here = `${current.pathname}${back.size ? `?${back}` : ''}${current.hash}`;
  return `${APP_ENTRY_PATH}?${new URLSearchParams({ connect: '1', [RETURN_PARAM]: here })}`;
}

/** The editor page the connection step was asked to return to: same origin and a workspace route only, else null. */
export function returnTargetFor(url: URL): string | null {
  const value = url.searchParams.get(RETURN_PARAM);
  if (!value) return null;
  try {
    const target = new URL(value, url.origin);
    if (target.origin !== url.origin || !isWorkspaceRoute(target.pathname)) return null;
    return `${target.pathname}${target.search}${target.hash}`;
  } catch {
    return null;
  }
}
