// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { useLayoutEffect, type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { CanonicalDocument, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { document, environment, scope } from '../../commands/__tests__/commitSessionEnvironment.ts';
import { AuthoredState } from '../../commands/clipMovePrimitives.ts';
import { submitClipScalarEdit, type CapturedClipScalarEdit } from '../../commands/clipScalarGesture.ts';
import fixture from '../../commands/fixtures/recipe_m2_app_clip_scalar_fields.json';
import { createShotCompositionAdapter } from '../../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../../data/shotCompositionProjection.ts';
import { buildTimelineData } from '../../lib/timeline-data.ts';
import { createInteractionState } from '../../lib/interaction-state.ts';
import { createTimelineStore, TimelineStoreProvider, useTimelineEditorData } from '../../hooks/timelineStore.ts';
import { useClipScalarControl } from '../../hooks/useClipScalarControl.ts';
import { useTimelineSave } from '../../hooks/useTimelineSave.ts';
import { createTimelineCommands } from '../../hooks/useTimelineCommandsService.ts';
import { TimelineCommandRecovery } from '../TimelineCommandRecovery.tsx';
import { ClipPanelBody } from './ClipPanelBody.tsx';
import { NO_TRANSITION } from './clip-panel-primitives.tsx';

// Keep the field's edit/commit events distinct, as in the real NumberField.
vi.mock('@/shared/components/ui/number-input.tsx', () => ({
  NumberInput: ({ value, onChange, onValueCommitted }: {
    value: number | null;
    onChange: (value: number | null) => void;
    onValueCommitted?: (value: number | null) => void;
  }) => <input type="number" value={value ?? ''}
    onChange={(event) => onChange(event.currentTarget.value === '' ? null : Number(event.currentTarget.value))}
    onBlur={(event) => onValueCommitted?.(event.currentTarget.value === '' ? null : Number(event.currentTarget.value))} />,
}));

// Registry/catalog behavior remains covered by the original transition suite.
vi.mock('@/shared/components/ui/select.tsx', () => ({
  Select: ({ value, onValueChange }: { value: string; onValueChange: (value: string) => void }) => (
    <select value={value} onChange={(event) => onValueChange(event.currentTarget.value)}>
      <option value="__none__">None</option><option value="crossfade">crossfade</option><option value="wipe">wipe</option>
    </select>
  ),
  SelectTrigger: () => null, SelectContent: () => null, SelectItem: () => null, SelectValue: () => null,
}));

const opaque = { selected_item_id: 'keep', nested: [null, '', { owner: 'unchanged' }] };
function parentDocument(): CanonicalDocument {
  const raw = document();
  const row = (raw.parent_revision.payload.clips as Array<Record<string, JSON>>)[0];
  Object.assign(row, { clipType: 'hold', hold: 6, speed: 2, app: { opaque },
    transition: { type: 'crossfade', duration: 0.5, params: { custom: 'keep' } }, extension: opaque });
  (raw.parent_revision.payload.config as Record<string, JSON>).clips = structuredClone(raw.parent_revision.payload.clips);
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  return raw;
}

function occurrenceDocument(): CanonicalDocument {
  const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
    { revision_id: 'initial', publication_id: 'initial' }, { children: true }).data.canonical_document;
  raw.parent_revision.payload = { ...structuredClone(fixture.bundle.parent),
    occurrences: fixture.bundle.placements.map((placement) => ({ ...structuredClone(placement), shot_id: 'shot-1', shot_revision_id: 'shot-r1' })) };
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const internal = raw.internal_timeline_revisions[0];
  internal.payload = structuredClone(Object.values(fixture.bundle.shots)[0].internal_timeline);
  const row = (internal.payload.clips as Array<Record<string, JSON>>).find((clip) => clip.id === 'f2-agent-clip')!;
  row.clipType = 'hold';
  internal.content_digest = fixtureDigest(internal.payload);
  raw.dependency_manifest.internal_timelines[0].content_digest = internal.content_digest;
  return raw;
}

