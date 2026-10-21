import { describe, expect, it } from 'vitest';
import type { JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import { canonicalJsonStringify, sha256Hex } from '../data/typed/timelineBundle.ts';
import { transcriptDocumentId } from '../data/typed/projectTranscript.ts';
import { computeHostFingerprint } from '@/sdk/video/timeline/sourceMap.ts';
import {
  captureTranscriptAssociation,
  executeTranscriptAssociation,
  finishTranscriptAssociation,
  TRANSCRIPT_SCHEMA_REF,
} from './transcriptAssociateCapture.ts';
import { copy, type AuthoredBundle } from './clipMovePrimitives.ts';

const PROJECT = 'project-1';
const MEDIA = `sha256:${'a'.repeat(64)}`;
const assetId = 'asset-a';
const sourceId = 'source-1';
const legacyId = 'transcript-source:source-1:segment:segment-a';
const canonicalId = 'transcript-source:asset-a:source:source-1:segment:segment-a';
const reviewKey = `transcript-source-review:${encodeURIComponent(legacyId)}`;

const sourceContent = (segmentId = canonicalId) => ({
  schema: 'media.transcript/v1' as const,
  media_id: MEDIA,
  source_id: sourceId,
  segments: [{
    id: segmentId,
    start: 0,
    end: 1,
    text: 'Hello',
    words: [{ id: `${segmentId}:word:word-a`, start: 0, end: 1, text: 'Hello' }],
  }],
});

async function source(segmentId = canonicalId, version = 1) {
  const content = sourceContent(segmentId);
  const documentId = await transcriptDocumentId(PROJECT, MEDIA, sourceId);
  const pin = {
    document_id: documentId,
    version,
    content_digest: `sha256:${await sha256Hex(canonicalJsonStringify(content))}`,
  };
  return {
    pin,
    document: {
      document_id: documentId,
      project_id: PROJECT,
      kind: 'media.transcript',
      version,
      content,
    },
  };
}

function projectedItem(id: string, sourceDocumentId = 'transcript:old') {
  return {
    id,
    shape: 'interval',
    domain: 'source_seconds',
    extent: { start: 0, end: 1 },
    schemaRef: TRANSCRIPT_SCHEMA_REF,
    sourceArtifactRef: { assetId },
    provenance: { adapterId: 'legacy.capture', adapterVersion: '1' },
    payload: {
      sourceId,
      segmentId: id,
      text: 'Old text',
      words: [{ id: `${id}:word:word-a`, start: 0, end: 1, text: 'Old' }],
      documentId: sourceDocumentId,
      documentVersion: 1,
      opaque: { keep: [null, false] },
    },
    opaqueEnvelope: { keep: true },
  };
}

function bundle({ sharedReview = false, collision = false, associated = false }: {
  sharedReview?: boolean;
  collision?: boolean;
  associated?: boolean;
} = {}): AuthoredBundle {
  const media = { id: 'media-a', asset: assetId, track: 'A1', clipType: 'audio' };
  const captionId = `transcript-caption-${computeHostFingerprint(`${legacyId}@media-a`).split(':')[1]}`;
  const caption = {
    id: captionId,
    track: 'transcript-caption-foundry-track',
    clipType: 'text',
    at: 0.1,
    hold: 2.3,
    text: { content: 'Human correction', color: '#cc3377', fontSize: 51 },
    opaque: { keep: [null, false, 0] },
    app: {
      retained: { future: [null, false] },
      __generated__: {
        extensionId: 'haus.astrid.transcript-lane',
        contributionId: 'transcript-caption-foundry',
        provenance: {
          contractVersion: 1,
          sourceSchemaRef: TRANSCRIPT_SCHEMA_REF,
          sourceItemId: legacyId,
          sourceFingerprint: 'keep-source-fingerprint',
          generatorVersion: '1.3.0',
          outputFingerprint: 'keep-output-fingerprint',
          conflictPolicy: 'preserve-output',
        },
      },
    },
  };
  const clips: JSON[] = [media, caption];
  if (collision) clips.push({ id: `transcript-caption-${computeHostFingerprint(`${canonicalId}@media-a`).split(':')[1]}`, track: 'other', clipType: 'text' });
  const oldItem = projectedItem(legacyId);
  const sourceItems: JSON[] = [oldItem];
  if (sharedReview) sourceItems.push({ ...copy(oldItem), sourceArtifactRef: { assetId: 'asset-b' } });
  const config = {
    output: { fps: 30 },
    tracks: [{ id: 'A1', kind: 'audio' }, { id: 'transcript-caption-foundry-track', kind: 'visual' }],
    clips,
    app: {
      unrelated: { keep: true },
      'haus.astrid.transcript-lane': {
        preferences: { color: 'blue' },
        [reviewKey]: {
          schemaVersion: 1,
          sourceSchemaRef: TRANSCRIPT_SCHEMA_REF,
          sourceItemId: legacyId,
          status: 'accepted-for-source-update',
          proposedText: 'Human correction',
          opaque: { keep: [null, false] },
        },
      },
    },
    bundle: {
      schema_version: 1,
      transcriptReferences: {
        schema: 'media.transcript.references/v1',
        associations: associated ? [{ assetId, documentId: 'transcript:old' }] : [],
      },
      itemsBySchemaRef: {
        'other/v1': [{ id: 'unrelated', shape: 'point', domain: 'ordinal', extent: { start: 0 }, schemaRef: 'other/v1', payload: { keep: true }, sourceArtifactRef: { assetId: 'other' }, provenance: { adapterId: 'other', adapterVersion: '1' } }],
        [TRANSCRIPT_SCHEMA_REF]: sourceItems,
      },
      opaqueBundle: { keep: true },
    },
  };
  return {
    schema_version: 1,
    project_id: PROJECT,
    timeline_id: 'film',
    parent: {
      config,
      clips: copy(clips),
      registry: { assets: { [assetId]: { media_id: MEDIA, type: 'audio' } } },
      opaqueParent: { keep: [null, false] },
    },
    placements: [],
    shots: {},
    source_mapping: {},
  } as AuthoredBundle;
}

describe('dormant transcript.associate capture', () => {
  it('matches the Agent record for nested source planes and no-asset caption/review reconciliation', async () => {
    const input = bundle();
    const before = copy(input);
    const document = await source();
    const basis = await captureTranscriptAssociation(input, assetId, document);
    const result = await finishTranscriptAssociation(basis);
    const nested = result.bundle.parent.config.bundle as Record<string, JSON>;
    const refs = nested.transcriptReferences as Record<string, JSON>;
    const items = (nested.itemsBySchemaRef as Record<string, JSON[]>)[TRANSCRIPT_SCHEMA_REF];
    const config = result.bundle.parent.config as Record<string, JSON>;
    const caption = (result.bundle.parent.clips as JSON[])[1] as Record<string, JSON>;
    const extension = (config.app as Record<string, JSON>)['haus.astrid.transcript-lane'] as Record<string, JSON>;

    expect(result.command).toMatchObject({
      schema_version: 1,
      op: 'transcript.associate',
      version: '1',
      select: 'parent/asset:asset-a',
      intent: { ownership: 'parent' },
      args: {
        asset_id: assetId,
        media_id: MEDIA,
        source_id: sourceId,
        document: document.pin,
        previous_document: null,
        source_schema_ref: TRANSCRIPT_SCHEMA_REF,
      },
      resolved: ['parent/asset:asset-a'],
    });
    expect(result.record.dependencies).toEqual([{ key: 'transcript.document', kind: 'transcript', pin: document.pin, policy: 'exact' }]);
    expect(result.record.command).toEqual(result.command);
    expect(result.command.bindings).toEqual({});
    expect(result.record.bindings).toEqual([
      { key: 'transcript.owner', ref: 'parent/asset:asset-a', policy: 'fixed', dependencies: [] },
      { key: `transcript.segment:${canonicalId}`, ref: 'parent/asset:asset-a', policy: 'fixed', dependencies: [] },
      { key: `transcript.word:${canonicalId}:word:word-a`, ref: 'parent/asset:asset-a', policy: 'fixed', dependencies: [] },
    ]);
    expect(result.record.created).toEqual([]);
    expect(result.record.selections).toEqual([expect.objectContaining({
      key: 'transcript.source-items',
      owner: 'parent',
      order: [`["asset-a","source-1","${legacyId}"]`],
    })]);
    expect((refs.associations as JSON[])).toEqual([{ assetId, documentId: document.pin.document_id }]);
    expect(Object.keys(nested.itemsBySchemaRef as Record<string, JSON>)).toEqual(['other/v1', TRANSCRIPT_SCHEMA_REF]);
    expect((nested.itemsBySchemaRef as Record<string, JSON[]> )['other/v1']).toEqual(expect.arrayContaining([{ id: 'unrelated', shape: 'point', domain: 'ordinal', extent: { start: 0 }, schemaRef: 'other/v1', payload: { keep: true }, sourceArtifactRef: { assetId: 'other' }, provenance: { adapterId: 'other', adapterVersion: '1' } }]));
    expect(items.map((item) => item.id)).toEqual([canonicalId]);
    expect(caption.id).toBe(`transcript-caption-${computeHostFingerprint(`${canonicalId}@media-a`).split(':')[1]}`);
    expect(caption).not.toHaveProperty('asset');
    expect(caption.text).toEqual({ content: 'Human correction', color: '#cc3377', fontSize: 51 });
    expect(caption.opaque).toEqual({ keep: [null, false, 0] });
    expect((caption.app as Record<string, JSON>).retained).toEqual({ future: [null, false] });
    expect(extension[reviewKey]).toBeUndefined();
    expect(extension[`transcript-source-review:${encodeURIComponent(canonicalId)}`]).toMatchObject({ sourceItemId: canonicalId, opaque: { keep: [null, false] } });
    expect(result.record.writes.map((write) => [write.ref, write.path])).toEqual([
      ['parent', ['config', 'bundle', 'transcriptReferences']],
      ['parent', ['config', 'bundle', 'itemsBySchemaRef']],
      ['parent', ['clips']],
      ['parent', ['config', 'app', 'haus.astrid.transcript-lane']],
    ]);
    expect(input).toEqual(before);
  });

  it('retains the exact prior pin on replacement and preserves source order', async () => {
    const input = bundle({ associated: true });
    const old = await source(legacyId);
    const next = await source();
    ((input.parent.config.bundle as Record<string, JSON>).transcriptReferences as Record<string, JSON>).associations = [
      { assetId, documentId: old.pin.document_id },
    ];
    const oldItems = (input.parent.config.bundle as Record<string, JSON>).itemsBySchemaRef as Record<string, JSON[]>;
    oldItems[TRANSCRIPT_SCHEMA_REF] = [projectedItem(legacyId, old.pin.document_id)];
    const result = await executeTranscriptAssociation(input, {
      schema_version: 1,
      op: 'transcript.associate',
      version: '1',
      select: 'parent/asset:asset-a',
      args: {
        asset_id: assetId,
        media_id: MEDIA,
        source_id: sourceId,
        document: next.pin,
        previous_document: old.pin,
        source_schema_ref: TRANSCRIPT_SCHEMA_REF,
      },
      intent: { ownership: 'parent' },
    }, next, old);
    expect(result.record.dependencies.map((dependency) => dependency.pin)).toEqual([next.pin, old.pin]);
    expect(result.bundle.parent.config.bundle.transcriptReferences.associations).toEqual([{ assetId, documentId: next.pin.document_id }]);
    expect(result.bundle.parent.config.bundle.itemsBySchemaRef[TRANSCRIPT_SCHEMA_REF][0].id).toBe(canonicalId);
  });

  it.each([
    ['caption destination collision', () => bundle({ collision: true }), 'caption destination'],
    ['shared review ownership', () => bundle({ sharedReview: true }), 'review ownership'],
  ])('refuses %s atomically', async (_label, make, message) => {
    const input = make();
    const before = copy(input);
    await expect(executeTranscriptAssociation(input, {
      schema_version: 1, op: 'transcript.associate', version: '1', select: 'parent/asset:asset-a',
      args: { asset_id: assetId, media_id: MEDIA, source_id: sourceId, document: (await source()).pin, previous_document: null, source_schema_ref: TRANSCRIPT_SCHEMA_REF },
      intent: { ownership: 'parent' },
    }, await source())).rejects.toThrow(message);
    expect(input).toEqual(before);
  });

  it('refuses malformed pinned source before changing either nested plane', async () => {
    const input = bundle();
    const before = copy(input);
    const valid = await source();
    const malformed = copy(valid);
    (malformed.document.content as Record<string, JSON>).segments = [];
    await expect(executeTranscriptAssociation(input, {
      schema_version: 1, op: 'transcript.associate', version: '1', select: 'parent/asset:asset-a',
      args: { asset_id: assetId, media_id: MEDIA, source_id: sourceId, document: valid.pin, previous_document: null, source_schema_ref: TRANSCRIPT_SCHEMA_REF },
      intent: { ownership: 'parent' },
    }, malformed)).rejects.toThrow('content is malformed');
    expect(input).toEqual(before);
  });
});
