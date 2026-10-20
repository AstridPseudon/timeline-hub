/**
 * The boot gate for the hosted build (Plan A, D3).
 *
 * On the hosted build the page and the Runtime are on different origins (`runtimeOrigin()` is the loopback
 * gateway), so the page must find out whether it can reach the Runtime before anything reads it:
 *
 *   permission (`local-network-access`) -> probe (`GET <runtime base>/v1/health`, then `/v1/realm`) -> queries
 *
 * - `granted`: probe at once, then re-check every few seconds and on focus until connected.
 * - `prompt`: send nothing. `awaitingConnect` is true; `connect()` probes without a timeout, which is what makes
 *   Chrome ask. Re-checking stays off until the browser reports `granted` (the permission's `onchange`).
 * - `denied`: `blocked`, nothing sent.
 *
 * A changed realm or identity asks for a restart at once. Otherwise two failed readings show setup help, or start
 * help if this browser connected before or the gateway answered. Background probes leave the current panel in place
 * while they run. Browsers without this permission probe directly. Once connected the
 * state is sticky: a Runtime that stops later shows a recovery card, keeping the editor and its unsaved work mounted.
 *
 * The first connection also marks this browser as one that chose the app (`rememberAppEntryPreference`), so the next
 * visit to the bare domain skips the landing page. The gate only exists on the hosted build, so a same-origin build
 * never sets it.
 *
 * Same-origin builds (no `VITE_RUNTIME_ORIGIN`: local dev, Plan B's relay) are not gated. `gated` is false, nothing
 * is probed, and the gate renders its children at once.
 *
 * The panel and pill are render props with a placeholder default each, so the real ones are plugged in here and
 * `Layout.tsx` is not edited again.
 */
import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { requireContextValue } from '@/shared/contexts/contextGuard';
import { rememberAppEntryPreference } from '@/app/entryClassification';
import {
  queryLocalNetworkPermission,
  watchLocalNetworkPermission,
  type LocalNetworkPermissionState,
  type PermissionsLike,
} from './localNetworkPermission.ts';
import {
  runtimeApiBase,
  runtimeOrigin,
  type RuntimeConnectionState,
} from './connection.ts';
import { autoConnectRequested, takeAutoConnectRequest } from './autoConnectRequest.ts';
import type { Realm } from './generated.ts';

const POLL_INTERVAL_MS = 3000;
const PROBE_TIMEOUT_MS = 5000;
const CONNECTED_BEFORE_KEY = 'astrid.runtime.connectedBefore';
/** The `error` codes of the Runtime door's refusals (astrid-runtime runtime_protocol/door.py): the only error bodies the page reads as the door's. */
export type RuntimeRefusalCode = 'runtime_unavailable' | 'runtime_identity_mismatch';
const GATEWAY_REFUSAL_OUTCOMES: Readonly<Record<RuntimeRefusalCode, 'down' | 'restart'>> = Object.freeze({
  runtime_unavailable: 'down',
  runtime_identity_mismatch: 'restart',
});

type RealmSummary = Pick<Realm, 'realm_id' | 'display_name'>;

export type RuntimeProbeOutcome =
  | { kind: 'connected'; realm: RealmSummary }
  | { kind: 'restart' }
  | { kind: 'down' }
  | { kind: 'silent' };

async function readJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    return undefined;
  }
}

/**
 * Asks the Runtime who it is, the way the gateway does: health, then realm. Never throws. An answer that is not
 * documented refusal codes at their refusal statuses count; unrelated servers and malformed responses are `silent`.
 */
