import { readFileSync, writeFileSync } from 'node:fs';
import { request } from 'node:http';
import { join } from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { describe, expect, it } from 'vitest';
import { ReighRuntimeClient } from '@/integrations/runtime/client.ts';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import type { Transport } from '@/integrations/runtime/generated.ts';
import { createShotCompositionAdapter, type PreparedShotComposition } from '@/tools/video-editor/data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '@/tools/video-editor/data/shotCompositionProjection.ts';
import { createShotTimelineDataProvider } from '@/tools/travel-between-images/components/shotTimelineDataProvider.ts';
import { cloneAssetRegistry } from '@/tools/video-editor/lib/timeline-domain.ts';
import { resolveTimelineConfig } from '@/tools/video-editor/lib/config-utils.ts';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults.ts';
import { serializeForDisk } from '@/tools/video-editor/lib/serialize.ts';
import type { AssetRegistry, ResolvedTimelineConfig, TimelineConfig } from '@/tools/video-editor/types/index.ts';

/**
 * S-PRES contract (WS-SAVE): opaque and unknown fields are kept across every
 * covered App save path: top-level config, `config.app` namespaces, clip and
 * track `app`, unknown clip fields, registry metadata, and the bundle. A known
 * field clear is the explicit `{"op":"clear"}` operation within its declared
 * coverage. Absent or removed values never reappear after save or exact reload.
 *
 * This fixture-backed harness intentionally retains red preservation checks
 * on the assigned base. It records the observed X0 output separately from the
 * current App serializer result; neither is rewritten as a pass.
 */

type JsonRecord = Record<string, unknown>;
type PreserveAssertion = { path: string; value: unknown };
type CapturedPublication = {
  idempotency_key: string;
  body: {
    expected_head: string;
    parent_revision_id: string;
    project_id: string;
    timeline_id: string;
    parent_composition: JsonRecord;
  };
};
type Case2Fixture = {
  B0: { immutable_base: { project_id: string; timeline_id: string; revision_id: string } };
  B2: { transactions: Array<{ gesture: string }> };
  B4: { publications: CapturedPublication[] };
  B5: { exact_reloads: Array<{ receipt_revision: string; reloaded_revision_id: string; status: string }> };
  expected: { must_preserve: PreserveAssertion[] };
};
type Case1Fixture = {
  B3: { scheduled: boolean };
  B4: { publication: unknown; composition_publication_count_before_first_edit: number };
  B5: { exact_reload: unknown; receipt_revision: unknown };
  expected: { revision_created: boolean; exact_reload: boolean; status: string };
};

const fixtureRoot = process.env.PRES_HARNESS_FIXTURE_ROOT;
const runtimeBaseUrl = process.env.PRES_HARNESS_RUNTIME_BASE_URL;
const runtimeEnabled = Boolean(runtimeBaseUrl);
const popupRuntimeReady = process.env.PRES_HARNESS_POPUP_RUNTIME_READY;
const popupEvidenceDirectory = process.env.PRES_HARNESS_POPUP_EVIDENCE_DIR;
const MISSING = Symbol('missing');
const case1Fixture = fixtureRoot ? readFixture<Case1Fixture>('x0-1-editor.json') : null;
const case2Fixture = fixtureRoot ? readFixture<Case2Fixture>('x0-2-editor.json') : null;

function asRecord(value: unknown): JsonRecord {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Expected a fixture object');
  }
  return value as JsonRecord;
}

function readFixture<T>(name: string): T {
  if (!fixtureRoot) throw new Error('Set PRES_HARNESS_FIXTURE_ROOT to the admitted X0-EDITOR fixture directory');
  return JSON.parse(readFileSync(join(fixtureRoot, name), 'utf8')) as T;
}

function cloneRecord<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function readDeep(value: unknown, parts: string[]): unknown | typeof MISSING {
  let current = value;
  for (const part of parts) {
    const object = current && typeof current === 'object' && !Array.isArray(current)
      ? current as JsonRecord
      : undefined;
    if (!object || !Object.prototype.hasOwnProperty.call(object, part)) return MISSING;
    current = object[part];
  }
  return current;
}

