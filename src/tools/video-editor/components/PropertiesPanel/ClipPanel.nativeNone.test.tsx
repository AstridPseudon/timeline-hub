// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { useLayoutEffect, type ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { CanonicalDocument, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '../../contexts/VideoEditorRuntimeContext.tsx';
import { document, environment, scope } from '../../commands/__tests__/commitSessionEnvironment.ts';
import { AuthoredState } from '../../commands/clipMovePrimitives.ts';
import { submitClipScalarEdit, type CapturedClipScalarEdit } from '../../commands/clipScalarGesture.ts';
import { createShotCompositionAdapter } from '../../data/shotCompositionAdapter.ts';
import { loadTimelineDraft } from '../../data/timelineDraftIndexedDb.ts';
import { projectCanonicalComposition } from '../../data/shotCompositionProjection.ts';
import { buildTimelineData } from '../../lib/timeline-data.ts';
import { createInteractionState } from '../../lib/interaction-state.ts';
import { createTimelineStore, TimelineStoreProvider, useTimelineEditorData } from '../../hooks/timelineStore.ts';
import { useClipScalarControl } from '../../hooks/useClipScalarControl.ts';
import { useTimelineSave } from '../../hooks/useTimelineSave.ts';
import { createTimelineCommands } from '../../hooks/useTimelineCommandsService.ts';
import { TimelineCommandRecovery } from '../TimelineCommandRecovery.tsx';
import { BulkClipPanelBody, type BulkClipPanelProps } from './BulkClipPanelBody.tsx';
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
vi.mock('@/shared/components/ui/select.tsx', async () => {
  const { createContext, useContext } = await vi.importActual<typeof import('react')>('react');
  const SelectValueContext = createContext<string | null>(null);
  return {
    Select: ({ value, onValueChange, children }: { value: string; onValueChange: (value: string) => void; children?: ReactNode }) => (
      <SelectValueContext.Provider value={value}>
        <select value={value} onChange={(event) => onValueChange(event.currentTarget.value)}>
          <option value="__none__">None</option><option value="crossfade">crossfade</option><option value="wipe">wipe</option>
        </select>
        {children}
      </SelectValueContext.Provider>
    ),
    SelectTrigger: ({ children }: { children?: ReactNode }) => <div>{children}</div>,
    SelectContent: ({ children }: { children?: ReactNode }) => <div>{children}</div>,
    SelectItem: ({ children }: { children?: ReactNode }) => <div>{children}</div>,
    SelectValue: ({ children, placeholder }: { children?: ReactNode; placeholder?: string }) => {
      const value = useContext(SelectValueContext);
      return <span data-testid="select-value">{children ?? value ?? placeholder}</span>;
    },
  };
});

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
      deviceClass="desktop" hasPredecessor={false}
      onChange={legacyChange} onScalarEditStart={capture} onResetPosition={vi.fn()} onClose={vi.fn()}
      onToggleMute={vi.fn()} onSplitAtPlayhead={vi.fn()} onMoveTrackUp={vi.fn()} onMoveTrackDown={vi.fn()}
      onSetInteractionMode={vi.fn()} compositionWidth={1920} compositionHeight={1080}
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
  // The mounted save hook holds command-session bootstrap behind its initial
  // IndexedDB recovery read. Drain that real read before using the session's
  // existing readiness surface, as the production editor does.
  await loadTimelineDraft(scope.timelineId);
  await act(async () => {
    await Promise.resolve();
    await Promise.resolve();
    await Promise.resolve();
  });
  await waitFor(() => expect(latest.commands.port).toBeDefined());
  expect(latest.commands.clipScalarPort).toBeDefined();
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

function transitionSection() {
  return screen.getByText('Transition').parentElement!;
}
const rowFrom = (bundle: unknown, ref: string) => new AuthoredState(bundle as never).entity(ref)!;
type Payload = { commands: EditCommand[]; before: unknown; after: unknown };

function bulkProps(sharedTransitionType: string | null = NO_TRANSITION): BulkClipPanelProps & { effectResources: never } {
  return {
    clips: [{} as never], visibleTabs: ['effects'], compositionWidth: 1920, compositionHeight: 1080,
    sharedEntrance: null, sharedExit: null, sharedContinuous: null, sharedText: null, sharedTransition: null,
    sharedEntranceType: null, sharedExitType: null, sharedContinuousType: null, sharedTransitionType,
    sharedSpeed: null, sharedFrom: null, sharedTo: null, sharedX: null, sharedY: null, sharedWidth: null,
    sharedHeight: null, sharedOpacity: null, sharedVolume: null, sharedFontSize: null, sharedTextColor: null,
    sharedTransitionDuration: null, onChange: vi.fn(), onChangeDeep: vi.fn(), onScalarEditsStart: vi.fn(() => []),
    onResetPosition: vi.fn(), onToggleMute: vi.fn(), onClose: vi.fn(), activeTab: 'effects', setActiveTab: vi.fn(),
    effectResources: {
      data: { entrance: [], exit: [], continuous: [] }, effects: [], entrance: [], exit: [], continuous: [],
      isLoading: false, isFetching: false, error: null, refetch: vi.fn(async () => undefined),
      canCreateEffect: false, canUpdateEffect: false, canDeleteEffect: false,
    } as never,
  };
}

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe('mounted native transition clear controls (unit transport)', () => {
  it('renders None for the bulk native transition sentinel', () => {
    render(<BulkClipPanelBody {...bulkProps()} />);
    const section = screen.getByText('Transition').parentElement!;
    expect(within(section).getByTestId('select-value')).toHaveTextContent('None');
    expect(within(section).getByTestId('select-value')).not.toHaveTextContent(NO_TRANSITION);
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


  it('keeps transition SET and duration on their original callback without converting them to clears', async () => {
    const host = await mounted(parentDocument(), 'x', 'effects');
    fireEvent.change(within(transitionSection()).getByRole('combobox'), { target: { value: 'crossfade' } });
    expect(host.legacyChange).toHaveBeenLastCalledWith({ transition: { type: 'crossfade', duration: 0.5, params: undefined } });
    fireEvent.change(within(transitionSection()).getByRole('spinbutton'), { target: { value: '0.75' } });
    expect(host.legacyChange).toHaveBeenLastCalledWith({ transition: { type: 'crossfade', duration: 0.75, params: { custom: 'keep' } } });
    expect(host.captureSpy).not.toHaveBeenCalled();
    expect(host.env.commits()).toHaveLength(0);
  });

});
