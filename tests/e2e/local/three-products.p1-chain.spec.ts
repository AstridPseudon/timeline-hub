/** P1: the mounted App's local split -> trim chain through the durable v2 save session. */
import { expect, type Page, type Route } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import type { CommitRequest } from '../../../src/integrations/runtime/timeline-commit-types.ts';
import { APP_ENTRY_ROUTE, commandOutboxes, expectConnected, firstTrackName, test as appTest } from './support/app.ts';
import { ASTRID_PYTHON, AstridCli } from './support/astrid.ts';
import { compositionPublication, harnessUnavailableReason, type DirectHarness } from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_WRITES = /\/timelines\/[^/]+\/composition-revisions$/;
const SOURCE_ID = 'p1-chain-source';
const SPLIT_AT = 2;

type ChainSeed = { projectSlug: string; timelineId: string; sourceId: string };
type CommitPost = { body: CommitRequest; raw: string; key: string; status?: number; response?: any };

const test = appTest.extend<object, { astrid: AstridCli }>({
  astrid: async ({ harness }, use) => {
    const client = await AstridCli.create(harness);
    await client.preflight();
    await use(client);
  },
});

test.beforeAll(() => {
  const reason = harnessUnavailableReason();
  if (reason) throw new Error(`P1 chain cannot run: ${reason}`);
});

