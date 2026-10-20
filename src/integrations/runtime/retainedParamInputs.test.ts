import { createHash } from 'node:crypto';
import { describe, expect, it, vi } from 'vitest';
import { ApiError, WorkspaceClient } from './generated.ts';
import type { DocumentPin, Transport, VerifiedDocument, VerifiedDocumentObject } from './generated.ts';
import { fixtureDigest } from './__tests__/timelineCommitFixture.ts';
import { readRetainedParamInputs } from './retainedParamInputs.ts';

const context = { project_id: 'project-1', realm_id: 'realm' };
const selected = { packId: 'test_pack', id: 'reveal', kind: 'effect', revision: `sha256:${'1'.repeat(64)}` };
const clone = <T>(value: T): T => JSON.parse(JSON.stringify(value));

// Portable-envelope shape from frozen027 project_packs._portable_snapshot and
// the seed schema from test_timeline_selected_schema_runtime.retained_pack.
// These are read-port specimens, not admitted native fixtures or capture goldens.
function fixture(maximum = 10, version = 1) {
  const schema = {
    schema_version: 1, id: 'reveal', kind: 'effect', pack_id: selected.packId,
    short_description: 'Test reveal.', defaults: { seed: 4 },
    schema: {
      type: 'object', properties: { seed: { type: 'number', maximum } },
      required: ['unrelated'], additionalProperties: false,
    },
    runtime: { adapter: 'remotion' },
  };
  const resource = Buffer.from(JSON.stringify(schema));
  const path = 'rendering/elements/effects/reveal/element.json';
  const bytes = Buffer.from(JSON.stringify({
    files: [{ path, sha256: createHash('sha256').update(resource).digest('hex'), bytes_base64: resource.toString('base64') }],
    // Deliberately no successful build identity: the adapter must not validate
    // or manufacture one. Native capture must validate the complete closure.
    build_receipt_base64: Buffer.from('{}').toString('base64'),
  }));
  const digest = `sha256:${createHash('sha256').update(bytes).digest('hex')}`;
  const descriptor = { object_id: digest, digest, size: bytes.length, media_type: 'application/json' as const };
  const snapshot: VerifiedDocumentObject = { ...descriptor, bytes_base64: bytes.toString('base64') };
  const admission = { id: selected.id, kind: selected.kind, revision: selected.revision,
    snapshot_digest: '2'.repeat(64), snapshot_object: descriptor };
  const content = {
    schema: 'astrid.project-pack/v1', pack_id: selected.packId, source_binding_key: 'project-packs',
    relative_manifest: `realm/project-1/packs/${selected.packId}/pack.yaml`, admissions: [admission],
  };
  const pin: DocumentPin = { document_id: 'original-pack-document', version, content_digest: fixtureDigest(content) };
  const verified: VerifiedDocument = { pin, document: {
    document_id: pin.document_id, project_id: context.project_id, kind: 'astrid.project-pack', version, content,
    created_at: '2026-10-19T00:00:00Z', updated_at: '2026-10-19T00:00:00Z',
    opaque: { literal: [null, false, {}, ''], nullable: null },
  } };
  const client = {
    getProjectVerifiedDocument: vi.fn<WorkspaceClient['getProjectVerifiedDocument']>(async () => verified),
    getProjectVerifiedDocumentObject: vi.fn<WorkspaceClient['getProjectVerifiedDocumentObject']>(async () => snapshot),
  };
  return { client, verified, snapshot, content, admission, pin };
}

function maximum(snapshot: VerifiedDocumentObject): number {
  const envelope = JSON.parse(Buffer.from(snapshot.bytes_base64, 'base64').toString());
  return JSON.parse(Buffer.from(envelope.files[0].bytes_base64, 'base64').toString()).schema.properties.seed.maximum;
}

