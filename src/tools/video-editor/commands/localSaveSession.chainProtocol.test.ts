import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { ApiError } from '@/integrations/runtime/generated.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { CommitRequest, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureClipMove, finishClipMove } from './clipMoveCapture.ts';
import { createCommitOutbox, toOutboxJson, type OutboxJson, type OutboxRecord } from './commitOutbox.ts';
import { createLocalSaveSession, type LocalSaveSession } from './localSaveSession.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { createTimelineLocalSaveHandoff, type TimelineGestureReadBasis, type TimelineSaveSource } from '../hooks/timelineLocalSaveHandoff.ts';
import { createDefaultTimelineConfig } from '../lib/defaults.ts';
import type { TimelineConfig } from '../types/index.ts';

const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project-commit', timelineId: 'timeline-commit' };
const h0 = { revisionId: 'r0', publicationId: 'p0' };

function canonical(at = 1, revision = h0.revisionId, publication = h0.publicationId) {
  const document = acceptedCommit({ revision_id: revision, publication_id: publication },
    { revision_id: h0.revisionId, publication_id: h0.publicationId }).data.canonical_document;
  const parent = document.parent_revision.payload as Record<string, OutboxJson>;
  const config = createDefaultTimelineConfig();
  config.clips = [{ id: 'x', track: 'V1', at, hold: 1, text: { content: 'keep' }, app: { opaque: null } }];
  parent.config = config;
  parent.registry = { assets: {} };
  parent.clips = structuredClone(config.clips);
  parent.tracks = structuredClone(config.tracks);
  parent.occurrences = [];
  parent.opaque = { absent: null };
  document.parent_revision.content_digest = fixtureDigest(parent);
  return document;
}

function sourceFor(document: ReturnType<typeof canonical>, publicationId = h0.publicationId): TimelineSaveSource {
  const parent = document.parent_revision.payload as Record<string, OutboxJson>;
  return {
    config: structuredClone(parent.config) as unknown as TimelineConfig,
    registry: structuredClone(parent.registry) as TimelineSaveSource['registry'],
    head: { projectId: document.project_id, timelineId: document.timeline_id,
      headRevisionId: document.parent_revision.revision_id, headPublicationId: publicationId },
  };
}

function sourceAt(source: TimelineSaveSource, at: number): TimelineSaveSource {
  const next = structuredClone(source);
  next.config.clips[0].at = at;
  return next;
}

function moveBasis(source: TimelineSaveSource): TimelineGestureReadBasis {
  return { kind: 'move', clipId: 'x', trackId: 'V1', config: structuredClone(source.config), registry: structuredClone(source.registry) };
}

function result(document: ReturnType<typeof canonical>, head: { revisionId: string; publicationId: string }, base = h0): TimelineCommitResult {
  const response = acceptedCommit({ revision_id: head.revisionId, publication_id: head.publicationId },
    { revision_id: base.revisionId, publication_id: base.publicationId });
  response.data.canonical_document = structuredClone(document);
  response.data.canonical_document.parent_revision.revision_id = head.revisionId;
  response.data.canonical_document.parent_revision.content_digest = fixtureDigest(
    response.data.canonical_document.parent_revision.payload,
  );
  response.data.document_digest = fixtureDigest(response.data.canonical_document);
  return { response, accepted: head, canonicalDocument: response.data.canonical_document, graph: {}, receipt: response.receipt };
}

async function editOwner(factory: ReturnType<typeof createFakeIndexedDB>, change: (record: OutboxRecord) => void) {
  await new Promise<void>((resolve, reject) => {
    const request = factory.open('astrid.command-outbox', 1);
    request.addEventListener('error', () => reject(request.error));
    request.addEventListener('success', () => {
      const db = request.result;
      const tx = db.transaction('owners', 'readwrite');
      const store = tx.objectStore('owners');
      const read = store.getAll();
      read.addEventListener('success', () => {
        for (const record of read.result as OutboxRecord[]) {
          change(record);
          store.put(record, JSON.stringify([scope.realmId, scope.actorId, scope.projectId, scope.timelineId, record.ownerId]));
        }
      });
      tx.addEventListener('complete', () => { db.close(); resolve(); });
      tx.addEventListener('abort', () => { db.close(); reject(tx.error); });
    });
  });
}