function pin(result: any) {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

async function seedOneClip(harness: DirectHarness): Promise<ChainSeed> {
  const timelineId = randomUUID();
  const publication = compositionPublication({ projectId: harness.seed.projectId, timelineId }, null, 'P1 chain', 30);
  const clip = {
    id: SOURCE_ID, at: 0, track: 'V1', clipType: 'media', asset: 'p1-video', from: 0, to: 8, speed: 1, hold: 8,
    app: { opaque: { keep: null, ordered: [false, 0, ''] }, astrid: { for: 8 } },
  };
  const parent = publication.parent_composition as Record<string, any>;
  parent.config = { ...parent.config, clips: [clip], opaque: { root: null, order: [0, false] } };
  parent.clips = [clip];
  parent.registry = { assets: {
    'p1-video': { file: harness.seed.video.mediaType === 'video/webm' ? 'p1-video.webm' : 'p1-video.mp4',
      type: harness.seed.video.mediaType, duration: 8, media_id: harness.seed.video.objectId, content_sha256: harness.seed.video.digest },
  } };
  const published = await harness.runtimeJson('POST', `/v1/projects/${harness.seed.projectId}/timelines/${timelineId}/composition-revisions`, publication);
  expect(published.status, JSON.stringify(published.body)).toBe(200);
  const project = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}`);
  return { projectSlug: project.body.data.slug, timelineId, sourceId: SOURCE_ID };
}

async function history(harness: DirectHarness, seed: ChainSeed) {
  const result = await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(result.status, JSON.stringify(result.body)).toBe(200);
  return result.body;
}

function observe(page: Page) {
  const posts: CommitPost[] = [];
  const legacy: string[] = [];
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const path = new URL(request.url()).pathname;
    if (COMMITS.test(path)) posts.push({ body: JSON.parse(request.postData() ?? '{}'), raw: request.postData() ?? '', key: request.headers()['idempotency-key'] });
    if (LEGACY_WRITES.test(path)) legacy.push(path);
  });
  page.on('response', (response) => {
    if (!COMMITS.test(new URL(response.url()).pathname)) return;
    const post = [...posts].reverse().find((candidate) => candidate.key === response.request().headers()['idempotency-key']);
    if (!post) return;
    post.status = response.status();
    void response.json().then((body) => { post.response = body; }).catch(() => {});
  });
  return { posts, legacy };
}

async function openChain(page: Page, harness: DirectHarness, seed: ChainSeed) {
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}?localProject=${encodeURIComponent(seed.projectSlug)}&localTimeline=${encodeURIComponent(seed.timelineId)}`);
  await expectConnected(page);
  await expect(firstTrackName(page)).toBeVisible();
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).some((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
}

async function splitSource(page: Page, seed: ChainSeed) {
  await page.locator(`.clip-action[data-clip-id="${seed.sourceId}"]`).click();
  await page.keyboard.press('ArrowRight');
  await page.keyboard.press('s');
}

async function trimSourceWindow(page: Page, clipId: string, value: string) {
  await page.locator(`.clip-action[data-clip-id="${clipId}"]`).click();
  await page.getByRole('tab', { name: 'Timing', exact: true }).click();
  const field = page.getByLabel('Source In');
  await expect(field).toBeVisible();
  const input = field.locator('input:not([aria-hidden="true"])');
  await expect(input).toBeEditable();
  await input.fill(value);
  await input.press('Enter');
  await input.press('Tab');
}

async function forward(route: Route, response: any, body: any) {
  await route.fulfill({ status: response.status(), headers: response.headers(), body: JSON.stringify(body) });
}

test('P1 split -> trim new clip: accepted split, merged trim after Agent edit, lost ACK restart and exact retry', async ({ page, harness, astrid }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const seed = await seedOneClip(harness);
  const traffic = observe(page);
  let holdTrim = false;
  let heldTrim: Route | undefined;
  await page.route(COMMITS, async (route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    const response = await route.fetch({ maxRetries: 0 });
    const body = await response.json();
    const post = traffic.posts.find((candidate) => candidate.key === route.request().headers()['idempotency-key']);
    if (post && holdTrim && traffic.posts.indexOf(post) === 1) {
      post.status = response.status(); post.response = body; heldTrim = route; return;
    }
    await forward(route, response, body);
  });
  await openChain(page, harness, seed);
  const before = await history(harness, seed);
  const original = (await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${before.head.revision_id}`)).body.payload;
  expect(original.clips).toHaveLength(1);
  const originalClip = structuredClone(original.clips[0]);
  await splitSource(page, seed);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  await expect.poll(() => traffic.posts[0].status, CEILING).not.toBeUndefined();
  await expect.poll(() => traffic.posts[0].response, CEILING).not.toBeUndefined();
  const split = traffic.posts[0];
  expect(split.status).toBe(200);
  const splitCommand = split.body.commands[0] as any;
  expect(splitCommand).toMatchObject({ schema_version: 1, op: 'doc.patch', version: '1', select: null });
  const changes = splitCommand.args.changes as Array<any>;
  const inserted = changes.find((change) => change.op === 'list.insert' && change.path.join('.') === 'clips');
  expect(inserted).toMatchObject({ before: { state: 'absent' }, value: { clipType: 'media', track: 'V1' } });
  expect(inserted.id).toMatch(/^p1-chain-source-/);
  const rightId = inserted.id;
  expect(split.body).toMatchObject({ api_version: 1, project_id: harness.seed.projectId, timeline_id: seed.timelineId,
    base_revision_id: before.head.revision_id, base_publication_id: before.head.publication_id,
    source: { via: 'app' }, merge: 'atomic', dry_run: false, label: expect.any(String), commands: [splitCommand] });
  expect(split.body.steps[0]).toMatchObject({ command_ordinals: [0], patch: splitCommand.args.changes });
  expect(split.response.data).toMatchObject({ document_digest: expect.any(String), commands: split.body.commands,
    id_map: expect.any(Object), provider_version: expect.any(String), compiler_version: expect.any(String),
    steps: expect.any(Array), dependencies: expect.any(Array), merge_mode: expect.any(String) });
  expect(split.response.receipt).toMatchObject({ receipt_id: expect.any(String), idempotency_key: split.key,
    request_hash: expect.any(String), result: split.response.data });
  const splitDocument = split.response.data.canonical_document.parent_revision.payload;
  expect(splitDocument.clips.map((clip: any) => clip.id)).toEqual([SOURCE_ID, rightId]);
  const originalFields = Object.fromEntries(Object.entries(originalClip).filter(([key]) => key !== 'app'));
  expect(splitDocument.clips[0]).toMatchObject({ ...originalFields, to: SPLIT_AT, hold: SPLIT_AT });
  expect(splitDocument.clips[1]).toMatchObject({ ...originalFields, id: rightId, at: SPLIT_AT, from: SPLIT_AT, to: originalClip.to, hold: originalClip.to - SPLIT_AT });
  expect(splitDocument.clips[0].app.opaque).toEqual(originalClip.app.opaque);
  expect(splitDocument.clips[1].app.opaque).toEqual(originalClip.app.opaque);
  expect(splitDocument.config.clips).toEqual(splitDocument.clips);
  expect(splitDocument.clips[0].app.astrid).toMatchObject({ for: SPLIT_AT });
  expect(splitDocument.clips[1].app).not.toHaveProperty('astrid');
  expect(splitDocument.config.opaque).toEqual({ root: null, order: [0, false] });
  expect(splitDocument.registry).toEqual((await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${split.response.data.accepted_revision_id}`)).body.payload.registry);

  holdTrim = true;
  await trimSourceWindow(page, rightId, '3');
  await expect.poll(() => traffic.posts.length, CEILING).toBe(2);
  await expect.poll(() => traffic.posts[1].status, CEILING).not.toBeUndefined();
  const trim = traffic.posts[1];
  expect(trim.status).toBe(200);
  expect(trim.body.commands[0]).toMatchObject({ op: 'doc.patch', select: null });
  const trimChange = (trim.body.commands[0] as any).args.changes.find((change: any) => change.path.includes(`id:${rightId}`) && change.path.at(-1) === 'from');
  expect(trimChange).toMatchObject({ value: 3, before: { state: 'present', value: SPLIT_AT } });

  const agent = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, pin(split.response), { kind: 'label', trackId: 'V1', label: 'Agent edit after split' }, 'p1-agent-after-split');
  expect(agent.data.status).toMatch(/^(accepted|rebased)$/);
  expect(heldTrim).toBeTruthy();
  const originalTrim = { raw: trim.raw, key: trim.key };
  await heldTrim!.abort('connectionreset');
  await page.unroute(COMMITS);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).some((owner) => owner.pending?.outcome?.kind === 'retry'), CEILING).toBe(true);
  const owner = (await commandOutboxes(page, seed.timelineId)).find((candidate) => candidate.pending?.request.key === originalTrim.key)!;
  expect(owner.pending?.request).toMatchObject({ body: originalTrim.raw, key: originalTrim.key });
  await page.reload();
  await openChain(page, harness, seed);
  const restarted = await harness.restartRuntime();
  expect(restarted.oldInstanceId).toBeTruthy();
  await expectConnected(page);
  const recovered = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${owner.ownerId}"]`)).click();
  const retryResponse = await recovered;
  expect(retryResponse.status()).toBe(200);
  expect(retryResponse.request().postData()).toBe(originalTrim.raw);
  expect(retryResponse.request().headers()['idempotency-key']).toBe(originalTrim.key);
  const retry = await retryResponse.json();
  expect(retry.data.status).toMatch(/^(merged|rebased)$/);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  expect(traffic.legacy).toEqual([]);
  const final = (await history(harness, seed)).items;
  expect(final).toHaveLength(before.items.length + 3);
  expect((await history(harness, seed)).items.filter((item: any) => item.receipt?.idempotency_key === originalTrim.key)).toHaveLength(1);
});

