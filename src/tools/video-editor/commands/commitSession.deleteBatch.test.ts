// @vitest-environment node
import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import { ApiError } from '@/integrations/runtime/generated.ts';
import type { CanonicalDocument, CommitRequest, EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { executeClipDeleteBatch, type ClipDeleteBatchMember } from './clipDeleteBatchCapture.ts';
import { captureClipDeleteBatchEdit, projectClipDeleteBatchPreview, submitClipDeleteBatchEdit } from './clipDeleteBatchGesture.ts';
import { captureClipDeleteEdit, projectClipDeletePreview, submitClipDeleteEdit } from './clipDeleteGesture.ts';
import { copy, type AuthoredBundle } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_clip_delete_batch.json';

const golden = fixture as unknown as { input: CanonicalDocument; cases: Array<{
  members: ClipDeleteBatchMember[]; commands: EditCommand[]; inverse_output: CanonicalDocument;
}> };
const scope = { projectId: 'project-1', timelineId: 'film', realmId: 'realm-1', actorId: 'actor-1' };
const initialHead = { revisionId: 'parent-1', publicationId: 'pub-0' };

// Fake unit acceptance with local replay, never a claim about accepted Runtime/UI projection.
async function setup(mutate?: (document: CanonicalDocument) => void) {
  const document = copy(golden.input);
  mutate?.(document);
  const initial: TimelineCommandBasis = { head: initialHead, canonicalDocument: document };
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: createFakeIndexedDB(), exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  let serverBundle = await authoringBundleFromDocument(document) as AuthoredBundle;
  let latest = initial;
  let loseNext = false;
  let unavailableNext = false;
  let refuseInverse = false;
  let publication = 0;
  const requests: Array<{ request: CommitRequest; key: string; body: string }> = [];
  const accepted = new Map<string, TimelineCommitResult>();
  const display = (basis: TimelineCommandBasis) => {
    const parent = basis.canonicalDocument.parent_revision.payload;
    const config = { ...parent.config as object, clips: parent.clips } as TimelineData['config'];
    return assembleTimelineData({ config, configVersion: 1, registry: parent.registry as TimelineData['registry'], assetMap: {},
      resolvedConfig: { ...config, tracks: config.tracks!, registry: {} },
      head: { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: basis.head.revisionId,
        headPublicationId: basis.head.publicationId } });
  };
  let current = display(initial);
  const previews: TimelineData[] = [];
  const nativePreview = (patch: Parameters<typeof projectClipDeletePreview>[0], data: TimelineData) =>
    projectClipDeleteBatchPreview(patch, data) ?? projectClipDeletePreview(patch, data)!;
  const send = async (request: CommitRequest, key: string): Promise<TimelineCommitResult> => {
    requests.push({ request: copy(request), key, body: JSON.stringify(request) });
    if (unavailableNext) { unavailableNext = false; throw new Error('transport still unavailable'); }
    const prior = accepted.get(key);
    if (prior) {
      expect(requests.at(-1)).toEqual(requests.find((entry) => entry.key === key));
      return prior;
    }
    let next: CanonicalDocument;
    if (request.commands[0].op === 'timeline.inverse') {
      if (refuseInverse) throw new ApiError(409, 'conflict', 'intervening_write', '', { status: 'conflict' });
      // Exact authored inverse exported by the native Agent over both indexed delete records.
      expect(request.commands).toHaveLength(1);
      expect(request.commands[0].args).toEqual({ publications: ['pub-1'] });
      next = copy(golden.cases[0].inverse_output);
    } else {
      try {
        const result = executeClipDeleteBatch(serverBundle, request.commands);
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
    latest = { head: result.accepted, canonicalDocument: next, graph: {} };
    accepted.set(key, result);
    if (loseNext) { loseNext = false; throw new Error('lost acknowledgement'); }
    return result;
  };
  const mount = (basis = initial) => createTimelineCommandSession({ scope, initial: basis, outboxes, send, changed: () => {},
    preview: (patch) => { const next = nativePreview(patch, current); current = next; previews.push(next); },
    project: async (basis, patches) => {
      let next = display(basis);
      for (const patch of patches) next = nativePreview(patch, next);
      current = next;
    },
  });
  return { mount, outboxes, current: () => current, latest: () => latest, previews, requests, server: () => serverBundle,
    accepted, loseAck: () => { loseNext = true; }, refuseInverse: () => { refuseInverse = true; },
    unavailable: () => { unavailableNext = true; },
    changeServer: (change: (bundle: AuthoredBundle) => void) => change(serverBundle) };
}

const capture = (session: Awaited<ReturnType<typeof createTimelineCommandSession>>, current: TimelineData) =>
  captureClipDeleteBatchEdit(session.clipDeleteBatchPort, current, golden.cases[0].members);

describe('one native parent multi-delete through the durable session', () => {
  it('installs once, persists one intent, retries exact bytes/key after reload, and undoes one publication', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    const edit = capture(session, env.current());
    const original = copy(edit.basis);
    submitClipDeleteBatchEdit(edit);
    expect(env.previews).toHaveLength(1);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-c']);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toEqual(golden.cases[0].commands);
    expect(stored.pending!.request.body).toBe(env.requests[0].body);
    expect(stored.pending!.request.key).toBe(env.requests[0].key);
    expect(env.requests[0].request.commands).toEqual(golden.cases[0].commands);
    expect(edit.basis).toEqual(original);
    await session.dispose();

    const reopened = await env.mount(env.latest());
    expect(reopened.getState().status).toBe('recovery');
    expect(env.requests).toHaveLength(1);
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
    expect(env.requests[2].request.commands).toMatchObject([{ op: 'timeline.inverse', args: { publications: ['pub-1'] } }]);
    expect(env.current().config.clips).toEqual((golden.input.parent_revision.payload.config as Record<string, unknown>).clips);
    expect(reopened.getState().canUndo).toBe(false);
    await expect(reopened.undo()).rejects.toThrow('No accepted local publication');
    await reopened.dispose();
  });

  it('recovers the entire local preview when exact retry is still uncertain', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    submitClipDeleteBatchEdit(capture(session, env.current()));
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    await session.dispose();
    const reopened = await env.mount();
    env.unavailable();
    await reopened.recover(stored.ownerId);
    expect(reopened.getState().status).toBe('retry');
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-c']);
    expect(env.previews).toHaveLength(1);
    expect(env.requests).toHaveLength(2);
    expect(env.requests[1]).toEqual(env.requests[0]);
    const [retained] = await env.outboxes.list(scope);
    expect(retained.intents[0].payload).toEqual(stored.intents[0].payload);
    expect(retained.pending!.request).toEqual(stored.pending!.request);
    await reopened.retry();
    await reopened.flush();
    expect(env.requests[2]).toEqual(env.requests[0]);
    await reopened.dispose();
  });

  it('keeps one batch suffix and its original shrinking selections through the earlier intent ACK', async () => {
    const env = await setup();
    const session = await env.mount();
    env.loseAck();
    submitClipDeleteEdit(captureClipDeleteEdit(session.clipDeletePort, env.current(), 'clip-c', 'parent'));
    const edit = capture(session, env.current());
    const original = copy(edit.basis.commands);
    submitClipDeleteBatchEdit(edit);
    expect(env.current().config.clips).toEqual([]);
    expect(env.previews).toHaveLength(2);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(2);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    expect((stored.intents[1].payload as unknown as { commands: EditCommand[] }).commands).toEqual(original);
    await session.dispose();
    const reopened = await env.mount(env.latest());
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(env.requests).toHaveLength(3);
    expect(env.requests[1]).toEqual(env.requests[0]);
    expect(env.requests[2].request).toMatchObject({ base_revision_id: 'parent-2', base_publication_id: 'pub-1', commands: original });
    expect((original as EditCommand[])[0].selections!.find((selection) => selection.key === 'collection.clips')!.order)
      .toEqual(['parent/clip:clip-a', 'parent/clip:clip-b']);
    expect(env.accepted.size).toBe(2);
    expect(env.current().config.clips).toEqual([]);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    await reopened.dispose();
  });

  it('preserves an executable earlier local deletion if the second batch member is unsupported', async () => {
    const env = await setup((document) => {
      const parent = document.parent_revision.payload;
      (parent.clips as Array<Record<string, unknown>>)[0].children = [];
      (parent.config as Record<string, unknown>).clips = copy(parent.clips);
    });
    const session = await env.mount();
    env.loseAck();
    submitClipDeleteEdit(captureClipDeleteEdit(session.clipDeletePort, env.current(), 'clip-c', 'parent'));
    const before = copy(env.current());
    expect(() => capture(session, env.current())).toThrow('nested clip ownership');
    expect(env.current()).toEqual(before);
    expect(env.previews).toHaveLength(1);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toHaveLength(1);
    expect(env.requests).toHaveLength(1);
    await session.dispose();
  });

  it.each(['order', 'dependency', 'second-row'])('retains one entire refused intent and local draft after remote %s', async (change) => {
    const env = await setup();
    const session = await env.mount();
    const edit = capture(session, env.current());
    env.changeServer((bundle) => {
      const rows = bundle.parent.clips as Array<Record<string, unknown>>;
      if (change === 'order') rows.reverse();
      if (change === 'dependency') rows[2].app = { astrid: { on: 'clip-a' } };
      if (change === 'second-row') rows[0].opaque = { accepted: true };
      (bundle.parent.config as Record<string, unknown>).clips = copy(rows);
    });
    const serverBefore = copy(env.server());
    submitClipDeleteBatchEdit(edit);
    const draft = copy(env.current());
    await vi.waitFor(() => expect(session.getState().status).toBe('conflict'));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect(stored.pending!.outcome!.kind).toBe('rejected');
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toEqual(edit.basis.commands);
    expect(env.server()).toEqual(serverBefore);
    expect(env.current()).toEqual(draft);
    expect(env.accepted.size).toBe(0);
    await session.retry();
    expect(env.requests).toHaveLength(1);
    await session.dispose();
  });

  it('accepts the original sequence over disjoint work while preserving the survivor bytes', async () => {
    const env = await setup();
    const session = await env.mount();
    const edit = capture(session, env.current());
    env.changeServer((bundle) => {
      (bundle.parent.clips as Array<Record<string, unknown>>)[2].opaque = { accepted: [null, false] };
      (bundle.parent.config as Record<string, unknown>).clips = copy(bundle.parent.clips);
    });
    submitClipDeleteBatchEdit(edit);
    await session.flush();
    expect(env.requests[0].request.commands).toEqual(edit.basis.commands);
    expect(env.current().config.clips).toMatchObject([{ id: 'clip-c', opaque: { accepted: [null, false] } }]);
    expect(env.server().parent.registry).toEqual(golden.input.parent_revision.payload.registry);
    await session.dispose();
  });

  it.each(['order', 'dependency', 'second-row'])('refuses finish after an observed %s change without touching state or outbox', async (change) => {
    const env = await setup();
    const session = await env.mount();
    const edit = capture(session, env.current());
    const original = copy(edit.basis);
    const remote = copy(golden.input);
    const parent = remote.parent_revision.payload;
    const rows = parent.clips as Array<Record<string, unknown>>;
    if (change === 'order') rows.reverse();
    if (change === 'dependency') rows[2].app = { astrid: { on: 'clip-a' } };
    if (change === 'second-row') rows[0].opaque = { accepted: null };
    (parent.config as Record<string, unknown>).clips = copy(rows);
    remote.parent_revision = { revision_id: 'remote-r', content_digest: fixtureDigest(parent), payload: parent };
    session.observe({ head: { revisionId: 'remote-r', publicationId: 'remote-p' }, canonicalDocument: remote });
    await vi.waitFor(() => expect(env.current().head!.headRevisionId).toBe('remote-r'));
    const before = copy(env.current());
    const outbox = await env.outboxes.list(scope);
    expect(() => submitClipDeleteBatchEdit(edit)).toThrow();
    expect(env.current()).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(outbox);
    expect(edit.basis).toEqual(original);
    expect(env.requests).toEqual([]);
    expect(env.previews).toEqual([]);
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });

  it.each([null, false, { occurrenceId: 'opaque', clipRef: 'occurrence:opaque/clip:clip-a' }])(
    'uses raw parent ownership for each target with opaque canonical metadata %j', async (canonical) => {
      const env = await setup((document) => {
        const parent = document.parent_revision.payload;
        (parent.clips as Array<Record<string, unknown>>)[0].app = { canonical, keep: null };
        (parent.config as Record<string, unknown>).clips = copy(parent.clips);
      });
      const session = await env.mount();
      const edit = capture(session, env.current());
      const commands = session.clipDeleteBatchPort.finish(edit.basis).commands;
      expect(commands.map((command) => command.select)).toEqual(['parent/clip:clip-b', 'parent/clip:clip-a']);
      expect(commands[1].expect!['parent/clip:clip-a::']).toMatchObject({ state: 'present', value: { app: { canonical, keep: null } } });
      submitClipDeleteBatchEdit(edit);
      await session.flush();
      expect(env.requests).toHaveLength(1);
      await session.dispose();
    });

  it('keeps an inverse refusal visible and leaves the accepted deletion unchanged', async () => {
    const env = await setup();
    const session = await env.mount();
    submitClipDeleteBatchEdit(capture(session, env.current()));
    await session.flush();
    const before = copy(env.server());
    env.refuseInverse();
    await session.undo();
    expect(session.getState().status).toBe('conflict');
    expect(env.server()).toEqual(before);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-c']);
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(1);
    await session.dispose();
  });

  it('fences display collisions, changed previews, reordered commands, stale finish and duplicate submit', async () => {
    const env = await setup();
    const session = await env.mount();
    const current = env.current();
    const collision = copy(current);
    collision.resolvedConfig.clips.push(copy(collision.resolvedConfig.clips[0]));
    expect(() => capture(session, collision)).toThrow();
    expect(() => capture(session, { ...current, head: { ...current.head!, headPublicationId: 'wrong' } })).toThrow('raw authoring basis');
    const edit = capture(session, current);
    const prepared = session.clipDeleteBatchPort.finish(edit.basis);
    const forged = copy(prepared);
    forged.commands.reverse();
    expect(() => session.clipDeleteBatchPort.submit(forged)).toThrow('not captured');
    forged.commands.reverse();
    forged.preview.operations.reverse();
    expect(() => session.clipDeleteBatchPort.submit(forged)).toThrow('exact native preview');
    expect(env.current()).toBe(current);
    expect(env.previews).toEqual([]);
    session.clipDeleteBatchPort.submit(prepared);
    expect(() => session.clipDeleteBatchPort.finish(edit.basis)).toThrow('Timeline changed');
    expect(() => session.clipDeleteBatchPort.submit(prepared)).toThrow();
    await session.flush();
    expect(env.requests).toHaveLength(1);
    await session.dispose();
  });
});