function writeDeep(value: JsonRecord, parts: string[], next: unknown): void {
  let current = value;
  for (const part of parts.slice(0, -1)) {
    const child = current[part];
    if (!child || typeof child !== 'object' || Array.isArray(child)) current[part] = {};
    current = current[part] as JsonRecord;
  }
  current[parts[parts.length - 1]!] = next;
}

function indexedPath(parent: JsonRecord, path: string): unknown | typeof MISSING {
  const indexed = /^(clips|tracks)\[([^\]]+)\]\.(.+)$/.exec(path);
  if (!indexed) return MISSING;
  const config = asRecord(parent.config);
  const collection = config[indexed[1]!];
  if (!Array.isArray(collection)) return MISSING;
  const item = collection.map(asRecord).find((candidate) => candidate.id === indexed[2]);
  return item ? readDeep(item, indexed[3]!.split('.')) : MISSING;
}

function readPreservationPath(parent: JsonRecord, path: string): unknown | typeof MISSING {
  if (path.startsWith('config.')) return readDeep(parent.config, path.slice('config.'.length).split('.'));
  if (path === 'unknownParentField') return readDeep(parent, ['unknownParentField']);
  if (path === 'registry.metadata') return readDeep(parent.registry, ['metadata']);

  const assetPath = /^registry\.assets\[([^\]]+)\]\.(.+)$/.exec(path);
  if (assetPath) {
    return readDeep(parent.registry, ['assets', assetPath[1]!, ...assetPath[2]!.split('.')]);
  }

  if (path.startsWith('clips[') || path.startsWith('tracks[')) return indexedPath(parent, path);
  return MISSING;
}

function writePreservationPath(parent: JsonRecord, path: string, value: unknown): void {
  if (path.startsWith('config.')) {
    writeDeep(asRecord(parent.config), path.slice('config.'.length).split('.'), value);
    return;
  }
  if (path === 'unknownParentField') {
    parent.unknownParentField = value;
    return;
  }
  if (path === 'registry.metadata') {
    writeDeep(asRecord(parent.registry), ['metadata'], value);
    return;
  }

  const assetPath = /^registry\.assets\[([^\]]+)\]\.(.+)$/.exec(path);
  if (assetPath) {
    writeDeep(asRecord(parent.registry), ['assets', assetPath[1]!, ...assetPath[2]!.split('.')], value);
    return;
  }

  const indexed = /^(clips|tracks)\[([^\]]+)\]\.(.+)$/.exec(path);
  if (indexed) {
    const config = asRecord(parent.config);
    const collection = config[indexed[1]!];
    if (!Array.isArray(collection)) throw new Error(`Missing ${indexed[1]} for ${path}`);
    const item = collection.map(asRecord).find((candidate) => candidate.id === indexed[2]);
    if (!item) throw new Error(`Missing ${indexed[1]} entry ${indexed[2]} for ${path}`);
    writeDeep(item, indexed[3]!.split('.'), value);
    return;
  }
  throw new Error(`Unsupported fixture preservation path: ${path}`);
}

function restoreRecordedBase(parentValue: JsonRecord, preserve: PreserveAssertion[]): JsonRecord {
  const parent = cloneRecord(parentValue);
  for (const assertion of preserve) writePreservationPath(parent, assertion.path, assertion.value);
  return parent;
}

function missingPreservationPaths(parent: JsonRecord, preserve: PreserveAssertion[]): string[] {
  return preserve
    .filter((assertion) => !isDeepStrictEqual(readPreservationPath(parent, assertion.path), assertion.value))
    .map((assertion) => assertion.path)
    .sort();
}

