// @vitest-environment jsdom
import { act, cleanup, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import type { CanonicalDocument, CommitRequest, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { occurrenceMediaFixtureGraph } from '../commands/__tests__/occurrenceMediaFixture.ts';
import type { DataProvider } from '../data/DataProvider.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { authoringBundleFromDocument } from '../commands/authoringBundle.ts';
import { environment } from '../commands/__tests__/commitSessionEnvironment.ts';
import { captureOccurrenceMediaEdit, occurrenceMediaPreview, projectOccurrenceMediaPreview, submitOccurrenceMediaEdit,
  type OccurrenceMediaRequest } from '../commands/occurrenceMediaGesture.ts';
import fixture from '../commands/fixtures/recipe_m2_occurrence_media.json';
import { createTimelineStore } from './timelineStore.ts';
import { TimelineEventBus } from './useTimelineEventBus.ts';
import { useTimelineCommit } from './useTimelineCommit.ts';
import { useTimelineCommandSession } from './useTimelineCommandSession.ts';

afterEach(() => { cleanup(); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

const request: OccurrenceMediaRequest = { kind: 'add', ownerRef: 'occurrence:occ-a', trackRef: 'occurrence:occ-a/track:picture',
  row: fixture.add.commands[0].args.row, media: fixture.add.commands[0].args.media };

async function setup() {
  const env = await environment();
  vi.stubGlobal('indexedDB', env.factory);
  const held = new Set<string>();
  vi.stubGlobal('navigator', { locks: { request: async (key: string, _options: unknown, work: (lock: unknown) => Promise<unknown>) => {
    if (held.has(key)) return work(null);
    held.add(key);
    try { return await work({ name: key }); } finally { held.delete(key); }
  } } });
  const raw: CanonicalDocument = { ...structuredClone(fixture.add.input), schema_version: 1 };
  const head = { revisionId: raw.parent_revision.revision_id, publicationId: 'p0' };
  const parent = raw.parent_revision.payload;
  const seed = await buildTimelineData({ ...parent.config as TimelineConfig, clips: parent.clips as TimelineConfig['clips'] },
    parent.registry as AssetRegistry, undefined, 1, undefined, { projectId: raw.project_id, timelineId: raw.timeline_id,
      headRevisionId: head.revisionId, headPublicationId: head.publicationId });
  const graph = occurrenceMediaFixtureGraph(raw);
  const shotComposition = { load: async () => graph };
  const initial = projectOccurrenceMediaPreview(occurrenceMediaPreview(await authoringBundleFromDocument(raw), graph), seed, shotComposition)!;
  let release!: (input: VerifiedMedia) => void;
  const read = vi.fn(() => new Promise<VerifiedMedia>((resolve) => { release = resolve; }));
  const send = vi.fn(async (_request: CommitRequest, _key: string) => { throw new Error('uncertain unit sender'); });
  const snapshots = vi.fn();
  const provider: DataProvider & { getProjectVerifiedMedia: typeof read } = { ...env.provider, resolveAssetUrl: async (file) => file,
    loadTimeline: vi.fn(), loadAssetRegistry: vi.fn(), saveTimeline: snapshots,
    getRecoverableIdentity: async () => ({ realmId: 'realm-1', actorId: 'actor-1' }),
    loadTimelineCommandBasis: async () => ({ head, canonicalDocument: raw, graph }),
    shotComposition, commitTimeline: send, getProjectVerifiedMedia: read };
  const configVersionRef = { current: initial.configVersion }, headRevisionRef = { current: initial.head };
  const lastSavedSignatureRef = { current: initial.stableSignature }, snapshotWriteBlockedRef = { current: false };
  const store = createTimelineStore(), eventBus = new TimelineEventBus();
  eventBus.on('scheduleSave', snapshots);
  let clean = true;
  const hook = renderHook(({ activeProvider, timelineId }: { activeProvider: DataProvider; timelineId: string }) => {
    const commit = useTimelineCommit({ eventBus, lastSavedSignatureRef, initialData: initial, snapshotWriteBlockedRef });
    const commands = useTimelineCommandSession({ provider: activeProvider, timelineId, commit, legacyClean: () => clean,
      resolveAssetUrl: async (file) => file, loaded: undefined, snapshotWriteBlockedRef, headRevisionRef,
      configVersionRef, lastSavedSignatureRef, store, shots: { canonicalDraft: null, shots: undefined, isLoading: false,
        error: null, refetchShots: vi.fn(), finalVideoMap: new Map(), dismissFinalVideo: vi.fn() } });
    return { commit, commands };
  }, { initialProps: { activeProvider: provider, timelineId: raw.timeline_id } });
  await waitFor(() => expect(hook.result.current.commands.occurrenceMediaPort).toBeDefined());
  return { hook, provider, send, read, snapshots, snapshotWriteBlockedRef, initial,
    current: () => hook.result.current.commit.dataRef.current!, release: () => release(structuredClone(fixture.add.verified_media[1])),
    setClean: (value: boolean) => { clean = value; } };
}

// Deferred App-only tests: detached read fixtures confer no media authority or Runtime acceptance.
describe('mounted occurrence media read fences', () => {
  it.each(['project', 'timeline', 'unmount', 'display', 'head'] as const)('refuses a late verified read after %s changes without preview or writes', async (change) => {
    const env = await setup();
    const captured = captureOccurrenceMediaEdit(env.hook.result.current.commands.occurrenceMediaPort, env.current(), request);
    const before = env.current();
    let rejected!: Promise<void>;
    act(() => { rejected = submitOccurrenceMediaEdit(captured); });
    const refusal = expect(rejected).rejects.toThrow();
    if (change === 'unmount') env.hook.unmount();
    else if (change === 'display' || change === 'head') act(() => {
      const changed = change === 'head'
        ? { ...before, head: { ...before.head!, headRevisionId: 'another-head', headPublicationId: 'another-publication' } }
        : { ...before, configVersion: before.configVersion + 1 };
      env.hook.result.current.commit.commitData(changed, { save: false, skipHistory: true });
    });
    else env.hook.rerender({ activeProvider: change === 'project'
      ? { ...env.provider, loadTimelineCommandBasis: async () => { throw new Error('another project'); } } : env.provider,
    timelineId: change === 'timeline' ? 'another-timeline' : 'film' });
    await act(async () => { env.release(); await refusal; });
    expect(env.send).not.toHaveBeenCalled();
    expect(env.snapshots).not.toHaveBeenCalled();
    expect(before.config.clips.some((clip) => clip.id === 'occ-a:reserved-child')).toBe(false);
    env.hook.unmount();
  });

  it('requires clean legacy state before and after the async read and retains the original request', async () => {
    const env = await setup(), port = env.hook.result.current.commands.occurrenceMediaPort!;
    env.setClean(false);
    expect(() => captureOccurrenceMediaEdit(port, env.current(), request)).toThrow('earlier timeline saves');
    env.setClean(true);
    const captured = captureOccurrenceMediaEdit(port, env.current(), request), original = structuredClone(captured.basis);
    const pending = submitOccurrenceMediaEdit(captured);
    env.setClean(false);
    const refusal = expect(pending).rejects.toThrow('earlier timeline saves');
    await act(async () => { env.release(); await refusal; });
    expect(captured.basis).toEqual(original);
    expect(env.send).not.toHaveBeenCalled();
    expect(env.snapshots).not.toHaveBeenCalled();
    env.hook.unmount();
  });

  it('previews and retains a prepared ADD through the same mounted outbox without a snapshot save', async () => {
    const env = await setup();
    const captured = captureOccurrenceMediaEdit(env.hook.result.current.commands.occurrenceMediaPort, env.current(), request);
    const pending = submitOccurrenceMediaEdit(captured);
    await act(async () => { env.release(); await pending; });
    await waitFor(() => expect(env.hook.result.current.commands.state.status).toBe('retry'));
    expect(env.current().editProjection).toMatchObject({ kind: 'local', base: {
      revisionId: fixture.add.input.parent_revision.revision_id, publicationId: 'p0',
    } });
    expect(env.current().resolvedConfig.clips.find((clip) => clip.id === 'occ-a:reserved-child'))
      .toMatchObject({ at: 8.125, from: 2, to: 6, speed: 2 });
    expect(env.send.mock.calls[0][0].commands).toEqual(fixture.add.commands);
    expect(env.snapshotWriteBlockedRef.current).toBe(true);
    expect(env.snapshots).not.toHaveBeenCalled();
    env.hook.unmount();
  });
});
