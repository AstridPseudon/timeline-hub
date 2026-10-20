import { describe, expect, it, vi } from 'vitest';
import type { CanonicalDocument, CommitRequest, EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import type { TimelineCommandBasis, TimelineCommitResult } from '../data/DataProvider.ts';
import type { TimelineConfig } from '../types/index.ts';
import { assembleTimelineData, type TimelineData } from '../lib/timeline-data.ts';
import { compileTimelinePatch } from '../lib/timeline-patch.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { captureClipScalarEdit, submitClipScalarEdit, type ClipScalarArgs } from './clipScalarGesture.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from './trackLabelGesture.ts';
import { environment, scope } from './__tests__/commitSessionEnvironment.ts';
import { AuthoredState, copy } from './clipMovePrimitives.ts';
import fixture from './fixtures/recipe_m2_app_clip_scalar_fields.json';

const golden = fixture;
const head = { revisionId: 'r0', publicationId: 'p0' };
const holdRef = 'occurrence:f2-occurrence/clip:f2-agent-clip';
const assetRef = 'occurrence:f2-occurrence/clip:f2-agent-clear-clip';
const transitionRef = 'parent/clip:f2-transition-clip';
const cases: Array<[string, ClipScalarArgs]> = [
  [holdRef, { values: { hold: 4 }, clear: [] }],
  [assetRef, { values: {}, clear: ['asset'] }],
  [transitionRef, { values: {}, clear: ['transition'] }],
];
const owner = (ref: string) => ref.slice(0, ref.lastIndexOf('/')) as 'parent' | `occurrence:${string}`;
const displayId = (ref: string) => owner(ref) === 'parent' ? ref.split('/clip:')[1] : `${owner(ref).slice(11)}:${ref.split('/clip:')[1]}`;

function rawDocument(): CanonicalDocument {
  const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
    { revision_id: 'initial', publication_id: 'initial' }, { children: true }).data.canonical_document;
  raw.parent_revision.payload = { ...copy(golden.bundle.parent), occurrences: golden.bundle.placements.map((placement) => ({
    ...copy(placement), shot_id: 'shot-1', shot_revision_id: 'shot-r1',
  })) };
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const internal = raw.internal_timeline_revisions[0];
  internal.payload = copy(Object.values(golden.bundle.shots)[0].internal_timeline);
  internal.content_digest = fixtureDigest(internal.payload);
  raw.dependency_manifest.internal_timelines[0].content_digest = internal.content_digest;
  return raw;
}

// A display fixture, not a replacement for the canonical composition projector.
function display(raw: CanonicalDocument, pin = head): TimelineData {
  const parent = raw.parent_revision.payload;
  const clips = copy(parent.clips) as TimelineConfig['clips'];
  for (const occurrence of parent.occurrences as Array<Record<string, JSON>>) {
    const shot = raw.shot_revisions.find((image) => image.revision_id === occurrence.shot_revision_id)!;
    const internal = raw.internal_timeline_revisions.find((image) => image.revision_id === shot.internal_timeline_revision_id)!;
    for (const clip of internal.payload.clips as TimelineConfig['clips']) {
      clips.push({ ...copy(clip), track: occurrence.track as string, id: `${occurrence.occurrence_id}:${clip.id}`,
        app: { ...clip.app, canonical: { clipRef: `occurrence:${occurrence.occurrence_id}/clip:${clip.id}` } } });
    }
  }
  const config = { ...copy(parent.config as object), output: { fps: 30, resolution: '1920x1080' }, clips } as TimelineConfig;
  return assembleTimelineData({ config, configVersion: 1, head: { ...scope,
    headRevisionId: pin.revisionId, headPublicationId: pin.publicationId }, registry: { assets: {} },
  resolvedConfig: { ...config, tracks: config.tracks ?? [], registry: {} }, output: config.output, assetMap: {} });
}

