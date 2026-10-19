import { useEffect, useRef, useState } from 'react';
import { runtimeApiBase } from '@/integrations/runtime/connection.ts';

/**
 * Notices, while connected, that Astrid stopped, restarted or changed.
 *
 * The client fences a restarted Runtime only when a request reaches it, and a connected page that is reading
 * nothing would never make one. So this asks the health route on an interval and on focus: the instance id seen
 * at the first answer is the baseline, and a different id is a restart. The door's 503 `runtime_identity_mismatch` (its
 * credential now names another identity) is Astrid changed under the page. Both are sticky: once seen, the page keeps its
 * drafts and waits for Reload.
 *
 * Two readings in a row that fail are `stopped`. A failed reading is a network error (nothing answers, about 6 seconds),
 * a 503 that is not an identity change (the Runtime's door answers but the Runtime is not ready), or any other
 * answer that is not ok. That one is not sticky: a reading with the same instance clears it, and a new instance is a
 * restart. An ok answer that names no instance is not a restart and changes nothing.
 */

export type RuntimeRestartStatus = 'ok' | 'stopped' | 'restarted' | 'realm_changed';

export const RESTART_CHECK_INTERVAL_MS = 3000;

/** Failed readings in a row before the page says Astrid stopped: one dropped request is not a stop. */
const FAILURES_BEFORE_STOPPED = 2;
/** A health request that has not answered by now counts as a failed reading. */
const HEALTH_TIMEOUT_MS = 3000;

type HealthReading =
  | { kind: 'instance'; instanceId: string }
  | { kind: 'realm_changed' }
  | { kind: 'unreachable' }
  | { kind: 'unknown' };

type FetchLike = (input: string, init?: RequestInit) => Promise<Response>;

async function readJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    return undefined;
  }
}

async function readHealth(fetchImpl: FetchLike): Promise<HealthReading> {
  let response: Response;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);
  try {
    response = await fetchImpl(`${runtimeApiBase()}/v1/health`, { cache: 'no-store', signal: controller.signal });
  } catch {
    return { kind: 'unreachable' };
  } finally {
    clearTimeout(timer);
  }
  if (response.status === 503) {
    const body = await readJson(response);
    const code = typeof body === 'object' && body !== null ? (body as { error?: unknown }).error : undefined;
    // A door that answers 503 because the Runtime is not ready is as stopped as one that does not answer at all.
    return code === 'runtime_identity_mismatch' ? { kind: 'realm_changed' } : { kind: 'unreachable' };
  }
  if (!response.ok) return { kind: 'unreachable' };
  const body = await readJson(response);
  const instanceId = typeof body === 'object' && body !== null ? (body as { runtime_instance_id?: unknown }).runtime_instance_id : undefined;
  return typeof instanceId === 'string' && instanceId ? { kind: 'instance', instanceId } : { kind: 'unknown' };
}

// Module-level so the effect's dependency is stable across renders; an inline default would re-run the effect every render.
const browserFetch: FetchLike = (input, init) => fetch(input, init);

export function useRuntimeRestartWatch(
  enabled: boolean,
  { intervalMs = RESTART_CHECK_INTERVAL_MS, fetchImpl = browserFetch }: { intervalMs?: number; fetchImpl?: FetchLike } = {},
): RuntimeRestartStatus {
  const [status, setStatus] = useState<RuntimeRestartStatus>('ok');
  // A ref, not an effect-local: a re-run of the effect must not forget the instance the page connected to.
  const baselineRef = useRef<string | null>(null);
  const settled = status === 'restarted' || status === 'realm_changed';

  useEffect(() => {
    if (!enabled || settled) return undefined;
    let stopped = false;
    let inFlight = false;
    let failures = 0;
    const check = async () => {
      if (inFlight) return;
      inFlight = true;
      try {
        const reading = await readHealth(fetchImpl);
        if (stopped) return;
        if (reading.kind === 'unreachable') {
          failures += 1;
          if (failures >= FAILURES_BEFORE_STOPPED) setStatus((current) => (current === 'ok' ? 'stopped' : current));
          return;
        }
        failures = 0;
        if (reading.kind === 'realm_changed') {
          setStatus('realm_changed');
        } else if (reading.kind === 'instance') {
          if (baselineRef.current === null) baselineRef.current = reading.instanceId;
          if (reading.instanceId !== baselineRef.current) setStatus('restarted');
          else setStatus((current) => (current === 'stopped' ? 'ok' : current));
        }
      } finally {
        inFlight = false;
      }
    };
    void check();
    const interval = setInterval(() => void check(), intervalMs);
    window.addEventListener('focus', check);
    return () => {
      stopped = true;
      clearInterval(interval);
      window.removeEventListener('focus', check);
    };
  }, [enabled, settled, intervalMs, fetchImpl]);

  return status;
}

/**
 * Runs `onAnswers` whenever Astrid starts answering the health route after this hook saw it not answering, and never
 * again while it keeps answering. The first reading is only the baseline: a caller mounted because a load failed while
 * Astrid was answering must not retry at once, or retry, fail and remount would loop. A thing that failed to load because
 * Astrid was not there uses it to try again by itself, as the connection panel opens by itself.
 */
export function useOnAstridAnswers(
  onAnswers: () => void,
  { intervalMs = RESTART_CHECK_INTERVAL_MS, fetchImpl = browserFetch }: { intervalMs?: number; fetchImpl?: FetchLike } = {},
): void {
  const latest = useRef(onAnswers);
  useEffect(() => {
    latest.current = onAnswers;
  });
  useEffect(() => {
    let disposed = false;
    let inFlight = false;
    /** Null until the first reading, which only sets the baseline. */
    let answering: boolean | null = null;
    const check = async () => {
      if (inFlight) return;
      inFlight = true;
      try {
        const reading = await readHealth(fetchImpl);
        if (disposed) return;
        const nowAnswering = reading.kind === 'instance' || reading.kind === 'unknown';
        const started = nowAnswering && answering === false;
        answering = nowAnswering;
        if (started) latest.current();
      } finally {
        inFlight = false;
      }
    };
    void check();
    const interval = setInterval(() => void check(), intervalMs);
    window.addEventListener('focus', check);
    return () => {
      disposed = true;
      clearInterval(interval);
      window.removeEventListener('focus', check);
    };
  }, [intervalMs, fetchImpl]);
}
