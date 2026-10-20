import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';
import type { CanonicalDocument, CommitRequest, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { copy } from './clipMovePrimitives.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { captureOccurrenceDuplicateEdit, submitOccurrenceDuplicateEdit } from './occurrenceDuplicateGesture.ts';
import fixture from './fixtures/recipe_m2_app_occurrence_duplicate.json';

const initialDocument = fixture.bundle.source_mapping._runtime_document as unknown as CanonicalDocument;
const acceptedDocument = fixture.after_document as unknown as CanonicalDocument;
const scope = { projectId: 'project-1', timelineId: 'film', realmId: 'realm-1', actorId: 'actor-1' };
const args = { occurrence_id: 'occ-copy', shot_id: 'shot-copy' };
const owner = 'occurrence:occ-0';
const initialHead = { revisionId: initialDocument.parent_revision.revision_id, publicationId: 'p0' };

// An in-memory transport consumes the Agent-produced closure. This does not exercise Runtime admission.
async function setup() {
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  const initial: TimelineCommandBasis = { head: initialHead, canonicalDocument: copy(initialDocument) };
  const display = (basis: TimelineCommandBasis) => {
    const parent = basis.canonicalDocument.parent_revision.payload;
    return buildTimelineData(parent.config as TimelineConfig, parent.registry as AssetRegistry, undefined, 1, undefined, {
      projectId: scope.projectId, timelineId: scope.timelineId,
      headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId,
    });
  };
  let current = await display(initial);
  const calls: { body: string; request: CommitRequest; key: string }[] = [];
  const previews = vi.fn();
  const projected: TimelineCommandBasis[] = [];
  let result: TimelineCommitResult | undefined;
  let lost = false;
  let failSuffix = false;
  const send = async (request: CommitRequest, key: string): Promise<TimelineCommitResult> => {
    calls.push({ body: JSON.stringify(request), request: copy(request), key });
    if (failSuffix && request.commands[0].args.occurrence_id !== args.occurrence_id) {
      throw new ApiError(409, 'conflict', 'intervening source publication', '', { status: 'conflict' });
    }
    if (!result) {
      expect(request.commands).toEqual([fixture.command]);
      const response = acceptedCommit({ revision_id: acceptedDocument.parent_revision.revision_id, publication_id: 'p1' },
        { revision_id: request.base_revision_id, publication_id: request.base_publication_id }, {
          projectId: scope.projectId, timelineId: scope.timelineId, commands: request.commands,
        });
      response.data.canonical_document = copy(acceptedDocument);
      response.data.document_digest = fixtureDigest(acceptedDocument);
      response.receipt.result = response.data;
      response.receipt.idempotency_key = key;
      result = { response, canonicalDocument: copy(acceptedDocument), graph: {}, receipt: response.receipt,
        accepted: { revisionId: acceptedDocument.parent_revision.revision_id, publicationId: 'p1' } };
    } else expect(calls.at(-1)).toEqual(calls[0]);
    if (lost) { lost = false; throw new Error('lost acknowledgement'); }
    return copy(result);
  };
  const mount = () => createTimelineCommandSession({ scope, initial, outboxes, send, changed: () => {}, preview: previews,
    project: async (basis, patches) => {
      expect(patches).toEqual([]);
      projected.push(copy(basis));
      current = await display(basis);
    },
  });
  return { mount, initial, outboxes, calls, previews, projected, current: () => current,
    loseAck: () => { lost = true; }, refuseSuffix: () => { failSuffix = true; } };
}

describe('staged duplicate through the existing command session', () => {
  it('persists reserved IDs and exact request bytes across lost ACK, restart, and retry', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    const captured = captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, env.current(), owner, args);
    submitOccurrenceDuplicateEdit(captured);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(env.previews).not.toHaveBeenCalled();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.pending?.request.body).toBe(env.calls[0].body);
    expect(stored.pending?.request.key).toBe(env.calls[0].key);
    expect(env.calls[0].request.commands).toEqual([fixture.command]);
    expect(env.calls[0].request).not.toHaveProperty('candidate');
    expect(env.calls[0].request).not.toHaveProperty('preview');
    await session.dispose();
    const reopened = await env.mount();
    expect(reopened.getState().status).toBe('recovery');
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.calls).toHaveLength(2);
    expect(env.calls[1]).toEqual(env.calls[0]);
    expect(env.projected.at(-1)!.canonicalDocument).toEqual(acceptedDocument);
    const raw = env.projected.at(-1)!.canonicalDocument.parent_revision.payload.occurrences as Record<string, unknown>[];
    expect(raw.at(-1)!.stable_deep_link).toBe(fixture.after_document.parent_revision.payload.occurrences.at(-1)!.stable_deep_link);
    expect(raw.at(-1)!.output_records).toEqual(raw[0].output_records);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await reopened.dispose();
  });

  it('keeps a dependent duplicate on its original guards while only its submission base advances', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    env.refuseSuffix();
    submitOccurrenceDuplicateEdit(captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, env.current(), owner, args));
    const suffix = captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, env.current(), owner,
      { occurrence_id: 'copy-2', shot_id: 'shot-2' });
    const prepared = session.occurrenceDuplicatePort.finish(suffix.basis);
    session.occurrenceDuplicatePort.submit(prepared);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const before = (await env.outboxes.list(scope))[0];
    expect(before.intents).toHaveLength(2);
    expect(before.intents[1].basis).toEqual({ after: before.intents[0].id });
    await session.retry();
    expect(session.getState().status).toBe('conflict');
    expect(env.calls).toHaveLength(3);
    expect(env.calls[1]).toEqual(env.calls[0]);
    expect(env.calls[2].key).not.toBe(env.calls[0].key);
    expect(env.calls[2].request.base_publication_id).toBe('p1');
    expect(env.calls[2].request.commands).toEqual([prepared.command]);
    expect(env.calls[2].request.commands[0].reads).toEqual(fixture.command.reads.map((read) =>
      read.ref === 'shot:shot-copy' ? { ...read, ref: 'shot:shot-2' }
        : read.ref === 'occurrence:occ-copy' ? { ...read, ref: 'occurrence:copy-2' } : read));
    const after = (await env.outboxes.list(scope))[0];
    expect(after.intents).toHaveLength(1);
    expect(after.pending?.request.body).toBe(env.calls[2].body);
    expect((after.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toEqual([prepared.command]);
    await session.dispose();
  });

  it('refuses changed project, timeline, revision, publication, owner, and stale reservations before sending', async () => {
    const env = await setup();
    const session = await env.mount();
    for (const [key, value] of [['projectId', 'other'], ['timelineId', 'other'], ['headRevisionId', 'other'], ['headPublicationId', 'other']]) {
      const current = copy(env.current());
      Object.assign(current.head!, { [key]: value });
      expect(() => captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, current, owner, args)).toThrow('basis');
    }
    expect(() => captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, env.current(), 'occurrence:missing', args)).toThrow();
    const captured = captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, env.current(), owner, args);
    const prepared = session.occurrenceDuplicatePort.finish(captured.basis);
    expect(() => session.occurrenceDuplicatePort.submit({ command: { ...prepared.command, args: { ...args, shot_id: 'forged' } } })).toThrow('captured');
    expect(env.calls).toEqual([]);
    session.occurrenceDuplicatePort.submit(prepared);
    expect(() => session.occurrenceDuplicatePort.finish(captured.basis)).toThrow('changed');
    expect(() => session.occurrenceDuplicatePort.submit(prepared)).toThrow('captured');
    await session.flush();
    expect(() => captureOccurrenceDuplicateEdit(session.occurrenceDuplicatePort, env.current(), owner, args)).toThrow('occupied');
    await session.dispose();
  });

  it('refuses a foreign session command without creating another queue', async () => {
    const env = await setup();
    const session = await env.mount();
    expect(() => session.occurrenceDuplicatePort.submit({ command: fixture.command as EditCommand })).toThrow('captured');
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(env.calls).toEqual([]);
    await session.dispose();
  });
});
