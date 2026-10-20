/**
 * Source-only M2 journey for one eligible parent-owned native clip.split.
 *
 * The ordinary three-products seed deliberately contains a neighbouring
 * transition, which native split refuses. This case publishes a separate
 * eligible parent timeline with the same real Runtime/media authority and
 * drives the actual selected-clip keyboard path. It remains staged until the
 * production hook submits clip.split through the durable command session.
 */
import { expect, type Page, type Request } from '@playwright/test';
import { randomUUID } from 'node:crypto';
import { CONTRACT_VERSION, SCHEMA_DIGEST } from '../../../src/integrations/runtime/generated-contract-metadata.ts';
import { checkCurrent013Sources, readCurrent013Inputs } from '../../../scripts/testing/current013-integration.mjs';
import { CURRENT013_PARENT_SPLIT_AGENT } from '../../../scripts/testing/current013-parent-split.mjs';
import type {
  CanonicalDocument, CommitAcceptedMutation, EditCommand, HeadPin, HistoryPage, Manifest,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';
import splitGolden from '../../../src/tools/video-editor/commands/fixtures/recipe_m2_clip_split.json';
import {
  commandOutboxes, expectConnected, firstTrackName, openApp,
  test as appTest,
} from './support/app.ts';
import { APP_ENTRY_ROUTE } from './support/app.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON, AstridCli, astridUnavailableReason, revisionSet } from './support/astrid.ts';
import { compositionPublication, harnessUnavailableReason, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const PUBLISHERS = /\/v1\/projects\/[^/]+\/(?:timelines|shots)(?:\/|$)/;
const SPLIT_AT = 1;

type SplitFixture = { commands: EditCommand[]; output: { parent_revision: { payload: Record<string, any> } }; };
const nativeSplit = splitGolden as SplitFixture;

const test = appTest.extend<object, { seed3: ThreeProductsSeed; astrid: AstridCli }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
  astrid: [async ({ harness }, use) => { await use(await AstridCli.create(harness)); }, { scope: 'worker', timeout: 240_000 }],
});

type SplitSeed = {
  projectSlug: string;
  timelineId: string;
  clipId: string;
  neighborId: string;
  headRevisionId: string;
};

test.beforeAll(() => {
  const input = readCurrent013Inputs();
  expect(input.agentSha, 'use the literal approved Agent source').toBe(CURRENT013_PARENT_SPLIT_AGENT);
  checkCurrent013Sources(input);
  const reason = harnessUnavailableReason() ?? astridUnavailableReason();
  if (reason) throw new Error(`the current013 parent-split journey cannot run: ${reason}`);
  expect(CONTRACT_VERSION).toBe('0.2.13');
  expect(SCHEMA_DIGEST).toBe('sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4');
});

const pinOf = (result: CommitAcceptedMutation): HeadPin => ({
  revision_id: result.data.accepted_revision_id,
  publication_id: result.receipt.receipt_id,
});

function parentPayload(document: CanonicalDocument): Record<string, any> {
  return document.parent_revision.payload as Record<string, any>;
}

function parentConfig(document: CanonicalDocument): Record<string, any> {
  return parentPayload(document).config as Record<string, any>;
}

