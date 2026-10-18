import { assertNativeEditorConnection } from '@/integrations/astrid/nativeEditorConnection.ts';
// @vitest-environment jsdom
import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { useAstridBridgeDiscovery } from '@/tools/video-editor/hooks/useAstridBridgeDiscovery.ts';

vi.mock('@/integrations/astrid/nativeEditorConnection.ts',()=>({assertNativeEditorConnection:vi.fn(async()=>undefined)}));

const workspaceMode = vi.hoisted(() => ({ v1: false }));
vi.mock('@/integrations/astrid/workspaceV1.ts', () => ({
  get isAstridWorkspaceV1() { return workspaceMode.v1; },
  astridProjectCollectionPath: () => workspaceMode.v1 ? '/v1/projects' : '/projects',
  astridTimelineCollectionPath: (project: string) =>
    `${workspaceMode.v1 ? '/v1' : ''}/projects/${encodeURIComponent(project)}/timelines`,
}));

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

function makeBridgeFetch(overrides?: {
  health?: () => Response | Promise<Response>;
  projects?: () => Response | Promise<Response>;
  timelines?: () => Response | Promise<Response>;
}) {
  const calls: string[] = [];
  vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
    const url = String(input);
    calls.push(url);
    if (url.endsWith('/api/astrid/health')) {
      return overrides?.health?.() ?? new Response(JSON.stringify({ ok: true }), { status: 200 });
    }
    if (url.endsWith('/api/astrid/projects')) {
      return overrides?.projects?.() ?? new Response(JSON.stringify({
        projects: [{ slug: 'ados-talks', name: 'Ados Talks' }],
      }), { status: 200 });
    }
    if (url.endsWith('/api/astrid/projects/ados-talks/timelines')) {
      return overrides?.timelines?.() ?? new Response(JSON.stringify({
        timelines: [{
          timeline_id: '11111111-1111-1111-1111-111111111111',
          timeline_ulid: '01JM4K5N7P0000000000000017',
          slug: 'intro-cut',
          name: 'Intro Cut',
          is_default: true,
        }],
      }), { status: 200 });
    }
    throw new Error(`Unexpected bridge request: ${url}`);
  }));
  return calls;
}

afterEach(() => {
  workspaceMode.v1 = false;
  vi.unstubAllGlobals();
  vi.useRealTimers();
});

