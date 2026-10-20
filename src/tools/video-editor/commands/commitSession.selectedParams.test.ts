import { describe, expect, it, vi } from 'vitest';
import type { DocumentPin, VerifiedDocument, VerifiedDocumentObject } from '@/integrations/runtime/timeline-commit-types.ts';
import { fixtureDigest } from '@/integrations/runtime/__tests__/timelineCommitFixture.ts';
import { captureClipParamsEdit, submitClipParamsEdit } from './clipParamsGesture.ts';
import { createTimelineCommandSession } from './commitSession.ts';
import { document, environment, scope } from './__tests__/commitSessionEnvironment.ts';

const selected = { packId: 'test_pack', id: 'reveal', kind: 'effect', revision: `sha256:${'1'.repeat(64)}` };
const edit = { values: { seed: 8 }, clear: [] };
const deferred = () => {
  let resolve!: () => void;
  const promise = new Promise<void>((done) => { resolve = done; });
  return { promise, resolve };
};

// Read-port specimens deliberately lack a valid portable build. Prefetch may
// forward these inputs; only native capture can validate them and enable PARAM.
function retained(version = 1, maximum = 10) {
  const bytes = Buffer.from(JSON.stringify({ maximum }));
  const descriptor = { object_id: fixtureDigest({ maximum }), digest: fixtureDigest({ maximum }),
    size: bytes.length, media_type: 'application/json' as const };
  const snapshot: VerifiedDocumentObject = { ...descriptor, bytes_base64: bytes.toString('base64') };
  const content = { schema: 'astrid.project-pack/v1', pack_id: selected.packId, source_binding_key: 'project-packs',
    relative_manifest: `${scope.realmId}/${scope.projectId}/packs/${selected.packId}/pack.yaml`,
    admissions: [{ id: 'other', kind: 'effect', revision: selected.revision,
      snapshot_object: { ...descriptor, object_id: `sha256:${'9'.repeat(64)}` } },
    { id: selected.id, kind: selected.kind, revision: selected.revision, snapshot_object: descriptor }] };
  const pin: DocumentPin = { document_id: 'original-pack', version, content_digest: fixtureDigest(content) };
  const verified: VerifiedDocument = { pin: structuredClone(pin), document: { document_id: pin.document_id,
    project_id: scope.projectId, kind: 'astrid.project-pack', version, content,
    created_at: '2026-10-19T00:00:00Z', updated_at: '2026-10-19T00:00:00Z' } };
  return { pin, verified, snapshot };
}
async function setup() {
  const raw = document();
  const clips = raw.parent_revision.payload.clips as Record<string, unknown>[];
  Object.assign(clips[0], { clipType: 'reveal', elementRef: structuredClone(selected), params: { seed: 4, opaque: [null, false] } });
  clips.push({ ...structuredClone(clips[0]), id: 'y' });
  raw.parent_revision.payload.config.clips = structuredClone(clips);
  raw.parent_revision.content_digest = fixtureDigest(raw.parent_revision.payload);
  const env = await environment(raw);
  const f = retained();
  const reads = {
    getProjectVerifiedDocument: vi.fn(async (_project: string, _pin: DocumentPin) => f.verified),
    getProjectVerifiedDocumentObject: vi.fn(async (_project: string, _pin: DocumentPin, _object: string) => f.snapshot),
    getDocument: vi.fn(),
  };
  const session = await createTimelineCommandSession({ scope, initial: env.initial, outboxes: env.outboxes,
    send: (request, key) => env.provider.commitTimeline(request, key),
    preview: env.previews, project: async () => {}, changed: () => {}, paramReadClient: reads });
  const captured = captureClipParamsEdit(session.clipParamsPort, env.current(), 'x');
  const outboxBefore = await env.outboxes.list(scope);
  return { env, f, reads, session, captured, outboxBefore };
}

