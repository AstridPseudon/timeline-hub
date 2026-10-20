// @vitest-environment jsdom
import { act, cleanup, render, renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AgentChatProvider } from '@/shared/contexts/AgentChatContext.tsx';
import { toast } from '@/shared/components/ui/runtime/sonner.tsx';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { document, environment, scope } from '../commands/__tests__/commitSessionEnvironment.ts';
import { ClipMoveError } from '../commands/clipMovePrimitives.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from '../commands/trackLabelGesture.ts';
import { VideoEditorProvider } from '../contexts/VideoEditorProvider.tsx';
import { assembleTimelineData } from '../lib/timeline-data.ts';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { createTimelineStore, useTimelineEditorData, useTimelineEditorOps } from './timelineStore.ts';
import * as commandSession from './useTimelineCommandSession.ts';
import { createTimelineCommands, useTimelineCommandsService } from './useTimelineCommandsService.ts';
import { useClipEditing } from './useClipEditing.ts';

// Keep provider/state, native captures, durable outbox, projection and Runtime client connected.
// Only external host services and initial reads are fixed. Transport is simulated, with no sockets.
vi.mock('@/tools/video-editor/runtime/installedTimelineHostServiceHooks.ts', async () => {
  const { PUBLIC_TIMELINE_SERVICE_HOOKS } = await import('../runtime/timelineHostServiceHooks.ts');
  return { INSTALLED_TIMELINE_SERVICE_HOOKS: PUBLIC_TIMELINE_SERVICE_HOOKS };
});
vi.mock('@/tools/video-editor/adapters/app/useAstridShotsHost.ts', () => {
  const shots = { shots: [], isLoading: false, error: null, refetchShots: vi.fn(),
    finalVideoMap: new Map(), dismissFinalVideo: vi.fn(), canonicalDraft: null };
  return { useAstridShotsHost: () => shots };
});
vi.mock('@/shared/hooks/settings/useToolSettings', () => ({ useToolSettings: () => ({ settings: {} }) }));
vi.mock('@/tools/video-editor/hooks/useEffects.ts', () => {
  const effects = { data: [] };
  return { useEffects: () => effects };
});
vi.mock('@/tools/video-editor/hooks/useTimelineQueries.ts', () => ({
  useTimelineQueries: (_provider: unknown, _id: string, _resolve: unknown, initial: unknown) => ({
    timelineQuery: { data: initial, isLoading: false, error: null, refetch: vi.fn() },
    assetRegistryQuery: { data: (initial as { registry: unknown }).registry },
  }),
}));
vi.mock('@/shared/components/ui/runtime/sonner.tsx', () => ({ toast: { error: vi.fn() } }));

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); vi.clearAllMocks(); });

const survivor = { id: 'keep', track: 'V1', clipType: 'text', at: 2.017, hold: 1.013,
  from: null, speed: null, opacity: null, params: { text: 'Keep 🦊' },
  app: { opaque: [null, false, 0, {}, []] }, custom: { id: 'x', clear: null } };
function rawDocument() {
  const raw = document();
  const parent = raw.parent_revision.payload;
  const target = parent.clips[0] as Record<string, JSON>;
  target.app = { opaque: null, canonical: { ownerRef: 'occurrence:opaque', clipRef: 'occurrence:opaque/clip:x' } };
  target.sourceURL = null;
  target.custom = { nested: [null, false], id: 'x' };
  parent.clips.push(structuredClone(survivor));
  Object.assign(parent.config, { clips: structuredClone(parent.clips), opaque: { retained: [null, false, []] } });
  raw.parent_revision.content_digest = fixtureDigest(parent);
  return raw;
}

