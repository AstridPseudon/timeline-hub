// @vitest-environment jsdom
// Mount the actual command bootstrap and preview consumer. Only the provider
// verified-basis boundary and Remotion media/clock/Player are test adapters.
import React, { type CSSProperties, type PropsWithChildren } from 'react';
import { act, cleanup, render, renderHook, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import type { TimelineCommandBasis, DataProvider } from '../../data/DataProvider.ts';
import { useTimelineCommandSession } from '../../hooks/useTimelineCommandSession.ts';
import { useTimelineCommit } from '../../hooks/useTimelineCommit.ts';
import { TimelineEventBus } from '../../hooks/useTimelineEventBus.ts';
import { useTimelineDataSelector } from '../../hooks/timelineStore.ts';
import type { TimelineData } from '../../lib/timeline-data.ts';
import type { PreviewRevision } from './previewRevision.ts';
import { TimelineComposition, compileCanonicalTransitions, prepareCompositionScene, toRuntimeTheme } from '@banodoco/timeline-composition';
import { querySceneFrame } from '@banodoco/timeline-composition/evaluation';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { CanonicalDocument, Transport } from '@/integrations/runtime/generated.ts';
import { VideoEditorRuntimeProvider, type VideoEditorRuntimeContextValue } from '@/tools/video-editor/contexts/VideoEditorRuntimeContext.tsx';
import { createTimelineStore, TimelineStoreProvider } from '@/tools/video-editor/hooks/timelineStore.ts';
import { buildTimelineData, loadTimelineJsonFromProvider } from '@/tools/video-editor/lib/timeline-data.ts';
import { createShotCompositionAdapter } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { compilePlayerTransitions, playerEvaluationClip, preparePlayerTrack } from '@/tools/video-editor/compositions/playerEvaluation.ts';
import { VisualClipSequence } from '@/tools/video-editor/compositions/VisualClip.tsx';
import { resolveTimelineRenderTheme } from '@/tools/video-editor/compositions/installed-themes.ts';
import { useVideoEditorPreviewComposition } from '@/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts';
import { useVideoEditorPreviewSurface } from '@/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx';
import type { CompiledCanonicalTransitions } from '@banodoco/timeline-composition';
import type { ResolvedTimelineConfig, TimelineConfig } from '@/tools/video-editor/types/index.ts';

let currentFrame = 0;
const player = vi.hoisted(() => ({ config: null as ResolvedTimelineConfig | null,
  compiled: undefined as CompiledCanonicalTransitions | undefined,
  delivered: [] as { config: ResolvedTimelineConfig; compiledTransitions?: CompiledCanonicalTransitions; previewRevision: PreviewRevision }[] }));
vi.mock('@remotion/player', async () => {
  const React = await import('react');
  return { Player: React.forwardRef(function Player(props: {
    inputProps: { config: ResolvedTimelineConfig; compiledTransitions?: CompiledCanonicalTransitions; previewRevision: PreviewRevision };
  }, ref) {
    player.delivered.push(props.inputProps);
    player.config = props.inputProps.config;
    player.compiled = props.inputProps.compiledTransitions;
    React.useImperativeHandle(ref, () => ({ addEventListener: vi.fn(), removeEventListener: vi.fn(),
      getCurrentFrame: () => 0, isPlaying: () => false, seekTo: vi.fn(), play: vi.fn(), pause: vi.fn(), toggle: vi.fn() }), []);
    return <div />;
  }) };
});
vi.mock('remotion', async () => {
  const React = await import('react');
  const Frame = React.createContext<number | null>(null);
  const useFrame = () => React.useContext(Frame) ?? currentFrame;
  return {
    useCurrentFrame: useFrame,
    Img: ({ src }: { src: string }) => <div data-public-src={src} data-frame={useFrame()} />,
    useVideoConfig: () => ({ fps: 30, width: 1920, height: 1080 }),
    useRemotionEnvironment: () => ({ isRendering: false, isClientSideRendering: false }),
    interpolate: (frame: number, [from, to]: number[]) => Math.min(1, Math.max(0, (frame - from) / (to - from))),
    AbsoluteFill: ({ children, style }: PropsWithChildren<{ style?: CSSProperties }>) => <div style={style}>{children}</div>,
    Sequence: ({ children, from = 0, durationInFrames = Infinity }: PropsWithChildren<{
      from?: number; durationInFrames?: number;
    }>) => {
      const frame = useFrame();
      if (frame < from || frame >= from + durationInFrames) return null;
      return <Frame.Provider value={frame - from}>{children}</Frame.Provider>;
    },
    Freeze: ({ frame, children }: PropsWithChildren<{ frame: number }>) => (
      <Frame.Provider value={frame}>{children}</Frame.Provider>
    ),
  };
});
vi.mock('@astrid/packs/rendering/shared/readiness-image', async () => {
  const { useCurrentFrame } = await import('remotion');
  return { ReadinessImage: ({ mediaId }: { mediaId: string }) => (
    <div data-preview-id={mediaId} data-frame={useCurrentFrame()} />
  ) };
});

const projectId = 'project-read', timelineId = 'timeline-read';
const head = { revisionId: 'read-r0', publicationId: 'read-p0' };
const track = { id: 'V1', kind: 'visual' as const, label: 'Picture' };
const cases = [
  { name: 'first', at: 2, duration: 0.4, first: true, frames: [60, 66, 89, 90] },
  { name: 'gap', at: 2, duration: 0.4, first: false, frames: [48, 54, 89, 90] },
  { name: 'oversized', at: 1, duration: 2, first: false, frames: [0, 30, 89, 90] },
];
async function readFixture(testCase: typeof cases[number]) {
  const image = (id: string, at: number) => ({ id, at, track: 'V1', clipType: 'hold' as const, hold: 1, asset: id });
  const clips = [...(testCase.first ? [] : [image('a', 0)]),
    { ...image('b', testCase.at), transition: { type: 'fade', duration: testCase.duration } }, image('c', testCase.at + 3)];
  const opaque = JSON.parse('{"opaque":{"retained":[null,false,[]]},"nullable":null,"ordered":[0,false,null,[],{}],"enabled":false,"count":0,"label":"","__proto__":{"prototype":null,"__proto__":[]},"constructor":false,"prototype":[]}');
  const config: TimelineConfig = { ...opaque, tracks: [track], clips,
    output: { fps: 30, resolution: '1920x1080', file: 'read.mp4' } };
  const registry = { assets: Object.fromEntries(clips.map(clip => [clip.id, {
    type: 'image' as const, file: `https://example.test/${clip.id}.png`,
  }])) };
  const payload = { config, tracks: [track], clips, registry, occurrences: [] };
  const document: CanonicalDocument = { schema_version: 1, project_id: projectId, timeline_id: timelineId,
    parent_revision: { revision_id: head.revisionId, content_digest: fixtureDigest(payload), payload },
    shot_revisions: [], internal_timeline_revisions: [],
    dependency_manifest: { shots: [], internal_timelines: [], media: [], documents: [] } };
  const calls: string[] = [];
  const transport: Transport = async (method, path) => {
    calls.push(`${method} ${path}`);
    const ok = (value: unknown) => ({ status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(value)) });
    if (path === '/v1/health') return ok({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      runtime_epoch: 1, runtime_instance_id: 'read-instance' });
    if (path === '/v1/handshake') return ok({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      actor_id: 'read-actor', realm_id: 'read-realm', scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read',
        'objects:write', 'tasks:read', 'tasks:write'], capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return ok({ realm_id: 'read-realm' });
    if (method === 'POST' && path === `/v1/projects/${projectId}/timelines/${timelineId}/inspect`) return ok({
      schema: 'runtime.timeline.declared_inputs/v1', evidence_kind: 'declared_inputs', render_requested: false,
      representation: 'canonical_head', authority: 'runtime_parent_composition', project_id: projectId, timeline_id: timelineId,
      revision_id: head.revisionId, head_revision_id: head.revisionId, head_publication_id: head.publicationId,
      is_current_head: true, parent_content_digest: document.parent_revision.content_digest,
      head_content_digest: document.parent_revision.content_digest, snapshot_digest: fixtureDigest(document),
      selectors: {}, selection_status: 'selected', target_count: 0, occurrence_count: 0, parent_clip_count: clips.length,
      parent_clip_target_count: 0, selected_clip_count: 0, selected: [], selected_parent_clips: [], next_cursor: null,
    });
    if (method === 'GET' && path === `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions/${head.revisionId}`) {
      return ok({ project_id: projectId, timeline_id: timelineId, ...document.parent_revision,
        dependency_manifest: document.dependency_manifest });
    }
    throw new Error(`Unexpected request: ${method} ${path}`);
  };
  const provider = new RuntimeDataProvider({ projectId, baseUrl: `http://read-${crypto.randomUUID()}.test`, token: 'token', transport });
  const data = await loadTimelineJsonFromProvider(provider, timelineId);
  expect(data.head).toEqual({ projectId, timelineId, headRevisionId: head.revisionId, headPublicationId: head.publicationId });
  expect(data.config.clips).toEqual(clips);
  expect(calls.filter(call => call.includes('/composition-revisions/'))).toHaveLength(1);
  expect(calls.every(call => call.startsWith('GET ') || call.endsWith('/inspect') || call.endsWith('/handshake'))).toBe(true);
  return { provider, data, document, calls, opaque, original: structuredClone(document) };
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(done => { resolve = done; });
  return { promise, resolve };
}

async function mountRead(testCase: typeof cases[number], delayAssets = false) {
  const fixture = await readFixture(testCase);
  const { provider, data: initial, document, calls } = fixture;
  if (delayAssets) {
    document.parent_revision.payload.registry = { assets: Object.fromEntries(
      Object.keys(initial.registry.assets).map(id => [id, { type: 'image', file: `${id}.png` }])) };
    document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
  }
  const basis: TimelineCommandBasis = { canonicalDocument: document, head };
  const read = deferred<TimelineCommandBasis>();
  // Provider closure verification has its own tests. This fixture deliberately
  // qualifies the producer/consumer seam after that boundary has admitted it.
  const load = vi.spyOn(provider, 'loadTimelineCommandBasis').mockReturnValue(read.promise);
  const assets = deferred<string>();
  const resolve = vi.spyOn(provider, 'resolveTimelineCommandAsset').mockImplementation(file =>
    delayAssets ? assets.promise : Promise.resolve(file));
  const save = vi.spyOn(provider, 'saveTimeline');
  const saveAtHead = vi.spyOn(provider, 'saveTimelineAtHead');
  vi.stubGlobal('indexedDB', createFakeIndexedDB());
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const store = createTimelineStore();
  store.getState().syncDataSlice({ ...store.getState().data, data: initial, resolvedConfig: initial.resolvedConfig });
  store.getState().syncChromeSlice({ ...store.getState().chrome, saveStatus: 'saved' });
  const shots = { shotComposition: createShotCompositionAdapter(provider.shotComposition), canonicalComposition: null, canonicalDraft: null,
    canonicalCompositionError: null, shots: [], isLoading: false, error: null, refetchShots: vi.fn(),
    finalVideoMap: new Map(), dismissFinalVideo: vi.fn() };
  const runtime: Pick<VideoEditorRuntimeContextValue, 'project' | 'timelineId' | 'userId' | 'shots'> = {
    project: { projectId }, timelineId, userId: null, shots };
  const wrapper = ({ children }: PropsWithChildren) => <VideoEditorRuntimeProvider value={runtime as VideoEditorRuntimeContextValue}>
    <TimelineStoreProvider store={store}>{children}</TimelineStoreProvider>
  </VideoEditorRuntimeProvider>;
  function Surface() {
    const data = useTimelineDataSelector(slice => slice.data);
    const config = useTimelineDataSelector(slice => slice.resolvedConfig);
    const composition = useVideoEditorPreviewComposition(config, data);
    const surface = useVideoEditorPreviewSurface();
    return <><div data-testid="initial-source">{composition.source}</div><div ref={surface.slotRef} />{surface.portal}</>;
  }
  const surface = render(<Surface />, { wrapper });
  expect(initial.editProjection).toBeUndefined();
  expect(player.config).toBe(initial.resolvedConfig);
  expect(player.compiled).toBeUndefined();
  expect(screen.getByTestId('initial-source')).toHaveTextContent('legacy');
  const eventBus = new TimelineEventBus();
  const snapshots = vi.fn();
  eventBus.on('scheduleSave', snapshots);
  const lastSavedSignatureRef = { current: initial.stableSignature };
  const configVersionRef = { current: initial.configVersion };
  const headRevisionRef = { current: initial.head };
  const snapshotWriteBlockedRef = { current: false };
  const installed: TimelineData[] = [];
  const hook = renderHook(({ provider }: { provider: DataProvider }) => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider, timelineId,
      commit: { ...commit, commitData: (data, options) => {
        commit.commitData(data, options);
        const committed = commit.dataRef.current!;
        installed.push(committed);
      } }, legacyClean: () => true, snapshotWriteBlockedRef, resolveAssetUrl: async file => file,
      loaded: initial, configVersionRef, headRevisionRef, lastSavedSignatureRef, store, shots });
    React.useLayoutEffect(() => {
      if (!commit.data) return;
      // Model the host subscription to the actual commit result. Keep the old
      // derived slice for facts, as equal-signature host memoization can do.
      store.getState().syncDataSlice({ ...store.getState().data, data: commit.data,
        resolvedConfig: commit.data.editProjection ? initial.resolvedConfig : commit.data.resolvedConfig });
    }, [commit.data]);
    return { commit, commands };
  }, { initialProps: { provider: provider as DataProvider }, wrapper });
  return { ...fixture, initial, basis, hook, surface, installed, held, resolve, assets, headRevisionRef, configVersionRef,
    release: () => act(() => { read.resolve(basis); }),
    assertNoWrites: () => {
      expect(snapshots).not.toHaveBeenCalled();
      expect(save).not.toHaveBeenCalled();
      expect(saveAtHead).not.toHaveBeenCalled();
      expect(calls.some(call => call.endsWith('/commit'))).toBe(false);
      expect(basis).not.toHaveProperty('graph');
      expect(load).toHaveBeenCalled();
    } };
}

