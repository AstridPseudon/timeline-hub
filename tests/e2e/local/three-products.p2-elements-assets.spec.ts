import { expect, type Locator, type Page, type Request, type Response } from '@playwright/test';
import { sha256Hex, THREE_PRODUCTS_REFERENCE_AT, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';
import { ASTRID_PYTHON } from './support/astrid.ts';
import { dropFileOnTimeline, openEmbeddedCanonicalShot, test as appTest } from './support/app.ts';
import { assertSemanticAddMediaRequest } from './support/p2-semantic-oracle.ts';
import type {
  CanonicalDocument,
  CommitAcceptedMutation,
  CommitRequest,
  HeadPin,
  HistoryEntry,
  HistoryPage,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';

/**
 * P2/A3's real mounted asset/element slice.  The existing P2 tour owns the
 * parent move and transition cases; this file owns the remaining mounted
 * element, registry and child-placement paths.
 */
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_WRITES = /\/timelines\/[^/]+\/(?:composition-revisions|saves)$/;
const CEILING = { timeout: 90_000 };
type JsonObject = Record<string, unknown>;

interface CommitPost {
  request: Request;
  response: Response;
  body: CommitRequest;
  json: unknown;
  key: string;
}

interface Wire {
  posts: CommitPost[];
  legacy: string[];
}

const test = appTest.extend<object, { seed3: ThreeProductsSeed }>({
  seed3: [async ({ harness }, use) => {
    await use(await harness.seedThreeProducts(THREE_PRODUCTS_REFERENCE_AT, 'native-none'));
  }, { scope: 'worker', timeout: 240_000 }],
});

test.describe.configure({ mode: 'serial' });

function object(value: unknown, label: string): JsonObject {
  expect(value, label).toBeTruthy();
  expect(typeof value, label).toBe('object');
  expect(Array.isArray(value), label).toBe(false);
  return value as JsonObject;
}

function digest(value: unknown): string {
  const json = JSON.stringify(value, (_key, item) => item && typeof item === 'object' && !Array.isArray(item)
    ? Object.fromEntries(Object.entries(item).sort(([a], [b]) => a.localeCompare(b)))
    : item);
  return sha256Hex(new TextEncoder().encode(json));
}

async function revisionBody(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string): Promise<JsonObject> {
  const response = await harness.runtimeJson<JsonObject>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revisionId}`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  return response.body;
}

async function canonicalAt(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string): Promise<CanonicalDocument> {
  const parent = await revisionBody(harness, seed, revisionId);
  const manifest = object(parent.dependency_manifest, 'canonical dependency manifest');
  const shots = await Promise.all((manifest.shots as Array<JsonObject>).map(async (pin) => {
    const response = await harness.runtimeJson<JsonObject>('GET', `/v1/projects/${harness.seed.projectId}/shots/${String(pin.shot_id)}/revisions/${String(pin.revision_id)}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    return { ...pin, payload: response.body.payload };
  }));
  const internals = await Promise.all((manifest.internal_timelines as Array<JsonObject>).map(async (pin) => {
    const response = await harness.runtimeJson<JsonObject>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${String(pin.revision_id)}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    return { ...pin, payload: response.body.payload };
  }));
  return {
    schema_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    parent_revision: { revision_id: String(parent.revision_id), content_digest: String(parent.content_digest), payload: parent.payload as CanonicalDocument['parent_revision']['payload'] },
    shot_revisions: shots as CanonicalDocument['shot_revisions'],
    internal_timeline_revisions: internals as CanonicalDocument['internal_timeline_revisions'],
    dependency_manifest: manifest as CanonicalDocument['dependency_manifest'],
  };
}

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const items: HistoryEntry[] = [];
  let cursor: string | null = null;
  let head: HeadPin | undefined;
  do {
    const response: { status: number; body: HistoryPage } = await harness.runtimeJson<HistoryPage>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ''}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    head ??= response.body.head;
    expect(response.body.head).toEqual(head);
    items.push(...response.body.items);
    cursor = response.body.next_cursor;
  } while (cursor);
  expect(head).toBeTruthy();
  return { items, head: head!, next_cursor: null };
}

