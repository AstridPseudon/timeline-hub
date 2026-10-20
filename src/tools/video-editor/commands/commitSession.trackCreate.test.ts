import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { CanonicalDocument, CommitRequest } from '@/integrations/runtime/generated.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { ClipMoveError, copy } from './clipMovePrimitives.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { executeTrackCreate } from './trackCreateCapture.ts';
import { captureTrackCreateEdit, projectTrackCreatePreview, submitTrackCreateEdit } from './trackCreateGesture.ts';
import { document, scope } from './__tests__/commitSessionEnvironment.ts';

const rows = [
  { id: 'A1', kind: 'audio', label: 'Audio', muted: null, opaque: { keep: [null, false] } },
  { id: 'V2', kind: 'visual', label: 'Second', unknown: { preserve: true } },
] as const;

type Call = { request: CommitRequest; key: string; body: string };

async function setup() {
  let serverDocument = document();
  let serverHead = { revisionId: 'r0', publicationId: 'p0' };
  let loseNext = false;
  const calls: Call[] = [];
  const accepted = new Map<string, { request: CommitRequest; result: TimelineCommitResult }>();
  const factory = createFakeIndexedDB();
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('outbox is already claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  const initial = (): TimelineCommandBasis => ({
    head: serverHead,
    canonicalDocument: copy(serverDocument),
    history: { items: [], next_cursor: null,
      head: { revision_id: serverHead.revisionId, publication_id: serverHead.publicationId } } as never,
  });
  const display = (basis: TimelineCommandBasis) => {
    const parent = basis.canonicalDocument.parent_revision.payload as Record<string, never>;
    const config = { ...(parent.config as TimelineConfig), clips: parent.clips };
    return buildTimelineData(config, parent.registry as AssetRegistry, undefined, 1, undefined, {
      projectId: scope.projectId, timelineId: scope.timelineId,
      headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId,
    });
  };
  let current = await display(initial());
  const send = async (request: CommitRequest, key: string): Promise<TimelineCommitResult> => {
    const body = JSON.stringify(request);
    calls.push({ request: copy(request), key, body });
    const prior = accepted.get(key);
    if (prior) {
      if (JSON.stringify(prior.request) !== body) {
        throw new Error('changed exact retry');
      }
      if (loseNext) { loseNext = false; throw new Error('lost acknowledgement'); }
      return prior.result;
    }
    let result;
    try {
      result = executeTrackCreate(await authoringBundleFromDocument(serverDocument), request.commands[0]);
    } catch (error) {
      if (error instanceof ClipMoveError) throw new Error(`conflict: ${error.message}`);
      throw error;
    }
    const nextRevision = `r${accepted.size + 1}`;
    const nextPublication = `p${accepted.size + 1}`;
    const payload = { ...result.bundle.parent, occurrences: copy(serverDocument.parent_revision.payload.occurrences) };
    const next: CanonicalDocument = { ...copy(serverDocument), parent_revision: {
      revision_id: nextRevision, content_digest: fixtureDigest(payload), payload,
    } };
    const response = acceptedCommit({ revision_id: nextRevision, publication_id: nextPublication },
      { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, { commands: request.commands });
    Object.assign(response.data, { previous_revision_id: serverHead.revisionId, previous_publication_id: serverHead.publicationId,
      accepted_revision_id: nextRevision, canonical_document: copy(next), document_digest: fixtureDigest(next) });
    response.receipt.result = response.data;
    response.receipt.idempotency_key = key;
    const acceptedResult: TimelineCommitResult = { response, accepted: { revisionId: nextRevision, publicationId: nextPublication },
      canonicalDocument: next, graph: {}, receipt: response.receipt };
    accepted.set(key, { request: copy(request), result: acceptedResult });
    serverDocument = next;
    serverHead = { revisionId: nextRevision, publicationId: nextPublication };
    if (loseNext) { loseNext = false; throw new Error('lost acknowledgement'); }
    return acceptedResult;
  };
  const mount = (basis = initial()) => createTimelineCommandSession({ initial: basis, scope, outboxes, send,
    preview: (patch) => { current = projectTrackCreatePreview(patch, current)!; },
    project: async (acceptedBasis, patches) => { current = await display(acceptedBasis); for (const patch of patches) current = projectTrackCreatePreview(patch, current)!; },
    changed: () => {},
  });
  return { mount, outboxes, initial, current: () => current, calls, loseAck: () => { loseNext = true; }, server: () => serverDocument };
}

describe('native parent track.create in the durable command session', () => {
  it('keeps full rows local, retries exact bytes after reload, and gives dependent commands fresh keys', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();

    submitTrackCreateEdit(captureTrackCreateEdit(session.trackCreatePort, env.current(), copy(rows[0])));
    submitTrackCreateEdit(captureTrackCreateEdit(session.trackCreatePort, env.current(), copy(rows[1])));
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));

    expect(env.current().config.tracks.at(-1)).toEqual(rows[1]);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.pending?.request.body).toBe(env.calls[0].body);
    expect(stored.pending?.request.key).toBe(env.calls[0].key);
    await session.dispose();

    const reopened = await env.mount(env.initial());
    expect(reopened.getState().status).toBe('recovery');
    await reopened.recover(stored.ownerId);
    await reopened.flush();

    expect(env.calls).toHaveLength(3);
    expect(env.calls[1]).toEqual(env.calls[0]);
    expect(env.calls[2].key).not.toBe(env.calls[0].key);
    expect(env.calls[2].request.base_publication_id).toBe('p1');
    expect(env.calls[2].request.commands[0].op).toBe('track.create');
    expect(env.server().parent_revision.payload.config).toMatchObject({ tracks: [
      { id: 'V1', kind: 'visual' }, rows[0], rows[1],
    ] });
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await reopened.dispose();
  });

  it('retains the original collection guard on a dependent command', async () => {
    const env = await setup();
    const session = await env.mount();
    const captured = captureTrackCreateEdit(session.trackCreatePort, env.current(), copy(rows[0]));
    const prepared = session.trackCreatePort.finish(captured.basis, { row: copy(rows[0]) });
    expect(prepared.command.selections?.[0]).toMatchObject({ owner: 'parent', order: ['parent/track:V1'] });
    expect(prepared.command.expect?.['parent/track:A1::']).toEqual({ state: 'absent' });
    session.trackCreatePort.submit(prepared);
    expect(() => session.trackCreatePort.finish(captured.basis, { row: copy(rows[0]) })).toThrow('Timeline changed');
    await session.dispose();
  });
});
