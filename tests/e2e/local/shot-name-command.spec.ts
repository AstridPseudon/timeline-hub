/** The mounted canonical shot-name command: one real parent session, one Runtime door, no fallback writer. */
import { execFileSync } from 'node:child_process';
import { expect, type Page, type Route } from '@playwright/test';
import {
  harnessUnavailableReason,
  REPO_ROOT,
  RUNTIME_CHECKOUT,
  type DirectHarness,
  type ThreeProductsSeed,
} from './support/harness.ts';
import {
  commandOutboxes,
  embeddedShotNameInput,
  expectConnected,
  openApp,
  openEmbeddedCanonicalShot,
  openSeededTimeline,
  revisionBody,
  test as appTest,
} from './support/app.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON } from './support/astrid.ts';
import type { CanonicalDocument, CommitAcceptedMutation, CommitRequest, HeadPin } from '../../../src/integrations/runtime/timeline-commit-types.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_SAVES = /\/timelines\/[^/]+\/composition-revisions$/;
const SHOT_NAME = 'F2 canonical shot';
const ACCEPTED_NAME = 'Édit 🎬';
const RETRY_NAME = 'F2 retry survives restart';
const CONFLICT_DRAFT = '  same-name draft 🎬  ';

type CommitPost = {
  body: CommitRequest;
  rawBody: string;
  key: string;
  status: number | null;
  response: any;
};

const test = appTest.extend<object, { seed3: ThreeProductsSeed }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
});

test.beforeAll(() => {
  const reason = harnessUnavailableReason();
  if (reason) throw new Error(`the shot-name journey cannot run: ${reason}`);
  for (const name of ['TIMELINE_BUNDLE_AGENT_HEAD', 'TIMELINE_BUNDLE_RUNTIME_HEAD']) {
    if (!/^[0-9a-f]{40}$/.test(process.env[name] ?? '')) {
      throw new Error(`the shot-name cohort requires ${name} as a full 40-character SHA`);
    }
  }
  const git = (checkout: string, ...args: string[]) => execFileSync('git', ['-C', checkout, ...args], { encoding: 'utf8' }).trim();
  expect(git(ASTRID_CHECKOUT, 'rev-parse', 'HEAD')).toBe(process.env.TIMELINE_BUNDLE_AGENT_HEAD);
  expect(git(RUNTIME_CHECKOUT, 'rev-parse', 'HEAD')).toBe(process.env.TIMELINE_BUNDLE_RUNTIME_HEAD);
  expect(git(ASTRID_CHECKOUT, 'status', '--porcelain', '--untracked-files=normal')).toBe('');
  expect(git(RUNTIME_CHECKOUT, 'status', '--porcelain', '--untracked-files=normal')).toBe('');
  console.log('[shot-name] source', JSON.stringify({
    app: { checkout: REPO_ROOT, head: git(REPO_ROOT, 'rev-parse', 'HEAD'), tree: git(REPO_ROOT, 'rev-parse', 'HEAD^{tree}') },
    agent: process.env.TIMELINE_BUNDLE_AGENT_HEAD,
    runtime: process.env.TIMELINE_BUNDLE_RUNTIME_HEAD,
  }));
});

test.describe.configure({ mode: 'serial' });

function pinOf(result: CommitAcceptedMutation): HeadPin {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

function shotPayload(document: CanonicalDocument) {
  const shot = document.shot_revisions.find((candidate) => candidate.shot_id === 'f2-shot');
  expect(shot, 'the accepted canonical document keeps the seeded shot revision').toBeTruthy();
  return shot!.payload as Record<string, any>;
}

async function rawShot(harness: DirectHarness, seed: ThreeProductsSeed, parentRevisionId: string) {
  const parent = await revisionBody(harness, parentRevisionId);
  const occurrence = (parent.payload.occurrences as Array<Record<string, any>>).find((candidate) => candidate.occurrence_id === seed.occurrenceId);
  expect(occurrence, 'the raw parent binds the requested occurrence').toBeTruthy();
  const shot = await harness.runtimeJson('GET', `/v1/projects/${seed.projectId}/shots/${seed.shotId}/revisions/${occurrence!.shot_revision_id}`);
  expect(shot.status, JSON.stringify(shot.body)).toBe(200);
  return { parent, shot: shot.body as { payload: Record<string, any> } };
}

function observeTraffic(page: Page) {
  const posts: CommitPost[] = [];
  const legacy: string[] = [];
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const pathname = new URL(request.url()).pathname;
    if (COMMITS.test(pathname)) {
      posts.push({ body: JSON.parse(request.postData() ?? '{}') as CommitRequest, rawBody: request.postData() ?? '', key: request.headers()['idempotency-key'], status: null, response: null });
    }
    if (LEGACY_SAVES.test(pathname)) legacy.push(pathname);
  });
  page.on('response', (response) => {
    if (response.request().method() !== 'POST' || !COMMITS.test(new URL(response.url()).pathname)) return;
    const key = response.request().headers()['idempotency-key'];
    const post = [...posts].reverse().find((candidate) => candidate.key === key);
    if (!post) return;
    post.status = response.status();
    void response.json().then((body) => { post.response = body; }).catch(() => {});
  });
  return { posts, legacy };
}