describe('useAstridBridgeDiscovery', () => {
  it('reports privacy-bounded outcomes for discovery success and invalid payloads', async () => {
    const onBridgeRequest = vi.fn();
    makeBridgeFetch({
      projects: () => new Response(JSON.stringify({ projects: 'not-a-list' }), { status: 200 }),
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
      expect(result.current.projectsQuery.isError).toBe(true);
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
      health: () => Promise.reject(new DOMException('timed out', 'TimeoutError')),
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
    await waitFor(() => expect(timeout.result.current.healthQuery.isError).toBe(true));
    expect(timeoutObserver).toHaveBeenCalledWith(expect.objectContaining({
      outcome: 'failure',
      errorClass: 'bridge.timeout',
    }));
    timeout.unmount();

    vi.unstubAllGlobals();
    const httpObserver = vi.fn();
    makeBridgeFetch({
      health: () => new Response('unavailable', { status: 503 }),
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
    await waitFor(() => expect(http.result.current.healthQuery.isError).toBe(true));
    expect(httpObserver).toHaveBeenCalledWith(expect.objectContaining({
      outcome: 'failure',
      errorClass: 'bridge.http_error',
    }));
  });

  it('fetches health, then projects, then timelines for the selected project', async () => {
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
        { slug: 'ados-talks', name: 'Ados Talks' },
      ]);
    });
    await waitFor(() => {
      expect(result.current.timelinesQuery.data?.timelines?.[0]?.timeline_id).toBe(
        '11111111-1111-1111-1111-111111111111',
      );
    });

    // Health is always first; projects only after the bridge is healthy.
    expect(calls[0]).toContain('/api/astrid/health');
    const healthIndex = calls.findIndex((c) => c.endsWith('/api/astrid/health'));
    const projectsIndex = calls.findIndex((c) => c.endsWith('/api/astrid/projects'));
    const timelinesIndex = calls.findIndex((c) => c.endsWith('/api/astrid/projects/ados-talks/timelines'));
    expect(healthIndex).toBeGreaterThanOrEqual(0);
    expect(projectsIndex).toBeGreaterThan(healthIndex);
    expect(timelinesIndex).toBeGreaterThan(projectsIndex);
  });

  it('does not fetch projects while the bridge is unhealthy', async () => {
    const calls = makeBridgeFetch({
      health: () => new Response(JSON.stringify({ ok: false }), { status: 200 }),
    });

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({ open: true, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { wrapper: createWrapper() },
    );

    await waitFor(() => {
      expect(result.current.bridgeDown).toBe(true);
    });
    expect(result.current.projectsQuery.data).toBeUndefined();
    expect(result.current.timelinesQuery.data).toBeUndefined();
    expect(calls.some((c) => c.endsWith('/api/astrid/projects'))).toBe(false);
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
    const closedProjectCalls = calls.filter((c) => c.endsWith('/api/astrid/projects')).length;
    const closedTimelineCalls = calls.filter((c) => c.endsWith('/api/astrid/projects/ados-talks/timelines')).length;
    expect(closedProjectCalls).toBeGreaterThanOrEqual(1);
    expect(closedTimelineCalls).toBeGreaterThanOrEqual(1);

    rerender({ open: true });

    await waitFor(() => {
      expect(calls.filter((c) => c.endsWith('/api/astrid/projects')).length).toBeGreaterThan(closedProjectCalls);
    });
    await waitFor(() => {
      expect(calls.filter((c) => c.endsWith('/api/astrid/projects/ados-talks/timelines')).length)
        .toBeGreaterThan(closedTimelineCalls);
    });
  });

  it('polls health every 3s while a local editor is waiting, then stops after success', async () => {
    vi.useFakeTimers();
    let healthy = false;
    const healthCalls: string[] = [];
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/astrid/health')) {
        healthCalls.push(url);
        return { ok: true, json: async () => ({ ok: healthy }) };
      }
      if (url.endsWith('/api/astrid/projects')) {
        return { ok: true, json: async () => ({ projects: [{ slug: 'ados-talks', name: 'Ados Talks' }] }) };
      }
      throw new Error(`Unexpected bridge request: ${url}`);
    }));

    const { result } = renderHook(
      () => useAstridBridgeDiscovery({ open: false, currentLocal: true, selectedProjectSlug: 'ados-talks' }),
      { wrapper: createWrapper() },
    );

    // Initial health probe settles once the microtask chain drains (the fake
    // timer advance below forces it).
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(healthCalls.length).toBeGreaterThan(0);
    const initialCount = healthCalls.length;

    // Bridge still down → the 3s poll keeps probing.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3_000);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(healthCalls.length).toBeGreaterThan(initialCount);

    // Bridge comes up → next poll succeeds and polling stops.
    healthy = true;
    await act(async () => {
      await vi.advanceTimersByTimeAsync(3_000);
    });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(result.current.bridgeHealthy).toBe(true);
    const countAfterSuccess = healthCalls.length;

    // No further polls while the local editor has a healthy bridge.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(9_000);
    });
    expect(healthCalls.length).toBe(countAfterSuccess);
  });

  it('polls projects while open and the projects list is empty, stopping once populated', async () => {
    vi.useFakeTimers();
    let projects: { slug: string; name: string }[] = [];
    const projectsCalls: string[] = [];
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.endsWith('/api/astrid/health')) {
        return { ok: true, json: async () => ({ ok: true }) };
      }
      if (url.endsWith('/api/astrid/projects')) {
        projectsCalls.push(url);
        return { ok: true, json: async () => ({ projects }) };
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
    projects = [{ slug: 'ados-talks', name: 'Ados Talks' }];
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
    workspaceMode.v1 = true;
    vi.stubGlobal('fetch', vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url === '/api/astrid/v1/health') {
        return new Response(JSON.stringify({ status: 'ok' }));
      }
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
  it('stops after three failed probes and admits an explicit retry only after verified recovery', async () => {
    workspaceMode.v1=true;
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
