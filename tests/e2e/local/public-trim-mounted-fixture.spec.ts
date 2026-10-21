import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';
import { expect, type Page, type Route } from '@playwright/test';
import { commandOutboxes, revisionBody, test as appTest } from './support/app.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON } from './support/astrid.ts';
import type { CanonicalDocument, CommitAcceptedMutation, CommitRequest, HistoryPage, Manifest } from '../../../src/integrations/runtime/timeline-commit-types.ts';
import { PRODUCT_ACTOR, REPO_ROOT, RUNTIME_CHECKOUT, type DirectHarness, type ThreeProductsSeed } from './support/harness.ts';

const CEILING = { timeout: 90_000 };
const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_WRITES = /(?:\/composition-revisions(?:\/|$)|\/timelines\/[^/]+\/revisions(?:\/|$)|\/timeline\/save(?:\/|$)|\/(?:restore|restore-history)(?:\/|$)|\/(?:supabase|rest\/v1|astrid\/v1)(?:\/|$))/i;
const LEGACY_MUTATION_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);
const EXACT_AGENT_COMMIT = '6efc81500a0e0688c2bb41e736503f0fc3e04abb';
const EXACT_AGENT_TREE = '2ed2b8a12b5b3391ca221ba6ff05390f71a73556';
const EXACT_RUNTIME_COMMIT = '95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c';
const EXACT_RUNTIME_TREE = 'd3a290b407fa61e6ab2d476f50c068073f70df00';
const EXACT_VENDOR_AGENT_COMMIT = '091aa23ec83ea05ffd3b0115a640230d51c8c429';
const EXACT_VENDOR_AGENT_TREE = 'e3ae90fe482ba6cad6c3f94069127faf76ebceb6';
const EXACT_RUNTIME_ARTIFACT_VERSION = 'sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac';
const EXACT_PUBLIC_COMPOSITION_SHA256 = '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738';
const IMMUTABLE_AGENT_CHECKOUT = '/home/user/work/wt/agt-pin-6efc8150';
const IMMUTABLE_RUNTIME_CHECKOUT = '/home/user/work/wt/rt-pin-95bd3c5f';

type CommitPost = { body: CommitRequest; rawBody: string; key: string; status: number | null; response: CommitAcceptedMutation | null; readError?: string };
const test = appTest.extend<object, { seed3: ThreeProductsSeed }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
});

