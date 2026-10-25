// @vitest-environment-options {"url":"https://astrid.haus/tools/video-editor?project=p1&timeline=t1#frame-42"}
import { act, cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { setRuntimeOrigin } from '@/integrations/runtime/connection.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { RuntimeConnectionGate, RuntimeConnectionProvider, type RuntimeConnectionValue } from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { connectionFor } from '@/shared/components/RuntimeConnection/connectionFixture.ts';
import WelcomeConnection from '@/app/onboarding/WelcomeConnection.tsx';
import { connectionStepFor, readWelcomePhase, writeWelcomePhase } from '@/app/onboarding/welcomeProgress.ts';
import { EditorConnectionPanel } from './RuntimeDocumentBoundary.tsx';

// The step is the only screen for a connection that needs the person; StarterProjectHandoff is not what a return runs.
vi.mock('@/app/onboarding/StarterProjectHandoff.tsx', () => ({
  StarterProjectHandoff: () => <div data-testid="starter-project-handoff" />,
}));
vi.mock('@/integrations/runtime/localNetworkPermission.ts', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/integrations/runtime/localNetworkPermission.ts')>();
  return { ...actual, requiresLocalNetworkPermission: () => true };
});

const replace = vi.fn();
const permission = { state: 'granted', onchange: null as ((this: unknown, event: Event) => unknown) | null };

/** jsdom cannot navigate and its Location methods are unforgeable: keep the real window, replace only the location. */
function stubLocation(href: string) {
  const url = new URL(href);
  const location = { href: url.href, origin: url.origin, pathname: url.pathname, search: url.search, hash: url.hash, assign: vi.fn(), replace };
  const browserWindow = window;
  vi.stubGlobal('window', new Proxy(browserWindow, { get(target, property) {
    if (property === 'location') return location;
    const value = Reflect.get(target, property, target);
    return ['addEventListener', 'removeEventListener', 'dispatchEvent', 'matchMedia'].includes(String(property)) && typeof value === 'function' ? value.bind(target) : value;
  } }));
}

const EDITOR_URL = 'https://astrid.haus/tools/video-editor?project=p1&timeline=t1#frame-42';

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  writeWelcomePhase(null);
  replace.mockReset();
  permission.state = 'granted';
  setRuntimeOrigin({ VITE_RUNTIME_ORIGIN: 'http://127.0.0.1:17340' });
  vi.spyOn(navigator, 'platform', 'get').mockReturnValue('MacIntel');
  vi.spyOn(navigator, 'userAgent', 'get').mockReturnValue('Mozilla/5.0 (Macintosh) Chrome/141.0.0.0 Safari/537.36');
  Object.defineProperty(navigator, 'permissions', { configurable: true, value: { query: vi.fn(async () => permission) } });
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('editor gate', () => {
  const panel = (state: RuntimeConnectionValue['state'], exit: { left: () => void } | null = null) =>
    render(<EditorConnectionPanel connection={connectionFor(state)} exit={exit} />);

  it.each(['needs_permission', 'blocked', 'not_running', 'refused', 'browser_update_needed', 'unsupported'] as const)(
    '%s sends the page to the connection step, returning to this address',
    async (status) => {
      stubLocation(EDITOR_URL);
      panel({ status });
      await waitFor(() => expect(replace).toHaveBeenCalledOnce());
      const step = new URL(replace.mock.calls[0]![0] as string, 'https://astrid.haus');
      expect(step.pathname).toBe('/tools/video-editor');
      expect(step.searchParams.get('connect')).toBe('1');
      expect(step.searchParams.get('return')).toBe('/tools/video-editor?project=p1&timeline=t1#frame-42');
      expect(replace.mock.calls[0]![0]).toBe(connectionStepFor(new URL(EDITOR_URL)));
      // No card flashes over the editor on the way out.
      expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'connecting');
    },
  );

  it.each([
    ['connecting', { status: 'connecting' }],
    ['phone', { status: 'phone' }],
    ['restart', { status: 'restart' }],
    ['update_needed', { status: 'update_needed' }],
  ] as const)('%s keeps its own screen and does not redirect', (_name, state) => {
    stubLocation(EDITOR_URL);
    panel(state);
    expect(replace).not.toHaveBeenCalled();
  });

  it.each(['not_running', 'refused', 'blocked'] as const)('does not redirect once connected (%s drawn on the way out)', (status) => {
    stubLocation(EDITOR_URL);
    panel({ status }, { left: () => {} });
    expect(replace).not.toHaveBeenCalled();
  });
});

