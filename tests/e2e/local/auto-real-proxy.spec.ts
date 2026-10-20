/**
 * One representative M2 automatic-placement gate. It starts the same Vite and discovery-proxy processes used by dev:local,
 * then drives the actual editor UI against the actual Runtime. The image executor is a temporary GenericPackHost pack in
 * DirectHarness.tmp, not an App command or a fake Runtime endpoint.
 */
import { expect, type Page } from '@playwright/test';
import { createServer } from 'node:net';
import path from 'node:path';
import { APP_ENTRY_ROUTE, commandOutboxes, expectConnected, openSeededTimeline, test as appTest } from './support/app.ts';
import { ASTRID_CHECKOUT, ASTRID_PYTHON, PRODUCT_ACTOR, RUNTIME_CHECKOUT, spawnGroup, stopGroup, type DirectHarness } from './support/harness.ts';
import type { ThreeProductsSeed } from './support/harness.ts';

const OPERATION_PREFIX = '/runtime-config/v1/operation';
const TASK_PATH = `${OPERATION_PREFIX}/runtime/v1/tasks`;
const COMMIT_PATH = new RegExp(`${OPERATION_PREFIX}/runtime/v1/projects/[^/]+/timelines/[^/]+/commit$`);
const LEGACY_POST = /^\/api\/runtime\/.*$/;
const CEILING = { timeout: 60_000 };
const test = appTest.extend<{ workspace: Workspace }>({
  workspace: [async ({ harness }, use) => {
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);
    const seed = await harness.seedThreeProducts();
    const vite = await startViteWorkspace(harness);
    try { await use({ harness, seed, vite }); } finally { await vite.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
});

type Workspace = { harness: DirectHarness; seed: ThreeProductsSeed; vite: ViteWorkspace };
type ViteWorkspace = { origin: string; restart(): Promise<void>; stop(): Promise<void> };
type Wire = { method: string; body: string; key: string; receipt?: Record<string, unknown> };

async function freePort(): Promise<number> {
  const server = createServer();
  await new Promise<void>((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  const port = (server.address() as { port: number }).port;
  await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  return port;
}

async function waitFor(url: string, ready: (response: Response) => boolean = (response) => response.ok): Promise<void> {
  const deadline = Date.now() + 60_000;
  for (;;) {
    try { const response = await fetch(url); if (ready(response)) return; } catch { /* process is still starting */ }
    if (Date.now() >= deadline) throw new Error(`Timed out waiting for ${url}`);
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
}

function processEnv(harness: DirectHarness): NodeJS.ProcessEnv {
  return {
    ...process.env,
    ASTRID_WORKSPACE_DISCOVERY: path.join(harness.supportDir, 'discovery.json'),
    PYTHONPATH: [ASTRID_CHECKOUT, RUNTIME_CHECKOUT].join(path.delimiter),
    PYTHONDONTWRITEBYTECODE: '1',
    PYTHONUNBUFFERED: '1',
  };
}

async function startViteWorkspace(harness: DirectHarness): Promise<ViteWorkspace> {
  const proxyPort = await freePort();
  const vitePort = await freePort();
  const origin = `http://127.0.0.1:${vitePort}`;
  const baseEnv = processEnv(harness);
  const proxy = spawnGroup(process.execPath, [path.resolve('scripts/runtime-discovery-proxy.mjs')], {
    cwd: process.cwd(), env: { ...baseEnv, ASTRID_RUNTIME_PROXY_PORT: String(proxyPort), ASTRID_RUNTIME_OPERATION_ORIGIN: origin },
  });
  const start = () => spawnGroup(process.execPath, [path.resolve('node_modules/vite/bin/vite.js'), '--config', 'config/vite/vite.config.ts', '--host', '127.0.0.1', '--port', String(vitePort), '--strictPort'], {
    cwd: process.cwd(), env: {
      ...baseEnv,
      ASTRID_CHECKOUT,
      ASTRID_PYTHON,
      ASTRID_RUNTIME_OPERATION_ORIGIN: origin,
      ASTRID_RUNTIME_PROXY_PORT: String(proxyPort),
      VITE_WORKSPACE_RUNTIME_URL: `http://127.0.0.1:${proxyPort}`,
      WORKSPACE_RUNTIME_TOKEN_FILE: harness.credentialPath,
      VITE_WORKSPACE_RUNTIME_EXPECTED_ACTOR_ID: PRODUCT_ACTOR,
      VITE_WORKSPACE_RUNTIME_EXPECTED_REALM_ID: harness.realmId,
      VITE_WORKSPACE_RUNTIME_EXPECTED_INSTANCE_ID: harness.runtimeInstanceId,
      VITE_RUNTIME_ORIGIN: '',
      VITE_DISABLE_REMOTE_FONTS: '1',
      VITE_ASTRID_EDITOR_ONLY: '1',
    },
  });
  let vite = start();
  try {
    await waitFor(`http://127.0.0.1:${proxyPort}/runtime-config/v1/workspace.json`);
    await waitFor(origin);
  } catch (error) {
    await stopGroup(vite); await stopGroup(proxy); throw error;
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
from astrid.sdk.workspace_client import resolve_runtime_connection
pack_root = Path(sys.argv[1]).resolve()
pack = pack_root / 'auto-real-image'
pack.mkdir(parents=True, exist_ok=True)
program = "import base64,hashlib,json; from pathlib import Path; out=Path('{out}'); data=base64.b64decode('${PNG}'); image=out/'generated.png'; image.write_bytes(data); (out/'manifest.json').write_text(json.dumps({'outputs':[{'name':'generated_images','path':'generated.png','artifact_type':'image/png','ordinal':0,'role':'result','is_primary':True,'bytes':len(data),'content_hash':'sha256:'+hashlib.sha256(data).hexdigest()}]}))"
(pack / 'executor.yaml').write_text(json.dumps({
    'schema_version': 1, 'id': 'generation.generate_image', 'name': 'M2 real image', 'kind': 'external', 'version': '1.0',
    'command': {'argv': ['{python_exec}', '-c', program]},
    'outputs': [
        {'name': 'generated_images', 'type': 'file', 'path_template': '{out}/generated.png', 'artifact_type': 'image/png'},
    ],
    'metadata': {'adapter_family': 'cpu', 'resource_keys': ['cpu'], 'output_result_manifest': True,
                 'generation_publication': {'version': 1, 'modality': 'image', 'output_port': 'generated_images'}},
}))
endpoint, token = resolve_runtime_connection(os.environ['ASTRID_TIMELINE_EVAL_ENDPOINT'], Path(sys.argv[2]))
runner = GenericPackHost(pack_roots=[pack_root], client=RuntimeProtocolClient(endpoint, token), executor_id=sys.argv[3], attempt_root=pack_root.with_name(pack_root.name + '-attempts'))
runner.discover(); runner.register(deliberate=True)
if sys.argv[4] == 'run':
    settled = runner.run(once=True); task = settled[0] if settled else None
    print(json.dumps({'task_id': task['task_id'] if task else None, 'state': task['state'] if task else 'idle', 'outputs': [{'name': item['name'], 'object_id': item['digest'], 'media_type': item['media_type'], 'size': item['size']} for item in (task or {}).get('result', {}).get('outputs', [])]}))
else:
    print(json.dumps({'state': 'registered', 'capability_id': 'generation.generate_image'}))
`;

async function runImageHost(harness: DirectHarness, mode: 'register' | 'run'): Promise<{ state: string; outputs?: Array<{ object_id: string; name: string }> }> {
  const discovery = harness.discovery();
  const packRoot = path.join(harness.tmp, 'auto-real-image-packs');
  const env = { ...processEnv(harness), ASTRID_TIMELINE_EVAL_ENDPOINT: discovery.endpoint };
  const child = spawnGroup(ASTRID_PYTHON, ['-c', IMAGE_HOST_PROGRAM, packRoot, discovery.worker_credential_file, discovery.worker_actor, mode], { cwd: harness.tmp, env });
  const code = await child.exited; await child.closed;
  if (code !== 0) throw new Error(`image host failed (${code}): ${child.stderr.slice(-3000)}`);
  return JSON.parse(child.stdout.trim().split('\n').pop()!) as { state: string; outputs?: Array<{ object_id: string; name: string }> };
}

async function canonicalImage(harness: DirectHarness, seed: ThreeProductsSeed, objectId: string): Promise<void> {
  const list = await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions?limit=1`);
  const revision = list.body.items.find((item: any) => item.is_current_head)?.revision_id;
  const parent = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/composition-revisions/${revision}`)).body.payload;
  const occurrence = parent.occurrences.find((item: any) => item.occurrence_id === seed.occurrenceId);
  const shot = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/shots/${seed.shotId}/revisions/${occurrence.shot_revision_id}`)).body;
  const inner = (await harness.runtimeJson<any>('GET', `/v1/projects/${harness.seed.projectId}/timelines/${seed.timelineId}/revisions/${shot.internal_timeline_revision_id}`)).body.payload;
  const clip = inner.clips.find((item: any) => inner.registry.assets[item.asset]?.media_id === objectId && item.clipType === 'image');
  expect(clip, 'accepted canonical occurrence image').toMatchObject({ track: 'S1', hold: 5, clipType: 'image' });
}

async function clickRecovery(page: Page, ownerId: string): Promise<void> {
  await page.getByRole('button', { name: /^Recover saved edits/ }).and(page.locator(`[data-owner-id="${ownerId}"]`)).click();
}

test('real operation proxy automatic image placement survives reconnect, lost ACK retry, reload and guarded undo', async ({ page, workspace }) => {
  const { harness, seed, vite } = workspace;
  const legacy: string[] = [];
  const operation: string[] = [];
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (url.pathname.startsWith(OPERATION_PREFIX)) operation.push(`${request.method()} ${url.pathname}`);
    if (request.method() === 'POST' && LEGACY_POST.test(url.pathname)) legacy.push(url.pathname);
  });

  await runImageHost(harness, 'register');
  await page.goto(`${vite.origin}${APP_ENTRY_ROUTE}`);
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await page.getByRole('button', { name: 'Generate image', exact: true }).click();
  const approval = page.getByRole('checkbox', { name: /Add the generated image to this timeline/ });
  await expect(approval).not.toBeChecked();
  expect((await commandOutboxes(page, seed.timelineId)).flatMap((item) => item.placementContinuations ?? [])).toHaveLength(0);
  await page.getByRole('button', { name: /Managed/ }).click();
  await page.locator('textarea[id^="fullPrompt-"]').first().fill('a deterministic one-pixel test image');
  await approval.check();
  await page.locator('label').filter({ hasText: 'Raw occurrence reference' }).locator('input').fill(`occurrence:${seed.occurrenceId}`);
  await page.locator('label').filter({ hasText: 'Raw lane ID' }).locator('input').fill('S1');
  await page.locator('label').filter({ hasText: 'Raw anchor clip ID' }).locator('input').fill('');

  let reserved: Awaited<ReturnType<typeof commandOutboxes>> | undefined;
  let taskPost: Wire | undefined;
  await page.route(`**${TASK_PATH}`, async (route) => {
    taskPost = { method: route.request().method(), body: route.request().postData() ?? '', key: route.request().headers()['idempotency-key'] ?? '' };
    reserved = await commandOutboxes(page, seed.timelineId);
    await route.continue();
  });
  await page.getByRole('button', { name: 'Generate 1 New Image', exact: true }).click();
  await expect.poll(() => taskPost, CEILING).not.toBeUndefined();
  const owner = (reserved ?? []).find((item) => item.placementContinuations?.length);
  expect(owner?.placementContinuations?.[0].input).toMatchObject({ ownerRef: `occurrence:${seed.occurrenceId}`, lane: 'S1', anchor: null });
  expect(owner?.placementContinuations?.[0].input.request).toEqual({ method: 'POST', path: '/v1/tasks', body: taskPost!.body, key: taskPost!.key });
  expect(owner?.placementContinuations?.[0].input.readClosure).toEqual(expect.objectContaining({ head: expect.anything(), savedCanonicalDocument: expect.anything() }));

  const admitted = await runImageHost(harness, 'run');
  expect(admitted.state).toBe('succeeded');
  const objectId = admitted.outputs?.find((item) => item.name === 'generated_images')?.object_id;
  expect(objectId).toMatch(/^sha256:/);

  // The operation handle is pinned to the old Runtime. Restart both Runtime and Vite, keeping the browser origin and IndexedDB.
  await harness.restartRuntime();
  await vite.restart();
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  const retained = (await commandOutboxes(page, seed.timelineId)).find((item) => item.placementContinuations?.length);
  expect(retained).toBeTruthy();
  await runImageHost(harness, 'run');

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
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
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
  await canonicalImage(harness, seed, objectId!);

  await page.unroute(COMMIT_PATH);
  await page.reload();
  await expectConnected(page);
  await openSeededTimeline(page, harness);
  await canonicalImage(harness, seed, objectId!);
  const beforeUndo = operation.length;
  const undoRequest = page.waitForRequest((request) => request.method() === 'POST' && COMMIT_PATH.test(new URL(request.url()).pathname), CEILING);
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
