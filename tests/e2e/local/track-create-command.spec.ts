/**
 * M2 source journey for the staged native footer track-create consumer.
 *
 * This stays separate from the existing label/M1/mixed/compound journeys.  It deliberately uses
 * the real + Video/+ Audio buttons and the real Runtime/Agent fixtures; it is not executable until
 * the footer worker is composed onto this source base.
 */
import { expect, type Page, type Request, type Route } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { CONTRACT_VERSION } from '../../../src/integrations/runtime/generated-contract-metadata.ts';
import type {
  CanonicalDocument, CommitAcceptedMutation, HeadPin, HistoryPage, Manifest,
} from '../../../src/integrations/runtime/timeline-commit-types.ts';
import {
  commandOutboxes, expectConnected, openApp, openSeededTimeline, revisionBody, test as appTest,
} from './support/app.ts';
import {
  ASTRID_CHECKOUT, ASTRID_PYTHON, AstridCli, astridUnavailableReason, revisionSet,
} from './support/astrid.ts';
import {
  harnessUnavailableReason, REPO_ROOT, RUNTIME_CHECKOUT, type DirectHarness, type ThreeProductsSeed,
} from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_SAVES = /\/timelines\/[^/]+\/composition-revisions$/;
const SNAPSHOT_WRITES = /\/(?:v1\/projects\/[^/]+\/timelines\/[^/]+|timelines\/[^/]+)\/composition-revisions(?:\/[^/]+)?$/;

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

function sourceContractVersion(checkout: string, file: string): string {
  const source = execFileSync('git', ['-C', checkout, 'show', `HEAD:${file}`], { encoding: 'utf8' });
  return source.match(/CONTRACT_VERSION\s*=\s*['"]([^'"]+)['"]/)?.[1] ?? '';
}

test.beforeAll(() => {
  const reason = harnessUnavailableReason() ?? astridUnavailableReason();
  if (reason) throw new Error(`the M2 track-create journey cannot run: ${reason}`);
  expect(CONTRACT_VERSION).toBe('0.2.3');
  expect(sourceContractVersion(ASTRID_CHECKOUT, 'astrid_runtime_client/contract_metadata.py')).toBe('0.2.3');
  expect(sourceContractVersion(RUNTIME_CHECKOUT, 'packages/python/astrid_runtime_client/contract_metadata.py')).toBe('0.2.3');

  for (const [name, checkout, expected] of [
    ['app', REPO_ROOT, undefined],
    ['agent', ASTRID_CHECKOUT, '027bd16d96010544331c953c0e1014e161786e71'],
    ['runtime', RUNTIME_CHECKOUT, '4c145dc62192f0e942e3ee3922a11488aefe9b41'],
  ] as const) {
    const actual = sourceHead(checkout);
    if (expected) {
      expect(actual.head, `${name} checkout is not the frozen ordinary source`).toBe(expected);
      expect(actual.status, `${name} frozen source lease must stay clean`).toBe('');
    }
    console.log('[track-create] source', JSON.stringify({ name, checkout, ...actual, contractVersion: name === 'app' ? CONTRACT_VERSION : '0.2.3' }));
  }
});

function pinOf(result: CommitAcceptedMutation): HeadPin {
  return { revision_id: result.data.accepted_revision_id, publication_id: result.receipt.receipt_id };
}

function timelineBase(harness: DirectHarness, seed: ThreeProductsSeed): string {
  return `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}`;
}

async function history(harness: DirectHarness, seed: ThreeProductsSeed): Promise<HistoryPage> {
  const response = await harness.runtimeJson<HistoryPage>('GET', `${timelineBase(harness, seed)}/commits?limit=50`);
  expect(response.status, JSON.stringify(response.body)).toBe(200);
  return response.body;
}