async function mounted(raw = parentDocument(), clipId = 'x', tab: 'timing' | 'effects' = 'timing') {
  const env = await environment(raw);
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  let initial = env.current();
  if (Array.isArray(raw.parent_revision.payload.occurrences) && raw.parent_revision.payload.occurrences.length && env.initial.graph) {
    const composition = createShotCompositionAdapter(env.provider.shotComposition).prepare(env.initial.graph);
    const { config } = projectCanonicalComposition(composition);
    initial = await buildTimelineData(config, { assets: config.registry }, async (file) => file, 1, undefined, initial.head);
  }
  const store = createTimelineStore();
  store.getState().setMounted(true);
  const legacyChange = vi.fn();
  const snapshotSaves = vi.fn();
  const saveTimeline = vi.spyOn(env.provider, 'saveTimeline');
  const saveTimelineAtHead = vi.spyOn(env.provider, 'saveTimelineAtHead');
  const publish = vi.spyOn(env.provider.shotComposition, 'publish');
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  const runtime = { provider: env.provider, timelineId: scope.timelineId, shots: { canonicalDraft: null },
    project: { projectId: scope.projectId }, toast: { error: vi.fn(), success: vi.fn() },
    assetResolver: { resolveAssetUrl: async (file: string) => file } } as unknown as VideoEditorRuntimeContextValue;
  const queries = { timelineQuery: { data: initial, isLoading: false }, assetRegistryQuery: { data: initial.registry } };
  const interactionStateRef = { current: createInteractionState() };
  let latest!: ReturnType<typeof useTimelineSave>;
  let capture!: () => CapturedClipScalarEdit;
  function Controls() {
    const { data } = useTimelineEditorData();
    capture = useClipScalarControl(clipId);
    const clip = data?.resolvedConfig.clips.find((candidate) => candidate.id === clipId) ?? null;
    return <ClipPanelBody clip={clip} track={data?.resolvedConfig.tracks.find((track) => track.id === clip?.track) ?? null}
      effectResources={{ data: { entrance: [], exit: [], continuous: [] }, effects: [], entrance: [], exit: [], continuous: [],
        isLoading: false, isFetching: false, error: null, refetch: vi.fn(async () => undefined),
        canCreateEffect: false, canUpdateEffect: false, canDeleteEffect: false }}
      deviceClass="desktop" interactionMode="move" precisionEnabled={false} hasPredecessor={false}
      onChange={legacyChange} onScalarEditStart={capture} onResetPosition={vi.fn()} onClose={vi.fn()}
      onToggleMute={vi.fn()} onSplitAtPlayhead={vi.fn()} onMoveTrackUp={vi.fn()} onMoveTrackDown={vi.fn()}
      onSetInteractionMode={vi.fn()} onSetPrecisionEnabled={vi.fn()} compositionWidth={1920} compositionHeight={1080}
      registry={data?.resolvedConfig.registry ?? {}} activeTab={tab} setActiveTab={vi.fn()} />;
  }
  function Host() {
    const save = useTimelineSave(queries, env.provider, interactionStateRef, store, initial);
    latest = save;
    useLayoutEffect(() => {
      store.getState().syncSlices({
        data: { ...store.getState().data, data: save.data, resolvedConfig: save.data?.resolvedConfig ?? null, dataRef: save.dataRef },
        ops: { ...store.getState().ops, clipMove: save.commands.port, clipScalar: save.commands.clipScalarPort },
      });
    }, [save.data, save.dataRef, save.commands.port, save.commands.clipScalarPort]);
    return <><Controls /><TimelineCommandRecovery commandSession={save.commands} /></>;
  }
  const wrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}><VideoEditorRuntimeProvider value={runtime}>
      <TimelineStoreProvider store={store}>{children}</TimelineStoreProvider>
    </VideoEditorRuntimeProvider></QueryClientProvider>
  );
  const view = render(<Host />, { wrapper });
  await waitFor(() => expect(latest.commands.clipScalarPort).toBeDefined());
  latest.eventBus.on('scheduleSave', snapshotSaves);
  const captureSpy = vi.spyOn(latest.commands.clipScalarPort!, 'capture');
  const noSnapshots = () => {
    expect(legacyChange).not.toHaveBeenCalled();
    expect(snapshotSaves).not.toHaveBeenCalled();
    expect(saveTimeline).not.toHaveBeenCalled();
    expect(saveTimelineAtHead).not.toHaveBeenCalled();
    expect(publish).not.toHaveBeenCalled();
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')
      .every((call) => call.path.endsWith('/commit'))).toBe(true);
  };
  return { ...view, env, store, latest: () => latest, capture: () => capture(), captureSpy, legacyChange, noSnapshots,
    records: () => env.outboxes.list(scope), service: createTimelineCommands(store) };
}

