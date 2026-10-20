import { afterEach, describe, expect, it, vi } from 'vitest';
import { createFakeIndexedDB } from 'fake-indexeddb';
import { ApiError } from '@/integrations/runtime/generated';
import type { CanonicalDocument, CommitRequest, JSON, Task, ManagedOutput } from '@/integrations/runtime/generated';
import { acceptedCommit } from '@/integrations/runtime/__tests__/timelineCommitFixture';
import { authoringBundleFromDocument } from '@/tools/video-editor/commands/authoringBundle';
import { captureOccurrenceAddMedia } from '@/tools/video-editor/commands/occurrenceMediaCapture';
import { createCommitOutbox } from '@/tools/video-editor/commands/commitOutbox';
import { createTimelineCommandSession } from '@/tools/video-editor/commands/commitSession';
import type { TimelineCommandBasis, TimelineCommitResult } from '@/tools/video-editor/data/DataProvider';
import native from '@/tools/video-editor/commands/fixtures/recipe_m2_occurrence_media.json';
import recovery from '../__fixtures__/runtimeRecoveryGeneration.json';
import { freezeRecoveryValue, type RuntimeRecoveryPlacementDraft } from './runtimeRecoveryDestinations';
import {
  createRuntimeRecoveryPlacement, type RuntimeRecoveryCommandBinding, type RuntimeRecoveryPlacementClient,
} from './runtimeRecoveryPlacement';

const disposals: (() => Promise<void>)[] = [];
afterEach(async () => { for (const dispose of disposals.splice(0)) await dispose(); });

async function environment() {
  const document = structuredClone(native.add.input) as CanonicalDocument;
  const basis: TimelineCommandBasis = { canonicalDocument: document,
    head: { revisionId: document.parent_revision.revision_id, publicationId: 'publication-original' } };
  const scope = { projectId: document.project_id, timelineId: document.timeline_id, actorId: 'manual-actor', realmId: 'manual-realm' };
  const media = structuredClone(native.add.commands[0].args.media);
  const task = { ...structuredClone(recovery.task), project_id: scope.projectId } as Task;
  const output = { ...structuredClone(recovery.outputs.items[0]), project_id: scope.projectId,
    object_id: media.object_id, media_type: 'video/fixture' } as ManagedOutput;
  const draft: RuntimeRecoveryPlacementDraft = { projectId: scope.projectId, timelineId: scope.timelineId, basis,
    source: { task, output, mediaTuple: media }, destination: {
      id: 'display-only', name: 'Duplicate · misleading:raw/owner', owner: { kind: 'occurrence', occurrenceId: 'occ-a' },
      shotId: 'chapter-shot', shotRevisionId: 'shot-1', internalTimelineId: document.internal_timeline_revisions[0].timeline_id,
      internalRevisionId: document.internal_timeline_revisions[0].revision_id, parentTrackId: 'picture', childTrackId: 'picture',
    }, on: 8.125, sourceWindow: { from: 2, to: 6 } };
  const client = {
    getRecoverableIdentity: vi.fn(async () => ({ actorId: scope.actorId, realmId: scope.realmId })),
    getTask: vi.fn(async () => task), getManagedOutput: vi.fn(async () => output),
    getProjectMediaSelection: vi.fn(async () => media),
    getProjectVerifiedMedia: vi.fn(async () => structuredClone(native.add.verified_media[1])),
    getProjectTimeline: vi.fn(async () => ({ project_id: scope.projectId, timeline_id: scope.timelineId,
      head_revision_id: basis.head.revisionId, head_publication_id: basis.head.publicationId })),
  };
  const factory = createFakeIndexedDB();
  const outboxes = createCommitOutbox({ indexedDB: factory, exclusiveLock: async (_name, work) => work() });
  const sent: { body: string; key: string }[] = [];
  let fault: 'lost' | 'refused' | null = null;
  const send = vi.fn(async (request: CommitRequest, key: string): Promise<TimelineCommitResult> => {
    sent.push({ body: JSON.stringify(request), key });
    if (fault === 'refused') throw new ApiError(409, 'conflict', 'ownership changed', '', { status: 'conflict' });
    if (fault === 'lost') throw new Error(fault);
    // Typed detached acceptance only. The real compiler/door is a separate gate.
    const response = acceptedCommit({ revision_id: 'accepted-manual', publication_id: 'accepted-publication' },
      { revision_id: basis.head.revisionId, publication_id: basis.head.publicationId }, { ...scope, commands: request.commands });
    const canonicalDocument = structuredClone(native.add.output) as CanonicalDocument;
    canonicalDocument.parent_revision.revision_id = 'accepted-manual';
    response.data.canonical_document = canonicalDocument;
    return { response, canonicalDocument, accepted: { revisionId: 'accepted-manual', publicationId: 'accepted-publication' } };
  });
  const projected = vi.fn();
  const session = await createTimelineCommandSession({ scope, initial: basis, outboxes, send,
    preview: () => { throw new Error('No optimistic manual placement'); }, project: projected, changed: vi.fn() });
  disposals.push(() => session.dispose());
  const boundClient = client as unknown as RuntimeRecoveryPlacementClient;
  let binding: RuntimeRecoveryCommandBinding | null = { client: boundClient, session };
  const request = createRuntimeRecoveryPlacement({ client: boundClient, getBinding: () => binding });
  return { draft, client, request, session, outboxes, factory, sent, send, projected, scope,
    rebind: (next: RuntimeRecoveryCommandBinding | null) => { binding = next; }, setFault: (value: typeof fault) => { fault = value; } };
}