function clip(document: CanonicalDocument, id: string): JsonObject {
  const payload = document.parent_revision.payload as unknown as JsonObject;
  const row = (payload.clips as Array<JsonObject>).find((candidate) => candidate.id === id);
  expect(row, `parent clip ${id}`).toBeTruthy();
  return row!;
}

function internal(document: CanonicalDocument): JsonObject {
  expect(document.internal_timeline_revisions).toHaveLength(1);
  return document.internal_timeline_revisions[0]!.payload as JsonObject;
}

function assertClosure(document: CanonicalDocument, harness: DirectHarness, seed: ThreeProductsSeed): void {
  expect(document.schema_version).toBe(1);
  expect(document.project_id).toBe(harness.seed.projectId);
  expect(document.timeline_id).toBe(seed.timelineId);
  expect(document.parent_revision.content_digest).toBe(digest(document.parent_revision.payload));
  for (const shot of document.shot_revisions) expect(shot.content_digest).toBe(digest(shot.payload));
  for (const timeline of document.internal_timeline_revisions) expect(timeline.content_digest).toBe(digest(timeline.payload));
  for (const pin of document.dependency_manifest.shots) {
    const shot = document.shot_revisions.find((candidate) => candidate.revision_id === pin.revision_id);
    expect(shot, `manifest shot ${pin.revision_id}`).toBeTruthy();
    expect(pin.content_digest).toBe(shot!.content_digest);
  }
  for (const pin of document.dependency_manifest.internal_timelines) {
    const timeline = document.internal_timeline_revisions.find((candidate) => candidate.revision_id === pin.revision_id);
    expect(timeline, `manifest internal ${pin.revision_id}`).toBeTruthy();
    expect(pin.content_digest).toBe(timeline!.content_digest);
  }
}

function wireFor(page: Page): Wire {
  const wire: Wire = { posts: [], legacy: [] };
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (!['GET', 'HEAD'].includes(request.method()) && (LEGACY_WRITES.test(pathname) || pathname.includes('/composition-revisions') || pathname.includes('/doorlog'))) {
      wire.legacy.push(`${request.method()} ${pathname}`);
    }
  });
  return wire;
}

async function commitFromGesture(page: Page, wire: Wire, gesture: () => Promise<void>): Promise<CommitPost> {
  const responsePromise = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
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

async function openTimeline(page: Page, harness: DirectHarness, seed: ThreeProductsSeed): Promise<void> {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await page.goto(`${harness.origin}/tools/video-editor`);
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('combobox', { name: 'Select project' })).toContainText(harness.seed.projectName);
  await expect(page.getByRole('textbox', { name: 'Track name' }).first()).toBeVisible();
  expect(seed.timelineId).toBe(harness.seed.timelineId);
}

function assertRequestV2(post: CommitPost, before: HeadPin): void {
  expect(post.key).toMatch(/\S/);
  expect(post.body).toMatchObject({
    api_version: 1,
    project_id: expect.any(String),
    timeline_id: expect.any(String),
    base_revision_id: before.revision_id,
    base_publication_id: before.publication_id,
    commands: expect.any(Array),
    label: expect.any(String),
    steps: expect.any(Array),
    merge: 'atomic',
    dry_run: false,
    source: { via: 'app' },
  });
  expect(Object.hasOwn(post.body, 'reads')).toBe(false);
  expect(post.body.commands.length).toBeGreaterThan(0);
  for (const key of ['rationale', 'group_id'] as const) {
    if (Object.hasOwn(post.body, key)) expect(post.body[key]).toEqual(expect.any(String));
  }
  expect(post.body.steps!.length).toBeGreaterThan(0);
  for (const step of post.body.steps!) {
    expect(step.id).toEqual(expect.any(String));
    expect(step.label).toEqual(expect.any(String));
    expect(step.intent).toEqual(expect.any(String));
    expect(step.tags).toEqual(expect.any(Array));
    expect(step.command_ordinals.length).toBeGreaterThan(0);
    expect(step.patch).toEqual(expect.any(Array));
    expect(step.patch.length).toBeGreaterThan(0);
    expect(Object.hasOwn(step, 'reads')).toBe(false);
  }
}