async function setup(raw = rawDocument()) {
  const storage = await environment();
  let current = display(raw);
  const initial: TimelineCommandBasis = { head, canonicalDocument: raw };
  const requests: Array<{ body: string; key: string }> = [];
  // Unit transport deliberately remains uncertain: no Runtime scalar acceptance is simulated.
  let send: (request: CommitRequest, key: string) => Promise<TimelineCommitResult> = async () => { throw new Error('unknown outcome'); };
  const project = vi.fn(async (basis, previews) => {
    current = display(basis.canonicalDocument, basis.head);
    for (const patch of previews) {
      const compiled = compileTimelinePatch(patch, current);
      if (!compiled.nextData) throw new Error('invalid recovered preview');
      current = compiled.nextData;
    }
  });
  const mount = (basis = initial) => createTimelineCommandSession({ scope, initial: basis, outboxes: storage.outboxes,
    send: (request, key) => { requests.push({ body: JSON.stringify(request), key }); return send(request, key); },
    preview: (patch) => {
      const compiled = compileTimelinePatch(patch, current);
      if (!compiled.nextData) throw new Error('invalid scalar preview');
      current = compiled.nextData;
    }, project, changed: () => {} });
  return { ...storage, initial, mount, requests, project, current: () => current,
    setSend: (next: typeof send) => { send = next; } };
}
const rawRow = (bundle: unknown, ref: string) => new AuthoredState(bundle as never).entity(ref)!;

