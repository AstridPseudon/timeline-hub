import { describe, expect, it, vi } from 'vitest';
import type { ClipSetParamsArgs, JSON, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { WorkspaceClient } from '@/integrations/runtime/generated.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { document, environment, scope } from './__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from './clipParamsGesture.ts';
import { selectedParamsCommand } from './clipParamsCapture.ts';
import type { TimelineCommandBasis } from '../data/DataProvider.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import { captureClipMove, submitClipMove } from './semanticGestures.ts';

const selected = { packId: 'test_pack', id: 'reveal', kind: 'effect', revision: `sha256:${'1'.repeat(64)}` };
function retained(version = 1, maximum = 10) {
  // Synthetic read-port/transport specimens. No native build/custody or schema-validation claim.
  const bytes = Buffer.from(JSON.stringify({ schema: { properties: { seed: { maximum } } } }));
  const digest = fixtureDigest({ version, maximum });
  const descriptor = { object_id: digest, digest, size: bytes.length, media_type: 'application/json' as const };
  const snapshot: VerifiedDocumentObject = { ...descriptor, bytes_base64: bytes.toString('base64') };
  const content = { schema: 'astrid.project-pack/v1', source_binding_key: 'project-packs', pack_id: selected.packId,
    relative_manifest: `${scope.realmId}/${scope.projectId}/packs/${selected.packId}/pack.yaml`,
    admissions: [{ id: selected.id, kind: selected.kind, revision: selected.revision, snapshot_object: descriptor }] };
  const pin = { document_id: 'retained-pack', version, content_digest: fixtureDigest(content) };
  const verified: VerifiedDocument = { pin, document: {
    document_id: pin.document_id, project_id: scope.projectId, kind: 'astrid.project-pack', version, content } };
  return { pin, verified, snapshot };
}
const edit = (pin = retained().pin): ClipSetParamsArgs => ({ values: { seed: 8 }, clear: [], schema_source: pin });
const payload = (value: unknown) => value as { commands: { args: ClipSetParamsArgs }[]; after: null;
  selectedParams: { basis: object; schema_inputs: unknown; realm_id: string } };

async function setup() {
  const f = retained();
  const raw = document();
  for (const rows of [raw.parent_revision.payload.clips, (raw.parent_revision.payload.config as { clips: object[] }).clips]) {
    Object.assign((rows as object[])[0], { clipType: 'text', elementRef: selected, params: { seed: 4, remove: null, opaque: [null, false, {}] } });
  }
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const env = await environment(raw, (before, command) => {
    // A deliberately synthetic server acceptance. App never executes this function.
    const next = structuredClone(before);
    const args = command.args as ClipSetParamsArgs;
    const rows = next.parent_revision.payload.clips as { params: Record<string, JSON> }[];
    rows[0].params = { ...rows[0].params, ...structuredClone(args.values) };
    for (const key of args.clear) delete rows[0].params[key];
    (next.parent_revision.payload.config as { clips: unknown }).clips = structuredClone(rows);
    return next;
  });
  const reads = {
    getProjectVerifiedDocument: vi.fn<WorkspaceClient['getProjectVerifiedDocument']>(async () => f.verified),
    getProjectVerifiedDocumentObject: vi.fn<WorkspaceClient['getProjectVerifiedDocumentObject']>(async () => f.snapshot),
    getDocument: vi.fn(),
  };
  let current = env.current();
  const project = vi.fn(async (basis: TimelineCommandBasis, _previews: TimelinePatch[]) => {
    const parent = basis.canonicalDocument.parent_revision.payload;
    current = await buildTimelineData({ ...parent.config as object, clips: parent.clips } as never,
      { assets: {} }, undefined, 1, undefined, { projectId: scope.projectId, timelineId: scope.timelineId,
        headRevisionId: basis.head.revisionId, headPublicationId: basis.head.publicationId });
  });
  const states: string[] = [];
  const mount = (initial = env.initial) => createTimelineCommandSession({ scope, initial, outboxes: env.outboxes,
    send: (request, key) => env.provider.commitTimeline(request, key), preview: env.previews, project,
    changed: (state) => states.push(state.status), paramReadClient: reads });
  const session = await mount();
  const capture = () => captureClipParamsEdit(session.clipParamsPort, current, 'x');
  const move = (at: number) => submitClipMove(captureClipMove(session.port, current, 'x'), at);
  return { env, f, reads, project, states, mount, session, capture, move };
}

describe('selected PARAM server authority staging (synthetic normal-port transport)', () => {
  it('persists exact literal draft/clear/pin/inputs, shows PENDING and obtains after-state only at ACK', async () => {
    const { env, f, reads, project, states, session, capture } = await setup();
    const pause = env.pause();
    const captured = capture();
    const inputs = await session.clipParamsPort.prefetch(captured.basis, f.pin);
    const args = { ...edit(f.pin), values: { seed: 8, literal: [null, false, '', {}, 'ƒ(16)'] }, clear: ['remove'] };
    const original = structuredClone(args);
    submitClipParamsEdit(captured, args);
    args.values.seed = 16;
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    expect(states).toContain('pending');
    expect(session.getState()).toMatchObject({ status: 'pending', error: expect.stringContaining('PENDING') });
    expect(env.previews).not.toHaveBeenCalled();
    expect(project).not.toHaveBeenCalled();
    const [saved] = await env.outboxes.list(scope);
    expect(payload(saved.intents[0].payload)).toMatchObject({ after: null,
      commands: [{ args: original }], selectedParams: { basis: captured.basis,
        schema_inputs: inputs.schema_inputs, realm_id: scope.realmId } });
    expect(env.commits()[0].body!.commands).toEqual([selectedParamsCommand('parent/clip:x', original)]);
    expect(env.commits()[0].body).not.toHaveProperty('schema_inputs');
    expect(env.commits()[0].body).not.toHaveProperty('realm_id');
    expect(reads.getDocument).not.toHaveBeenCalled();
    pause.resolve();
    await session.flush();
    expect(project).toHaveBeenCalledTimes(1);
    expect(project.mock.calls[0][0].canonicalDocument.parent_revision.payload.clips[0].params).toEqual({
      seed: 8, literal: original.values.literal, opaque: [null, false, {}] });
    expect(session.getState().status).toBe('saved');
    await session.dispose();
  });

  it.each(['validation', 'refused', 'conflict'] as const)('retains raw16 and the ordinary suffix on typed %s refusal', async (fault) => {
    const { env, f, project, session, capture } = await setup();
    const pause = env.pause();
    env.setFault(fault);
    const args = { ...edit(f.pin), values: { seed: 16 } };
    submitClipParamsEdit(capture(), args);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    env.move(session, 5);
    pause.resolve();
    await expect(session.flush()).rejects.toThrow();
    expect(session.getState().status).toBe(fault === 'conflict' ? 'conflict' : 'error');
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(2);
    expect(payload(saved.intents[0].payload).commands[0].args).toEqual(args);
    expect(saved.intents[1].payload).toMatchObject({ commands: [{ op: 'clip.move', args: { on: 5 } }] });
    expect(project).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(1);
    await session.dispose();
  });

  it('reloads the exact request/key and V1 inputs after V2/removal, then sends the original ordinary suffix', async () => {
    const { env, f, reads, project, mount, session, capture } = await setup();
    const captured = capture();
    await session.clipParamsPort.prefetch(captured.basis, f.pin);
    env.setFault('lost');
    submitClipParamsEdit(captured, edit(f.pin));
    await expect(session.flush()).rejects.toThrow('lost acknowledgement');
    const [before] = await env.outboxes.list(scope);
    const original = structuredClone(before.pending!.request);
    env.move(session, 5);
    await session.dispose();
    reads.getDocument.mockResolvedValueOnce(retained(2, 20).verified.document).mockResolvedValueOnce(null);
    reads.getProjectVerifiedDocument.mockRejectedValue(new Error('No recapture on reopen'));
    const reopened = await mount();
    await reopened.recover(before.ownerId);
    expect(env.commits()[1].key).toBe(original.key);
    expect(JSON.stringify(env.commits()[1].body)).toBe(original.body);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ op: 'clip.move', args: { on: 5 } }] });
    expect(reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(1);
    expect(reads.getDocument).not.toHaveBeenCalled();
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0]).toMatchObject({ at: 5, params: { seed: 8 } });
    expect(reopened.getState().status).toBe('saved');
    await reopened.undo();
    await reopened.flush();
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0]).toMatchObject({ at: 1, params: { seed: 8 } });
    await reopened.dispose();
  });

  it('supports a selected ACK, ordinary capture after ACK, and the native inverse request', async () => {
    const { env, f, project, session, capture, move } = await setup();
    submitClipParamsEdit(capture(), edit(f.pin));
    await session.flush();
    move(5);
    await session.flush();
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0]).toMatchObject({ at: 5, params: { seed: 8 } });
    await session.undo();
    await session.flush();
    await session.undo();
    await session.flush();
    expect(env.commits()[3].body!.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: ['p1'] } });
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(4);
    await session.dispose();
  });

  it('submits a new selected capture on an already accepted ordinary closure', async () => {
    const { env, f, project, session, capture, move } = await setup();
    move(5);
    await session.flush();
    const captured = capture();
    expect(captured.basis.acceptedBasisAvailable).toBe(true);
    submitClipParamsEdit(captured, edit(f.pin));
    await session.flush();
    expect(env.commits()[1].body).toMatchObject({ base_revision_id: 'r1', base_publication_id: 'p1',
      commands: [{ op: 'clip.set-params', args: edit(f.pin) }] });
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0]).toMatchObject({ at: 5, params: { seed: 8 } });
    await session.dispose();
  });

  it('keeps a selected draft over unacknowledged work unsent through ACK and reload', async () => {
    const { env, f, mount, session, capture } = await setup();
    const pause = env.pause();
    env.move(session, 5);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    const captured = capture();
    submitClipParamsEdit(captured, edit(f.pin));
    pause.resolve();
    await expect(session.flush()).rejects.toThrow('accepted original basis');
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].basis).toHaveProperty('after');
    expect(payload(saved.intents[0].payload).selectedParams.basis).toEqual(captured.basis);
    await session.dispose();
    const reopened = await mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(saved.ownerId);
    expect(reopened.getState()).toMatchObject({ status: 'pending', error: expect.stringContaining('unsent draft preserved') });
    expect(env.commits()).toHaveLength(1);
    expect((await env.outboxes.list(scope))[0].intents[0].payload).toEqual(saved.intents[0].payload);
    await reopened.dispose();
  });

  it('fences late reads and never refreshes the original pin', async () => {
    const { env, f, reads, session, capture } = await setup();
    const captured = capture();
    await session.clipParamsPort.prefetch(captured.basis, f.pin);
    await expect(session.clipParamsPort.prefetch(captured.basis, retained(2, 20).pin)).rejects.toThrow('cannot refresh');
    expect(() => submitClipParamsEdit(captured, edit(retained(2, 20).pin))).toThrow('original retained');
    let release!: () => void;
    reads.getProjectVerifiedDocumentObject.mockImplementationOnce(async () => {
      await new Promise<void>((resolve) => { release = resolve; });
      return f.snapshot;
    });
    const loading = session.clipParamsPort.prefetch(captured.basis, f.pin);
    const refusal = expect(loading).rejects.toThrow('capture changed');
    await vi.waitFor(() => expect(release).toBeDefined());
    session.clipParamsPort.invalidatePrefetch();
    release();
    await refusal;
    expect(env.commits()).toHaveLength(0);
    expect(env.previews).not.toHaveBeenCalled();
    await session.dispose();
  });

  it('passes schema-semantic errors unchanged to the provider and guards own JSON keys', async () => {
    const { env, f, session, capture } = await setup();
    const values = JSON.parse('{"seed":16,"__proto__":{"polluted":true},"constructor":null,"tuple":["wrong"]}');
    env.setFault('validation');
    submitClipParamsEdit(capture(), { values, clear: ['toString'], schema_source: f.pin });
    await expect(session.flush()).rejects.toThrow();
    const wire = env.commits()[0].body!.commands[0].args as ClipSetParamsArgs;
    expect(Object.keys(wire.values)).toEqual(Object.keys(values));
    expect(wire.values.__proto__).toEqual({ polluted: true });
    expect(Object.prototype).not.toHaveProperty('polluted');
    expect(() => selectedParamsCommand('parent/clip:x', { values, clear: ['__proto__'], schema_source: f.pin })).toThrow('literal values');
    expect(() => selectedParamsCommand('parent/clip:x', { values: { x: Infinity }, clear: [], schema_source: f.pin })).toThrow('finite JSON');
    await session.dispose();
  });
});