function environment() {
  const initialDocument = canonical();
  const initial: TimelineCommandBasis = { head: h0, canonicalDocument: initialDocument };
  const factory = createFakeIndexedDB();
  const outboxes = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (_key, work) => work() });
  const send = vi.fn<(request: CommitRequest, key: string) => Promise<TimelineCommitResult>>();
  const prepareDisplay = vi.fn(async (basis: TimelineCommandBasis, draft?: OutboxJson) => {
    await authoringBundleFromDocument(basis.canonicalDocument);
    const document = structuredClone(draft ?? toOutboxJson(basis.canonicalDocument));
    return { document, adopt() {} };
  });
  const mount = async (basis = initial) => {
    const session = await createLocalSaveSession({ scope, initial: basis,
      document: toOutboxJson(basis.canonicalDocument), outboxes, send, loadLatest: async () => basis,
      prepareDisplay, changed: () => {} });
    const source = sourceFor(basis.canonicalDocument, basis.head.publicationId);
    const handoff = createTimelineLocalSaveHandoff({ initial: basis, source, session,
      adopted: (landed) => ({ receipt: { configVersion: 0, head: { projectId: scope.projectId, timelineId: scope.timelineId,
        headRevisionId: landed.head.revisionId, headPublicationId: landed.head.publicationId } }, source: sourceFor(landed.canonicalDocument, landed.head.publicationId) }) });
    return { session, handoff, source };
  };
  return { initial, factory, outboxes, send, prepareDisplay, mount,
    accepted: (at: number, head: { revisionId: string; publicationId: string }, base = h0) =>
      result(canonical(at, head.revisionId, head.publicationId), head, base) };
}

