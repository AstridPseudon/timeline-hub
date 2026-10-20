// @vitest-environment jsdom
import React from 'react';
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, expect, it, vi } from 'vitest';
import { environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import { captureClipDeleteEdit } from '../commands/clipDeleteGesture.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../contexts/VideoEditorRuntimeContext.tsx';
import { createInteractionState } from '../lib/interaction-state.ts';
import type { TimelineData } from '../lib/timeline-data.ts';
import { createTimelineStore } from './timelineStore.ts';
import { useTimelineSave } from './useTimelineSave.ts';

vi.mock('../compositions/TimelineRenderer.tsx', () => ({ invalidateReferencedTimelineCache: vi.fn() }));
afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

it.each(['basis first', 'display first'] as const)('cold load installs a verified projection before native Delete (%s)', async (order) => {
  const env = await environment();
  vi.stubGlobal('indexedDB', env.factory);
  vi.stubGlobal('navigator', { locks: { request: async (_key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => work({}) } });
  let release!: () => void;
  const gate = new Promise<void>((resolve) => { release = resolve; });
  const load = vi.spyOn(env.provider, 'loadTimelineCommandBasis').mockImplementation(async () => {
    if (order === 'display first') await gate;
    return env.initial;
  });
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const runtime = { provider: env.provider, timelineId: 'timeline-commit', shots: { canonicalDraft: null } } as unknown as VideoEditorRuntimeContextValue;
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={client}>
      <VideoEditorRuntimeProvider value={runtime}>{children}</VideoEditorRuntimeProvider>
    </QueryClientProvider>
  );
  const interaction = { current: createInteractionState() };
  const store = createTimelineStore();
  const hook = renderHook(({ loaded }: { loaded: TimelineData | undefined }) => useTimelineSave({
    timelineQuery: { data: loaded, isLoading: !loaded }, assetRegistryQuery: { data: undefined },
  }, env.provider, interaction, store), { wrapper, initialProps: { loaded: undefined } });
  await act(async () => { await Promise.resolve(); });
  const loaded = { ...env.current(), head: { ...env.current().head!, headPublicationId: null } };
  act(() => { hook.rerender({ loaded }); });
  await waitFor(() => expect(hook.result.current.data).not.toBeNull());
  act(() => { release(); });
  await waitFor(() => expect(hook.result.current.commands.clipDeletePort).toBeDefined());
  expect(load).toHaveBeenCalled();
  expect(hook.result.current.data?.editProjection).toEqual({ kind: 'accepted', head: env.initial.head });
  expect(hook.result.current.data?.head?.headPublicationId).toBe(env.initial.head.publicationId);
  const captured = captureClipDeleteEdit(hook.result.current.commands.clipDeletePort, hook.result.current.data!, 'x');
  expect(captured.basis.command).toMatchObject({ op: 'clip.delete', select: 'parent/clip:x' });
  expect(env.commits()).toHaveLength(0);
  hook.unmount();
  client.clear();
});
