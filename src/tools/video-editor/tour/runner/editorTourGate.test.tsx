// @vitest-environment jsdom
import { render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  RuntimeConnectionGate,
  RuntimeConnectionProvider,
} from '@/integrations/runtime/RuntimeConnectionProvider.tsx';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { exitEditorTour, getEditorTourState } from '@/shared/state/editorTourStore.ts';
import { useEditorTourHost } from './useEditorTourHost';

vi.mock('@/shared/hooks/mobile', () => ({
  useIsMobile: () => false,
  useIsTablet: () => false,
  useViewportWidth: () => 1440,
  isTabletHardware: () => false,
}));

const json = (body: unknown) => new Response(JSON.stringify(body), { status: 200, headers: { 'Content-Type': 'application/json' } });

/** A Runtime that answers or does not, switchable between probes. */
function fakeRuntime() {
  let up = false;
  const fetchImpl = vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    if (url.endsWith('/v1/health')) {
      if (!up) throw new TypeError('Failed to fetch');
      return json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST });
    }
    if (url.endsWith('/v1/realm')) return json({ realm_id: 'realm-1', display_name: 'Direct Journey' });
    throw new Error(`unexpected request ${url}`);
  }) as unknown as typeof fetch;
  return { fetchImpl, start: () => { up = true; } };
}

/** What VideoEditorPage does: the tour host runs with the user's selection once the page is mounted. */
function EditorPage() {
  useEditorTourHost(true);
  return <div data-testid="editor" />;
}

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
});

afterEach(() => {
  exitEditorTour();
  localStorage.clear();
});

describe('the editor tour and the connection gate', () => {
  it('cannot start under the connection cards or the Connected moment: the page is not mounted until the gate opens', async () => {
    const runtime = fakeRuntime();
    render(
      <RuntimeConnectionProvider gated fetchImpl={runtime.fetchImpl} permissions={{ query: vi.fn(async () => ({ state: 'granted', onchange: null })) } as never} pollIntervalMs={10}>
        <RuntimeConnectionGate
          panel={({ state }) => <p data-testid="panel">{state.status}</p>}
          connected={() => <p data-testid="moment">Connected</p>}
        >
          <EditorPage />
        </RuntimeConnectionGate>
      </RuntimeConnectionProvider>,
    );

    await waitFor(() => expect(screen.getByTestId('panel')).toHaveTextContent('set_up'));
    expect(getEditorTourState().status).toBe('idle');

    runtime.start();
    await waitFor(() => expect(screen.getByTestId('moment')).toBeInTheDocument());
    expect(screen.queryByTestId('editor')).toBeNull();
    expect(getEditorTourState().status).toBe('idle');
    expect(localStorage.getItem('astrid-editor-tour-v1')).toBeNull();

    await waitFor(() => expect(screen.getByTestId('editor')).toBeInTheDocument(), { timeout: 3000 });
    expect(screen.queryByTestId('moment')).toBeNull();
    expect(getEditorTourState().status).toBe('running');
  });
});
