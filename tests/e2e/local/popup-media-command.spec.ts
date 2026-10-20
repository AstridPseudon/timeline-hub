import { expect, type Locator, type Page, type Route } from '@playwright/test';
import {
  commandOutboxes,
  expectConnected,
  openApp,
  openEmbeddedCanonicalShot,
  openSeededTimeline,
  revisionBody,
  test as appTest,
} from './support/app.ts';
import { ASTRID_PYTHON } from './support/astrid.ts';
import { harnessUnavailableReason, makePng, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';
import type { CommitAcceptedMutation, CommitRequest } from '../../../src/integrations/runtime/timeline-commit-types.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_SAVES = /\/timelines\/[^/]+\/composition-revisions$/;
const MEDIA_SELECTION = /\/media-selection(?:\/verified)?(?:\?|$)/;

type CommitPost = {
  body: CommitRequest;
  rawBody: string;
  key: string;
  status: number | null;
  response: CommitAcceptedMutation | null;
};

const test = appTest.extend<object, { seed3: ThreeProductsSeed }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
});

test.beforeAll(() => {
  const reason = harnessUnavailableReason();
  if (reason) throw new Error(`the popup media journey cannot run: ${reason}`);
  for (const name of ['TIMELINE_BUNDLE_AGENT_HEAD', 'TIMELINE_BUNDLE_RUNTIME_HEAD']) {
    if (!/^[0-9a-f]{40}$/.test(process.env[name] ?? '')) {
      throw new Error(`the popup media cohort requires ${name} as a full 40-character SHA`);
    }
  }
});

test.describe.configure({ mode: 'serial' });

function observeTraffic(page: Page) {
  const posts: CommitPost[] = [];
  const legacy: string[] = [];
  const mediaSelections: string[] = [];
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (request.method() === 'POST' && COMMITS.test(pathname)) {
      posts.push({
        body: JSON.parse(request.postData() ?? '{}') as CommitRequest,
        rawBody: request.postData() ?? '',
        key: request.headers()['idempotency-key'],
        status: null,
        response: null,
      });
    }
    if (request.method() === 'POST' && LEGACY_SAVES.test(pathname)) legacy.push(pathname);
    if (request.method() === 'GET' && MEDIA_SELECTION.test(pathname + new URL(request.url()).search)) {
      mediaSelections.push(pathname + new URL(request.url()).search);
    }
  });
  page.on('response', (response) => {
    if (response.request().method() !== 'POST' || !COMMITS.test(new URL(response.url()).pathname)) return;
    const post = [...posts].reverse().find((candidate) => candidate.key === response.request().headers()['idempotency-key']);
    if (!post) return;
    post.status = response.status();
    void response.json().then((body) => { post.response = body as CommitAcceptedMutation; }).catch(() => {});
  });
  return { posts, legacy, mediaSelections };
}

async function waitForPost(posts: CommitPost[], index: number) {
  await expect.poll(() => posts[index]?.status, CEILING).toBe(200);
  await expect.poll(() => posts[index]?.response, CEILING).not.toBeNull();
  return posts[index]!;
}

