/**
 * One representative M2 automatic-placement gate. It starts the same Vite and discovery-proxy processes used by dev:local,
 * then drives the actual editor UI against the actual Runtime. The image executor is a temporary GenericPackHost pack in
 * DirectHarness.tmp, not an App command or a fake Runtime endpoint.
 */
import { expect, type Page, type Request } from '@playwright/test';
import { execFileSync } from 'node:child_process';
import { createServer } from 'node:net';
import { mkdirSync, unlinkSync } from 'node:fs';
import path from 'node:path';
import { APP_ENTRY_ROUTE, commandOutboxes, openSeededTimeline, test as appTest, UI } from './support/app.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON } from './support/astrid.ts';
import { RUNTIME_CHECKOUT, spawnGroup, stopGroup, type DirectHarness } from './support/harness.ts';
import type { ThreeProductsSeed } from './support/harness.ts';

const OPERATION_PREFIX = '/runtime-config/v1/operation';
const NORMAL_RUNTIME_PREFIX = '/api/runtime/v1';
const TASK_PATH = `${OPERATION_PREFIX}/runtime/v1/tasks`;
const COMMIT_PATH = new RegExp(`${OPERATION_PREFIX}/runtime/v1/projects/[^/]+/timelines/[^/]+/commit$`);
const NATIVE_RUNTIME_COMMIT = /^\/api\/runtime\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const TASK_API_POST = /^\/api\/runtime\/v1\/(?:tasks(?:\/[^/]+\/(?:cancel|retry))?|managed-outputs\/[^/]+\/export)$/;
const LEGACY_POST = /^\/api\/runtime\/.*$/;
const PLACEMENT_LANE = 'V2';
const CEILING = { timeout: 60_000 };
const test = appTest.extend<{ workspace: Workspace }>({
  workspace: [async ({ harness }, use) => {
    const seed = await harness.seedThreeProducts();
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);
    const composerCheckout = prepareComposerCheckout(harness);
    await runImageHost(harness, 'register', composerCheckout);
    const vite = await startViteWorkspace(harness, composerCheckout);
    try { await use({ harness, seed, vite }); } finally { await vite.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
});

type Workspace = { harness: DirectHarness; seed: ThreeProductsSeed; vite: ViteWorkspace };
type ViteWorkspace = { origin: string; restart(): Promise<void>; stop(): Promise<void> };
type Wire = { method: string; body: string; key: string; receipt?: Record<string, unknown> };
type RuntimePostKind = 'native-commit' | 'task-api' | 'legacy-writer' | 'other';

function classifyRuntimePost(method: string, pathname: string): RuntimePostKind {
  if (method !== 'POST') return 'other';
  if (NATIVE_RUNTIME_COMMIT.test(pathname)) return 'native-commit';
  if (TASK_API_POST.test(pathname)) return 'task-api';
  return LEGACY_POST.test(pathname) ? 'legacy-writer' : 'other';
}

function normalRuntimeCommitPath(projectId: string, timelineId: string): string {
  return `/api/runtime/v1/projects/${encodeURIComponent(projectId)}/timelines/${encodeURIComponent(timelineId)}/commit`;
}

function isExpectedInverseRequest(request: Request, projectId: string, timelineId: string, publicationId: string): boolean {
  if (request.method() !== 'POST') return false;
  let url: URL;
  let body: Record<string, unknown>;
  try {
    url = new URL(request.url());
    body = request.postDataJSON() as Record<string, unknown>;
  } catch { return false; }
  if (url.pathname !== normalRuntimeCommitPath(projectId, timelineId) || url.search || url.hash
    || !body || Array.isArray(body) || typeof body !== 'object'
    || typeof body.base_revision_id !== 'string' || !body.base_revision_id
    || typeof body.base_publication_id !== 'string' || !body.base_publication_id) return false;
  return JSON.stringify(body) === JSON.stringify({
    api_version: 1,
    project_id: projectId,
    timeline_id: timelineId,
    base_revision_id: body.base_revision_id,
    base_publication_id: body.base_publication_id,
    commands: [{
      schema_version: 1,
      op: 'timeline.inverse',
      version: '1',
      select: null,
      args: { publications: [publicationId] },
    }],
    source: { via: 'app' },
  });
}

function sanitizedError(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

async function freePort(): Promise<number> {
  const server = createServer();
  await new Promise<void>((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  const port = (server.address() as { port: number }).port;
  await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  return port;
}

async function waitFor(url: string, ready: (response: Response) => boolean = (response) => response.ok): Promise<void> {
  const deadline = Date.now() + 60_000;
  let lastFailure = '';
  for (;;) {
    try {
      const response = await fetch(url);
      if (ready(response)) return;
      lastFailure = `${response.status} ${await response.text()}`;
    } catch (error) { lastFailure = error instanceof Error ? error.message : String(error); }
    if (Date.now() >= deadline) throw new Error(`Timed out waiting for ${url}${lastFailure ? ` (last response: ${lastFailure})` : ''}`);
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
}

async function reloadEditor(page: Page, url: string): Promise<void> {
  let lastError: unknown;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      await page.reload({ waitUntil: 'domcontentloaded' });
      return;
    } catch (error) {
      lastError = error;
      if (!(error instanceof Error) || !/ERR_ABORTED|frame was detached/.test(error.message)) throw error;
      await waitFor(url);
    }
  }
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded' });
  } catch (error) {
    throw new Error(`${lastError instanceof Error ? lastError.message : String(lastError)}; fallback navigation failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function processEnv(harness: DirectHarness): NodeJS.ProcessEnv {
  return {
    ...process.env,
    ASTRID_WORKSPACE_DISCOVERY: path.join(harness.supportDir, 'discovery.json'),
    WORKSPACE_RUNTIME_TOKEN_FILE: harness.credentialPath,
    PYTHONPATH: [ASTRID_CHECKOUT, RUNTIME_CHECKOUT].join(path.delimiter),
    PYTHONDONTWRITEBYTECODE: '1',
    PYTHONUNBUFFERED: '1',
  };
}

function prepareComposerCheckout(harness: DirectHarness): string {
  const checkout = path.join(harness.tmp, 'agent-compose-checkout');
  execFileSync('cp', ['-al', ASTRID_CHECKOUT, checkout], { stdio: 'ignore' });
  unlinkSync(path.join(checkout, 'astrid', 'packs', 'generation', 'pack.yaml'));
  unlinkSync(path.join(checkout, 'config', 'astrid-beta-capabilities.json'));
  return checkout;
}

async function startViteWorkspace(harness: DirectHarness, composerCheckout: string): Promise<ViteWorkspace> {
  const proxyPort = await freePort();
  const vitePort = await freePort();
  const origin = `http://127.0.0.1:${vitePort}`;
  const compositionOverlay = path.join(harness.tmp, 'timeline-composition-overlay');
  mkdirSync(compositionOverlay, { recursive: true });
  // This test-only gate follows the current App D10 source attribution and its
  // already-pinned public13 Composition artifact; it does not change any
  // external Runtime or producer pin.
  execFileSync('tar', ['-xzf', path.resolve('vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz'), '-C', compositionOverlay]);
  const compositionRoot = path.join(compositionOverlay, 'package');
  const baseEnv = processEnv(harness);
  const proxy = spawnGroup(process.execPath, [path.resolve('scripts/runtime-discovery-proxy.mjs')], {
    cwd: process.cwd(), env: { ...baseEnv, ASTRID_RUNTIME_PROXY_PORT: String(proxyPort), ASTRID_RUNTIME_OPERATION_ORIGIN: origin },
  });
  const start = () => spawnGroup(process.execPath, [path.resolve('node_modules/vite/bin/vite.js'), '--config', 'config/vite/vite.config.ts', '--host', '127.0.0.1', '--port', String(vitePort), '--strictPort'], {
    cwd: process.cwd(), env: {
      ...baseEnv,
      PORT: String(vitePort),
      ASTRID_CHECKOUT: composerCheckout,
      ASTRID_PYTHON,
      PYTHONPATH: [composerCheckout, RUNTIME_CHECKOUT].join(path.delimiter),
      VITE_ASTRID_BRIDGE_PORT: String(proxyPort),
      ASTRID_BRIDGE_TOKEN: harness.productToken,
      ASTRID_RUNTIME_OPERATION_ORIGIN: origin,
      ASTRID_RUNTIME_PROXY_PORT: String(proxyPort),
      VITE_WORKSPACE_RUNTIME_URL: `http://127.0.0.1:${proxyPort}`,
      WORKSPACE_RUNTIME_TOKEN_FILE: harness.credentialPath,
      VITE_CACHE_DIR: path.join(harness.tmp, 'vite-cache'),
      VITE_TIMELINE_COMPOSITION_ROOT: compositionRoot,
      VITE_DISABLE_REMOTE_FONTS: '1',
      VITE_ASTRID_EDITOR_ONLY: '1',
    },
  });
  let vite = start();
  try {
    await waitFor(`http://127.0.0.1:${proxyPort}/runtime-config/v1/workspace.json`);
    await waitFor(origin);
  } catch (error) {
    const details = [
      `proxy stdout:\n${proxy.stdout.slice(-2000)}`,
      `proxy stderr:\n${proxy.stderr.slice(-4000)}`,
      `vite stdout:\n${vite.stdout.slice(-2000)}`,
      `vite stderr:\n${vite.stderr.slice(-4000)}`,
    ].join('\n');
    await stopGroup(vite); await stopGroup(proxy);
    throw new Error(`${error instanceof Error ? error.message : String(error)}\n${details}`);
  }
  return {
    origin,
    async restart() { await stopGroup(vite); vite = start(); await waitFor(origin); },
    async stop() { await stopGroup(vite); await stopGroup(proxy); },
  };
}

const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=';
const IMAGE_HOST_PROGRAM = String.raw`
import base64, hashlib, json, os, sys
from pathlib import Path
from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
from astrid.core.pack.loader import _load_manifest_payload
from astrid.sdk.workspace_client import resolve_runtime_connection
import yaml
pack_root = Path(sys.argv[1]).resolve()
pack = pack_root / 'generation'
pack.mkdir(parents=True, exist_ok=True)
program = "import base64,hashlib,json; from pathlib import Path; out=Path('{out}'); data=base64.b64decode('${PNG}'); image=out/'generated.png'; image.write_bytes(data); (out/'manifest.json').write_text(json.dumps({'outputs':[{'name':'generated_images','path':'generated.png','artifact_type':'image/png','ordinal':0,'role':'result','is_primary':True,'bytes':len(data),'content_hash':'sha256:'+hashlib.sha256(data).hexdigest()}]}))"
source_manifest = Path(os.environ['ASTRID_SOURCE_CHECKOUT']) / 'astrid' / 'packs' / 'generation' / 'pack.yaml'
source_pack = _load_manifest_payload(source_manifest)
action = json.loads(json.dumps(source_pack['actions']['generate_image']))
action.pop('resources', None)
action['metadata'].update({'adapter_family': 'cpu', 'resource_keys': ['cpu']})
for key in ('api_provider', 'env', 'secrets_required', 'network_policy'):
    action['metadata'].pop(key, None)
action['isolation']['network'] = False
action['invocation'] = {'kind': 'command', 'command': {'argv': ['{python_exec}', '-c', program]}}
(pack / 'pack.yaml').write_text(yaml.safe_dump({
    'schema_version': 3, 'id': 'generation', 'name': 'Astrid Generation Test',
    'version': source_pack['version'], 'actions': {'generate_image': action},
}, sort_keys=False))
endpoint, token = resolve_runtime_connection(os.environ['ASTRID_TIMELINE_EVAL_ENDPOINT'], Path(sys.argv[2]))
runner = GenericPackHost(pack_roots=[pack_root], client=RuntimeProtocolClient(endpoint, token), executor_id=sys.argv[3], attempt_root=pack_root.with_name(pack_root.name + '-attempts'))
runner.discover(); runner.register(deliberate=True)
if sys.argv[4] == 'run':
    settled = runner.run(once=True); task = settled[0] if settled else None
    print(json.dumps({'task_id': task['task_id'] if task else None, 'state': task['state'] if task else 'idle', 'outputs': [{'name': item['name'], 'object_id': item['digest'], 'media_type': item['media_type'], 'size': item['size']} for item in (task or {}).get('result', {}).get('outputs', [])]}))
else:
    print(json.dumps({'state': 'registered', 'capability_id': 'generation.generate_image'}))
`;

async function runImageHost(harness: DirectHarness, mode: 'register' | 'run', composerCheckout: string): Promise<{ state: string; outputs?: Array<{ object_id: string; name: string }> }> {
  const discovery = harness.discovery();
  const packRoot = path.join(composerCheckout, 'astrid', 'packs');
  const env = {
    ...processEnv(harness),
    ASTRID_CHECKOUT: composerCheckout,
    ASTRID_SOURCE_CHECKOUT: ASTRID_CHECKOUT,
    PYTHONPATH: [composerCheckout, RUNTIME_CHECKOUT].join(path.delimiter),
    ASTRID_TIMELINE_EVAL_ENDPOINT: discovery.endpoint,
  };
  const child = spawnGroup(ASTRID_PYTHON, ['-c', IMAGE_HOST_PROGRAM, packRoot, discovery.worker_credential_file, discovery.worker_actor, mode], { cwd: harness.tmp, env });
  const code = await child.exited; await child.closed;
  if (code !== 0) throw new Error(`image host failed (${code}): ${child.stderr.slice(-3000)}`);
  return JSON.parse(child.stdout.trim().split('\n').pop()!) as { state: string; outputs?: Array<{ object_id: string; name: string }> };
}

async function canonicalImage(harness: DirectHarness, seed: ThreeProductsSeed, objectId: string): Promise<void> {
  await expect.poll(async () => {
    const list = await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions?limit=1`);
    const revision = list.body.items.find((item: any) => item.is_current_head)?.revision_id;
    if (!revision) return undefined;
    const parent = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revision}`)).body.payload;
    const occurrence = parent.occurrences.find((item: any) => item.occurrence_id === seed.occurrenceId);
    if (!occurrence) return undefined;
    const shot = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/shots/${seed.shotId}/revisions/${occurrence.shot_revision_id}`)).body;
    const inner = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${shot.internal_timeline_revision_id}`)).body.payload;
    return inner.clips.find((item: any) => inner.registry.assets[item.asset]?.media_id === objectId && item.clipType === 'image');
  }, CEILING).toMatchObject({ track: PLACEMENT_LANE, hold: 5, clipType: 'image' });
}

async function clickRecovery(page: Page, ownerId: string): Promise<void> {
  await page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${ownerId}"]`)).click();
}

async function chooseTextGeneration(page: Page): Promise<void> {
  const textSource = page.getByRole('radio', { name: 'Just text', exact: true });
  await expect(textSource).toBeVisible(CEILING);
  await textSource.click();
  await expect(textSource).toHaveAttribute('aria-checked', 'true');
  const textModel = page.getByRole('radio', { name: 'Qwen Image 2512', exact: true });
  await expect(textModel).toBeVisible(CEILING);
  await textModel.click();
  await expect(textModel).toHaveAttribute('aria-checked', 'true');
}

async function expectConnectedWithDiagnostics(page: Page, diagnostics: string[]): Promise<void> {
  try {
    const status = page.locator(UI.status);
    if (await status.count()) {
      await expect(status).toHaveAttribute('data-state', 'connected', CEILING);
    } else {
      // Same-origin dev proxy mode has no hosted connection gate; the live editor is its readiness signal.
      await expect(page.getByRole('button', { name: 'Generate image', exact: true })).toBeVisible(CEILING);
    }
  } catch (error) {
    const body = await page.locator('body').innerText().catch(() => '');
    throw new Error(`${error instanceof Error ? error.message : String(error)}\n` + [
      `page url: ${page.url()}`,
      `page title: ${await page.title().catch(() => '')}`,
      `body: ${body.slice(-4000)}`,
      ...diagnostics.slice(-40),
    ].join('\n'));
  }
}

test('real operation proxy automatic image placement survives reconnect, lost ACK retry, reload and guarded undo', async ({ page, workspace }) => {
  const { harness, seed, vite } = workspace;
  const composerCheckout = path.join(harness.tmp, 'agent-compose-checkout');
  const legacy: string[] = [];
  const operation: string[] = [];
  const requests: string[] = [];
  const responses: string[] = [];
  const diagnostics: string[] = [];
  page.on('pageerror', (error) => diagnostics.push(`pageerror: ${error.message}`));
  page.on('console', (message) => { if (message.type() === 'error') diagnostics.push(`console: ${message.text()}`); });
  page.on('requestfailed', (request) => diagnostics.push(`requestfailed: ${request.method()} ${request.url()} ${request.failure()?.errorText ?? ''}`));
  page.on('response', (response) => {
    const url = new URL(response.url());
    if (url.pathname.startsWith('/api/runtime') || url.pathname.startsWith(OPERATION_PREFIX)) {
      responses.push(`${response.status()} ${url.pathname}${url.search}`);
    }
  });
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (request.method() === 'POST') requests.push(`${request.method()} ${url.pathname}`);
    if (url.pathname.startsWith(OPERATION_PREFIX) || url.pathname.startsWith(NORMAL_RUNTIME_PREFIX)) operation.push(`${request.method()} ${url.pathname}`);
    if (classifyRuntimePost(request.method(), url.pathname) === 'legacy-writer') legacy.push(url.pathname);
  });

  await page.goto(`${vite.origin}${APP_ENTRY_ROUTE}`);
  await expectConnectedWithDiagnostics(page, diagnostics);
  await openSeededTimeline(page, harness);
  await expect.poll(
    () => responses.filter((entry) => entry.startsWith('200 /api/runtime/v1/events?')).length,
    CEILING,
  ).toBeGreaterThanOrEqual(2);
  await page.getByRole('button', { name: 'Generate image', exact: true }).click();
  const approval = page.getByRole('checkbox', { name: /Add the generated image to this timeline/ });
  await expect(approval).not.toBeChecked();
  expect((await commandOutboxes(page, seed.timelineId)).flatMap((item) => item.placementContinuations ?? [])).toHaveLength(0);
  await approval.check();
  await expect(approval).toBeChecked();
  await chooseTextGeneration(page);
  await page.locator('label').filter({ hasText: 'Raw occurrence reference' }).locator('input').fill(`occurrence:${seed.occurrenceId}`);
  await page.locator('label').filter({ hasText: 'Raw lane ID' }).locator('input').fill(PLACEMENT_LANE);
  await page.locator('label').filter({ hasText: 'Raw anchor clip ID' }).locator('input').fill(seed.agentClipId);
  await page.getByRole('radio', { name: /Managed/ }).click();
  const promptSummary = page.getByText(/Click to add prompts|currently active/).first();
  await expect(promptSummary).toBeVisible(CEILING);
  await promptSummary.click();
  await expect(page.locator('textarea[id^="fullPrompt-"]').first()).toBeVisible(CEILING);
  await page.locator('textarea[id^="fullPrompt-"]').first().fill('a deterministic one-pixel test image');
  await page.getByRole('button', { name: 'Close', exact: true }).first().click();

  let reserved: Awaited<ReturnType<typeof commandOutboxes>> | undefined;
  let taskPost: Wire | undefined;
  let reservationProbeFailure: string | undefined;
  await page.route(`**${TASK_PATH}`, async (route) => {
    taskPost = { method: route.request().method(), body: route.request().postData() ?? '', key: route.request().headers()['idempotency-key'] ?? '' };
    let stage = 'initial reservation probe';
    try {
      reserved = await commandOutboxes(page, seed.timelineId);
      if (!reserved.some((item) => item.placementContinuations?.length)) {
        // Keep the admission request paused: the continuation must become
        // observable before Runtime receives the task body.
        stage = 'reservation probe polling';
        await expect.poll(async () => {
          reserved = await commandOutboxes(page, seed.timelineId);
          return reserved.some((item) => item.placementContinuations?.length);
        }, CEILING).toBe(true);
      }
      await route.continue();
    } catch (error) {
      // Keep the original probe error visible while fail-closing the paused
      // admission request. A probe failure must not permit task transmission.
      reservationProbeFailure = `${stage}: ${sanitizedError(error)}`;
      await route.abort('failed').catch(() => {});
    }
  });
  await page.getByRole('button', { name: 'Generate 1 New Image', exact: true }).click();
  try {
    await expect.poll(() => taskPost, CEILING).not.toBeUndefined();
  } catch (error) {
    throw new Error(`${error instanceof Error ? error.message : String(error)}\n` + [
      `operation requests: ${operation.join(' | ')}`,
      `POST requests: ${requests.join(' | ')}`,
      `Runtime responses: ${responses.slice(-60).join(' | ')}`,
      `diagnostics: ${diagnostics.slice(-40).join(' | ')}`,
      `modal body: ${(await page.locator('body').innerText().catch(() => '')).slice(-4000)}`,
    ].join('\n'));
  }
  const owner = (reserved ?? []).find((item) => item.placementContinuations?.length);
  if (!owner) {
    const probe = reservationProbeFailure ? ` (${reservationProbeFailure})` : '';
    throw new Error(`placement reservation missing before task admission${probe}: ${JSON.stringify(reserved)}`);
  }
  expect(owner?.placementContinuations?.[0].input).toMatchObject({ ownerRef: `occurrence:${seed.occurrenceId}`, lane: PLACEMENT_LANE, anchor: seed.agentClipId });
  expect(owner?.placementContinuations?.[0].input.request).toEqual({ method: 'POST', path: '/v1/tasks', body: taskPost!.body, key: taskPost!.key });
  expect(owner?.placementContinuations?.[0].input.readClosure).toEqual(expect.objectContaining({ head: expect.anything(), savedCanonicalDocument: expect.anything() }));

  const admitted = await runImageHost(harness, 'run', composerCheckout);
  expect(admitted.state).toBe('succeeded');
  const objectId = admitted.outputs?.find((item) => item.name === 'generated_images')?.object_id;
  expect(objectId).toMatch(/^sha256:/);

  // The operation handle is pinned to the old Runtime. Restart both Runtime and Vite, keeping the browser origin and IndexedDB.
  await harness.restartRuntime();
  await vite.restart();
  await waitFor(`${vite.origin}${APP_ENTRY_ROUTE}`);
  await reloadEditor(page, `${vite.origin}${APP_ENTRY_ROUTE}`);
  await expectConnectedWithDiagnostics(page, diagnostics);
  await openSeededTimeline(page, harness);
  const retained = (await commandOutboxes(page, seed.timelineId)).find((item) => item.placementContinuations?.length);
  expect(retained).toBeTruthy();
  await runImageHost(harness, 'run', composerCheckout);
  const taskId = retained!.placementContinuations?.[0].taskLocator?.taskId;
  expect(taskId).toBeTruthy();
  await expect.poll(
    async () => (await harness.runtimeJson<any>('GET', `/v1/tasks/${taskId}`)).body.state,
    CEILING,
  ).toBe('succeeded');
  await expect.poll(
    async () => (await harness.runtimeJson<any>('GET', `/v1/tasks/${taskId}/managed-outputs?limit=50`)).body.items?.length ?? 0,
    CEILING,
  ).toBeGreaterThan(0);

  let lost: Wire | undefined;
  await page.route(COMMIT_PATH, async (route) => {
    const response = await route.fetch();
    lost = { method: route.request().method(), body: route.request().postData() ?? '', key: route.request().headers()['idempotency-key'] ?? '', receipt: await response.json() };
    await route.abort('connectionreset');
  });
  await clickRecovery(page, retained!.ownerId);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).find((item) => item.ownerId === retained!.ownerId)?.pending?.outcome?.kind, CEILING).toBe('retry');
  expect(lost?.body).toBeTruthy();
  await canonicalImage(harness, seed, objectId!);

  await harness.restartRuntime();
  await vite.restart();
  await waitFor(`${vite.origin}${APP_ENTRY_ROUTE}`);
  const operationAfterRestart = operation.length;
  await reloadEditor(page, `${vite.origin}${APP_ENTRY_ROUTE}`);
  await expectConnectedWithDiagnostics(page, diagnostics);
  await openSeededTimeline(page, harness);
  await expect.poll(() => operation.slice(operationAfterRestart).some((entry) => entry.endsWith('/realm')), CEILING).toBe(true);
  const responsesAfterOpen = responses.length;
  await expect.poll(() => responses.length, CEILING).toBeGreaterThan(responsesAfterOpen);
  await new Promise((resolve) => setTimeout(resolve, 1000));
  const recovered = (await commandOutboxes(page, seed.timelineId)).find((item) => item.ownerId === retained!.ownerId)!;
  let retry: Wire | undefined;
  await page.unroute(COMMIT_PATH);
  await page.route(COMMIT_PATH, async (route) => {
    const response = await route.fetch();
    const body = await response.body();
    retry = { method: route.request().method(), body: route.request().postData() ?? '', key: route.request().headers()['idempotency-key'] ?? '', receipt: JSON.parse(body.toString()) };
    await route.fulfill({ status: response.status(), headers: response.headers(), body });
  });
  await clickRecovery(page, recovered.ownerId);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).every((item) => !item.pending && !item.intents.length && !item.placementContinuations?.some((placement) => !placement.placement?.accepted)), CEILING).toBe(true);
  expect(retry).toMatchObject({ method: lost!.method, body: lost!.body, key: lost!.key, receipt: lost!.receipt });
  const completed = (await commandOutboxes(page, seed.timelineId)).find((item) => item.ownerId === recovered.ownerId);
  const inversePublicationId = completed?.placementContinuations?.find((placement) => placement.id === recovered.placementContinuations?.[0]?.id)?.placement?.accepted?.head.publicationId;
  if (!inversePublicationId) throw new Error('automatic placement did not retain its accepted publication for guarded undo');
  await canonicalImage(harness, seed, objectId!);

  await page.unroute(COMMIT_PATH);
  await reloadEditor(page, `${vite.origin}${APP_ENTRY_ROUTE}`);
  await expectConnectedWithDiagnostics(page, diagnostics);
  await openSeededTimeline(page, harness);
  await canonicalImage(harness, seed, objectId!);
  const beforeUndo = operation.length;
  const undoRequest = page.waitForRequest((request) => isExpectedInverseRequest(request, harness.seed.projectId, seed.timelineId, inversePublicationId), CEILING);
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  const undoBody = JSON.parse((await undoRequest).postData() ?? '{}') as { base_revision_id?: string; base_publication_id?: string; commands?: Array<{ op?: string }> };
  expect(undoBody).toMatchObject({ base_revision_id: expect.any(String), base_publication_id: expect.any(String), commands: [{ op: 'timeline.inverse' }] });
  await expect.poll(() => operation.length, CEILING).toBeGreaterThan(beforeUndo);
  await expect.poll(async () => (await commandOutboxes(page, seed.timelineId)).every((item) => !item.pending && !item.intents.length), CEILING).toBe(true);

  const head = await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions?limit=1`);
  const current = head.body.items.find((item: any) => item.is_current_head);
  const undone = await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${current.revision_id}`);
  const occurrence = undone.body.payload.occurrences.find((item: any) => item.occurrence_id === seed.occurrenceId);
  const shot = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/shots/${seed.shotId}/revisions/${occurrence.shot_revision_id}`)).body;
  const inner = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${shot.internal_timeline_revision_id}`)).body.payload;
  expect(inner.clips.some((item: any) => inner.registry.assets[item.asset]?.media_id === objectId)).toBe(false);
  expect(legacy, 'automatic placement never uses legacy POST traffic').toEqual([]);
  expect(operation.some((path) => path.includes('/tasks'))).toBe(true);
  expect(operation.some((path) => /\/tasks\/[^/]+$/.test(path))).toBe(true);
  expect(operation.some((path) => /\/tasks\/[^/]+\/managed-outputs$/.test(path))).toBe(true);
  expect(operation.some((path) => path.includes('/media-selection/verified'))).toBe(true);
  expect(operation.some((path) => path.endsWith('/commit'))).toBe(true);
});