function observedCase2LossPaths(parent: JsonRecord): string[] {
  const registry = asRecord(parent.registry);
  const assets = asRecord(registry.assets);
  const assetMetadataFields = ['asset_id', 'digest', 'media_type', 'object_id', 'role', 'scope'];
  const assetLosses = Object.keys(assets).flatMap((assetId) =>
    assetMetadataFields.map((field) => `registry.assets[${assetId}].${field}`));
  const trackLosses = ['video', 'audio', 'titles', 'source-video'].map((trackId) => `tracks[${trackId}].name`);
  return ['registry.metadata', ...assetLosses, ...trackLosses].sort();
}

const unchangedCase2SentinelPaths = [
  'config.app',
  'config.vendorNamespace',
  'config.unknownConfigField',
  'config.bundle',
  'unknownParentField',
  'clips[parent-clip-one].app',
  'clips[parent-clip-one].unknownClipField',
  'clips[parent-clip-two].clipType',
  'clips[parent-clip-two].steps',
  'tracks[source-video].app.source',
  'tracks[source-video].app.x0TrackSentinel',
];

async function runAppSerializer(parent: JsonRecord): Promise<{ config: TimelineConfig; registry: AssetRegistry }> {
  const sourceConfig = asRecord(parent.config);
  const inputConfig = {
    ...sourceConfig,
    // `output` is derived editor state and is stripped by serializeForDisk.
    output: createDefaultTimelineConfig().output,
  } as unknown as TimelineConfig;
  const sourceRegistry = parent.registry as AssetRegistry;
  const resolved = await resolveTimelineConfig(
    inputConfig,
    sourceRegistry,
    async (file) => `https://fixture.invalid/${encodeURIComponent(file)}`,
  );
  return {
    config: serializeForDisk(resolved as ResolvedTimelineConfig),
    registry: cloneAssetRegistry(sourceRegistry),
  };
}

