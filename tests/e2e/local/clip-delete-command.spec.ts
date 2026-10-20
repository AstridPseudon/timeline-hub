/**
 * M2 real parent-owned clip.delete qualification.
 *
 * This is intentionally not group deletion. The seeded App clip is a direct
 * parent clip; the selected UI row emits the native command, persists its
 * exact request in IndexedDB, and the real Runtime accepts it. The Runtime
 * stays renderer-independent throughout.
 */
import { expect, type Page, type Request } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { CONTRACT_VERSION } from '../../../src/integrations/runtime/generated-contract-metadata.ts';
import {
  harnessUnavailableReason,
  RUNTIME_CHECKOUT,
  type ThreeProductsSeed,
  type DirectHarness,
} from './support/harness.ts';
import {
  commandOutboxes,
  expectConnected,
  openApp,
  openSeededTimeline,
  revisionBody,
  test as appTest,
} from './support/app.ts';
import {
  ASTRID_CHECKOUT,
  ASTRID_PYTHON,
  AstridCli,
  astridUnavailableReason,
  revisionSet,
} from './support/astrid.ts';
import type { CanonicalDocument, CommitAcceptedMutation, HeadPin, HistoryPage, Manifest } from '../../../src/integrations/runtime/timeline-commit-types.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const SNAPSHOT_WRITES = /\/(?:v1\/projects\/[^/]+\/timelines\/[^/]+|timelines\/[^/]+)\/composition-revisions(?:\/[^/]+)?$/;
const COMMIT_ROUTE = /\/api\/runtime\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const FROZEN_AGENT_HEAD = '027bd16d96010544331c953c0e1014e161786e71';
const FROZEN_RUNTIME_HEAD = '4c145dc62192f0e942e3ee3922a11488aefe9b41';

type CommitPost = { request: Request; body: Record<string, any> };

const test = appTest.extend<object, { seed3: ThreeProductsSeed; astrid: AstridCli }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
  astrid: [async ({ harness }, use) => { await use(await AstridCli.create(harness)); }, { scope: 'worker', timeout: 240_000 }],
});

test.describe.configure({ mode: 'serial' });

function sourceHead(checkout: string): { head: string; tree: string; status: string } {
  const git = (...args: string[]) => execFileSync('git', ['-C', checkout, ...args], { encoding: 'utf8' }).trim();
  return { head: git('rev-parse', 'HEAD'), tree: git('rev-parse', 'HEAD^{tree}'), status: git('status', '--porcelain', '--untracked-files=normal') };
}

function sourceContractVersion(checkout: string, head: string): string {
  const git = (...args: string[]) => execFileSync('git', ['-C', checkout, ...args], { encoding: 'utf8' }).trim();
  const path = checkout === ASTRID_CHECKOUT
    ? 'astrid_runtime_client/contract_metadata.py'
    : 'packages/python/astrid_runtime_client/contract_metadata.py';
  const source = git('show', `${head}:${path}`);
  return source.match(/CONTRACT_VERSION\s*=\s*['"]([^'"]+)['"]/)?.[1] ?? '';
}

test.beforeAll(() => {
  const reason = harnessUnavailableReason() ?? astridUnavailableReason();
  if (reason) throw new Error(`the M2 parent-delete qualification cannot run: ${reason}`);

  const expected = [
    ['agent', ASTRID_CHECKOUT, process.env.TIMELINE_BUNDLE_AGENT_HEAD],
    ['runtime', RUNTIME_CHECKOUT, process.env.TIMELINE_BUNDLE_RUNTIME_HEAD],
  ] as const;
  expect(CONTRACT_VERSION, 'App must use the frozen Bundle2 client contract').toBe('0.2.3');
  for (const [name, checkout, expectedHead] of expected) {
    expect(expectedHead, `${name} expected head must be supplied by the qualification config`).toBeTruthy();
    expect(checkout, `${name} checkout must be supplied by the qualification config`).toBeTruthy();
    const actual = sourceHead(checkout);
    expect(actual.head, `${name} checkout is not the approved source`).toBe(expectedHead);
    expect(actual.status, `${name} approved source must be clean`).toBe('');
    expect(sourceContractVersion(checkout, expectedHead), `${name} must use client contract 0.2.3`).toBe('0.2.3');
    console.log('[clip-delete] source', JSON.stringify({ name, checkout, ...actual }));
  }
  expect(process.env.TIMELINE_BUNDLE_AGENT_HEAD).toBe(FROZEN_AGENT_HEAD);
  expect(process.env.TIMELINE_BUNDLE_RUNTIME_HEAD).toBe(FROZEN_RUNTIME_HEAD);
});