async function initialRead(testCase: typeof cases[number]) {
  const mounted = await mountRead(testCase);
  mounted.release();
  await waitFor(() => expect(mounted.hook.result.current.commands.port).toBeDefined());
  const data = mounted.hook.result.current.commit.data!;
  await waitFor(() => expect(player.config).toBe(data.resolvedConfig));
  expect(data.editProjection).toEqual({ kind: 'accepted', head });
  expect(data.head).toEqual(mounted.initial.head);
  expect(mounted.installed).toEqual([data]);
  expect(screen.getByTestId('initial-source')).toHaveTextContent('canonical');
  expect(player.compiled).toBeDefined();
  expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed read-r0');
  const expected = await buildTimelineData({ ...mounted.document.parent_revision.payload.config as TimelineConfig,
    clips: mounted.document.parent_revision.payload.clips as TimelineConfig['clips'] }, mounted.initial.registry,
    async file => file, mounted.initial.configVersion + 1, undefined, mounted.initial.head);
  expect(data).toEqual({ ...expected, editProjection: { kind: 'accepted', head } });
  for (const config of [mounted.initial.config, mounted.initial.resolvedConfig, data.config, data.resolvedConfig]) {
    expect(Object.fromEntries(Object.keys(mounted.opaque).map(key => [key, (config as unknown as Record<string, unknown>)[key]]))).toStrictEqual(mounted.opaque);
    for (const key of Object.keys(mounted.opaque)) expect(Object.hasOwn(config, key)).toBe(true);
    expect(Object.getPrototypeOf(config)).toBe(Object.prototype);
    expect(Object.hasOwn(config, 'absent')).toBe(false);
    expect(config).not.toHaveProperty('editProjection');
  }
  expect(mounted.document).toStrictEqual(mounted.original);
  expect(mounted.headRevisionRef.current).toEqual(data.head);
  expect(mounted.configVersionRef.current).toBe(data.configVersion);
  // Every delivered props tuple is wholly raw or wholly projected, including
  // the 150ms mailbox interval. A head or saved status alone never adds a vector.
  for (const props of player.delivered) {
    expect(props.previewRevision).toEqual({ kind: 'committed', revisionId: head.revisionId });
    expect(Object.fromEntries(Object.keys(mounted.opaque).map(key => [key, (props.config as unknown as Record<string, unknown>)[key]]))).toStrictEqual(mounted.opaque);
    expect(props.config).not.toHaveProperty('editProjection');
    if (props.config === mounted.initial.resolvedConfig) expect(props.compiledTransitions).toBeUndefined();
    else {
      expect(props.config).toBe(data.resolvedConfig);
      expect(props.compiledTransitions).toEqual(compilePlayerTransitions(data.resolvedConfig));
    }
  }
  mounted.assertNoWrites();
  return { data, delivered: { config: player.config!, compiled: player.compiled } };
}
afterEach(() => { cleanup(); currentFrame = 0; player.delivered = []; vi.unstubAllGlobals(); vi.restoreAllMocks(); });