describe.skipIf(!fixtureRoot)('X0-EDITOR admitted preservation harness', () => {
  const case1 = case1Fixture as Case1Fixture;
  const case2 = case2Fixture as Case2Fixture;

  it('records case 1 as a no-edit open with no publication and no receipt reload', () => {
    expect(case1.B3.scheduled).toBe(false);
    expect(case1.B4.composition_publication_count_before_first_edit).toBe(0);
    expect(case1.B4.publication).toBeNull();
    expect(case1.B5.exact_reload).toBeNull();
    expect(case1.B5.receipt_revision).toBeNull();
    expect(case1.expected).toMatchObject({ revision_created: false, exact_reload: false, status: 'pass' });
  });

  it('keeps the captured case 2 red signature explicit: 23 of 34 preserved paths are absent', () => {
    expect(case2.B4.publications).toHaveLength(3);
    expect(case2.B5.exact_reloads).toHaveLength(3);
    const expectedLosses = observedCase2LossPaths(case2.B4.publications[0]!.body.parent_composition);
    expect(case2.expected.must_preserve).toHaveLength(34);
    expect(unchangedCase2SentinelPaths).toHaveLength(11);

    for (const [index, publication] of case2.B4.publications.entries()) {
      const parent = publication.body.parent_composition;
      const missing = missingPreservationPaths(parent, case2.expected.must_preserve);
      expect(publication.idempotency_key).toBe(publication.body.parent_revision_id);
      expect(publication.body.expected_head).toBe(
        index === 0 ? case2.B0.immutable_base.revision_id : case2.B5.exact_reloads[index - 1]!.receipt_revision,
      );
      expect(publication.body.project_id).toBe(case2.B0.immutable_base.project_id);
      expect(publication.body.timeline_id).toBe(case2.B0.immutable_base.timeline_id);
      expect(missing).toEqual(expectedLosses);
      expect(missing).toHaveLength(23);
      for (const path of unchangedCase2SentinelPaths) {
        const assertion = case2.expected.must_preserve.find((candidate) => candidate.path === path);
        expect(assertion, `Fixture is missing sentinel assertion ${path}`).toBeDefined();
        expect(readPreservationPath(parent, path), `Captured save changed sentinel ${path}`).toEqual(assertion!.value);
      }
      expect(case2.B5.exact_reloads[index]).toMatchObject({
        status: 'captured',
        receipt_revision: case2.B5.exact_reloads[index]!.reloaded_revision_id,
      });
    }
  });

  it('shows the admitted config.app and clip/track app sentinels still pass App resolution and serialization', async () => {
    for (const publication of case2.B4.publications) {
      const parent = restoreRecordedBase(publication.body.parent_composition, case2.expected.must_preserve);
      const sourceConfig = asRecord(parent.config);
      const resolvedAndSerialized = await runAppSerializer(parent);

      expect(resolvedAndSerialized.config.app).toEqual(sourceConfig.app);
      for (const clipId of ['parent-clip-one', 'parent-clip-two']) {
        const sourceClip = asRecord((sourceConfig.clips as unknown[]).map(asRecord).find((clip) => clip.id === clipId));
        const serializedClip = resolvedAndSerialized.config.clips.find((clip) => clip.id === clipId);
        if (sourceClip.app !== undefined) expect(serializedClip?.app).toEqual(sourceClip.app);
      }
      for (const track of sourceConfig.tracks as Array<Record<string, unknown>>) {
        if (track.app !== undefined) {
          expect(resolvedAndSerialized.config.tracks?.find((candidate) => candidate.id === track.id)?.app).toEqual(track.app);
        }
      }
    }
  });

  it('preserves every admitted X0 sentinel through the assigned App serializer (base red)', async () => {
    const findings: Array<{ gesture: string; missing: string[] }> = [];
    const serializerPaths = case2.expected.must_preserve.filter(({ path }) => path !== 'unknownParentField');

    for (const [index, publication] of case2.B4.publications.entries()) {
      const parent = restoreRecordedBase(publication.body.parent_composition, case2.expected.must_preserve);
      const serialized = await runAppSerializer(parent);
      const actual = { config: serialized.config, registry: serialized.registry } as JsonRecord;
      const missing = missingPreservationPaths(actual, serializerPaths);
      // A finding denotes a loss; keep the original empty-findings assertion
      // meaningful once every path survives, and check each snapshot directly.
      expect(missing, case2.B2.transactions[index]!.gesture).toEqual([]);
      if (missing.length === 0) continue;
      findings.push({ gesture: case2.B2.transactions[index]!.gesture, missing });
    }

    expect(findings, `Base App serializer preservation losses:\n${JSON.stringify(findings, null, 2)}`).toEqual([]);
  });

  const exactReloadIt = runtimeEnabled ? it : it.skip;
  exactReloadIt('loads each captured receipt revision through the App Runtime client', async () => {
    const client = new ReighRuntimeClient({ baseUrl: runtimeBaseUrl! });
    const firstBody = case2.B4.publications[0]!.body;
    const projectId = String(firstBody.project_id);
    const timelineId = String(firstBody.timeline_id);

    for (const reload of case2.B5.exact_reloads) {
      const record = await client.getProjectParentCompositionRevision(projectId, timelineId, reload.receipt_revision);
      expect(record.revision_id).toBe(reload.reloaded_revision_id);
      const payload = asRecord(record.payload);
      const missing = missingPreservationPaths(payload, case2.expected.must_preserve);
      expect(missing, `Exact Runtime reload lost: ${missing.join(', ')}`).toEqual([]);
    }
  });
});

/**
 * Constructed provider replay from admitted X0-EDITOR values, never a captured
 * X0-POPUP fixture. Opt in only with a task-owned loopback Runtime/store.
 * Three shot-local geometry edits repeat the original 23 repaired-value and
 * 11 sentinel predicates; these are 69/33 comparisons, not unique defects.
 * No parent split occurs, so the 16 split-child predicates remain inapplicable
 * here and retain their separate existing editor-path proof.
 */