function assertAcceptedReply(post: CommitPost, before: HeadPin): CommitAcceptedMutation {
  expect(post.response.status(), JSON.stringify(post.json)).toBe(200);
  const envelope = object(post.json, 'commit envelope');
  const data = object(envelope.data, 'commit data');
  expect(['accepted', 'merged', 'rebased']).toContain(data.status);
  expect(data.base_revision_id).toBe(before.revision_id);
  expect(data.base_publication_id).toBe(before.publication_id);
  expect(data.previous_revision_id).toBe(before.revision_id);
  expect(data.previous_publication_id).toBe(before.publication_id);
  expect(data.accepted_revision_id).toEqual(expect.any(String));
  expect(data.canonical_document).toEqual(expect.any(Object));
  expect(data.document_digest).toEqual(expect.any(String));
  expect(data.commands).toEqual(expect.any(Array));
  expect(data.commands).toHaveLength(post.body.commands.length);
  for (const [ordinal, submitted] of post.body.commands.entries()) {
    const accepted = (data.commands as Array<JsonObject>)[ordinal]!;
    for (const [key, value] of Object.entries(submitted as unknown as JsonObject)) expect(accepted[key], `normalized command ${ordinal}.${key}`).toEqual(value);
  }
  expect(data.label).toBe(post.body.label);
  for (const key of ['rationale', 'group_id'] as const) {
    if (Object.hasOwn(post.body, key)) expect(data[key]).toEqual(post.body[key]);
  }
  expect(data.id_map).toEqual(expect.any(Object));
  expect(data.provider_version).toEqual(expect.any(String));
  expect(data.compiler_version).toEqual(expect.any(String));
  expect(data.publisher).toEqual(expect.any(String));
  expect(data.merge_mode).toBe(post.body.merge);
  expect(data.steps).toEqual(expect.any(Array));
  expect(data.steps).toHaveLength(post.body.steps!.length);
  for (const [ordinal, submitted] of post.body.steps!.entries()) {
    expect((data.steps as Array<JsonObject>)[ordinal]).toMatchObject({
      id: submitted.id,
      label: submitted.label,
      intent: submitted.intent,
      tags: submitted.tags,
      command_ordinals: submitted.command_ordinals,
    });
  }
  expect(data.source).toEqual(post.body.source);
  const receipt = object(envelope.receipt, 'commit receipt');
  expect(receipt.receipt_id).toBe(post.key);
  expect(receipt.idempotency_key).toBe(post.key);
  expect(receipt.result).toEqual(envelope.data);
  expect(Object.keys(receipt).sort()).toEqual(['command_kind', 'created_at', 'event_ids', 'idempotency_key', 'project_id', 'project_seq', 'receipt_id', 'request_hash', 'result'].sort());
  return envelope as unknown as CommitAcceptedMutation;
}

function assertCanonicalResult(result: CommitAcceptedMutation, actual: CanonicalDocument, harness: DirectHarness, seed: ThreeProductsSeed): void {
  const document = result.data.canonical_document;
  assertClosure(document, harness, seed);
  expect(document.parent_revision.revision_id).toBe(result.data.accepted_revision_id);
  expect(result.data.document_digest).toBe(digest(document));
  expect(actual).toEqual(document);
}

function assertHistoryEntry(page: HistoryPage, post: CommitPost, result: CommitAcceptedMutation): void {
  const entry = page.items.find((candidate) => candidate.publication_id === post.key);
  expect(entry, 'commit is recorded in /commits').toBeTruthy();
  expect(entry!.intent).toBe('recorded');
  expect(entry!.records).not.toBeNull();
  expect(entry!.revision_id).toBe(result.data.accepted_revision_id);
  expect(entry!.receipt).toEqual(result.receipt);
  expect(entry!.label).toBe(post.body.label);
  expect(entry!.merge_mode).toBe(result.data.merge_mode);
  expect(entry!.source).toEqual(post.body.source);
  expect(entry!.steps).toEqual(result.data.steps);
  expect(entry!.records!.commands.map((record) => record.command)).toEqual(result.data.commands);
  expect(entry!.records!.undo_steps).toBeDefined();
  for (const step of entry!.records!.steps ?? []) {
    expect(step.patch.length).toBeGreaterThan(0);
    expect(step.dependencies?.length).toBeGreaterThan(0);
  }
  for (const record of entry!.records!.commands) {
    expect(record.writes.length).toBeGreaterThan(0);
    expect(record.reads.length).toBeGreaterThan(0);
    expect(record.bindings.length).toBeGreaterThan(0);
    expect(record.dependencies).toEqual(expect.any(Array));
    expect(record.derived_writes).toEqual(expect.any(Array));
  }
}