it.each(cases)('$name initial canonical read selects the canonical compiler without edits or a graph', async testCase => {
  const { delivered } = await initialRead(testCase);
  expect(delivered.compiled).toEqual(compilePlayerTransitions(delivered.config));
});

it.each(cases.flatMap(testCase => testCase.frames.map(frame => ({ ...testCase, frame }))))(
  '$name initial read at frame $frame matches public canonical picture and content clock', async testCase => {
    const { data, delivered } = await initialRead(testCase);
    const clips = delivered.config.clips;
    const inputs = [{ track, clips: clips.map(playerEvaluationClip) }];
    const theme = toRuntimeTheme(resolveTimelineRenderTheme({}));
    const compiled = compileCanonicalTransitions(inputs, 30, theme);
    expect(delivered.compiled).toEqual(compiled);
    const publicScene = prepareCompositionScene(inputs, data.registry, 30, theme, 1920, 1080,
      undefined, undefined, undefined, undefined, undefined, undefined, compiled);
    const preview = preparePlayerTrack(track, clips, 30, 1920, 1080, undefined, delivered.compiled);
    const incoming = clips.find(clip => clip.id === 'b')!;
    currentFrame = testCase.frame;
    const view = render(<>
      <VisualClipSequence clip={incoming} predecessor={testCase.first ? undefined : clips[0]} track={track} fps={30}
        drawPlan={preview.plans.get('b') ?? null} />
      <TimelineComposition timeline={{ ...delivered.config, theme: 'default', clips: inputs[0].clips }}
        assets={data.registry} compiledTransitions={compiled} />
    </>);
    const readPicture = (node: Element | null) => {
      if (!node) return null;
      let opacity = 1;
      for (let parent = node.parentElement; parent; parent = parent.parentElement) {
        if (parent.style.opacity) opacity *= Number(parent.style.opacity);
      }
      return { contentFrame: Number(node.getAttribute('data-frame')), opacity };
    };
    const actual = readPicture(view.container.querySelector('[data-preview-id="b"]'));
    const expected = readPicture(view.container.querySelector(`[data-public-src="${incoming.assetEntry!.src}"]`));
    const layer = querySceneFrame(publicScene, currentFrame).layers.find(layer => layer.clipId === 'b');
    if (currentFrame === 90) expect(querySceneFrame(publicScene, currentFrame).layers).toEqual([]);
    expect(expected).toEqual(layer ? { contentFrame: layer.contentFrame, opacity: layer.transitionOpacity } : null);
    expect(actual).toEqual(expected);
  },
);

