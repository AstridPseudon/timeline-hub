// @vitest-environment node
import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import type { CommitRequest } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelineCommitResult } from '../data/DataProvider.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import type { TimelineCommandBasis } from '../data/DataProvider.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { executeClipSplit } from './clipSplitCapture.ts';
import { executeClipMove } from './clipMoveCapture.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { captureClipSplitEdit, submitClipSplitEdit } from './clipSplitGesture.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import { projectClipSplitPreview } from './clipSplitGesture.ts';
import fixture from './fixtures/recipe_m2_clip_split.json';

const golden = fixture as unknown as { input: TimelineCommandBasis['canonicalDocument'] };
const scope = { projectId: 'project-1', timelineId: 'film', realmId: 'realm-1', actorId: 'actor-1' };
const initialHead = { revisionId: 'parent-1', publicationId: 'pub-0' };

function documentFor(bundle: AuthoredBundle, revisionId: string) {
  const document = structuredClone(golden.input);
  const payload = { ...bundle.parent, occurrences: [] };
  document.parent_revision = { revision_id: revisionId, content_digest: fixtureDigest(payload), payload };
  return document;
}

async function harness(options: { lost?: boolean; reject?: boolean } = {}) {
  const initialDocument = structuredClone(golden.input);
  const initial: TimelineCommandBasis = { head: initialHead, canonicalDocument: initialDocument };
  const factory = createFakeIndexedDB();
  const held = new Set<string>();
  const outboxes = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (key, work) => {
    if (held.has(key)) throw new Error('claimed');
    held.add(key);
    try { return await work(); } finally { held.delete(key); }
  } });
  let serverBundle = await authoringBundleFromDocument(initialDocument) as AuthoredBundle;
  let current = await buildTimelineData(initialDocument.parent_revision.payload.config as never,
    initialDocument.parent_revision.payload.registry as never, undefined, 1, undefined,
    { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: initialHead.revisionId,
      headPublicationId: initialHead.publicationId });
  let publication = 0;
  let loseNext = options.lost === true;
  const requests: Array<{ request: CommitRequest; key: string }> = [];
  const accepted = new Map<string, TimelineCommitResult>();
  const previous = new Map<string, AuthoredBundle>();
  const previews: TimelineData[] = [];
  const states: Array<string> = [];
  const send = async (request: CommitRequest, key: string): Promise<TimelineCommitResult> => {
    requests.push({ request: structuredClone(request), key });
    const prior = accepted.get(key);
    if (prior) {
      if (loseNext) throw new Error('lost acknowledgement');
      return prior;
    }
    if (options.reject) throw new ApiError(409, 'conflict', 'split refused', '', { status: 'conflict' });
    const command = request.commands[0];
    const result = command.op === 'timeline.inverse'
      ? { bundle: previous.get((command.args.publications as string[])[0])! }
      : command.op === 'clip.move' ? executeClipMove(serverBundle, command) : executeClipSplit(serverBundle, command);
    const nextPublication = `pub-${++publication}`;
    const nextRevision = `parent-${publication + 1}`;
    const canonicalDocument = documentFor(result.bundle, nextRevision);
    const mutation = acceptedCommit({ revision_id: nextRevision, publication_id: nextPublication },
      { revision_id: request.base_revision_id, publication_id: request.base_publication_id },
      { projectId: scope.projectId, timelineId: scope.timelineId, commands: request.commands });
    mutation.data.canonical_document = canonicalDocument;
    mutation.data.accepted_revision_id = nextRevision;
    mutation.data.document_digest = fixtureDigest(canonicalDocument);
    mutation.data.commands = request.commands;
    mutation.receipt.result = mutation.data;
    const acceptedResult = { response: mutation, accepted: { revisionId: nextRevision, publicationId: nextPublication },
      canonicalDocument, graph: {}, receipt: mutation.receipt };
    previous.set(nextPublication, serverBundle);
    serverBundle = result.bundle;
    accepted.set(key, acceptedResult);
    if (loseNext) {
      loseNext = false;
      throw new Error('lost acknowledgement');
    }
    return acceptedResult;
  };
  const mount = async (basis = initial) => {
    const session = await createTimelineCommandSession({
      scope, initial: basis, outboxes, send, changed: (state) => states.push(state.status),
      preview: (patch) => {
        const next = projectClipSplitPreview(patch, current) ?? compileTimelinePatch(patch, current).nextData;
        if (!next) throw new Error('split preview missing');
        current = next;
        previews.push(next);
      },
      project: async (acceptedBasis, patches) => {
        let next = await buildTimelineData(acceptedBasis.canonicalDocument.parent_revision.payload.config as never,
          acceptedBasis.canonicalDocument.parent_revision.payload.registry as never, undefined, 1, undefined,
          { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: acceptedBasis.head.revisionId,
            headPublicationId: acceptedBasis.head.publicationId });
        for (const patch of patches) next = projectClipSplitPreview(patch, next) ?? compileTimelinePatch(patch, next).nextData!;
        current = next;
      },
    });
    return session;
  };
  return { mount, current: () => current, initial, outboxes, requests, previews, states };
}