function assertUndoHistoryEntry(page: HistoryPage, undo: CommitPost, target: CommitPost): void {
  const entry = page.items.find((candidate) => candidate.publication_id === undo.key);
  expect(entry, 'Undo is recorded in /commits').toBeTruthy();
  expect(entry!.records?.undo_of).toEqual([target.key]);
  expect(entry!.records?.undo_steps).toBeNull();
}

function assertNoLegacy(wire: Wire): void {
  expect(wire.legacy, 'mounted edits do not write old routes').toEqual([]);
}

function assertParentListIsolation(
  before: CanonicalDocument,
  after: CanonicalDocument,
  newId?: string,
  changedId?: string,
  changedField?: string,
  changedConfigKeys: string[] = [],
): void {
  const beforeParent = before.parent_revision.payload as unknown as JsonObject;
  const afterParent = after.parent_revision.payload as unknown as JsonObject;
  const beforeClips = beforeParent.clips as Array<JsonObject>;
  const afterClips = afterParent.clips as Array<JsonObject>;
  expect(afterClips.map((row) => row.id).filter((id) => id !== newId)).toEqual(beforeClips.map((row) => row.id));
  for (const row of beforeClips) {
    const next = afterClips.find((candidate) => candidate.id === row.id)!;
    if (row.id === changedId && changedField) {
      expect({ ...next, [changedField]: undefined }).toEqual({ ...row, [changedField]: undefined });
    } else expect(next).toEqual(row);
  }
  const beforeConfig = object(beforeParent.config, 'parent config');
  const afterConfig = object(afterParent.config, 'updated parent config');
  expect(afterConfig.clips).toEqual(afterClips);
  expect(Object.fromEntries(Object.entries(afterConfig).filter(([key]) => key !== 'clips' && !changedConfigKeys.includes(key))))
    .toEqual(Object.fromEntries(Object.entries(beforeConfig).filter(([key]) => key !== 'clips' && !changedConfigKeys.includes(key))));
}