test('P1 split -> trim new clip: a real Agent move refuses the stale trim and the App rolls back with a message', async ({ page, harness, astrid }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const seed = await seedOneClip(harness);
  const traffic = observe(page);
  await openChain(page, harness, seed);
  const before = await history(harness, seed);
  await splitSource(page, seed);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  await expect.poll(() => traffic.posts[0].response, CEILING).not.toBeUndefined();
  const split = traffic.posts[0];
  const inserted = (split.body.commands[0] as any).args.changes.find((change: any) => change.op === 'list.insert');
  const rightId = inserted.id;
  const agent = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, pin(split.response), { kind: 'move', clipId: rightId, on: 3 }, 'p1-agent-conflict');
  expect(agent.data.status).toMatch(/^(accepted|rebased)$/);
  await trimSourceWindow(page, rightId, '3');
  await expect.poll(() => traffic.posts.length, CEILING).toBe(2);
  await expect.poll(() => traffic.posts[1].status, CEILING).not.toBeUndefined();
  expect(traffic.posts[1].status).toBe(409);
  expect(traffic.posts[1].response.details.status).toBe('conflict');
  await expect(page.getByTestId('timeline-command-recovery')).toContainText('Your changes are retained and need resolution before they can be saved.');
  const current = await history(harness, seed);
  expect(current.items).toHaveLength(before.items.length + 2);
  expect(current.head.revision_id).toBe(agent.data.accepted_revision_id);
  expect(traffic.legacy).toEqual([]);
});
