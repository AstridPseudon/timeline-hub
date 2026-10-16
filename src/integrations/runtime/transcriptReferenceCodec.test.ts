import { describe, expect, it } from 'vitest';
import { migrateTranscriptReferencesV1, readTranscriptReferences } from './transcriptReferenceCodec';

// Synthetic contract fields only. D owns schema validation and ID generation.
// This literal was returned by D-TRANSCRIPT-DTO-101-NORMAL-handback.md; tests
// below prove pass-through, not a joined-helper/golden-ID validation claim.
const documentId = 'document:f0433b93-7d84-5eed-a7d7-f26ebc7a39fb';
const subject = { media_object_id: 'media-object-01', media_sha256: 'a'.repeat(64) };
const source = {
  producer_id: 'fixture.transcriber', source_id: 'transcript.main',
  lineage_id: 'lineage-1', revision_id: 'revision-1', producer_digest: 'b'.repeat(64),
};
const words = [
  { id: 'word-fixture-a', text: 'Hello', start_s: 0, end_s: 0.4 },
  { id: 'word-fixture-b', text: 'world', start_s: 0.4, end_s: 0.9 },
];
const segments = [{ id: 'segment-fixture-a', word_ids: words.map((word) => word.id) }];
const reference = () => ({
  document: { id: documentId, version: 1, content_digest: 'c'.repeat(64) },
  snapshot: { object_id: 'fixture-snapshot-1', sha256: 'c'.repeat(64) },
  subject: { ...subject }, source: { ...source },
  metadata: {
    opaque: { nullable: null, underscore: { _preserve: ['Unicode: café 🎬', false, 0] } },
    // Opaque preservation probe, not an embedded-transcript product convention.
    source_record: {
      schema_version: 1, subject: { ...subject }, source: { ...source },
      clock: { kind: 'media', unit: 'seconds', origin_seconds: 0 },
      words: structuredClone(words), segments: structuredClone(segments),
    },
  },
});
const nested = (references: unknown, v: unknown = 1) => ({ config: { app: { transcript: { v, references } } } });

function freeze<T>(value: T): T {
  if (value && typeof value === 'object') {
    for (const child of Object.values(value)) freeze(child);
    Object.freeze(value);
  }
  return value;
}

function migrationValue(input: unknown) {
  const result = migrateTranscriptReferencesV1(input);
  expect(result.ok).toBe(true);
  if (!result.ok) throw new Error(`${result.reason}: ${result.path}`);
  return result;
}

function expectRefusal(input: unknown, reason: string) {
  const before = structuredClone(input);
  const bytes = JSON.stringify(input);
  freeze(input);
  expect(readTranscriptReferences(input)).toMatchObject({ ok: false, reason });
  const result = migrateTranscriptReferencesV1(input);
  expect(result).toMatchObject({ ok: false, reason });
  expect(result.value).toBe(input);
  expect(input).toEqual(before);
  expect(JSON.stringify(input)).toBe(bytes);
}

