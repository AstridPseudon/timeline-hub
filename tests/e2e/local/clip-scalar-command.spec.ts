/**
 * ordinaryBundle2 source journey; execution awaits the manager's composed release qualification.
 * The original three-products journey and its scene are preserved. The seeded child has hold=3
 * but clipType=media, whose descriptor exposes source bounds, not the Duration control. Cover the
 * supported parent transition clear here; do not relabel the child as a presentation-only hold.
 */
import { expect, type Page, type Request } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { CONTRACT_VERSION, SCHEMA_DIGEST } from '../../../src/integrations/runtime/generated-contract-metadata.ts';
import type {
  CanonicalDocument, CommitAcceptedMutation, EditCommand, HeadPin, HistoryPage,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';
import scalarGolden from '../../../src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_scalar_fields.json';
import {
  commandOutboxes, dragTimelineClip, expectConnected, openApp, openSeededTimeline,
  revisionBody, test as appTest,
} from './support/app.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON, AstridCli, astridUnavailableReason, revisionSet } from './support/astrid.ts';
import {
  harnessUnavailableReason, PRODUCT_ACTOR, REPO_ROOT, RUNTIME_CHECKOUT, THREE_PRODUCTS_REFERENCE_AT,
  type DirectHarness, type ThreeProductsSeed,
} from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const PUBLISHERS = /\/v1\/projects\/[^/]+\/(?:timelines|shots)(?:\/|$)/;
const SCHEMA = 'sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6';

const test = appTest.extend<object, { seed3: ThreeProductsSeed; astrid: AstridCli }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
  astrid: [async ({ harness }, use) => { await use(await AstridCli.create(harness)); }, { scope: 'worker', timeout: 240_000 }],
});

function sources() {
  return [
    ['app', REPO_ROOT, undefined],
    ['agent', ASTRID_CHECKOUT, process.env.TIMELINE_BUNDLE_AGENT_HEAD],
    ['runtime', RUNTIME_CHECKOUT, process.env.TIMELINE_BUNDLE_RUNTIME_HEAD],
  ].map(([name, checkout, expected]) => {
    const git = (...args: string[]) => execFileSync('git', ['-C', checkout!, ...args], { encoding: 'utf8' }).trim();
    const head = git('rev-parse', 'HEAD');
    const tree = git('rev-parse', 'HEAD^{tree}');
    const status = git('status', '--porcelain', '--untracked-files=normal');
    if (name !== 'app') {
      expect(expected, `${name} requires an explicit frozen source head`).toBeTruthy();
      expect(head, `${name} must remain the frozen ordinaryBundle2 source`).toBe(expected);
      expect(status, `${name} source lease must stay clean`).toBe('');
    }
    return { name, checkout, head, tree, status };
  });
}

test.beforeAll(() => {
  const reason = harnessUnavailableReason() ?? astridUnavailableReason();
  if (reason) throw new Error(`the ordinary scalar journey cannot run: ${reason}`);
  expect(CONTRACT_VERSION).toBe('0.2.3');
  expect(SCHEMA_DIGEST).toBe(SCHEMA);
  console.log('[clip-scalar] sources', JSON.stringify(sources()));
});

const pinOf = (result: CommitAcceptedMutation): HeadPin => ({
  revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id,
});
const transitionSelect = (page: Page) => page.getByText('Transition', { exact: true })
  .locator('xpath=following::*[@role="combobox"][1]');

async function inspectTransition(page: Page, clipId: string) {
  await page.locator(`.clip-action[data-clip-id="${clipId}"]`).first().click();
  await page.getByRole('tab', { name: 'Effects', exact: true }).click();
  await expect(transitionSelect(page)).toBeVisible();
}

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const response = await harness.runtimeJson<HistoryPage>('GET',
    `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/commits?limit=50`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  expect(response.body.next_cursor, 'this bounded journey reads the entire history').toBeNull();
  return response.body;
}