async function history(harness: DirectHarness, seed: { timelineId: string }): Promise<HistoryPage> {
  const response = await harness.runtimeJson<HistoryPage>('GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  expect(response.body.next_cursor, 'this bounded journey reads the entire history').toBeNull();
  return response.body;
}

async function canonicalAt(harness: DirectHarness, seed: { timelineId: string }, head: HeadPin): Promise<CanonicalDocument> {
  const parentResponse = await harness.runtimeJson('GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${head.revision_id}`);
  expect(parentResponse.status, JSON.stringify(parentResponse.body)).toBe(200);
  const parent = parentResponse.body;
  const manifest = parent.dependency_manifest as Manifest;
  const root = `/v1/projects/${harness.seed.projectId}`;
  const [shotRevisions, internalRevisions] = await Promise.all([
    Promise.all(manifest.shots.map(async (pin) => {
      const response = await harness.runtimeJson('GET', `${root}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
      expect(response.status, JSON.stringify(response.body)).toBe(200);
      return {
        shot_id: response.body.shot_id,
        revision_id: response.body.revision_id,
        internal_timeline_revision_id: response.body.internal_timeline_revision_id,
        content_digest: response.body.content_digest,
        payload: response.body.payload,
      };
    })),
    Promise.all(manifest.internal_timelines.map(async (pin) => {
      const response = await harness.runtimeJson('GET', `${root}/timelines/${pin.timeline_id}/revisions/${pin.revision_id}`);
      expect(response.status, JSON.stringify(response.body)).toBe(200);
      return {
        timeline_id: response.body.timeline_id,
        revision_id: response.body.revision_id,
        content_digest: response.body.content_digest,
        payload: response.body.payload,
      };
    })),
  ]);
  return {
    schema_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    parent_revision: { revision_id: parent.revision_id, content_digest: parent.content_digest, payload: parent.payload },
    shot_revisions: shotRevisions,
    internal_timeline_revisions: internalRevisions,
    dependency_manifest: manifest,
  };
}

async function expectReadback(harness: DirectHarness, document: CanonicalDocument) {
  const root = `/v1/projects/${document.project_id}`;
  const parent = await harness.runtimeJson('GET', `${root}/timelines/${document.timeline_id}/composition-revisions/${document.parent_revision.revision_id}`);
  expect(parent.status, JSON.stringify(parent.body)).toBe(200);
  expect(parent.body.payload).toEqual(document.parent_revision.payload);
  expect(parent.body.content_digest).toBe(document.parent_revision.content_digest);
  expect(parent.body.dependency_manifest).toEqual(document.dependency_manifest);
  for (const shot of document.shot_revisions) {
    const response = await harness.runtimeJson('GET', `${root}/shots/${shot.shot_id}/revisions/${shot.revision_id}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    expect(response.body.payload).toEqual(shot.payload);
    expect(response.body.content_digest).toBe(shot.content_digest);
  }
  for (const internal of document.internal_timeline_revisions) {
    const response = await harness.runtimeJson('GET', `${root}/timelines/${internal.timeline_id}/revisions/${internal.revision_id}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    expect(response.body.payload).toEqual(internal.payload);
    expect(response.body.content_digest).toBe(internal.content_digest);
  }
}

function attachTraffic(page: Page) {
  const commits: Array<{ request: Request; body: Record<string, any> }> = [];
  const legacy: string[] = [];
  const renderer: string[] = [];
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (request.method() === 'POST' && COMMITS.test(pathname)) commits.push({ request, body: request.postDataJSON() as Record<string, any> });
    else if (request.method() === 'POST' && PUBLISHERS.test(pathname)) legacy.push(`${request.method()} ${pathname}`);
    if (/render|export/i.test(pathname)) renderer.push(`${request.method()} ${pathname}`);
  });
  return { commits, legacy, renderer };
}

async function openSplitTimeline(page: Page, harness: DirectHarness, seed: SplitSeed) {
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}?localProject=${encodeURIComponent(seed.projectSlug)}&localTimeline=${encodeURIComponent(seed.timelineId)}`);
  await expectConnected(page);
  await expect(firstTrackName(page)).toBeVisible();
}

async function seedEligibleTimeline(harness: DirectHarness): Promise<SplitSeed> {
  const timelineId = randomUUID();
  const clipId = 'native-split-source';
  const neighborId = 'native-split-neighbor';
  const speed = 1.3;
  const sourceOut = 4;
  const clip = {
    id: clipId, at: 0, track: 'V1', clipType: 'media', asset: 'split-video',
    from: 0, to: sourceOut, speed, hold: sourceOut / speed,
    app: { opaque: { keep: [null, false, 0, { source: 'split' }] }, astrid: { for: sourceOut / speed } },
  };
  const neighbor = { id: neighborId, at: 5, track: 'V1', clipType: 'media', asset: 'split-video', from: 4, to: 8, speed: 1, hold: 4 };
  const clips = [clip, neighbor];
  const publication = compositionPublication({ projectId: harness.seed.projectId, timelineId }, null, 'Native split eligible', 30);
  const parent = publication.parent_composition as Record<string, any>;
  const config = parent.config as Record<string, any>;
  config.output = { resolution: '1280x720', fps: { numerator: 30000, denominator: 1001 }, file: 'out.mp4' };
  config.tracks = [{ id: 'V1', kind: 'visual', label: 'V1' }];
  config.clips = clips;
  config.opaque = { timeline: 'split', nullValue: null, nested: [false, 0] };
  parent.clips = clips;
  parent.registry = {
    assets: {
      'split-video': {
        file: `split-video.${harness.seed.video.mediaType === 'video/webm' ? 'webm' : 'mp4'}`,
        type: harness.seed.video.mediaType,
        duration: 12,
        media_id: harness.seed.video.objectId,
        content_sha256: harness.seed.video.digest,
      },
    },
  };
  const published = await harness.runtimeJson('POST', `/v1/projects/${harness.seed.projectId}/timelines/${timelineId}/composition-revisions`, publication);
  expect(published.status, JSON.stringify(published.body)).toBe(200);
  return {
    projectSlug: (await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}`)).body.data.slug,
    timelineId,
    clipId,
    neighborId,
    headRevisionId: published.body.data.new_head,
  };
}

function remapFixtureValue(value: any, clipId: string, neighborId: string, rightId: string): any {
  if (typeof value === 'string') {
    return value
      .replaceAll('parent/clip:clip-a', `parent/clip:${clipId}`)
      .replaceAll('parent/clip:clip-b', `parent/clip:${neighborId}`)
      .replaceAll('parent/clip:right', `parent/clip:${rightId}`);
  }
  if (Array.isArray(value)) return value.map((entry) => remapFixtureValue(entry, clipId, neighborId, rightId));
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, entry]) => [key, remapFixtureValue(entry, clipId, neighborId, rightId)]));
  return value;
}

function expectedNativeCommand(original: Record<string, any>, registryEntry: Record<string, any>, fps: Record<string, number>, clipId: string, neighborId: string, rightId: string): EditCommand {
  const expected = structuredClone(nativeSplit.commands[0]) as any;
  expected.select = `parent/clip:${clipId}`;
  expected.args = { on: SPLIT_AT, right_id: rightId };
  expected.resolved = [`parent/clip:${clipId}`];
  expected.reads = expected.reads.map((read: any) => remapFixtureValue(read, clipId, neighborId, rightId));
  expected.selections = expected.selections.map((selection: any) => remapFixtureValue(selection, clipId, neighborId, rightId));
  expected.bindings = { 'split.target': `parent/clip:${clipId}` };
  expected.created = [`parent/clip:${rightId}`];
  expected.reads.forEach((read: any) => {
    if (read.ref === `parent/clip:${clipId}` && read.path.length === 0) read.state.value = original;
    if (read.ref === 'parent/registry') read.state.value = registryEntry;
    if (read.ref === 'parent' && read.path.join('.') === 'config.output.fps') read.state.value = fps;
  });
  expected.expect = remapFixtureValue(expected.expect, clipId, neighborId, rightId);
  expected.expect[`parent/clip:${clipId}::hold`].value = original.hold;
  expected.expect[`parent/clip:${clipId}::to`].value = original.to;
  expected.expect[`parent/clip:${clipId}::app.astrid.for`].value = original.app.astrid.for;
  return expected as EditCommand;
}

function splitRows(original: Record<string, any>, rightId: string) {
  const sourceIn = original.from as number;
  const speed = original.speed as number;
  const sourceCut = sourceIn + SPLIT_AT * speed;
  const left = structuredClone(original);
  left.hold = SPLIT_AT;
  left.to = sourceCut;
  left.app.astrid.for = SPLIT_AT / speed;
  const right = structuredClone(original);
  right.id = rightId;
  right.at = SPLIT_AT;
  right.hold = (original.hold as number) - SPLIT_AT;
  right.from = sourceCut;
  right.app.astrid.for = right.hold / speed;
  return { left, right };
}

test('native parent split survives lost durable ACK, reload, exact retry, and guarded UI undo', async ({ page, harness, astrid, seed3 }, testInfo) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const identity = await astrid.preflight();
  // The ordinary seed remains the preserved refusal fixture: its neighbouring
  // parent clip carries a transition, so this case intentionally uses a
  // separate eligible timeline instead of changing that fixture.
  expect(seed3.transitionClipId).toBeTruthy();
  const seed = await seedEligibleTimeline(harness);
  const initialHistory = await history(harness, seed);
  expect(initialHistory.head.revision_id).toBe(seed.headRevisionId);
  const original = await canonicalAt(harness, seed, initialHistory.head);
  const originalParent = parentPayload(original);
  const originalConfig = parentConfig(original);
  const originalClip = originalParent.clips.find((clip: Record<string, any>) => clip.id === seed.clipId);
  expect(originalClip).toBeTruthy();
  expect(originalConfig.clips).toEqual(originalParent.clips);
  expect(originalConfig.output.fps).toEqual({ numerator: 30000, denominator: 1001 });
  expect(originalClip).toMatchObject({ from: 0, to: 4, speed: 1.3, app: { opaque: { keep: [null, false, 0, { source: 'split' }] } } });

  await openApp(page, harness);
  await openSplitTimeline(page, harness, seed);
  const traffic = attachTraffic(page);

  let durable!: CommitAcceptedMutation;
  let loseAck!: () => Promise<void>;
  await page.route(COMMITS, async (route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    const response = await route.fetch({ maxRetries: 0 });
    expect(response.status()).toBe(200);
    durable = await response.json() as CommitAcceptedMutation;
    loseAck = () => route.abort('connectionreset');
  });

  const clip = page.locator(`[data-clip-id="${seed.clipId}"]`).first();
  await expect(clip).toBeVisible();
  await clip.click();
  await page.keyboard.press('ArrowRight');
  const splitRequestPromise = page.waitForRequest((request) => request.method() === 'POST' && COMMITS.test(new URL(request.url()).pathname), CEILING);
  await page.keyboard.press('s');
  const splitRequest = await splitRequestPromise;
  const splitBody = splitRequest.postDataJSON() as Record<string, any>;
  expect(splitBody).toMatchObject({
    base_revision_id: initialHistory.head.revision_id,
    base_publication_id: initialHistory.head.publication_id,
    source: { via: 'app' },
  });
  expect(splitBody).not.toHaveProperty('parent_composition');
  expect(splitBody.commands).toHaveLength(1);
  const command = splitBody.commands[0] as EditCommand;
  const rightId = command.args.right_id as string;
  expect(rightId).toMatch(new RegExp(`^${seed.clipId}-\\d+$`));
  expect(command).toEqual(expectedNativeCommand(originalClip!, originalParent.registry.assets['split-video'], originalConfig.output.fps, seed.clipId, seed.neighborId, rightId));
  expect(command.args.on).toBe(SPLIT_AT);
  expect(command.reads).toContainEqual(expect.objectContaining({ ref: `parent/clip:${seed.clipId}`, path: [], state: { state: 'present', value: originalClip } }));
  expect(command.created).toEqual([`parent/clip:${rightId}`]);
  expect(command.selections?.every((selection) => selection.policy === 'guard-membership')).toBe(true);
  expect(splitRequest.headers()['idempotency-key']).toBeTruthy();

  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).find((record) => record.pending?.request), CEILING).toBeTruthy();
  const beforeLoss = (await commandOutboxes(page, seed.timelineId)).find((record) => record.pending?.request)!;
  expect(beforeLoss.pending?.request).toEqual({
    method: 'POST',
    path: `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commit`,
    body: splitRequest.postData(),
    key: splitRequest.headers()['idempotency-key'],
  });
  expect(beforeLoss.intents).toHaveLength(1);
  expect((beforeLoss.intents[0].payload as { commands: EditCommand[] }).commands).toEqual([command]);
  await expect.poll(() => !!loseAck, CEILING).toBe(true);
  await loseAck();
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).find((record) => record.ownerId === beforeLoss.ownerId)?.pending?.outcome?.kind, CEILING).toBe('retry');

  const split = durable;
  expect(split.data.status).toMatch(/^(accepted|rebased)$/);
  const splitDocument = split.data.canonical_document;
  const { left, right } = splitRows(originalClip!, rightId);
  const expectedSplitParent = structuredClone(originalParent);
  expectedSplitParent.clips = [left, right, ...originalParent.clips.slice(1)];
  (expectedSplitParent.config as Record<string, any>).clips = structuredClone(expectedSplitParent.clips);
  expect(parentPayload(splitDocument)).toEqual(expectedSplitParent);
  expect(splitDocument.shot_revisions).toEqual(original.shot_revisions);
  expect(splitDocument.internal_timeline_revisions).toEqual(original.internal_timeline_revisions);
  expect(splitDocument.dependency_manifest).toEqual(original.dependency_manifest);
  await expectReadback(harness, splitDocument);
  const splitHistory = await history(harness, seed);
  expect(splitHistory.head).toEqual(pinOf(split));
  expect(splitHistory.items).toHaveLength(initialHistory.items.length + 1);

  await page.unroute(COMMITS);
  await page.reload();
  await openSplitTimeline(page, harness, seed);
  const oldRuntimeInstance = harness.runtimeInstanceId;
  const restarted = await harness.restartRuntime();
  expect(restarted.oldInstanceId).toBe(oldRuntimeInstance);
  expect(harness.runtimeInstanceId).not.toBe(oldRuntimeInstance);
  await expectConnected(page);
  await openSplitTimeline(page, harness, seed);
  const reloaded = (await commandOutboxes(page, seed.timelineId)).find((record) => record.ownerId === beforeLoss.ownerId)!;
  expect(reloaded.pending?.request).toEqual(beforeLoss.pending?.request);
  expect(reloaded.intents).toEqual(beforeLoss.intents);
  expect(await history(harness, seed)).toEqual(splitHistory);
  const leftClip = page.locator(`[data-clip-id="${seed.clipId}"]`).first();
  const rightClip = page.locator(`[data-clip-id="${rightId}"]`).first();
  await expect(leftClip).toBeVisible();
  await expect(rightClip).toBeVisible();
  const transition = page.locator(`[data-clip-id="${seed.neighborId}"]`).first();
  const leftBox = await leftClip.boundingBox();
  const rightBox = await rightClip.boundingBox();
  const neighborBox = await transition.boundingBox();
  expect(leftBox && rightBox && neighborBox).toBeTruthy();
  const pixelsPerSecond = (neighborBox!.x - leftBox!.x) / 5;
  expect(rightBox!.x).toBeCloseTo(leftBox!.x + pixelsPerSecond, 1);
  expect(rightBox!.width).toBeCloseTo((right.hold as number) * pixelsPerSecond, 1);
  expect(rightBox!.x + rightBox!.width).toBeCloseTo(leftBox!.x + (SPLIT_AT + (right.hold as number)) * pixelsPerSecond, 1);

  const retrying = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${beforeLoss.ownerId}"]`)).click();
  const retryResponse = await retrying;
  expect(retryResponse.status(), await retryResponse.text()).toBe(200);
  expect(retryResponse.request().postData()).toBe(splitRequest.postData());
  expect(retryResponse.request().headers()['idempotency-key']).toBe(splitRequest.headers()['idempotency-key']);
  expect(await retryResponse.json()).toEqual(split);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).every((record) => !record.pending && !record.intents.length), CEILING).toBe(true);
  expect(await history(harness, seed)).toEqual(splitHistory);
  expect(await page.locator(`[data-clip-id="${rightId}"]`).count()).toBe(1);

  const independent = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, pinOf(split), { kind: 'track', id: 'split-independent' }, 'split-independent');
  const independentDocument = independent.data.canonical_document;
  expect(parentPayload(independentDocument).clips).toEqual(parentPayload(splitDocument).clips);
  expect(parentConfig(independentDocument).tracks).toEqual(expect.arrayContaining([expect.objectContaining({ id: 'split-independent' })]));
  expect(parentPayload(independentDocument).opaque).toEqual(originalParent.opaque);
  await expectReadback(harness, independentDocument);

  await page.reload();
  await openSplitTimeline(page, harness, seed);
  await expect(page.locator(`[data-clip-id="${rightId}"]`)).toHaveCount(1);
  const undoResponsePromise = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  const undoResponse = await undoResponsePromise;
  expect(undoResponse.status(), await undoResponse.text()).toBe(200);
  const undone = await undoResponse.json() as CommitAcceptedMutation;
  expect(undoResponse.request().postDataJSON()).toMatchObject({
    base_revision_id: independent.data.accepted_revision_id,
    base_publication_id: independent.receipt.receipt_id,
    commands: [{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [split.receipt.receipt_id] } }],
  });
  const undoneDocument = undone.data.canonical_document;
  const expectedUndoParent = structuredClone(originalParent);
  (expectedUndoParent.config as Record<string, any>).tracks = parentConfig(independentDocument).tracks;
  expect(parentPayload(undoneDocument)).toEqual(expectedUndoParent);
  expect(undoneDocument.shot_revisions).toEqual(independentDocument.shot_revisions);
  expect(undoneDocument.internal_timeline_revisions).toEqual(independentDocument.internal_timeline_revisions);
  expect(undoneDocument.dependency_manifest).toEqual(independentDocument.dependency_manifest);
  await expectReadback(harness, undoneDocument);
  await expect(page.locator(`[data-clip-id="${rightId}"]`)).toHaveCount(0);
  await expect(page.locator(`[data-clip-id="${seed.clipId}"]`)).toBeVisible();
  expect((await history(harness, seed)).items).toHaveLength(initialHistory.items.length + 3);
  expect(traffic.legacy, 'native split, retry, and undo never publish a legacy snapshot').toEqual([]);
  expect(traffic.renderer, 'native acceptance never starts the renderer').toEqual([]);
  expect(traffic.commits.map((post) => post.body.commands[0].op)).toEqual(['clip.split', 'clip.split', 'timeline.inverse']);
  expect(traffic.commits[0].body.commands[0].args.right_id).toBe(rightId);
  expect(traffic.commits[1].body).toEqual(traffic.commits[0].body);
  expect(traffic.commits[1].request.headers()['idempotency-key']).toBe(traffic.commits[0].request.headers()['idempotency-key']);
  expect(new Set(traffic.commits.map((post) => post.request.headers()['idempotency-key'])).size).toBe(2);
  expect(parentPayload(undoneDocument).clips.filter((clip: Record<string, any>) => clip.id === rightId)).toHaveLength(0);
  expect(parentPayload(undoneDocument).clips.filter((clip: Record<string, any>) => clip.id === seed.clipId)).toHaveLength(1);

  // A direct-neighbor write must produce a real Runtime 409 and retain the captured draft.
  let releaseConflict!: () => void;
  let conflictBody: Record<string, any> | undefined;
  const conflictRequest = new Promise<void>((resolve) => { releaseConflict = resolve; });
  await page.route(COMMITS, async (route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    conflictBody = route.request().postDataJSON() as Record<string, any>;
    await conflictRequest;
    await route.continue();
  });
  await page.locator(`[data-clip-id="${seed.clipId}"]`).first().click();
  await page.keyboard.press('ArrowRight');
  const conflictResponsePromise = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.keyboard.press('s');
  await expect.poll(() => !!conflictBody, CEILING).toBe(true);
  const neighborEdit = await astrid.commitCaptured(harness.seed.projectId, seed.timelineId, pinOf(undone),
    { kind: 'move', clipId: seed.neighborId, on: 6 }, 'split-neighbor-conflict');
  expect(parentPayload(neighborEdit.data.canonical_document).clips).toEqual(expect.arrayContaining([
    expect.objectContaining({ id: seed.neighborId, at: 6 }),
  ]));
  releaseConflict();
  const conflictResponse = await conflictResponsePromise;
  expect(conflictResponse.status(), await conflictResponse.text()).toBe(409);
  let conflictOutbox: any;
  await expect.poll(async () => {
    conflictOutbox = (await commandOutboxes(page, seed.timelineId))
      .find((record) => record.pending?.outcome?.kind === 'rejected');
    return conflictOutbox?.pending?.outcome?.kind;
  }, CEILING).toBe('rejected');
  expect(conflictOutbox.intents).toHaveLength(1);
  expect(conflictOutbox.intents[0].payload).toEqual(expect.objectContaining({ commands: [conflictBody!.commands[0]] }));
  expect(conflictOutbox.pending?.request.body).toBe(conflictResponse.request().postData());
  expect((await history(harness, seed)).head).toEqual(pinOf(neighborEdit));
  await page.unroute(COMMITS);
  await page.reload();
  await openSplitTimeline(page, harness, seed);
  const retained = (await commandOutboxes(page, seed.timelineId)).find((record) => record.ownerId === conflictOutbox.ownerId)!;
  expect(retained.intents).toEqual(conflictOutbox.intents);
  expect(retained.pending).toEqual(conflictOutbox.pending);
  expect(traffic.legacy).toEqual([]);

  await testInfo.attach('clip-split-readback', {
    contentType: 'application/json',
    body: Buffer.from(JSON.stringify({
      renderer: 'not started',
      sources: revisionSet(identity),
      approvedInputs: readCurrent013Inputs(),
      nativeFixture: 'recipe_m2_clip_split.json',
      original,
      split: splitDocument,
      independent: independentDocument,
      undone: undoneDocument,
      requests: traffic.commits.map((post) => ({ body: post.body, idempotencyKey: post.request.headers()['idempotency-key'] })),
      legacyPublishers: traffic.legacy,
    }, null, 2)),
  });
});
