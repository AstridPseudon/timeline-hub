import { describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { ApiError, type CanonicalDocument } from '@/integrations/runtime/generated.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { CommitRequest, HistoryPage } from '@/integrations/runtime/timeline-commit-types.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { createDefaultTimelineConfig } from '../lib/defaults.ts';
import { createCommitOutbox, toOutboxJson, type OutboxJson } from './commitOutbox.ts';
import { createLocalSaveSession, type LocalSaveSession } from './localSaveSession.ts';
import { createTimelineLocalSaveHandoff, type TimelineSaveSource } from '../hooks/timelineLocalSaveHandoff.ts';

const scope = { realmId: 'realm', actorId: 'actor', projectId: 'project-commit', timelineId: 'timeline-commit' };
const h0 = { revisionId: 'r0', publicationId: 'p0' };

type ParentPayload = Record<string, OutboxJson>;

function parent(document: CanonicalDocument): ParentPayload {
  return document.parent_revision.payload as unknown as ParentPayload;
}

function track(source: TimelineSaveSource): Record<string, OutboxJson> {
  return (source.config.tracks as unknown as Array<Record<string, OutboxJson>>)[0];
}

function sourceFor(document: CanonicalDocument, head: { revisionId: string; publicationId: string }): TimelineSaveSource {
  const payload = parent(document);
  return {
    config: structuredClone(payload.config) as unknown as TimelineConfig,
    registry: structuredClone(payload.registry) as unknown as AssetRegistry,
    head: { projectId: scope.projectId, timelineId: scope.timelineId,
      headRevisionId: head.revisionId, headPublicationId: head.publicationId },
  };
}

function documentFor(source: TimelineSaveSource, basis: CanonicalDocument): CanonicalDocument {
  const next = structuredClone(basis);
  const payload = parent(next);
  const config = structuredClone(source.config) as unknown as ParentPayload;
  payload.config = config;
  payload.registry = structuredClone(source.registry) as unknown as OutboxJson;
  payload.clips = structuredClone(config.clips);
  payload.tracks = structuredClone(config.tracks);
  return next;
}

function acceptedResult(document: CanonicalDocument, head: { revisionId: string; publicationId: string }, base: { revisionId: string; publicationId: string }): TimelineCommitResult {
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

function history(head: { revisionId: string; publicationId: string }): HistoryPage {
  const entry = (revisionId: string, publicationId: string, previous: { revision_id: string; publication_id: string } | null,
    undoOf: string[] = []) => ({ publication_id: publicationId, revision_id: revisionId, previous,
    receipt: {}, intent: revisionId === 'r0' ? 'bootstrap' : 'recorded', records: revisionId === 'r0' ? null : {
      schema_version: 1, commands: [], undo_of: undoOf, restored_from: null,
    }, provider_version: null, compiler_version: null, publisher: null });
  const items = [entry('r0', 'p0', null)];
  if (head.publicationId !== 'p0') items.push(entry('r1', 'p1', { revision_id: 'r0', publication_id: 'p0' }));
  if (head.publicationId !== 'p0' && head.publicationId !== 'p1') {
    items.push(entry(head.revisionId, head.publicationId, { revision_id: 'r1', publication_id: 'p1' }, ['p1']));
  }
  return { items, next_cursor: null, head: { revision_id: head.revisionId, publication_id: head.publicationId } } as unknown as HistoryPage;
}

async function environment(originalLabel?: string) {
  const config = createDefaultTimelineConfig();
  config.clips = [{ id: 'x', track: 'V1', at: 1, hold: 1, clipType: 'video' }];
  config.tracks = config.tracks.map(({ label: _label, ...withoutLabel }) => withoutLabel);
  if (originalLabel !== undefined) (config.tracks[0] as Record<string, OutboxJson>).label = originalLabel;
  const raw = acceptedCommit({ revision_id: h0.revisionId, publication_id: h0.publicationId },
    { revision_id: h0.revisionId, publication_id: h0.publicationId }).data.canonical_document;
  const payload: ParentPayload = {
    config: structuredClone(config) as unknown as OutboxJson,
    registry: { assets: {} },
    clips: structuredClone(config.clips) as unknown as OutboxJson,
    tracks: structuredClone(config.tracks) as unknown as OutboxJson,
    occurrences: [],
    opaque: { absent: null },
  };
  raw.parent_revision.payload = payload as unknown as CanonicalDocument['parent_revision']['payload'];
  raw.parent_revision.content_digest = fixtureDigest(payload);
  const initial: TimelineCommandBasis = { head: h0, canonicalDocument: raw };
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (_key, work) => work() });
  const expected: CanonicalDocument[] = [];
  const replies = new Map<string, TimelineCommitResult>();
  let latest = initial;
  let sequence = 0;
  let loseNext = false;
  let conflictNext = false;
  const visible: OutboxJson[] = [];
  const prepareDisplay = vi.fn(async (basis: TimelineCommandBasis, draft?: OutboxJson) => {
    const document = structuredClone(draft ?? toOutboxJson(basis.canonicalDocument));
    return { document, adopt() { visible.push(document); } };
  });
  const send = vi.fn<(request: CommitRequest, key: string) => Promise<TimelineCommitResult>>(async (request, key) => {
    const existing = replies.get(key);
    if (existing) return existing;
    if (conflictNext) {
      conflictNext = false;
      throw new ApiError(409, 'conflict', 'original capture', '', {
        status: 'conflict', reason: 'original_capture', path: ['tracks', 'id:V1', 'label'],
      });
    }
    const document = expected.shift();
    if (!document) throw new Error('Test transport has no canonical reply queued');
    sequence += 1;
    const head = { revisionId: `r${sequence}`, publicationId: `p${sequence}` };
    const result = acceptedResult(document, head, { revisionId: request.base_revision_id, publicationId: request.base_publication_id });
    replies.set(key, result);
    latest = { head, canonicalDocument: result.canonicalDocument, graph: {} };
    if (loseNext) {
      loseNext = false;
      throw new Error('lost acknowledgement');
    }
    return result;
  });
  const mount = async (basis = latest) => {
    const session = await createLocalSaveSession({ scope, initial: basis, document: toOutboxJson(basis.canonicalDocument),
      outboxes, send, loadLatest: async () => latest, prepareDisplay, changed: () => {} });
    const source = sourceFor(basis.canonicalDocument, basis.head);
    const handoff = createTimelineLocalSaveHandoff({ initial: basis, source, session,
      loadHistory: async () => ({ ...latest, history: history(latest.head) }),
      adopted: (accepted) => ({ receipt: { configVersion: 0, head: { projectId: scope.projectId, timelineId: scope.timelineId,
        headRevisionId: accepted.head.revisionId, headPublicationId: accepted.head.publicationId } }, source: sourceFor(accepted.canonicalDocument, accepted.head) }) });
    return { session, source, handoff };
  };
  return {
    initial, outboxes, send, prepareDisplay, mount, expected, latest: () => latest, visible: () => visible,
    sourceForInitial: () => sourceFor(initial.canonicalDocument, initial.head),
    sourceFor: (basis: TimelineCommandBasis) => sourceFor(basis.canonicalDocument, basis.head),
    queue(document: CanonicalDocument) { expected.push(structuredClone(document)); },
    lose() { loseNext = true; },
    conflict() { conflictNext = true; },
    document(source: TimelineSaveSource, basis = raw) { return documentFor(source, basis); },
    remote(change: (document: CanonicalDocument) => void) {
      const document = structuredClone(latest.canonicalDocument);
      change(document);
      document.parent_revision.revision_id = `external-${latest.head.revisionId}`;
      document.parent_revision.content_digest = fixtureDigest(document.parent_revision.payload);
      return { document, source: sourceFor(document, { revisionId: document.parent_revision.revision_id, publicationId: `external-${latest.head.publicationId}` }) };
    },
  };
}