async function seedImageFile(harness: DirectHarness): Promise<{ name: string; type: string; bytesBase64: string }> {
  const response = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(harness.seed.image.objectId)}`);
  expect(response.status).toBe(200);
  const bytes = new Uint8Array(await response.arrayBuffer());
  expect(bytes.byteLength).toBe(harness.seed.image.size);
  expect(sha256Hex(bytes)).toBe(harness.seed.image.digest);
  return { name: 'p2-mounted-image.png', type: harness.seed.image.mediaType, bytesBase64: Buffer.from(bytes).toString('base64') };
}

async function dropFileIn(scope: Locator, file: { name: string; type: string; bytesBase64: string }, clipId: string, referenceId: string, from: number, referenceAt: number, time: number): Promise<void> {
  const clipLocator = scope.locator(`.clip-action[data-clip-id="${clipId}"]`).first();
  const referenceLocator = scope.locator(`.clip-action[data-clip-id="${referenceId}"]`).first();
  const wrapper = scope.locator('.timeline-wrapper').first();
  await expect(clipLocator).toBeVisible();
  await expect(referenceLocator).toBeVisible();
  const [clipBox, referenceBox, wrapperBox] = await Promise.all([clipLocator.boundingBox(), referenceLocator.boundingBox(), wrapper.boundingBox()]);
  if (!clipBox || !referenceBox || !wrapperBox) throw new Error('child timeline is not measurable');
  const pixelsPerSecond = (referenceBox.x - clipBox.x) / (referenceAt - from);
  const clientX = clipBox.x + (time - from) * pixelsPerSecond;
  const clientY = clipBox.y + clipBox.height / 2;
  expect(clientX).toBeGreaterThanOrEqual(wrapperBox.x);
  expect(clientX).toBeLessThanOrEqual(wrapperBox.x + wrapperBox.width);
  await wrapper.evaluate((target, input) => {
    const binary = atob(input.bytesBase64);
    const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
    const transfer = new DataTransfer();
    transfer.items.add(new File([bytes], input.name, { type: input.type }));
    for (const eventType of ['dragover', 'drop'] as const) {
      target.dispatchEvent(new DragEvent(eventType, { bubbles: true, cancelable: true, clientX: input.clientX, clientY: input.clientY, dataTransfer: transfer }));
    }
  }, { ...file, clientX, clientY });
}

async function assertReload(
  page: Page,
  harness: DirectHarness,
  seed: ThreeProductsSeed,
  revisionId: string,
  expected: CanonicalDocument,
  assertMounted: () => Promise<void>,
): Promise<void> {
  await page.reload();
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('textbox', { name: 'Track name' }).first()).toBeVisible();
  await expect(page.getByTestId('preview-revision-label').filter({ hasText: `Committed ${revisionId}` }).first()).toBeVisible(CEILING);
  const current = await history(harness, seed);
  expect(current.head.revision_id).toBe(revisionId);
  const reread = await canonicalAt(harness, seed, current.head.revision_id);
  assertClosure(reread, harness, seed);
  expect(reread).toEqual(expected);
  await assertMounted();
}

test('P2 mounted element edit: real catalog apply, exact params patch, reload and guarded Undo', async ({ page, harness, seed3 }) => {
  await openTimeline(page, harness, seed3);
  const wire = wireFor(page);
  const beforeHistory = await history(harness, seed3);
  const original = await canonicalAt(harness, seed3, beforeHistory.head.revision_id);
  await page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first().click();

  const apply = await commitFromGesture(page, wire, async () => {
    await page.getByRole('button', { name: 'Elements', exact: true }).click();
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();
    await dialog.getByPlaceholder('Search elements').fill('am-burst');
    await expect(dialog.getByText('AM Burst', { exact: true })).toBeVisible();
    await dialog.getByRole('button', { name: 'Apply', exact: true }).click();
    await expect(dialog.getByRole('status')).toContainText('applied');
  });
  assertRequestV2(apply, beforeHistory.head);
  expect(apply.body.commands[0]!.op).toBe('doc.patch');
  expect((apply.body.commands[0]!.args.changes as Array<JsonObject>).some((change) => change.op === 'list.insert')).toBe(true);
  const applied = assertAcceptedReply(apply, beforeHistory.head);
  const appliedDocument = applied.data.canonical_document;
  const actualApplied = await canonicalAt(harness, seed3, applied.data.accepted_revision_id);
  assertCanonicalResult(applied, actualApplied, harness, seed3);
  assertClosure(appliedDocument, harness, seed3);
  const newElementClip = (appliedDocument.parent_revision.payload as unknown as JsonObject).clips as Array<JsonObject>;
  const originalIds = new Set(((original.parent_revision.payload as unknown as JsonObject).clips as Array<JsonObject>).map((row) => String(row.id)));
  const addedId = newElementClip.find((row) => !originalIds.has(String(row.id)))?.id as string | undefined;
  expect(addedId, 'catalog apply creates a mounted clip').toEqual(expect.any(String));
  expect(clip(appliedDocument, addedId!)).toMatchObject({ elementRef: { id: 'am-burst', kind: 'effect', packId: 'astrid_motion' } });
  assertParentListIsolation(original, appliedDocument, addedId);
  const appliedHistory = await history(harness, seed3);
  assertHistoryEntry(appliedHistory, apply, applied);
  assertNoLegacy(wire);

  const beforeParams = await history(harness, seed3);
  const paramsBase = await canonicalAt(harness, seed3, beforeParams.head.revision_id);
  await page.locator(`.clip-action[data-clip-id="${addedId}"]`).first().click();
  await expect(page.getByTestId('astrid-element-params')).toBeVisible();
  const bob = page.getByRole('spinbutton').first();
  await expect(bob).toBeVisible();
  const paramsCommit = await commitFromGesture(page, wire, async () => {
    await bob.fill('12');
    await bob.press('Enter');
    await bob.blur();
  });
  assertRequestV2(paramsCommit, beforeParams.head);
  expect(paramsCommit.body.commands[0]!.op).toBe('doc.patch');
  const paramsChanges = paramsCommit.body.commands[0]!.args.changes as Array<JsonObject>;
  expect(paramsChanges).toHaveLength(1);
  expect(paramsChanges[0]).toMatchObject({ op: 'set', ref: 'parent', path: ['clips', `id:${addedId}`, 'params'] });
  const paramsResult = assertAcceptedReply(paramsCommit, beforeParams.head);
  const paramsDocument = paramsResult.data.canonical_document;
  assertCanonicalResult(paramsResult, await canonicalAt(harness, seed3, paramsResult.data.accepted_revision_id), harness, seed3);
  assertParentListIsolation(paramsBase, paramsDocument, undefined, addedId, 'params');
  expect((clip(paramsDocument, addedId!).params as JsonObject).bob).toBe(12);
  const paramsHistory = await history(harness, seed3);
  assertHistoryEntry(paramsHistory, paramsCommit, paramsResult);
  await assertReload(page, harness, seed3, paramsResult.data.accepted_revision_id, paramsDocument, async () => {
    await page.locator(`.clip-action[data-clip-id="${addedId}"]`).first().click();
    await expect(page.getByTestId('astrid-element-params')).toBeVisible();
    await expect(page.getByRole('spinbutton').first()).toHaveValue('12');
  });

  const undo = await commitFromGesture(page, wire, async () => {
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
  });
  assertRequestV2(undo, { revision_id: paramsResult.data.accepted_revision_id, publication_id: paramsCommit.key });
  expect(undo.body.commands[0]).toEqual({ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [paramsCommit.key] } });
  const undoneParams = assertAcceptedReply(undo, { revision_id: paramsResult.data.accepted_revision_id, publication_id: paramsCommit.key });
  expect(undoneParams.data.canonical_document.parent_revision.payload).toEqual(paramsBase.parent_revision.payload);
  assertNoLegacy(wire);
  assertUndoHistoryEntry(await history(harness, seed3), undo, paramsCommit);
  const restoredBob = (clip(paramsBase, addedId!).params as JsonObject).bob;
  await assertReload(page, harness, seed3, undoneParams.data.accepted_revision_id, paramsBase, async () => {
    await page.locator(`.clip-action[data-clip-id="${addedId}"]`).first().click();
    await expect(page.getByTestId('astrid-element-params')).toBeVisible();
    await expect(page.getByRole('spinbutton').first()).toHaveValue(String(restoredBob));
  });

  const undoApply = await commitFromGesture(page, wire, async () => {
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
  });
  const undoneApply = assertAcceptedReply(undoApply, { revision_id: undoneParams.data.accepted_revision_id, publication_id: undo.key });
  expect(undoneApply.data.canonical_document.parent_revision.payload).toEqual(original.parent_revision.payload);
  assertNoLegacy(wire);
  assertUndoHistoryEntry(await history(harness, seed3), undoApply, apply);
  await assertReload(page, harness, seed3, undoneApply.data.accepted_revision_id, original, async () => {
    await expect(page.locator(`.clip-action[data-clip-id="${addedId}"]`)).toHaveCount(0);
  });
});

test('P2 mounted registerAsset save: real file drop, exact media/registry fields, reload and guarded Undo', async ({ page, harness, seed3 }) => {
  await openTimeline(page, harness, seed3);
  const wire = wireFor(page);
  const before = await history(harness, seed3);
  const original = await canonicalAt(harness, seed3, before.head.revision_id);
  const file = await seedImageFile(harness);
  const importResponse = page.waitForResponse((response) => response.request().method() === 'POST' && /\/media-imports$/.test(new URL(response.url()).pathname), CEILING);
  const selectionResponse = page.waitForResponse((response) => response.request().method() === 'GET' && /\/media-selection\?/.test(new URL(response.url()).pathname + new URL(response.url()).search), CEILING);
  const post = await commitFromGesture(page, wire, () => dropFileOnTimeline(page, file, seed3.appClipId, seed3.transitionClipId, 0, THREE_PRODUCTS_REFERENCE_AT, 5));
  const imported = object((await (await importResponse).json()).data, 'registered media import');
  const selected = await selectionResponse.then((response) => response.json()) as JsonObject;
  assertSemanticAddMediaRequest(post, before.head, original, { op: 'clip.add-media', owner: 'parent', select: 'parent', label: 'Edit timeline' });
  const command = post.body.commands[0]!;
  expect(command.op).toBe('clip.add-media');
  expect(command.select).toBe('parent');
  expect(command.intent).toEqual({});
  expect(command.args.media).toEqual(selected);
  expect(selected.object_id).toBe(harness.seed.image.objectId);
  expect(imported.entry).toMatchObject({ object_id: harness.seed.image.objectId, content_sha256: harness.seed.image.digest, media_type: harness.seed.image.mediaType });
  const row = command.args.row as JsonObject;
  expect(row).toMatchObject({ id: expect.any(String), track: 'V1', at: 5, clipType: 'media' });
  expect(row.asset).toEqual(expect.any(String));
  expect(Object.keys(row)).not.toEqual(expect.arrayContaining(['asset_id', 'media_id', 'object_id', 'clip_type', 'source', 'sourceURL', 'sourceUrl', 'source_url']));
  const result = assertAcceptedReply(post, before.head);
  const after = result.data.canonical_document;
  assertCanonicalResult(result, await canonicalAt(harness, seed3, result.data.accepted_revision_id), harness, seed3);
  assertParentListIsolation(original, after, row.id as string, undefined, undefined, ['registry']);
  const afterParent = after.parent_revision.payload as unknown as JsonObject;
  const beforeParent = original.parent_revision.payload as unknown as JsonObject;
  const beforeAssets = object(object(beforeParent.config, 'original config').registry, 'original registry').assets as JsonObject;
  const afterConfig = object(afterParent.config, 'updated config');
  const afterAssets = object(object(afterConfig.registry, 'updated registry').assets, 'updated assets');
  expect(Object.keys(afterAssets).filter((key) => !Object.hasOwn(beforeAssets, key))).toEqual([row.asset]);
  expect(afterAssets[row.asset as string]).toMatchObject({ media_id: harness.seed.image.objectId, content_sha256: harness.seed.image.digest, type: harness.seed.image.mediaType });
  expect(Object.fromEntries(Object.entries(afterAssets).filter(([key]) => Object.hasOwn(beforeAssets, key)))).toEqual(beforeAssets);
  expect(object(afterParent.registry, 'updated parent registry').assets).toEqual(afterAssets);
  const committed = await history(harness, seed3);
  assertHistoryEntry(committed, post, result);
  assertNoLegacy(wire);
  await assertReload(page, harness, seed3, result.data.accepted_revision_id, after, async () => {
    await expect(page.locator(`.clip-action[data-clip-id="${row.id as string}"]`)).toBeVisible();
  });
  const undo = await commitFromGesture(page, wire, async () => { await page.getByRole('button', { name: 'Undo', exact: true }).click(); });
  assertRequestV2(undo, { revision_id: result.data.accepted_revision_id, publication_id: post.key });
  expect(undo.body.commands[0]).toEqual({ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [post.key] } });
  const undone = assertAcceptedReply(undo, { revision_id: result.data.accepted_revision_id, publication_id: post.key });
  expect(undone.data.canonical_document.parent_revision.payload).toEqual(original.parent_revision.payload);
  assertNoLegacy(wire);
  assertUndoHistoryEntry(await history(harness, seed3), undo, post);
  await assertReload(page, harness, seed3, undone.data.accepted_revision_id, original, async () => {
    await expect(page.locator(`.clip-action[data-clip-id="${row.id as string}"]`)).toHaveCount(0);
    await expect(page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first()).toBeVisible();
  });
});

test('P2 mounted automatic child placement: embedded shot file gesture, occurrence command, closure and guarded Undo', async ({ page, harness, seed3 }) => {
  await openTimeline(page, harness, seed3);
  const wire = wireFor(page);
  const before = await history(harness, seed3);
  const original = await canonicalAt(harness, seed3, before.head.revision_id);
  const file = await seedImageFile(harness);
  const dialog = await openEmbeddedCanonicalShot(page, seed3.occurrenceId, 'F2 agent shot');
  const importResponse = page.waitForResponse((response) => response.request().method() === 'POST' && /\/media-imports$/.test(new URL(response.url()).pathname), CEILING);
  const selectionResponse = page.waitForResponse((response) => response.request().method() === 'GET' && /\/media-selection\?/.test(new URL(response.url()).pathname + new URL(response.url()).search), CEILING);
  const post = await commitFromGesture(page, wire, () => dropFileIn(dialog, file, seed3.agentClipId, seed3.agentClearClipId, 3, 6, 4.5));
  const imported = object((await (await importResponse).json()).data, 'child media import');
  const selected = await selectionResponse.then((response) => response.json()) as JsonObject;
  assertSemanticAddMediaRequest(post, before.head, original, {
    op: 'occurrence.add-media', owner: `occurrence:${seed3.occurrenceId}`, select: `occurrence:${seed3.occurrenceId}`, label: 'Edit timeline',
  });
  const command = post.body.commands[0]!;
  expect(command.op).toBe('occurrence.add-media');
  expect(command.select).toBe(`occurrence:${seed3.occurrenceId}`);
  expect(command.intent).toEqual({ ownership: 'occurrence' });
  expect(command.args.media).toEqual(selected);
  expect(selected.object_id).toBe(harness.seed.image.objectId);
  expect(imported.entry).toMatchObject({ object_id: harness.seed.image.objectId, content_sha256: harness.seed.image.digest, media_type: harness.seed.image.mediaType });
  const row = command.args.row as JsonObject;
  expect(row).toMatchObject({ id: expect.any(String), track: 'V2', at: 4.5, clipType: 'media', asset: selected.asset });
  const result = assertAcceptedReply(post, before.head);
  const after = result.data.canonical_document;
  assertCanonicalResult(result, await canonicalAt(harness, seed3, result.data.accepted_revision_id), harness, seed3);
  const beforeInternal = internal(original);
  const afterInternal = internal(after);
  const beforeRows = beforeInternal.clips as Array<JsonObject>;
  const afterRows = afterInternal.clips as Array<JsonObject>;
  expect(afterRows.filter((candidate) => !beforeRows.some((known) => known.id === candidate.id))).toEqual([expect.objectContaining(row)]);
  for (const known of beforeRows) expect(afterRows.find((candidate) => candidate.id === known.id)).toEqual(known);
  expect(afterRows.map((candidate) => candidate.id)).toEqual([...beforeRows.map((candidate) => candidate.id), row.id]);
  expect(after.parent_revision.payload).toEqual(original.parent_revision.payload);
  expect(after.shot_revisions).toEqual(original.shot_revisions);
  const beforeChildAssets = object(object(beforeInternal.registry, 'original child registry').assets, 'original child assets');
  const childRegistry = object(object(afterInternal.registry, 'child registry').assets, 'child assets');
  expect(Object.fromEntries(Object.entries(childRegistry).filter(([key]) => Object.hasOwn(beforeChildAssets, key)))).toEqual(beforeChildAssets);
  expect(childRegistry[row.asset as string]).toMatchObject({ media_id: harness.seed.image.objectId, content_sha256: harness.seed.image.digest, type: harness.seed.image.mediaType });
  assertHistoryEntry(await history(harness, seed3), post, result);
  assertNoLegacy(wire);
  await assertReload(page, harness, seed3, result.data.accepted_revision_id, after, async () => {
    const reloadedDialog = await openEmbeddedCanonicalShot(page, seed3.occurrenceId, 'F2 agent shot');
    await expect(reloadedDialog.locator(`.clip-action[data-clip-id="${row.id as string}"]`)).toBeVisible();
  });
  const undo = await commitFromGesture(page, wire, async () => { await page.getByRole('button', { name: 'Undo', exact: true }).click(); });
  assertRequestV2(undo, { revision_id: result.data.accepted_revision_id, publication_id: post.key });
  expect(undo.body.commands[0]).toEqual({ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [post.key] } });
  const undone = assertAcceptedReply(undo, { revision_id: result.data.accepted_revision_id, publication_id: post.key });
  expect(undone.data.canonical_document.parent_revision.payload).toEqual(original.parent_revision.payload);
  expect(undone.data.canonical_document.shot_revisions).toEqual(original.shot_revisions);
  expect(undone.data.canonical_document.internal_timeline_revisions).toEqual(original.internal_timeline_revisions);
  assertNoLegacy(wire);
  assertUndoHistoryEntry(await history(harness, seed3), undo, post);
  await assertReload(page, harness, seed3, undone.data.accepted_revision_id, original, async () => {
    const reloadedDialog = await openEmbeddedCanonicalShot(page, seed3.occurrenceId, 'F2 agent shot');
    await expect(reloadedDialog.locator(`.clip-action[data-clip-id="${row.id as string}"]`)).toHaveCount(0);
  });
});
