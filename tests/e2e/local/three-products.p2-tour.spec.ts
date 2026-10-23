/**
 * P2's first mounted tour slice.  The original three-products journey remains
 * the behavioural baseline; this file adds v2 proof for the smallest ready
 * parent gestures without copying that journey's broad fixture or helpers.
 */
import { expect, type Page, type Request, type Response } from '@playwright/test';
import { THREE_PRODUCTS_REFERENCE_AT, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';
import { ASTRID_PYTHON } from './support/astrid.ts';
import { test as appTest } from './support/app.ts';
import type { CanonicalDocument, CommitAcceptedMutation, CommitRequest, HeadPin, HistoryEntry, HistoryPage } from '../../../src/integrations/runtime/timeline-commit-types.ts';

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

interface TourWire {
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

async function revisionBody(harness: DirectHarness, revisionId: string): Promise<JsonObject> {
  const response = await harness.runtimeJson<JsonObject>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions/${revisionId}`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  return response.body;
}

async function canonicalDocumentAt(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string): Promise<CanonicalDocument> {
  const parent = await revisionBody(harness, revisionId);
  const manifest = object(parent.dependency_manifest, `dependency manifest for ${revisionId}`);
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
  let pinnedHead: HeadPin | undefined;
  do {
    const query = `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ''}`;
    const response = await harness.runtimeJson<HistoryPage>('GET', query);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    pinnedHead ??= response.body.head;
    expect(response.body.head, 'every cursor page keeps the first page head').toEqual(pinnedHead);
    items.push(...response.body.items);
    cursor = response.body.next_cursor;
  } while (cursor);
  expect(pinnedHead).toBeTruthy();
  return { items, head: pinnedHead!, next_cursor: null };
}

function wireFor(page: Page): TourWire {
  const wire: TourWire = { posts: [], legacy: [] };
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const pathname = new URL(request.url()).pathname;
    if (LEGACY_WRITES.test(pathname) || pathname.includes('/composition-revisions')) wire.legacy.push(pathname);
  });
  return wire;
}

async function commitFromGesture(page: Page, wire: TourWire, action: () => Promise<void>): Promise<CommitPost> {
  const responsePromise = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await action();
  const response = await responsePromise;
  const request = response.request();
  const body = request.postDataJSON() as CommitRequest;
  const post: CommitPost = {
    request,
    response,
    body,
    json: await response.json(),
    key: request.headers()['idempotency-key'] ?? '',
  };
  wire.posts.push(post);
  return post;
}

async function openCommandTimeline(page: Page, harness: DirectHarness, seed: ThreeProductsSeed): Promise<void> {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await page.goto(`${harness.origin}/tools/video-editor`);
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('combobox', { name: 'Select project' })).toContainText(harness.seed.projectName);
  await expect(page.getByRole('textbox', { name: 'Track name' }).first()).toBeVisible();
  expect(seed.timelineId).toBe(harness.seed.timelineId);
}

function clipById(document: CanonicalDocument, clipId: string): JsonObject {
  const parent = document.parent_revision.payload as unknown as JsonObject;
  const clips = parent.clips as Array<JsonObject>;
  const clip = clips.find((candidate) => candidate.id === clipId);
  expect(clip, `parent clip ${clipId}`).toBeTruthy();
  return clip!;
}

function assertOnlyParentClipFieldsChanged(before: CanonicalDocument, after: CanonicalDocument, clipIds: string[], fields: string[]): void {
  const beforeParent = before.parent_revision.payload as unknown as JsonObject;
  const afterParent = after.parent_revision.payload as unknown as JsonObject;
  const allowed = new Set(clipIds.flatMap((clipId) => fields.map((field) => `${clipId}:${field}`)));
  const compare = (left: unknown, right: unknown, path: string): void => {
    if (Array.isArray(left) && Array.isArray(right)) {
      expect(right.length, `${path} length is stable`).toBe(left.length);
      left.forEach((value, index) => compare(value, right[index], `${path}[${index}]`));
      return;
    }
    if (left && typeof left === 'object' && right && typeof right === 'object' && !Array.isArray(left) && !Array.isArray(right)) {
      const keys = new Set([...Object.keys(left), ...Object.keys(right)]);
      for (const key of keys) compare((left as JsonObject)[key], (right as JsonObject)[key], `${path}.${key}`);
      return;
    }
    if (canonical(left) === canonical(right)) return;
    const match = /\.clips\[(\d+)\]\.(.+)$/.exec(path);
    if (!match) throw new Error(`unexpected canonical delta at ${path}`);
    const clip = (beforeParent.clips as Array<JsonObject>)[Number(match[1])];
    expect(allowed.has(`${String(clip.id)}:${match[2]}`), `only intended field changed at ${path}`).toBe(true);
  };
  compare(before.parent_revision.payload, after.parent_revision.payload, 'parent');
  expect(before.shot_revisions).toEqual(after.shot_revisions);
  expect(before.internal_timeline_revisions).toEqual(after.internal_timeline_revisions);
  expect(before.dependency_manifest).toEqual(after.dependency_manifest);
}

function assertRawTransitionCleared(before: CanonicalDocument, after: CanonicalDocument, ids: string[]): void {
  const beforeParent = before.parent_revision.payload as unknown as JsonObject;
  const afterParent = after.parent_revision.payload as unknown as JsonObject;
  for (const [key, value] of Object.entries(beforeParent)) {
    if (key !== 'clips') expect((afterParent as JsonObject)[key]).toEqual(value);
  }
  for (const id of ids) {
    const beforeClip = clipById(before, id);
    const afterClip = clipById(after, id);
    expect(Object.hasOwn(afterClip, 'transition'), `${id}: None is raw absence`).toBe(false);
    expect(Object.hasOwn(beforeClip, 'transition')).toBe(true);
  }
  for (const [label, beforeClips, afterClips] of [
    ['parent.clips', beforeParent.clips, afterParent.clips],
    ['parent.config.clips', (beforeParent.config as JsonObject).clips, (afterParent.config as JsonObject).clips],
  ] as const) {
    expect(afterClips, `${label} remains an array`).toEqual(expect.any(Array));
    const beforeRows = beforeClips as Array<JsonObject>;
    const afterRows = afterClips as Array<JsonObject>;
    expect(afterRows.map((clip) => clip.id), `${label} order is stable`).toEqual(beforeRows.map((clip) => clip.id));
    for (const id of ids) {
      const beforeClip = beforeRows.find((clip) => clip.id === id)!;
      const afterClip = afterRows.find((clip) => clip.id === id)!;
      expect(Object.hasOwn(afterClip, 'transition'), `${label}/${id}: None is raw absence`).toBe(false);
      expect(Object.hasOwn(beforeClip, 'transition')).toBe(true);
    }
  }
}

function assertReplyShape(post: CommitPost, before: HeadPin): CommitAcceptedMutation {
  expect(post.response.status(), JSON.stringify(post.json)).toBe(200);
  const envelope = object(post.json, 'commit reply');
  const data = object(envelope.data, 'commit reply data');
  expect(['accepted', 'merged']).toContain(data.status);
  expect(data.base_revision_id).toBe(before.revision_id);
  expect(data.base_publication_id).toBe(before.publication_id);
  expect(data.accepted_revision_id).toEqual(expect.any(String));
  expect(data.canonical_document).toBeTruthy();
  expect(data.document_digest).toEqual(expect.any(String));
  expect(data.merge_mode).toEqual(expect.any(String));
  expect(data.steps).toEqual(expect.any(Array));
  const receipt = object(envelope.receipt, 'accepted receipt');
  expect(receipt.receipt_id).toBe(post.key);
  expect(receipt.result).toEqual(envelope.data);
  if (data.status === 'merged') expect(data.rebased_onto).toMatchObject({ revision_id: expect.any(String), publication_id: expect.any(String) });
  return envelope as unknown as CommitAcceptedMutation;
}

function assertRequestV2(post: CommitPost, before: HeadPin): void {
  expect(post.key).toBeTruthy();
  expect(post.body).toMatchObject({
    api_version: 1,
    project_id: expect.any(String),
    timeline_id: expect.any(String),
    base_revision_id: before.revision_id,
    base_publication_id: before.publication_id,
    commands: expect.any(Array),
  });
  expect(post.body.commands.length).toBeGreaterThan(0);
  expect(post.body.label).toEqual(expect.any(String));
  expect(post.body.steps).toEqual(expect.any(Array));
  expect(post.body.steps!.length).toBeGreaterThan(0);
  for (const step of post.body.steps!) {
    expect(step.id).toEqual(expect.any(String));
    expect(step.command_ordinals.length).toBeGreaterThan(0);
    expect(step.patch).toEqual(expect.any(Array));
    if (step.reads !== undefined) expect(step.reads).toEqual(expect.any(Array));
  }
  expect(['fields', 'atomic']).toContain(post.body.merge ?? 'fields');
  expect(post.body.dry_run ?? false).toBe(false);
  if (post.body.reads !== undefined) expect(post.body.reads).toEqual(expect.any(Array));
}

function assertHistoryMetadata(entry: HistoryEntry, post: CommitPost, result: CommitAcceptedMutation): void {
  expect(entry.intent).toBe('recorded');
  expect(entry.records).not.toBeNull();
  expect(entry.publication_id).toBe(post.key);
  expect(entry.receipt).toEqual(result.receipt);
  expect(entry.publisher).toBe(result.data.publisher);
  expect(entry.label).toBe(post.body.label);
  expect(entry.merge).toBe(post.body.merge ?? 'fields');
  expect(entry.merge_mode).toBe(result.data.merge_mode);
  expect(entry.steps).toEqual(result.data.steps);
  expect(entry.records!.steps).toEqual(result.data.steps);
  expect(entry.records!.commands.map((record) => record.command)).toEqual(post.body.commands);
  for (const step of entry.records!.steps ?? []) {
    expect(step.patch).toEqual(expect.any(Array));
    expect(step.command_ordinals.length).toBeGreaterThan(0);
    if (step.dependencies !== undefined) expect(step.dependencies).toEqual(expect.any(Array));
  }
  for (const record of entry.records!.commands) {
    expect(record.writes.length).toBeGreaterThan(0);
    expect(record.reads.length).toBeGreaterThan(0);
    expect(record.bindings.length).toBeGreaterThan(0);
    expect(record.dependencies).toEqual(expect.any(Array));
  }
  if (post.body.reads !== undefined) expect(entry.reads).toEqual(post.body.reads);
}

function assertHistoryProof(
  entry: HistoryEntry,
  post: CommitPost,
  result: CommitAcceptedMutation,
  original: CanonicalDocument,
  after: CanonicalDocument,
  clipIds: string[],
  fields: string[],
): void {
  assertHistoryMetadata(entry, post, result);
  const patches = (entry.records!.steps ?? []).flatMap((step) => step.patch);
  for (const clipId of clipIds) {
    for (const field of fields) {
      const patch = patches.find((change) => change.ref === `parent/clip:${clipId}` && change.path.at(-1) === field);
      expect(patch, `authoritative step patch for ${clipId}.${field}`).toBeTruthy();
      const beforeValue = clipById(original, clipId)[field];
      expect(patch!.before).toEqual(Object.hasOwn(clipById(original, clipId), field)
        ? { state: 'present', value: beforeValue }
        : { state: 'absent' });
      if (patch!.op === 'set') expect(patch!.value).toEqual(clipById(after, clipId)[field]);
      if (patch!.op === 'remove') expect(Object.hasOwn(clipById(after, clipId), field)).toBe(false);
    }
  }
}

function assertNoNewLegacyEntries(before: HistoryPage, after: HistoryPage): void {
  const known = new Set(before.items.map((entry) => entry.publication_id));
  for (const entry of after.items.filter((candidate) => !known.has(candidate.publication_id))) {
    expect(entry.intent, `new history entry ${entry.publication_id} is recorded`).toBe('recorded');
    expect(entry.records, `new history entry ${entry.publication_id} has records`).not.toBeNull();
    expect(['timeline.commit', 'timeline.inverse']).toContain(entry.receipt.command_kind);
  }
}

function assertCanonicalRestored(original: CanonicalDocument, undone: CanonicalDocument): void {
  expect(undone.parent_revision.payload).toEqual(original.parent_revision.payload);
  expect(undone.shot_revisions).toEqual(original.shot_revisions);
  expect(undone.internal_timeline_revisions).toEqual(original.internal_timeline_revisions);
  expect(undone.dependency_manifest).toEqual(original.dependency_manifest);
}

async function assertReloaded(page: Page, harness: DirectHarness, revision: string): Promise<void> {
  await page.reload();
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('textbox', { name: 'Track name' }).first()).toBeVisible();
  await expect(page.getByTestId('preview-revision-label').filter({ hasText: `Committed ${revision}` }).first()).toBeVisible(CEILING);
  expect(harness.runtimePort).toBeGreaterThan(0);
}

async function transitionSelect(page: Page) {
  return page.getByText('Transition', { exact: true }).locator('xpath=following::*[@role="combobox"][1]');
}

async function clearTransition(page: Page, clipId: string): Promise<void> {
  await page.locator(`[data-clip-id="${clipId}"]`).first().click();
  await page.getByRole('tab', { name: 'Effects', exact: true }).click();
  await (await transitionSelect(page)).click();
  await page.getByRole('option', { name: 'None', exact: true }).click();
  await expect(await transitionSelect(page)).toContainText('None');
}

async function clearTransitionBulk(page: Page, seed: ThreeProductsSeed): Promise<void> {
  await page.locator(`[data-clip-id="${seed.appClipId}"]`).first().click();
  await page.locator(`[data-clip-id="${seed.transitionClipId}"]`).first().click({ modifiers: ['Shift'] });
  await expect(page.getByText('2 clips selected', { exact: true })).toBeVisible();
  await page.getByRole('tab', { name: 'Effects', exact: true }).click();
  await (await transitionSelect(page)).click();
  await page.getByRole('option', { name: 'None', exact: true }).click();
  await expect(await transitionSelect(page)).toContainText('None');
}

async function proveGestureAndUndo(
  page: Page,
  harness: DirectHarness,
  seed: ThreeProductsSeed,
  wire: TourWire,
  before: HistoryPage,
  original: CanonicalDocument,
  gesture: () => Promise<void>,
  expectedClipIds: string[],
  expectedFields: string[],
  assertCommands: (body: CommitRequest) => void,
  assertAfter: (after: CanonicalDocument) => void,
  assertUndo: (undone: CanonicalDocument) => void,
): Promise<void> {
  const post = await commitFromGesture(page, wire, gesture);
  assertRequestV2(post, before.head);
  assertCommands(post.body);
  const result = assertReplyShape(post, before.head);
  const after = result.data.canonical_document;
  assertOnlyParentClipFieldsChanged(original, after, expectedClipIds, expectedFields);
  assertAfter(after);
  const committed = await history(harness, seed);
  const entry = committed.items.find((candidate) => candidate.publication_id === post.key);
  expect(entry, 'history joins by receipt/publication id').toBeTruthy();
  assertHistoryProof(entry!, post, result, original, after, expectedClipIds, expectedFields);
  assertNoNewLegacyEntries(before, committed);
  expect(committed.head.revision_id).toBe(result.data.accepted_revision_id);
  expect(committed.head.publication_id).toBe(post.key);
  await assertReloaded(page, harness, result.data.accepted_revision_id);
  expect(wire.legacy, 'the mounted gesture has no old-route write').toEqual([]);

  const inverse = await commitFromGesture(page, wire, async () => {
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
  });
  assertRequestV2(inverse, pinOf(result));
  const inverseResult = assertReplyShape(inverse, pinOf(result));
  const undone = inverseResult.data.canonical_document;
  assertCanonicalRestored(original, undone);
  assertUndo(undone);
  expect(inverse.body.commands).toEqual([expect.objectContaining({ op: 'timeline.inverse', args: { publications: [post.key] } })]);
  const finalHistory = await history(harness, seed);
  const inverseEntry = finalHistory.items.find((candidate) => candidate.publication_id === inverse.key);
  expect(inverseEntry, 'Undo history joins by receipt/publication id').toBeTruthy();
  assertHistoryMetadata(inverseEntry!, inverse, inverseResult);
  expect(inverseEntry?.records?.undo_of).toEqual([post.key]);
  assertNoNewLegacyEntries(before, finalHistory);
  expect(finalHistory.head).toEqual(pinOf(inverseResult));
  expect(wire.legacy, 'mounted Undo has no old-route write').toEqual([]);
}

test('P2 mounted single parent move: v2 commit, exact field delta, reload and guarded Undo', async ({ page, harness, seed3 }) => {
  await openCommandTimeline(page, harness, seed3);
  const wire = wireFor(page);
  const before = await history(harness, seed3);
  const original = await canonicalDocumentAt(harness, seed3, before.head.revision_id);
  const from = Number(clipById(original, seed3.appClipId).at);
  await proveGestureAndUndo(page, harness, seed3, wire, before, original,
    async () => {
      const clip = page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first();
      const reference = page.locator(`.clip-action[data-clip-id="${seed3.transitionClipId}"]`).first();
      const clipBox = await clip.boundingBox();
      const referenceBox = await reference.boundingBox();
      if (!clipBox || !referenceBox) throw new Error('mounted parent clips are not measurable');
      const pixelsPerSecond = (referenceBox.x - clipBox.x) / (THREE_PRODUCTS_REFERENCE_AT - from);
      await page.mouse.move(clipBox.x + Math.min(clipBox.width / 2, 24), clipBox.y + clipBox.height / 2);
      await page.mouse.down();
      await page.mouse.move(clipBox.x + Math.min(clipBox.width / 2, 24) + (5 - from) * pixelsPerSecond, clipBox.y + clipBox.height / 2, { steps: 12 });
      await page.mouse.up();
    },
    [seed3.appClipId], ['at'],
    (body) => expect(body.commands).toEqual([expect.objectContaining({
      op: 'clip.move', select: `parent/clip:${seed3.appClipId}`, args: { on: 5 },
    })]),
    (after) => expect(clipById(after, seed3.appClipId).at).toBe(5),
    (undone) => expect(clipById(undone, seed3.appClipId).at).toBe(from));
});

test('P2 mounted transition None single: raw clear preserves opaque data/order and guarded Undo', async ({ page, harness, seed3 }) => {
  await openCommandTimeline(page, harness, seed3);
  const wire = wireFor(page);
  const before = await history(harness, seed3);
  const original = await canonicalDocumentAt(harness, seed3, before.head.revision_id);
  await proveGestureAndUndo(page, harness, seed3, wire, before, original,
    () => clearTransition(page, seed3.transitionClipId),
    [seed3.transitionClipId], ['transition'],
    (body) => {
      expect(body.commands).toHaveLength(1);
      expect(body.commands[0]).toMatchObject({ op: 'clip.set', select: `parent/clip:${seed3.transitionClipId}` });
      expect(body.commands[0]!.args).toEqual({ values: {}, clear: ['transition'] });
    },
    (after) => assertRawTransitionCleared(original, after, [seed3.transitionClipId]),
    (undone) => expect(clipById(undone, seed3.transitionClipId).transition).toEqual(clipById(original, seed3.transitionClipId).transition));
});

test('P2 mounted transition None bulk: atomic raw clears preserve unknown fields/order and guarded Undo', async ({ page, harness, seed3 }) => {
  await openCommandTimeline(page, harness, seed3);
  const wire = wireFor(page);
  const before = await history(harness, seed3);
  const original = await canonicalDocumentAt(harness, seed3, before.head.revision_id);
  const ids = [seed3.appClipId, seed3.transitionClipId];
  await proveGestureAndUndo(page, harness, seed3, wire, before, original,
    () => clearTransitionBulk(page, seed3), ids, ['transition'],
    (body) => {
      expect(body.commands).toHaveLength(ids.length);
      for (const command of body.commands) {
        expect(command).toMatchObject({ op: 'clip.set', select: expect.stringMatching(/^parent\/clip:/) });
        expect(command.args).toEqual({ values: {}, clear: ['transition'] });
      }
      expect(body.commands.map((command) => command.select).sort()).toEqual(ids.map((id) => `parent/clip:${id}`).sort());
    },
    (after) => assertRawTransitionCleared(original, after, ids),
    (undone) => {
      for (const id of ids) expect(clipById(undone, id).transition).toEqual(clipById(original, id).transition);
    });
});