async function waitForPost(posts: CommitPost[], index: number) {
  await expect.poll(() => posts[index]?.status, CEILING).not.toBeNull();
  await expect.poll(() => posts[index]?.response, CEILING).not.toBeNull();
  return posts[index];
}

async function acceptAndRecord(route: Route, posts: CommitPost[]) {
  const response = await route.fetch({ maxRetries: 0 });
  const post = posts[posts.length - 1];
  post.status = response.status();
  post.response = await response.json();
  await route.fulfill({ response });
}

async function openParent(page: Page, harness: DirectHarness) {
  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await expect.poll(async () => (await commandOutboxes(page, harness.seed.timelineId)).some((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
}

async function editShotName(page: Page, seed: ThreeProductsSeed, value: string) {
  const dialog = await openEmbeddedCanonicalShot(page, seed.occurrenceId, SHOT_NAME);
  await dialog.locator('span[title="Click to edit shot name"]').first().click();
  const input = embeddedShotNameInput(dialog);
  await expect(input).toBeVisible();
  await input.fill(value);
  await input.press('Enter');
  return { dialog, input };
}

test('M2 real embedded shot name: raw preservation, undo, lost ACK restart retry, and same-name conflict draft', async ({ page, harness, seed3 }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await openParent(page, harness);
  const traffic = observeTraffic(page);
  const initialHead = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed3.timelineId}/composition-revisions?limit=1`)).body.items.find((item: any) => item.is_current_head).revision_id as string;
  const initial = await rawShot(harness, seed3, initialHead);
  expect(initial.shot.payload.name).toBe(SHOT_NAME);
  expect(initial.shot.payload.provenance).toEqual({ source: 'three-products-seed', revision: 1 });
  expect(initial.shot.payload.x_f2_opaque).toEqual(seed3.opaque.shot);

  // Capture happens on the production name click, before the Unicode draft is typed.
  const first = await editShotName(page, seed3, `  ${ACCEPTED_NAME}  `);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(1);
  await waitForPost(traffic.posts, 0);
  const accepted = traffic.posts[0];
  expect(accepted.body).toMatchObject({
    base_revision_id: initialHead,
    commands: [{ schema_version: 1, op: 'shot.set', version: '1', select: `occurrence:${seed3.occurrenceId}/shot`, args: { values: { name: ACCEPTED_NAME }, clear: [] } }],
  });
  expect(accepted.body).not.toHaveProperty('parent_composition');
  expect(accepted.body.commands[0].reads).toEqual(expect.arrayContaining([
    { ref: `occurrence:${seed3.occurrenceId}`, path: ['occurrence_id'], state: { state: 'present', value: seed3.occurrenceId } },
  ]));
  expect(accepted.body.commands[0].dependencies).toEqual(expect.arrayContaining([
    expect.objectContaining({ key: 'shot.source', policy: 'exact' }),
  ]));
  const acceptedResponse = traffic.posts[0].response as CommitAcceptedMutation;
  expect(acceptedResponse.data.status).toMatch(/^(accepted|rebased)$/);
  expect(shotPayload(acceptedResponse.data.canonical_document)).toMatchObject({
    name: ACCEPTED_NAME,
    provenance: initial.shot.payload.provenance,
    x_f2_opaque: initial.shot.payload.x_f2_opaque,
  });
  await expect(first.dialog.locator('input')).toHaveCount(0);
  await expect(first.dialog.getByText(ACCEPTED_NAME, { exact: true }).first()).toBeVisible();
  const acceptedPin = pinOf(acceptedResponse);
  const acceptedRaw = await rawShot(harness, seed3, acceptedPin.revision_id);
  expect(acceptedRaw.shot.payload).toEqual(expect.objectContaining({ name: ACCEPTED_NAME, provenance: initial.shot.payload.provenance, x_f2_opaque: initial.shot.payload.x_f2_opaque }));

  // Reload reads the accepted shot, then the parent session's real Runtime inverse restores only this name.
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await expect.poll(() => page.getByRole('button', { name: 'Undo', exact: true }).isVisible(), CEILING).toBe(true);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  await expect.poll(() => traffic.posts.length, CEILING).toBe(2);
  await waitForPost(traffic.posts, 1);
  expect(traffic.posts[1].body.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [acceptedPin.publication_id] } }]);
  const undone = traffic.posts[1].response as CommitAcceptedMutation;
  expect(shotPayload(undone.data.canonical_document)).toMatchObject({ name: SHOT_NAME, provenance: initial.shot.payload.provenance, x_f2_opaque: initial.shot.payload.x_f2_opaque });
  const undonePin = pinOf(undone);
  const undoneRaw = await rawShot(harness, seed3, undonePin.revision_id);
  expect(undoneRaw.shot.payload).toEqual(initial.shot.payload);

  // The first retry case holds the accepted Runtime response, then aborts only the browser acknowledgement.
  let releaseAck!: () => void;
  const ackGate = new Promise<void>((resolve) => { releaseAck = resolve; });
  let heldAck = false;
  const ackInterceptor = async (route: Route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    if (!heldAck) {
      heldAck = true;
      const response = await route.fetch({ maxRetries: 0 });
      const post = traffic.posts[traffic.posts.length - 1];
      post.status = response.status();
      post.response = await response.json();
      await ackGate;
      await route.abort('connectionreset').catch(() => {});
      return;
    }
    await acceptAndRecord(route, traffic.posts);
  };
  await page.route(COMMITS, ackInterceptor);
  const retry = await editShotName(page, seed3, RETRY_NAME);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(3);
  await waitForPost(traffic.posts, 2);
  const originalRetry = { body: traffic.posts[2].rawBody, key: traffic.posts[2].key };
  const acceptedRetry = traffic.posts[2].response as CommitAcceptedMutation;
  expect(shotPayload(acceptedRetry.data.canonical_document).name).toBe(RETRY_NAME);
  releaseAck();
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.pending)?.pending?.outcome?.kind, CEILING).toBe('retry');
  await expect(retry.input).toHaveValue(RETRY_NAME);
  await page.reload();
  await expectConnected(page);
  const beforeRestart = (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.pending)!;
  expect(beforeRestart.pending?.request.body).toBe(originalRetry.body);
  expect(beforeRestart.pending?.request.key).toBe(originalRetry.key);
  const restarted = await harness.restartRuntime();
  expect(restarted.oldInstanceId).not.toBe(harness.runtimeInstanceId);
  await expect(page.getByRole('heading', { name: 'Astrid restarted' })).toBeVisible(CEILING);
  await page.getByRole('button', { name: 'Reload', exact: true }).click();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const ownerId = beforeRestart.ownerId;
  await page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${ownerId}"]`)).click();
  await expect.poll(() => traffic.posts.length, CEILING).toBe(4);
  expect(traffic.posts[3].rawBody).toBe(originalRetry.body);
  expect(traffic.posts[3].key).toBe(originalRetry.key);
  expect(traffic.posts[3].response).toEqual(traffic.posts[2].response);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  await page.unroute(COMMITS, ackInterceptor);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  await expect.poll(() => traffic.posts.length, CEILING).toBe(5);
  await waitForPost(traffic.posts, 4);
  const afterRetryUndo = traffic.posts[4].response as CommitAcceptedMutation;
  expect(shotPayload(afterRetryUndo.data.canonical_document).name).toBe(SHOT_NAME);

  // Hold the actual App request before Runtime acceptance; a second writer changes this same shot-name leaf.
  let releaseConflict!: () => void;
  const conflictGate = new Promise<void>((resolve) => { releaseConflict = resolve; });
  let heldConflict = false;
  const conflictInterceptor = async (route: Route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    if (!heldConflict) {
      heldConflict = true;
      await conflictGate;
      const response = await route.fetch({ maxRetries: 0 });
      const post = traffic.posts[traffic.posts.length - 1];
      post.status = response.status();
      post.response = await response.json();
      await route.fulfill({ response });
      return;
    }
    await route.fallback();
  };
  await page.route(COMMITS, conflictInterceptor);
  const conflict = await editShotName(page, seed3, CONFLICT_DRAFT);
  await expect.poll(() => traffic.posts.length, CEILING).toBe(6);
  const held = traffic.posts[5];
  const externalCommand = structuredClone(held.body.commands[0]);
  externalCommand.args = { values: { name: 'Other writer' }, clear: [] };
  const external = await harness.runtimeJson('POST', `/v1/projects/${harness.seed.projectId}/timelines/${seed3.timelineId}/commit`, {
    ...held.body,
    commands: [externalCommand],
  });
  expect(external.status).toBe(200);
  releaseConflict();
  await waitForPost(traffic.posts, 5);
  expect(traffic.posts[5].status).toBe(409);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.pending)?.pending?.outcome?.kind, CEILING).toBe('rejected');
  await expect(conflict.input).toHaveValue(CONFLICT_DRAFT);
  expect(traffic.legacy).toEqual([]);
  await page.unroute(COMMITS, conflictInterceptor);
});