describe('connection step with a return address', () => {
  function door() {
    return vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      const json = (body: unknown) => new Response(JSON.stringify(body), { status: 200, headers: { 'Content-Type': 'application/json' } });
      if (url.endsWith('/v1/health')) return json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST });
      if (url.endsWith('/v1/realm')) return json({ realm_id: 'r', display_name: 'Studio' });
      throw new Error(`Unexpected request ${url}`);
    });
  }

  it('connects, then goes back to the original editor address, not to a starter project', async () => {
    stubLocation(`https://astrid.haus${connectionStepFor(new URL(EDITOR_URL))}`);
    vi.stubGlobal('fetch', door());
    render(<WelcomeConnection onBack={() => {}} />);
    await waitFor(() => expect(replace).toHaveBeenCalledOnce(), { timeout: 5000 });
    expect(replace).toHaveBeenCalledWith('/tools/video-editor?project=p1&timeline=t1#frame-42');
    expect(screen.queryByTestId('starter-project-handoff')).not.toBeInTheDocument();
    expect(readWelcomePhase()).toBe('complete');
  });

  it('stays on the step, with no way back to the editor, while Astrid is unreachable', async () => {
    stubLocation(`https://astrid.haus${connectionStepFor(new URL(EDITOR_URL))}`);
    vi.stubGlobal('fetch', vi.fn(async () => { throw new TypeError('Failed to fetch'); }));
    render(<WelcomeConnection onBack={() => {}} />);
    await waitFor(() => expect(screen.getByTestId('runtime-not-connected')).toHaveAttribute('data-state', 'not_running'), { timeout: 15000 });
    expect(replace).not.toHaveBeenCalled();
    // A returning visitor has no tour to go Back to.
    expect(screen.queryByRole('button', { name: 'Back' })).not.toBeInTheDocument();
  }, 20000);
});

describe('editor gate: the permission is lost after a connection', () => {
  const door = () => vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    const json = (body: unknown) => new Response(JSON.stringify(body), { status: 200, headers: { 'Content-Type': 'application/json' } });
    if (url.endsWith('/v1/health')) return json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST });
    if (url.endsWith('/v1/realm')) return json({ realm_id: 'r', display_name: 'Studio' });
    throw new Error(`Unexpected request ${url}`);
  });

  it.each(['prompt', 'denied'] as const)('goes to the connection step with its return address when the permission becomes %s', async (lost) => {
    stubLocation(EDITOR_URL);
    vi.stubGlobal('fetch', door());
    render(
      <RuntimeConnectionProvider gated requireLocalNetworkPermission pollIntervalMs={600_000}>
        <RuntimeConnectionGate panel={(connection, exit) => <EditorConnectionPanel connection={connection} exit={exit} />}>
          <div data-testid="editor" />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );
    await waitFor(() => expect(screen.getByTestId('editor')).toBeInTheDocument());
    await waitFor(() => expect(screen.queryByTestId('runtime-not-connected')).not.toBeInTheDocument(), { timeout: 5000 });
    expect(replace).not.toHaveBeenCalled();

    // Site data cleared or the permission revoked, possibly in another tab: Chrome says so on the tab's return.
    permission.state = lost;
    await act(async () => { window.dispatchEvent(new Event('focus')); });
    await waitFor(() => expect(replace).toHaveBeenCalledOnce());
    expect(replace).toHaveBeenCalledWith(connectionStepFor(new URL(EDITOR_URL)));
    // Never "stopped": no claim about Astrid is made without the permission.
    expect(screen.queryByText(/Astrid stopped|isn't answering|running but/)).not.toBeInTheDocument();
  });
});
