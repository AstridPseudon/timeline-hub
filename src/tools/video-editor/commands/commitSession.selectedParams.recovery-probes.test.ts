import { describe, expect, it, vi } from 'vitest';
import type { ClipSetParamsArgs, JSON, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import type { WorkspaceClient } from '@/integrations/runtime/generated.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { document, environment, scope } from '@/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts';
import { createTimelineCommandSession } from '@/tools/video-editor/commands/commitSession.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from '@/tools/video-editor/commands/clipParamsGesture.ts';
import { selectedParamsCommand } from '@/tools/video-editor/commands/clipParamsCapture.ts';
import type { TimelineCommandBasis } from '@/tools/video-editor/data/DataProvider.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import { buildTimelineData } from '@/tools/video-editor/lib/timeline-data.ts';
import { captureClipMove, submitClipMove } from '@/tools/video-editor/commands/semanticGestures.ts';

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
  return { env, f, reads, project, states, mount, session, capture, move, current: () => current };
}


describe('independent neighboring lifecycle probes', () => {
  it.each(['selected', 'inverse'] as const)('recovers the accepted %s value after an intervening ordinary ACK and ordinary refusal', async (mode) => {
    const { env, f, session, capture, project, mount, move } = await setup();
    let pause = env.pause();
    let accepting: Promise<unknown>;
    if (mode === 'selected') {
      submitClipParamsEdit(capture(), edit(f.pin));
      accepting = session.flush();
    } else {
      pause.resolve();
      submitClipParamsEdit(capture(), edit(f.pin));
      await session.flush();
      pause = env.pause();
      accepting = session.undo();
    }
    const startCount = mode === 'selected' ? 1 : 2;
    await vi.waitFor(() => expect(env.commits()).toHaveLength(startCount));
    move(5);
    move(7);
    await vi.waitFor(async () => expect((await env.outboxes.list(scope))[0].intents).toHaveLength(3));
    const [before] = await env.outboxes.list(scope);
    // Trigger the refusal only after the first ordinary suffix has actually been accepted.
    const send = env.provider.commitTimeline.bind(env.provider);
    vi.spyOn(env.provider, 'commitTimeline').mockImplementation(async (request, key) => {
      const result = await send(request, key);
      if (request.commands[0].op === 'clip.move' && request.commands[0].args.on === 5) env.setFault('conflict');
      return result;
    });
    pause.resolve();
    if (mode === 'selected') await expect(accepting).rejects.toThrow('conflict');
    else await accepting;
    await expect(session.flush()).rejects.toThrow('conflict');
    expect(session.getState().status).toBe('conflict');
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toEqual(before.intents.at(-1)!.payload);
    expect((saved.accepted!.value as any).response.data.commands[0].op).toBe('clip.move');
    const seed = mode === 'selected' ? 8 : 4;
    expect((saved.accepted!.value as any).canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(seed);
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(seed);
    await session.dispose();
    const reopened = await mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(saved.ownerId);
    expect(reopened.getState().status).toBe('conflict');
    expect((await env.outboxes.list(scope))[0].intents).toEqual(saved.intents);
    const recoveredSeed = project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed;
    await reopened.dispose();
    expect(recoveredSeed).toBe(seed);
  });
});


describe('independent cancellation and new-capture positive control', () => {
  it('retains the original false basis across inverse ACK/reopen, cancels explicitly, then sends fresh selected and ordinary work on real acceptance', async () => {
    const { env, f, session, capture, project, mount, current, move } = await setup();
    submitClipParamsEdit(capture(), edit(f.pin));
    await session.flush();
    const pause = env.pause();
    const undoing = session.undo();
    await vi.waitFor(() => expect(env.commits()).toHaveLength(2));
    const captured = capture();
    const originalBasis = structuredClone(captured.basis);
    expect(captured.basis.acceptedBasisAvailable).toBe(false);
    await session.clipParamsPort.prefetch(captured.basis, f.pin);
    submitClipParamsEdit(captured, { ...edit(f.pin), values: { seed: 9 } });
    move(5);
    pause.resolve();
    await undoing;
    await expect(session.flush()).rejects.toThrow('accepted original basis');
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(2);
    expect((saved.intents[0].payload as any).selectedParams).toMatchObject({ basis: originalBasis,
      schema_inputs: [[f.verified, { [f.snapshot.object_id]: f.snapshot }]], realm_id: scope.realmId });
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(4);
    await session.dispose();
    const reopened = await mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(saved.ownerId);
    expect((await env.outboxes.list(scope))[0].intents).toEqual(saved.intents);
    expect(reopened.getState()).toMatchObject({ status: 'pending', canUndo: true,
      error: expect.stringContaining('unsent draft preserved') });
    expect(env.commits()).toHaveLength(2);
    await reopened.undo();
    expect((await env.outboxes.list(scope))[0].intents).toEqual(saved.intents.slice(0, 1));
    await reopened.undo();
    expect(reopened.getState().status).toBe('saved');
    const fresh = captureClipParamsEdit(reopened.clipParamsPort, current(), 'x');
    expect(fresh.basis).toMatchObject({ acceptedBasisAvailable: true,
      localBasis: { head: { revisionId: 'r2', publicationId: 'p2' } },
      bundle: { parent: { clips: [{ at: 1, params: { seed: 4 } }] } } });
    const nextPause = env.pause();
    const projections = project.mock.calls.length;
    submitClipParamsEdit(fresh, { ...edit(f.pin), values: { seed: 6 } });
    await vi.waitFor(() => expect(env.commits()).toHaveLength(3));
    expect(project).toHaveBeenCalledTimes(projections);
    expect(current().config.clips[0].params.seed).toBe(4);
    expect((await env.outboxes.list(scope))[0].intents[0].payload).toMatchObject({ after: null,
      commands: [{ args: { values: { seed: 6 }, schema_source: f.pin } }] });
    submitClipMove(captureClipMove(reopened.port, current(), 'x'), 5);
    nextPause.resolve();
    await reopened.flush();
    expect(env.commits()).toHaveLength(4);
    expect(env.commits()[2].body).toMatchObject({ base_revision_id: 'r2', base_publication_id: 'p2',
      commands: [{ op: 'clip.set-params', args: { values: { seed: 6 }, schema_source: f.pin } }] });
    expect(env.commits()[3].body).toMatchObject({ base_revision_id: 'r3', base_publication_id: 'p3',
      commands: [{ op: 'clip.move', args: { on: 5 }, expect: { 'parent/clip:x::at': { state: 'present', value: 1 } } }] });
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0]).toMatchObject({ at: 5, params: { seed: 6 } });
    expect(captured.basis).toEqual(originalBasis);
    expect(env.calls.every((call) => call.method === 'GET' || call.path.endsWith('/handshake') || call.path.endsWith('/commit'))).toBe(true);
    await reopened.dispose();
  });
});
