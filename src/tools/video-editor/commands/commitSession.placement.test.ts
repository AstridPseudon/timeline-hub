import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import type { CanonicalDocument, CommandRecord, CommitRequest, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import type { ResolvedTimelineConfig } from '../types/index.ts';
import type { PreparedShotComposition } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { stableOccurrenceDeepLink, stableOutputIdentity } from '../data/shotComposition.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { createTimelineCommandSession, type TimelineCommandSession } from './commitSession.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { capturePlacement, finishPlacement } from './placementCapture.ts';
import { copy } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_placement.json';

type Golden = { input: CanonicalDocument; output: CanonicalDocument; command: EditCommand; records: CommandRecord[];
  request: { owner: 'parent' | `occurrence:${string}`; ownership: 'parent' | 'occurrence'; clip_id: string; on: number } };
const cases = (fixture as unknown as { cases: Golden[] }).cases;
const initialHead = { revisionId: cases[0].input.parent_revision.revision_id, publicationId: 'original-publication' };
const scope = { projectId: cases[0].input.project_id, timelineId: cases[0].input.timeline_id, realmId: 'realm', actorId: 'actor' };
const displayId = (golden: Golden) => golden.request.owner === 'parent' ? golden.request.clip_id
  : `${golden.request.owner.slice(11)}:${golden.request.clip_id}`;

function display(raw: CanonicalDocument, pin: TimelineCommandBasis['head']): TimelineData {
  const parent = raw.parent_revision.payload;
  const occurrences = (parent.occurrences as Array<Record<string, JSON>>).map((occurrence, ordinal) => {
    const shot = raw.shot_revisions.find((image) => image.revision_id === occurrence.shot_revision_id)!;
    const internal = raw.internal_timeline_revisions.find((image) => image.revision_id === shot.internal_timeline_revision_id)!;
    const occurrenceId = occurrence.occurrence_id as string;
    return { projectId: raw.project_id, parentDocumentId: raw.timeline_id, occurrenceId,
      shotId: shot.shot_id, revisionId: shot.revision_id, ordinal,
      atMs: (occurrence.placement as { start_ms: number }).start_ms, durationMs: occurrence.duration_ms as number,
      trackId: occurrence.track as string, sourceOffsetMs: occurrence.source_offset as number,
      speed: occurrence.speed as number, gain: occurrence.gain as number, muted: occurrence.muted as boolean,
      stableDeepLink: stableOccurrenceDeepLink(raw.project_id, raw.timeline_id, shot.shot_id, shot.revision_id, occurrenceId),
      outputIdentity: stableOutputIdentity(raw.project_id, raw.timeline_id, occurrenceId),
      revision: { ...copy(shot.payload), shot_id: shot.shot_id, revision_id: shot.revision_id,
        internal_timeline_revision: { revision_id: internal.revision_id, timeline: copy(internal.payload) } },
    };
  });
  const composition: PreparedShotComposition = {
    projectId: raw.project_id, parentDocumentId: raw.timeline_id, headRevisionId: pin.revisionId, occurrences,
    contract: { schema_version: 1, project: { project_id: raw.project_id, document_id: raw.timeline_id },
      primary_timeline: { document_id: raw.timeline_id, head: { revision_id: pin.revisionId } },
      parent_composition: copy(parent), shot_revisions: raw.shot_revisions.map((shot) =>
        occurrences.find((occurrence) => occurrence.shotId === shot.shot_id && occurrence.revisionId === shot.revision_id)!.revision),
      occurrences: copy(parent.occurrences) as Array<Record<string, JSON>>, cases: {} },
  };
  const { config } = projectCanonicalComposition(composition, {
    ...copy(parent.config as object), 
    clips: copy(parent.clips), registry: {},
  } as ResolvedTimelineConfig);
  return assembleTimelineData({ config, configVersion: 1, head: { projectId: raw.project_id, timelineId: raw.timeline_id,
    headRevisionId: pin.revisionId, headPublicationId: pin.publicationId }, registry: { assets: {} },
  resolvedConfig: { ...config, tracks: config.tracks ?? [], registry: {} }, output: config.output, assetMap: {} });
}


// Controlled unit responses qualify App capture/outbox semantics, not Runtime acceptance.
async function setup(golden = cases[0], input = copy(golden.input)) {
  const initial: TimelineCommandBasis = { head: initialHead, canonicalDocument: input };
  let current = display(input, initialHead);
  const previews = vi.fn((patch) => {
    const next = compileTimelinePatch(patch, current).nextData;
    if (!next) throw new Error('Invalid placement preview');
    current = next;
  });
  const projected = vi.fn(async (basis: TimelineCommandBasis, patches) => {
    current = display(basis.canonicalDocument, basis.head);
    patches.forEach(previews);
  });
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  const requests: Array<{ body: string; key: string }> = [];
  let send: (request: CommitRequest, key: string) => Promise<TimelineCommitResult> = async () => { throw new Error('lost acknowledgement'); };
  const mount = (basis = initial) => createTimelineCommandSession({ initial: basis, scope, outboxes,
    send: (request, key) => { requests.push({ body: JSON.stringify(request), key }); return send(request, key); },
    preview: previews, project: projected, changed: () => {} });
  const capture = (session: TimelineCommandSession, on = golden.request.on) => session.placementPort.capture({
    clipId: displayId(golden), ownerRef: golden.request.owner, ownership: golden.request.ownership, on, current });
  const place = (session: TimelineCommandSession, on = golden.request.on) => {
    const basis = capture(session, on);
    const prepared = session.placementPort.finish(basis, on);
    session.placementPort.submit(prepared);
    return { basis, ...prepared };
  };
  const result = (request: CommitRequest, document = golden.output, publicationId = 'accepted-A'): TimelineCommitResult => {
    const accepted = { revisionId: document.parent_revision.revision_id, publicationId };
    const response = acceptedCommit({ revision_id: accepted.revisionId, publication_id: publicationId },
      { revision_id: request.base_revision_id, publication_id: request.base_publication_id },
      { projectId: scope.projectId, timelineId: scope.timelineId, commands: request.commands });
    Object.assign(response.data, { canonical_document: copy(document), document_digest: fixtureDigest(document) });
    response.receipt.result = response.data;
    return { response, accepted, canonicalDocument: copy(document), graph: {}, receipt: response.receipt };
  };
  return { initial, mount, outboxes, requests, previews, projected, capture, place, result, current: () => current,
    setSend: (next: typeof send) => { send = next; } };
}

const requestAt = (env: Awaited<ReturnType<typeof setup>>, index: number) => JSON.parse(env.requests[index].body) as CommitRequest;

describe('explicit placement in the existing durable session', () => {
  it.each(cases)('retains the exact native golden command and basis for $request.owner', async (golden) => {
    const env = await setup(golden);
    const session = await env.mount();
    const { basis, command } = env.place(session);
    expect(command).toEqual(golden.command);
    expect(basis.bundle).toEqual(await authoringBundleFromDocument(golden.input));
    expect(basis.localBasis).toEqual({ head: initialHead });
    await session.retry();
    expect(session.getState().status).toBe('retry');
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents[0].basis).toEqual({ head: initialHead });
    expect(saved.intents[0].payload).toMatchObject({ commands: [golden.command], before: basis.bundle,
      displayBasis: env.initial });
    expect(JSON.parse(saved.pending!.request.body).commands).toEqual([golden.command]);
    expect(requestAt(env, 0)).toEqual({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
      base_revision_id: initialHead.revisionId, base_publication_id: initialHead.publicationId,
      commands: [golden.command], source: { via: 'app' } });
    expect(env.current().resolvedConfig.clips.find((clip) => clip.id === displayId(golden))!.at).toBe(golden.request.on);
    await session.dispose();
  });

  it.each(cases)('recovers exact request bytes and identity, then projects accepted closure and inverse for $request.owner', async (golden) => {
    const env = await setup(golden);
    const first = await env.mount();
    env.place(first);
    await first.retry();
    const original = copy(env.requests[0]);
    const owner = first.getState().ownerId!;
    await first.dispose();
    const fresh: TimelineCommandBasis = { head: { revisionId: golden.output.parent_revision.revision_id, publicationId: 'accepted-A' },
      canonicalDocument: golden.output };
    const second = await env.mount(fresh);
    expect(second.getState().status).toBe('recovery');
    expect(env.requests.every((request) => request.body === original.body && request.key === original.key)).toBe(true);
    env.setSend(async (request) => env.result(request));
    await second.recover(owner);
    expect(env.requests.at(-1)).toEqual(original);
    expect(second.getState().status).toBe('saved');
    expect(env.projected.mock.calls.at(-1)).toEqual([{ ...fresh, graph: {} }, []]);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    const restored = copy(golden.input);
    restored.parent_revision.revision_id = 'restored-revision';
    env.setSend(async (request) => env.result(request, restored, 'inverse-publication'));
    await second.undo();
    expect(requestAt(env, env.requests.length - 1)).toMatchObject({ base_revision_id: fresh.head.revisionId,
      base_publication_id: 'accepted-A', commands: [{ op: 'timeline.inverse', args: { publications: ['accepted-A'] } }] });
    expect(env.projected.mock.calls.at(-1)![0].canonicalDocument).toEqual(restored);
    expect(second.getState().canUndo).toBe(false);
    await second.dispose();
  });

  it('persists B after unacknowledged A, keeps its original claims through reload, and submits only after A ACK', async () => {
    const golden = cases[0];
    const env = await setup();
    const first = await env.mount();
    const a = env.place(first);
    await first.retry();
    const originalA = copy(env.requests[0]);
    const b = env.place(first, 8.008);
    const nativeA = finishPlacement(capturePlacement(await authoringBundleFromDocument(golden.input), 'parent', 'clip-a', 4.004, 'parent'), 4.004);
    const nativeB = finishPlacement(capturePlacement(nativeA.bundle, 'parent', 'clip-a', 8.008, 'parent'), 8.008);
    expect(b.command).toEqual(nativeB.command);
    expect(b.command).not.toEqual(a.command);
    await first.retry();
    expect(env.requests.every((request) => request.body === originalA.body && request.key === originalA.key)).toBe(true);
    const [pending] = await env.outboxes.list(scope);
    expect(pending.intents[1].basis).toEqual({ after: pending.intents[0].id });
    expect(pending.intents[1].payload).toMatchObject({ commands: [nativeB.command], before: nativeA.bundle,
      displayBasis: env.initial });
    await first.dispose();
    const second = await env.mount({ head: { revisionId: golden.output.parent_revision.revision_id, publicationId: 'accepted-A' },
      canonicalDocument: golden.output });
    let sawA = false;
    env.setSend(async (request, key) => {
      if (key === originalA.key) { sawA = true; return env.result(request); }
      expect(sawA).toBe(true);
      expect(request).toMatchObject({ base_revision_id: golden.output.parent_revision.revision_id,
        base_publication_id: 'accepted-A', commands: [nativeB.command] });
      const output = copy(golden.output);
      output.parent_revision = { revision_id: 'accepted-B-revision', content_digest: fixtureDigest(nativeB.bundle.parent),
        payload: { ...nativeB.bundle.parent, occurrences: copy(output.parent_revision.payload.occurrences) } };
      return env.result(request, output, 'accepted-B');
    });
    await second.recover(pending.ownerId);
    expect(second.getState().status).toBe('saved');
    const recovery = env.projected.mock.calls.find(([, patches]) => patches.length === 2)!;
    expect(recovery[0]).toEqual(env.initial);
    expect(recovery[1]).toEqual([a.preview, b.preview]);
    expect(env.current().resolvedConfig.clips.find((clip) => clip.id === 'clip-a')!.at).toBe(8.008);
    expect(env.requests.at(-2)).toEqual(originalA);
    expect(requestAt(env, env.requests.length - 1).commands).toEqual([nativeB.command]);
    await second.dispose();
  });

  it('refuses missing explicit ownership or media pins without changing the draft or outbox', async () => {
    const env = await setup();
    const session = await env.mount();
    const before = copy(env.current());
    const saved = await env.outboxes.list(scope);
    for (const ownerRef of [undefined, 'shared', 'occurrence:occ-a']) {
      expect(() => session.placementPort.capture({ clipId: 'clip-a', ownerRef: ownerRef as 'parent', ownership: 'parent',
        on: 4.004, current: env.current() })).toThrow();
    }
    expect(env.current()).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(saved);
    expect(env.requests).toEqual([]);
    await session.dispose();
    const input = copy(cases[0].input);
    input.parent_revision.payload.registry = { assets: {} };
    const unpinned = await setup(cases[0], input);
    const unpinnedSession = await unpinned.mount();
    expect(() => unpinned.capture(unpinnedSession)).toThrow('pinned media');
    expect((await unpinned.outboxes.list(scope))[0].intents).toEqual([]);
    expect(unpinned.requests).toEqual([]);
    await unpinnedSession.dispose();
  });

  it('refuses forged previews, stale generations and fabricated commands without losing a prepared draft', async () => {
    const env = await setup();
    const session = await env.mount();
    const basis = env.capture(session);
    const prepared = session.placementPort.finish(basis, 4.004);
    expect(() => session.placementPort.submit({ ...prepared, preview: { version: 1, operations: [] } })).toThrow('exact same-clip');
    expect(() => session.placementPort.submit({ ...prepared, command: { ...prepared.command, op: 'clip.delete' } })).toThrow('not captured');
    session.placementPort.submit(prepared);
    expect(() => session.placementPort.finish(basis, 4.004)).toThrow('changed during placement');
    await session.dispose();
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(1);
  });
});