it.each(['local mutation', 'newer accepted head', 'unmount'] as const)(
  'a delayed initial verified read preserves an intervening %s through the mounted delivery', async intervening => {
    const mounted = await mountRead(cases[0], true);
    mounted.release();
    await waitFor(() => expect(mounted.resolve).toHaveBeenCalled());
    expect(mounted.installed).toEqual([]);
    let retained: TimelineData | null = mounted.initial;
    if (intervening === 'local mutation') {
      act(() => {
        mounted.hook.result.current.commit.applyEdit({ type: 'config', resolvedConfig: {
          ...mounted.initial.resolvedConfig, clips: mounted.initial.resolvedConfig.clips.map(clip => ({ ...clip, label: 'local edit' })),
        } }, { save: false });
      });
      retained = mounted.hook.result.current.commit.data;
      expect(retained?.config.clips[0].label).toBe('local edit');
      await waitFor(() => expect(player.config).toBe(retained!.resolvedConfig));
      expect(player.compiled).toBeUndefined();
    } else if (intervening === 'newer accepted head') {
      const newer = structuredClone(mounted.basis);
      newer.head = { revisionId: 'read-new', publicationId: 'publication-new' };
      newer.canonicalDocument.parent_revision.revision_id = newer.head.revisionId;
      (newer.canonicalDocument.parent_revision.payload.clips as TimelineConfig['clips'])[0].label = 'newer accepted';
      newer.canonicalDocument.parent_revision.content_digest = fixtureDigest(newer.canonicalDocument.parent_revision.payload);
      // Reinitialize the real lifecycle at the new provider generation. The new
      // accepted fact is produced by the hook, never assigned to a raw config.
      const provider = Object.create(mounted.provider) as RuntimeDataProvider;
      provider.loadTimelineCommandBasis = vi.fn().mockResolvedValue(newer);
      provider.resolveTimelineCommandAsset = vi.fn(async file => `https://example.test/${file}`);
      act(() => { mounted.hook.rerender({ provider }); });
      await waitFor(() => expect(mounted.hook.result.current.commit.data?.editProjection).toEqual({ kind: 'accepted', head: newer.head }));
      retained = mounted.hook.result.current.commit.data;
      await waitFor(() => expect(player.config).toBe(retained!.resolvedConfig));
      expect(screen.getByTestId('preview-revision-label')).toHaveTextContent('Committed read-new');
    } else {
      mounted.hook.unmount();
      mounted.surface.unmount();
    }
    const installed = [...mounted.installed];
    const headBefore = mounted.headRevisionRef.current;
    const versionBefore = mounted.configVersionRef.current;
    const deliveredBefore = [...player.delivered];
    await act(async () => { mounted.assets.resolve('https://example.test/late.png'); await mounted.assets.promise; });
    if (intervening === 'unmount') await waitFor(() => expect(mounted.held.size).toBe(0));
    else await waitFor(() => expect(mounted.hook.result.current.commands.port).toBeDefined());
    expect(mounted.hook.result.current.commit.dataRef.current).toBe(retained);
    expect(mounted.installed).toEqual(installed);
    expect(mounted.headRevisionRef.current).toBe(headBefore);
    expect(mounted.configVersionRef.current).toBe(versionBefore);
    expect(player.delivered).toEqual(deliveredBefore);
    mounted.assertNoWrites();
  },
);