async function mounted(existingEnv?: Awaited<ReturnType<typeof environment>>) {
  const env = existingEnv ?? await environment(rawDocument());
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const installs: Parameters<Parameters<typeof commandSession.useTimelineCommandSession>[0]['commit']['commitData']>[] = [];
  const realHook = commandSession.useTimelineCommandSession;
  const hook = vi.spyOn(commandSession, 'useTimelineCommandSession').mockImplementation((options) => realHook({
    ...options, commit: { ...options.commit, commitData: (...args) => {
      installs.push(args);
      options.commit.commitData(...args);
    } },
  }));
  const save = vi.spyOn(env.provider, 'saveTimeline');
  const saveAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  let editor!: ReturnType<typeof useTimelineEditorData>;
  let ops!: ReturnType<typeof useTimelineEditorOps>;
  let facade!: ReturnType<typeof useTimelineCommandsService>;
  function Inspector() {
    editor = useTimelineEditorData();
    ops = useTimelineEditorOps();
    facade = useTimelineCommandsService();
    return null;
  }
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const view = render(<QueryClientProvider client={client}><MemoryRouter><AgentChatProvider>
    <VideoEditorProvider dataProvider={env.provider} projectId={scope.projectId}
      timelineId={scope.timelineId} userId={null} initialTimelineData={env.current()}>
      <Inspector />
    </VideoEditorProvider>
  </AgentChatProvider></MemoryRouter></QueryClientProvider>);
  const session = () => hook.mock.results.at(-1)!.value as ReturnType<typeof commandSession.useTimelineCommandSession>;
  await waitFor(() => expect(ops.clipDelete).toBeDefined());
  expect(ops.clipDelete).toBe(session().clipDeletePort);
  return { env, view, installs, save, saveAtHead, session, current: () => editor.dataRef.current!,
    ops: () => ops, selection: () => editor.selectedClipId, facade: () => facade };
}