function withTrackLabel(source: TimelineSaveSource, label: string | undefined): TimelineSaveSource {
  const next = structuredClone(source);
  if (label === undefined) delete track(next).label;
  else track(next).label = label;
  return next;
}

function withClipAt(source: TimelineSaveSource, at: number): TimelineSaveSource {
  const next = structuredClone(source);
  ((next.config.clips as unknown as Array<Record<string, OutboxJson>>)[0]).at = at;
  return next;
}

describe('track labels in the existing durable command session', () => {
  it('forwards mounted empty input as a value-empty label edit', async () => {
    const original = 'Original';
    const env = await environment(original);
    const source = withTrackLabel(env.sourceForInitial(), original);
    const session = await env.mount();
    const next = withTrackLabel(source, '');
    const after = env.document(next, env.initial.canonicalDocument);
    env.queue(after);
    await session.handoff.capture(next);
    await session.handoff.flush();
    const request = env.send.mock.calls[0][0];
    const command = request.commands[0];
    expect(command).toMatchObject({ op: 'doc.patch', version: '1', select: null, created: [],
      args: { changes: [{ op: 'set', ref: 'parent', path: ['tracks', 'id:V1', 'label'],
        before: { state: 'present', value: original }, value: '' }] } });
    const changes = command.args.changes as unknown as Array<Record<string, OutboxJson>>;
    expect(changes).toHaveLength(1);
    expect(changes[0].path).toEqual(['tracks', 'id:V1', 'label']);
    expect(Object.keys(changes[0])).toContain('before');
    const accepted = session.session.getDocument() as unknown as CanonicalDocument;
    const acceptedPayload = parent(accepted);
    const rawPayload = parent(env.initial.canonicalDocument);
    expect((acceptedPayload.config as ParentPayload).tracks).toEqual(expect.arrayContaining([
      expect.objectContaining({ id: 'V1', label: '' }),
    ]));
    expect(acceptedPayload.opaque).toEqual(rawPayload.opaque);
    expect(acceptedPayload.clips).toEqual(rawPayload.clips);
    expect(acceptedPayload.tracks).toEqual((acceptedPayload.config as ParentPayload).tracks);
    expect(accepted.shot_revisions).toEqual(env.initial.canonicalDocument.shot_revisions);
    expect(accepted.internal_timeline_revisions).toEqual(env.initial.canonicalDocument.internal_timeline_revisions);
    expect(accepted.dependency_manifest).toEqual(env.initial.canonicalDocument.dependency_manifest);
    expect(env.send.mock.calls.every(([sent]) => sent.commands.every(({ op }) => op === 'doc.patch'))).toBe(true);
    await session.session.dispose();
  });

  it('keeps queued move → label guards and the exact native pending identity through reload', async () => {
    const env = await environment();
    const session = await env.mount();
    const source = withClipAt(session.source, 5);
    env.queue(env.document(source));
    await session.handoff.capture(source);
    const labelSource = withTrackLabel(source, 'Queued label');
    env.queue(env.document(labelSource));
    await session.handoff.capture(labelSource);
    env.lose();
    await expect(session.handoff.flush()).rejects.toThrow('unacknowledged');
    const original = env.send.mock.calls[0];
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    const labelPayload = structuredClone(stored.intents[1].payload);
    expect(labelPayload).toMatchObject({ documentIntent: { changes: [{ op: 'set', ref: 'parent', path: ['tracks', 'id:V1', 'label'],
      before: { state: 'absent' }, value: 'Queued label' }] } });
    expect((labelPayload.after as unknown as CanonicalDocument).parent_revision.payload.config.tracks)
      .toEqual(expect.arrayContaining([expect.objectContaining({ label: 'Queued label' })]));
    expect(stored.pending?.request.key).toBe(original[1]);
    expect(JSON.parse(stored.pending!.request.body)).toEqual(original[0]);
    await session.session.dispose();
    const reopened = await env.mount(env.latest());
    expect(reopened.session.getState().status).toBe('recovery');
    expect(env.send).toHaveBeenCalledTimes(1);
    await reopened.session.recover(stored.ownerId);
    expect(env.send.mock.calls[1]).toEqual(original);
    expect(env.send.mock.calls[2][0]).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ op: 'doc.patch', args: { changes: (labelPayload.documentIntent as { changes: unknown }).changes } }] });
    expect(env.send.mock.calls[2][1]).not.toBe(original[1]);
    const final = reopened.session.getDocument() as unknown as CanonicalDocument;
    expect((parent(final).config as ParentPayload).clips).toEqual(expect.arrayContaining([expect.objectContaining({ at: 5 })]));
    expect((parent(final).config as ParentPayload).tracks).toEqual(expect.arrayContaining([expect.objectContaining({ label: 'Queued label' })]));
    await reopened.session.dispose();
  });

  it('keeps typing capture original when A is acknowledged before label completion', async () => {
    const env = await environment();
    const session = await env.mount();
    const moveSource = withClipAt(session.source, 5);
    env.queue(env.document(moveSource));
    await session.handoff.capture(moveSource);
    const captured = structuredClone(moveSource);
    env.lose();
    await expect(session.handoff.flush()).rejects.toThrow('unacknowledged');
    const basis = structuredClone(captured);
    await session.handoff.flush();
    const typed = withTrackLabel(env.sourceFor(env.latest()), 'Typed over A');
    env.queue(env.document(typed, env.latest().canonicalDocument));
    await session.handoff.capture(typed);
    await session.handoff.flush();
    expect(captured).toEqual(basis);
    expect(env.send.mock.calls[2][0]).toMatchObject({ base_publication_id: 'p1', commands: [{ op: 'doc.patch',
      args: { changes: [{ path: ['tracks', 'id:V1', 'label'], before: { state: 'absent' } }] } }] });
    expect((parent(session.session.getDocument() as unknown as CanonicalDocument).config as ParentPayload).clips)
      .toEqual(expect.arrayContaining([expect.objectContaining({ at: 5 })]));
    await session.session.dispose();
  });

  it('refuses an observed external label mutation during typing without replacing the input', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = structuredClone(session.source);
    const observed = env.remote((raw) => { (parent(raw).config as ParentPayload).tracks = [{ id: 'V1', kind: 'visual', label: 'Someone else' }];
      parent(raw).tracks = structuredClone((parent(raw).config as ParentPayload).tracks); });
    const args = withTrackLabel(observed.source, 'My typing');
    await expect(session.handoff.capture(args)).rejects.toThrow('original verified authoring head');
    expect(track(args).label).toBe('My typing');
    expect(track(captured)).not.toHaveProperty('label');
    expect(env.send).not.toHaveBeenCalled();
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    await session.session.dispose();
  });

  it('surfaces an unobserved external label change as a real guarded conflict', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = structuredClone(session.source);
    const typed = withTrackLabel(captured, 'My typing');
    env.queue(env.document(typed));
    await session.handoff.capture(typed);
    env.conflict();
    await expect(session.handoff.flush()).rejects.toThrow();
    expect(session.session.getState().status).toBe('conflict');
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ documentIntent: { changes: [{ path: ['tracks', 'id:V1', 'label'], value: 'My typing' }] } });
    expect((stored.intents[0].payload.after as unknown as CanonicalDocument).parent_revision.payload.config.tracks)
      .toEqual(expect.arrayContaining([expect.objectContaining({ label: 'My typing' })]));
    await session.session.dispose();
  });

});
