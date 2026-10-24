/**
 * P2 popup media proof.  The fixture is deliberately prepared through the
 * Runtime's current media-import and composition APIs; the gestures below
 * are the mounted popup controls and their A2 commit boundary.
 *
 * The mounted Add/Swap controls are being restored by A3.  Keeping this test
 * on the existing labels and data hooks makes that seam explicit without
 * adding a second product caller here.
 */
import { expect, type Page, type Request, type Response } from '@playwright/test';
import {
  makePng,
  sha256Hex,
  THREE_PRODUCTS_REFERENCE_AT,
  type DirectHarness,
  type ThreeProductsSeed,
} from './support/harness.ts';
import {
  expectConnected,
  openSeededTimeline,
  test as appTest,
} from './support/app.ts';
import { ASTRID_PYTHON } from './support/astrid.ts';
import type {
  CanonicalDocument,
  CommitAcceptedMutation,
  CommitRequest,
  CommitRead,
  PatchChange,
  AgentSelection,
  HeadPin,
  HistoryEntry,
  HistoryPage,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';

const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const CEILING = { timeout: 90_000 };
const TARGET_CLIP_ID = 'f2-agent-clip';

type JsonObject = Record<string, unknown>;
type JsonArray = Array<JsonObject>;

interface MediaFixture {
  asset: string;
  generation_id: string;
  variant_id: string;
  object_id: string;
  catalog_digest: string;
  entry: JsonObject;
}

interface PopupSeed extends ThreeProductsSeed {
  sourceOccurrenceId: string;
  sharedOccurrenceId: string;
  oldMedia: MediaFixture;
  file: { name: string; type: string; buffer: Buffer };
}

interface CommitPost {
  request: Request;
  response: Response;
  body: CommitRequest;
  json: unknown;
  key: string;
}

interface PopupWire {
  posts: CommitPost[];
  mutations: Request[];
  selections: Response[];
  imports: Response[];
}

const test = appTest.extend<object, { popup: PopupSeed }>({
  popup: [async ({ harness }, use) => {
    const seed = await preparePopupSeed(harness);
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);
    await use(seed);
  }, { scope: 'worker', timeout: 240_000 }],
});

test.describe.configure({ mode: 'serial' });

function object(value: unknown, label: string): JsonObject {
  expect(value, label).toBeTruthy();
  expect(typeof value, label).toBe('object');
  expect(Array.isArray(value), label).toBe(false);
  return value as JsonObject;
}

function array(value: unknown, label: string): JsonArray {
  expect(Array.isArray(value), label).toBe(true);
  return value as JsonArray;
}

function clone<T>(value: T): T {
  return structuredClone(value);
}

