import { useEffect, useRef, useState } from 'react';
import { runtimeApiBase } from '@/integrations/runtime/connection.ts';

/**
 * Notices, while connected, that the Runtime restarted or changed realm (Plan A, D3).
 *
 * The client fences a restarted Runtime only when a request reaches it, and a connected page that is reading
 * nothing would never make one. So this asks the health route on an interval and on focus: the instance id seen
 * at the first answer is the baseline, and a different id is a restart. A gateway 503 `realm_changed` is a
 * different workspace. Both are sticky: once seen, the page keeps its drafts and waits for Reload.
 * Anything else (the Runtime briefly down, a network error) is not a restart and changes nothing.
 */

export type RuntimeRestartStatus = 'ok' | 'restarted' | 'realm_changed';

export const RESTART_CHECK_INTERVAL_MS = 3000;

type HealthReading =
  | { kind: 'instance'; instanceId: string }
  | { kind: 'realm_changed' }
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
  try {
    response = await fetchImpl(`${runtimeApiBase()}/v1/health`, { cache: 'no-store' });
  } catch {
    return { kind: 'unknown' };
  }
  if (response.status === 503) {
    const body = await readJson(response);
    const code = typeof body === 'object' && body !== null ? (body as { error?: unknown }).error : undefined;
    return code === 'realm_changed' ? { kind: 'realm_changed' } : { kind: 'unknown' };
  }
  if (!response.ok) return { kind: 'unknown' };
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

  useEffect(() => {
    if (!enabled || status !== 'ok') return undefined;
    let stopped = false;
    let inFlight = false;
    const check = async () => {
      if (inFlight) return;
      inFlight = true;
      try {
        const reading = await readHealth(fetchImpl);
        if (stopped) return;
        if (reading.kind === 'realm_changed') {
          setStatus('realm_changed');
        } else if (reading.kind === 'instance') {
          if (baselineRef.current === null) baselineRef.current = reading.instanceId;
          else if (reading.instanceId !== baselineRef.current) setStatus('restarted');
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
  }, [enabled, status, intervalMs, fetchImpl]);

  return status;
}