async function expectReadback(harness: DirectHarness, seed: ThreeProductsSeed, result: CommitAcceptedMutation) {
  const document = result.data.canonical_document;
  expect(document.project_id).toBe(harness.seed.projectId);
  expect(document.timeline_id).toBe(seed.timelineId);
  expect(document.parent_revision.revision_id).toBe(result.data.accepted_revision_id);
  const root = `/v1/projects/${document.project_id}`;
  const parent = await harness.runtimeJson('GET',
    `${root}/timelines/${document.timeline_id}/composition-revisions/${document.parent_revision.revision_id}`);
  expect(parent.status, JSON.stringify(parent.body)).toBe(200);
  expect(parent.body).toMatchObject({ ...document.parent_revision, dependency_manifest: document.dependency_manifest });
  expect(parent.body.payload).toEqual(document.parent_revision.payload);
  expect(parent.body.dependency_manifest).toEqual(document.dependency_manifest);
  for (const shot of document.shot_revisions) {
    const row = await harness.runtimeJson('GET', `${root}/shots/${shot.shot_id}/revisions/${shot.revision_id}`);
    expect(row.status, JSON.stringify(row.body)).toBe(200);
    expect(row.body).toMatchObject(shot);
    expect(row.body.payload).toEqual(shot.payload);
  }
  for (const internal of document.internal_timeline_revisions) {
    const row = await harness.runtimeJson('GET', `${root}/timelines/${internal.timeline_id}/revisions/${internal.revision_id}`);
    expect(row.status, JSON.stringify(row.body)).toBe(200);
    expect(row.body).toMatchObject(internal);
    expect(row.body.payload).toEqual(internal.payload);
  }
  const entry = (await history(harness, seed)).items.find((item) => item.publication_id === result.receipt.receipt_id);
  expect(entry?.receipt).toEqual(result.receipt);
  expect(entry?.revision_id).toBe(document.parent_revision.revision_id);
}

function expectChildrenUnchanged(document: CanonicalDocument, before: CanonicalDocument) {
  expect(document.shot_revisions).toEqual(before.shot_revisions);
  expect(document.internal_timeline_revisions).toEqual(before.internal_timeline_revisions);
  expect(document.dependency_manifest).toEqual(before.dependency_manifest);
  expect(document.parent_revision.payload.occurrences).toEqual(before.parent_revision.payload.occurrences);
  expect(document.parent_revision.payload.registry).toEqual(before.parent_revision.payload.registry);
}

function accepted(status: number, result: CommitAcceptedMutation) {
  expect(status, JSON.stringify(result)).toBe(200);
  expect(result.data.status).toMatch(/^(accepted|rebased)$/);
  expect(result.receipt.receipt_id).toBeTruthy();
  expect(result.receipt.result).toEqual(result.data);
  return result;
}