function pinOf(result: CommitAcceptedMutation): HeadPin {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

function canonical(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical((value as JsonObject)[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function digest(value: unknown): string {
  return sha256Hex(Buffer.from(canonical(value)));
}

async function revisionBody(harness: DirectHarness, revisionId: string): Promise<JsonObject> {
  const result = await harness.runtimeJson<JsonObject>(
    'GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions/${revisionId}`,
  );
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  return result.body;
}

async function canonicalAt(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string): Promise<CanonicalDocument> {
  const parent = await revisionBody(harness, revisionId);
  const manifest = object(parent.dependency_manifest, `dependency manifest for ${revisionId}`);
  const shots = await Promise.all(array(manifest.shots, 'manifest shots').map(async (pin) => {
    const result = await harness.runtimeJson<JsonObject>(
      'GET',
      `/v1/projects/${harness.seed.projectId}/shots/${String(pin.shot_id)}/revisions/${String(pin.revision_id)}`,
    );
    expect(result.status, JSON.stringify(result.body)).toBe(200);
    expect(result.body.content_digest).toBe(pin.content_digest);
    expect(result.body.internal_timeline_revision_id).toBe(pin.internal_timeline_revision_id);
    return { ...pin, payload: result.body.payload };
  }));
  const internals = await Promise.all(array(manifest.internal_timelines, 'manifest internal timelines').map(async (pin) => {
    const result = await harness.runtimeJson<JsonObject>(
      'GET',
      `/v1/projects/${harness.seed.projectId}/timelines/${String(pin.timeline_id)}/revisions/${String(pin.revision_id)}`,
    );
    expect(result.status, JSON.stringify(result.body)).toBe(200);
    expect(result.body.content_digest).toBe(pin.content_digest);
    return { ...pin, payload: result.body.payload };
  }));
  return {
    schema_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    parent_revision: {
      revision_id: String(parent.revision_id),
      content_digest: String(parent.content_digest),
      payload: parent.payload as CanonicalDocument['parent_revision']['payload'],
    },
    shot_revisions: shots as CanonicalDocument['shot_revisions'],
    internal_timeline_revisions: internals as CanonicalDocument['internal_timeline_revisions'],
    dependency_manifest: manifest as CanonicalDocument['dependency_manifest'],
  };
}

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const result = await harness.runtimeJson<HistoryPage>(
    'GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`,
  );
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  return result.body;
}

async function importMedia(harness: DirectHarness, file: { name: string; type: string; buffer: Buffer }): Promise<MediaFixture> {
  const response = await harness.runtimeFetch(`/v1/projects/${harness.seed.projectId}/media-imports`, {
    method: 'POST',
    headers: {
      'Content-Type': file.type,
      'Idempotency-Key': `p2-popup-${file.name}`,
      'X-Original-Name': file.name,
    },
    body: new Uint8Array(file.buffer).buffer,
  });
  const responseText = response.status === 201 ? null : await response.text();
  expect(response.status, responseText ?? undefined).toBe(201);
  const body = await response.json() as { data: JsonObject };
  const data = object(body.data, 'Runtime media-import result');
  const entry = object(data.entry, 'Runtime registered media entry');
  const asset = String(data.asset_id);
  const generation_id = String(data.generation_id);
  const variant_id = String(data.variant_id);
  const object_id = String(entry.object_id);
  const selectionResponse = await harness.runtimeJson<JsonObject>(
    'GET',
    `/v1/projects/${harness.seed.projectId}/media-selection?asset=${encodeURIComponent(asset)}&generation_id=${encodeURIComponent(generation_id)}&variant_id=${encodeURIComponent(variant_id)}`,
  );
  expect(selectionResponse.status, JSON.stringify(selectionResponse.body)).toBe(200);
  const selected = object(selectionResponse.body, 'Runtime selected media');
  expect(selected).toMatchObject({ asset, generation_id, variant_id, object_id });
  const media = {
    asset,
    generation_id,
    variant_id,
    object_id,
    catalog_digest: String(selected.catalog_digest),
  };
  // Canonical raw registry codec, bound to the real Runtime selection above.
  return { ...media, entry: { media_id: object_id, type: 'image', generationId: generation_id, variantId: variant_id } };
}

async function commitFixtureCommand(
  harness: DirectHarness,
  seed: ThreeProductsSeed,
  base: HeadPin,
  command: CommitRequest['commands'][number],
  label: string,
  patch: PatchChange[] = [],
): Promise<HeadPin> {
  const body: CommitRequest = {
    api_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    base_revision_id: base.revision_id,
    base_publication_id: base.publication_id,
    commands: [command],
    label,
    steps: [{ id: label.toLowerCase().replace(/[^a-z0-9]+/g, '-'), label, intent: label, tags: [], command_ordinals: [0], patch }],
    merge: 'atomic',
    dry_run: false,
    source: { via: 'python' },
  };
  const result = await harness.runtimeJson<CommitAcceptedMutation>(
    'POST',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commit`,
    body,
  );
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  expect(result.body.data.status).toBe('accepted');
  expect(result.body.data.base_revision_id).toBe(base.revision_id);
  expect(result.body.data.base_publication_id).toBe(base.publication_id);
  expect(result.body.data.rebased_onto).toBeNull();
  return pinOf(result.body);
}

async function preparePopupSeed(harness: DirectHarness): Promise<PopupSeed> {
  const seed = await harness.seedThreeProducts(THREE_PRODUCTS_REFERENCE_AT, 'native-none');
  const before = await canonicalAt(harness, seed, seed.headRevisionId);
  const occurrences = array(before.parent_revision.payload.occurrences, 'seed occurrences');
  const sourceOccurrence = object(occurrences.find((row) => row.occurrence_id === seed.occurrenceId), 'seed occurrence');
  const shot = before.shot_revisions.find((row) => row.shot_id === sourceOccurrence.shot_id
    && row.revision_id === sourceOccurrence.shot_revision_id);
  expect(shot, 'seed shot revision').toBeTruthy();
  const internal = before.internal_timeline_revisions.find((row) => row.revision_id === shot!.internal_timeline_revision_id);
  expect(internal, 'seed internal timeline revision').toBeTruthy();

  const objectResponse = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(harness.seed.image.objectId)}`);
  expect(objectResponse.status).toBe(200);
  const file = { name: 'p2-popup-old.png', type: 'image/png', buffer: Buffer.from(await objectResponse.arrayBuffer()) };
  const oldMedia = await importMedia(harness, file);
  const childClips = array((internal!.payload as unknown as JsonObject).clips, 'seed child clips');
  const target = object(childClips.find((row) => row.id === TARGET_CLIP_ID), 'selected child clip');
  const originalTargetAsset = target.asset;

  const sharedOccurrenceId = 'f2-occurrence-copy';
  const initial = await history(harness, seed);
  const placed = await commitFixtureCommand(harness, seed, initial.head, {
    schema_version: 1,
    op: 'occurrence.place-shared',
    version: '1',
    select: `occurrence:${seed.occurrenceId}`,
    args: { occurrence_id: sharedOccurrenceId, on: 12 },
    intent: { ownership: 'occurrence' },
    created: [`occurrence:${sharedOccurrenceId}`],
  }, 'P2 popup shared placement');

  const opaque = { keep: [null, false, 0, { source: 'fixture' }] };
  const changes: PatchChange[] = [
    { op: 'set', ref: 'parent', path: ['p2_popup_opaque'], before: { state: 'absent' }, value: opaque },
    { op: 'set', ref: `internal-revision:${internal!.revision_id}`, path: ['clips', `id:${TARGET_CLIP_ID}`, 'asset'],
      before: { state: 'present', value: originalTargetAsset as string }, value: oldMedia.asset },
    { op: 'set', ref: `internal-revision:${internal!.revision_id}`, path: ['registry', 'assets', oldMedia.asset],
      before: { state: 'absent' }, value: oldMedia.entry as PatchChange['value'] },
  ];
  const setupHead = (await commitFixtureCommand(harness, seed, placed, {
    schema_version: 1,
    op: 'doc.patch',
    version: '1',
    select: null,
    created: [
      `occurrence:${seed.occurrenceId}/asset:${oldMedia.asset}`,
      `occurrence:${sharedOccurrenceId}/asset:${oldMedia.asset}`,
    ],
    args: { changes },
  }, 'P2 popup authored media', changes));
  return {
    ...seed,
    headRevisionId: setupHead.revision_id,
    sourceOccurrenceId: seed.occurrenceId,
    sharedOccurrenceId,
    oldMedia,
    // Runtime asset IDs are object IDs: a renamed identical PNG is the same
    // asset. Import distinct decodable bytes to exercise a real ADD/SWAP.
    file: { name: 'p2-popup-new.png', type: 'image/png', buffer: makePng(65, 49) },
  };
}

function wireFor(page: Page): PopupWire {
  const wire: PopupWire = { posts: [], mutations: [], selections: [], imports: [] };
  page.on('request', (request) => {
    if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method())
      && /\/v1\/projects\//.test(new URL(request.url()).pathname)) wire.mutations.push(request);
  });
  page.on('response', (response) => {
    const path = new URL(response.url()).pathname;
    if (path.endsWith('/media-selection')) wire.selections.push(response);
    if (path.endsWith('/media-imports')) wire.imports.push(response);
  });
  return wire;
}

function assertOnlyCommits(wire: PopupWire, expected: CommitPost[]): void {
  // Media acquisition precedes the film edit; every other mutation must be the
  // exact observed commit. This catches unknown routes as well as old saves.
  const film = wire.mutations.filter((request) => !/\/projects\/[^/]+\/media-imports$/.test(new URL(request.url()).pathname));
  expect(film).toEqual(expected.map((post) => post.request));
  expect(film.every((request) => request.method() === 'POST' && COMMITS.test(new URL(request.url()).pathname))).toBe(true);
}

async function openPopup(page: Page, harness: DirectHarness, seed: PopupSeed, navigate = true): Promise<import('@playwright/test').Locator> {
  if (navigate) await page.goto(`${harness.origin}/tools/video-editor`);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const label = page.locator(`[data-shot-group-key^="${seed.sharedOccurrenceId}:"]`).first();
  await expect(label, 'shared occurrence shot group').toBeVisible();
  await label.dblclick();
  const dialog = page.getByRole('dialog');
  await expect(dialog.locator(`[data-canonical-occurrence-id="${seed.sharedOccurrenceId}"]`)).toBeVisible();
  await expect(dialog.locator('[data-shot-timeline-editor="true"]')).toBeVisible();
  await expect(dialog.locator('[data-shot-timeline-editor="true"]')).toHaveAttribute('data-shot-timeline-current-time', '0');
  return dialog;
}

async function commitFromGesture(page: Page, wire: PopupWire, gesture: () => Promise<void>): Promise<CommitPost> {
  const responsePromise = page.waitForResponse(
    (response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname),
    CEILING,
  );
  await gesture();
  const response = await responsePromise;
  const request = response.request();
  const post: CommitPost = {
    request,
    response,
    body: request.postDataJSON() as CommitRequest,
    json: await response.json(),
    key: request.headers()['idempotency-key'] ?? '',
  };
  wire.posts.push(post);
  return post;
}

function assertFullRequest(post: CommitPost, before: HeadPin, seed: PopupSeed, harness: DirectHarness): void {
  expect(post.key).toMatch(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/);
  expect(post.body).toMatchObject({
    api_version: 1, project_id: harness.seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: before.revision_id, base_publication_id: before.publication_id,
    commands: expect.any(Array), label: expect.any(String), steps: expect.any(Array),
    merge: 'fields', dry_run: false, source: { via: 'app' },
  });
  expect(post.body.label!.trim()).not.toBe('');
  expect(post.body.steps).toHaveLength(1);
  const step = post.body.steps![0];
  expect(step).toMatchObject({ id: expect.any(String), label: post.body.label,
    intent: post.body.label, tags: [], command_ordinals: post.body.commands.map((_, index) => index), patch: [] });
  expect(step.id).not.toBe('');
  // C0 §1: semantic reads are captured by the provider. Optional caller reads
  // remain exact assertions when supplied; annotations must never be invented.
  if (Object.prototype.hasOwnProperty.call(post.body, 'reads')) assertReads(post.body.reads!);
  if (Object.prototype.hasOwnProperty.call(step, 'reads')) assertReads(step.reads!);
  for (const key of ['rationale', 'group_id'] as const) {
    if (Object.prototype.hasOwnProperty.call(post.body, key)) expect(typeof post.body[key]).toBe('string');
  }
}

function assertReads(reads: CommitRead[]): void {
  expect(Array.isArray(reads)).toBe(true);
  for (const read of reads) {
    expect(read).toMatchObject({ ref: expect.any(String), path: expect.any(Array) });
    expect(['field', 'collection', 'scope']).toContain(read.kind);
    if (read.kind === 'field') {
      expect(read.state).toMatchObject({ state: expect.stringMatching(/^(present|absent)$/) });
      expect(Object.keys(read.state).sort()).toEqual(read.state.state === 'present' ? ['state', 'value'] : ['state']);
    }
    if (read.kind === 'collection') {
      expect(new Set(read.members).size).toBe(read.members.length);
      if (read.order !== null) {
        expect([...read.order].sort()).toEqual([...read.members].sort());
        expect(new Set(read.order).size).toBe(read.order.length);
      }
    }
  }
}

function accepted(post: CommitPost, before: HeadPin): CommitAcceptedMutation {
  expect(post.response.status(), JSON.stringify(post.json)).toBe(200);
  const result = post.json as CommitAcceptedMutation;
  expect(Object.keys(object(result, 'commit envelope')).sort()).toEqual(['data', 'receipt']);
  expect(result.receipt).toMatchObject({ receipt_id: post.key, idempotency_key: post.key,
    command_kind: 'timeline.commit', project_id: post.body.project_id,
    request_hash: expect.any(String), project_seq: [expect.any(Number), expect.any(Number)],
    event_ids: expect.any(Array), created_at: expect.any(String), result: result.data });
  expect(result.data).toMatchObject({ status: 'accepted', base_revision_id: before.revision_id,
    base_publication_id: before.publication_id, previous_revision_id: before.revision_id,
    previous_publication_id: before.publication_id, accepted_revision_id: expect.any(String), rebased_onto: null,
    canonical_document: { schema_version: 1, project_id: post.body.project_id, timeline_id: post.body.timeline_id },
    document_digest: expect.stringMatching(/^sha256:[0-9a-f]{64}$/), commands: expect.any(Array),
    id_map: expect.any(Object), provider_version: expect.any(String), compiler_version: expect.any(String),
    merge_mode: post.body.merge, steps: expect.any(Array), publisher: expect.any(String),
    source: post.body.source, label: post.body.label });
  for (const key of ['rationale', 'group_id'] as const) {
    expect(Object.prototype.hasOwnProperty.call(result.data, key)).toBe(Object.prototype.hasOwnProperty.call(post.body, key));
    if (Object.prototype.hasOwnProperty.call(post.body, key)) expect(result.data[key]).toBe(post.body[key]);
  }
  expect(result.data.canonical_document.parent_revision.revision_id).toBe(result.data.accepted_revision_id);
  expect(result.data.document_digest).toBe(digest(result.data.canonical_document));
  expect(result.receipt.result).toEqual(result.data);
  return result;
}

async function assertSharedMediaCommands(
  post: CommitPost, seed: PopupSeed, wire: PopupWire, op: 'occurrence.add-media' | 'occurrence.swap-media',
): Promise<void> {
  const owner = `occurrence:${seed.sharedOccurrenceId}`;
  expect(post.body.commands.map((command) => command.op)).toEqual(['occurrence.fork', op]);
  const fork = post.body.commands[0];
  expect(fork).toEqual({ schema_version: 1, op: 'occurrence.fork', version: '1', select: owner,
    args: { shot_id: fork.args.shot_id }, intent: { ownership: 'occurrence' }, created: [`shot:${fork.args.shot_id}`] });
  expect(fork.args.shot_id).toEqual(expect.stringMatching(/^shot-fork-/));
  expect(wire.imports).toHaveLength(1);
  expect(wire.imports[0].status()).toBe(201);
  const imported = object((await wire.imports[0].json()).data, 'gesture media import');
  expect(imported).toMatchObject({ provider: 'runtime', status: 'completed', project: post.body.project_id,
    entry: { media_type: seed.file.type, filename: seed.file.name } });
  const selected = await Promise.all(wire.selections.map(async (response) => {
    expect(response.status()).toBe(200);
    const media = object(await response.json(), 'authenticated media selection');
    const query = new URL(response.url()).searchParams;
    expect(media).toMatchObject({ asset: query.get('asset'), generation_id: query.get('generation_id'), variant_id: query.get('variant_id') });
    return media;
  }));
  const media = { asset: imported.asset_id, generation_id: imported.generation_id, variant_id: imported.variant_id,
    object_id: object(imported.entry, 'import entry').object_id,
    catalog_digest: object(selected.find((value) => value.asset === imported.asset_id), 'selected imported asset').catalog_digest };
  expect(media).toMatchObject({ asset: expect.any(String), generation_id: expect.any(String), variant_id: expect.any(String),
    object_id: expect.stringMatching(/^sha256:[0-9a-f]{64}$/), catalog_digest: expect.stringMatching(/^sha256:[0-9a-f]{64}$/) });
  expect(media.asset).not.toBe(seed.oldMedia.asset);
  expect(media.generation_id).not.toBe(seed.oldMedia.generation_id);
  expect(media.variant_id).not.toBe(seed.oldMedia.variant_id);
  expect(media.object_id).not.toBe(seed.oldMedia.object_id);
  expect(media.object_id).toBe(sha256Hex(seed.file.buffer));
  expect(selected).toContainEqual(media);
  const command = post.body.commands[1];
  const args = op === 'occurrence.swap-media'
    ? { old_media: { asset: seed.oldMedia.asset, generation_id: seed.oldMedia.generation_id,
      variant_id: seed.oldMedia.variant_id, object_id: seed.oldMedia.object_id, catalog_digest: seed.oldMedia.catalog_digest }, media }
    : { row: expectedAddedRow(command, media.asset), media };
  expect(command).toEqual({ schema_version: 1, op, version: '1',
    select: op === 'occurrence.swap-media' ? `${owner}/clip:${TARGET_CLIP_ID}` : owner,
    args, intent: { ownership: 'occurrence' } });
  if (op === 'occurrence.swap-media') expect(selected).toContainEqual(args.old_media);
}

function expectedAddedRow(command: CommitRequest['commands'][number], asset: unknown): JsonObject {
  const id = object(command.args.row, 'reserved added row').id;
  expect(typeof id).toBe('string');
  expect(id).not.toBe(TARGET_CLIP_ID);
  // The UI starts at child-local zero with V2 selected and imports a PNG.
  return { id, asset, track: 'V2', at: 0, clipType: 'hold', hold: 5, opacity: 1 };
}

function identity(kind: string, ...parts: unknown[]): string {
  return `${kind}-${sha256Hex(Buffer.from([kind, ...parts.map(canonical)].join('\0'))).slice(7)}`;
}

function expectedPopupDocument(before: CanonicalDocument, seed: PopupSeed, post: CommitPost, forkOnly = false): CanonicalDocument {
  const expected = clone(before);
  const occurrences = array(expected.parent_revision.payload.occurrences, 'all original occurrences');
  const source = object(occurrences.find((row) => row.occurrence_id === seed.sourceOccurrenceId), 'source occurrence');
  const shared = object(occurrences.find((row) => row.occurrence_id === seed.sharedOccurrenceId), 'selected occurrence');
  expect(shared.placement).toEqual({ start_ms: 12000 });
  expect(shared.shot_id).toBe(source.shot_id);
  expect(shared.shot_revision_id).toBe(source.shot_revision_id);
  const shot = clone(before.shot_revisions.find((row) => row.revision_id === shared.shot_revision_id)!);
  const internal = clone(before.internal_timeline_revisions.find((row) => row.revision_id === shot.internal_timeline_revision_id)!);
  expect(shot.payload.items, 'fixture has no shot-item identities to remap').toEqual([]);
  const command = post.body.commands[1];
  const media = object(command.args.media, 'new authenticated media');
  const assets = object(object(internal.payload.registry, 'registry').assets, 'registry assets');
  expect(Object.prototype.hasOwnProperty.call(assets, String(media.asset))).toBe(false);
  if (!forkOnly) assets[String(media.asset)] = { media_id: media.object_id, type: 'image', generationId: media.generation_id, variantId: media.variant_id };
  const rows = array(internal.payload.clips, 'raw child rows');
  if (!forkOnly && command.op === 'occurrence.add-media') rows.push(expectedAddedRow(command, media.asset));
  else if (!forkOnly) object(rows.find((row) => row.id === TARGET_CLIP_ID), 'exact selected raw child').asset = media.asset;
  const forkId = String(post.body.commands[0].args.shot_id);
  internal.timeline_id = before.timeline_id;
  internal.revision_id = identity('authoring-timeline-revision', before.project_id, before.timeline_id, forkId, internal.payload);
  internal.content_digest = digest(internal.payload);
  shot.shot_id = forkId;
  shot.internal_timeline_revision_id = internal.revision_id;
  shot.payload.internal_timeline_revision_id = internal.revision_id;
  shot.content_digest = digest(shot.payload);
  shot.revision_id = identity('authoring-shot-revision', before.project_id, forkId, shot.payload);
  shared.shot_id = forkId;
  shared.shot_revision_id = shot.revision_id;
  expected.shot_revisions.push(shot);
  expected.shot_revisions.sort((a, b) => a.shot_id.localeCompare(b.shot_id) || a.revision_id.localeCompare(b.revision_id));
  expected.internal_timeline_revisions.push(internal);
  expected.internal_timeline_revisions.sort((a, b) => a.timeline_id.localeCompare(b.timeline_id) || a.revision_id.localeCompare(b.revision_id));
  expected.dependency_manifest.shots = expected.shot_revisions.map(({ payload: _payload, ...pin }) => pin);
  expected.dependency_manifest.internal_timelines = expected.internal_timeline_revisions.map(({ payload: _payload, ...pin }) => pin);
  expect(before.dependency_manifest.media.map((pin) => pin.media_id)).not.toContain(media.object_id);
  if (!forkOnly) {
    expected.dependency_manifest.media.push({ media_id: String(media.object_id), content_digest: String(media.object_id) });
    expected.dependency_manifest.media.sort((a, b) => a.media_id.localeCompare(b.media_id));
  }
  expected.parent_revision.content_digest = digest(expected.parent_revision.payload);
  expected.parent_revision.revision_id = `authoring-parent-revision-${digest({ project_id: before.project_id,
    timeline_id: before.timeline_id, parent: expected.parent_revision.payload, manifest: expected.dependency_manifest }).slice(7)}`;
  return expected;
}

function imageAt(document: CanonicalDocument, ref: string) {
  return ref === 'parent' ? document.parent_revision
    : document.shot_revisions.find((row) => ref === `shot-revision:${row.revision_id}`)
      ?? document.internal_timeline_revisions.find((row) => ref === `internal-revision:${row.revision_id}`);
}

function site(document: CanonicalDocument, ref: string, path: string[]): { ref: string; path: string[] } {
  const [owner, entity] = ref.split('/');
  if (owner.startsWith('occurrence:')) {
    const id = owner.slice(11);
    const occurrence = array(document.parent_revision.payload.occurrences, 'bound occurrences').find((row) => row.occurrence_id === id)!;
    if (!entity) return { ref: 'parent', path: ['occurrences', `occurrence_id:${id}`, ...path] };
    const shot = document.shot_revisions.find((row) => row.revision_id === occurrence.shot_revision_id)!;
    const child = `internal-revision:${shot.internal_timeline_revision_id}`;
    if (entity === 'source') return { ref: child, path };
    if (entity === 'shot') return path[0] === 'payload'
      ? { ref: `shot-revision:${shot.revision_id}`, path: path.slice(1) }
      : { ref: 'parent', path: ['occurrences', `occurrence_id:${id}`, ...path] };
    if (entity.startsWith('asset:')) return { ref: child, path: ['registry', 'assets', entity.slice(6), ...path] };
    if (entity === 'registry') return { ref: child, path: ['registry', ...path] };
    if (entity.startsWith('collection:')) return { ref: child, path: [`${entity.slice(11)}s`] };
    const [kind, key] = entity.split(':');
    return { ref: child, path: [`${kind}s`, `id:${key}`, ...path] };
  }
  if (owner.startsWith('shot:')) return { ref: 'timeline', path: [] };
  if (ref === 'parent/collection:occurrence') return { ref: 'parent', path: ['occurrences'] };
  return { ref, path };
}

function expectedSelection(document: CanonicalDocument, key: string, owner: string): AgentSelection {
  const occurrences = array(document.parent_revision.payload.occurrences, 'selected collection occurrences');
  const row = occurrences.find((candidate) => `occurrence:${candidate.occurrence_id}` === owner);
  const shot = document.shot_revisions.find((image) => image.revision_id === row?.shot_revision_id);
  const internal = document.internal_timeline_revisions.find((image) => image.revision_id === shot?.internal_timeline_revision_id);
  let members: string[];
  let boundaries: string[];
  if (key === 'collection.occurrences') {
    members = occurrences.map((candidate) => `occurrence:${candidate.occurrence_id}`);
    boundaries = members;
  } else if (key === 'collection.clips' || key === 'collection.tracks') {
    const kind = key === 'collection.clips' ? 'clip' : 'track';
    members = array(internal!.payload[`${kind}s`], key).map((candidate) => `${owner}/${kind}:${candidate.id}`);
    boundaries = members;
  } else {
    expect(key).toBe('placement.owners');
    members = occurrences.filter((candidate) => candidate.shot_revision_id === row!.shot_revision_id)
      .map((candidate) => `occurrence:${candidate.occurrence_id}`);
    boundaries = [`shot:${shot!.shot_id}`];
  }
  return { key, query_version: 1, owner, members, order: members, boundaries, policy: 'guard-membership' };
}

function expectedEffects(before: CanonicalDocument, after: CanonicalDocument, seed: PopupSeed): PatchChange[] {
  const beforeRows = array(before.parent_revision.payload.occurrences, 'before effect occurrences');
  const afterRows = array(after.parent_revision.payload.occurrences, 'after effect occurrences');
  const old = beforeRows.find((row) => row.occurrence_id === seed.sharedOccurrenceId)!;
  const next = afterRows.find((row) => row.occurrence_id === seed.sharedOccurrenceId)!;
  const changes: PatchChange[] = [];
  for (const image of after.internal_timeline_revisions.filter((row) => !before.internal_timeline_revisions.some((prior) => prior.revision_id === row.revision_id))) {
    changes.push({ op: 'set', ref: `internal-revision:${image.revision_id}`, path: [], before: { state: 'absent' }, value: image.payload as PatchChange['value'] });
  }
  for (const image of after.shot_revisions.filter((row) => !before.shot_revisions.some((prior) => prior.revision_id === row.revision_id))) {
    changes.push({ op: 'set', ref: `shot-revision:${image.revision_id}`, path: [], before: { state: 'absent' }, value: image.payload as PatchChange['value'] });
  }
  for (const field of ['shot_id', 'shot_revision_id']) changes.push({ op: 'set', ref: 'parent',
    path: ['occurrences', `occurrence_id:${seed.sharedOccurrenceId}`, field],
    before: { state: 'present', value: old[field] as string }, value: next[field] as string });
  for (const image of before.shot_revisions.filter((row) => !after.shot_revisions.some((next) => next.revision_id === row.revision_id))) {
    changes.push({ op: 'remove', ref: `shot-revision:${image.revision_id}`, path: [], before: { state: 'present', value: image.payload as NonNullable<PatchChange['value']> } });
  }
  for (const image of before.internal_timeline_revisions.filter((row) => !after.internal_timeline_revisions.some((next) => next.revision_id === row.revision_id))) {
    changes.push({ op: 'remove', ref: `internal-revision:${image.revision_id}`, path: [], before: { state: 'present', value: image.payload as NonNullable<PatchChange['value']> } });
  }
  return changes;
}

function assertHistory(
  entry: HistoryEntry, post: CommitPost, result: CommitAcceptedMutation,
  before: CanonicalDocument, after: CanonicalDocument, inputs: CanonicalDocument[], seed: PopupSeed, undoOf: string[],
): void {
  const data = result.data;
  expect(entry).toMatchObject({ publication_id: post.key, revision_id: data.accepted_revision_id,
    previous: { revision_id: data.previous_revision_id, publication_id: data.previous_publication_id },
    receipt: result.receipt, intent: 'recorded', provider_version: data.provider_version,
    compiler_version: data.compiler_version, merge: post.body.merge, merge_mode: data.merge_mode,
    publisher: data.publisher, source: post.body.source, label: post.body.label, steps: data.steps,
    records: { schema_version: 1, label: data.label, merge_mode: data.merge_mode,
      steps: data.steps, undo_of: undoOf, undo_steps: null, restored_from: null } });
  for (const key of ['reads', 'rationale', 'group_id'] as const) {
    expect(Object.prototype.hasOwnProperty.call(entry, key)).toBe(Object.prototype.hasOwnProperty.call(post.body, key));
    if (Object.prototype.hasOwnProperty.call(post.body, key)) expect(entry[key]).toEqual(post.body[key]);
  }
  const records = entry.records!;
  expect(records.commands.map((record) => record.ordinal)).toEqual(post.body.commands.map((_, index) => index));
  expect(data.commands).toEqual(records.commands.map((record) => record.command));
  expect(data.steps).toHaveLength(post.body.steps!.length);
  for (const [index, requested] of post.body.steps!.entries()) {
    const step = data.steps![index];
    expect(step).toEqual({ ...requested, patch: expectedEffects(before, after, seed), dependencies: step.dependencies });
    assertReads(step.dependencies!);
    expect(step.dependencies!.length).toBeGreaterThan(0);
    const covers = (read: CommitRead) => step.dependencies!.some((dependency) =>
      dependency.kind === 'scope' && dependency.path.length === 0 && (dependency.ref === 'timeline' || dependency.ref === read.ref)
      || canonical(dependency) === canonical(read));
    for (const read of [...(post.body.reads ?? []), ...(requested.reads ?? [])]) {
      expect(covers({ ...read, ...site(before, read.ref, read.path) })).toBe(true);
    }
    for (const ordinal of step.command_ordinals) {
      const record = records.commands[ordinal];
      const input = inputs[ordinal];
      const submitted = post.body.commands[ordinal];
      // Runtime may enrich semantic operands with its captured guards, but
      // every submitted operand and any optional caller read remains exact.
      expect(record.command).toMatchObject(submitted);
      expect(record.command.args).toEqual(submitted.args);
      expect(record.command.select).toBe(submitted.select);
      expect(record).toMatchObject({ writes: expect.any(Array), reads: expect.any(Array), selections: expect.any(Array),
        bindings: expect.any(Array), created: expect.any(Array), dependencies: expect.any(Array), derived_writes: expect.any(Array) });
      expect(record.reads.length).toBeGreaterThan(0);
      expect(record.writes.length).toBeGreaterThan(0);
      for (const read of record.reads) {
        if (read.state.state === 'absent' && record.created.some((created) => created.ref === read.ref)) continue;
        const bound = site(input, read.ref, read.path);
        if (read.ref.includes('/collection:')) {
          expect(step.dependencies!.some((dependency) => covers({ kind: 'scope', ref: bound.ref, path: [] })
            || dependency.kind === 'collection' && dependency.ref === bound.ref && canonical(dependency.path) === canonical(bound.path))).toBe(true);
        } else expect(covers(bound.ref === 'timeline' || !bound.path.length
          ? { kind: 'scope', ...bound } : { kind: 'field', ...bound, state: read.state }), `captured read ${canonical(read)}`).toBe(true);
      }
      for (const binding of record.bindings) {
        expect(binding.dependencies.every((key) => record.dependencies.filter((dependency) => dependency.key === key).length === 1)).toBe(true);
        if (binding.key === 'inverse.stage') {
          expect(binding.boundary).toMatchObject({ publication_id: undoOf[0], step_id: expect.any(String), command_ordinals: [0, 1] });
          continue;
        }
        expect(binding.boundary).toMatchObject({ base_revision_id: post.body.base_revision_id,
          base_publication_id: post.body.base_publication_id, evaluated_head: entry.previous,
          step_id: step.id, command_ordinal: ordinal });
        const boundaryDocument = binding.boundary?.phase === 'effect'
          ? binding.boundary.side === 'after' ? after : before : input;
        const image = imageAt(boundaryDocument, binding.physical_ref!);
        expect(image, `physical source binding ${binding.key}`).toBeTruthy();
        expect(binding.revision_id).toBe(image!.revision_id);
        expect(binding.content_digest).toBe(image!.content_digest);
        if (binding.dependency) expect(covers(binding.dependency)).toBe(true);
        if (binding.key === 'commit.effect') {
          expect(binding.step_id).toBe(step.id);
          const effect = step.patch[binding.effect_ordinal!];
          expect(binding.ref).toBe(effect.ref);
          expect(binding.path).toEqual(effect.path);
        }
      }
      const mediaKeys = submitted.op === 'occurrence.swap-media' ? ['media.old', 'media.new']
        : submitted.op === 'occurrence.add-media' ? ['media.new'] : [];
      if (!undoOf.length) {
        expect(record.dependencies.map((dependency) => dependency.key).sort()).toEqual(mediaKeys.sort());
        const owner = `occurrence:${seed.sharedOccurrenceId}`;
        const requiredBindings = submitted.op === 'occurrence.fork' ? ['fork.source', 'fork.owner']
          : submitted.op === 'occurrence.swap-media' ? ['media.owner', 'media.track', 'media.target'] : ['media.owner', 'media.track', 'create.owner'];
        for (const key of requiredBindings) expect(record.bindings.filter((binding) => binding.key === key)).toHaveLength(1);
        if (submitted.op === 'occurrence.swap-media') {
          expect(record.bindings.find((binding) => binding.key === 'media.target'))
            .toMatchObject({ ref: `${owner}/clip:${TARGET_CLIP_ID}`, dependencies: ['media.old', 'media.new'] });
        }
      }
      for (const dependency of record.dependencies) {
        if (dependency.key.startsWith('media.')) expect(dependency).toEqual({ key: dependency.key, kind: 'media', policy: 'exact',
          pin: dependency.key === 'media.old' ? submitted.args.old_media : submitted.args.media });
      }
      // D13: the shared-popup decision reads the exact raw child/shot and the
      // selected occurrence. These remain protected at the provider boundary.
      if (submitted.op === 'occurrence.fork') {
        const owner = `occurrence:${seed.sharedOccurrenceId}`;
        expect(record.reads).toContainEqual({ ref: `${owner}/source`, path: [],
          state: { state: 'present', value: input.internal_timeline_revisions.find((row) => row.revision_id === input.shot_revisions.find((row) => row.shot_id === seed.shotId)!.internal_timeline_revision_id)!.payload } });
        const sourceShot = input.shot_revisions.find((row) => row.shot_id === seed.shotId)!;
        expect(record.reads).toContainEqual({ ref: `${owner}/shot`, path: ['payload'], state: { state: 'present', value: sourceShot.payload } });
        expect(record.selections.map((selection) => selection.key)).toEqual(expect.arrayContaining(['collection.clips', 'collection.tracks']));
        const raw = input.internal_timeline_revisions.find((row) => row.revision_id === sourceShot.internal_timeline_revision_id)!;
        for (const kind of ['clip', 'track']) {
          const members = array(raw.payload[`${kind}s`], `source ${kind}s`).map((row) => `${owner}/${kind}:${row.id}`);
          expect(record.selections.find((selection) => selection.key === `collection.${kind}s`))
            .toMatchObject({ owner, members, order: members, boundaries: members, policy: 'guard-membership' });
        }
        expect(record.created).toContainEqual({ ref: `shot:${submitted.args.shot_id}`, kind: 'shot', owner: null });
        expect(record.bindings.find((binding) => binding.key === 'fork.source')?.ref).toBe(`${owner}/source`);
      }
      if (!undoOf.length) {
        for (const selection of record.selections) expect(selection).toEqual(expectedSelection(input, selection.key, selection.owner));
      }
      for (const read of submitted.reads ?? []) expect(record.reads).toContainEqual(read);
    }
    for (const [effectOrdinal, effect] of step.patch.entries()) {
      const bindings = records.commands.flatMap((record) => record.bindings).filter((binding) => binding.key === 'commit.effect'
        && binding.effect_ordinal === effectOrdinal && binding.step_id === step.id);
      for (const side of ['before', 'after']) {
        const document = side === 'before' ? before : after;
        expect(bindings.filter((binding) => binding.boundary?.side === side)).toHaveLength(imageAt(document, effect.ref) ? 1 : 0);
      }
    }
  }
}

async function assertReloadUndo(
  page: Page, harness: DirectHarness, seed: PopupSeed, wire: PopupWire, before: HistoryPage,
  original: CanonicalDocument, post: CommitPost, result: CommitAcceptedMutation, expected: CanonicalDocument,
): Promise<void> {
  const committed = await history(harness, seed);
  expect(committed.items.filter((candidate) => !before.items.some((known) => known.publication_id === candidate.publication_id))
    .map((entry) => entry.publication_id)).toEqual([post.key]);
  const entry = committed.items.find((candidate) => candidate.publication_id === post.key)!;
  assertHistory(entry, post, result, original, expected, [original, expectedPopupDocument(original, seed, post, true)], seed, []);
  expect(committed.head).toEqual(pinOf(result));
  assertOnlyCommits(wire, [post]);
  expect(await canonicalAt(harness, seed, committed.head.revision_id)).toEqual(expected);
  await page.reload();
  const dialog = await openPopup(page, harness, seed, false);
  const editedId = post.body.commands[1].op === 'occurrence.swap-media' ? TARGET_CLIP_ID : String(object(post.body.commands[1].args.row, 'added row').id);
  const selected = array(expected.parent_revision.payload.occurrences, 'reloaded occurrences')
    .find((row) => row.occurrence_id === seed.sharedOccurrenceId)!;
  await expect(dialog.locator(`[data-canonical-occurrence-id="${seed.sharedOccurrenceId}"]`))
    .toHaveAttribute('data-canonical-shot-id', String(selected.shot_id));
  await expect(dialog.locator(`[data-canonical-occurrence-id="${seed.sharedOccurrenceId}"]`))
    .toHaveAttribute('data-canonical-revision-id', String(selected.shot_revision_id));
  await expect(dialog.locator('[data-shot-timeline-preview="true"]'))
    .toHaveAttribute('data-shot-timeline-head-revision-id', expected.parent_revision.revision_id);
  await expect(dialog.locator(`.clip-action[data-clip-id="${editedId}"]`)).toBeVisible();
  const canvas = dialog.locator('[data-shot-timeline-canvas="true"]');
  await expect(canvas).toHaveAttribute('data-shot-timeline-clip-count', post.body.commands[1].op === 'occurrence.add-media' ? '4' : '3');
  await expect(canvas).toHaveAttribute('data-shot-timeline-tracks', 'plate:visual|V2:visual');
  const editedFields = post.body.commands[1].op === 'occurrence.add-media'
    ? `${editedId}:V2:0:no-from:no-to:5:hold:asset:image`
    : `${TARGET_CLIP_ID}:V2:3:no-from:no-to:3:media:asset:image`;
  await expect(canvas).toHaveAttribute('data-shot-timeline-clip-assets', new RegExp(editedFields));
  await dialog.locator(`.clip-action[data-clip-id="${editedId}"]`).click();
  await expect(dialog.getByText(`Selected clip: ${editedId}`, { exact: true })).toBeVisible();
  const reloaded = await history(harness, seed);
  expect(reloaded).toEqual(committed);
  expect(await canonicalAt(harness, seed, reloaded.head.revision_id)).toEqual(expected);
  await dialog.getByRole('button', { name: 'Close', exact: true }).click();
  const inverse = await commitFromGesture(page, wire, async () => {
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
  });
  assertFullRequest(inverse, pinOf(result), seed, harness);
  expect(inverse.body.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [post.key] } }]);
  const inverseResult = accepted(inverse, pinOf(result));
  expect(inverseResult.data.canonical_document).toEqual(original);
  const finalHistory = await history(harness, seed);
  const inverseEntry = finalHistory.items.find((candidate) => candidate.publication_id === inverse.key)!;
  assertHistory(inverseEntry, inverse, inverseResult, expected, original, [expected], seed, [post.key]);
  const queries = [...new Map(entry.records!.commands.flatMap((record) => record.selections)
    .map((selection) => [`${selection.key}:${selection.owner}`, expectedSelection(expected, selection.key, selection.owner)])).values()];
  const byQuery = (a: AgentSelection, b: AgentSelection) => `${a.key}:${a.owner}`.localeCompare(`${b.key}:${b.owner}`);
  expect([...inverseEntry.records!.commands[0].selections].sort(byQuery)).toEqual(queries.sort(byQuery));
  expect(finalHistory.items.find((candidate) => candidate.publication_id === post.key)).toEqual(entry);
  expect(finalHistory.head).toEqual(pinOf(inverseResult));
  expect(await canonicalAt(harness, seed, finalHistory.head.revision_id)).toEqual(original);
  expect(finalHistory.items.filter((candidate) => !before.items.some((known) => known.publication_id === candidate.publication_id))).toHaveLength(2);
  assertOnlyCommits(wire, [post, inverse]);
  expect(await history(harness, seed)).toEqual(finalHistory);
}