describe('explicit manual recovery native ADD callback (source only)', () => {
  it('routes frozen raw ownership and all five pin fields to ONE durable native command', async () => {
    const env = await environment(), original = structuredClone(env.draft);
    await env.request(freezeRecoveryValue(env.draft));
    expect(env.draft).toEqual(original);
    expect(env.client.getProjectVerifiedMedia).toHaveBeenCalledExactlyOnceWith(env.scope.projectId, original.source.mediaTuple);
    expect(env.client.getProjectMediaSelection).toHaveBeenCalledWith(env.scope.projectId, {
      association_id: original.source.output.association_id, object_id: original.source.mediaTuple.object_id, version: original.source.output.version,
    });
    expect(env.sent).toHaveLength(1);
    const wire = JSON.parse(env.sent[0].body) as CommitRequest, command = wire.commands[0];
    expect(wire).toMatchObject({ project_id: env.scope.projectId, timeline_id: env.scope.timelineId,
      base_revision_id: original.basis.head.revisionId, base_publication_id: original.basis.head.publicationId });
    expect(wire.commands).toHaveLength(1);
    expect(command).toMatchObject({ op: 'occurrence.add-media', select: 'occurrence:occ-a', intent: { ownership: 'occurrence' },
      args: { media: original.source.mediaTuple, row: { clipType: 'video', track: 'picture', asset: original.source.mediaTuple.asset,
        at: 0.125, hold: 4, from: 2, to: 6 } } });
    const captured = captureOccurrenceAddMedia(await authoringBundleFromDocument(original.basis.canonicalDocument), command.select!,
      command.args.row as Record<string, JSON>, original.source.mediaTuple, native.add.verified_media);
    expect(command).toEqual(captured.command);
    expect(command.created).toEqual(['occurrence:occ-a/asset:reserved-new', `occurrence:occ-a/clip:${(command.args.row as { id: string }).id}`]);
    expect(command.args).not.toHaveProperty('task_producer_guard');
    expect(await env.outboxes.list(env.scope)).toHaveLength(1);
    expect(env.projected).toHaveBeenCalledOnce();
    expect(env.session.getState().status).toBe('saved');
    await expect(env.request(original)).rejects.toThrow('already submitted');
    expect(env.sent).toHaveLength(1);
  });

  it('maps explicit image hold without inventing a source window or four-second default', async () => {
    const env = await environment();
    env.draft.sourceWindow = { from: 0, to: 1.25 };
    env.client.getProjectVerifiedMedia.mockResolvedValue({ ...native.add.verified_media[1], media_type: 'image/png' });
    await env.request(env.draft);
    const row = JSON.parse(env.sent[0].body).commands[0].args.row;
    expect(row).toMatchObject({ at: 0.125, hold: 1.25, clipType: 'image' });
    expect(row).not.toHaveProperty('from');
    expect(row).not.toHaveProperty('to');
  });

  it.each(['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'] as const)('refuses changed verified %s without sending', async (field) => {
    const env = await environment(), before = structuredClone(env.draft);
    const verified = structuredClone(native.add.verified_media[1]);
    verified.selection[field] += '-changed';
    env.client.getProjectVerifiedMedia.mockResolvedValue(verified);
    await expect(env.request(env.draft)).rejects.toThrow('frozen selection');
    expect(env.draft).toEqual(before);
    expect(env.sent).toEqual([]);
  });

  it.each(['missing', 'client', 'scope', 'actor', 'head', 'publication', 'owner', 'shot', 'internal', 'track', 'parent', 'timing', 'map', 'nonfinite', 'boundary'])('retains draft and refuses %s', async (change) => {
    const env = await environment();
    if (change === 'missing') env.rebind(null);
    if (change === 'client') env.rebind({ session: env.session, client: { ...env.client } as unknown as RuntimeRecoveryPlacementClient });
    if (change === 'scope') env.draft.timelineId = 'another-film';
    if (change === 'actor') env.client.getRecoverableIdentity.mockResolvedValue({ actorId: 'another-actor', realmId: env.scope.realmId });
    if (change === 'head') env.client.getProjectTimeline.mockResolvedValue({ project_id: env.scope.projectId, timeline_id: env.scope.timelineId, head_revision_id: 'new', head_publication_id: env.draft.basis.head.publicationId });
    if (change === 'publication') env.client.getProjectTimeline.mockResolvedValue({ project_id: env.scope.projectId, timeline_id: env.scope.timelineId, head_revision_id: env.draft.basis.head.revisionId, head_publication_id: 'new' });
    if (change === 'owner') env.draft.destination.owner.occurrenceId = 'occ-a:display-child';
    if (change === 'shot') env.draft.destination.shotRevisionId = 'another-revision';
    if (change === 'internal') env.draft.destination.internalRevisionId = 'another-internal';
    if (change === 'track') env.draft.destination.childTrackId = 'picture:display-track';
    if (change === 'parent') env.draft.destination.owner.kind = 'parent' as 'occurrence';
    if (change === 'timing') env.draft.on = 1;
    if (change === 'boundary') env.draft.sourceWindow.to = 7;
    if (change === 'map' || change === 'nonfinite') {
      const rows = env.draft.basis.canonicalDocument.parent_revision.payload.occurrences as Record<string, unknown>[];
      if (change === 'map') rows[0].speed = 2;
      else env.draft.sourceWindow = { from: Number.NaN, to: 3 };
    }
    const before = structuredClone(env.draft);
    await expect(env.request(env.draft)).rejects.toThrow();
    expect(env.draft).toEqual(before);
    expect(env.sent).toEqual([]);
    expect(env.projected).not.toHaveBeenCalled();
  });

  it.each(['cancel', 'owner', 'actor', 'head', 'source'])('fences a pending metadata read on %s change', async (change) => {
    const env = await environment(), controller = new AbortController();
    let release!: () => void;
    const gate = new Promise<void>((resolve) => { release = resolve; });
    env.client.getProjectVerifiedMedia.mockImplementation(async () => { await gate; return structuredClone(native.add.verified_media[1]); });
    const running = env.request(env.draft, controller.signal);
    await vi.waitFor(() => expect(env.client.getProjectVerifiedMedia).toHaveBeenCalledOnce());
    if (change === 'cancel') controller.abort();
    if (change === 'owner') env.rebind(null);
    if (change === 'actor') env.client.getRecoverableIdentity.mockResolvedValue({ actorId: 'changed', realmId: env.scope.realmId });
    if (change === 'head') env.client.getProjectTimeline.mockRejectedValue(new Error('changed head'));
    if (change === 'source') env.client.getTask.mockRejectedValue(new Error('changed task'));
    release();
    await expect(running).rejects.toThrow();
    expect(env.sent).toEqual([]);
  });

  it('keeps an unknown outcome in the existing outbox and retries its exact IDs/body/key through that owner', async () => {
    const env = await environment(), original = structuredClone(env.draft);
    env.setFault('lost');
    await expect(env.request(env.draft)).rejects.toThrow();
    expect(env.session.getState().status).toBe('retry');
    expect(env.draft).toEqual(original);
    const [owner] = await env.outboxes.list(env.scope);
    expect(owner.intents).toHaveLength(1);
    expect(owner.pending?.request.body).toBe(env.sent[0].body);
    expect(env.projected).not.toHaveBeenCalled();
    await expect(env.request(env.draft)).rejects.toThrow('already submitted');
    expect(env.sent).toHaveLength(1);
    env.setFault(null);
    await env.session.retry();
    expect(env.sent).toHaveLength(2);
    expect(env.sent[1]).toEqual(env.sent[0]);
    expect(env.session.getState().status).toBe('saved');
  });

  it.each(['append', 'ack'] as const)('keeps the original capture with the owner after %s storage failure', async (stage) => {
    const env = await environment(), original = structuredClone(env.draft);
    const capture = vi.spyOn(env.session, 'addOccurrenceMedia');
    const open = env.factory.open.bind(env.factory);
    const failStorage = () => { env.factory.open = () => { throw new Error('disk full'); }; };
    if (stage === 'append') failStorage();
    else {
      const send = env.send.getMockImplementation()!;
      env.send.mockImplementationOnce(async (...args) => {
        const result = await send(...args);
        failStorage();
        return result;
      });
    }
    try {
      await expect(env.request(env.draft)).rejects.toThrow('disk full');
      expect(env.session.getState().status).toBe('error');
      expect(env.draft).toEqual(original);
      expect(env.projected).not.toHaveBeenCalled();
      await expect(env.request(env.draft)).rejects.toThrow('already submitted');
      env.draft.sourceWindow.to = 5;
      await expect(env.request(env.draft)).rejects.toThrow('already submitted');
      expect(capture).toHaveBeenCalledOnce();
    } finally { env.factory.open = open; }
    const [owner] = await env.outboxes.list(env.scope);
    expect(owner.intents).toHaveLength(stage === 'append' ? 0 : 1);
    if (stage === 'ack') {
      expect(owner.pending?.request.body).toBe(env.sent[0].body);
      expect(owner.pending?.request.key).toBe(env.sent[0].key);
    } else expect(env.sent).toEqual([]);
    await env.session.retry();
    expect(env.session.getState().status).toBe('saved');
    expect(env.sent).toHaveLength(stage === 'append' ? 1 : 2);
    if (stage === 'ack') expect(env.sent[1]).toEqual(env.sent[0]);
    const command = JSON.parse(env.sent[0].body).commands[0];
    expect(command.args.row).toEqual(capture.mock.calls[0][0].row);
    expect(command.args.row).toMatchObject({ id: capture.mock.calls[0][0].row.id, from: 2, to: 6, hold: 4 });
    expect(capture).toHaveBeenCalledOnce();
  });

  it('retains a definitive Runtime refusal without recapture or legacy placement', async () => {
    const env = await environment(), original = structuredClone(env.draft);
    env.setFault('refused');
    await expect(env.request(env.draft)).rejects.toThrow('ownership changed');
    expect(env.session.getState().status).toBe('conflict');
    const [owner] = await env.outboxes.list(env.scope);
    expect(owner.pending?.outcome?.kind).toBe('rejected');
    expect(owner.intents).toHaveLength(1);
    expect(env.draft).toEqual(original);
    expect(env.projected).not.toHaveBeenCalled();
    await expect(env.request(env.draft)).rejects.toThrow('already submitted');
    expect(env.sent).toHaveLength(1);
  });

  it('checks chooser cancellation again after the session’s asynchronous basis conversion', async () => {
    const env = await environment(), controller = new AbortController();
    const add = env.session.addOccurrenceMedia;
    vi.spyOn(env.session, 'addOccurrenceMedia').mockImplementation(async (input) => { controller.abort(); return add(input); });
    await expect(env.request(env.draft, controller.signal)).rejects.toThrow('cancelled');
    expect(env.sent).toEqual([]);
    expect((await env.outboxes.list(env.scope))[0].intents).toEqual([]);
  });
});

