// @vitest-environment node
import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import { ApiError } from '@/integrations/runtime/generated.ts';
import type { CanonicalDocument, CommitRequest, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { executeClipSplitBatch } from './clipSplitBatchCapture.ts';
import { captureClipSplitBatchEdit, projectClipSplitBatchPreview, submitClipSplitBatchEdit } from './clipSplitBatchGesture.ts';
import { captureClipSplitEdit, projectClipSplitPreview, submitClipSplitEdit } from './clipSplitGesture.ts';
import { copy, type AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_clip_split_batch.json';

const golden = fixture as unknown as { input: CanonicalDocument; inverse_output: CanonicalDocument };
const scope = { projectId: 'project-1', timelineId: 'film', realmId: 'realm-1', actorId: 'actor-1' };
const initialHead = { revisionId: 'parent-1', publicationId: 'pub-0' };
const reserve = (_used: string[], clipId: string) => `right:${clipId.slice(-1)}`;

async function setup(mutate?: (document: CanonicalDocument) => void) {
  const document = copy(golden.input);
  mutate?.(document);
  const initial: TimelineCommandBasis = { head: initialHead, canonicalDocument: document };
  const factory = createFakeIndexedDB();
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  let serverBundle = await authoringBundleFromDocument(document) as AuthoredBundle;
  let loseNext = false;
  let publication = 0;
  const requests: Array<{ request: CommitRequest; key: string; body: string }> = [];
  const accepted = new Map<string, TimelineCommitResult>();
  const display = (basis: TimelineCommandBasis) => buildTimelineData(
    basis.canonicalDocument.parent_revision.payload.config as never,
    basis.canonicalDocument.parent_revision.payload.registry as never, undefined, 1, undefined,
    { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: basis.head.revisionId,
      headPublicationId: basis.head.publicationId });
  let current = await display(initial);
  const previews: TimelineData[] = [];
  const nativePreview = (patch: Parameters<typeof projectClipSplitPreview>[0], data: TimelineData) =>
    projectClipSplitBatchPreview(patch, data) ?? projectClipSplitPreview(patch, data)!;
  const send = async (request: CommitRequest, key: string): Promise<TimelineCommitResult> => {
    requests.push({ request: copy(request), key, body: JSON.stringify(request) });
    const prior = accepted.get(key);
    if (prior) {
      expect(requests.at(-1)).toEqual(requests.find((entry) => entry.key === key));
      return prior;
    }
    let next: CanonicalDocument;
    if (request.commands[0].op === 'timeline.inverse') {
      // Authored result exported from the real native inverse over both accepted records.
      expect(request.commands).toHaveLength(1);
      expect(request.commands[0].args).toEqual({ publications: ['pub-1'] });
      next = copy(golden.inverse_output);
    } else {
      try {
        const result = executeClipSplitBatch(serverBundle, request.commands);
        next = copy(document);
        const payload = { ...result.bundle.parent, occurrences: copy(document.parent_revision.payload.occurrences) };
        next.parent_revision = { revision_id: 'pending', content_digest: fixtureDigest(payload), payload };
      } catch (error) {
        throw new ApiError(409, 'conflict', String(error), '', { status: 'conflict' });
      }
    }
    const nextRevision = `parent-${publication + 2}`;
    const nextPublication = `pub-${++publication}`;
    next.parent_revision.revision_id = nextRevision;
    const response = acceptedCommit({ revision_id: nextRevision, publication_id: nextPublication },
      { revision_id: request.base_revision_id, publication_id: request.base_publication_id },
      { projectId: scope.projectId, timelineId: scope.timelineId, commands: request.commands });
    Object.assign(response.data, { canonical_document: next, accepted_revision_id: nextRevision,
      document_digest: fixtureDigest(next), commands: request.commands });
    response.receipt.result = response.data;
    const result: TimelineCommitResult = { response, accepted: { revisionId: nextRevision, publicationId: nextPublication },
      canonicalDocument: next, graph: {}, receipt: response.receipt };
    serverBundle = await authoringBundleFromDocument(next) as AuthoredBundle;
    accepted.set(key, result);
    if (loseNext) { loseNext = false; throw new Error('lost acknowledgement'); }
    return result;
  };
  const mount = () => createTimelineCommandSession({ scope, initial, outboxes, send, changed: () => {},
    preview: (patch) => { const next = nativePreview(patch, current); current = next; previews.push(next); },
    project: async (basis, patches) => {
      let next = await display(basis);
      for (const patch of patches) next = nativePreview(patch, next);
      current = next;
    },
  });
  return { mount, outboxes, current: () => current, previews, requests, server: () => serverBundle,
    accepted, loseAck: () => { loseNext = true; }, changeServer: (change: (bundle: AuthoredBundle) => void) => change(serverBundle) };
}

function capture(session: Awaited<ReturnType<typeof createTimelineCommandSession>>, current: TimelineData) {
  return captureClipSplitBatchEdit(session.clipSplitBatchPort, current, ['clip-b', 'clip-a'], 3, reserve)!;
}

describe('one native split batch through the durable session', () => {
  it('installs one preview, persists one intent, retries exact bytes/key after reload, and undoes one publication', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    const edit = capture(session, env.current());
    const original = copy(edit.basis);
    submitClipSplitBatchEdit(edit);
    expect(env.previews).toHaveLength(1);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-a', 'right:a', 'clip-b', 'right:b']);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.pending!.request.body).toBe(env.requests[0].body);
    expect(stored.pending!.request.key).toBe(env.requests[0].key);
    expect(env.requests[0].request.commands.map((command) => command.select)).toEqual(['parent/clip:clip-b', 'parent/clip:clip-a']);
    expect(edit.basis).toEqual(original);
    await session.dispose();

    const reopened = await env.mount();
    expect(reopened.getState().status).toBe('recovery');
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.requests).toHaveLength(2);
    expect(env.requests[1]).toEqual(env.requests[0]);
    expect(env.accepted.size).toBe(1);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(reopened.getState().canUndo).toBe(true);
    await reopened.undo();
    await reopened.flush();
    expect(env.requests).toHaveLength(3);
    expect(env.requests[2].request.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['pub-1'] } });
    expect(env.current().config.clips).toEqual((golden.input.parent_revision.payload.config as Record<string, unknown>).clips);
    expect(reopened.getState().canUndo).toBe(false);
    await expect(reopened.undo()).rejects.toThrow('No accepted local publication');
    await reopened.dispose();
  });

  it('refuses the second unsupported member without a preview or durable intent and keeps the raw basis', async () => {
    const env = await setup((document) => {
      const parent = document.parent_revision.payload;
      (parent.clips as Array<Record<string, unknown>>)[0].time_map = {};
      (parent.config as Record<string, unknown>).clips = copy(parent.clips);
    });
    const session = await env.mount();
    const before = copy(env.current());
    expect(() => capture(session, env.current())).toThrow('time_map');
    expect(env.current()).toEqual(before);
    expect(env.previews).toEqual([]);
    await session.flush();
    expect(env.requests).toEqual([]);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    const single = captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-b', 3, 'single-right');
    expect((single.basis.command as unknown as EditCommand).selections![0].order).toEqual(['parent/clip:clip-a', 'parent/clip:clip-b']);
    submitClipSplitEdit(single);
    await session.flush();
    expect(env.requests).toHaveLength(1);
    await session.dispose();
  });

  it.each(['order', 'membership'] as const)('retains the whole draft after a server %s conflict', async (change) => {
    const env = await setup();
    const session = await env.mount();
    const edit = capture(session, env.current());
    env.changeServer((bundle) => {
      const rows = bundle.parent.clips as Array<Record<string, unknown>>;
      if (change === 'order') rows.reverse();
      else rows.push({ ...copy(rows[0]), id: 'inserted' });
      (bundle.parent.config as Record<string, unknown>).clips = copy(rows);
    });
    const serverBefore = copy(env.server());
    submitClipSplitBatchEdit(edit);
    await vi.waitFor(() => expect(session.getState().status).toBe('conflict'));
    expect(env.server()).toEqual(serverBefore);
    expect(env.accepted.size).toBe(0);
    expect(env.current().config.clips).toHaveLength(4);
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.pending!.outcome!.kind).toBe('rejected');
    expect(env.requests[0].request.commands).toEqual(edit.basis.commands);
    await session.dispose();
  });

  it('keeps original outside-playhead members untouched while splitting the eligible subset', async () => {
    const env = await setup((document) => {
      const parent = document.parent_revision.payload;
      const outside = (parent.clips as Array<Record<string, unknown>>)[1];
      outside.at = 5;
      outside.time_map = {};
      (parent.config as Record<string, unknown>).clips = copy(parent.clips);
    });
    const session = await env.mount();
    const outside = copy(env.current().config.clips[1]);
    const edit = capture(session, env.current());
    expect(edit.clipIds).toEqual(['clip-b', 'clip-a']);
    expect(edit.members).toEqual([{ clipId: 'clip-a', rightId: 'right:a' }]);
    submitClipSplitBatchEdit(edit);
    expect(env.previews).toHaveLength(1);
    expect(env.current().config.clips[2]).toEqual(outside);
    await session.flush();
    expect(env.requests[0].request.commands).toHaveLength(1);
    expect(env.current().config.clips[2]).toEqual(outside);
    await session.dispose();
  });

  it('rejects projected/display collisions for both single and batch capture', async () => {
    const env = await setup();
    const session = await env.mount();
    const collision = copy(env.current());
    collision.resolvedConfig.clips.push(copy(collision.resolvedConfig.clips[0]));
    expect(() => capture(session, collision)).toThrow('literal parent');
    expect(() => captureClipSplitEdit(session.clipSplitPort, collision, 'clip-a', 3, 'right')).toThrow('unambiguous');
    expect(env.previews).toEqual([]);
    await session.flush();
    expect(env.requests).toEqual([]);
    await session.dispose();
  });

  it('fences stale finish and forged submissions while preserving raw parent opaque canonical data', async () => {
    const env = await setup((document) => {
      const parent = document.parent_revision.payload;
      const row = (parent.clips as Array<Record<string, unknown>>)[0];
      (row.app as Record<string, unknown>).canonical = { occurrenceId: 'opaque', clipRef: 'foreign/opaque' };
      (parent.config as Record<string, unknown>).clips = copy(parent.clips);
    });
    const session = await env.mount();
    const single = captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-a', 3, 'single-right');
    expect(session.clipSplitPort.finish(single.basis).command.select).toBe('parent/clip:clip-a');
    const edit = capture(session, env.current());
    const prepared = session.clipSplitBatchPort.finish(edit.basis);
    const forged = copy(prepared);
    forged.commands.reverse();
    expect(() => session.clipSplitBatchPort.submit(forged)).toThrow('not captured');
    forged.commands.reverse();
    forged.preview = { ...forged.preview, operations: [...forged.preview.operations].reverse() };
    expect(() => session.clipSplitBatchPort.submit(forged)).toThrow('exact native preview');
    session.clipSplitBatchPort.submit(prepared);
    expect(() => session.clipSplitBatchPort.finish(edit.basis)).toThrow('Timeline changed');
    expect(env.current().config.clips[1].app).toMatchObject({ canonical: { occurrenceId: 'opaque', clipRef: 'foreign/opaque' } });
    await session.flush();
    await session.dispose();
  });
});