describe('retained selected PARAM read inputs', () => {
  it('returns the original semantic inputs and reads exactly one selected object', async () => {
    const f = fixture();
    const before = clone({ verified: f.verified, snapshot: f.snapshot, selected, context });
    const result = await readRetainedParamInputs(f.client, context, f.pin, selected);
    expect(result.verified).toBe(f.verified);
    expect(result.objects).toEqual({ [f.snapshot.object_id]: f.snapshot });
    expect(result.objects[f.snapshot.object_id]).toBe(f.snapshot);
    expect({ verified: f.verified, snapshot: f.snapshot, selected, context }).toEqual(before);
    expect(result.verified.document.opaque).toEqual({ literal: [null, false, {}, ''], nullable: null });
    expect(result.verified.document).not.toHaveProperty('absent');
    expect(f.client.getProjectVerifiedDocument).toHaveBeenCalledExactlyOnceWith(context.project_id, f.pin);
    expect(f.client.getProjectVerifiedDocumentObject).toHaveBeenCalledExactlyOnceWith(context.project_id, f.pin, f.snapshot.object_id);
    expect(f.client.getProjectVerifiedDocument.mock.calls[0][1]).toBe(f.pin);
    expect(f.client.getProjectVerifiedDocumentObject.mock.calls[0][1]).toBe(f.pin);
    expect(f.snapshot.digest).not.toBe(selected.revision);
    expect(f.snapshot.digest).not.toBe(f.pin.content_digest);
  });

  it.each(['elementRef', 'element_ref'])('takes the raw selected %s without a UI descriptor', async (field) => {
    const f = fixture();
    const clip = { [field]: { ...selected, opaque: { nullable: null } } };
    expect((await readRetainedParamInputs(f.client, context, f.pin, clip[field])).verified).toBe(f.verified);
  });

  it('ignores an unselected corrupt object and selects by the full admission identity', async () => {
    const f = fixture();
    const other = { object_id: `sha256:${'3'.repeat(64)}`, digest: `sha256:${'3'.repeat(64)}`,
      size: 1, media_type: 'application/json' as const };
    for (const change of [{ id: 'other' }, { kind: 'animation' }, { revision: `sha256:${'4'.repeat(64)}` }]) {
      f.content.admissions.unshift({ ...f.admission, ...change, snapshot_object: other });
    }
    f.pin.content_digest = fixtureDigest(f.content);
    const objects = { [other.object_id]: { ...other, bytes_base64: 'corrupt' }, [f.snapshot.object_id]: f.snapshot };
    f.client.getProjectVerifiedDocumentObject = vi.fn(async (_project, _pin, objectId: string) => objects[objectId]);
    const result = await readRetainedParamInputs(f.client, context, f.pin, selected);
    expect(Object.keys(result.objects)).toEqual([f.snapshot.object_id]);
    expect(f.client.getProjectVerifiedDocumentObject).toHaveBeenCalledExactlyOnceWith(context.project_id, f.pin, f.snapshot.object_id);
  });

  it.each(['live V2', 'live removal', 'latest read error'])('keeps the V1 max10 bytes under fake %s', async (state) => {
    const f = fixture();
    const live = state === 'live V2' ? fixture(20, 2) : undefined;
    const before = clone(f.verified);
    // The fake normal read supplies retained V1; latest state cannot replace it.
    const client = { ...f.client, getDocument: vi.fn(async () => {
      if (state === 'latest read error') throw new Error('latest unavailable');
      return live?.verified.document ?? null;
    }) };
    const result = await readRetainedParamInputs(client, context, f.pin, selected);
    expect(maximum(result.objects[f.snapshot.object_id])).toBe(10);
    if (live) expect(maximum(live.snapshot)).toBe(20);
    expect(result.verified).toEqual(before);
    expect(result.objects[f.snapshot.object_id].bytes_base64).toBe(f.snapshot.bytes_base64);
    expect(client.getDocument).not.toHaveBeenCalled();
  });

  it.each(['document', 'object'])('refuses substituted live V2 %s inputs', async (stage) => {
    const f = fixture();
    const v2 = fixture(20, 2);
    const before = clone({ verified: f.verified, snapshot: f.snapshot });
    if (stage === 'document') f.client.getProjectVerifiedDocument.mockResolvedValue(v2.verified);
    else f.client.getProjectVerifiedDocumentObject.mockResolvedValue(v2.snapshot);
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects
      .toThrow(stage === 'document' ? 'original exact pin' : 'does not match selected admission');
    expect({ verified: f.verified, snapshot: f.snapshot }).toEqual(before);
  });

  it.each([{ project_id: '', realm_id: 'realm' }, { project_id: 'project-1', realm_id: '' },
    { project_id: 'slug/alias', realm_id: 'realm' }, { project_id: 'project-1', realm_id: null }])(
    'refuses unavailable canonical authenticated context: %j', async (scope) => {
      const f = fixture();
      await expect(readRetainedParamInputs(f.client, scope as typeof context, f.pin, selected)).rejects.toThrow('authenticated canonical');
      expect(f.client.getProjectVerifiedDocument).not.toHaveBeenCalled();
    },
  );

  it.each([undefined, null, {}, { document_id: 'display-only' },
    { document_id: 'doc', version: 0, content_digest: `sha256:${'a'.repeat(64)}` },
    { document_id: 'doc', version: 1, content_digest: 'not-a-digest' },
  ])('refuses an unavailable or invalid original pin before reads: %j', async (pin) => {
    const f = fixture();
    await expect(readRetainedParamInputs(f.client, context, pin as DocumentPin, selected)).rejects.toThrow('original exact DocumentPin');
    expect(f.client.getProjectVerifiedDocument).not.toHaveBeenCalled();
    expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
  });

  it.each([null, {}, { ...selected, packId: null }, { ...selected, id: '' }, { ...selected, revision: undefined }])(
    'refuses an incomplete selected reference before reads: %j', async (ref) => {
      const f = fixture();
      await expect(readRetainedParamInputs(f.client, context, f.pin, ref)).rejects.toThrow('owner-qualified element reference');
      expect(f.client.getProjectVerifiedDocument).not.toHaveBeenCalled();
    },
  );

  it.each([
    ['wrong document id', { document_id: 'another' }], ['wrong version', { version: 2 }],
    ['wrong digest', { content_digest: `sha256:${'5'.repeat(64)}` }],
  ])('refuses a response for %s without selected-object I/O', async (_name, change) => {
    const f = fixture();
    f.verified.pin = { ...f.pin, ...change };
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects.toThrow('original exact pin');
    expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
  });

  it.each([
    ['foreign project', { project_id: 'foreign' }], ['wrong row pin', { document_id: 'another' }],
    ['wrong row version', { version: 2 }], ['wrong document kind', { kind: 'astrid.config' }],
  ])('refuses %s without selected-object I/O', async (_name, change) => {
    const f = fixture();
    Object.assign(f.verified.document, change);
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects.toThrow('original scoped pin');
    expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
  });

  it.each([
    ['pack owner', { pack_id: 'foreign' }, 'owner or scope'],
    ['realm', { relative_manifest: `foreign/project-1/packs/${selected.packId}/pack.yaml` }, 'owner or scope'],
    ['schema', { schema: 'unsupported' }, 'schema/source binding'],
    ['binding', { source_binding_key: null }, 'schema/source binding'],
    ['missing admissions', { admissions: undefined }, 'schema/source binding'],
    ['null admissions', { admissions: null }, 'schema/source binding'],
  ])('refuses mismatched %s', async (_name, change, message) => {
    const f = fixture();
    Object.assign(f.content, change);
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects.toThrow(message);
    expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
  });

  it.each(['packId', 'id', 'kind', 'revision'])('refuses the wrong selected %s', async (key) => {
    const f = fixture();
    await expect(readRetainedParamInputs(f.client, context, f.pin, { ...selected, [key]: 'another' }))
      .rejects.toThrow(key === 'packId' ? 'owner or scope' : 'exactly one admission');
    expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
  });

  it('refuses duplicate matching admissions even if their object IDs agree', async () => {
    const f = fixture();
    f.content.admissions.push(clone(f.admission));
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects.toThrow('exactly one admission');
    expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
  });

  it.each([undefined, null, {}, { object_id: selected.revision }, { ...fixture().admission.snapshot_object, size: null }])(
    'refuses missing or malformed selected object descriptor: %j', async (descriptor) => {
      const f = fixture();
      Object.assign(f.admission, { snapshot_object: descriptor });
      if (descriptor === undefined) delete (f.admission as Partial<typeof f.admission>).snapshot_object;
      await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects
        .toThrow(descriptor == null ? 'snapshot unavailable; re-admit pack' : 'invalid pack snapshot object descriptor');
      expect(f.client.getProjectVerifiedDocumentObject).not.toHaveBeenCalled();
    },
  );

  it.each([
    { object_id: selected.revision }, { digest: selected.revision }, { size: 0 },
    { media_type: 'text/plain' }, { bytes_base64: null }, { extra: 'metadata' },
  ])('refuses mismatched selected-object response metadata: %j', async (change) => {
    const f = fixture();
    Object.assign(f.snapshot, change);
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects.toThrow('does not match selected admission');
    expect(f.client.getProjectVerifiedDocumentObject).toHaveBeenCalledTimes(1);
  });

  it('leaves byte corruption to native capture/acceptance without declaring a schema', async () => {
    const f = fixture();
    f.snapshot.bytes_base64 = 'corrupt';
    const result = await readRetainedParamInputs(f.client, context, f.pin, selected);
    expect(result).toEqual({ verified: f.verified, objects: { [f.snapshot.object_id]: f.snapshot } });
  });

  it.each(['document', 'object'])('propagates %s read refusal without fallback or mutation', async (stage) => {
    const f = fixture();
    const before = clone({ verified: f.verified, snapshot: f.snapshot });
    const error = new ApiError(404, 'unreachable', 'exact retained input unavailable');
    if (stage === 'document') f.client.getProjectVerifiedDocument.mockRejectedValue(error);
    else f.client.getProjectVerifiedDocumentObject.mockRejectedValue(error);
    await expect(readRetainedParamInputs(f.client, context, f.pin, selected)).rejects.toBe(error);
    expect({ verified: f.verified, snapshot: f.snapshot }).toEqual(before);
    expect(f.client.getProjectVerifiedDocument).toHaveBeenCalledTimes(1);
    expect(f.client.getProjectVerifiedDocumentObject).toHaveBeenCalledTimes(stage === 'document' ? 0 : 1);
  });

  it('uses the normal generated authenticated GET responses and exact original pin', async () => {
    const f = fixture();
    const transport = vi.fn<Transport>(async (method, path, headers, body) => {
      expect(method).toBe('GET');
      expect(headers.Authorization).toBe('Bearer credential');
      expect(body).toBeUndefined();
      const url = new URL(path, 'http://runtime.test');
      expect(url.searchParams.get('document_id')).toBe(f.pin.document_id);
      expect(url.searchParams.get('version')).toBe(String(f.pin.version));
      expect(url.searchParams.get('content_digest')).toBe(f.pin.content_digest);
      const objectRead = url.pathname === '/v1/projects/project-1/document-objects/verified';
      expect(url.pathname).toBe(objectRead ? '/v1/projects/project-1/document-objects/verified' : '/v1/projects/project-1/document-inputs/verified');
      expect([...url.searchParams.keys()].sort()).toEqual(
        ['document_id', 'version', 'content_digest', ...(objectRead ? ['object_id'] : [])].sort());
      if (objectRead) expect(url.searchParams.get('object_id')).toBe(f.snapshot.object_id);
      return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(objectRead ? f.snapshot : f.verified)) };
    });
    const client = new WorkspaceClient('http://runtime.test', 'credential', transport);
    const result = await readRetainedParamInputs(client, context, f.pin, selected);
    expect(result).toEqual({ verified: f.verified, objects: { [f.snapshot.object_id]: f.snapshot } });
    expect(maximum(result.objects[f.snapshot.object_id])).toBe(10);
    expect(transport).toHaveBeenCalledTimes(2);
  });
});