export async function probeRuntime(
  signal?: AbortSignal,
  fetchImpl: typeof fetch = (input, init) => fetch(input, init),
): Promise<RuntimeProbeOutcome> {
  const base = runtimeApiBase();
  const get = async (path: string): Promise<RuntimeProbeOutcome | { body: unknown }> => {
    let response: Response;
    try {
      response = await fetchImpl(`${base}${path}`, { signal, cache: 'no-store' });
    } catch {
      return { kind: 'silent' };
    }
    const body = await readJson(response);
    if ((response.status === 502 || response.status === 503) && typeof body === 'object' && body !== null && 'error' in body) {
      const kind = typeof body.error === 'string' ? GATEWAY_REFUSAL_OUTCOMES[body.error] : undefined;
      if (kind) return { kind };
    }
    if (response.status !== 200) return { kind: 'silent' };
    return { body };
  };

  const health = await get('/v1/health');
  if ('kind' in health) return health;
  if (typeof health.body !== 'object' || health.body === null || typeof (health.body as { status?: unknown }).status !== 'string') {
    return { kind: 'silent' };
  }
  const realm = await get('/v1/realm');
  if ('kind' in realm) return realm;
  const { realm_id, display_name } = (realm.body ?? {}) as Partial<RealmSummary>;
  if (typeof realm_id !== 'string' || typeof display_name !== 'string') return { kind: 'silent' };
  return { kind: 'connected', realm: { realm_id, display_name } };
}

function readConnectedBefore(): boolean {
  try {
    return window.localStorage.getItem(CONNECTED_BEFORE_KEY) === '1';
  } catch {
    return false;
  }
}

function writeConnectedBefore(): void {
  try {
    window.localStorage.setItem(CONNECTED_BEFORE_KEY, '1');
  } catch {
    // Private window or blocked storage: the panel just keeps its first-time wording.
  }
}

export interface RuntimeConnectionValue {
  /** True on the hosted build (a Runtime origin is configured). False means same-origin: nothing is probed. */
  gated: boolean;
  state: RuntimeConnectionState;
  isConnected: boolean;
  /** The permission or the first probe is still pending: nothing can be shown yet, so the app renders nothing. */
  isBooting: boolean;
  /** An explicit Connect probe is in flight; background checks never enter a visible checking state. */
  isChecking: boolean;
  /** The permission is `prompt`: nothing has been sent and `connect()` is what asks Chrome. */
  awaitingConnect: boolean;
  /** The connected Runtime's realm display name, for the pill. */
  realmName: string | null;
  /** Probes now without a timeout, so Chrome's permission prompt can stay open. No-op when connected, denied or checking. */
  connect: () => void;
}

const RuntimeConnectionContext = createContext<RuntimeConnectionValue | undefined>(undefined);

export interface RuntimeConnectionProviderProps {
  children: React.ReactNode;
  /** Override for tests; defaults to "a Runtime origin is configured". */
  gated?: boolean;
  /** Override for tests; defaults to `navigator.permissions`. */
  permissions?: PermissionsLike;
  /** Override for tests; defaults to `fetch`. */
  fetchImpl?: typeof fetch;
  pollIntervalMs?: number;
  /** Called each time the connection comes up (once per page): where Runtime queries are invalidated. */
  onConnected?: () => void;
}

