import { describe, expect, it, vi } from 'vitest';
import type { CanonicalDocument, CommitRequest, MediaSelection, VerifiedMedia } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { copy } from './clipMovePrimitives.ts';
import { OccurrenceMediaState } from './occurrenceMediaPrimitives.ts';
import { executeClipSet } from './clipScalarCapture.ts';
import { captureClipScalarEdit, submitClipScalarEdit } from './clipScalarGesture.ts';
import { captureOccurrenceMediaEdit, occurrenceMediaPreview, projectOccurrenceMediaPreview, submitOccurrenceMediaEdit,
  type OccurrenceMediaRequest } from './occurrenceMediaGesture.ts';
import { environment } from './__tests__/commitSessionEnvironment.ts';
import { occurrenceMediaFixtureGraph } from './__tests__/occurrenceMediaFixture.ts';
import fixture from './fixtures/recipe_m2_occurrence_media.json';

const scope = { projectId: 'project-1', timelineId: 'film', realmId: 'realm-1', actorId: 'actor-1' };
const head = { revisionId: fixture.add.input.parent_revision.revision_id, publicationId: 'p0' };
const ownerRef = 'occurrence:occ-a', trackRef = `${ownerRef}/track:picture`, clipRef = `${ownerRef}/clip:clip-a`;
const request = (kind: 'add' | 'swap'): OccurrenceMediaRequest => kind === 'add'
  ? { kind, ownerRef, trackRef, row: copy(fixture.add.commands[0].args.row), media: copy(fixture.add.commands[0].args.media) }
  : { kind, ownerRef, trackRef, clipRef, oldMedia: copy(fixture.swap.commands[0].args.old_media), media: copy(fixture.swap.commands[0].args.media) };
const row = (bundle: unknown, ref = clipRef) => new OccurrenceMediaState(bundle as never).entity(ref)!;

async function setup(kind: 'add' | 'swap' = 'add') {
  const { outboxes } = await environment();
  const raw: CanonicalDocument = { ...copy(fixture[kind].input), schema_version: 1 };
  const graph = occurrenceMediaFixtureGraph(raw);
  const shotComposition = { load: async () => graph };
  const initial: TimelineCommandBasis = { head, canonicalDocument: raw, graph };
  const parent = raw.parent_revision.payload;
  const seed = await buildTimelineData({ ...parent.config as TimelineConfig, clips: parent.clips as TimelineConfig['clips'] },
    parent.registry as AssetRegistry, undefined, 1, undefined, { ...scope, headRevisionId: head.revisionId, headPublicationId: head.publicationId });
  const initialBundle = await authoringBundleFromDocument(raw);
  let current = projectOccurrenceMediaPreview(occurrenceMediaPreview(initialBundle, graph), seed, shotComposition)!;
  const reads = vi.fn(async (pin: MediaSelection): Promise<VerifiedMedia> => copy(fixture[kind].verified_media.find((input) => input.selection.object_id === pin.object_id)!));
  const requests: Array<{ body: string; key: string }> = [];
  let send: (request: CommitRequest, key: string) => Promise<TimelineCommitResult> = async () => { throw new Error('lost acknowledgement (unit sender)'); };
  const applyPreview = (patch: Parameters<typeof projectOccurrenceMediaPreview>[0]) => {
    const native = projectOccurrenceMediaPreview(patch, current, shotComposition);
    const next = native ?? compileTimelinePatch(patch, current).nextData;
    if (!next) throw new Error('Invalid local preview');
    current = next;
  };
  const preview = vi.fn(applyPreview);
  const project = vi.fn(async (_basis: TimelineCommandBasis, previews: Parameters<typeof projectOccurrenceMediaPreview>[0][]) => {
    current = projectOccurrenceMediaPreview(occurrenceMediaPreview(initialBundle, graph), seed, shotComposition)!;
    for (const patch of previews) applyPreview(patch);
  });
  const mount = (read: typeof reads | null = reads) => createTimelineCommandSession({ scope, initial, outboxes,
    getProjectVerifiedMedia: read ?? undefined, preview, project, changed: () => {},
    send: (body, key) => { requests.push({ body: JSON.stringify(body), key }); return send(body, key); } });
  return { outboxes, initial, initialBundle, seed, mount, reads, requests, project, preview, current: () => current,
    setSend: (next: typeof send) => { send = next; } };
}