/** Build the immutable closure from an accepted Runtime head; no App projection is used as authority. */
async function canonicalAt(harness: DirectHarness, seed: ThreeProductsSeed, head: HeadPin): Promise<CanonicalDocument> {
  const parent = await revisionBody(harness, head.revision_id);
  const manifest = parent.dependency_manifest as Manifest;
  const root = `/v1/projects/${harness.seed.projectId}`;
  const [shotRevisions, internalRevisions] = await Promise.all([
    Promise.all(manifest.shots.map(async (pin) => {
      const response = await harness.runtimeJson('GET', `${root}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
      expect(response.status, JSON.stringify(response.body)).toBe(200);
      return { ...pin, payload: response.body.payload };
    })),
    Promise.all(manifest.internal_timelines.map(async (pin) => {
      const response = await harness.runtimeJson('GET', `${root}/timelines/${pin.timeline_id}/revisions/${pin.revision_id}`);
      expect(response.status, JSON.stringify(response.body)).toBe(200);
      return { ...pin, payload: response.body.payload };
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
  } as CanonicalDocument;
}

async function expectReadback(harness: DirectHarness, document: CanonicalDocument) {
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

function parentConfig(document: CanonicalDocument): Record<string, any> {
  return document.parent_revision.payload.config as Record<string, any>;
}

function parentPayload(document: CanonicalDocument): Record<string, any> {
  return document.parent_revision.payload as Record<string, any>;
}

function attachTraffic(page: Page) {
  const commits: CommitPost[] = [];
  const legacy: string[] = [];
  const renderer: string[] = [];
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    if (request.method() === 'POST' && COMMITS.test(pathname)) {
      commits.push({ request, body: request.postDataJSON() as Record<string, any> });
    }
    if (request.method() === 'POST' && (LEGACY_SAVES.test(pathname) || SNAPSHOT_WRITES.test(pathname))) legacy.push(pathname);
    if (/render|export/i.test(pathname)) renderer.push(`${request.method()} ${pathname}`);
  });
  return { commits, legacy, renderer };
}

function trackRow(document: CanonicalDocument, id: string): Record<string, any> {
  const row = (parentConfig(document).tracks as Array<Record<string, any>>).find((track) => track.id === id);
  expect(row, `accepted parent row ${id} exists`).toBeTruthy();
  return row!;
}

function expectAgentOpaqueClosure(document: CanonicalDocument, seed: ThreeProductsSeed) {
  expect(parentConfig(document).x_f2_opaque).toEqual(seed.opaque.config);
  const child = document.internal_timeline_revisions
    .flatMap((revision) => ((revision.payload as Record<string, any>).clips as Array<Record<string, any>> | undefined) ?? [])
    .find((clip) => clip.id === seed.agentClipId);
  expect(child?.app?.f2Opaque, 'the independent Agent-owned opaque child state survives').toEqual(seed.opaque.clip);
}

function expectCreateClosure(before: CanonicalDocument, after: CanonicalDocument, row: Record<string, any>, seed: ThreeProductsSeed) {
  const expected = structuredClone(parentPayload(before));
  const config = expected.config as Record<string, any>;
  config.tracks = [...(config.tracks as Array<Record<string, any>>), structuredClone(row)];
  expect(parentPayload(after)).toEqual(expected);
  expect(after.shot_revisions).toEqual(before.shot_revisions);
  expect(after.internal_timeline_revisions).toEqual(before.internal_timeline_revisions);
  expect(after.dependency_manifest).toEqual(before.dependency_manifest);
  expectAgentOpaqueClosure(after, seed);
}

function expectTrackCreateRequest(
  request: Request,
  before: CanonicalDocument,
  base: HeadPin,
  kind: 'visual' | 'audio',
): { body: Record<string, any>; command: Record<string, any>; row: Record<string, any> } {
  const body = request.postDataJSON() as Record<string, any>;
  const command = body.commands?.[0] as Record<string, any>;
  expect(body).toMatchObject({
    base_revision_id: base.revision_id,
    base_publication_id: base.publication_id,
    commands: [expect.objectContaining({
      schema_version: 1, op: 'track.create', version: '1', select: 'parent', intent: {},
    })],
  });
  expect(body).not.toHaveProperty('parent_composition');
  expect(body.commands).toHaveLength(1);
  const row = command.args?.row as Record<string, any>;
  expect(row).toEqual(expect.objectContaining({ id: expect.any(String), kind }));
  expect(row.id).not.toMatch(/\/|::/);
  expect(command.created).toEqual([`parent/track:${row.id}`]);
  expect(command.reads).toEqual(expect.arrayContaining([
    { ref: `parent/track:${row.id}`, path: [], state: { state: 'absent' } },
  ]));
  const refs = (parentConfig(before).tracks as Array<Record<string, any>>).map((track) => `parent/track:${track.id}`);
  expect(command.selections).toEqual(expect.arrayContaining([expect.objectContaining({
    key: 'track.create', owner: 'parent', members: refs, order: refs, boundaries: refs, policy: 'guard-membership',
  })]));
  expect(command.expect).toMatchObject({ [`parent/track:${row.id}::`]: { state: 'absent' } });
  expect(command.authorship).toMatchObject({ [`parent/track:${row.id}::`]: 'direct' });
  return { body, command, row };
}

test('M2 real + Video/+ Audio footer track.create survives durable lost ACK, restart/recovery, and guarded undo', async ({ page, harness, astrid, seed3 }, testInfo) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const identity = await astrid.preflight();
  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);

  const traffic = attachTraffic(page);
  const kinds = [
    { kind: 'visual' as const, button: '+ Video', agentId: 'track-create-agent-video' },
    { kind: 'audio' as const, button: '+ Audio', agentId: 'track-create-agent-audio' },
  ];

  for (const { kind, button, agentId } of kinds) {
    await page.reload();
    await expectConnected(page);
    await openSeededTimeline(page, harness);
    const beforeHistory = await history(harness, seed3);
    const before = await canonicalAt(harness, seed3, beforeHistory.head);
    const initialRowCount = await page.locator('[data-sortable-id^="track-"]').count();
    const appRequestIndex = traffic.commits.length;
    let durable!: CommitAcceptedMutation;
    let loseAck: (() => Promise<void>) | undefined;
    const loseAckRoute = async (route: Route) => {
      if (route.request().method() !== 'POST') return route.fallback();
      const response = await route.fetch({ maxRetries: 0 });
      expect(response.status(), await response.text()).toBe(200);
      durable = await response.json() as CommitAcceptedMutation;
      loseAck = () => route.abort('connectionreset');
    };
    await page.route(COMMITS, loseAckRoute);

    const requestPromise = page.waitForRequest((request) => request.method() === 'POST' && COMMITS.test(new URL(request.url()).pathname), CEILING);
    await page.getByRole('button', { name: button, exact: true }).click();
    const request = await requestPromise;
    await expect.poll(() => Boolean(loseAck), CEILING).toBe(true);
    const captured = expectTrackCreateRequest(request, before, beforeHistory.head, kind);
    const originalBytes = request.postData()!;
    const originalKey = request.headers()['idempotency-key'];
    expect(originalKey).toBeTruthy();

    // The complete row is visible from the real local preview while the Runtime has already accepted it.
    await expect(page.locator(`[data-sortable-id="track-${captured.row.id}"]`)).toBeVisible();
    await expect(page.locator(`[data-sortable-id="track-${captured.row.id}"]`).getByRole('textbox', { name: 'Track name' }))
      .toHaveValue(captured.row.label);
    await expect(page.locator('[data-sortable-id^="track-"]')).toHaveCount(initialRowCount + 1);
    expect(durable.data.commands).toEqual([captured.command]);
    expect(trackRow(durable.data.canonical_document, captured.row.id)).toEqual(captured.row);
    expectCreateClosure(before, durable.data.canonical_document, captured.row, seed3);
    await expectReadback(harness, durable.data.canonical_document);
    const acceptedHistory = await history(harness, seed3);
    expect(acceptedHistory.items).toHaveLength(beforeHistory.items.length + 1);
    expect(acceptedHistory.head).toEqual(pinOf(durable));
    await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId))
      .some((owner) => owner.pending?.request.key === originalKey), CEILING).toBe(true);

    // Drop only the acknowledgement after the Runtime has durably accepted the exact request.
    await loseAck!();
    await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId))
      .find((owner) => owner.pending?.request.key === originalKey)?.pending?.outcome?.kind, CEILING).toBe('retry');
    await page.unroute(COMMITS, loseAckRoute);

    await harness.restartRuntime();
    await astrid.preflight();
    await page.reload();
    await expectConnected(page);
    await openSeededTimeline(page, harness);
    const persisted = (await commandOutboxes(page, seed3.timelineId))
      .find((owner) => owner.pending?.request.key === originalKey);
    expect(persisted?.pending?.request.body).toBe(originalBytes);
    expect(persisted?.pending?.request.key).toBe(originalKey);
    expect(await history(harness, seed3)).toEqual(acceptedHistory);

    const ownerId = persisted!.ownerId;
    const retrying = page.waitForResponse((response) => response.request().method() === 'POST'
      && COMMITS.test(new URL(response.url()).pathname), CEILING);
    await page.getByRole('button', { name: /^Recover saved edits/ })
      .and(page.locator(`[data-owner-id="${ownerId}"]`)).click();
    // Recovery is the only action that authorizes the persisted owner; no second row is locally allocated.
    const retry = await retrying;
    expect(retry.status(), await retry.text()).toBe(200);
    expect(retry.request().postData()).toBe(originalBytes);
    expect(retry.request().headers()['idempotency-key']).toBe(originalKey);
    expect(await retry.json()).toEqual(durable);
    await expect.poll(() => traffic.commits.length, CEILING).toBe(appRequestIndex + 2);
    const retryHistory = await history(harness, seed3);
    expect(retryHistory).toEqual(acceptedHistory);
    expect(retryHistory.items.filter((item) => item.publication_id === durable.receipt.receipt_id)).toHaveLength(1);
    await expect(page.locator(`[data-sortable-id="track-${captured.row.id}"]`)).toBeVisible();
    await expect(page.locator(`[data-sortable-id="track-${captured.row.id}"]`).getByRole('textbox', { name: 'Track name' }))
      .toHaveValue(captured.row.label);
    await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId))
      .every((item) => !item.pending && !item.intents.length), CEILING).toBe(true);

    // A disjoint native Agent edit advances the head; UI undo must preserve it while removing only this App row.
    const independent = await astrid.commitCaptured(
      harness.seed.projectId, seed3.timelineId, pinOf(durable), { kind: 'track', id: agentId }, `m2-track-create-${kind}-agent`,
    );
    expect(parentConfig(independent.data.canonical_document).tracks)
      .toEqual(expect.arrayContaining([expect.objectContaining({ id: agentId, kind: 'audio' })]));
    expectCreateClosure(durable.data.canonical_document, independent.data.canonical_document, trackRow(durable.data.canonical_document, captured.row.id), seed3);
    await expectReadback(harness, independent.data.canonical_document);

    const undoResponse = page.waitForResponse((response) => response.request().method() === 'POST'
      && COMMITS.test(new URL(response.url()).pathname), CEILING);
    await page.getByRole('button', { name: 'Undo', exact: true }).click();
    const undo = await undoResponse;
    expect(undo.status(), await undo.text()).toBe(200);
    const undone = await undo.json() as CommitAcceptedMutation;
    expect(undone.data.commands).toEqual([{
      schema_version: 1, op: 'timeline.inverse', version: '1', select: null,
      args: { publications: [durable.receipt.receipt_id] },
    }]);
    const expectedUndone = structuredClone(independent.data.canonical_document);
    const undoneConfig = parentConfig(expectedUndone);
    undoneConfig.tracks = (undoneConfig.tracks as Array<Record<string, any>>).filter((track) => track.id !== captured.row.id);
    expect(undone.data.canonical_document.parent_revision.payload).toEqual(expectedUndone.parent_revision.payload);
    expect(trackRow(undone.data.canonical_document, agentId)).toEqual(trackRow(independent.data.canonical_document, agentId));
    expect(parentConfig(undone.data.canonical_document).tracks)
      .not.toEqual(expect.arrayContaining([expect.objectContaining({ id: captured.row.id })]));
    expectAgentOpaqueClosure(undone.data.canonical_document, seed3);
    await expectReadback(harness, undone.data.canonical_document);
    await expect(page.locator(`[data-sortable-id="track-${captured.row.id}"]`)).toHaveCount(0);
    expect(await history(harness, seed3)).toHaveLength(beforeHistory.items.length + 3);
  }

  expect(traffic.commits.slice(-6).map((post) => post.body.commands[0].op)).toEqual([
    'track.create', 'track.create', 'timeline.inverse', 'track.create', 'track.create', 'timeline.inverse',
  ]);
  expect(traffic.commits.every((post) => !Object.prototype.hasOwnProperty.call(post.body, 'parent_composition'))).toBe(true);
  expect(traffic.legacy, 'footer track.create must not emit legacy canonical snapshot writes').toEqual([]);
  expect(traffic.renderer, 'track creation/undo must not start the renderer').toEqual([]);
  await testInfo.attach('track-create-readback', {
    contentType: 'application/json',
    body: Buffer.from(JSON.stringify({
      sources: revisionSet(identity),
      clientVersion: CONTRACT_VERSION,
      renderer: 'not started',
      legacyCanonicalWrites: traffic.legacy,
      commands: traffic.commits.map((post) => ({ body: post.body, idempotencyKey: post.request.headers()['idempotency-key'] })),
    }, null, 2)),
  });
});