function holdInput() {
  return within(screen.getByText('Duration (seconds)').parentElement!).getByRole('spinbutton');
}
function transitionSection() {
  return screen.getByText('Transition').parentElement!;
}
const rowFrom = (bundle: unknown, ref: string) => new AuthoredState(bundle as never).entity(ref)!;
type Payload = { commands: EditCommand[]; before: unknown; after: unknown };

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('mounted scalar controls → Runtime provider → durable command outbox (unit transport)', () => {
  it('captures once before typing, then commits SOURCE hold seconds once on blur', async () => {
    const host = await mounted();
    const paused = host.env.pause();
    expect(holdInput()).toHaveValue(6); // speed=2: the timeline extent is only three seconds.
    fireEvent.change(holdInput(), { target: { value: '7' } });
    fireEvent.change(holdInput(), { target: { value: '8' } });
    expect(host.captureSpy).toHaveBeenCalledTimes(1);
    expect(host.latest().dataRef.current!.config.clips[0].hold).toBe(6);
    expect(host.env.commits()).toHaveLength(0);
    fireEvent.blur(holdInput());
    fireEvent.blur(holdInput());
    await waitFor(() => expect(host.env.commits()).toHaveLength(1));
    const [record] = await host.records();
    const command = host.env.commits()[0].body!.commands[0];
    expect(command).toMatchObject({ schema_version: 1, op: 'clip.set', version: '1', select: 'parent/clip:x',
      args: { values: { hold: 8 }, clear: [] }, expect: { 'parent/clip:x::hold': { state: 'present', value: 6 } } });
    expect(command.args).toEqual({ values: { hold: 8 }, clear: [] });
    expect(JSON.parse(record.pending!.request.body).commands).toEqual([command]);
    const payload = record.intents[0].payload as Payload;
    expect(rowFrom(payload.before, 'parent/clip:x').hold).toBe(6);
    expect(rowFrom(payload.after, 'parent/clip:x')).toMatchObject({ hold: 8, speed: 2, app: { opaque }, extension: opaque });
    expect(host.latest().dataRef.current!.config.clips[0].hold).toBe(8);
    await act(async () => { paused.resolve(); await host.latest().commands.flush(); });
    const accepted = await host.env.provider.loadTimelineCommandBasis(scope.timelineId);
    expect((accepted.canonicalDocument.parent_revision.payload.clips as Array<Record<string, JSON>>)[0])
      .toMatchObject({ hold: 8, speed: 2, app: { opaque }, extension: opaque });
    host.noSnapshots();
  });

  it.each(['None', 'Remove'])('maps only explicit %s to transition ABSENT', async (action) => {
    const host = await mounted(parentDocument(), 'x', 'effects');
    const paused = host.env.pause();
    if (action === 'None') fireEvent.change(within(transitionSection()).getByRole('combobox'), { target: { value: NO_TRANSITION } });
    else fireEvent.click(within(transitionSection()).getByRole('button', { name: 'Remove' }));
    await waitFor(() => expect(host.env.commits()).toHaveLength(1));
    const command = host.env.commits()[0].body!.commands[0];
    expect(command).toMatchObject({ op: 'clip.set', select: 'parent/clip:x',
      args: { values: {}, clear: ['transition'] },
      expect: { 'parent/clip:x::transition': { state: 'present', value: { type: 'crossfade', duration: 0.5, params: { custom: 'keep' } } } } });
    expect(command.args).toEqual({ values: {}, clear: ['transition'] });
    const [record] = await host.records();
    expect(JSON.parse(record.pending!.request.body).commands).toEqual([command]);
    const after = rowFrom((record.intents[0].payload as Payload).after, 'parent/clip:x');
    expect(after).not.toHaveProperty('transition');
    expect(after).toMatchObject({ hold: 6, speed: 2, app: { opaque }, extension: opaque });
    expect(host.latest().dataRef.current!.config.clips[0]).not.toHaveProperty('transition');
    await act(async () => { paused.resolve(); await host.latest().commands.flush(); });
    host.noSnapshots();
  });

  it.each(['hold', 'None'] as const)('edits parent %s despite full opaque occurrence metadata through the actual hook', async (action) => {
    const source = await environment(occurrenceDocument());
    const composition = createShotCompositionAdapter(source.provider.shotComposition).prepare(source.initial.graph!);
    const projected = projectCanonicalComposition(composition).config.clips
      .find((clip) => clip.id === 'f2-occurrence:f2-agent-clip')!;
    const raw = parentDocument();
    const row = (raw.parent_revision.payload.clips as Array<Record<string, JSON>>)[0];
    row.app = { opaque, canonical: structuredClone(projected.app!.canonical) as JSON };
    (raw.parent_revision.payload.config as Record<string, JSON>).clips = structuredClone(raw.parent_revision.payload.clips);
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const original = structuredClone(row);
    const host = await mounted(raw, 'x', action === 'hold' ? 'timing' : 'effects');
    const paused = host.env.pause();
    if (action === 'hold') {
      expect(holdInput()).toHaveValue(6); // SOURCE seconds, with speed=2.
      fireEvent.change(holdInput(), { target: { value: '8' } });
      fireEvent.blur(holdInput());
    } else {
      const select = within(transitionSection()).getByRole('combobox');
      expect(select).toHaveValue('crossfade');
      fireEvent.change(select, { target: { value: NO_TRANSITION } });
    }
    await waitFor(() => expect(host.env.commits()).toHaveLength(1));
    expect(host.captureSpy).toHaveBeenCalledTimes(1);
    const records = await host.records();
    expect(records).toHaveLength(1);
    expect(records[0].intents).toHaveLength(1);
    const payload = records[0].intents[0].payload as Payload;
    expect(payload.commands).toEqual(host.env.commits()[0].body!.commands);
    expect(payload.commands[0]).toMatchObject({ op: 'clip.set', select: 'parent/clip:x',
      args: action === 'hold' ? { values: { hold: 8 }, clear: [] } : { values: {}, clear: ['transition'] } });
    expect(JSON.parse(records[0].pending!.request.body).commands).toEqual(payload.commands);
    const expected = structuredClone(original);
    if (action === 'hold') expected.hold = 8;
    else delete expected.transition;
    expect(rowFrom(payload.before, 'parent/clip:x')).toEqual(original);
    expect(rowFrom(payload.after, 'parent/clip:x')).toEqual(expected);
    expect(host.latest().dataRef.current!.resolvedConfig.clips.find((clip) => clip.id === 'x')!.app).toEqual(original.app);
    expect(row).toEqual(original);
    if (action === 'hold') expect(holdInput()).toHaveValue(8);
    else expect(within(transitionSection()).getByRole('combobox')).toHaveValue(NO_TRANSITION);
    await act(async () => { paused.resolve(); await host.latest().commands.flush(); });
    const accepted = await host.env.provider.loadTimelineCommandBasis(scope.timelineId);
    expect((accepted.canonicalDocument.parent_revision.payload.clips as Array<Record<string, JSON>>)[0]).toEqual(expected);
    host.noSnapshots();
  });

  it.each(['conflict', 'validation', 'authorization', 'unavailable'] as const)('retains the hold and durable intent with a visible %s error', async (fault) => {
    const host = await mounted();
    host.env.setFault(fault);
    fireEvent.change(holdInput(), { target: { value: '8' } });
    fireEvent.blur(holdInput());
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/retained|still here|uncertain/));
    expect(holdInput()).toHaveValue(8);
    expect(host.latest().dataRef.current!.config.clips[0].hold).toBe(8);
    const [record] = await host.records();
    expect(record.intents).toHaveLength(1);
    expect(record.pending!.request.body).toBe(JSON.stringify(host.env.commits()[0].body));
    expect(rowFrom((record.intents[0].payload as Payload).after, 'parent/clip:x')).toMatchObject({ hold: 8, app: { opaque } });
    host.noSnapshots();
  });

  it('retains the typed value when capture is unavailable, without using the presentation callback', async () => {
    const host = await mounted();
    const before = host.latest().dataRef.current;
    await act(async () => host.store.getState().syncOpsSlice({ ...host.store.getState().ops, clipScalar: undefined }));
    fireEvent.change(holdInput(), { target: { value: '8' } });
    fireEvent.blur(holdInput());
    expect(screen.getByRole('alert')).toHaveTextContent('clip.set capture is unavailable');
    expect(holdInput()).toHaveValue(8);
    expect(host.latest().dataRef.current).toBe(before);
    expect((await host.records())[0].intents).toHaveLength(0);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it('treats an empty hold as no edit, never a wire clear', async () => {
    const host = await mounted();
    fireEvent.change(holdInput(), { target: { value: '' } });
    fireEvent.blur(holdInput(), { target: { value: '' } });
    expect(host.captureSpy).not.toHaveBeenCalled();
    expect((await host.records())[0].intents).toHaveLength(0);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it.each(['0', '-1'])('retains an invalid hold %s locally without mutation or append', async (value) => {
    const host = await mounted();
    const before = host.latest().dataRef.current;
    fireEvent.change(holdInput(), { target: { value } });
    fireEvent.blur(holdInput());
    fireEvent.blur(holdInput());
    expect(screen.getByRole('alert')).toHaveTextContent('positive');
    expect(holdInput()).toHaveValue(Number(value));
    expect(host.captureSpy).toHaveBeenCalledTimes(1);
    expect(host.latest().dataRef.current).toBe(before);
    expect((await host.records())[0].intents).toHaveLength(0);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it('retains a failed transition removal and displays the capture error', async () => {
    const host = await mounted(parentDocument(), 'x', 'effects');
    await act(async () => host.store.getState().syncOpsSlice({ ...host.store.getState().ops, clipScalar: undefined }));
    fireEvent.click(within(transitionSection()).getByRole('button', { name: 'Remove' }));
    expect(screen.getByRole('alert')).toHaveTextContent('clip.set capture is unavailable');
    expect(host.latest().dataRef.current!.config.clips[0].transition).toEqual({ type: 'crossfade', duration: 0.5, params: { custom: 'keep' } });
    expect((await host.records())[0].intents).toHaveLength(0);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it('refuses an interleaved edit without recapturing the typed hold guards', async () => {
    const host = await mounted();
    fireEvent.change(holdInput(), { target: { value: '8' } });
    await act(async () => {
      expect(host.service.moveClip({ clipId: 'x', time: 5 }).ok).toBe(true);
      await host.latest().commands.flush();
    });
    fireEvent.blur(holdInput());
    expect(screen.getByRole('alert')).toHaveTextContent('Timeline changed during the scalar edit');
    expect(holdInput()).toHaveValue(8);
    expect(host.captureSpy).toHaveBeenCalledTimes(1);
    expect(host.env.commits()).toHaveLength(1);
    expect(host.env.commits()[0].body!.commands[0].op).toBe('clip.move');
    expect(host.latest().dataRef.current!.config.clips[0].hold).toBe(6);
    host.noSnapshots();
  });

  it('refuses unsupported mixed fields atomically before preview or append', async () => {
    const host = await mounted();
    const before = host.latest().dataRef.current;
    expect(() => submitClipScalarEdit(host.capture(), { values: { hold: 8, speed: 3 }, clear: ['transition'] }))
      .toThrow('clip.set only supports hold values');
    expect(host.latest().dataRef.current).toBe(before);
    expect((await host.records())[0].intents).toHaveLength(0);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it('shares the same outbox for a lost hold ACK and newer typing, retrying the exact original request', async () => {
    const host = await mounted();
    host.env.setFault('lost');
    fireEvent.change(holdInput(), { target: { value: '8' } });
    fireEvent.blur(holdInput());
    await waitFor(() => expect(host.latest().commands.state.status).toBe('retry'));
    const first = (await host.records())[0];
    fireEvent.change(holdInput(), { target: { value: '9' } });
    fireEvent.blur(holdInput());
    await waitFor(async () => expect((await host.records())[0].intents).toHaveLength(2));
    const queued = (await host.records())[0];
    expect(queued.ownerId).toBe(first.ownerId);
    expect(queued.pending!.request).toEqual(first.pending!.request);
    expect(queued.intents[1].basis).toEqual({ after: queued.intents[0].id });
    expect((queued.intents[1].payload as Payload).commands[0]).toMatchObject({
      args: { values: { hold: 9 }, clear: [] }, expect: { 'parent/clip:x::hold': { state: 'present', value: 8 } } });
    expect(host.env.commits()).toHaveLength(1);
    fireEvent.click(screen.getByTestId('timeline-command-retry'));
    await waitFor(() => expect(host.latest().commands.state.status).toBe('saved'));
    expect(host.env.commits()).toHaveLength(3);
    expect(JSON.stringify(host.env.commits()[1].body)).toBe(first.pending!.request.body);
    expect(host.env.commits()[1].key).toBe(first.pending!.request.key);
    expect(host.env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1' });
    expect(holdInput()).toHaveValue(9);
    host.noSnapshots();
  });

  it('binds a projected occurrence hold to its raw owner and preserves opaque data and its shared sibling', async () => {
    const host = await mounted(occurrenceDocument(), 'f2-occurrence:f2-agent-clip');
    host.env.setFault('conflict'); // This fixture transport does not model child publication.
    fireEvent.change(holdInput(), { target: { value: '4' } });
    fireEvent.blur(holdInput());
    await waitFor(() => expect(host.latest().commands.state.status).toBe('conflict'));
    const [record] = await host.records();
    const payload = record.intents[0].payload as Payload;
    expect(payload.commands[0]).toMatchObject({ op: 'clip.set', select: 'occurrence:f2-occurrence/clip:f2-agent-clip',
      args: { values: { hold: 4 }, clear: [] }, expect: { 'occurrence:f2-occurrence/clip:f2-agent-clip::hold': { state: 'present', value: 3 } } });
    expect(JSON.parse(record.pending!.request.body).commands).toEqual(payload.commands);
    const ref = 'occurrence:f2-occurrence/clip:f2-agent-clip';
    expect(rowFrom(payload.after, ref)).toEqual({ ...rowFrom(payload.before, ref), hold: 4 });
    const sibling = 'occurrence:shared-sibling/clip:f2-agent-clip';
    expect(rowFrom(payload.after, sibling)).toEqual(rowFrom(payload.before, sibling));
    expect(holdInput()).toHaveValue(4);
    host.noSnapshots();
  });

  it('visibly refuses a forged occurrence binding before preview or outbox append', async () => {
    const host = await mounted(occurrenceDocument(), 'f2-occurrence:f2-agent-clip');
    const current = host.latest().dataRef.current!;
    const clip = current.resolvedConfig.clips.find((candidate) => candidate.id === 'f2-occurrence:f2-agent-clip')!;
    clip.app = { ...clip.app, canonical: { ...(clip.app!.canonical as object), ownerRef: 'occurrence:shared-sibling' } };
    fireEvent.change(holdInput(), { target: { value: '4' } });
    fireEvent.blur(holdInput());
    expect(screen.getByRole('alert')).toHaveTextContent('matching raw clip owner');
    expect(holdInput()).toHaveValue(4);
    expect(host.latest().dataRef.current).toBe(current);
    expect((await host.records())[0].intents).toHaveLength(0);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it('refuses a complete shared sibling binding on another occurrence output through the actual hook', async () => {
    const host = await mounted(occurrenceDocument(), 'f2-occurrence:f2-agent-clip');
    const current = host.latest().dataRef.current!;
    const clip = current.resolvedConfig.clips.find((candidate) => candidate.id === 'f2-occurrence:f2-agent-clip')!;
    const sibling = current.resolvedConfig.clips.find((candidate) => candidate.id === 'shared-sibling:f2-agent-clip')!;
    clip.app = { ...clip.app, canonical: structuredClone(sibling.app!.canonical) };
    const before = structuredClone(current);
    const records = await host.records();
    fireEvent.change(holdInput(), { target: { value: '4' } });
    fireEvent.blur(holdInput());
    expect(screen.getByRole('alert')).toHaveTextContent('matching raw clip owner');
    expect(holdInput()).toHaveValue(4);
    expect(host.captureSpy).toHaveBeenCalledTimes(1);
    expect(host.latest().dataRef.current).toEqual(before);
    expect(await host.records()).toEqual(records);
    expect(host.env.commits()).toHaveLength(0);
    host.noSnapshots();
  });

  it('keeps transition SET and duration on their original callback without converting them to clears', async () => {
    const host = await mounted(parentDocument(), 'x', 'effects');
    fireEvent.change(within(transitionSection()).getByRole('combobox'), { target: { value: 'crossfade' } });
    expect(host.legacyChange).toHaveBeenLastCalledWith({ transition: { type: 'crossfade', duration: 0.5, params: undefined } });
    fireEvent.change(within(transitionSection()).getByRole('spinbutton'), { target: { value: '0.75' } });
    expect(host.legacyChange).toHaveBeenLastCalledWith({ transition: { type: 'crossfade', duration: 0.75, params: { custom: 'keep' } } });
    expect(host.captureSpy).not.toHaveBeenCalled();
    expect(host.env.commits()).toHaveLength(0);
  });

  it('keeps non-scalar timing edits on the original callback without clearing omitted fields', async () => {
    const host = await mounted();
    const start = within(screen.getByText('Start (seconds)').parentElement!).getByRole('spinbutton');
    fireEvent.change(start, { target: { value: '2' } });
    expect(host.legacyChange).toHaveBeenCalledWith({ at: 2 });
    expect(host.captureSpy).not.toHaveBeenCalled();
    expect(host.env.commits()).toHaveLength(0);
    expect((await host.records())[0].intents).toHaveLength(0);
  });
});