describe('mounted single-parent deletion ingresses', () => {
  it.each(['single', 'selection', 'facade'] as const)('captures %s before its only local installation, preserving whole rows and selection', async (ingress) => {
    const m = await mounted();
    // Existing display normalization drops unknown root config keys at load. Seed a prior local
    // display extension explicitly so this bounded preview must preserve it without normalizing.
    const rootMetadata = { nullable: null, ordered: [false, 0, {}, []] };
    Object.assign(m.current(), { rootMetadata });
    Object.assign(m.current().config, { opaque: { retained: [null, false, []] } });
    act(() => m.ops().selectClip('x'));
    await waitFor(() => expect(m.selection()).toBe('x'));
    const before = m.current();
    const port = m.ops().clipDelete!;
    const capture = vi.spyOn(port, 'capture');
    const finish = vi.spyOn(port, 'finish');
    const submit = vi.spyOn(port, 'submit');
    const gate = m.env.pause();
    m.installs.length = 0;
    act(() => {
      if (ingress === 'single') m.ops().handleDeleteClip('x');
      else if (ingress === 'selection') m.ops().handleDeleteClips(['x', 'x']);
      else expect(m.facade().deleteClip({ clipId: 'x' })).toEqual({ ok: true, data: { clipId: 'x' } });
    });
    expect(capture).toHaveBeenCalledExactlyOnceWith({ clipId: 'x', current: before, ownerRef: 'parent' });
    expect(finish).toHaveBeenCalledOnce();
    expect(submit).toHaveBeenCalledOnce();
    expect(m.installs).toHaveLength(1);
    expect(m.installs[0][1]).toEqual({ save: false, skipHistory: true });
    expect(m.current().config.clips).toEqual([survivor]);
    expect(m.current().resolvedConfig.clips.map((clip) => clip.id)).toEqual(['keep']);
    expect(m.current().rows.flatMap((row) => row.actions.map((action) => action.id))).toEqual(['keep']);
    expect(m.current().meta).not.toHaveProperty('x');
    expect(m.current().meta.keep).toEqual(before.meta.keep);
    expect(m.current().config).toMatchObject({ opaque: { retained: [null, false, []] } });
    expect(m.current()).toMatchObject({ rootMetadata });
    expect(m.current().registry).toBe(before.registry);
    expect(m.current().editProjection).toMatchObject({ kind: 'local', base: { revisionId: 'r0', publicationId: 'p0' } });
    await waitFor(() => expect(m.selection()).toBeNull());
    await waitFor(() => expect(m.env.commits()).toHaveLength(1));
    const command = m.env.commits()[0].body!.commands[0];
    expect(command).toMatchObject({ schema_version: 1, op: 'clip.delete', version: '1', select: 'parent/clip:x', args: {},
      expect: { 'parent/clip:x::': { state: 'present', value: rawDocument().parent_revision.payload.clips[0] } },
      resolved: ['parent/clip:x'], created: [] });
    expect(command.selections).toEqual(expect.arrayContaining([expect.objectContaining({
      key: 'collection.clips', owner: 'parent', members: ['parent/clip:x', 'parent/clip:keep'],
    })]));
    expect(command.reads).toEqual(expect.arrayContaining([expect.objectContaining({ ref: 'parent/clip:x', path: [] })]));
    expect(m.save).not.toHaveBeenCalled();
    expect(m.saveAtHead).not.toHaveBeenCalled();
    await act(async () => { gate.resolve(); await m.session().flush(); });
    expect(m.session().state.status).toBe('saved');
    expect(m.installs.every(([, options]) => options?.save === false)).toBe(true);
    expect(m.current().config.clips).toEqual([survivor]);
    const accepted = await m.env.provider.loadTimelineCommandBasis(scope.timelineId);
    expect(accepted.canonicalDocument.parent_revision.payload.config).toMatchObject({
      opaque: { retained: [null, false, []] }, clips: [survivor],
    });
    m.view.unmount();
  });

  it.each(['single', 'facade'] as const)('shows %s native dependency refusal and retains the prior local draft', async (ingress) => {
    const raw = rawDocument();
    raw.parent_revision.payload.clips[0].transition = { type: 'crossfade', duration: 0.25 };
    raw.parent_revision.payload.config.clips = structuredClone(raw.parent_revision.payload.clips);
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const m = await mounted(await environment(raw));
    const gate = m.env.pause();
    act(() => submitTrackLabelEdit(captureTrackLabelEdit(m.session().trackLabelPort, m.current(), 'V1'),
      { values: { label: 'Earlier local label' }, clear: [] }));
    await waitFor(() => expect(m.env.commits()).toHaveLength(1));
    const before = m.current();
    m.installs.length = 0;
    act(() => {
      if (ingress === 'single') m.ops().handleDeleteClip('x');
      else {
        const result = m.facade().deleteClip({ clipId: 'x' });
        expect(result).toMatchObject({ ok: false, error: { code: 'mutation_failed',
          cause: { kind: 'unsupported_dependency' } } });
        if (!result.ok) expect(result.error.cause).toBeInstanceOf(ClipMoveError);
      }
    });
    if (ingress === 'single') expect(toast.error).toHaveBeenCalledWith(expect.stringContaining('semantic dependencies'));
    expect(m.current()).toBe(before);
    expect(m.current().config.tracks![0].label).toBe('Earlier local label');
    expect(m.installs).toHaveLength(0);
    expect(m.env.commits()).toHaveLength(1);
    expect(m.save).not.toHaveBeenCalled();
    expect(m.saveAtHead).not.toHaveBeenCalled();
    await act(async () => { gate.resolve(); await m.session().flush(); });
    m.view.unmount();
  });

  it('keeps an asynchronously conflicted delete through durable recovery and never resubmits it on retry', async () => {
    const m = await mounted();
    m.env.setFault('conflict');
    act(() => m.ops().handleDeleteClip('x'));
    await waitFor(() => expect(m.session().state.status).toBe('conflict'));
    expect(m.session().state.error).toBeTruthy();
    const draft = structuredClone(m.current().config);
    const [stored] = await m.env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.pending!.outcome!.kind).toBe('rejected');
    const original = structuredClone(stored.intents[0].payload);
    await act(async () => { await expect(m.session().flush()).rejects.toThrow(); await m.session().retry(); });
    expect(m.env.commits()).toHaveLength(1);
    expect(m.current().config).toEqual(draft);
    m.view.unmount();
    vi.restoreAllMocks();
    const reopened = await mounted(m.env);
    await waitFor(() => expect(reopened.session().state.status).toBe('recovery'));
    await act(async () => reopened.session().recover(stored.ownerId));
    await waitFor(() => expect(reopened.session().state.status).toBe('conflict'));
    expect(reopened.current().config).toEqual(draft);
    expect((await m.env.outboxes.list(scope))[0].intents[0].payload).toEqual(original);
    expect(m.env.commits()).toHaveLength(1);
    expect(reopened.save).not.toHaveBeenCalled();
    expect(reopened.saveAtHead).not.toHaveBeenCalled();
    reopened.view.unmount();
  });
});

describe('unavailable single delete does not enter a snapshot path', () => {
  it('reports the error and preserves the exact displayed draft', async () => {
    const env = await environment(rawDocument());
    const dataRef = { current: env.current() };
    const applyEdit = vi.fn();
    const hook = renderHook(() => useClipEditing({ dataRef, resolvedConfig: dataRef.current.resolvedConfig,
      selectedClipId: 'x', selectedTrack: null, currentTime: 0, selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit }));
    const before = dataRef.current;
    act(() => hook.result.current.handleDeleteClip('x'));
    expect(toast.error).toHaveBeenCalledWith('clip.delete capture is unavailable.');
    expect(dataRef.current).toBe(before);
    expect(applyEdit).not.toHaveBeenCalled();
  });
});