function timelineBase(harness: DirectHarness, seed: ThreeProductsSeed): string {
  return `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}`;
}

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const response = await harness.runtimeJson<HistoryPage>('GET', `${timelineBase(harness, seed)}/commits?limit=50`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  return response.body;
}

/** Build the complete immutable closure that a commit returns, starting at a Runtime head. */
async function canonicalAt(harness: DirectHarness, seed: ThreeProductsSeed, head: HeadPin): Promise<CanonicalDocument> {
  const parent = await revisionBody(harness, head.revision_id);
  const manifest = parent.dependency_manifest as Manifest;
  const root = `/v1/projects/${harness.seed.projectId}`;
  const shotRevisions = await Promise.all(manifest.shots.map(async (pin) => {
    const response = await harness.runtimeJson('GET', `${root}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    return {
      shot_id: response.body.shot_id,
      revision_id: response.body.revision_id,
      internal_timeline_revision_id: response.body.internal_timeline_revision_id,
      content_digest: response.body.content_digest,
      payload: response.body.payload,
    };
  }));
  const internalRevisions = await Promise.all(manifest.internal_timelines.map(async (pin) => {
    const response = await harness.runtimeJson('GET', `${root}/timelines/${pin.timeline_id}/revisions/${pin.revision_id}`);
    expect(response.status, JSON.stringify(response.body)).toBe(200);
    return {
      timeline_id: response.body.timeline_id,
      revision_id: response.body.revision_id,
      content_digest: response.body.content_digest,
      payload: response.body.payload,
    };
  }));
  return {
    schema_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    parent_revision: {
      revision_id: parent.revision_id,
      content_digest: parent.content_digest,
      payload: parent.payload,
    },
    shot_revisions: shotRevisions,
    internal_timeline_revisions: internalRevisions,
    dependency_manifest: manifest,
  };
}

async function expectReadback(harness: DirectHarness, document: CanonicalDocument): Promise<void> {
  const root = `/v1/projects/${document.project_id}`;
  const parent = await harness.runtimeJson('GET', `${root}/timelines/${document.timeline_id}/composition-revisions/${document.parent_revision.revision_id}`);
  expect(parent.status, JSON.stringify(parent.body)).toBe(200);
  expect(parent.body.payload).toEqual(document.parent_revision.payload);
  expect(parent.body.content_digest).toBe(document.parent_revision.content_digest);
  expect(parent.body.dependency_manifest).toEqual(document.dependency_manifest);
  for (const shot of document.shot_revisions) {
    const row = await harness.runtimeJson('GET', `${root}/shots/${shot.shot_id}/revisions/${shot.revision_id}`);
    expect(row.status, JSON.stringify(row.body)).toBe(200);
    expect(row.body.payload).toEqual(shot.payload);
    expect(row.body.content_digest).toBe(shot.content_digest);
    expect(row.body.internal_timeline_revision_id).toBe(shot.internal_timeline_revision_id);
  }
  for (const internal of document.internal_timeline_revisions) {
    const row = await harness.runtimeJson('GET', `${root}/timelines/${internal.timeline_id}/revisions/${internal.revision_id}`);
    expect(row.status, JSON.stringify(row.body)).toBe(200);
    expect(row.body.payload).toEqual(internal.payload);
    expect(row.body.content_digest).toBe(internal.content_digest);
  }
}

function attachTraffic(page: Page) {
  const commits: CommitPost[] = [];
  const snapshotWrites: string[] = [];
  const renderer: string[] = [];
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (request.method() === 'POST' && COMMITS.test(pathname)) {
      commits.push({ request, body: request.postDataJSON() as Record<string, any> });
    }
    if (request.method() === 'POST' && SNAPSHOT_WRITES.test(pathname)) snapshotWrites.push(pathname);
    if (/render|export/i.test(pathname)) renderer.push(`${request.method()} ${pathname}`);
  });
  return { commits, snapshotWrites, renderer };
}

function parentConfig(document: CanonicalDocument): Record<string, any> {
  return document.parent_revision.payload.config as Record<string, any>;
}

function parentPayload(document: CanonicalDocument): Record<string, any> {
  return document.parent_revision.payload as Record<string, any>;
}

function internalClip(document: CanonicalDocument, clipId: string): Record<string, any> | undefined {
  return document.internal_timeline_revisions
    .flatMap((revision) => (revision.payload.clips as Array<Record<string, any>> | undefined) ?? [])
    .find((clip) => clip.id === clipId);
}

test('M2 real parent clip delete captures to IDB, accepts on Runtime, and guarded undo restores exact closure', async ({ page, harness, astrid, seed3 }, testInfo) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const identity = await astrid.preflight();
  const initialHistory = await history(harness, seed3);
  expect(initialHistory.head.revision_id).toBe(seed3.headRevisionId);
  const original = await canonicalAt(harness, seed3, initialHistory.head);
  const originalParent = parentPayload(original);
  const originalConfig = parentConfig(original);
  expect(originalConfig.clips).toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.appClipId })]));
  expect(originalParent.clips).toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.appClipId })]));
  expect(originalParent.occurrences).toEqual(expect.arrayContaining([expect.objectContaining({ occurrence_id: seed3.occurrenceId })]));

  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const traffic = attachTraffic(page);

  // Hold exactly the first native commit. The browser must have persisted the
  // request in IDB before the disjoint Agent edit advances the Runtime head.
  let releaseHeldCommit!: () => void;
  const heldCommit = new Promise<void>((resolve) => { releaseHeldCommit = resolve; });
  let holdFirst = true;
  await page.route(COMMIT_ROUTE, async (route) => {
    if (!holdFirst) {
      await route.continue();
      return;
    }
    holdFirst = false;
    await heldCommit;
    await route.continue();
  });

  const clip = page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`).first();
  await expect(clip).toBeVisible();
  const deleteResponsePromise = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  const deleteRequestPromise = page.waitForRequest((request) => request.method() === 'POST'
    && COMMITS.test(new URL(request.url()).pathname), CEILING);
  await clip.click();
  await page.keyboard.press('Delete');
  const deleteRequest = await deleteRequestPromise;
  const deleteBody = deleteRequest.postDataJSON() as Record<string, any>;
  const command = deleteBody.commands?.[0] as Record<string, any>;
  expect(deleteBody).toMatchObject({
    base_revision_id: initialHistory.head.revision_id,
    base_publication_id: initialHistory.head.publication_id,
  });
  expect(deleteBody).not.toHaveProperty('parent_composition');
  expect(deleteBody.commands).toHaveLength(1);
  expect(command).toMatchObject({
    schema_version: 1,
    op: 'clip.delete',
    version: '1',
    select: `parent/clip:${seed3.appClipId}`,
    args: {},
  });
  expect(command.expect && Object.keys(command.expect).length).toBeGreaterThan(0);
  expect(command.reads && command.reads.length).toBeGreaterThan(0);
  expect(command.selections && command.selections.length).toBeGreaterThan(0);

  await expect.poll(async () => {
    const records = await commandOutboxes(page, seed3.timelineId);
    return records.find((record) => record.pending?.request);
  }, CEILING).toBeTruthy();
  const pending = await commandOutboxes(page, seed3.timelineId);
  const owner = pending.find((record) => record.pending?.request);
  expect(owner?.pending?.request.method).toBe('POST');
  expect(owner?.pending?.request.path).toMatch(COMMITS);
  expect(owner?.pending?.request.key).toBe(deleteRequest.headers()['idempotency-key']);
  expect(JSON.parse(owner!.pending!.request.body)).toEqual(deleteBody);
  expect(commandOutboxes(page, seed3.timelineId)).resolves.toEqual(expect.arrayContaining([expect.objectContaining({ pending: expect.objectContaining({ request: expect.any(Object) }) })]));

  // This is the required real Agent edit while the App acknowledgement is in flight.
  const independent = await astrid.commitCaptured(
    harness.seed.projectId,
    seed3.timelineId,
    initialHistory.head,
    { kind: 'track', id: 'f2-delete-independent-C' },
    'm2-parent-delete-independent',
  );
  const independentDocument = independent.data.canonical_document;
  expect(parentConfig(independentDocument).tracks).toEqual(expect.arrayContaining([expect.objectContaining({ id: 'f2-delete-independent-C' })]));
  expect(parentConfig(independentDocument).clips).toEqual(originalConfig.clips);
  expect(parentPayload(independentDocument).registry).toEqual(originalParent.registry);
  expect(parentPayload(independentDocument).occurrences).toEqual(originalParent.occurrences);
  expect(independentDocument.shot_revisions).toEqual(original.shot_revisions);
  expect(independentDocument.internal_timeline_revisions).toEqual(original.internal_timeline_revisions);

  releaseHeldCommit();
  const deleteResponse = await deleteResponsePromise;
  await page.unroute(COMMIT_ROUTE);
  expect(deleteResponse.status(), await deleteResponse.text()).toBe(200);
  await expect.poll(() => traffic.commits.length, CEILING).toBe(1);
  const deleted = await deleteResponse.json() as CommitAcceptedMutation;
  expect(deleted.data.status).toMatch(/^(accepted|rebased)$/);
  expect(deleted.data.previous_revision_id).toBe(independent.data.accepted_revision_id);
  expect(deleted.data.previous_publication_id).toBe(independent.receipt.receipt_id);
  const deletedDocument = deleted.data.canonical_document;
  expect(parentConfig(deletedDocument).clips).not.toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.appClipId })]));
  expect(parentPayload(deletedDocument).clips).not.toEqual(expect.arrayContaining([expect.objectContaining({ id: seed3.appClipId })]));
  expect(parentPayload(deletedDocument).registry).toEqual(originalParent.registry);
  expect(parentPayload(deletedDocument).occurrences).toEqual(originalParent.occurrences);
  expect(internalClip(deletedDocument, seed3.agentClipId)?.app?.f2Opaque).toEqual(seed3.opaque.clip);
  await expectReadback(harness, deletedDocument);
  await expect(clip).toHaveCount(0);
  await expect(commandOutboxes(page, seed3.timelineId)).resolves.toEqual(expect.arrayContaining([expect.objectContaining({ intents: [] })]));

  // Reload proves the accepted Runtime state, not a local projection, owns the absence.
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await expect(page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`)).toHaveCount(0);

  const inverseResponsePromise = page.waitForResponse((response) => response.request().method() === 'POST'
    && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  const inverseResponse = await inverseResponsePromise;
  expect(inverseResponse.status(), await inverseResponse.text()).toBe(200);
  await expect.poll(() => traffic.commits.length, CEILING).toBe(2);
  const inversePost = traffic.commits[1];
  expect(inversePost.body.commands).toEqual([{
    schema_version: 1,
    op: 'timeline.inverse',
    version: '1',
    select: null,
    args: { publications: [deleted.receipt.receipt_id] },
  }]);
  const undone = await inverseResponse.json() as CommitAcceptedMutation;
  expect(undone.data.previous_revision_id).toBe(deleted.data.accepted_revision_id);
  expect(undone.data.previous_publication_id).toBe(deleted.receipt.receipt_id);
  const undoneDocument = undone.data.canonical_document;
  const expectedConfig = { ...originalConfig, tracks: parentConfig(independentDocument).tracks };
  expect(parentConfig(undoneDocument)).toEqual(expectedConfig);
  expect(parentPayload(undoneDocument).clips).toEqual(originalParent.clips);
  expect(parentPayload(undoneDocument).registry).toEqual(originalParent.registry);
  expect(parentPayload(undoneDocument).occurrences).toEqual(originalParent.occurrences);
  expect(parentConfig(undoneDocument).x_f2_opaque).toEqual(seed3.opaque.config);
  expect(internalClip(undoneDocument, seed3.agentClipId)?.app?.f2Opaque).toEqual(seed3.opaque.clip);
  expect(undoneDocument.shot_revisions).toEqual(independentDocument.shot_revisions);
  expect(undoneDocument.internal_timeline_revisions).toEqual(independentDocument.internal_timeline_revisions);
  expect(undoneDocument.dependency_manifest).toEqual(independentDocument.dependency_manifest);
  await expectReadback(harness, undoneDocument);
  await expect(page.locator(`.clip-action[data-clip-id="${seed3.appClipId}"]`)).toBeVisible();

  expect(traffic.snapshotWrites, 'delete and Runtime inverse must never emit snapshot or legacy writes').toEqual([]);
  expect(traffic.renderer, 'renderer remains off for command acceptance').toEqual([]);
  expect(traffic.commits.map((post) => post.body.commands[0].op)).toEqual(['clip.delete', 'timeline.inverse']);
  expect(traffic.commits.every((post) => !Object.prototype.hasOwnProperty.call(post.body, 'parent_composition'))).toBe(true);

  await testInfo.attach('clip-delete-readback', {
    contentType: 'application/json',
    body: Buffer.from(JSON.stringify({
      renderer: 'not started',
      sources: revisionSet(identity),
      approvedCheckouts: { agent: ASTRID_CHECKOUT, runtime: RUNTIME_CHECKOUT },
      approvedHeads: { agent: process.env.TIMELINE_BUNDLE_AGENT_HEAD, runtime: process.env.TIMELINE_BUNDLE_RUNTIME_HEAD },
      original,
      independent: independentDocument,
      deleted: deletedDocument,
      undone: undoneDocument,
      requests: traffic.commits.map((post) => ({ body: post.body, idempotencyKey: post.request.headers()['idempotency-key'] })),
      legacySnapshotWrites: traffic.snapshotWrites,
    }, null, 2)),
  });
});