describe('staged selected PARAM prefetch on the original session capture', () => {
  it('returns frozen native inputs with the original raw capture and exactly one selected object read', async () => {
    const { env, f, reads, session, captured, outboxBefore } = await setup();
    const original = structuredClone(captured.basis);
    const originalPin = structuredClone(f.pin);
    const pause = deferred();
    reads.getProjectVerifiedDocument.mockImplementationOnce(async () => { await pause.promise; return f.verified; });
    const loading = session.clipParamsPort.prefetch!(captured.basis, f.pin);
    // Neither UI normalization nor mutable caller arguments replace the target/pin.
    env.current().resolvedConfig.clips[0].elementRef = { ...selected, packId: 'ui-only' };
    f.pin.version = 2;
    pause.resolve();
    const inputs = await loading;
    expect(inputs.basis).toEqual(original);
    expect(inputs.schema_source).toEqual(originalPin);
    expect(inputs.realm_id).toBe(scope.realmId);
    expect(inputs.schema_inputs).toEqual([[f.verified, { [f.snapshot.object_id]: f.snapshot }]]);
    expect(inputs.schema_inputs[0][0]).not.toBe(f.verified);
    expect(Object.isFrozen(inputs.basis.bundle)).toBe(true);
    expect(Object.isFrozen(inputs.schema_source)).toBe(true);
    expect(Object.isFrozen(inputs.schema_inputs[0][1][f.snapshot.object_id])).toBe(true);
    expect(reads.getProjectVerifiedDocument).toHaveBeenCalledExactlyOnceWith(scope.projectId, originalPin);
    expect(reads.getProjectVerifiedDocumentObject).toHaveBeenCalledExactlyOnceWith(scope.projectId, originalPin, f.snapshot.object_id);
    expect(reads.getDocument).not.toHaveBeenCalled();
    expect(env.previews).not.toHaveBeenCalled();
    expect(await env.outboxes.list(scope)).toEqual(outboxBefore);
    await session.dispose();
  });

  it('does not bless read-port bytes as a schema or change the original selected-value refusal', async () => {
    const { env, f, session, captured, outboxBefore } = await setup();
    const original = structuredClone(captured.basis);
    await session.clipParamsPort.prefetch!(captured.basis, f.pin);
    expect(() => submitClipParamsEdit(captured, edit)).toThrow('exact schema_source and verified immutable inputs');
    expect(captured.basis).toEqual(original);
    expect(edit).toEqual({ values: { seed: 8 }, clear: [] });
    expect(session.getState().status).toBe('saved');
    expect(env.previews).not.toHaveBeenCalled();
    expect(await env.outboxes.list(scope)).toEqual(outboxBefore);
    await session.dispose();
  });

  it.each(['selection', 'invalid selection', 'local edit', 'head', 'close', 'cancel', 'new read'] as const)(
    'refuses a late A result after %s changes without installing inputs or losing the draft', async (change) => {
      const { env, f, reads, session, captured } = await setup();
      const pause = deferred();
      reads.getProjectVerifiedDocumentObject.mockImplementationOnce(async () => { await pause.promise; return f.snapshot; });
      const loading = session.clipParamsPort.prefetch!(captured.basis, f.pin);
      // Attach the assertion before allowing a rejection.
      const refusal = expect(loading).rejects.toThrow(/changed|unavailable/);
      await vi.waitFor(() => expect(reads.getProjectVerifiedDocumentObject).toHaveBeenCalledTimes(1));
      if (change === 'selection') captureClipParamsEdit(session.clipParamsPort, env.current(), 'y');
      if (change === 'invalid selection') expect(() => session.clipParamsPort.capture({ clipId: 'missing', current: env.current() })).toThrow();
      if (change === 'local edit') submitClipParamsEdit(captured, { values: {}, clear: ['missing'] });
      if (change === 'head') {
        session.observe(await env.external((raw) => {
          (raw.parent_revision.payload.clips as Record<string, unknown>[])[1].label = 'remote';
        }));
      }
      if (change === 'close') await session.dispose();
      if (change === 'cancel') session.clipParamsPort.invalidatePrefetch!();
      if (change === 'new read') await session.clipParamsPort.prefetch!(captured.basis, f.pin);
      pause.resolve();
      await refusal;
      expect(captured.basis.select).toBe('parent/clip:x');
      expect(edit.values.seed).toBe(8);
      expect(env.previews).not.toHaveBeenCalled();
      expect(env.commits()).toHaveLength(0);
      await session.dispose();
    },
  );

  it('rejects a forged or older capture before any read', async () => {
    const { env, f, reads, session, captured } = await setup();
    await expect(session.clipParamsPort.prefetch!({ ...captured.basis, select: 'parent/clip:y' }, f.pin)).rejects.toThrow('capture changed');
    captureClipParamsEdit(session.clipParamsPort, env.current(), 'y');
    await expect(session.clipParamsPort.prefetch!(captured.basis, f.pin)).rejects.toThrow('capture changed');
    expect(reads.getProjectVerifiedDocument).not.toHaveBeenCalled();
    await session.dispose();
  });

  it('refuses unavailable reads explicitly while preserving the existing draft basis', async () => {
    const { env, f, session } = await setup();
    await session.dispose();
    const unstaged = await env.mount();
    const captured = captureClipParamsEdit(unstaged.clipParamsPort, env.current(), 'x');
    await expect(unstaged.clipParamsPort.prefetch!(captured.basis, f.pin)).rejects.toThrow('reads are unavailable; draft preserved');
    expect(() => submitClipParamsEdit(captured, edit)).toThrow('exact schema_source and verified immutable inputs');
    expect(env.previews).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await unstaged.dispose();
  });

  it.each(['document', 'object'] as const)('propagates a %s refusal without touching the draft or outbox', async (failure) => {
    const { env, f, reads, session, captured, outboxBefore } = await setup();
    const original = structuredClone(captured.basis);
    if (failure === 'document') reads.getProjectVerifiedDocument.mockRejectedValueOnce(new Error('retained access refused'));
    else reads.getProjectVerifiedDocumentObject.mockRejectedValueOnce(new Error('retained access refused'));
    await expect(session.clipParamsPort.prefetch!(captured.basis, f.pin)).rejects.toThrow('retained access refused');
    expect(captured.basis).toEqual(original);
    expect(await env.outboxes.list(scope)).toEqual(outboxBefore);
    expect(env.previews).not.toHaveBeenCalled();
    if (failure === 'document') expect(reads.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
    await session.dispose();
  });

  it('rereads the complete V1 pin after V2/removal/reopen without a latest fallback or shared cache', async () => {
    const { env, f, reads, session, captured } = await setup();
    const v2 = retained(2, 20);
    await session.clipParamsPort.prefetch!(captured.basis, f.pin);
    reads.getDocument.mockResolvedValue(v2.verified.document);
    expect((await session.clipParamsPort.prefetch!(captured.basis, f.pin)).schema_source).toEqual(f.pin);
    reads.getDocument.mockResolvedValue(null);
    await session.dispose();
    const reopened = await createTimelineCommandSession({ scope, initial: env.initial, outboxes: env.outboxes,
      send: (request, key) => env.provider.commitTimeline(request, key), preview: env.previews,
      project: async () => {}, changed: () => {}, paramReadClient: reads });
    const next = captureClipParamsEdit(reopened.clipParamsPort, env.current(), 'x');
    const inputs = await reopened.clipParamsPort.prefetch!(next.basis, f.pin);
    expect(inputs.schema_inputs).toEqual([[f.verified, { [f.snapshot.object_id]: f.snapshot }]]);
    expect(reads.getProjectVerifiedDocument).toHaveBeenCalledTimes(3);
    for (const call of reads.getProjectVerifiedDocument.mock.calls) expect(call).toEqual([scope.projectId, f.pin]);
    expect(reads.getDocument).not.toHaveBeenCalled();
    expect(env.commits()).toHaveLength(0);
    await reopened.dispose();
  });
});