describe('independent retry controls', () => {
  it('can retry a pre-capture cancellation with the same reserved identity', async () => {
    const env = await environment(), controller = new AbortController();
    const add = env.session.addOccurrenceMedia;
    const capture = vi.spyOn(env.session, 'addOccurrenceMedia').mockImplementationOnce(async (input) => { controller.abort(); return add(input); });
    const uuid = vi.spyOn(crypto, 'randomUUID');
    await expect(env.request(env.draft, controller.signal)).rejects.toThrow('cancelled');
    expect(env.sent).toEqual([]);
    expect((await env.outboxes.list(env.scope))[0].intents).toEqual([]);
    const reserved = uuid.mock.results[0].value;
    await expect(env.request(env.draft, new AbortController().signal)).resolves.toBeUndefined();
    expect((capture.mock.calls[1][0].row).id).toBe(reserved);
    uuid.mockRestore();
  });
  it('can correct an unsupported source window after an atomic capture refusal', async () => {
    const env = await environment();
    env.draft.sourceWindow.to = 7;
    await expect(env.request(env.draft)).rejects.toThrow();
    expect(env.sent).toEqual([]);
    expect((await env.outboxes.list(env.scope))[0].intents).toEqual([]);
    env.draft.sourceWindow.to = 6;
    await expect(env.request(env.draft)).resolves.toBeUndefined();
    expect(env.sent).toHaveLength(1);
  });
});