describe('local save session chain protocol', () => {
  it('keeps an unknown free transform conservative instead of inferring reads from its changes', async () => {
    const env = environment();
    const { session } = await env.mount();
    const before = env.initial.canonicalDocument;
    const after = structuredClone(before);
    ((after.parent_revision.payload as Record<string, OutboxJson>).opaque as Record<string, OutboxJson>).absent = 'authored';
    await session.appendDocument({ before, after, roots: [{ ref: 'parent', revisionId: h0.revisionId,
      contentDigest: before.parent_revision.content_digest }], label: 'Edit timeline',
      step: { id: 'free-transform-step', label: 'Edit timeline', intent: 'Edit timeline', tags: [] } });
    env.send.mockRejectedValueOnce(new Error('patch transport unavailable'));
    await expect(session.flush()).rejects.toThrow('draft retained');
    const first = env.send.mock.calls[0];
    const request = first[0];
    expect(request).toMatchObject({ api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
      base_revision_id: 'r0', base_publication_id: 'p0', label: 'Edit timeline', merge: 'atomic', dry_run: false,
      source: { via: 'app' } });
    expect(request).not.toHaveProperty('reads');
    expect(request.steps?.[0].patch).toEqual(request.commands[0].args.changes);
    env.send.mockResolvedValueOnce(env.accepted(1, { revisionId: 'r1', publicationId: 'p1' }));
    await session.flush();
    expect(env.send.mock.calls[1]).toEqual(first);
    await session.dispose();
  });

  it.each([
    ['missing dependency manifest', (document: Record<string, unknown>) => { delete document.dependency_manifest; }, ''],
    ['changed project scope', (document: Record<string, unknown>) => { document.project_id = 'other-project'; }, 'scope'],
  ] as const)('refuses a corrupt original display closure and retains the saved draft: %s', async (_name, corrupt, reason) => {
    const env = environment();
    const { session } = await env.mount();
    const before = env.initial.canonicalDocument;
    const after = structuredClone(before);
    ((after.parent_revision.payload as Record<string, OutboxJson>).opaque as Record<string, OutboxJson>).absent = 'authored';
    await session.appendDocument({ before, after, roots: [{ ref: 'parent', revisionId: h0.revisionId,
      contentDigest: before.parent_revision.content_digest }], label: 'Edit timeline',
      step: { id: 'corrupt-closure-step', label: 'Edit timeline', intent: 'Edit timeline', tags: [] } });
    env.send.mockRejectedValueOnce(new Error('busy'));
    await expect(session.flush()).rejects.toThrow('draft retained');
    const [saved] = await env.outboxes.list(scope);
    await session.dispose();
    await editOwner(env.factory, (record) => corrupt((record.intents[0].payload as { displayBasis: { canonicalDocument: Record<string, unknown> } }).displayBasis.canonicalDocument));
    const [corrupted] = await env.outboxes.list(scope);
    const beforeRefusal = { intents: structuredClone(corrupted.intents), pending: structuredClone(corrupted.pending) };
    const newer = { head: { revisionId: 'newer', publicationId: 'newer-p' }, canonicalDocument: canonical(1, 'newer') };
    const reopened = await env.mount(newer);
    const recovery = reopened.session.recover(saved.ownerId);
    if (reason) await expect(recovery).rejects.toThrow(reason);
    else await expect(recovery).rejects.toThrow();
    expect(reopened.session.getState().status).toBe('saved');
    expect(env.send).toHaveBeenCalledTimes(1);
    const [retained] = await env.outboxes.list(scope);
    expect({ intents: retained.intents, pending: retained.pending }).toEqual(beforeRefusal);
    await reopened.session.dispose();
  });

  it('captures dependent A5/B7 before preview, submits B at HA with original guards and a fresh key', async () => {
    const env = environment();
    const { session, handoff, source } = await env.mount();
    const a = sourceAt(source, 5);
    const b = sourceAt(a, 7);
    await handoff.capture(a, moveBasis(source));
    await handoff.capture(b, moveBasis(a));
    const gate = deferred<void>();
    env.send.mockImplementationOnce(async () => { await gate.promise; return env.accepted(5, { revisionId: 'r1', publicationId: 'p1' }); });
    env.send.mockResolvedValueOnce(env.accepted(7, { revisionId: 'r2', publicationId: 'p2' }, { revisionId: 'r1', publicationId: 'p1' }));
    const flushing = handoff.flush();
    await vi.waitFor(() => expect(env.send).toHaveBeenCalledTimes(1));
    expect(env.prepareDisplay).not.toHaveBeenCalled();
    gate.resolve();
    await flushing;
    const [first, second] = env.send.mock.calls;
    expect(first[0].base_publication_id).toBe('p0');
    expect(second[0].base_publication_id).toBe('p1');
    expect(second[0].commands[0].args.changes).toContainEqual({ op: 'set', ref: 'parent', path: ['clips', 'id:x', 'at'],
      before: { state: 'present', value: 5 }, value: 7 });
    expect(second[1]).not.toBe(first[1]);
    expect(env.prepareDisplay).toHaveBeenCalledTimes(2);
    await session.dispose();
  });

  it('keeps a drag capture original when its predecessor is acknowledged before drop', async () => {
    const env = environment();
    const first = await env.mount();
    const a = sourceAt(first.source, 5);
    const captured = moveBasis(a);
    const original = structuredClone(captured);
    await first.handoff.capture(a, moveBasis(first.source));
    env.send.mockRejectedValueOnce(new Error('lost acknowledgement'));
    await expect(first.handoff.flush()).rejects.toThrow('draft retained');
    env.send.mockResolvedValueOnce(env.accepted(5, { revisionId: 'r1', publicationId: 'p1' }));
    await first.handoff.flush();
    const landed = sourceFor(canonical(5, 'r1', 'p1'), 'p1');
    await first.handoff.capture(sourceAt(landed, 7), captured);
    env.send.mockResolvedValueOnce(env.accepted(7, { revisionId: 'r2', publicationId: 'p2' }, { revisionId: 'r1', publicationId: 'p1' }));
    await first.handoff.flush();
    expect(captured).toEqual(original);
    expect(env.send.mock.calls[2][0].base_publication_id).toBe('p1');
    expect(env.send.mock.calls[2][0].commands[0].args.changes).toContainEqual({ op: 'set', ref: 'parent', path: ['clips', 'id:x', 'at'],
      before: { state: 'present', value: 5 }, value: 7 });
    await first.session.dispose();
  });

  it('advances publication identity when a same-value move reuses the content revision', async () => {
    const env = environment();
    const { session, handoff, source } = await env.mount();
    await handoff.capture(sourceAt(source, 5), moveBasis(source));
    env.send.mockResolvedValueOnce(env.accepted(5, { revisionId: 'r1', publicationId: 'p1' }));
    const firstLanded = await handoff.flush();
    expect(firstLanded.head).toMatchObject({ headRevisionId: 'r1', headPublicationId: 'p1' });
    const bundle = await authoringBundleFromDocument(session.getDocument() as never);
    const captured = captureClipMove(bundle, 'parent/clip:x');
    const prepared = finishClipMove(captured, 5);
    const before = session.getDocument();
    await session.append({ before, after: before, label: 'Move timeline', commands: [prepared.command] });
    env.send.mockResolvedValueOnce(env.accepted(5, { revisionId: 'r1', publicationId: 'p2' }, { revisionId: 'r1', publicationId: 'p1' }));
    const secondLanded = await session.flush();
    expect(secondLanded.head).toEqual({ revisionId: 'r1', publicationId: 'p2' });
    expect(env.send.mock.calls.slice(0, 2).map(([request]) => ({ revisionId: request.base_revision_id, publicationId: request.base_publication_id }))).toEqual([
      { revisionId: 'r0', publicationId: 'p0' }, { revisionId: 'r1', publicationId: 'p1' },
    ]);
    const inverse: EditCommand = { schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
      args: { publications: ['p2'] } };
    const undoBefore = session.getDocument();
    await session.append({ before: undoBefore, after: undoBefore, label: 'Undo timeline', commands: [inverse] });
    env.send.mockResolvedValueOnce(env.accepted(1, { revisionId: 'r2', publicationId: 'p3' }, { revisionId: 'r1', publicationId: 'p2' }));
    await session.flush();
    expect(env.send.mock.calls[2][0]).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p2', commands: [inverse] });
    await session.dispose();
  });

  it.each(['accepted', 'conflict'] as const)('queues B authored after uncertain A without retransmitting, then recovers exact A: %s', async (outcome) => {
    const env = environment();
    const first = await env.mount();
    const a = sourceAt(first.source, 5);
    const b = sourceAt(a, 7);
    const basisB = moveBasis(a);
    await first.handoff.capture(a, moveBasis(first.source));
    env.send.mockRejectedValueOnce(new Error('lost acknowledgement'));
    await expect(first.handoff.flush()).rejects.toThrow('draft retained');
    const [original] = await env.outboxes.list(scope);
    const requestA = original.pending!.request;
    const wireA = structuredClone(env.send.mock.calls[0]);
    await first.handoff.capture(b, basisB);
    await expect(first.handoff.capture(sourceAt(b, 9), basisB)).rejects.toThrow('gesture read basis');
    const [queued] = await env.outboxes.list(scope);
    expect(queued.pending).toEqual(original.pending);
    expect(queued.intents).toHaveLength(2);
    expect(queued.intents[1]).toMatchObject({ basis: { after: queued.intents[0].id }, payload: { displayBasis: env.initial } });
    expect(queued.intents[1].readyBase).toBeUndefined();
    expect(env.send.mock.calls).toEqual([wireA]);
    expect(basisB).toEqual(moveBasis(a));
    await first.session.dispose();

    const acceptedA = env.accepted(5, { revisionId: 'r1', publicationId: 'p1' });
    const recovered = await env.mount({ head: acceptedA.accepted, canonicalDocument: acceptedA.canonicalDocument });
    if (outcome === 'accepted') {
      env.send.mockResolvedValueOnce(acceptedA).mockResolvedValueOnce(env.accepted(7, { revisionId: 'r2', publicationId: 'p2' }, { revisionId: 'r1', publicationId: 'p1' }));
    } else {
      env.send.mockResolvedValueOnce(acceptedA).mockRejectedValueOnce(new ApiError(409, 'conflict', 'conflict', '', { status: 'conflict' }));
    }
    await recovered.session.recover(queued.ownerId);
    expect(env.send.mock.calls[1]).toEqual([JSON.parse(requestA.body), requestA.key]);
    expect(env.send.mock.calls[1][0]).toEqual(JSON.parse(requestA.body));
    if (outcome === 'accepted') {
      expect(env.send).toHaveBeenCalledTimes(3);
      expect(env.send.mock.calls[2][0]).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1' });
      expect(recovered.session.getState().status).toBe('saved');
      expect(recovered.session.getDocument()).toMatchObject({ parent_revision: { payload: { config: { clips: [{ at: 7 }] } } } });
    } else {
      expect(recovered.session.getState().status).toBe('conflict');
      const [retained] = await env.outboxes.list(scope);
      expect(retained.intents.every((intent) => intent.conflict !== undefined)).toBe(true);
      expect(retained.pending?.request).not.toEqual(requestA);
      expect(JSON.parse(retained.pending!.request.body).base_publication_id).toBe('p1');
      await expect(recovered.session.flush()).rejects.toThrow('draft retained');
      expect(env.send).toHaveBeenCalledTimes(3);
    }
    await recovered.session.dispose();
  });
});

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((done) => { resolve = done; });
  return { promise, resolve };
}
