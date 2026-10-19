import { assertNativeEditorConnection } from '@/integrations/astrid/nativeEditorConnection.ts';
// @vitest-environment jsdom
import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useAstridBridgeDiscovery } from '@/tools/video-editor/hooks/useAstridBridgeDiscovery.ts';

vi.mock('@/integrations/astrid/nativeEditorConnection.ts',()=>({assertNativeEditorConnection:vi.fn(async()=>undefined)}));

const PROJECTS_PATH = '/api/astrid/v1/projects';
const TIMELINES_PATH = '/api/astrid/v1/projects/ados-talks/timelines';
const ADOS_TIMELINE_ID = '11111111-1111-1111-1111-111111111111';

const ADOS_PROJECT = {
  project_id: 'project-ados',
  slug: 'ados-talks',
  name: 'Ados Talks',
  version: 1,
  metadata: {},
  created_at: '2026-10-11T00:00:00Z',
  updated_at: '2026-10-11T00:00:00Z',
  archived: false,
};

const ADOS_TIMELINE = {
  timeline_id: ADOS_TIMELINE_ID,
  timeline_ulid: '01JM4K5N7P0000000000000017',
  slug: 'intro-cut',
  name: 'Intro Cut',
  is_default: true,
};

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

function jsonBody(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), { status });
}

/** Request paths without the query string, for counting calls per route. */
function countPath(calls: string[], path: string): number {
  return calls.filter((call) => call.split('?')[0] === path).length;
}

function makeBridgeFetch(overrides?: {
  projects?: () => Response | Promise<Response>;
  timelines?: () => Response | Promise<Response>;
}) {
  const calls: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    calls.push(url);
    if (url.startsWith(`${PROJECTS_PATH}?`)) {
      return overrides?.projects?.() ?? jsonBody({ items: [ADOS_PROJECT], next_cursor: null });
    }
    if (url.startsWith(`${TIMELINES_PATH}?`)) {
      return overrides?.timelines?.() ?? jsonBody({ items: [ADOS_TIMELINE], next_cursor: null });
    }
    throw new Error(`Unexpected bridge request: ${url}`);
  }));
  return calls;
}