describe('clip scalars in the existing durable session (unit transport only)', () => {
  it.each(cases)('captures original journey intent %s → previews → persists → reloads → retries exact bytes/key', async (ref, args) => {
    const env = await setup();
    const session = await env.mount();
    const before = copy(env.current().config);
    const id = displayId(ref);
    const sibling = copy(before.clips.find((clip) => clip.id === `shared-sibling:${ref.split('/clip:')[1]}`));
    const captured = captureClipScalarEdit(session.clipScalarPort, env.current(), id, owner(ref));
    const { command } = session.clipScalarPort.finish(captured.basis, args);
    submitClipScalarEdit(captured, args);
    const previewRow = env.current().config.clips.find((clip) => clip.id === id)!;
    for (const key of args.clear) {
      expect(previewRow).not.toHaveProperty(key);
      expect(env.current().resolvedConfig.clips.find((clip) => clip.id === id)).not.toHaveProperty(key);
    }
    if ('hold' in args.values) expect(previewRow.hold).toBe(4);
    expect(env.current().config.clips.map((clip) => clip.id)).toEqual(before.clips.map((clip) => clip.id));
    if (sibling) expect(env.current().config.clips.find((clip) => clip.id === sibling.id)).toEqual(sibling);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    const payload = stored.intents[0].payload as unknown as { commands: EditCommand[]; after: unknown };
    expect(payload.commands).toEqual([command]);
    const row = rawRow(payload.after, ref);
    const original = rawRow(captured.basis.bundle, ref);
    const expected = { ...original, ...args.values };
    for (const key of args.clear) delete expected[key];
    expect(row).toEqual(expected);
    expect(payload.commands[0]).toMatchObject({ select: ref, op: 'clip.set', args, bindings: { 'scalar.target': ref } });
    expect(stored.pending!.request.body).toBe(env.requests[0].body);
    expect(stored.pending!.request.key).toBe(env.requests[0].key);
    await session.dispose();
    const reopened = await env.mount();
    expect(reopened.getState().status).toBe('recovery');
    expect(env.requests).toHaveLength(1);
    await reopened.recover(stored.ownerId);
    expect(env.requests[1]).toEqual(env.requests[0]);
    const recovered = env.current().config.clips.find((clip) => clip.id === id)!;
    for (const key of args.clear) expect(recovered).not.toHaveProperty(key);
    if ('hold' in args.values) expect(recovered.hold).toBe(4);
    expect(JSON.parse(env.requests[0].body).commands).toEqual([command]);
    await reopened.dispose();
  });

  it.each(['absent', 'null', 'empty'] as const)('retains original %s and clears asset to ABSENT through recovery', async (state) => {
    const raw = rawDocument();
    const row = (raw.parent_revision.payload.clips as Array<Record<string, JSON>>)[0];
    if (state === 'absent') delete row.asset;
    else row.asset = state === 'null' ? null : '';
    const env = await setup(raw);
    const session = await env.mount();
    submitClipScalarEdit(captureClipScalarEdit(session.clipScalarPort, env.current(), row.id as string, 'parent'),
      { values: {}, clear: ['asset'] });
    expect(env.current().config.clips[0]).not.toHaveProperty('asset');
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const command = JSON.parse(env.requests[0].body).commands[0];
    expect(command.expect[`parent/clip:${row.id}::asset`]).toEqual(state === 'absent'
      ? { state: 'absent' } : { state: 'present', value: state === 'null' ? null : '' });
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const reopened = await env.mount();
    await reopened.recover(stored.ownerId);
    expect(env.current().config.clips[0]).not.toHaveProperty('asset');
    expect(env.requests[1]).toEqual(env.requests[0]);
    await reopened.dispose();
  });

  it('keeps B original guards and predecessor across A acknowledgement without refreshing capture', async () => {
    const env = await setup();
    const session = await env.mount();
    submitTrackLabelEdit(captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1'), { values: { label: 'A' }, clear: [] });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureClipScalarEdit(session.clipScalarPort, env.current(), displayId(assetRef), owner(assetRef));
    const original = copy(captured.basis);
    submitClipScalarEdit(captured, cases[1][1]);
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(2));
    const [stored] = await env.outboxes.list(scope);
    const suffix = copy(stored.intents[1]);
    expect(suffix.basis).toEqual({ after: stored.intents[0].id });
    const next = copy(env.initial.canonicalDocument);
    (next.parent_revision.payload.config as { tracks: Array<{ label: string }> }).tracks[0].label = 'A';
    next.parent_revision.revision_id = 'r1';
    env.setSend(async (request, key) => {
      if (request.commands[0].op !== 'track.set') throw new Error('unknown scalar outcome');
      const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' });
      response.data.canonical_document = next;
      return { accepted: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: next, response,
        receipt: { ...response.receipt, idempotency_key: key }, graph: {} };
    });
    await session.retry();
    const scalarRequest = env.requests.at(-1)!;
    expect(env.requests.slice(0, -1).every((request) => request.body === env.requests[0].body && request.key === env.requests[0].key)).toBe(true);
    expect(JSON.parse(scalarRequest.body)).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: (suffix.payload as { commands: unknown }).commands });
    expect(scalarRequest.key).not.toBe(env.requests[0].key);
    expect(captured.basis).toEqual(original);
    expect(env.current().config.clips.find((clip) => clip.id === displayId(assetRef))).not.toHaveProperty('asset');
    await session.dispose();
    const reopened = await env.mount({ head: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: next });
    await reopened.recover(stored.ownerId);
    expect(env.requests.at(-1)).toEqual(scalarRequest);
    expect(env.project.mock.calls.at(-1)![0].head).toEqual(head);
    await reopened.dispose();
  });

  it('finishes a capture after A acknowledgement with identical original claims and raw opaque bytes', async () => {
    const env = await setup();
    const session = await env.mount();
    submitTrackLabelEdit(captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1'), { values: { label: 'A' }, clear: [] });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const captured = captureClipScalarEdit(session.clipScalarPort, env.current(), displayId(assetRef), owner(assetRef));
    const original = session.clipScalarPort.finish(captured.basis, cases[1][1]).command;
    const next = copy(env.initial.canonicalDocument);
    (next.parent_revision.payload.config as { tracks: Array<{ label: string }> }).tracks[0].label = 'A';
    next.parent_revision.payload.opaque_after_capture = { keep: [null, 9] };
    next.parent_revision.revision_id = 'r1';
    env.setSend(async (request) => {
      if (request.commands[0].op !== 'track.set') throw new Error('unknown scalar outcome');
      const response = acceptedCommit({ revision_id: 'r1', publication_id: 'p1' }, { revision_id: 'r0', publication_id: 'p0' });
      response.data.canonical_document = next;
      return { accepted: { revisionId: 'r1', publicationId: 'p1' }, canonicalDocument: next, response,
        receipt: response.receipt, graph: {} };
    });
    await session.retry();
    expect(session.getState().status).toBe('saved');
    expect(session.clipScalarPort.finish(captured.basis, cases[1][1]).command).toEqual(original);
    submitClipScalarEdit(captured, cases[1][1]);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(JSON.parse(env.requests.at(-1)!.body)).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: [original] });
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents[0].payload).toMatchObject({ after: { parent: { opaque_after_capture: { keep: [null, 9] } } } });
    await session.dispose();
  });

  it('clears hold only when its source window survives, preserving speed and exact window leaves', async () => {
    const raw = rawDocument();
    const row = (raw.internal_timeline_revisions[0].payload.clips as Array<Record<string, JSON>>).find((clip) => clip.id === 'f2-agent-clip')!;
    Object.assign(row, { from: 1, to: 4, speed: 2 });
    const env = await setup(raw);
    const session = await env.mount();
    submitClipScalarEdit(captureClipScalarEdit(session.clipScalarPort, env.current(), displayId(holdRef), owner(holdRef)),
      { values: {}, clear: ['hold'] });
    const preview = env.current().config.clips.find((clip) => clip.id === displayId(holdRef))!;
    expect(preview).not.toHaveProperty('hold');
    expect(preview).toMatchObject({ from: 1, to: 4, speed: 2 });
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    const [stored] = await env.outboxes.list(scope);
    const after = rawRow((stored.intents[0].payload as { after: unknown }).after, holdRef);
    expect(after).not.toHaveProperty('hold');
    expect(after).toMatchObject({ from: 1, to: 4, speed: 2 });
    await session.dispose();
  });

  it('rejects wrong owners, stale claims and forged previews while preserving the local draft', async () => {
    const env = await setup();
    const session = await env.mount();
    const current = env.current();
    expect(() => captureClipScalarEdit(session.clipScalarPort, current, displayId(assetRef), 'parent')).toThrow('matching raw clip owner');
    const captured = captureClipScalarEdit(session.clipScalarPort, current, displayId(assetRef), owner(assetRef));
    const prepared = session.clipScalarPort.finish(captured.basis, cases[1][1]);
    expect(() => session.clipScalarPort.submit({ command: prepared.command, preview: { version: 1, operations: [
      { op: 'clip.update', target: displayId(assetRef), payload: { asset: null } },
    ] } })).toThrow('exact leaf-only preview');
    expect(env.current()).toBe(current);
    expect(env.requests).toHaveLength(0);
    const beforeArgs = copy(cases[1][1]);
    submitClipScalarEdit(captured, cases[1][1]);
    expect(() => submitClipScalarEdit(captured, cases[1][1])).toThrow('Timeline changed');
    expect(cases[1][1]).toEqual(beforeArgs);
    expect(env.current().config.clips.find((clip) => clip.id === displayId(assetRef))).not.toHaveProperty('asset');
    await session.dispose();
  });

  it('keeps unsupported hold-after-move intentions visibly refused without changing the draft', async () => {
    const raw = rawDocument();
    const row = (raw.internal_timeline_revisions[0].payload.clips as Array<Record<string, JSON>>).find((clip) => clip.id === 'f2-agent-clip')!;
    row.app = { astrid: { for: 3 } };
    const env = await setup(raw);
    const session = await env.mount();
    const current = env.current();
    const captured = captureClipScalarEdit(session.clipScalarPort, current, displayId(holdRef), owner(holdRef));
    expect(() => submitClipScalarEdit(captured, cases[0][1])).toThrow('does not support for');
    expect(env.current()).toBe(current);
    expect(env.requests).toHaveLength(0);
    await session.dispose();
  });
});