it.skipIf(!popupRuntimeReady || !popupEvidenceDirectory || !fixtureRoot)(
  'constructed popup provider preserves admitted X0 values through actual Runtime exact reload',
  async () => {
    const ready = JSON.parse(readFileSync(popupRuntimeReady!, 'utf8')) as {
      endpoint: string; project_id: string; timeline_id: string; base_revision: string;
      occurrence_id: string; token_file: string;
    };
    expect(new URL(ready.endpoint).hostname).toBe('127.0.0.1');
    const token = readFileSync(ready.token_file, 'utf8').trim();
    const evidence = (name: string, value: unknown) =>
      writeFileSync(join(popupEvidenceDirectory!, name), JSON.stringify(value, null, 2));
    const exchanges: Array<{
      method: string; path: string; request: unknown; idempotencyKey?: string;
      status: number; result: unknown; responseUtf8: string;
    }> = [];
    const transport: Transport = async (method, path, headers, body) => {
      const bytes = body === undefined ? undefined : Buffer.from(ArrayBuffer.isView(body)
        ? new Uint8Array(body.buffer, body.byteOffset, body.byteLength)
        : await (body as Blob).arrayBuffer());
      const response = await new Promise<{ status: number; headers: Record<string, string>; body: Buffer }>((resolve, reject) => {
        const req = request(ready.endpoint + path, {
          method, headers: { ...headers, Authorization: `Bearer ${token}`,
            ...(bytes ? { 'Content-Length': String(bytes.length) } : {}) },
        }, (res) => {
          const chunks: Buffer[] = [];
          res.on('data', (chunk: Buffer) => chunks.push(chunk));
          res.on('end', () => resolve({
            status: res.statusCode!,
            headers: Object.fromEntries(Object.entries(res.headers)
              .filter((entry): entry is [string, string] => typeof entry[1] === 'string')),
            body: Buffer.concat(chunks),
          }));
        });
        req.on('error', reject);
        if (bytes) req.write(bytes);
        req.end();
      });
      exchanges.push({
        method, path, request: bytes ? JSON.parse(bytes.toString('utf8')) : null,
        idempotencyKey: headers['Idempotency-Key'], status: response.status,
        result: JSON.parse(response.body.toString('utf8')), responseUtf8: response.body.toString('utf8'),
      });
      evidence('popup-http.json', exchanges);
      return response;
    };
    const runtime = new RuntimeDataProvider({
      projectId: ready.project_id, baseUrl: ready.endpoint, transport, commitSessionStorage: null,
    });
    const client = new ReighRuntimeClient({ baseUrl: ready.endpoint, transport });
    const adapter = createShotCompositionAdapter(runtime.shotComposition);
    const base = await client.getProjectParentCompositionRevision(
      ready.project_id, ready.timeline_id, ready.base_revision,
    );
    expect(missingPreservationPaths(asRecord(base.payload), case2Fixture!.expected.must_preserve)).toEqual([]);
    let composition = await adapter.load({ projectId: ready.project_id, parentDocumentId: ready.timeline_id });
    expect(composition.headRevisionId).toBe(ready.base_revision);
    evidence('popup-base-exact.json', base);
    evidence('popup-loaded-graph.json', composition.contract);
    const opaqueParent = Object.fromEntries(Object.entries(asRecord(base.payload))
      .filter(([key]) => !['config', 'registry', 'clips', 'occurrences'].includes(key)));
    expect(opaqueParent).toHaveProperty('unknownParentField');
    const assertOpaqueParent = (parent: JsonRecord) => {
      for (const [key, value] of Object.entries(opaqueParent)) {
        expect(Object.hasOwn(parent, key), `Opaque parent sibling ${key} is absent`).toBe(true);
        expect(parent[key], `Opaque parent sibling ${key} changed`).toEqual(value);
      }
      expect(parent).not.toHaveProperty('opaqueParentAbsent');
    };
    assertOpaqueParent(asRecord(composition.contract.parent_composition));
    const counts = { repaired: 0, unaffected: 0 };
    for (const x of [12, 24, 36]) {
      const occurrence = composition.occurrences.find((item) => item.occurrenceId === ready.occurrence_id)!;
      const config = projectCanonicalComposition({ ...composition, occurrences: [occurrence] },
        { ...createDefaultTimelineConfig(), clips: [], tracks: [], registry: {} },
        { clampToOccurrenceDuration: false }).config;
      const published: PreparedShotComposition[] = [];
      const popup = createShotTimelineDataProvider(config, composition, ready.occurrence_id, adapter,
        (next) => published.push(next));
      const session = `${ready.timeline_id}:shot:${ready.occurrence_id}`;
      const loaded = await popup.loadTimeline(session);
      const edited = { ...loaded.config,
        clips: loaded.config.clips.map((clip) => ({ ...clip, x })) };
      // Supported canonical popup publication, with no serializer shortcut.
      const configVersion = await popup.saveTimeline(session, edited, loaded.configVersion);
      expect(published).toHaveLength(1);
      const receipt = { configVersion, publication: published[0]!.publicationReceipt };
      const revision = published[0]!.headRevisionId;
      evidence(`popup-${x}-app-receipt.json`, receipt);
      expect(revision).not.toBe(composition.headRevisionId);
      const first = await client.getProjectParentCompositionRevision(ready.project_id, ready.timeline_id, revision);
      const second = await client.getProjectParentCompositionRevision(ready.project_id, ready.timeline_id, revision);
      evidence(`popup-${x}-exact-1.json`, first);
      evidence(`popup-${x}-exact-2.json`, second);
      expect(first.revision_id).toBe(revision);
      expect(second).toEqual(first);
      const reads = exchanges.filter((item) => item.method === 'GET'
        && item.path.endsWith(`/composition-revisions/${revision}`)).slice(-2);
      expect(reads).toHaveLength(2);
      expect(reads[0]!.responseUtf8).toBe(reads[1]!.responseUtf8);
      const publication = exchanges.filter((item) => item.method === 'POST'
        && item.path.endsWith('/composition-revisions')).at(-1)!;
      evidence(`popup-${x}-publication.json`, publication);
      expect(publication.status).toBe(200);
      expect(publication.idempotencyKey).toMatch(/^reigh\.shot-popup\./);
      assertOpaqueParent(asRecord(asRecord(publication.request).parent_composition));
      assertOpaqueParent(asRecord(first.payload));
      assertOpaqueParent(asRecord(second.payload));
      composition = await adapter.loadAtHead({
        projectId: ready.project_id, parentDocumentId: ready.timeline_id, headRevisionId: revision,
      });
      assertOpaqueParent(asRecord(composition.contract.parent_composition));
      const accepted = composition.occurrences.find((item) => item.occurrenceId === ready.occurrence_id)!;
      const internal = asRecord(accepted.revision.internal_timeline_revision);
      const clips = asRecord(internal.timeline).clips as JsonRecord[];
      evidence(`popup-${x}-accepted-shot.json`, accepted);
      expect(clips.length).toBeGreaterThan(0);
      expect(clips.every((clip) => clip.x === x)).toBe(true);
      const parent = asRecord(first.payload);
      const predicates = case2Fixture!.expected.must_preserve.map((check) => {
        const actual = readPreservationPath(parent, check.path);
        return { ...check, actual: actual === MISSING ? { missing: true } : actual,
          passed: isDeepStrictEqual(actual, check.value),
          category: unchangedCase2SentinelPaths.includes(check.path) ? 'unaffected' : 'repaired' };
      });
      evidence(`popup-${x}-predicates.json`, predicates);
      // Do not submit any subsequent edit after detecting a product loss.
      for (const check of predicates) {
        expect(check.passed, `Popup lost ${check.path}; see exact revision ${revision}`).toBe(true);
        counts[check.category as keyof typeof counts]++;
      }
    }
    expect(counts).toEqual({ repaired: 69, unaffected: 33 });
    evidence('popup-verification.json', { counts, splitChildAbsences: {
      applicable: 0, open: 16, reason: 'Shot-local geometry edit creates no parent split child.',
    } });
  }, 30_000,
);