test('ordinary parent transition None survives lost durable ACK, reload, exact retry and guarded UI undo', async ({ page, harness, astrid, seed3 }, testInfo) => {
  const beforeSources = sources();
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const identity = await astrid.preflight();
  expect(identity.schema_digest).toBe(SCHEMA);
  const requests: Request[] = [];
  const legacy: string[] = [];
  page.on('request', (request) => {
    if (!['POST', 'PUT', 'PATCH', 'DELETE'].includes(request.method())) return;
    const pathname = new URL(request.url()).pathname;
    if (COMMITS.test(pathname)) requests.push(request);
    else if (PUBLISHERS.test(pathname)) legacy.push(`${request.method()} ${pathname}`);
  });
  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const fromPage = await page.evaluate(async (base) => {
    const [health, realm] = await Promise.all([fetch(`${base}/v1/health`), fetch(`${base}/v1/realm`)]);
    return { health: await health.json(), realm: await realm.json() };
  }, harness.doorBase);
  expect(fromPage.health).toMatchObject({ runtime_instance_id: identity.runtime_instance_id, schema_digest: SCHEMA });
  expect(fromPage.realm.realm_id).toBe(identity.realm_id);
  const initialHistory = await history(harness, seed3);
  expect(initialHistory.head.revision_id).toBe(seed3.headRevisionId);
  const initial = await revisionBody(harness, initialHistory.head.revision_id);

  // Activate the ordinary command session with the existing real pointer gesture.
  const moving = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await dragTimelineClip(page, seed3.appClipId, seed3.transitionClipId, 0, 5, THREE_PRODUCTS_REFERENCE_AT);
  const moveResponse = await moving;
  const move = accepted(moveResponse.status(), await moveResponse.json() as CommitAcceptedMutation);
  expect(requests).toHaveLength(1);
  expect(requests[0].postDataJSON()).toMatchObject({
    base_revision_id: initialHistory.head.revision_id, base_publication_id: initialHistory.head.publication_id,
    commands: [{ op: 'clip.move', select: `parent/clip:${seed3.appClipId}`, args: { on: 5 } }],
  });
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId))
    .every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  const moveOwner = (await commandOutboxes(page, seed3.timelineId))
    .find((owner) => owner.accepted?.head.revisionId === pinOf(move).revision_id)!;
  expect(moveOwner.accepted?.intentId).toBeTruthy();
  const moved = move.data.canonical_document;
  expect(moved.parent_revision.payload.registry).toEqual(initial.payload.registry);
  expect(moved.parent_revision.payload.occurrences).toEqual(initial.payload.occurrences);
  expect(moved.dependency_manifest).toEqual(initial.dependency_manifest);
  expect((moved.parent_revision.payload.config as Record<string, any>).x_f2_opaque).toEqual(seed3.opaque.config);
  const child = moved.internal_timeline_revisions.flatMap((row) => row.payload.clips as Array<Record<string, any>>)
    .find((clip) => clip.id === seed3.agentClipId)!;
  expect(child).toMatchObject({ clipType: 'media', hold: 3, app: { f2Opaque: seed3.opaque.clip } });
  await expectReadback(harness, seed3, move);

  // The checked-in native golden defines the WHOLE guard footprint. Only immutable media identities
  // vary with the real seeded video; this expected command is never used to supply capture or state.
  const expectedCommand = structuredClone(scalarGolden.commands[2]) as EditCommand;
  const video = (moved.parent_revision.payload.registry as Record<string, any>).assets['f2-video'];
  expect(video.media_id).toBe(harness.seed.video.objectId);
  expect(video.content_sha256).toBe(harness.seed.video.digest);
  for (const read of expectedCommand.reads!) {
    const field = read.path[read.path.length - 1];
    if (read.ref === 'parent/registry' && ['media_id', 'content_sha256'].includes(field)) {
      read.state = { state: 'present', value: video[field] };
    }
  }
  const movedHistory = await history(harness, seed3);
  expect(movedHistory.head).toEqual(pinOf(move));
  expect(movedHistory.items).toHaveLength(initialHistory.items.length + 1);

  let cleared!: CommitAcceptedMutation;
  let loseAck: (() => Promise<void>) | undefined;
  await page.route(COMMITS, async (route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    const response = await route.fetch({ maxRetries: 0 });
    cleared = accepted(response.status(), await response.json() as CommitAcceptedMutation);
    loseAck = () => route.abort('connectionreset');
  });
  await inspectTransition(page, seed3.transitionClipId);
  await expect(transitionSelect(page)).toContainText('crossfade');
  await transitionSelect(page).click();
  await page.getByRole('option', { name: 'None', exact: true }).click();
  await expect.poll(() => !!loseAck, CEILING).toBe(true);
  expect(requests).toHaveLength(2);
  const scalarRequest = requests[1];
  const scalarBody = scalarRequest.postDataJSON();
  expect(scalarBody).toMatchObject({
    base_revision_id: pinOf(move).revision_id, base_publication_id: pinOf(move).publication_id,
    source: { via: 'app' },
  });
  expect(scalarBody).not.toHaveProperty('parent_composition');
  expect(scalarBody.commands).toEqual([expectedCommand]);
  expect(cleared.data.commands).toEqual([expectedCommand]);
  expect(scalarRequest.headers()['idempotency-key']).toBeTruthy();
  expect(scalarRequest.headers()['idempotency-key']).not.toBe(requests[0].headers()['idempotency-key']);
  const expectedParent = structuredClone(moved.parent_revision.payload) as Record<string, any>;
  for (const clips of [expectedParent.clips, expectedParent.config.clips] as Array<Array<Record<string, any>>>) {
    delete clips.find((clip) => clip.id === seed3.transitionClipId)!.transition;
  }
  expect(cleared.data.canonical_document.parent_revision.payload).toEqual(expectedParent);
  expectChildrenUnchanged(cleared.data.canonical_document, moved);
  await expectReadback(harness, seed3, cleared);
  const pending = (await commandOutboxes(page, seed3.timelineId))
    .find((owner) => owner.pending?.request.key === scalarRequest.headers()['idempotency-key'])!;
  expect(pending.ownerId).toBe(moveOwner.ownerId);
  expect(pending.scope).toEqual({ realmId: harness.realmId, actorId: PRODUCT_ACTOR,
    projectId: harness.seed.projectId, timelineId: seed3.timelineId });
  expect(pending.pending?.request).toEqual({ method: 'POST',
    path: `/v1/projects/${harness.seed.projectId}/timelines/${seed3.timelineId}/commit`,
    body: scalarRequest.postData(), key: scalarRequest.headers()['idempotency-key'] });
  expect(pending.intents).toHaveLength(1);
  expect(pending.pending!.intentId).toBe(pending.intents[0].id);
  expect((pending.intents[0].payload as { commands: EditCommand[] }).commands).toEqual([expectedCommand]);
  expect(pending.intents[0].id).not.toBe(moveOwner.accepted!.intentId);
  await loseAck!();
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId))
    .find((owner) => owner.ownerId === pending.ownerId)?.pending?.outcome?.kind, CEILING).toBe('retry');
  const clearedHistory = await history(harness, seed3);
  expect(clearedHistory.head).toEqual(pinOf(cleared));
  expect(clearedHistory.items).toHaveLength(movedHistory.items.length + 1);
  await page.unroute(COMMITS);
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const reloaded = (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.ownerId === pending.ownerId)!;
  expect(reloaded.pending?.request).toEqual(pending.pending!.request);
  expect(reloaded.intents).toEqual(pending.intents);
  expect(requests).toHaveLength(2);
  expect(await history(harness, seed3)).toEqual(clearedHistory);
  const retrying = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: /^Recover saved edits/ })
    .and(page.locator(`[data-owner-id="${pending.ownerId}"]`)).click();
  const retry = await retrying;
  expect(retry.status(), await retry.text()).toBe(200);
  expect(retry.request().postData()).toBe(scalarRequest.postData());
  expect(retry.request().headers()['idempotency-key']).toBe(scalarRequest.headers()['idempotency-key']);
  expect(await retry.json()).toEqual(cleared);
  expect(await history(harness, seed3)).toEqual(clearedHistory);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId))
    .every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  await inspectTransition(page, seed3.transitionClipId);
  await expect(transitionSelect(page)).toContainText('None');

  const independent = await astrid.commitCaptured(harness.seed.projectId, seed3.timelineId, pinOf(cleared),
    { kind: 'track', id: 'scalar-independent' }, 'scalar-independent');
  expectChildrenUnchanged(independent.data.canonical_document, moved);
  await expectReadback(harness, seed3, independent);
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await inspectTransition(page, seed3.transitionClipId);
  await expect(transitionSelect(page)).toContainText('None');
  const undoing = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  const undoResponse = await undoing;
  const undone = accepted(undoResponse.status(), await undoResponse.json() as CommitAcceptedMutation);
  expect(undoResponse.request().postDataJSON()).toMatchObject({
    base_revision_id: pinOf(independent).revision_id, base_publication_id: pinOf(independent).publication_id,
  });
  expect(undoResponse.request().postDataJSON().commands).toEqual([{
    schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
    args: { publications: [pinOf(cleared).publication_id] },
  }]);
  expect(undone.data.previous_revision_id).toBe(pinOf(independent).revision_id);
  expect(undone.data.previous_publication_id).toBe(pinOf(independent).publication_id);
  const restoredParent = structuredClone(independent.data.canonical_document.parent_revision.payload) as Record<string, any>;
  const transition = (moved.parent_revision.payload.clips as Array<Record<string, any>>)
    .find((clip) => clip.id === seed3.transitionClipId)!.transition;
  for (const clips of [restoredParent.clips, restoredParent.config.clips] as Array<Array<Record<string, any>>>) {
    clips.find((clip) => clip.id === seed3.transitionClipId)!.transition = structuredClone(transition);
  }
  expect(undone.data.canonical_document.parent_revision.payload).toEqual(restoredParent);
  expect(restoredParent.config.tracks).toContainEqual({ id: 'scalar-independent', kind: 'audio', label: 'scalar-independent' });
  expect(restoredParent.clips.find((clip: Record<string, any>) => clip.id === seed3.appClipId).at).toBe(5);
  expectChildrenUnchanged(undone.data.canonical_document, moved);
  await expectReadback(harness, seed3, undone);
  const finalHistory = await history(harness, seed3);
  expect(finalHistory.head).toEqual(pinOf(undone));
  expect(finalHistory.items).toHaveLength(initialHistory.items.length + 4);
  expect(finalHistory.items.find((entry) => entry.publication_id === pinOf(undone).publication_id)?.records?.undo_of)
    .toEqual([pinOf(cleared).publication_id]);
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await inspectTransition(page, seed3.transitionClipId);
  await expect(transitionSelect(page)).toContainText('crossfade');
  expect(requests.map((request) => request.postDataJSON().commands[0].op))
    .toEqual(['clip.move', 'clip.set', 'clip.set', 'timeline.inverse']);
  const keys = requests.map((request) => request.headers()['idempotency-key']);
  expect(new Set([keys[0], keys[1], keys[3]]).size).toBe(3);
  expect(keys[2]).toBe(keys[1]);
  expect(requests.every((request) => request.url().startsWith(`${harness.doorBase}/v1/`))).toBe(true);
  expect(legacy, 'ordinary edits and undo never publish a legacy snapshot').toEqual([]);
  const afterSources = sources();
  expect(afterSources).toEqual(beforeSources);
  await testInfo.attach('clip-scalar-readback', { contentType: 'application/json', body: Buffer.from(JSON.stringify({
    beforeSources, afterSources, identity: revisionSet(identity), fromPage, initial,
    requests: requests.map((request) => ({ body: request.postData(), key: request.headers()['idempotency-key'] })),
    moved: move, cleared, independent, undone, pending, reloaded, finalHistory, legacy, renderer: 'not started',
    holdCoverage: 'UNSUPPORTED UI: seed child clipType=media has no Duration control; raw hold=3 preserved',
  }, null, 2)) });
});