afterEach(() => {
  vi.mocked(assertNativeEditorConnection).mockReset().mockResolvedValue(undefined);
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

describe('useAstridBridgeDiscovery', () => {
  it('reports privacy-bounded outcomes for discovery success and invalid payloads', async () => {
    const onBridgeRequest = vi.fn();
    makeBridgeFetch({
      timelines: () => jsonBody({ items: 'not-a-list', next_cursor: null }),
    });

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({
        open: true,
        currentLocal: true,
        selectedProjectSlug: 'ados-talks',
        onBridgeRequest,
      }),
      { wrapper: createWrapper() },
    );

    await waitFor(() => {
      expect(result.current.bridgeHealthy).toBe(true);
      expect(result.current.timelinesQuery.isError).toBe(true);
    });
    expect(onBridgeRequest).toHaveBeenCalledWith(expect.objectContaining({
      outcome: 'success',
      durationMs: expect.any(Number),
    }));
    expect(onBridgeRequest).toHaveBeenCalledWith(expect.objectContaining({
      outcome: 'failure',
      errorClass: 'bridge.invalid_response',
      durationMs: expect.any(Number),
    }));
    for (const observation of onBridgeRequest.mock.calls.flat()) {
      expect(observation).not.toHaveProperty('path');
      expect(observation).not.toHaveProperty('payload');
    }
  });

  it('classifies discovery timeouts separately from HTTP failures', async () => {
    const timeoutObserver = vi.fn();
    makeBridgeFetch({
      projects: () => Promise.reject(new DOMException('timed out', 'TimeoutError')),
    });
    const timeout = renderHook(
      () => useAstridBridgeDiscovery({
        open: true,
        currentLocal: true,
        selectedProjectSlug: null,
        onBridgeRequest: timeoutObserver,
      }),
      { wrapper: createWrapper() },
    );
    await waitFor(() => expect(timeout.result.current.projectsQuery.isError).toBe(true));
    expect(timeoutObserver).toHaveBeenCalledWith(expect.objectContaining({
      outcome: 'failure',
      errorClass: 'bridge.timeout',
    }));
    timeout.unmount();

    vi.unstubAllGlobals();
    const httpObserver = vi.fn();
    makeBridgeFetch({
      projects: () => new Response('unavailable', { status: 503 }),
    });
    const http = renderHook(
      () => useAstridBridgeDiscovery({
        open: true,
        currentLocal: true,
        selectedProjectSlug: null,
        onBridgeRequest: httpObserver,
      }),
      { wrapper: createWrapper() },
    );
    await waitFor(() => expect(http.result.current.projectsQuery.isError).toBe(true));
    expect(httpObserver).toHaveBeenCalledWith(expect.objectContaining({
      outcome: 'failure',
      errorClass: 'bridge.http_error',
    }));
  });

  it('probes the native editor connection, then fetches projects, then timelines for the selected project', async () => {
    const calls = makeBridgeFetch();

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({ open: true, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { wrapper: createWrapper() },
    );

    await waitFor(() => {
      expect(result.current.bridgeHealthy).toBe(true);
    });
    await waitFor(() => {
      expect(result.current.projectsQuery.data?.projects).toEqual([
        {
          slug: 'ados-talks',
          name: 'Ados Talks',
          project_id: 'project-ados',
          version: 1,
          created_at: '2026-10-11T00:00:00Z',
          metadata: {},
        },
      ]);
    });
    await waitFor(() => {
      expect(result.current.timelinesQuery.data?.timelines?.[0]?.timeline_id).toBe(ADOS_TIMELINE_ID);
    });

    // Health is the native probe, so projects only follow the bridge being healthy.
    expect(vi.mocked(assertNativeEditorConnection)).toHaveBeenCalled();
    const projectsIndex = calls.findIndex((c) => c.startsWith(`${PROJECTS_PATH}?`));
    const timelinesIndex = calls.findIndex((c) => c.startsWith(`${TIMELINES_PATH}?`));
    expect(projectsIndex).toBe(0);
    expect(timelinesIndex).toBeGreaterThan(projectsIndex);
  });

  it('does not fetch projects while the native probe reports the bridge down', async () => {
    vi.mocked(assertNativeEditorConnection).mockRejectedValue(new Error('Workspace discovery: 503'));
    const calls = makeBridgeFetch();

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({ open: true, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { wrapper: createWrapper() },
    );

    await waitFor(() => {
      expect(result.current.bridgeDown).toBe(true);
    });
    expect(result.current.projectsQuery.data).toBeUndefined();
    expect(result.current.timelinesQuery.data).toBeUndefined();
    expect(calls).toEqual([]);
  });

  it('refetches projects and timelines when the dropdown opens', async () => {
    const calls = makeBridgeFetch();

    const { result, rerender } = renderHook(
      ({ open }: { open: boolean }) =>
        useAstridBridgeDiscovery({ open, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { initialProps: { open: false }, wrapper: createWrapper() },
    );

    // In local mode the lists are fetched while closed (the page needs the
    // timelines to auto-pick), so opening the dropdown refetches them.
    await waitFor(() => {
      expect(result.current.projectsQuery.data?.projects?.length).toBe(1);
    });
    const closedProjectCalls = countPath(calls, PROJECTS_PATH);
    const closedTimelineCalls = countPath(calls, TIMELINES_PATH);
    expect(closedProjectCalls).toBeGreaterThanOrEqual(1);
    expect(closedTimelineCalls).toBeGreaterThanOrEqual(1);

    rerender({ open: true });

    await waitFor(() => {
      expect(countPath(calls, PROJECTS_PATH)).toBeGreaterThan(closedProjectCalls);
    });
    await waitFor(() => {
      expect(countPath(calls, TIMELINES_PATH)).toBeGreaterThan(closedTimelineCalls);
    });
  });

  it('polls the native probe every 3s while a local editor is waiting, then stops after success', async () => {
    vi.useFakeTimers();
    let healthy = false;
    const probe = vi.mocked(assertNativeEditorConnection);
    probe.mockClear().mockImplementation(async () => {
      if (!healthy) throw new Error('Workspace discovery: 503');
    });
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.startsWith(`${PROJECTS_PATH}?`)) {
        return jsonBody({ items: [ADOS_PROJECT], next_cursor: null });
      }
      throw new Error(`Unexpected bridge request: ${url}`);
    }));

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({ open: false, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { wrapper: createWrapper() },
    );

    // Initial probe settles once the microtask chain drains (the fake
    // timer advance below forces it).
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(probe.mock.calls.length).toBeGreaterThan(0);
    const initialCount = probe.mock.calls.length;

    // Bridge still down → the 3s poll keeps probing.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3_000);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(probe.mock.calls.length).toBeGreaterThan(initialCount);

    // Bridge comes up → next poll succeeds and polling stops.
    healthy = true;
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3_000);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(result.current.bridgeHealthy).toBe(true);
    const countAfterSuccess = probe.mock.calls.length;

    // No further polls while the local editor has a healthy bridge.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(9_000);
    });
    expect(probe.mock.calls.length).toBe(countAfterSuccess);
  });

  it('polls projects while open and the projects list is empty, stopping once populated', async () => {
    vi.useFakeTimers();
    let projects: (typeof ADOS_PROJECT)[] = [];
    const projectsCalls: string[] = [];
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.startsWith(`${PROJECTS_PATH}?`)) {
        projectsCalls.push(url);
        return { ok: true, json: async () => ({ items: projects, next_cursor: null }) };
      }
      throw new Error(`Unexpected bridge request: ${url}`);
    }));

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({ open: true, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { wrapper: createWrapper() },
    );

    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(projectsCalls.length).toBeGreaterThan(0);
    const initialCount = projectsCalls.length;

    // Empty list → the 3s poll keeps refetching.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3_000);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(projectsCalls.length).toBeGreaterThan(initialCount);

    // A projects root appears → polling stops.
    projects = [ADOS_PROJECT];
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3_000);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(result.current.projectsQuery.data?.projects?.length).toBe(1);
    const countAfterPopulated = projectsCalls.length;

    await act(async () => {
      await vi.advanceTimersByTimeAsync(9_000);
    });
    expect(projectsCalls.length).toBe(countAfterPopulated);
  });
});