// Detached metadata and an uncertain unit sender exercise App mechanics only; no Runtime authority/acceptance.
describe('occurrence media in the existing durable session', () => {
  it('refuses capture without a Runtime verified-media reader before preview or outbox writes', async () => {
    const env = await setup(), session = await env.mount(null);
    expect(() => captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('add')))
      .toThrow('Runtime verified-media read is unavailable');
    expect(env.reads).not.toHaveBeenCalled();
    expect(env.preview).not.toHaveBeenCalled();
    expect(env.requests).toHaveLength(0);
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    await session.dispose();
  });

  it.each(['add', 'swap'] as const)('retains exact native %s claims, both pins, opaque bytes and restart retry identity', async (kind) => {
    const env = await setup(kind), session = await env.mount();
    const input = request(kind);
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), input);
    const original = copy(captured.basis);
    input.media.asset = 'caller-mutated-after-capture';
    await submitOccurrenceMediaEdit(captured);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(JSON.parse(env.requests[0].body).commands).toEqual(fixture[kind].commands);
    expect(env.reads.mock.calls.map(([pin]) => pin)).toEqual(kind === 'add'
      ? [fixture.add.commands[0].args.media] : [fixture.swap.commands[0].args.old_media, fixture.swap.commands[0].args.media]);
    const [stored] = await env.outboxes.list(scope);
    const payload = stored.intents[0].payload as { before: unknown; after: unknown };
    const target = kind === 'add' ? `${ownerRef}/clip:reserved-child` : clipRef;
    expect(row(payload.after, target)).toEqual(kind === 'add' ? fixture.add.commands[0].args.row
      : { ...row(payload.before), asset: fixture.swap.commands[0].args.media.asset });
    const sibling = 'occurrence:occ-b/clip:clip-a';
    expect(row(payload.after, sibling)).toEqual(row(payload.before, sibling));
    expect(captured.basis).toEqual(original);
    const projected = copy(env.current().config);
    await session.retry();
    expect(env.requests[1]).toEqual(env.requests[0]);
    await session.dispose();
    const reopened = await env.mount();
    expect(reopened.getState().status).toBe('recovery');
    expect(env.requests).toHaveLength(2);
    await reopened.recover(stored.ownerId);
    expect(env.requests[2]).toEqual(env.requests[0]);
    expect(env.current().config).toEqual(projected);
    expect(env.reads).toHaveBeenCalledTimes(kind === 'add' ? 1 : 2); // Recovery never resolves pins again.
    expect((await env.outboxes.list(scope))[0].pending).toEqual(stored.pending);
    await reopened.dispose();
  });

  it('projects the full ADD source window, registry and occurrence geometry through the canonical projector', async () => {
    const env = await setup(), session = await env.mount();
    await submitOccurrenceMediaEdit(captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('add')));
    const clip = env.current().resolvedConfig.clips.find((clip) => clip.id === 'occ-a:reserved-child')!;
    expect(clip).toMatchObject({ at: 8.125, from: 2, to: 6, speed: 2,
      app: { canonical: { ownerRef, rawClipId: 'reserved-child', clipRef: `${ownerRef}/clip:reserved-child` } } });
    expect(clip.assetEntry).toMatchObject({ media_id: fixture.add.commands[0].args.media.object_id, type: 'video' });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(env.current().config.clips.filter((clip) => clip.id === 'occ-a:reserved-child')).toHaveLength(1);
    const [stored] = await env.outboxes.list(scope);
    expect(row((stored.intents[0].payload as { after: unknown }).after, `${ownerRef}/clip:reserved-child`))
      .toEqual(fixture.add.commands[0].args.row); // Includes null params, opaque, hold and raw local start.
    await session.dispose();
  });

  it.each(['old', 'new'] as const)('retains the immutable swap intention after a %s media lifecycle refusal', async (which) => {
    const env = await setup('swap'), session = await env.mount();
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('swap'));
    const original = copy(captured.basis), current = env.current();
    env.reads.mockImplementation(async (pin) => {
      if (pin.generation_id === `generation-${which}`) throw new Error('media lifecycle changed');
      return copy(fixture.swap.verified_media.find((input) => input.selection.object_id === pin.object_id)!);
    });
    await expect(submitOccurrenceMediaEdit(captured)).rejects.toThrow('media lifecycle changed');
    expect(session.getState()).toMatchObject({ status: 'error', error: 'media lifecycle changed' });
    expect(env.current()).toBe(current);
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    expect(env.requests).toHaveLength(0);
    expect(captured.basis).toEqual(original);
    env.reads.mockImplementation(async (pin) => copy(fixture.swap.verified_media.find((input) => input.selection.object_id === pin.object_id)!));
    await submitOccurrenceMediaEdit(captured);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(JSON.parse(env.requests[0].body).commands).toEqual(fixture.swap.commands);
    await session.dispose();
  });

  it.each(['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest'] as const)('refuses a mismatched verified %s without refreshing the pin', async (field) => {
    const env = await setup(), session = await env.mount();
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('add'));
    env.reads.mockImplementation(async (pin) => ({ ...copy(fixture.add.verified_media[1]), selection: { ...pin, [field]: 'different' } }));
    await expect(submitOccurrenceMediaEdit(captured)).rejects.toThrow('original immutable pin');
    expect(env.preview).not.toHaveBeenCalled();
    expect(env.requests).toHaveLength(0);
    await session.dispose();
  });

  it('fences a delayed read after another local edit and rejects a cloned basis from another owner', async () => {
    const env = await setup('swap'), session = await env.mount();
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('swap'));
    let release!: (value: VerifiedMedia) => void;
    env.reads.mockImplementationOnce(() => new Promise((resolve) => { release = resolve; }));
    const pending = submitOccurrenceMediaEdit(captured);
    // Reuse an ordinary port in this same queue; its preview is irrelevant to the pending read fence.
    submitClipScalarEdit(captureClipScalarEdit(session.clipScalarPort, env.current(), 'clip-a', 'parent'), { values: { hold: 3 }, clear: [] });
    release(copy(fixture.swap.verified_media[0]));
    await expect(pending).rejects.toThrow('Timeline changed during the media read');
    expect(env.preview.mock.calls.filter(([patch]) => patch.source === 'occurrence.media')).toHaveLength(0);
    const other = await env.mount();
    await expect(other.occurrenceMediaPort.finish(copy(captured.basis))).rejects.toThrow();
    await other.dispose();
    await session.dispose();
  });

  it.each([
    { ownerRef: 'occurrence:occ-b' }, { trackRef: 'occurrence:occ-b/track:picture' },
    { clipRef: 'occurrence:occ-b/clip:clip-a' }, { clipRef: 'occurrence:occ-a/clip:occ-a:clip-a' },
  ])('refuses mismatched owner/raw track/raw child refs %j before reads', async (change) => {
    const env = await setup('swap'), session = await env.mount();
    expect(() => captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), { ...request('swap'), ...change } as OccurrenceMediaRequest)).toThrow();
    expect(env.reads).not.toHaveBeenCalled();
    expect(env.preview).not.toHaveBeenCalled();
    expect(env.requests).toHaveLength(0);
    await session.dispose();
  });

  it('refuses a forged partial preview while keeping the prepared complete intention usable', async () => {
    const env = await setup(), session = await env.mount();
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('add'));
    const result = await session.occurrenceMediaPort.finish(captured.basis);
    expect(() => session.occurrenceMediaPort.submit({ ...result, preview: { version: 1, operations: [
      { op: 'clip.add', target: 'reserved-child', payload: { track: 'picture', at: 0.125, clipType: 'video' } },
    ] } })).toThrow('complete closure preview');
    expect(env.preview).not.toHaveBeenCalled();
    session.occurrenceMediaPort.submit(result);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(JSON.parse(env.requests[0].body).commands).toEqual(fixture.add.commands);
    await session.dispose();
  });

  it('keeps a dependent media suffix behind an uncertain ordinary edit in the same outbox', async () => {
    const env = await setup('swap'), session = await env.mount();
    submitClipScalarEdit(captureClipScalarEdit(session.clipScalarPort, env.current(), 'clip-a', 'parent'),
      { values: { hold: 3 }, clear: [] });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('swap'));
    const original = copy(captured.basis);
    await submitOccurrenceMediaEdit(captured);
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2));
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[1].basis).toEqual({ after: stored.intents[0].id });
    expect(stored.intents[1].payload).toMatchObject({ commands: fixture.swap.commands });
    expect(row((stored.intents[1].payload as { after: unknown }).after, 'parent/clip:clip-a').hold).toBe(3);
    expect(captured.basis).toEqual(original);
    await session.dispose();
    const reopened = await env.mount();
    await reopened.recover(stored.ownerId);
    expect((await env.outboxes.list(scope))[0].intents).toEqual(stored.intents);
    expect(env.requests.every((item) => JSON.parse(item.body).commands[0].op === 'clip.set')).toBe(true);
    expect(env.requests.every((item) => item.body === env.requests[0].body && item.key === env.requests[0].key)).toBe(true);
    expect(env.reads).toHaveBeenCalledTimes(2);
    await reopened.dispose();
  });

  it('keeps the original media display graph when a mocked ordinary ACK advances the submission base', async () => {
    const env = await setup('swap'), session = await env.mount();
    const scalar = (id: string) => submitClipScalarEdit(captureClipScalarEdit(session.clipScalarPort, env.current(), id, 'parent'),
      { values: { hold: 3 }, clear: [] });
    scalar('clip-a');
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    scalar('clip-b');
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2));
    env.setSend(async (request, key) => {
      if (request.commands[0].select !== 'parent/clip:clip-a') throw new Error('uncertain ordinary suffix');
      const after = executeClipSet(env.initialBundle, request.commands[0]).bundle;
      const raw = copy(env.initial.canonicalDocument);
      raw.parent_revision = { revision_id: 'r1', content_digest: '', payload: {
        ...after.parent, occurrences: copy(raw.parent_revision.payload.occurrences),
      } };
      raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
      const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' },
        { revision_id: head.revisionId, publication_id: head.publicationId }, { ...scope, commands: request.commands });
      response.data.canonical_document = raw;
      response.receipt.idempotency_key = key;
      return { response, receipt: response.receipt, accepted: { revisionId: 'r1', publicationId: 'p1' },
        canonicalDocument: raw, graph: occurrenceMediaFixtureGraph(raw) };
    });
    await session.retry();
    const captured = captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('swap'));
    await submitOccurrenceMediaEdit(captured);
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2));
    const [stored] = await env.outboxes.list(scope);
    const media = stored.intents[1].payload as { displayBasis: TimelineCommandBasis; commands: unknown };
    expect(media.displayBasis.head).toEqual(head); // ACK changes submission, never the original displayed closure.
    expect(media.commands).toEqual(fixture.swap.commands);
    await session.dispose();
    const reopened = await env.mount();
    await reopened.recover(stored.ownerId);
    expect((await env.outboxes.list(scope))[0].intents[1].payload).toEqual(stored.intents[1].payload);
    expect(env.current().config.clips.find((clip) => clip.id === 'clip-a')?.hold).toBe(3);
    expect(env.current().config.clips.find((clip) => clip.id === 'clip-b')?.hold).toBe(3);
    expect(env.reads).toHaveBeenCalledTimes(2);
    await reopened.dispose();
  });

  it('retains the exact refused Runtime prefix across restart without any new media read', async () => {
    const env = await setup('swap'), session = await env.mount();
    const { ApiError } = await import('@/integrations/runtime/generated.ts');
    env.setSend(async () => { throw new ApiError(409, 'conflict', 'media lifecycle changed', '', { status: 'conflict' }); });
    await submitOccurrenceMediaEdit(captureOccurrenceMediaEdit(session.occurrenceMediaPort, env.current(), request('swap')));
    await vi.waitFor(() => expect(session.getState().status).toBe('conflict'));
    const [stored] = await env.outboxes.list(scope);
    await session.dispose();
    const reopened = await env.mount();
    await reopened.recover(stored.ownerId);
    expect(reopened.getState().status).toBe('conflict');
    expect((await env.outboxes.list(scope))[0].intents).toEqual(stored.intents);
    expect(env.requests).toHaveLength(1);
    expect(env.reads).toHaveBeenCalledTimes(2);
    await reopened.dispose();
  });
});