async function openParent(page: Page, harness: DirectHarness) {
  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await expect.poll(async () => (await commandOutboxes(page, harness.seed.timelineId)).some((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
}

async function rawShotState(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string) {
  const parent = (await revisionBody(harness, revisionId)).payload as Record<string, any>;
  const occurrence = (parent.occurrences as Array<Record<string, any>>).find((item) => item.occurrence_id === seed.occurrenceId);
  expect(occurrence).toBeTruthy();
  const shotResponse = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/shots/${seed.shotId}/revisions/${occurrence!.shot_revision_id}`);
  expect(shotResponse.status, JSON.stringify(shotResponse.body)).toBe(200);
  const shot = shotResponse.body as Record<string, any>;
  const internalResponse = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${shot.internal_timeline_revision_id}`);
  expect(internalResponse.status, JSON.stringify(internalResponse.body)).toBe(200);
  const internal = internalResponse.body as Record<string, any>;
  return { parent, occurrence, shot, internal, clips: internal.payload.clips as Array<Record<string, any>> };
}

function accepted(post: CommitPost): CommitAcceptedMutation {
  expect(post.status, JSON.stringify(post.response)).toBe(200);
  expect(post.response?.data.status).toMatch(/^(accepted|rebased)$/);
  return post.response!;
}

function fiveFieldSelection(value: unknown): asserts value is Record<string, string> {
  expect(value).toBeTruthy();
  expect(Object.keys(value as object).sort()).toEqual(['asset', 'catalog_digest', 'generation_id', 'object_id', 'variant_id']);
  for (const key of ['asset', 'generation_id', 'variant_id', 'object_id', 'catalog_digest']) {
    expect((value as Record<string, unknown>)[key]).toEqual(expect.any(String));
  }
  expect((value as Record<string, string>).object_id).toMatch(/^sha256:[0-9a-f]{64}$/);
  expect((value as Record<string, string>).catalog_digest).toMatch(/^sha256:[0-9a-f]{64}$/);
}

async function chooseMedia(dialog: Locator, name: string, width: number, height: number) {
  const chooser = dialog.getByLabel('Choose media for shot timeline');
  await expect(chooser).toHaveCount(1);
  await chooser.setInputFiles({ name, mimeType: 'image/png', buffer: makePng(width, height) });
}

test('M2 real popup media ADD/SWAP: raw preservation, occurrence isolation, reload retry, Runtime undo and zero legacy', async ({ page, harness, seed3 }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const traffic = observeTraffic(page);
  await openParent(page, harness);
  const beforeHead = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed3.timelineId}/composition-revisions?limit=1`)).body.items.find((item: any) => item.is_current_head).revision_id as string;
  const before = await rawShotState(harness, seed3, beforeHead);
  const beforeOpaqueChild = structuredClone(before.clips.find((clip) => clip.id === seed3.agentClipId));
  const beforeParent = structuredClone(before.parent);
  const beforeOccurrence = structuredClone(before.occurrence);

  const dialog = await openEmbeddedCanonicalShot(page, seed3.occurrenceId, 'F2 canonical shot');
  await dialog.locator('[data-track-id="V2"]').click();
  await expect(dialog.getByRole('button', { name: 'Add media', exact: true })).toBeEnabled();
  await chooseMedia(dialog, 'popup-add.png', 33, 31);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  const addPost = await waitForPost(traffic.posts, 0);
  expect(addPost.body).not.toHaveProperty('parent_composition');
  const addCommand = addPost.body.commands[0];
  expect(addCommand).toMatchObject({
    schema_version: 1,
    op: 'occurrence.add-media',
    version: '1',
    select: `occurrence:${seed3.occurrenceId}`,
    intent: { ownership: 'occurrence' },
  });
  fiveFieldSelection(addCommand.args.media);
  const addRow = addCommand.args.row as Record<string, any>;
  expect(addRow).toMatchObject({ clipType: 'image', track: 'V2', asset: (addCommand.args.media as any).asset });
  expect(addRow.id).toMatch(/^popup-child-/);
  const addResult = accepted(addPost);
  const addedState = await rawShotState(harness, seed3, addResult.data.accepted_revision_id);
  expect(addedState.parent).toEqual(beforeParent);
  expect(addedState.occurrence).toEqual(beforeOccurrence);
  expect(addedState.clips.find((clip) => clip.id === seed3.agentClipId)).toEqual(beforeOpaqueChild);
  expect(addedState.clips).toContainEqual(expect.objectContaining({ id: addRow.id, asset: addRow.asset, track: 'V2' }));
  expect(traffic.mediaSelections.some((path) => path.includes('/media-selection?'))).toBe(true);
  expect(traffic.mediaSelections.some((path) => path.includes('/media-selection/verified?'))).toBe(true);

  const addedClip = dialog.locator(`[data-clip-id="${seed3.occurrenceId}:${addRow.id}"]`);
  await expect(addedClip).toBeVisible(CEILING);
  await addedClip.click();
  await expect(dialog.getByRole('button', { name: 'Swap selected clip', exact: true })).toBeEnabled();

  let heldRoute: Route | undefined;
  await page.route(COMMITS, async (route) => {
    if (heldRoute || route.request().method() !== 'POST') return route.fallback();
    const response = await route.fetch({ maxRetries: 0 });
    const post = traffic.posts.find((candidate) => candidate.key === route.request().headers()['idempotency-key']);
    if (!post) throw new Error('swap commit was not observed');
    post.status = response.status();
    post.response = await response.json() as CommitAcceptedMutation;
    heldRoute = route;
  });
  await chooseMedia(dialog, 'popup-swap.png', 35, 29);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(2);
  const swapPost = await waitForPost(traffic.posts, 1);
  expect(swapPost.body.commands[0]).toMatchObject({
    op: 'occurrence.swap-media',
    select: `occurrence:${seed3.occurrenceId}/clip:${addRow.id}`,
    intent: { ownership: 'occurrence' },
  });
  const swapArgs = swapPost.body.commands[0].args as any;
  fiveFieldSelection(swapArgs.old_media);
  fiveFieldSelection(swapArgs.media);
  expect(swapArgs.old_media).toEqual(addCommand.args.media);
  expect(swapArgs.media).not.toEqual(swapArgs.old_media);
  const swapResult = accepted(swapPost);
  const swappedState = await rawShotState(harness, seed3, swapResult.data.accepted_revision_id);
  expect(swappedState.parent).toEqual(beforeParent);
  expect(swappedState.occurrence).toEqual(beforeOccurrence);
  expect(swappedState.clips.find((clip) => clip.id === seed3.agentClipId)).toEqual(beforeOpaqueChild);
  expect(swappedState.clips.find((clip) => clip.id === addRow.id)).toEqual(expect.objectContaining({ ...addRow, asset: swapArgs.media.asset }));

  const pendingOwner = (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.pending?.request.key === swapPost.key);
  expect(pendingOwner, 'the uncertain swap remains in the durable outbox').toBeTruthy();
  expect(pendingOwner?.pending?.request.body).toBe(swapPost.rawBody);
  await heldRoute!.abort('connectionreset');
  await page.unroute(COMMITS);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.ownerId === pendingOwner!.ownerId)?.pending?.outcome?.kind, CEILING).toBe('retry');

  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const recovered = page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${pendingOwner!.ownerId}"]`));
  await expect(recovered).toBeVisible(CEILING);
  await recovered.click();
  await expect.poll(() => traffic.posts.length, CEILING).toBe(3);
  const retryPost = await waitForPost(traffic.posts, 2);
  expect(retryPost.rawBody).toBe(swapPost.rawBody);
  expect(retryPost.key).toBe(swapPost.key);
  expect(accepted(retryPost).data.canonical_document).toEqual(swapResult.data.canonical_document);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);

  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  await expect.poll(() => traffic.posts.length, CEILING).toBe(4);
  const undoPost = await waitForPost(traffic.posts, 3);
  expect(undoPost.body.commands).toEqual([{
    schema_version: 1,
    op: 'timeline.inverse',
    version: '1',
    select: null,
    args: { publications: [swapResult.receipt.receipt_id] },
  }]);
  const undone = accepted(undoPost);
  expect(undone.data.canonical_document.parent_revision.payload).toEqual(addResult.data.canonical_document.parent_revision.payload);
  expect(traffic.legacy, 'popup ADD/SWAP never posts the canonical legacy graph writer').toEqual([]);
});
