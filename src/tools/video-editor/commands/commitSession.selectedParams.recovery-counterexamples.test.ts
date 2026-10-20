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
  return { env, f, reads, project, states, mount, session, capture, move };
}

describe('independent selected authority review counterexamples', () => {
  it('projects an accepted selected inverse while its selected suffix stays permanently unsent', async () => {
    const { env, f, session, capture, project } = await setup();
    submitClipParamsEdit(capture(), edit(f.pin));
    await session.flush();
    const pause = env.pause();
    const undoing = session.undo();
    await vi.waitFor(() => expect(env.commits()).toHaveLength(2));
    const pendingCapture = capture();
    expect(pendingCapture.basis.acceptedBasisAvailable).toBe(false);
    submitClipParamsEdit(pendingCapture, { ...edit(f.pin), values: { seed: 9 } });
    pause.resolve();
    await undoing;
    await expect(session.flush()).rejects.toThrow('accepted original basis');
    const [saved] = await env.outboxes.list(scope);
    expect(saved.accepted!.head.publicationId).toBe('p2');
    expect((saved.accepted!.value as any).canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(4);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ args: { values: { seed: 9 } } }],
      selectedParams: { basis: { acceptedBasisAvailable: false } } });
    expect(env.commits()).toHaveLength(2);
    await session.dispose();
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(4);
  });

  it('recovery retains accepted selected params when only the refused ordinary suffix remains', async () => {
    const { env, f, session, capture, project, mount } = await setup();
    const send = env.provider.commitTimeline.bind(env.provider);
    vi.spyOn(env.provider, 'commitTimeline').mockImplementation(async (request, key) => {
      const result = await send(request, key);
      if (request.commands[0].op === 'clip.set-params') env.setFault('conflict');
      return result;
    });
    const pause = env.pause();
    submitClipParamsEdit(capture(), edit(f.pin));
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    env.move(session, 5);
    pause.resolve();
    await expect(session.flush()).rejects.toThrow();
    const [saved] = await env.outboxes.list(scope);
    expect(saved.accepted!.head.publicationId).toBe('p1');
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toMatchObject({ commands: [{ op: 'clip.move' }] });
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(8);
    await session.dispose();
    const reopened = await mount(await env.provider.loadTimelineCommandBasis(scope.timelineId));
    await reopened.recover(saved.ownerId);
    expect(reopened.getState().status).toBe('conflict');
    expect((await env.outboxes.list(scope))[0].intents).toEqual(saved.intents);
    await reopened.dispose();
    expect(project.mock.calls.at(-1)![0].canonicalDocument.parent_revision.payload.clips[0].params.seed).toBe(8);
  });

  it('canceling an ordinary tail keeps the remaining unsent selected draft visibly pending', async () => {
    const { env, f, session, capture } = await setup();
    const pause = env.pause();
    env.move(session, 5);
    await vi.waitFor(() => expect(env.commits()).toHaveLength(1));
    submitClipParamsEdit(capture(), edit(f.pin));
    env.move(session, 7);
    pause.resolve();
    await expect(session.flush()).rejects.toThrow('accepted original basis');
    await session.undo();
    const [saved] = await env.outboxes.list(scope);
    expect(saved.intents).toHaveLength(1);
    expect(saved.intents[0].payload).toMatchObject({ selectedParams: { basis: { acceptedBasisAvailable: false } } });
    expect(env.commits()).toHaveLength(1);
    const state = session.getState();
    await session.dispose();
    expect(state).toMatchObject({ status: 'pending', error: expect.stringContaining('unsent draft preserved') });
  });

  it('a fresh selected capture after explicitly canceling the inverse suffix uses the accepted closure', async () => {
    const { env, f, session, capture } = await setup();
    submitClipParamsEdit(capture(), edit(f.pin));
    await session.flush();
    const pause = env.pause();
    const undoing = session.undo();
    await vi.waitFor(() => expect(env.commits()).toHaveLength(2));
    submitClipParamsEdit(capture(), { ...edit(f.pin), values: { seed: 9 } });
    pause.resolve();
    await undoing;
    await expect(session.flush()).rejects.toThrow('accepted original basis');
    await session.undo();
    expect((await env.outboxes.list(scope))[0].intents).toHaveLength(0);
    expect(session.getState().status).toBe('saved');
    const fresh = capture();
    await session.dispose();
    expect(fresh.basis).toMatchObject({ acceptedBasisAvailable: true,
      bundle: { parent: { clips: [{ params: { seed: 4 } }] } } });
  });
});
