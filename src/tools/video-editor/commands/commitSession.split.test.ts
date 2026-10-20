// @vitest-environment node
import { createFakeIndexedDB } from 'fake-indexeddb';
import { describe, expect, it, vi } from 'vitest';
import type { CommitRequest, TimelineCommitResult } from '@/integrations/runtime/generated.ts';
import { ApiError } from '@/integrations/runtime/generated.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { buildTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import type { TimelineCommandBasis } from '../data/DataProvider.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createCommitOutbox } from './commitOutbox.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { executeClipSplit } from './clipSplitCapture.ts';
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
    const result = executeClipSplit(serverBundle, request.commands[0]);
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
        const next = projectClipSplitPreview(patch, current);
        if (!next) throw new Error('split preview missing');
        current = next;
        previews.push(next);
      },
      project: async (acceptedBasis, patches) => {
        let next = await buildTimelineData(acceptedBasis.canonicalDocument.parent_revision.payload.config as never,
          acceptedBasis.canonicalDocument.parent_revision.payload.registry as never, undefined, 1, undefined,
          { projectId: scope.projectId, timelineId: scope.timelineId, headRevisionId: acceptedBasis.head.revisionId,
            headPublicationId: acceptedBasis.head.publicationId });
        for (const patch of patches) next = projectClipSplitPreview(patch, next)!;
        current = next;
      },
    });
    return session;
  };
  return { mount, current: () => current, initial, outboxes, requests, previews, states };
}

describe('native clip.split through the durable command session', () => {
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
});