export function RuntimeConnectionProvider({
  children,
  gated = runtimeOrigin() !== '',
  permissions,
  fetchImpl,
  pollIntervalMs = POLL_INTERVAL_MS,
  onConnected,
}: RuntimeConnectionProviderProps) {
  const [permission, setPermission] = useState<LocalNetworkPermissionState | null>(null);
  const [outcome, setOutcome] = useState<RuntimeProbeOutcome | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [failedReadings, setFailedReadings] = useState(0);
  const [gatewayAnswered, setGatewayAnswered] = useState(false);
  const [connectedBefore, setConnectedBefore] = useState(() => gated && readConnectedBefore());

  const mounted = useRef(true);
  const inFlight = useRef<AbortController | null>(null);
  /** The untimed probe `connect()` started while the permission was not yet granted: the one a grant must replace. */
  const promptProbe = useRef<AbortController | null>(null);
  /** Sticky once a probe connects (set in `runProbe`, before the render): no probe starts after it. */
  const connectedRef = useRef(false);
  const permissionRef = useRef(permission);
  permissionRef.current = permission;
  const onConnectedRef = useRef(onConnected);
  onConnectedRef.current = onConnected;

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      inFlight.current?.abort();
    };
  }, []);

  // The permission, and every change the browser reports to it.
  useEffect(() => {
    if (!gated) return undefined;
    let cancelled = false;
    let unwatch: () => void = () => {};
    void (async () => {
      const stop = await watchLocalNetworkPermission((next) => {
        if (!cancelled) setPermission(next);
      }, permissions);
      if (cancelled) {
        stop();
        return;
      }
      unwatch = stop;
      const current = await queryLocalNetworkPermission(permissions);
      if (!cancelled) setPermission(current);
    })();
    return () => {
      cancelled = true;
      unwatch();
    };
  }, [gated, permissions]);

  const runProbe = useCallback(async (untimed: boolean) => {
    if (inFlight.current || connectedRef.current) return;
    const controller = new AbortController();
    inFlight.current = controller;
    if (untimed && permissionRef.current !== 'granted') promptProbe.current = controller;
    setIsChecking(untimed);
    const timer = untimed ? undefined : setTimeout(() => controller.abort(), PROBE_TIMEOUT_MS);
    let result: RuntimeProbeOutcome;
    try {
      result = await probeRuntime(controller.signal, fetchImpl);
    } finally {
      clearTimeout(timer);
    }
    // A grant replaced this probe (see the granted effect): its abort is not an answer, and the new probe owns the state.
    if (inFlight.current !== controller) return;
    inFlight.current = null;
    if (promptProbe.current === controller) promptProbe.current = null;
    if (!mounted.current) return;
    setIsChecking(false);
    if (connectedRef.current) return;
    // Latch the connection now, not on the render that `setOutcome` schedules: `inFlight` is already clear, and an
    // interval tick or focus event that lands before that render would otherwise start a second probe.
    if (result.kind === 'connected') {
      connectedRef.current = true;
    }
    setFailedReadings((previous) => result.kind === 'connected' ? 0 : previous + 1);
    if (result.kind === 'down') setGatewayAnswered(true);
    setOutcome(result);
    if (result.kind !== 'connected' && permissionRef.current !== 'granted') {
      // A denied fetch looks like nothing listening, so the permission is the only way to tell them apart.
      const current = await queryLocalNetworkPermission(permissions);
      if (mounted.current) setPermission(current);
    }
  }, [fetchImpl, permissions]);

  const isConnected = outcome?.kind === 'connected';

  // Granted: probe at once, then on an interval and on focus, until connected.
  useEffect(() => {
    if (!gated || permission !== 'granted' || isConnected) return undefined;
    // A probe started under `prompt` is untimed and stays pending until the person answers Chrome; once the answer
    // is `granted` it is replaced by a fresh one (`runProbe` would otherwise return at once because it is in flight).
    if (promptProbe.current && inFlight.current === promptProbe.current) {
      inFlight.current.abort();
      inFlight.current = null;
      promptProbe.current = null;
    }
    const check = () => void runProbe(false);
    check();
    const interval = setInterval(check, pollIntervalMs);
    window.addEventListener('focus', check);
    return () => {
      clearInterval(interval);
      window.removeEventListener('focus', check);
    };
  }, [gated, permission, isConnected, pollIntervalMs, runProbe]);

  useEffect(() => {
    if (!isConnected) return;
    writeConnectedBefore();
    // A visitor who has reached their Runtime from this browser goes straight into the app the next time they open
    // the bare domain (`resolveReturningAppEntry`); the landing page stays for first visits and /home.
    rememberAppEntryPreference();
    setConnectedBefore(true);
    onConnectedRef.current?.();
  }, [isConnected]);

  const connect = useCallback(() => {
    if (!gated || connectedRef.current || permissionRef.current === 'denied') return;
    void runProbe(true);
  }, [gated, runProbe]);

  const value = useMemo<RuntimeConnectionValue>(() => {
    if (!gated) {
      return {
        gated: false,
        state: { status: 'connected', realm: { realm_id: '', display_name: '' } },
        isConnected: true,
        isBooting: false,
        isChecking: false,
        awaitingConnect: false,
        realmName: null,
        connect,
      };
    }
    const base = { gated: true, isChecking, connect } as const;
    if (outcome?.kind === 'connected') {
      return { ...base, state: { status: 'connected', realm: outcome.realm }, isConnected: true, isBooting: false, awaitingConnect: false, realmName: outcome.realm.display_name };
    }
    const notConnected = { ...base, isConnected: false, realmName: null, awaitingConnect: permission === 'prompt' };
    if (permission === null) return { ...notConnected, state: { status: 'connecting' }, isBooting: true };
    if (permission === 'denied') return { ...notConnected, state: { status: 'blocked' }, isBooting: false };
    if (permission === 'prompt') return { ...notConnected, state: { status: 'connecting' }, isBooting: false };
    if (outcome?.kind === 'restart') return { ...notConnected, state: { status: 'restart_needed' }, isBooting: false };
    if (failedReadings >= 2) {
      return { ...notConnected, state: { status: connectedBefore || gatewayAnswered ? 'not_running' : 'set_up' }, isBooting: false };
    }
    // Boot ends after the first answer; the second reading only decides which recovery panel to show.
    return { ...notConnected, state: { status: 'connecting' }, isBooting: outcome === null };
  }, [gated, outcome, permission, isChecking, connectedBefore, connect, failedReadings, gatewayAnswered]);

  return <RuntimeConnectionContext.Provider value={value}>{children}</RuntimeConnectionContext.Provider>;
}