describe('workspace.v1 canonical timeline discovery', () => {
  const timelineId = '01M4M5EFF7TKDN0N5RXRVVAQBR';
  const head = 'sha256:' + 'a'.repeat(64);
  const canonical = {
    timeline_id: timelineId, project_id: 'project-1', version: 2,
    head_revision_id: head, archived: false, shots: [], references: [],
    is_default: false,
  };

  function discover(row: Record<string, unknown>) {
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url === '/api/astrid/v1/projects?limit=200') {
        return new Response(JSON.stringify({ items: [{
          project_id: 'project-1', slug: 'ados-talks', name: 'Ados Talks', version: 1,
          metadata: { default_timeline_id: timelineId },
          created_at: '2026-10-11T00:00:00Z', updated_at: '2026-10-11T00:00:00Z', archived: false,
        }], next_cursor: null }));
      }
      if (url === '/api/astrid/v1/projects/ados-talks/timelines?limit=200') {
        return new Response(JSON.stringify({ items: [row], next_cursor: null }));
      }
      throw new Error(`Unexpected canonical request: ${url}`);
    }));
    return renderHook(() => useAstridBridgeDiscovery({
      open: false, currentLocal: true, selectedProjectSlug: 'ados-talks',
    }), { wrapper: createWrapper() });
  }

  // 663dcd40 (timeline names): a nameless row whose id is a raw ULID is shown
  // as 'Untitled timeline' instead of the opaque id; identity stays untouched.
  it('displays a nameless canonical row without rewriting identity, version or head', async () => {
    const { result } = discover(canonical);
    await waitFor(() => expect(result.current.projectsQuery.isSuccess).toBe(true));
    expect(result.current.projectsQuery.data?.projects).toEqual([{
      slug: 'ados-talks',
      name: 'Ados Talks',
      project_id: 'project-1',
      version: 1,
      created_at: '2026-10-11T00:00:00Z',
      metadata: { default_timeline_id: timelineId },
    }]);
    await waitFor(() => expect(result.current.timelinesQuery.isSuccess).toBe(true));
    expect(result.current.timelinesQuery.data?.timelines).toEqual([{
      ...canonical, name: 'Untitled timeline', is_default: true, is_shot: false,
    }]);
    expect(result.current.timelinesQuery.data?.timelines?.[0]).toMatchObject({
      timeline_id: timelineId, version: 2, head_revision_id: head,
    });
  });

  it('accepts a null supplied name as nameless and shows the readable fallback', async () => {
    const { result } = discover({ ...canonical, name: null });
    await waitFor(() => expect(result.current.timelinesQuery.isSuccess).toBe(true));
    expect(result.current.timelinesQuery.data?.timelines).toEqual([{
      ...canonical, name: 'Untitled timeline', is_default: true, is_shot: false,
    }]);
  });

  it('falls back to the slug, then to a readable non-ULID id, never to a raw ULID', async () => {
    const withSlug = discover({ ...canonical, slug: 'intro-cut' });
    await waitFor(() => expect(withSlug.result.current.timelinesQuery.isSuccess).toBe(true));
    expect(withSlug.result.current.timelinesQuery.data?.timelines?.[0]).toMatchObject({
      timeline_id: timelineId, name: 'intro-cut',
    });
    withSlug.unmount();

    const readableId = discover({ ...canonical, timeline_id: 'main-cut' });
    await waitFor(() => expect(readableId.result.current.timelinesQuery.isSuccess).toBe(true));
    expect(readableId.result.current.timelinesQuery.data?.timelines?.[0]).toMatchObject({
      timeline_id: 'main-cut', name: 'main-cut',
    });
  });

  it('retains a supplied legacy display name on a canonical row', async () => {
    const { result } = discover({ ...canonical, name: 'Intro Cut' });
    await waitFor(() => expect(result.current.projectsQuery.isSuccess).toBe(true));
    await waitFor(() => expect(result.current.timelinesQuery.isSuccess).toBe(true));
    expect(result.current.timelinesQuery.data?.timelines?.[0]).toMatchObject({
      ...canonical, name: 'Intro Cut', is_default: true,
    });
  });

  it.each([
    ['empty supplied name', { name: '' }],
    ['malformed supplied name', { name: 7 }],
    ['empty canonical identity', { timeline_id: '' }],
    ['missing canonical identity', { timeline_id: undefined }],
  ])('rejects %s without a display or identity fallback', async (_label, invalid) => {
    const { result } = discover({ ...canonical, ...invalid });
    await waitFor(() => expect(result.current.timelinesQuery.isError).toBe(true));
    expect(result.current.timelinesQuery.data).toBeUndefined();
    expect(result.current.timelinesQuery.error?.message).toContain('malformed timelines list');
  });
});


