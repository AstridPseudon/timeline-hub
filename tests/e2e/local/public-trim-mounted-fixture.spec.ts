import { expect, type Page, type Route } from '@playwright/test';
import { commandOutboxes, test as appTest } from './support/app.ts';
import { ASTRID_PYTHON } from './support/astrid.ts';
import type { CommitAcceptedMutation, CommitRequest, HistoryPage } from '../../../src/integrations/runtime/timeline-commit-types.ts';
import type { DirectHarness, ThreeProductsSeed } from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;

type CommitPost = { body: CommitRequest; rawBody: string; key: string; status: number | null; response: CommitAcceptedMutation | null };
const test = appTest.extend<object, { seed3: ThreeProductsSeed }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
});

test.beforeAll(() => {
  for (const name of ['TIMELINE_BUNDLE_AGENT_HEAD', 'TIMELINE_BUNDLE_RUNTIME_HEAD']) {
    if (!/^[0-9a-f]{40}$/.test(process.env[name] ?? '')) throw new Error(`the public-trim fixture requires ${name} as a full 40-character SHA`);
  }
});

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const result = await harness.runtimeJson<HistoryPage>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  return result.body;
}

async function revision(harness: DirectHarness, seed: ThreeProductsSeed, id: string) {
  const result = await harness.runtimeJson<Record<string, any>>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${id}`);
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  return result.body.payload as Record<string, any>;
}

function parentClip(parent: Record<string, any>, clipId: string) {
  const clips = (parent.clips as Array<Record<string, any>>).filter((clip) => clip.id === clipId);
  expect(clips).toHaveLength(1);
  return clips[0];
}

async function openFixture(page: Page, harness: DirectHarness, seed: ThreeProductsSeed) {
  await page.goto(`${harness.devOrigin}/tests/e2e/fixtures/public-trim/index.html?project=${encodeURIComponent(harness.seed.projectId)}&timeline=${encodeURIComponent(seed.timelineId)}`);
  await expect(page.getByTestId('public-trim-trigger')).toBeEnabled(CEILING);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).some((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
}

async function waitForPost(posts: CommitPost[], index: number) {
  await expect.poll(() => posts[index]?.status, CEILING).not.toBeNull();
  await expect.poll(() => posts[index]?.response, CEILING).not.toBeNull();
  return posts[index];
}

test('M2 public trim fixture: source window, exact retry/reload, guarded undo and no legacy traffic', async ({ page, harness, seed3 }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await harness.startPublicTrimFixtureDevServer();
  const posts: CommitPost[] = [];
  const legacy: string[] = [];
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const pathname = new URL(request.url()).pathname;
    if (COMMITS.test(pathname)) posts.push({ body: request.postDataJSON() as CommitRequest, rawBody: request.postData() ?? '', key: request.headers()['idempotency-key'], status: null, response: null });
    if (/composition-revisions$/.test(pathname)) legacy.push(pathname);
  });
  page.on('response', (response) => {
    if (!COMMITS.test(new URL(response.url()).pathname)) return;
    const post = [...posts].reverse().find((candidate) => candidate.key === response.request().headers()['idempotency-key']);
    if (post) { post.status = response.status(); void response.json().then((body) => { post.response = body as CommitAcceptedMutation; }); }
  });

  await openFixture(page, harness, seed3);
  const before = await history(harness, seed3);
  const original = await revision(harness, seed3, before.head.revision_id);
  const originalAppClip = structuredClone(parentClip(original, seed3.appClipId));
  await page.getByTestId('public-trim-trigger').click();
  await waitForPost(posts, 0);
  expect(posts[0].body.commands).toEqual([expect.objectContaining({ op: 'clip.trim', select: `parent/clip:${seed3.transitionClipId}`, args: { in_s: null, out_s: 2.5 } })]);
  expect(posts[0].status).toBe(200);
  const first = posts[0].response!;
  const firstParent = first.data.canonical_document.parent_revision.payload as Record<string, any>;
  expect(parentClip(firstParent, seed3.transitionClipId)).toMatchObject({ from: 0, to: 2.5, hold: 2.5 });
  expect(parentClip(firstParent, seed3.appClipId)).toEqual(originalAppClip);
  const firstPublication = first.receipt.receipt_id;

  await page.reload();
  await expect(page.getByTestId('public-trim-trigger')).toBeEnabled(CEILING);
  await page.getByTestId('public-trim-undo').click();
  await waitForPost(posts, 1);
  expect(posts[1].body.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [firstPublication] } }]);
  expect(posts[1].response!.data.canonical_document.parent_revision.payload).toEqual(original);

  let heldRoute: Route | undefined;
  let holdAck = true;
  const retryPosts: CommitPost[] = [];
  const holdRetry = async (route: Route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    const response = await route.fetch({ maxRetries: 0 });
    const post = { body: route.request().postDataJSON() as CommitRequest, rawBody: route.request().postData() ?? '', key: route.request().headers()['idempotency-key'], status: response.status(), response: await response.json() as CommitAcceptedMutation };
    retryPosts.push(post);
    if (holdAck) heldRoute = route; else await route.fulfill({ response });
  };
  await page.route(COMMITS, holdRetry);
  await page.getByTestId('public-trim-trigger').click();
  await expect.poll(() => retryPosts.length, CEILING).toBe(1);
  const originalRetry = retryPosts[0];
  holdAck = false;
  await heldRoute!.abort('connectionreset');
  await page.unroute(COMMITS, holdRetry);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.pending)?.pending?.outcome?.kind, CEILING).toBe('retry');
  await page.reload();
  await expect(page.getByTestId('public-trim-recover')).toBeEnabled(CEILING);
  const retryResponse = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByTestId('public-trim-recover').click();
  const response = await retryResponse;
  expect(response.status()).toBe(200);
  expect(response.request().postData()).toBe(originalRetry.rawBody);
  expect(response.request().headers()['idempotency-key']).toBe(originalRetry.key);
  const retried = await response.json() as CommitAcceptedMutation;
  const retriedParent = retried.data.canonical_document.parent_revision.payload as Record<string, any>;
  expect(parentClip(retriedParent, seed3.transitionClipId)).toMatchObject({ from: 0, to: 2.5, hold: 2.5 });
  expect(parentClip(retriedParent, seed3.appClipId)).toEqual(originalAppClip);
  expect(legacy).toEqual([]);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  expect((await history(harness, seed3)).items).toHaveLength(before.items.length + 3);
});