export const useRuntimeConnection = (): RuntimeConnectionValue =>
  requireContextValue(useContext(RuntimeConnectionContext), 'useRuntimeConnection', 'RuntimeConnectionProvider');

/** Placeholder until the real panel is plugged in (A2.P): the state name and nothing else. */
function PlaceholderPanel({ state }: RuntimeConnectionValue) {
  return (
    <div
      role="status"
      data-testid="runtime-not-connected"
      data-state={state.status}
      className="grid min-h-screen place-items-center bg-background text-muted-foreground"
    >
      {state.status}
    </div>
  );
}

export interface RuntimeConnectionGateProps {
  children: React.ReactNode;
  /** Rendered instead of `children` while the Runtime is not connected. */
  panel?: (connection: RuntimeConnectionValue) => React.ReactNode;
  /** Rendered beside `children` once connected. Nothing until A2.P. */
  pill?: (connection: RuntimeConnectionValue) => React.ReactNode;
}

/**
 * Renders `children` once the Runtime is connected, and `panel` until then. A same-origin build renders `children`
 * at once. The default `panel` and `pill` are the places A2.P replaces.
 */
export function RuntimeConnectionGate({
  children,
  panel = (connection) => <PlaceholderPanel {...connection} />,
  pill = () => null,
}: RuntimeConnectionGateProps) {
  const connection = useRuntimeConnection();
  // The landing page's "use it right here" click asked to go in (`autoConnectRequest.ts`): the flag is read once, in the
  // first render, so the explainer is never painted for the frame before the effect below asks Chrome.
  const [autoConnect, setAutoConnect] = useState(autoConnectRequested);
  const { gated, awaitingConnect, isBooting, isConnected, connect } = connection;
  useEffect(() => {
    if (!gated || !autoConnect) return;
    if (awaitingConnect) {
      // The flag is one-shot: after it is used, a later `prompt` (a permission reset) shows the explainer again.
      if (takeAutoConnectRequest()) connect();
      setAutoConnect(false);
    } else if (isConnected || !isBooting) {
      // The permission was not `prompt` (granted or denied), so the flag has nothing to do and must not linger.
      takeAutoConnectRequest();
      setAutoConnect(false);
    }
  }, [gated, autoConnect, awaitingConnect, isBooting, isConnected, connect]);
  if (!gated) return <>{children}</>;
  if (!connection.isConnected) {
    // While the flag is waiting for its effect, the panel shows Chrome's prompt screen, not the explainer.
    const shown = autoConnect && awaitingConnect ? { ...connection, isChecking: true } : connection;
    return <>{panel(shown)}</>;
  }
  return (
    <>
      {pill(connection)}
      {children}
    </>
  );
}