async function runPopupCase(
  page: Page, harness: DirectHarness, seed: PopupSeed,
  action: (dialog: import('@playwright/test').Locator, file: PopupSeed['file']) => Promise<void>,
  op: 'occurrence.add-media' | 'occurrence.swap-media',
): Promise<void> {
  const dialog = await openPopup(page, harness, seed);
  const wire = wireFor(page);
  const before = await history(harness, seed);
  const original = await canonicalAt(harness, seed, before.head.revision_id);
  const post = await commitFromGesture(page, wire, () => action(dialog, seed.file));
  assertFullRequest(post, before.head, seed, harness);
  await assertSharedMediaCommands(post, seed, wire, op);
  const result = accepted(post, before.head);
  const expected = expectedPopupDocument(original, seed, post);
  // Whole-document equality preserves every sibling, registry entry, ordered
  // row, opaque value, explicit null, absent key and source_mapping field.
  expect(result.data.canonical_document).toEqual(expected);
  await assertReloadUndo(page, harness, seed, wire, before, original, post, result, expected);
}

test('P2 popup mounted ADD on selected child uses shared occurrence fork and A2 commit', async ({ page, harness, popup }) => {
  await runPopupCase(page, harness, popup, async (dialog, file) => {
    await dialog.locator(`.clip-action[data-clip-id="${popup.sharedOccurrenceId}:${TARGET_CLIP_ID}"]`).click();
    await dialog.getByRole('button', { name: 'Add media', exact: true }).click();
    await dialog.getByLabel('Choose media for shot timeline').setInputFiles({ name: file.name, mimeType: file.type, buffer: file.buffer });
  }, 'occurrence.add-media');
});

test('P2 popup mounted SWAP on selected child uses authenticated old/new media selections', async ({ page, harness, popup }) => {
  await runPopupCase(page, harness, popup, async (dialog, file) => {
    await dialog.locator(`.clip-action[data-clip-id="${popup.sharedOccurrenceId}:${TARGET_CLIP_ID}"]`).click();
    await dialog.getByRole('button', { name: 'Swap selected clip', exact: true }).click();
    await dialog.getByLabel('Choose media for shot timeline').setInputFiles({ name: file.name, mimeType: file.type, buffer: file.buffer });
  }, 'occurrence.swap-media');
});
