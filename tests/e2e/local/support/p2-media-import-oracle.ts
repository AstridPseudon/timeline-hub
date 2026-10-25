import { strict as assert } from 'node:assert';
import { createHash } from 'node:crypto';

type JsonObject = Record<string, unknown>;

export interface MediaImportFileEvidence {
  name: string;
  type: string;
  bytesBase64: string;
}

export interface MediaImportSourceEvidence {
  objectId: string;
  digest: string;
  mediaType: string;
}

export interface MediaImportEvidence {
  bytes: Uint8Array;
  source: MediaImportSourceEvidence;
  rawEntry: {
    object_id: string;
    media_type: string;
    size: number;
    filename: string;
  };
}

function record(value: unknown, label: string): JsonObject {
  assert(value !== null && typeof value === 'object' && !Array.isArray(value), `${label} must be an object`);
  return value as JsonObject;
}

function digest(bytes: Uint8Array): string {
  return `sha256:${createHash('sha256').update(bytes).digest('hex')}`;
}

/** Build import expectations from the source bytes, never from the received import response. */
export function mediaImportEvidence(
  file: MediaImportFileEvidence,
  source: MediaImportSourceEvidence,
): MediaImportEvidence {
  const bytes = new Uint8Array(Buffer.from(file.bytesBase64, 'base64'));
  assert.equal(digest(bytes), source.digest, 'source digest must be the digest of the genuine file bytes');
  assert.equal(file.type, source.mediaType, 'source media type must be the genuine file media type');
  return {
    bytes,
    source,
    rawEntry: {
      object_id: source.objectId,
      media_type: source.mediaType,
      size: bytes.byteLength,
      filename: file.name,
    },
  };
}

/** The Runtime import boundary is a closed four-field ABI. */
export function assertRawMediaImportEntry(actual: unknown, expected: MediaImportEvidence['rawEntry']): void {
  assert.deepStrictEqual(actual, expected, 'raw media import entry must exactly match the Runtime ABI and genuine source');
}

/** The editor catalogue is a distinct normalized stage, carrying original identity without raw ABI fields. */
export function assertNormalizedCatalogueEntry(
  actual: unknown,
  source: MediaImportSourceEvidence,
): void {
  const entry = record(actual, 'normalized catalogue entry');
  for (const key of ['object_id', 'media_type', 'size', 'filename']) {
    assert.equal(Object.hasOwn(entry, key), false, `normalized catalogue entry must not expose raw field ${key}`);
  }
  for (const [key, expected] of [
    ['media_id', source.objectId],
    ['content_sha256', source.digest],
    ['type', source.mediaType],
  ] as const) {
    assert.equal(Object.hasOwn(entry, key), true, `normalized catalogue entry must contain ${key}`);
    assert.equal(entry[key], expected, `normalized catalogue entry ${key} must preserve the genuine source value`);
  }
}