describe('explicit transcript reference carrier codec', () => {
  it.each([
    {}, { config: {} }, { config: { app: {} } },
    { config: { app: { transcript: { source_id: 'managed-declaration' } } } },
    { config: { app: { transcript: { v: 1, source_id: 'managed-declaration' } } } },
  ])('keeps a missing index absent and creates no namespace: %j', (input) => {
    freeze(input);
    expect(readTranscriptReferences(input)).toMatchObject({ ok: true, references: { present: false } });
    const result = migrationValue(input);
    expect(result).toMatchObject({ changed: false, references: { present: false } });
    expect(result.value).toBe(input);
  });

  it.each([
    { transcriptReferences: {} }, nested({}), { transcriptReferences: {}, ...nested({}) },
  ])('keeps explicit empty/clear indexes present: %j', (input) => {
    const result = migrationValue(freeze(input));
    expect(result.references).toEqual({ present: true, value: {} });
    expect(result.value).toEqual(nested({}));
    expect(Object.hasOwn(result.value, 'transcriptReferences')).toBe(false);
  });

  it.each([
    { transcriptReferences: {}, ...nested({ main: reference() }) },
    { transcriptReferences: { main: reference() }, ...nested({}) },
  ])('refuses explicit clear versus populated competing carriers', (input) => {
    expectRefusal(input, 'conflicting-carriers');
  });

  it('dual-reads legacy without implicitly migrating it', () => {
    const input = freeze({ transcriptReferences: { main: reference() }, untouched: true });
    const bytes = JSON.stringify(input);
    expect(readTranscriptReferences(input)).toEqual({
      ok: true, carriers: { legacy: true, nested: false },
      references: { present: true, value: input.transcriptReferences },
    });
    expect(JSON.stringify(input)).toBe(bytes);
    expect(Object.hasOwn(input, 'config')).toBe(false);
  });

  it('dual-reads a v1 nested carrier without requiring migration', () => {
    const input = freeze(nested({ main: reference() }));
    expect(readTranscriptReferences(input)).toMatchObject({
      ok: true, carriers: { legacy: false, nested: true },
      references: { present: true, value: { main: reference() } },
    });
    expect(migrationValue(input)).toMatchObject({ changed: false, value: input });
  });

  it('preserves the complete managed declaration, foreign owners, and unknown metadata', () => {
    const declaration = {
      source_id: 'managed-take', source_version: 7, producer: { id: 'managed' },
      file: 'managed.json', media: { object_id: 'managed-media' }, sha256: 'd'.repeat(64),
      _opaque: { unknown: [null, 'keep', { x: true }] },
    };
    const input = freeze({
      _root: { weird: [1, 2] }, tracks: [{ app: { scaleAppliesToPositionedClips: true } }],
      transcriptReferences: { main: reference() },
      config: { _foreign: { x: 5 }, app: { transcript: declaration, astrid: { v: 1 },
        'foreign.owner': { v: 'malformed-but-foreign', payload: [null, true] }, other: null } },
    });
    const before = JSON.stringify(input);
    const result = migrationValue(input);
    expect(result.value).toEqual({
      _root: input._root, tracks: input.tracks,
      config: { ...input.config, app: { ...input.config.app,
        transcript: { ...declaration, v: 1, references: { main: reference() } } } },
    });
    expect(JSON.stringify(input)).toBe(before);
    expect(result.value.config).not.toBe(input.config);
    expect(migrationValue(result.value)).toMatchObject({ changed: false, value: result.value });
  });

  it('coalesces equal values with recursively reordered object keys, preserving opaque data', () => {
    const original = reference();
    function reorder(value: any): any {
      if (Array.isArray(value)) return value.map(reorder);
      if (value && typeof value === 'object') {
        return Object.fromEntries(Object.entries(value).reverse().map(([key, child]) => [key, reorder(child)]));
      }
      return value;
    }
    const input = freeze({ transcriptReferences: { main: original }, ...nested({ main: reorder(original) }) });
    const result = migrationValue(input);
    expect(result.references).toEqual({ present: true, value: { main: original } });
    expect(result.value).toEqual(nested({ main: original }));
  });

  it('merges disjoint explicit association keys and retains equal overlaps', () => {
    const other = { ...reference(), source: { ...source, source_id: 'transcript.take-2' } };
    const input = freeze({ transcriptReferences: { main: reference(), oldOnly: other },
      ...nested({ main: reference(), newOnly: { _opaque: 'retained' } }) });
    expect(migrationValue(input).references).toEqual({ present: true, value: {
      main: reference(), oldOnly: other, newOnly: { _opaque: 'retained' },
    } });
  });

  it('preserves arbitrary JSON association keys without prototype pollution', () => {
    const index = JSON.parse('{"__proto__":{"value":"old"},"constructor":{"value":"new"},"a/b~c":{"value":null}}');
    const result = migrationValue(freeze({ transcriptReferences: index }));
    expect(result.references).toEqual({ present: true, value: index });
    if (!result.references.present) throw new Error('missing index');
    expect(Object.hasOwn(result.references.value, '__proto__')).toBe(true);
    expect(({} as any).value).toBeUndefined();
  });

  it.each([
    { ...reference(), extra: 'opaque-difference' },
    { ...reference(), source: { ...source, revision_id: 'revision-2' } },
    { ...reference(), metadata: { ...reference().metadata, opaque: { nullable: null } } },
    { ...reference(), metadata: { ...reference().metadata, source_record: {
      ...reference().metadata.source_record, words: [...words].reverse(),
    } } },
  ])('refuses every unequal overlapping association without mutation', (competing) => {
    expectRefusal({ transcriptReferences: { main: reference() }, ...nested({ main: competing }) }, 'conflicting-carriers');
  });

  it.each([null, [], 'reference', 1, false, { main: null }, { main: [] }, { main: 'scalar' }])(
    'refuses malformed legacy even with a valid nested carrier: %j', (bad) => {
      expectRefusal({ transcriptReferences: bad, ...nested({ main: reference() }) }, 'malformed-carrier');
    },
  );
  it.each([null, [], 'reference', 1, false, { main: null }, { main: [] }, { main: 'scalar' }])(
    'refuses malformed nested even with a valid legacy carrier: %j', (bad) => {
      expectRefusal({ transcriptReferences: { main: reference() }, ...nested(bad) }, 'malformed-carrier');
    },
  );
  it.each([null, '1', true, 0, -1, 1.5, [], {}])('refuses malformed versions: %j', (v) => {
    expectRefusal({ transcriptReferences: { main: reference() }, ...nested({ main: reference() }, v) }, 'malformed-version');
  });
  it.each([2, 99])('refuses unsupported versions before relocation: %j', (v) => {
    expectRefusal({ transcriptReferences: { main: reference() }, ...nested({ main: reference() }, v) }, 'unsupported-version');
  });
  it('does not reinterpret an unversioned nested index as v1', () => {
    expectRefusal({ transcriptReferences: { main: reference() }, config: { app: { transcript: { references: {} } } } }, 'malformed-version');
  });
  it('refuses unsupported owner versions even without an index', () => {
    expectRefusal({ config: { app: { transcript: { v: 2, source_id: 'managed' } } } }, 'unsupported-version');
  });
  it.each([null, [], { config: null }, { config: { app: [] } }, { config: { app: { transcript: null } } }])(
    'refuses malformed envelope layers: %j', (input) => expectRefusal(input, 'malformed-envelope'),
  );
  it.each([undefined, NaN, Infinity, 1n, () => 1, Symbol('opaque')])(
    'refuses non-JSON opaque values instead of silently dropping/coercing them', (bad) => {
      const input = { transcriptReferences: { main: { opaque: bad } } };
      expect(migrateTranscriptReferencesV1(input)).toMatchObject({ ok: false, reason: 'malformed-carrier', value: input });
    },
  );
  it('refuses cycles, sparse arrays, hidden fields, symbol keys, and getters in a carrier', () => {
    const cycle: any = {}; cycle.self = cycle;
    const getter = Object.defineProperty({}, 'x', { enumerable: true, get() { throw new Error('must not run'); } });
    const hidden = Object.defineProperty({}, 'x', { value: true });
    const symbol = { [Symbol('key')]: 'preserve-or-refuse' };
    const sparse = new Array(2);
    for (const bad of [cycle, getter, hidden, symbol, { sparse }]) {
      const input = { transcriptReferences: { main: bad } };
      const result = migrateTranscriptReferencesV1(input);
      expect(result).toMatchObject({ ok: false, reason: 'malformed-carrier' });
      expect(result.value).toBe(input);
    }
  });

  it('returns detached reference values so callers cannot mutate input through a read or migration', () => {
    const input = freeze({ transcriptReferences: { main: reference() } });
    const read = readTranscriptReferences(input);
    const migrated = migrationValue(input);
    if (!read.ok || !read.references.present || !migrated.references.present) throw new Error('missing index');
    (read.references.value.main as any).source.source_id = 'caller-edit';
    (migrated.references.value.main as any).metadata.source_record.words[0].id = 'caller-edit';
    expect(input.transcriptReferences.main).toEqual(reference());
    expect((migrated.value as any).config.app.transcript.references.main).toEqual(reference());
  });

  it('preserves flat word IDs, ordered segment membership, subject/source, and occurrence provenance', () => {
    const association = { ...reference(), occurrences: [{ occurrence_id: 'first' }, { occurrence_id: 'repeat' }] };
    const result = migrationValue(freeze({ transcriptReferences: { main: association } }));
    expect(result.references).toEqual({ present: true, value: { main: association } });
    expect((result.value as any).config.app.transcript.references.main.metadata.source_record).toEqual({
      schema_version: 1, subject, source,
      clock: { kind: 'media', unit: 'seconds', origin_seconds: 0 }, words, segments,
    });
  });

  it.each(['revision', 'content', 'segmentation', 'occurrence'])(
    'preserves producer-supplied identity across a %s-only variant', (variant) => {
      const association: any = reference();
      if (variant === 'revision') association.source.revision_id = 'revision-2';
      if (variant === 'content') association.metadata.source_record.words[0].text = 'HELLO';
      if (variant === 'segmentation') association.metadata.source_record.segments = [
        { id: 'segment-one', word_ids: [words[0].id] },
        { id: 'segment-two', word_ids: [words[1].id] },
      ];
      if (variant === 'occurrence') association.occurrence_id = 'repeated-occurrence';
      const result = migrationValue(freeze({ transcriptReferences: { main: association } }));
      expect(result.references).toEqual({ present: true, value: { main: association } });
      const migrated = (result.value as any).config.app.transcript.references.main;
      expect(migrated.document.id).toBe(documentId);
      expect(migrated.metadata.source_record.words.map((word: any) => word.id)).toEqual(words.map((word) => word.id));
    },
  );

  it('keeps a same-key correction conflicting until explicit adoption, while a different source key merges', () => {
    // Logical cases from B-ASTRA101-TRANSCRIPT-GOLDEN-001-NORMAL: revision,
    // segmentation, content and occurrence are excluded from D's immutable key.
    // This carrier never computes that key or a document ID itself.
    const correction = reference();
    correction.source.revision_id = 'revision-2';
    correction.metadata.source_record.source.revision_id = 'revision-2';
    correction.metadata.source_record.words[1] = { ...words[1], id: 'word-replacement', text: 'friend' };
    correction.metadata.source_record.segments = [
      { id: 'segment-split-a', word_ids: ['word-fixture-a'] },
      { id: 'segment-split-b', word_ids: ['word-replacement'] },
    ];
    expect(correction.document.id).toBe(documentId); // opaque identity supplied by producer
    expectRefusal({ transcriptReferences: { main: reference() }, ...nested({ main: correction }) }, 'conflicting-carriers');
    expect(migrationValue({ transcriptReferences: { main: correction } }).references)
      .toEqual({ present: true, value: { main: correction } });
    const newSource = { ...reference(), source: { ...source, source_id: 'transcript.take-2' },
      document: { ...reference().document, id: 'fixture:new-source-helper-output-pending' } };
    expect(migrationValue({ transcriptReferences: { main: reference() }, ...nested({ take2: newSource }) }).references)
      .toEqual({ present: true, value: { main: reference(), take2: newSource } });
  });
});
