import { describe, expect, it, vi } from 'vitest';
import type { EditCommand } from '@/integrations/runtime/timeline-commit-types.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { environment, document, scope } from './__tests__/commitSessionEnvironment.ts';
import { captureClipScalarEdit, submitClipScalarEdit } from './clipScalarGesture.ts';
import { captureTrackLabelEdit, submitTrackLabelEdit } from './trackLabelGesture.ts';
import { GenericPatchRefusal } from './genericPatchCapture.ts';
import { copy } from './clipMovePrimitives.ts';
import { acceptedCommit, fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { stableOutputIdentity } from '../data/shotComposition.ts';

const patch = (hold = 2.123456789): TimelinePatch => ({ version: 1, operations: [
  { op: 'track.update', target: 'V1', payload: { label: '', mode: 'merge' } },
  { op: 'clip.update', target: 'x', payload: { hold } },
] });

describe('native label/hold patch in the one durable session (fake transport)', () => {
  it('enqueues one payload, previews once, recovers the exact lost-ACK batch and sends one inverse', async () => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('lost');
    const input = patch();
    const current = copy(env.current());
    const captured = session.genericPatchPort.capture({ patch: input, current: env.current() });
    const original = copy(captured);
    input.operations[0].payload!.label = 'late caller mutation';
    const finished = session.genericPatchPort.finish(captured);
    session.genericPatchPort.submit(finished);
    expect(env.previews).toHaveBeenCalledExactlyOnceWith(finished.preview);
    expect(captured).toEqual(original);
    expect(env.current()).toEqual(current);
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(env.commits()).toHaveLength(1);
    const request = copy(env.commits()[0]);
    expect(request.body!.commands).toEqual(finished.commands);
    expect(finished.commands.map((command) => command.op)).toEqual(['track.set', 'clip.set']);
    expect(finished.commands[0].args).toEqual({ values: { label: '' }, clear: [] });
    expect(finished.commands[1].args).toEqual({ values: { hold: 2.123456789 }, clear: [] });
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toEqual(finished.commands);
    expect(stored.pending!.request.key).toBe(request.key);
    await session.dispose();
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    const capture = vi.spyOn(reopened.genericPatchPort, 'capture');
    await reopened.recover(stored.ownerId);
    await reopened.flush();
    expect(capture).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(2);
    expect(env.commits()[1]).toEqual(request);
    expect(env.current().config.tracks![0].label).toBe('');
    expect(env.current().config.clips[0]).toMatchObject({ hold: 2.123456789, app: { opaque: null }, text: { content: 'keep' } });
    expect(reopened.getState().canUndo).toBe(true);
    await reopened.undo();
    await reopened.flush();
    expect(env.commits()).toHaveLength(3);
    expect(env.commits()[2].body!.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1',
      select: null, args: { publications: ['p1'] } }]);
    expect(env.current().config.clips[0]).toMatchObject({ hold: 1, app: { opaque: null }, text: { content: 'keep' } });
    expect(reopened.getState().canUndo).toBe(false);
    expect(env.calls.filter((call) => call.method !== 'GET' && call.path !== '/v1/handshake')).toEqual(env.commits());
    await reopened.dispose();
  });

  it('keeps original sequential guards when a predecessor ACK arrives before finish', async () => {
    const env = await environment();
    const session = await env.mount();
    const paused = env.pause();
    submitTrackLabelEdit(captureTrackLabelEdit(session.trackLabelPort, env.current(), 'V1'), { values: { label: 'A' }, clear: [] });
    const captured = session.genericPatchPort.capture({ patch: patch(3.987654321), current: env.current() });
    const original = copy(captured);
    expect(captured.capture.commands[0].expect!['parent/track:V1::label']).toEqual({ state: 'present', value: 'A' });
    paused.resolve();
    await session.flush();
    env.setFault('lost');
    session.genericPatchPort.submit(session.genericPatchPort.finish(captured));
    await vi.waitFor(() => expect(session.getState().status).toBe('retry'));
    expect(env.commits()[1].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1', commands: captured.capture.commands });
    expect(captured).toEqual(original);
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    const reopened = await env.mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(stored.ownerId);
    expect(env.commits()[2]).toEqual(env.commits()[1]);
    expect(env.current().config.clips[0].hold).toBe(3.987654321);
    await reopened.dispose();
  });

  it('preserves disjoint remote state while finishing original claims and undoing the batch', async () => {
    const env = await environment();
    const session = await env.mount();
    const captured = session.genericPatchPort.capture({ patch: patch(), current: env.current() });
    const remote = await env.external((raw) => { raw.parent_revision.payload.independent = { keep: [null, false, 0] }; });
    session.observe(remote);
    await vi.waitFor(() => expect(env.projected).toHaveLength(1));
    session.genericPatchPort.submit(session.genericPatchPort.finish(captured));
    await session.flush();
    expect(env.projected.at(-1)!.canonicalDocument.parent_revision.payload.independent).toEqual({ keep: [null, false, 0] });
    await session.undo();
    await session.flush();
    expect(env.projected.at(-1)!.canonicalDocument.parent_revision.payload.independent).toEqual({ keep: [null, false, 0] });
    await session.dispose();
  });

  it.each(['capture', 'finish'] as const)('fences a newer local generation after %s', async (stage) => {
    const env = await environment();
    const session = await env.mount();
    env.setFault('unavailable');
    const captured = session.genericPatchPort.capture({ patch: patch(), current: env.current() });
    const finished = stage === 'finish' ? session.genericPatchPort.finish(captured) : undefined;
    submitClipScalarEdit(captureClipScalarEdit(session.clipScalarPort, env.current(), 'x'), { values: { hold: 4 }, clear: [] });
    expect(() => finished ? session.genericPatchPort.submit(finished) : session.genericPatchPort.finish(captured)).toThrow('changed');
    await session.dispose();
    const [stored] = await env.outboxes.list(scope);
    expect(stored.intents).toHaveLength(1);
    expect((stored.intents[0].payload as unknown as { commands: EditCommand[] }).commands).toHaveLength(1);
  });

  it('refuses all mixed intentions and a native second-member failure before preview or append', async () => {
    const raw = document();
    (raw.parent_revision.payload.clips as Array<Record<string, unknown>>)[0].app = { astrid: { for: 2 } };
    raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
    const env = await environment(raw);
    const session = await env.mount();
    const before = copy(env.current());
    const stored = await env.outboxes.list(scope);
    for (const input of [patch(), { version: 1, operations: [...patch().operations,
      { op: 'project-data.write', target: 'extension', payload: { value: 1 } }] } as TimelinePatch]) {
      try {
        session.genericPatchPort.capture({ patch: input, current: env.current() });
        expect.fail('unsupported patch accepted');
      } catch (error) {
        expect(error).toBeInstanceOf(GenericPatchRefusal);
        expect((error as GenericPatchRefusal).intentions).toHaveLength(input.operations.length);
      }
    }
    expect(env.current()).toEqual(before);
    expect(env.previews).not.toHaveBeenCalled();
    expect(await env.outboxes.list(scope)).toEqual(stored);
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });

  it('refuses stale versions, ambiguous selection and a forged occurrence owner atomically', async () => {
    const env = await environment();
    const session = await env.mount();
    const before = copy(env.current());
    const stored = await env.outboxes.list(scope);
    expect(() => session.genericPatchPort.capture({ patch: { ...patch(), version: 2 }, current: env.current() })).toThrow('stale');
    const duplicate = copy(before);
    duplicate.resolvedConfig.clips.push(copy(duplicate.resolvedConfig.clips[0]));
    expect(() => session.genericPatchPort.capture({ patch: patch(), current: duplicate })).toThrow('one raw clip');
    const forged = copy(before);
    forged.resolvedConfig.clips[0].id = 'occ-0:x';
    forged.resolvedConfig.clips[0].app = { canonical: { ownerRef: 'occurrence:occ-0', clipRef: 'occurrence:occ-0/clip:x' } };
    const input: TimelinePatch = { version: 1, operations: [patch().operations[0],
      { op: 'clip.update', target: 'occ-0:x', payload: { hold: 2 } }] };
    expect(() => session.genericPatchPort.capture({ patch: input, current: forged })).toThrow('identity occ-0');
    expect(env.current()).toEqual(before);
    expect(await env.outboxes.list(scope)).toEqual(stored);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });

  it('binds a validated occurrence and keeps its shared sibling isolated', async () => {
    const raw = acceptedCommit({ revision_id: 'r0', publication_id: 'p0' },
      { revision_id: 'initial', publication_id: 'initial' }, { children: true }).data.canonical_document;
    const internal = raw.internal_timeline_revisions[0];
    internal.payload.tracks = [{ id: 'child-lane', kind: 'visual' }];
    (internal.payload.clips as Array<Record<string, unknown>>)[0].track = 'child-lane';
    internal.content_digest = fixtureDigest(internal.payload);
    raw.dependency_manifest.internal_timelines[0].content_digest = internal.content_digest;
    const env = await environment(raw);
    const session = await env.mount();
    const current = copy(env.current());
    const canonical = { ownerRef: 'occurrence:occ-0', clipRef: 'occurrence:occ-0/clip:child-title',
      rawClipId: 'child-title', occurrenceId: 'occ-0', projectId: scope.projectId, parentDocumentId: scope.timelineId,
      shotId: 'shot-1', revisionId: 'shot-r1', internalTimelineRevisionId: internal.revision_id,
      outputIdentity: stableOutputIdentity(scope.projectId, scope.timelineId, 'occ-0') };
    current.resolvedConfig.clips.push({ id: 'occ-0:child-title', at: 0, hold: 1, track: 'child-lane', app: { canonical } });
    const input: TimelinePatch = { version: 1, operations: [patch().operations[0],
      { op: 'clip.update', target: 'occ-0:child-title', payload: { hold: 0.5123456789 } }] };
    const basis = session.genericPatchPort.capture({ patch: input, current });
    const finished = session.genericPatchPort.finish(basis);
    expect(finished.commands[1].select).toBe('occurrence:occ-0/clip:child-title');
    expect(finished.commands[1].args).toEqual({ values: { hold: 0.5123456789 }, clear: [] });
    expect(Object.keys(basis.capture.bundle.shots).some((key) => key.startsWith('shot-placement-'))).toBe(true);
    const sibling = basis.capture.bundle.placements[1].shot_id as string;
    expect(basis.capture.bundle.shots[sibling].internal_timeline).toEqual(internal.payload);
    expect(basis.capture.bundle.placements[0].shot_id).not.toBe(sibling);
    canonical.revisionId = 'stale-shot';
    expect(() => session.genericPatchPort.capture({ patch: input, current })).toThrow('matching raw clip owner');
    expect(finished.commands[1]).toEqual(basis.capture.commands[1]);
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });

  it('refuses changed second-member guards before enqueue and rejects altered prepared previews', async () => {
    const env = await environment();
    const session = await env.mount();
    const basis = session.genericPatchPort.capture({ patch: patch(), current: env.current() });
    const finished = session.genericPatchPort.finish(basis);
    expect(() => session.genericPatchPort.submit({ ...finished, preview: patch(99) })).toThrow('exact combined preview');
    const remote = await env.external((raw) => { (raw.parent_revision.payload.clips as Array<Record<string, unknown>>)[0].hold = 7; });
    session.observe(remote);
    await vi.waitFor(() => expect(env.projected).toHaveLength(1));
    expect(() => session.genericPatchPort.finish(basis)).toThrow('original capture');
    expect(() => session.genericPatchPort.submit(finished)).toThrow('changed');
    expect(env.previews).not.toHaveBeenCalled();
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    expect(env.commits()).toHaveLength(0);
    await session.dispose();
  });

  it('keeps bundle/outbox unchanged on preview failure and permits the exact prepared retry', async () => {
    const env = await environment();
    const session = await env.mount();
    const basis = session.genericPatchPort.capture({ patch: patch(), current: env.current() });
    const finished = session.genericPatchPort.finish(basis);
    const stored = await env.outboxes.list(scope);
    env.previews.mockImplementationOnce(() => { throw new Error('preview failed'); });
    expect(() => session.genericPatchPort.submit(finished)).toThrow('preview failed');
    expect(await env.outboxes.list(scope)).toEqual(stored);
    expect(session.genericPatchPort.capture({ patch: patch(), current: env.current() }).capture).toEqual(basis.capture);
    expect(env.commits()).toHaveLength(0);
    session.genericPatchPort.submit(finished);
    await session.flush();
    expect(env.commits()).toHaveLength(1);
    await session.dispose();
  });
});