describe('native clip.split through the durable command session', () => {
  it.each(['matching', 'divergent neighbor', 'empty payload', 'empty config', 'absent payload', 'absent config clips'] as const)(
    'uses native collection validation before capture for %s', async (kind) => {
      const env = await harness();
      const document = structuredClone(env.initial.canonicalDocument);
      const parent = document.parent_revision.payload;
      const config = parent.config as AuthoredBundle['parent'];
      if (kind === 'divergent neighbor') (config.clips as AuthoredBundle['parent'][])[1].at = 99;
      if (kind === 'empty payload') parent.clips = [];
      if (kind === 'empty config') config.clips = [];
      if (kind === 'absent payload') delete parent.clips;
      if (kind === 'absent config clips') delete config.clips;
      const before = structuredClone(document);
      const session = await env.mount({ ...env.initial, canonicalDocument: document });
      const current = env.current();
      const eligible = ['matching', 'absent payload', 'absent config clips'].includes(kind);
      expect(session.clipSplitPort.supports!({ clipId: 'clip-a', current })).toBe(eligible);
      const capture = () => session.clipSplitPort.capture({ clipId: 'clip-a', on: 3, rightId: 'right', current });
      if (eligible) expect(capture().command).toMatchObject({ op: 'clip.split' });
      else expect(capture).toThrow('divergent parent clip mirrors');
      expect(document).toEqual(before);
      expect(env.previews).toEqual([]);
      expect(env.requests).toEqual([]);
      expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
      await session.dispose();
    });

  it.each(['retry', 'reload'] as const)('holds split B and a move suffix behind unknown A until explicit %s', async (action) => {
    const env = await harness({ lost: true });
    const first = await env.mount();
    submitClipSplitEdit(captureClipSplitEdit(first.clipSplitPort, env.current(), 'clip-a', 3, 'right'));
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [pendingA] = await env.outboxes.list(scope);
    const originalRequest = structuredClone(pendingA.pending!.request);
    const split = captureClipSplitEdit(first.clipSplitPort, env.current(), 'right', 4, 'right-2');
    const originalBasis = structuredClone(split.basis);
    submitClipSplitEdit(split);
    submitClipMove(captureClipMove(first.port, env.current(), 'right-2'), 6);
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(3));
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [queued] = await env.outboxes.list(scope);
    expect(env.requests).toHaveLength(1);
    expect(queued.pending!.request).toEqual(originalRequest);
    expect(queued.intents.slice(1).map((intent) => intent.basis))
      .toEqual([{ after: queued.intents[0].id }, { after: queued.intents[1].id }]);
    const commands = queued.intents.map((intent) => (intent.payload as { commands: unknown[] }).commands);
    expect(commands[1]).toMatchObject([{ op: 'clip.split', args: { on: 4, right_id: 'right-2' },
      created: ['parent/clip:right-2'], expect: { 'parent/clip:right::to': { state: 'present', value: 10 } } }]);
    expect(commands[2]).toMatchObject([{ op: 'clip.move', expect: { 'parent/clip:right-2::at': { state: 'present', value: 4 } } }]);
    let session = first;
    if (action === 'reload') {
      await first.dispose();
      session = await env.mount();
      expect(session.getState().status).toBe('recovery');
      expect(env.requests).toHaveLength(1);
      const capture = vi.spyOn(session.clipSplitPort, 'capture');
      await session.recover(queued.ownerId);
      expect(capture).not.toHaveBeenCalled();
    } else await session.retry();
    await session.flush();
    expect(env.requests).toHaveLength(4);
    expect(env.requests[1]).toEqual(env.requests[0]);
    expect(JSON.stringify(env.requests[1].request)).toBe(originalRequest.body);
    expect(env.requests.slice(2).map(({ request }) => request.commands)).toEqual(commands.slice(1));
    expect(env.requests.slice(2).map(({ request }) => request.base_publication_id)).toEqual(['pub-1', 'pub-2']);
    expect(new Set(env.requests.map(({ key }) => key)).size).toBe(3);
    expect(split.basis).toEqual(originalBasis);
    // Ordinary move keeps its existing 180-frame quantization at 30000/1001 fps.
    expect(env.current().config.clips.map(({ id, at }) => ({ id, at })))
      .toEqual([{ id: 'clip-a', at: 1 }, { id: 'right', at: 3 }, { id: 'right-2', at: 6.006 }, { id: 'clip-b', at: 5 }]);
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });

  it('finishes split B on its original capture after A is acknowledged without recapture', async () => {
    const env = await harness({ lost: true });
    const session = await env.mount();
    submitClipSplitEdit(captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-a', 3, 'right'));
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const split = captureClipSplitEdit(session.clipSplitPort, env.current(), 'right', 4, 'right-2');
    const original = structuredClone(split.basis);
    const capture = vi.spyOn(session.clipSplitPort, 'capture');
    await session.retry();
    submitClipSplitEdit(split);
    await session.flush();
    expect(capture).not.toHaveBeenCalled();
    expect(split.basis).toEqual(original);
    expect(env.requests[1]).toEqual(env.requests[0]);
    expect(env.requests[2].request).toMatchObject({ base_publication_id: 'pub-1', commands: [original.command] });
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-a', 'right', 'right-2', 'clip-b']);
    await session.dispose();
  });

  it('uses one prepared command, keeps the raw preview, and retries the exact lost request', async () => {
    const env = await harness({ lost: true });
    const session = await env.mount();
    const captured = captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-a', 3, 'right');
    const originalBasis = structuredClone(captured.basis);
    submitClipSplitEdit(captured);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));

    expect(env.requests).toHaveLength(1);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-a', 'right', 'clip-b']);
    expect(env.current().config.clips[0]).toMatchObject({ from: 2, to: 6, speed: 2,
      opaque: { literal: 'clip-a' }, params: { unknown: [null, false] } });
    expect(captured.basis).toEqual(originalBasis);
    await session.retry();
    await session.flush();
    expect(env.requests).toHaveLength(2);
    expect(env.requests[1]).toEqual(env.requests[0]);
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });

  it('persists an unacknowledged split suffix and reloads it behind the exact prefix', async () => {
    const env = await harness({ lost: true });
    const first = await env.mount();
    const firstEdit = captureClipSplitEdit(first.clipSplitPort, env.current(), 'clip-a', 3, 'right');
    submitClipSplitEdit(firstEdit);
    const secondEdit = captureClipSplitEdit(first.clipSplitPort, env.current(), 'right', 4, 'right-2');
    submitClipSplitEdit(secondEdit);
    await vi.waitFor(() => expect(first.getState().status).toBe('retry'));
    const [savedBeforeReload] = await env.outboxes.list(scope);
    const suffixCommand = (savedBeforeReload.intents[1].payload as { commands: unknown[] }).commands[0];
    const owner = first.getState().ownerId!;
    await first.dispose();

    const second = await env.mount();
    expect(second.getState().status).toBe('recovery');
    await second.recover(owner);
    await second.flush();
    expect(env.requests[1]).toEqual(env.requests[0]);
    expect(env.requests[2].request.base_publication_id).toBe('pub-1');
    expect(env.requests[2].request.commands[0]).toEqual(suffixCommand);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-a', 'right', 'right-2', 'clip-b']);
    await second.dispose();
  });

  it('retains the immutable native draft and local raw preview when acceptance is refused', async () => {
    const env = await harness({ reject: true });
    const session = await env.mount();
    const captured = captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-a', 3, 'right');
    const original = structuredClone(captured.basis);
    submitClipSplitEdit(captured);
    await vi.waitFor(() => expect(session.getState().status).toBe('conflict'));
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(['clip-a', 'right', 'clip-b']);
    expect(captured.basis).toEqual(original);
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.split', select: 'parent/clip:clip-a',
      args: { on: 3, right_id: 'right' } }] });
    await session.dispose();
  });
  it('abandons capture without preview, persistence or a request and fences duplicate completion', async () => {
    const env = await harness();
    const session = await env.mount();
    const current = env.current();
    const captured = captureClipSplitEdit(session.clipSplitPort, current, 'clip-a', 3, 'right');
    const first = session.clipSplitPort.finish(captured.basis);
    expect(session.clipSplitPort.finish(captured.basis)).toEqual(first);
    expect(env.current()).toBe(current);
    expect(env.previews).toEqual([]);
    expect((await env.outboxes.list(scope))[0].intents).toEqual([]);
    expect(env.requests).toEqual([]);
    session.clipSplitPort.submit(first);
    expect(() => session.clipSplitPort.submit(first)).toThrow('not captured');
    expect(() => session.clipSplitPort.finish(captured.basis)).toThrow('changed');
    await session.flush();
    expect(env.requests).toHaveLength(1);
    expect(env.previews).toHaveLength(1);
    await session.dispose();
  });

  it('undoes one accepted split through the existing guarded publication inverse request', async () => {
    const env = await harness();
    const session = await env.mount();
    const before = structuredClone(env.current().config);
    submitClipSplitEdit(captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-a', 3, 'right'));
    await session.flush();
    expect(session.getState().canUndo).toBe(true);
    await session.undo();
    await session.flush();
    expect(env.requests[1].request.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse',
      version: '1', select: null, args: { publications: ['pub-1'] } }]);
    expect(env.current().config).toEqual(before);
    expect(session.getState().canUndo).toBe(false);
    await session.dispose();
  });

  it('uses raw parent ownership with opaque canonical metadata and a colon in the reserved ID', async () => {
    const env = await harness({ lost: true });
    const document = structuredClone(env.initial.canonicalDocument);
    const rows = document.parent_revision.payload.clips as Array<Record<string, unknown>>;
    rows[0].app = { ...rows[0].app as object, canonical: { ownerRef: 'opaque', occurrenceId: 'literal', clipRef: 'literal' } };
    (document.parent_revision.payload.config as Record<string, unknown>).clips = structuredClone(rows);
    const basis = { ...env.initial, canonicalDocument: document };
    const session = await env.mount(basis);
    const current = env.current();
    current.config.clips[0].app = rows[0].app as never;
    current.resolvedConfig.clips[0].app = rows[0].app as never;
    const captured = captureClipSplitEdit(session.clipSplitPort, current, 'clip-a', 3, 'right:part');
    const finished = session.clipSplitPort.finish(captured.basis);
    expect(finished.preview.operations[0].payload!.right).toMatchObject({ id: 'right:part',
      app: { canonical: (rows[0].app as Record<string, unknown>).canonical, astrid: { for: 2 } } });
    // No opaque namespace is rewritten into an owner or a suffix-generated identity.
    expect(finished.command.select).toBe('parent/clip:clip-a');
    expect(finished.command.created).toEqual(['parent/clip:right:part']);
    await session.dispose();
  });

  it.each(['head', 'group', 'collision', 'occurrence'])('refuses unsupported %s before local preview', async (kind) => {
    const env = await harness();
    const session = await env.mount();
    const current = structuredClone(env.current());
    if (kind === 'head') current.head!.headPublicationId = 'other';
    if (kind === 'group') current.config.pinnedShotGroups = [{ clipIds: ['clip-a'] }] as never;
    if (kind === 'collision') current.config.clips.push({ id: 'right' } as never);
    if (kind === 'occurrence') {
      current.config.clips[0].id = 'occ:clip-a';
      current.resolvedConfig.clips[0].id = 'occ:clip-a';
    }
    expect(() => captureClipSplitEdit(session.clipSplitPort, current,
      kind === 'occurrence' ? 'occ:clip-a' : 'clip-a', 3, 'right')).toThrow();
    expect(env.previews).toEqual([]);
    expect(env.requests).toEqual([]);
    await session.dispose();
  });

  it('refuses altered previews and stale prepared commands without appending anything', async () => {
    const env = await harness();
    const session = await env.mount();
    const captured = captureClipSplitEdit(session.clipSplitPort, env.current(), 'clip-a', 3, 'right');
    const finished = session.clipSplitPort.finish(captured.basis);
    const changed = structuredClone(finished);
    changed.preview.operations[0].payload!.right = { id: 'forged' };
    expect(() => session.clipSplitPort.submit(changed)).toThrow('exact native preview');
    expect(env.previews).toEqual([]);
    expect(env.requests).toEqual([]);
    session.clipSplitPort.submit(finished);
    await session.flush();
    expect(() => session.clipSplitPort.submit(finished)).toThrow('not captured');
    await session.dispose();
  });

});