function git(checkout: string, ...args: string[]) {
  return execFileSync('git', ['-C', checkout, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function requireCleanPin(checkout: string, commit: string, tree: string, label: string) {
  expect(realpathSync(checkout), `${label} checkout`).toBe(realpathSync(label === 'Agent' ? IMMUTABLE_AGENT_CHECKOUT : IMMUTABLE_RUNTIME_CHECKOUT));
  expect(git(checkout, 'rev-parse', 'HEAD'), `${label} commit`).toBe(commit);
  expect(git(checkout, 'rev-parse', 'HEAD^{tree}'), `${label} tree`).toBe(tree);
  expect(git(checkout, 'status', '--porcelain', '--untracked-files=normal'), `${label} checkout must be clean`).toBe('');
}

function verifySourceTuple() {
  expect(process.env.TIMELINE_BUNDLE_AGENT_HEAD).toBe(EXACT_AGENT_COMMIT);
  if (ASTRID_CHECKOUT !== IMMUTABLE_AGENT_CHECKOUT || RUNTIME_CHECKOUT !== IMMUTABLE_RUNTIME_CHECKOUT) throw new Error('public-trim requires the dedicated immutable Agent/Runtime checkouts');
  requireCleanPin(ASTRID_CHECKOUT, EXACT_AGENT_COMMIT, EXACT_AGENT_TREE, 'Agent');
  const provenance = JSON.parse(readFileSync(path.join(REPO_ROOT, 'vendor/astrid-browser/provenance.json'), 'utf8')) as { astrid_commit: string; astrid_tree: string };
  expect(provenance).toMatchObject({ astrid_commit: EXACT_VENDOR_AGENT_COMMIT, astrid_tree: EXACT_VENDOR_AGENT_TREE });
  expect(provenance.astrid_commit).not.toBe(EXACT_AGENT_COMMIT);
  const runtimeLock = JSON.parse(readFileSync(path.join(REPO_ROOT, 'runtime.lock.json'), 'utf8')) as { source_commit: string; producer_version: string };
  expect(runtimeLock).toEqual({ source_commit: EXACT_RUNTIME_COMMIT, producer_version: EXACT_RUNTIME_ARTIFACT_VERSION });
  expect(process.env.TIMELINE_BUNDLE_RUNTIME_HEAD).toBe(runtimeLock.source_commit);
  requireCleanPin(RUNTIME_CHECKOUT, runtimeLock.source_commit, EXACT_RUNTIME_TREE, 'Runtime');
  expect(readFileSync(path.join(REPO_ROOT, 'src/integrations/runtime/generated-contract-metadata.ts'), 'utf8')).toContain('CONTRACT_VERSION = "0.2.14"');
  const vendorCheck = execFileSync(process.execPath, [path.join(REPO_ROOT, 'scripts/vendor-lock.mjs'), 'check', path.join(REPO_ROOT, 'runtime.lock.json'), '--producer', RUNTIME_CHECKOUT], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  expect(vendorCheck).toContain('ok runtime.lock.json (matches pinned producer commit)');
  const vendorSourcesCheck = execFileSync(process.execPath, [path.join(REPO_ROOT, 'scripts/build/verify-astrid-vendor-sources.mjs')], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  expect(vendorSourcesCheck).toContain('Verified');
  const artifacts = JSON.parse(readFileSync(path.join(RUNTIME_CHECKOUT, 'contract/artifacts.json'), 'utf8')) as { artifacts: Record<string, unknown>; producer: string; version: string };
  expect(Object.keys(artifacts).sort()).toEqual(['artifacts', 'producer', 'version']);
  expect(Object.keys(artifacts.artifacts)).toHaveLength(76);
  expect(artifacts).toMatchObject({ producer: 'astrid-runtime', version: runtimeLock.producer_version });
  const archive = path.join(REPO_ROOT, 'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz');
  expect(createHash('sha256').update(readFileSync(archive)).digest('hex')).toBe(EXACT_PUBLIC_COMPOSITION_SHA256);
  const members = execFileSync('tar', ['-tzf', archive], { encoding: 'utf8' }).split('\n').filter((member) => member && !member.endsWith('/'));
  expect(members).toHaveLength(77);
  expect(members.every((member) => member.startsWith('package/'))).toBe(true);
  const modules = JSON.parse(execFileSync(ASTRID_PYTHON, ['-c', 'import astrid, runtime_protocol, json; print(json.dumps({"astrid": astrid.__file__, "runtime": runtime_protocol.__file__}))'], {
    encoding: 'utf8',
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1', PYTHONPATH: [ASTRID_CHECKOUT, RUNTIME_CHECKOUT].join(path.delimiter) },
  })) as { astrid: string; runtime: string };
  expect(realpathSync(modules.astrid)).toContain(`${realpathSync(ASTRID_CHECKOUT)}${path.sep}`);
  expect(realpathSync(modules.runtime)).toContain(`${realpathSync(RUNTIME_CHECKOUT)}${path.sep}`);
}

test.beforeAll(() => verifySourceTuple());

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

async function canonicalDocumentAt(harness: DirectHarness, seed: ThreeProductsSeed, revisionId: string): Promise<CanonicalDocument> {
  const parent = await revisionBody(harness, revisionId);
  const manifest = parent.dependency_manifest as Manifest;
  expect(manifest).toBeTruthy();
  const shotRevisions = await Promise.all(manifest.shots.map(async (pin) => {
    const result = await harness.runtimeJson<Record<string, any>>('GET', `/v1/projects/${harness.seed.projectId}/shots/${pin.shot_id}/revisions/${pin.revision_id}`);
    expect(result.status, JSON.stringify(result.body)).toBe(200);
    expect(result.body).toMatchObject(pin);
    return { ...pin, payload: result.body.payload };
  }));
  const internalTimelineRevisions = await Promise.all(manifest.internal_timelines.map(async (pin) => {
    const result = await harness.runtimeJson<Record<string, any>>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${pin.timeline_id}/revisions/${pin.revision_id}`);
    expect(result.status, JSON.stringify(result.body)).toBe(200);
    expect(result.body).toMatchObject(pin);
    return { ...pin, payload: result.body.payload };
  }));
  return {
    schema_version: 1,
    project_id: harness.seed.projectId,
    timeline_id: seed.timelineId,
    parent_revision: { revision_id: parent.revision_id, content_digest: parent.content_digest, payload: parent.payload },
    shot_revisions: shotRevisions,
    internal_timeline_revisions: internalTimelineRevisions,
    dependency_manifest: manifest,
  } as CanonicalDocument;
}

async function expectImmutableClosure(harness: DirectHarness, seed: ThreeProductsSeed, result: CommitAcceptedMutation) {
  const document = result.data.canonical_document;
  expect(await canonicalDocumentAt(harness, seed, document.parent_revision.revision_id)).toEqual(document);
  const entry = (await history(harness, seed)).items.find((candidate) => candidate.publication_id === result.receipt.receipt_id);
  expect(entry).toMatchObject({
    revision_id: document.parent_revision.revision_id,
    publication_id: result.receipt.receipt_id,
    receipt: result.receipt,
  });
  expect(entry?.receipt).toEqual(result.receipt);
}

function expectAcceptedReceipt(result: CommitAcceptedMutation) {
  expect(result.receipt.result).toEqual(result.data);
  return result;
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
  await expect.poll(() => {
    if (posts[index]?.readError) throw new Error(posts[index].readError);
    return posts[index]?.status;
  }, CEILING).not.toBeNull();
  await expect.poll(() => posts[index]?.response, CEILING).not.toBeNull();
  return posts[index];
}

test('M2 public trim fixture: source window, exact retry/reload, guarded undo and no legacy traffic', async ({ page, harness, seed3 }) => {
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  await harness.startPublicTrimFixtureDevServer();
  const posts: CommitPost[] = [];
  const legacy: string[] = [];
  const credentialLeaks: string[] = [];
  const credentialChecks: Promise<void>[] = [];
  const credentialReadErrors: string[] = [];
  const secret = harness.productToken;
  expect(secret).toBeTruthy();
  const inspectForCredential = (value: string | undefined, source: string) => { if (value?.includes(secret)) credentialLeaks.push(source); };
  page.on('request', (request) => {
    const pathname = new URL(request.url()).pathname;
    inspectForCredential(request.url(), `request URL ${pathname}`);
    inspectForCredential(request.postData() ?? undefined, `request body ${pathname}`);
    for (const [name, value] of Object.entries(request.headers())) inspectForCredential(value, `request header ${name}`);
    if (LEGACY_MUTATION_METHODS.has(request.method()) && LEGACY_WRITES.test(pathname)) legacy.push(`${request.method()} ${pathname}`);
    if (request.method() !== 'POST') return;
    if (COMMITS.test(pathname)) posts.push({ body: request.postDataJSON() as CommitRequest, rawBody: request.postData() ?? '', key: request.headers()['idempotency-key'], status: null, response: null });
  });
  page.on('response', (response) => {
    const pathname = new URL(response.url()).pathname;
    inspectForCredential(response.url(), `response URL ${pathname}`);
    const post = [...posts].reverse().find((candidate) => candidate.key === response.request().headers()['idempotency-key']);
    if (post) post.status = response.status();
    const check = (async () => {
      const headers = await response.allHeaders();
      for (const [name, value] of Object.entries(headers)) inspectForCredential(value, `response header ${name} ${pathname}`);
      const body = await response.body();
      inspectForCredential(body.toString('utf8'), `response body ${pathname}`);
      if (post) post.response = JSON.parse(body.toString('utf8')) as CommitAcceptedMutation;
    })().catch(() => {
      credentialReadErrors.push(`unreadable response ${pathname}`);
      if (post) post.readError = `unreadable response ${pathname}`;
    });
    credentialChecks.push(check);
  });
  page.on('console', (message) => inspectForCredential(message.text(), 'console'));
  page.on('pageerror', (error) => inspectForCredential(error.message, 'page error'));

  await openFixture(page, harness, seed3);
  const before = await history(harness, seed3);
  const original = await revision(harness, seed3, before.head.revision_id);
  const originalAppClip = structuredClone(parentClip(original, seed3.appClipId));
  await page.getByTestId('public-trim-trigger').click();
  await waitForPost(posts, 0);
  expect(posts[0].body).toMatchObject({ project_id: harness.seed.projectId, timeline_id: seed3.timelineId, base_revision_id: before.head.revision_id, base_publication_id: before.head.publication_id });
  expect(posts[0].body.commands).toEqual([expect.objectContaining({ op: 'clip.trim', select: `parent/clip:${seed3.transitionClipId}`, args: { in_s: null, out_s: 2.5 } })]);
  expect(posts[0].status).toBe(200);
  const first = expectAcceptedReceipt(posts[0].response!);
  const firstParent = first.data.canonical_document.parent_revision.payload as Record<string, any>;
  expect(parentClip(firstParent, seed3.transitionClipId)).toMatchObject({ from: 0, to: 2.5, hold: 2.5 });
  expect(parentClip(firstParent, seed3.appClipId)).toEqual(originalAppClip);
  const firstPublication = first.receipt.receipt_id;

  await page.reload();
  await expect(page.getByTestId('public-trim-trigger')).toBeEnabled(CEILING);
  await page.getByTestId('public-trim-undo').click();
  await waitForPost(posts, 1);
  expect(posts[1].body.commands).toEqual([{ schema_version: 1, op: 'timeline.inverse', version: '1', select: null, args: { publications: [firstPublication] } }]);
  const undone = expectAcceptedReceipt(posts[1].response!);
  expect(undone.data.canonical_document.parent_revision.payload).toEqual(original);

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
  expect(originalRetry.body).toMatchObject({ project_id: harness.seed.projectId, timeline_id: seed3.timelineId, base_revision_id: before.head.revision_id, base_publication_id: before.head.publication_id });
  holdAck = false;
  await heldRoute!.abort('connectionreset');
  await page.unroute(COMMITS, holdRetry);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).find((owner) => owner.pending)?.pending?.outcome?.kind, CEILING).toBe('retry');
  const pendingOwners = (await commandOutboxes(page, seed3.timelineId)).filter((owner) => owner.pending?.request.key === originalRetry.key);
  expect(pendingOwners).toHaveLength(1);
  const retryOwner = pendingOwners[0];
  expect(retryOwner).toMatchObject({
    ownerId: expect.any(String),
    scope: { realmId: harness.realmId, actorId: PRODUCT_ACTOR, projectId: harness.seed.projectId, timelineId: seed3.timelineId },
    pending: { request: { method: 'POST', path: `/v1/projects/${harness.seed.projectId}/timelines/${seed3.timelineId}/commit`, body: originalRetry.rawBody, key: originalRetry.key } },
  });
  const retryOwnerId = retryOwner.ownerId;
  await page.reload();
  const recover = page.locator(`[data-testid="public-trim-recover"][data-owner-id="${retryOwnerId}"]`);
  await expect(recover).toHaveCount(1);
  await expect(recover).toBeEnabled(CEILING);
  const persistedOwners = (await commandOutboxes(page, seed3.timelineId)).filter((owner) => owner.ownerId === retryOwnerId);
  expect(persistedOwners).toHaveLength(1);
  expect(persistedOwners[0]).toMatchObject({
    scope: { realmId: harness.realmId, actorId: PRODUCT_ACTOR, projectId: harness.seed.projectId, timelineId: seed3.timelineId },
    pending: { request: { method: 'POST', path: `/v1/projects/${harness.seed.projectId}/timelines/${seed3.timelineId}/commit`, body: originalRetry.rawBody, key: originalRetry.key } },
  });
  const retryResponse = page.waitForResponse((response) => response.request().method() === 'POST' && COMMITS.test(new URL(response.url()).pathname), CEILING);
  await recover.click();
  const response = await retryResponse;
  expect(response.status()).toBe(200);
  expect(response.request().postData()).toBe(originalRetry.rawBody);
  expect(response.request().headers()['idempotency-key']).toBe(originalRetry.key);
  const retried = expectAcceptedReceipt(await response.json() as CommitAcceptedMutation);
  const retriedParent = retried.data.canonical_document.parent_revision.payload as Record<string, any>;
  expect(parentClip(retriedParent, seed3.transitionClipId)).toMatchObject({ from: 0, to: 2.5, hold: 2.5 });
  expect(parentClip(retriedParent, seed3.appClipId)).toEqual(originalAppClip);
  expect(legacy).toEqual([]);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);
  await expectImmutableClosure(harness, seed3, retried);
  const finalHistory = await history(harness, seed3);
  expect(finalHistory.head).toEqual({ revision_id: retried.data.accepted_revision_id, publication_id: retried.receipt.receipt_id });
  expect((await revisionBody(harness, finalHistory.head.revision_id)).parent_revision).toEqual(retried.data.canonical_document.parent_revision);
  expect(finalHistory.items).toHaveLength(before.items.length + 3);
  const storage = await page.evaluate(() => JSON.stringify({
    localStorage: Object.fromEntries(Object.entries(window.localStorage)),
    sessionStorage: Object.fromEntries(Object.entries(window.sessionStorage)),
    cookie: document.cookie,
  }));
  inspectForCredential(storage, 'browser storage');
  await Promise.all(credentialChecks);
  expect(credentialReadErrors).toEqual([]);
  expect(credentialLeaks).toEqual([]);
  expect(await page.evaluate(() => `${location.href}\n${document.body.textContent ?? ''}`)).not.toContain(secret);
  const restarted = await harness.restartRuntime();
  expect(harness.runtimePort).not.toBe(restarted.oldPort);
  expect(harness.runtimeInstanceId).not.toBe(restarted.oldInstanceId);
  const discovery = harness.discovery();
  expect(discovery.endpoint).toBe(harness.runtimeUrl);
  expect(discovery.active_realm).toBe(harness.realmId);
  expect(discovery.runtime_instance_id).toBe(harness.runtimeInstanceId);
  const durable = await history(harness, seed3);
  expect(durable.head).toEqual({ revision_id: retried.data.accepted_revision_id, publication_id: retried.receipt.receipt_id });
  await expectImmutableClosure(harness, seed3, retried);
  const durableRevision = await revisionBody(harness, durable.head.revision_id);
  expect(durableRevision).toMatchObject({ project_id: harness.seed.projectId, timeline_id: seed3.timelineId, revision_id: durable.head.revision_id });
  expect(durableRevision.parent_revision).toEqual(retried.data.canonical_document.parent_revision);
  const durableStorage = await page.evaluate(() => JSON.stringify({
    localStorage: Object.fromEntries(Object.entries(window.localStorage)),
    sessionStorage: Object.fromEntries(Object.entries(window.sessionStorage)),
    cookie: document.cookie,
  }));
  inspectForCredential(durableStorage, 'browser storage after restart');
  expect(credentialReadErrors).toEqual([]);
  expect(credentialLeaks).toEqual([]);
});