describe('separate unconverted deletion ingresses', () => {
  it.each(['group single', 'group batch', 'free batch'] as const)('preserves the existing %s edit as one row mutation without native submissions', async (ingress) => {
    const raw = rawDocument();
    if (ingress !== 'free batch') raw.parent_revision.payload.config.pinnedShotGroups = [
      { shotId: 'legacy-shot', trackId: 'V1', clipIds: ['x', 'keep'] },
    ];
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const env = await environment(raw);
    const session = await env.mount();
    const capture = vi.spyOn(session.clipDeletePort, 'capture');
    const submit = vi.spyOn(session.clipDeletePort, 'submit');
    const dataRef = { current: env.current() };
    const applyEdit = vi.fn();
    const hook = renderHook(() => useClipEditing({ dataRef, resolvedConfig: dataRef.current.resolvedConfig,
      clipDeletePort: session.clipDeletePort, selectedClipId: 'x', selectedTrack: null, currentTime: 0,
      selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit }));
    act(() => {
      if (ingress === 'group single') hook.result.current.handleDeleteClip('x', { allowPinnedGroupDelete: true });
      else hook.result.current.handleDeleteClips(['x', 'keep'], { allowPinnedGroupDelete: true });
    });
    const ids = ingress === 'group single' ? ['x'] : ['x', 'keep'];
    expect(applyEdit).toHaveBeenCalledExactlyOnceWith({ type: 'rows',
      rows: dataRef.current.rows.map((row) => ({ ...row, actions: row.actions.filter((action) => !ids.includes(action.id)) })),
      metaDeletes: ids }, { semantic: true });
    expect(capture).not.toHaveBeenCalled();
    expect(submit).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });

  it('keeps validated occurrence deletion on its existing hook and facade paths', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'old', publication_id: 'old' }, { children: true }).data.canonical_document;
    const env = await environment(raw);
    const session = await env.mount();
    const composition = createShotCompositionAdapter({ load: async () => env.initial.graph }).prepare(env.initial.graph);
    const { config } = projectCanonicalComposition(composition, env.current().resolvedConfig);
    const current = { ...env.current(), ...assembleTimelineData({ ...env.current(), config, resolvedConfig: config }) };
    const dataRef = { current };
    const applyEdit = vi.fn();
    const capture = vi.spyOn(session.clipDeletePort, 'capture');
    const submit = vi.spyOn(session.clipDeletePort, 'submit');
    const id = 'occ-0:child-title';
    const hook = renderHook(() => useClipEditing({ dataRef, resolvedConfig: current.resolvedConfig,
      clipDeletePort: session.clipDeletePort, selectedClipId: id, selectedTrack: null, currentTime: 0,
      selectClip: vi.fn(), setSelectedTrackId: vi.fn(), applyEdit }));
    act(() => hook.result.current.handleDeleteClip(id));
    const expected = { type: 'rows', rows: current.rows.map((row) => ({ ...row,
      actions: row.actions.filter((action) => action.id !== id) })), metaDeletes: [id] };
    expect(applyEdit).toHaveBeenCalledExactlyOnceWith(expected, { semantic: true });
    const store = createTimelineStore();
    store.getState().syncSlices({ data: { ...store.getState().data, data: current, dataRef },
      ops: { ...store.getState().ops, applyEdit, clipDelete: session.clipDeletePort } });
    const result = createTimelineCommands(store).deleteClip({ clipId: id });
    expect(result).toEqual({ ok: true, data: { clipId: id } });
    expect(applyEdit).toHaveBeenLastCalledWith(expected, { semantic: true });
    expect(capture).not.toHaveBeenCalled();
    expect(submit).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });

  it('returns a structured facade failure when the parent capture port is unavailable', async () => {
    const env = await environment(rawDocument());
    const current = env.current();
    const applyEdit = vi.fn();
    const store = createTimelineStore();
    store.getState().syncSlices({ data: { ...store.getState().data, data: current, dataRef: { current } },
      ops: { ...store.getState().ops, applyEdit } });
    expect(createTimelineCommands(store).deleteClip({ clipId: 'x' })).toMatchObject({ ok: false,
      error: { code: 'mutation_failed', message: 'clip.delete capture is unavailable.', cause: expect.any(Error) } });
    expect(store.getState().data.dataRef.current).toBe(current);
    expect(applyEdit).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
  });
});
