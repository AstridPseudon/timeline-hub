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
  compositionPublication,
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
  EditCommand,
  HeadPin,
  HistoryEntry,
  HistoryPage,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';

const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_WRITES = /\/timelines\/[^/]+\/(?:composition-revisions|saves)$/;
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
  legacy: string[];
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
    return { ...pin, payload: result.body.payload };
  }));
  const internals = await Promise.all(array(manifest.internal_timelines, 'manifest internal timelines').map(async (pin) => {
    const result = await harness.runtimeJson<JsonObject>(
      'GET',
      `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${String(pin.revision_id)}`,
    );
    expect(result.status, JSON.stringify(result.body)).toBe(200);
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
    body: file.buffer,
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
  return { ...media, entry: { ...entry, generationId: generation_id, variantId: variant_id } };
}

async function preparePopupSeed(harness: DirectHarness): Promise<PopupSeed> {
  const seed = await harness.seedThreeProducts(THREE_PRODUCTS_REFERENCE_AT, 'native-none');
  const before = await canonicalAt(harness, seed, seed.headRevisionId);
  const parent = clone(before.parent_revision.payload as unknown as JsonObject);
  const occurrences = array(parent.occurrences, 'seed occurrences');
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
  const childPayload = clone(internal!.payload as unknown as JsonObject);
  const childClips = array(childPayload.clips, 'seed child clips');
  const target = object(childClips.find((row) => row.id === TARGET_CLIP_ID), 'selected child clip');
  target.asset = oldMedia.asset;
  const registry = object(childPayload.registry, 'child registry');
  const assets = object(registry.assets, 'child registry assets');
  assets[oldMedia.asset] = oldMedia.entry;

  const sharedOccurrenceId = 'f2-occurrence-copy';
  parent.occurrences = [
    ...occurrences,
    {
      ...clone(sourceOccurrence),
      occurrence_id: sharedOccurrenceId,
      placement: { ...(object(sourceOccurrence.placement, 'source placement')), start_ms: 12000 },
    },
  ];
  parent['p2_popup_opaque'] = { keep: [null, false, 0, { source: 'fixture' }] };

  const publication = compositionPublication(
    { projectId: harness.seed.projectId, timelineId: seed.timelineId },
    before.parent_revision.revision_id,
    'P2 popup fixture',
    30,
  );
  publication.parent_composition = parent as typeof publication.parent_composition;
  publication.shot_revisions = [{
    shot_id: shot!.shot_id,
    revision_id: shot!.revision_id,
    internal_timeline_revision_id: shot!.internal_timeline_revision_id,
    payload: clone(shot!.payload),
  }];
  publication.internal_timeline_revisions = [{
    timeline_id: internal!.timeline_id,
    revision_id: internal!.revision_id,
    payload: childPayload,
  }];
  const published = await harness.runtimeJson<JsonObject>(
    'POST',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions`,
    publication,
  );
  expect(published.status, JSON.stringify(published.body)).toBe(200);
  const setupHead = String(object(published.body.data, 'popup fixture publication').new_head);
  return {
    ...seed,
    headRevisionId: setupHead,
    sourceOccurrenceId: seed.occurrenceId,
    sharedOccurrenceId,
    oldMedia,
    file: { ...file, name: 'p2-popup-new.png' },
  };
}

function wireFor(page: Page): PopupWire {
  const wire: PopupWire = { posts: [], legacy: [] };
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (request.method() !== 'GET' && request.method() !== 'HEAD' && LEGACY_WRITES.test(pathname)) {
      wire.legacy.push(`${request.method()} ${pathname}`);
    }
  });
  return wire;
}

async function openPopup(page: Page, harness: DirectHarness, seed: PopupSeed): Promise<import('@playwright/test').Locator> {
  await page.goto(`${harness.origin}/tools/video-editor`);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const label = page.locator(`[data-shot-group-key^="${seed.sharedOccurrenceId}:"]`).first();
  await expect(label, 'shared occurrence shot group').toBeVisible();
  await label.dblclick();
  const dialog = page.getByRole('dialog');
  await expect(dialog.locator(`[data-canonical-occurrence-id="${seed.sharedOccurrenceId}"]`)).toBeVisible();
  await expect(dialog.locator('[data-shot-timeline-editor="true"]')).toBeVisible();
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

function assertFullRequest(post: CommitPost, before: HeadPin): void {
  expect(post.key).toMatch(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/);
  expect(post.body).toMatchObject({
    api_version: 1,
    project_id: expect.any(String),
    timeline_id: expect.any(String),
    base_revision_id: before.revision_id,
    base_publication_id: before.publication_id,
    commands: expect.any(Array),
    label: expect.any(String),
    steps: expect.any(Array),
    merge: expect.any(String),
    reads: expect.any(Array),
    dry_run: false,
    source: { via: 'app' },
    rationale: expect.any(String),
    group_id: expect.any(String),
  });
  expect(['fields', 'atomic']).toContain(post.body.merge);
  expect(post.body.commands.length).toBeGreaterThan(0);
  for (const command of post.body.commands) {
    expect(command).toMatchObject({ schema_version: 1, op: expect.any(String), version: '1', args: expect.any(Object) });
  }
  for (const step of post.body.steps ?? []) {
    expect(step).toMatchObject({
      id: expect.any(String), label: expect.any(String), intent: expect.any(String), tags: expect.any(Array),
      command_ordinals: expect.any(Array), patch: expect.any(Array), reads: expect.any(Array),
    });
  }
}

function accepted(post: CommitPost, before?: HeadPin): CommitAcceptedMutation {
  expect(post.response.status(), JSON.stringify(post.json)).toBe(200);
  const envelope = object(post.json, 'commit reply');
  const receipt = object(envelope.receipt, 'commit receipt');
  expect(receipt.receipt_id).toBe(post.key);
  expect(receipt.idempotency_key).toBe(post.key);
  const data = object(envelope.data, 'commit reply data');
  expect(['accepted', 'merged', 'rebased', 'historicalrebased']).toContain(data.status);
  expect(data).toMatchObject({
    base_revision_id: before?.revision_id ?? expect.any(String),
    base_publication_id: before?.publication_id ?? expect.any(String),
    previous_revision_id: expect.any(String),
    previous_publication_id: expect.any(String),
    accepted_revision_id: expect.any(String),
    canonical_document: expect.any(Object),
    document_digest: expect.stringMatching(/^sha256:/),
    commands: expect.any(Array),
    id_map: expect.any(Object),
    provider_version: expect.any(String),
    compiler_version: expect.any(String),
    merge_mode: expect.any(String),
    steps: expect.any(Array),
    publisher: expect.any(String),
    source: { via: 'app' },
    label: expect.any(String),
    rationale: expect.any(String),
    group_id: expect.any(String),
  });
  expect(receipt.result).toEqual(data);
  return envelope as unknown as CommitAcceptedMutation;
}

function assertSharedMediaCommands(post: CommitPost, seed: PopupSeed, op: 'occurrence.add-media' | 'occurrence.swap-media'): void {
  expect(post.body.commands.map((command) => command.op)).toEqual(['occurrence.fork', op]);
  expect(post.body.commands[0]).toMatchObject({
    select: `occurrence:${seed.sharedOccurrenceId}`,
    intent: { ownership: 'occurrence' },
    created: expect.arrayContaining([expect.stringMatching(/^shot:/)]),
  });
  expect(post.body.commands[1]).toMatchObject({ intent: { ownership: 'occurrence' } });
  const media = op === 'occurrence.swap-media'
    ? object(post.body.commands[1].args.old_media, 'swap old selection')
    : object(post.body.commands[1].args.media, 'add selection');
  expect(media).toMatchObject({
    asset: expect.any(String), generation_id: expect.any(String), variant_id: expect.any(String),
    object_id: expect.stringMatching(/^sha256:/), catalog_digest: expect.stringMatching(/^sha256:/),
  });
  if (op === 'occurrence.swap-media') expect(post.body.commands[1].args.media).toMatchObject({
    asset: expect.any(String), generation_id: expect.any(String), variant_id: expect.any(String),
    object_id: expect.stringMatching(/^sha256:/), catalog_digest: expect.stringMatching(/^sha256:/),
  });
}

function assertPopupDelta(before: CanonicalDocument, after: CanonicalDocument, seed: PopupSeed, post: CommitPost): void {
  const beforeParent = before.parent_revision.payload as unknown as JsonObject;
  const afterParent = after.parent_revision.payload as unknown as JsonObject;
  expect(afterParent.p2_popup_opaque).toEqual(beforeParent.p2_popup_opaque);
  expect(afterParent.config).toEqual(beforeParent.config);
  expect(afterParent.clips).toEqual(beforeParent.clips);
  const beforeOccurrences = array(beforeParent.occurrences, 'before occurrences');
  const afterOccurrences = array(afterParent.occurrences, 'after occurrences');
  const beforeSource = object(beforeOccurrences.find((row) => row.occurrence_id === seed.sourceOccurrenceId), 'before source occurrence');
  const afterSource = object(afterOccurrences.find((row) => row.occurrence_id === seed.sourceOccurrenceId), 'after source occurrence');
  expect(afterSource).toEqual(beforeSource);
  const afterShared = object(afterOccurrences.find((row) => row.occurrence_id === seed.sharedOccurrenceId), 'after shared occurrence');
  expect(afterShared.placement).toEqual(beforeSource.placement);
  expect(afterShared.duration_ms).toEqual(beforeSource.duration_ms);
  expect(afterShared.shot_revision_id).not.toBe(beforeSource.shot_revision_id);

  const oldInternal = before.internal_timeline_revisions.find((row) => row.revision_id === before.shot_revisions.find((shot) => shot.revision_id === beforeSource.shot_revision_id)!.internal_timeline_revision_id)!;
  const forkShot = after.shot_revisions.find((shot) => shot.revision_id === afterShared.shot_revision_id)!;
  const forkInternal = after.internal_timeline_revisions.find((row) => row.revision_id === forkShot.internal_timeline_revision_id)!;
  expect(forkInternal.payload.tracks).toEqual(oldInternal.payload.tracks);
  expect(forkInternal.payload.registry).toMatchObject({ assets: expect.any(Object) });
  const oldRows = array(oldInternal.payload.clips, 'old child clips');
  const newRows = array(forkInternal.payload.clips, 'fork child clips');
  const command = post.body.commands[1];
  if (command.op === 'occurrence.add-media') {
    const row = object(command.args.row, 'added child row');
    expect(newRows.some((candidate) => candidate.id === row.id)).toBe(true);
    for (const oldRow of oldRows) expect(newRows.find((candidate) => candidate.id === oldRow.id)).toEqual(oldRow);
  } else {
    const changedId = String(command.select).split('/clip:')[1];
    expect(newRows).toHaveLength(oldRows.length);
    for (const oldRow of oldRows) {
      const next = newRows.find((candidate) => candidate.id === oldRow.id)!;
      if (oldRow.id === changedId) {
        expect({ ...next, asset: undefined }).toEqual({ ...oldRow, asset: undefined });
        expect(next.asset).not.toBe(oldRow.asset);
      } else expect(next).toEqual(oldRow);
    }
  }
}

async function assertReloadUndo(
  page: Page,
  harness: DirectHarness,
  seed: PopupSeed,
  wire: PopupWire,
  before: HistoryPage,
  original: CanonicalDocument,
  post: CommitPost,
  result: CommitAcceptedMutation,
): Promise<void> {
  const committed = await history(harness, seed);
  const entry = committed.items.find((candidate) => candidate.publication_id === post.key);
  expect(entry, 'popup commit is in Runtime /commits history').toBeTruthy();
  expect(entry?.records).toBeTruthy();
  expect(entry?.records?.commands.some((record) => JSON.stringify(record.bindings).includes(seed.sharedOccurrenceId))).toBe(true);
  expect(committed.head).toEqual(pinOf(result));
  await page.reload();
  await expectConnected(page);
  await expect(page.locator(`[data-canonical-occurrence-id="${seed.sharedOccurrenceId}"]`)).toBeVisible(CEILING);
  const inverse = await commitFromGesture(page, wire, async () => {
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
  });
  const inverseResult = accepted(inverse, pinOf(result));
  expect(inverse.body.commands[0]).toMatchObject({ op: 'timeline.inverse', args: { publications: [post.key] } });
  expect(inverseResult.data.canonical_document.parent_revision.payload).toEqual(original.parent_revision.payload);
  expect(inverseResult.data.canonical_document.shot_revisions).toEqual(original.shot_revisions);
  expect(inverseResult.data.canonical_document.internal_timeline_revisions).toEqual(original.internal_timeline_revisions);
  const finalHistory = await history(harness, seed);
  expect(finalHistory.items.find((candidate) => candidate.publication_id === inverse.key)?.records?.undo_of).toEqual([post.key]);
  expect(finalHistory.items.filter((candidate) => !before.items.some((known) => known.publication_id === candidate.publication_id))).toHaveLength(2);
  expect(wire.legacy).toEqual([]);
}

async function runPopupCase(
  page: Page,
  harness: DirectHarness,
  seed: PopupSeed,
  action: (dialog: import('@playwright/test').Locator, file: PopupSeed['file']) => Promise<void>,
  op: 'occurrence.add-media' | 'occurrence.swap-media',
): Promise<void> {
  const dialog = await openPopup(page, harness, seed);
  const wire = wireFor(page);
  const before = await history(harness, seed);
  const original = await canonicalAt(harness, seed, before.head.revision_id);
  const post = await commitFromGesture(page, wire, () => action(dialog, seed.file));
  assertFullRequest(post, before.head);
  assertSharedMediaCommands(post, seed, op);
  const result = accepted(post, before.head);
  assertPopupDelta(original, result.data.canonical_document, seed, post);
  await assertReloadUndo(page, harness, seed, wire, before, original, post, result);
}

test('P2 popup mounted ADD on selected child uses shared occurrence fork and A2 commit', async ({ page, harness, popup }) => {
  await runPopupCase(page, harness, popup, async (dialog, file) => {
    await dialog.locator(`.clip-action[data-clip-id="${TARGET_CLIP_ID}"]`).click();
    await dialog.getByRole('button', { name: 'Add media', exact: true }).click();
    await dialog.getByLabel('Choose media for shot timeline').setInputFiles({ name: file.name, mimeType: file.type, buffer: file.buffer });
  }, 'occurrence.add-media');
});

test('P2 popup mounted SWAP on selected child uses authenticated old/new media selections', async ({ page, harness, popup }) => {
  await runPopupCase(page, harness, popup, async (dialog, file) => {
    await dialog.locator(`.clip-action[data-clip-id="${TARGET_CLIP_ID}"]`).click();
    await dialog.getByRole('button', { name: 'Swap selected clip', exact: true }).click();
    await dialog.getByLabel('Choose media for shot timeline').setInputFiles({ name: file.name, mimeType: file.type, buffer: file.buffer });
  }, 'occurrence.swap-media');
});