describe('bounded native authority recovery', () => {
  it('keeps failure visible while an unsuccessful initial connection is retried', async () => {
    const probe = vi.mocked(assertNativeEditorConnection);
    probe.mockRejectedValueOnce(new Error('Workspace discovery: 503'));
    let finishRetry!: () => void;
    probe.mockImplementationOnce(() => new Promise<void>((resolve) => { finishRetry = resolve; }));
    vi.stubGlobal('fetch', vi.fn(async () => new Response(JSON.stringify({ items: [], next_cursor: null }))));
    const { result } = renderHook(() => useAstridBridgeDiscovery({ open: false, currentLocal: true, selectedProjectSlug: null }), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.bridgeDown).toBe(true));
    let retry!: ReturnType<typeof result.current.healthQuery.refetch>;
    act(() => { retry = result.current.healthQuery.refetch(); });
    await waitFor(() => expect(result.current.healthQuery.isFetching).toBe(true));
    expect(result.current.bridgeDown).toBe(true);
    await act(async () => { finishRetry(); await retry; });
    await waitFor(() => expect(result.current.bridgeDown).toBe(false));
    expect(result.current.bridgeHealthy).toBe(true);
  });

  it('stops after three failed probes and admits an explicit retry only after verified recovery', async () => {
    vi.useFakeTimers({toFake:['setInterval','clearInterval']});
    const probe=vi.mocked(assertNativeEditorConnection);
    probe.mockClear().mockRejectedValue(new Error('Workspace discovery: 503'));
    vi.stubGlobal('fetch',vi.fn(async()=>new Response(JSON.stringify({items:[],next_cursor:null}))));
    const {result,unmount}=renderHook(()=>useAstridBridgeDiscovery({open:false,currentLocal:true,selectedProjectSlug:null}),{wrapper:createWrapper()});
    await waitFor(()=>expect(probe).toHaveBeenCalledTimes(1));
    await act(async()=>{await vi.advanceTimersByTimeAsync(3000);});
    await waitFor(()=>expect(probe).toHaveBeenCalledTimes(2));
    await act(async()=>{await vi.advanceTimersByTimeAsync(3000);});
    await waitFor(()=>expect(probe).toHaveBeenCalledTimes(3));
    await act(async()=>{await vi.advanceTimersByTimeAsync(15000);});
    expect(probe).toHaveBeenCalledTimes(3);expect(result.current.bridgeDown).toBe(true);expect(result.current.healthQuery.isFetching).toBe(false);
    vi.useRealTimers();
    probe.mockResolvedValue(undefined);
    await act(async()=>{const receipt=await result.current.healthQuery.refetch();expect(receipt.error).toBeNull();expect(receipt.data).toBe(true);});
    expect(probe).toHaveBeenCalledTimes(4);await waitFor(()=>{expect(result.current.bridgeHealthy).toBe(true);expect(result.current.bridgeDown).toBe(false);});
    unmount();
  });
});
