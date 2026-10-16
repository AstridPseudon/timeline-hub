/**
 * Plan A journey harness (phase A0): the hosted app used from a browser on the same machine as the
 * user's Runtime, through the local loopback gateway (tasks/2026-10-16-plan-a-same-machine-direct.md §3).
 *
 *   npm run test:e2e:direct            # builds dist if it is stale, then runs this file
 *
 * Not part of `npm test`, and not wired into GitHub Actions: .github/workflows/test.yml has only the
 * vitest, boundary and similar unit lanes, no integration or nightly lane to put it in.
 *
 * What runs: a production build served over HTTPS at https://reigh.test:<port> (test certificate made at
 * run time, host mapped by Chromium's --host-resolver-rules, the page marked "public" with
 * --ip-address-space-overrides so Chromium applies its public -> loopback rules), scripts/reigh-loopback-gateway.ts
 * on its well-known port (17340, override with REIGH_DIRECT_GATEWAY_PORT), and a real Runtime daemon on a
 * throwaway SQLite realm. See support/harness.ts for how each is started and torn down.
 *
 * Expected failures: cases that need App or gateway behaviour that does not exist yet are test.fail(), each
 * with a `known-failure:` comment naming the cause (file:line) and the Plan A phase that fixes it. When the
 * phase lands, the case starts passing, Playwright reports it as an unexpected pass, and the marker comes off.
 *
 * Provisional App contract the UI cases assert (firmed up in A1/A2, change here when the App picks names):
 *   [data-testid="runtime-connection-status"][data-state="connected"]   the status pill
 *   [data-testid="runtime-not-connected"]                               the "not connected" panel
 *   a button named "Copy instructions for your agent" inside that panel
 */
import { chromium, expect, test as base, type Browser, type Page } from '@playwright/test';
import { createHash, randomBytes, randomUUID } from 'node:crypto';
import { existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { BIG_DOWNLOAD_BYTES, BIG_UPLOAD_BYTES, DirectHarness, GATEWAY_PORT, harnessUnavailableReason, rawRequest, sha256Hex, startDirectHarness, compositionPublication } from './support/harness.ts';
import { SpeedTable } from './support/measure.ts';

/** Gateway RSS may grow by at most this much while streaming a 60 or 200 MB body ("bounded" means well under the file size). */
const GATEWAY_RSS_GROWTH_LIMIT = 100 * 1024 * 1024;
const UI = {
  status: '[data-testid="runtime-connection-status"]',
  panel: '[data-testid="runtime-not-connected"]',
  copyInstructions: 'Copy instructions for your agent',
};

function resolveChromium(): string | undefined {
  if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) return process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  if (existsSync(chromium.executablePath())) return undefined;
  // The installed Playwright may expect a newer browser build than the one in the image; use what is there.
  const browsers = process.env.PLAYWRIGHT_BROWSERS_PATH ?? '';
  const found = existsSync(browsers) ? readdirSync(browsers).filter((name) => /^chromium-\d+$/.test(name)).sort().pop() : undefined;
  const candidate = found ? path.join(browsers, found, 'chrome-linux', 'chrome') : undefined;
  return candidate && existsSync(candidate) ? candidate : undefined;
}

const test = base.extend<object, { harness: DirectHarness; browser: Browser }>({
  // Playwright reads fixture dependencies from the destructuring pattern, so the empty pattern is required.
  // eslint-disable-next-line no-empty-pattern
  harness: [async ({}, use) => {
    const harness = await startDirectHarness();
    try { await use(harness); } finally { await harness.stop(); }
  }, { scope: 'worker', timeout: 240_000 }],
  browser: [async ({ harness }, use) => {
    const browser = await chromium.launch({ args: harness.chromiumArgs, executablePath: resolveChromium() });
    try { await use(browser); } finally { await browser.close(); }
  }, { scope: 'worker' }],
  context: async ({ browser, harness }, use) => {
    const context = await browser.newContext(harness.contextOptions as Parameters<Browser['newContext']>[0]);
    try { await use(context); } finally { await context.close(); }
  },
});

test.describe.configure({ mode: 'serial' });
test.beforeEach(() => {
  const reason = harnessUnavailableReason();
  test.skip(reason !== null, reason ?? '');
});

const speed = new SpeedTable();
let lastDownload: Buffer | undefined;

// ---------------------------------------------------------------------------------------------
// Helpers

interface PageResponse { status: number; headers: Record<string, string>; text: string }

/** fetch() executed inside the page, so CORS, preflights and local-network rules apply as in a real visit. */
async function pageFetch(page: Page, url: string, init: { method?: string; headers?: Record<string, string>; body?: string } = {}): Promise<PageResponse> {
  return page.evaluate(async ({ url, init }) => {
    const response = await fetch(url, init);
    return { status: response.status, headers: Object.fromEntries(response.headers.entries()), text: await response.text() };
  }, { url, init });
}

const json = <T = any>(response: PageResponse): T => JSON.parse(response.text);

async function openHostedPage(page: Page, harness: DirectHarness) {
  await page.goto(`${harness.origin}/__blank.html`);
}

async function currentHead(harness: DirectHarness): Promise<string> {
  const timelines = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions?limit=1`);
  return timelines.body.items.find((item: any) => item.is_current_head).revision_id;
}

function reportRss(what: string, baselineBytes: number, growthBytes: number) {
  const description = `${what}: gateway RSS baseline ${(baselineBytes / 1048576).toFixed(0)} MB, peak growth ${(growthBytes / 1048576).toFixed(0)} MB (limit ${GATEWAY_RSS_GROWTH_LIMIT / 1048576} MB)`;
  test.info().annotations.push({ type: 'gateway-rss', description });
  console.log(`[direct] ${description}`);
}

async function waitForAudit(harness: DirectHarness, predicate: (entry: ReturnType<DirectHarness['audit']>[number]) => boolean, timeoutMs = 3000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const hit = harness.audit().filter(predicate);
    if (hit.length || Date.now() > deadline) return hit;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
}

/** Opens the App at the hosted origin with nothing in the URL and returns the requests it made to the gateway. */
async function openApp(page: Page, harness: DirectHarness) {
  const gatewayRequests: string[] = [];
  page.on('request', (request) => { if (request.url().startsWith(`http://127.0.0.1:${GATEWAY_PORT}/`)) gatewayRequests.push(`${request.method()} ${request.url()}`); });
  await page.goto(`${harness.origin}/`);
  return gatewayRequests;
}
const expectConnected = (page: Page) => expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected');

function connectProbe(harness: DirectHarness, options: { origin?: string | null; host?: string } = {}) {
  const headers: Record<string, string> = {};
  if (options.origin !== null) headers.Origin = options.origin ?? harness.origin;
  return rawRequest({ port: harness.gatewayPort, path: '/v1/connect', headers, host: options.host });
}

// ---------------------------------------------------------------------------------------------
// 1. Zero-click connection

test.describe('zero-click connection (App)', () => {
  // known-failure: reigh-app | 2026-10-30 | the App never looks for the gateway: src/integrations/runtime/client.ts:33 hard-wires the same-origin /api/runtime (404 on the hosted origin); fixed by Plan A A1 (resolver + GET /v1/connect)
  test.fail('opening the hosted origin connects to the local Runtime with nothing in the URL', async ({ page, harness }) => {
    const gatewayRequests = await openApp(page, harness);
    await expectConnected(page);
    expect(page.url()).toBe(`${harness.origin}/`);
    expect(gatewayRequests.some((request) => request.startsWith('GET ') && request.endsWith('/v1/connect'))).toBe(true);
    await expect(page.getByText(harness.seed.projectName)).toBeVisible();
  });

  // known-failure: reigh-app | 2026-10-30 | same cause as above: no connection state exists in the App (client.ts:33, no resolver); fixed by Plan A A1
  test.fail('a reload stays connected', async ({ page, harness }) => {
    await openApp(page, harness);
    await expectConnected(page);
    await page.reload();
    await expectConnected(page);
    expect(page.url()).toBe(`${harness.origin}/`);
  });

  // known-failure: reigh-app | 2026-10-30 | no "not connected" panel, copy control or re-check loop exists (client.ts:33 gives the App only /api/runtime); fixed by Plan A A2 (D3)
  test.fail('with the gateway stopped the panel offers agent instructions, then connects by itself once it starts', async ({ page, harness, context }) => {
    await context.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: harness.origin });
    await harness.stopGateway();
    try {
      await openApp(page, harness);
      await page.evaluate(() => { (window as unknown as { __noReload: boolean }).__noReload = true; });
      const panel = page.locator(UI.panel);
      await expect(panel).toBeVisible();
      await panel.getByRole('button', { name: UI.copyInstructions }).click();
      const copied = await page.evaluate(() => navigator.clipboard.readText());
      expect(copied).toContain('banodoco-local up --profile astrid');
      expect(copied).toContain('npm run dev:local');
      await harness.startGateway();
      await expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected', { timeout: 20_000 });
      expect(await page.evaluate(() => (window as unknown as { __noReload?: boolean }).__noReload)).toBe(true);
    } finally {
      await harness.resetToHealthy();
    }
  });
});

test.describe('first time and returning panels (App)', () => {
  // known-failure: reigh-app | 2026-10-30 | the App keeps no record of an earlier connection and has no panel at all (src/integrations/runtime/client.ts:33 gives it only the same-origin /api/runtime); fixed by Plan A A2 (D3a)
  test.fail('a fresh profile shows "Set up Reigh on this computer", and after one connection the same profile shows "Reigh isn\'t running"', async ({ page, harness }) => {
    // Same context for both phases, so localStorage carries over; the fixture context is fresh, so nothing is remembered at the start.
    await harness.stopGateway();
    await harness.stopRuntime();
    try {
      await openApp(page, harness);
      const panel = page.locator(UI.panel);
      await expect(panel.getByRole('heading', { name: 'Set up Reigh on this computer' })).toBeVisible();
      await expect(panel.getByText('Already installed? Start it')).toBeVisible();
      await expect(panel.getByRole('button', { name: UI.copyInstructions })).toBeVisible();

      await harness.startRuntime();
      await harness.startGateway();
      await expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected', { timeout: 20_000 });

      await harness.stopGateway();
      await page.reload();
      await expect(panel.getByRole('heading', { name: "Reigh isn't running" })).toBeVisible();
      await expect(panel.getByText('Set up Reigh on this computer')).toHaveCount(0);
    } finally {
      await harness.resetToHealthy();
    }
  });
});

test.describe('GET /v1/connect (gateway)', () => {
  // known-failure: reigh-app | 2026-10-30 | the gateway has no /v1/connect: scripts/reigh-loopback-gateway.ts:58 answers every non-session path with 401 session_required; fixed by Plan A A1 (D1)
  test.fail('answers the configured origin with the session base, realm and Runtime instance', async ({ harness }) => {
    const response = await connectProbe(harness);
    expect(response.status).toBe(200);
    expect(response.headers['access-control-allow-origin']).toBe(harness.origin);
    const body = response.json();
    expect(body.base).toMatch(new RegExp(`^http://127\\.0\\.0\\.1:${harness.gatewayPort}/session/[A-Za-z0-9_-]{32,}/api/runtime$`));
    expect(JSON.stringify(body)).toContain(harness.realmId);
    expect(JSON.stringify(body)).toContain(harness.runtimeInstanceId);
    const viaLocalhost = await connectProbe(harness, { host: `localhost:${harness.gatewayPort}` });
    expect(viaLocalhost.status).toBe(200);
  });

  // known-failure: reigh-app | 2026-10-30 | no /v1/connect yet (reigh-loopback-gateway.ts:58); without the 200 control below the refusal would be vacuous; fixed by Plan A A1 (D1)
  test.fail('refuses another origin', async ({ harness }) => {
    expect((await connectProbe(harness)).status).toBe(200);
    const refused = await connectProbe(harness, { origin: harness.otherOrigin });
    expect(refused.status).toBe(403);
    expect(refused.headers['access-control-allow-origin']).toBeUndefined();
    expect(refused.text).not.toContain('/session/');
  });

  // known-failure: reigh-app | 2026-10-30 | no /v1/connect yet (reigh-loopback-gateway.ts:58); fixed by Plan A A1 (D1)
  test.fail('refuses a rebinding Host', async ({ harness }) => {
    expect((await connectProbe(harness)).status).toBe(200);
    for (const host of [`${'evil.test'}:${harness.gatewayPort}`, '127.0.0.1', 'localhost', `127.0.0.1:${harness.gatewayPort + 1}`, `127.0.0.1.evil.test:${harness.gatewayPort}`]) {
      const refused = await connectProbe(harness, { host });
      expect(refused.status, `Host ${host}`).toBe(403);
      expect(refused.text).not.toContain('/session/');
    }
  });

  // known-failure: reigh-app | 2026-10-30 | no /v1/connect yet (reigh-loopback-gateway.ts:58); fixed by Plan A A1 (D1)
  test.fail('refuses a request without an Origin', async ({ harness }) => {
    expect((await connectProbe(harness)).status).toBe(200);
    const refused = await connectProbe(harness, { origin: null });
    expect(refused.status).toBe(403);
    expect(refused.text).not.toContain('/session/');
  });
});

// ---------------------------------------------------------------------------------------------
// 2. Core journey

test.describe('core journey', () => {
  // known-failure: reigh-app | 2026-10-30 | the App cannot reach the Runtime from the hosted origin (client.ts:33), so nothing opens; the editor selectors are provisional; fixed by Plan A A1 (core journey green)
  test.fail('App: open the seeded project, edit, save, reload byte-identical', async ({ page, harness }) => {
    await openApp(page, harness);
    await expectConnected(page);
    await page.getByText(harness.seed.projectName).click();
    const editor = page.locator('[data-testid="timeline-editor"]');
    await expect(editor).toBeVisible();
    await page.getByRole('button', { name: 'Save' }).click();
    await expect(page.locator('[data-testid="timeline-saved"]')).toBeVisible();
    const before = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions/${await currentHead(harness)}`);
    await page.reload();
    await expectConnected(page);
    const after = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions/${await currentHead(harness)}`);
    expect(JSON.stringify(after.body)).toBe(JSON.stringify(before.body));
  });

  // known-failure: reigh-app | 2026-10-30 | same cause (client.ts:33), and no draft survives a refused save (F3, Plan A A2); fixed by Plan A A1 (conflict shown) and A2 (draft kept)
  test.fail('App: a second writer saves first, the App shows the conflict and keeps the draft', async ({ page, harness }) => {
    await openApp(page, harness);
    await expectConnected(page);
    await page.getByText(harness.seed.projectName).click();
    await expect(page.locator('[data-testid="timeline-editor"]')).toBeVisible();
    await page.locator('[data-testid="timeline-title-input"]').fill('Draft from the first writer');
    const head = await currentHead(harness);
    const second = await harness.runtimeJson('POST', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions`, compositionPublication(harness.seed, head, 'Second writer', 24));
    expect(second.status).toBe(200);
    await page.getByRole('button', { name: 'Save' }).click();
    await expect(page.getByText(/conflict/i)).toBeVisible();
    await expect(page.locator('[data-testid="timeline-title-input"]')).toHaveValue('Draft from the first writer');
  });

  test('through the hosted origin: open, read the timeline, save with the expected head, reload byte-identical', async ({ page, harness }) => {
    const { projectId, timelineId } = harness.seed;
    await openHostedPage(page, harness);
    const call = (suffix: string, init?: Parameters<typeof pageFetch>[2]) => pageFetch(page, `${harness.gatewayBase}${suffix}`, init);

    const projects = await call('/v1/projects?limit=100');
    expect(projects.status).toBe(200);
    expect(json(projects).items.map((item: any) => item.project_id)).toContain(projectId);

    const inspectPath = `/v1/projects/${projectId}/timelines/${timelineId}/inspect`;
    const read = await call(inspectPath, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    expect(read.status).toBe(200);
    const direct = await harness.runtimeFetch(inspectPath, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    expect(read.text).toBe(await direct.text());

    const head = await currentHead(harness);
    const publication = compositionPublication(harness.seed, head, 'Main (edited through the gateway)', 24);
    const saved = await call(`/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': randomUUID() }, body: JSON.stringify(publication),
    });
    expect(saved.status, saved.text).toBe(200);
    const newHead: string = json(saved).data.new_head;
    expect(newHead).not.toBe(head);

    const revisionPath = `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions/${newHead}`;
    const beforeReload = await call(revisionPath);
    expect(beforeReload.status).toBe(200);
    expect(beforeReload.text).toContain('Main (edited through the gateway)');
    const afterReadInspect = await call(inspectPath, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });

    await page.reload();
    const afterReload = await call(revisionPath);
    expect(afterReload.text).toBe(beforeReload.text);
    expect((await call(inspectPath, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })).text).toBe(afterReadInspect.text);
    // And the bytes the Runtime holds are the same bytes the page saw.
    expect(await (await harness.runtimeFetch(revisionPath)).text()).toBe(afterReload.text);
  });

  test('through the hosted origin: a second writer saves first, the stale save is refused and the first writer keeps its draft', async ({ page, harness }) => {
    const { projectId, timelineId } = harness.seed;
    await openHostedPage(page, harness);
    const publishUrl = `${harness.gatewayBase}/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`;
    const head = await currentHead(harness);
    const draft = compositionPublication(harness.seed, head, 'First writer draft', 12); // held by the caller

    const second = await harness.runtimeJson('POST', `/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, compositionPublication(harness.seed, head, 'Second writer', 24));
    expect(second.status).toBe(200);

    const refused = await pageFetch(page, publishUrl, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': 'journey-stale-save' }, body: JSON.stringify(draft) });
    expect(refused.status).toBe(409);
    expect(json(refused).details).toMatchObject({ reason: 'stale_head', expected_head: head, actual_head: second.body.data.new_head });
    // Nothing of the draft reached the Runtime; the draft object itself is untouched for a retry.
    expect(await currentHead(harness)).toBe(second.body.data.new_head);
    expect(draft.expected_head).toBe(head);
    expect(draft.parent_composition.name).toBe('First writer draft');
    const rebased = await pageFetch(page, publishUrl, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': 'journey-rebased-save' }, body: JSON.stringify({ ...draft, expected_head: second.body.data.new_head }) });
    expect(rebased.status, rebased.text).toBe(200);
  });
});

// ---------------------------------------------------------------------------------------------
// 3. Media and big files

test.describe('media', () => {
  const objectUrl = (harness: DirectHarness, objectId: string) => `${harness.gatewayBase}/v1/objects/${encodeURIComponent(objectId)}`;

  test('an image element loads with crossorigin=anonymous (Origin), and without it only with an explicit referrer policy', async ({ page, harness }) => {
    await openHostedPage(page, harness);
    const src = objectUrl(harness, harness.seed.image.objectId);
    const load = (variant: 'cors' | 'plain' | 'referrer-origin') => page.evaluate(({ src, variant }) => new Promise<number[] | string>((resolve) => {
      const image = new Image();
      if (variant === 'cors') image.crossOrigin = 'anonymous';
      if (variant === 'referrer-origin') image.referrerPolicy = 'origin';
      image.onload = () => resolve([image.naturalWidth, image.naturalHeight]);
      image.onerror = () => resolve('error');
      image.src = `${src}?${variant}=1`;
    }), { src, variant });
    expect(await load('cors'), 'crossorigin=anonymous').toEqual([64, 48]);
    // Finding for Plan A D5: the default referrer policy sends no Referer on https -> http, so the gateway's
    // Referer fallback (reigh-loopback-gateway.ts:72-76) does not rescue a plain element. Media must say crossorigin.
    expect(await load('plain'), 'no crossorigin attribute, default referrer policy').toBe('error');
    expect(await load('referrer-origin'), 'no crossorigin attribute, referrerpolicy=origin').toEqual([64, 48]);
    const served = await waitForAudit(harness, (entry) => entry.path === `/v1/objects/${harness.seed.image.objectId}` && entry.status === 200);
    expect(served.some((entry) => entry.origin === harness.origin)).toBe(true); // browser sent Origin
    expect(served.some((entry) => entry.origin === null)).toBe(true); // Referer accepted
    expect(harness.audit().some((entry) => entry.path === `/v1/objects/${harness.seed.image.objectId}` && entry.origin === null && entry.status === 403)).toBe(true); // the plain one
  });

  test('a video loads, and seeking it is a 206 Range read', async ({ page, harness }) => {
    const { video } = harness.seed;
    test.skip(!video.decodable, 'ffmpeg is not installed; the fallback MP4 cannot be decoded by stock Chromium (Range is still checked below)');
    await openHostedPage(page, harness);
    const result = await page.evaluate(({ src }) => new Promise<{ duration: number; seekedTo: number } | string>((resolve) => {
      const element = document.createElement('video');
      element.crossOrigin = 'anonymous';
      element.muted = true;
      element.preload = 'auto';
      element.onerror = () => resolve(`error ${element.error?.code}`);
      element.onloadedmetadata = () => { element.currentTime = element.duration * 0.6; };
      element.onseeked = () => resolve({ duration: element.duration, seekedTo: element.currentTime });
      element.src = src;
      document.body.append(element);
    }), { src: objectUrl(harness, video.objectId) });
    expect(typeof result).toBe('object');
    const outcome = result as { duration: number; seekedTo: number };
    expect(outcome.duration).toBeGreaterThan(10);
    expect(outcome.seekedTo).toBeGreaterThan(5);
    const ranged = await waitForAudit(harness, (entry) => entry.path === `/v1/objects/${video.objectId}` && entry.status === 206);
    expect(ranged.length).toBeGreaterThan(0);
  });

  test('Range reads return 206 with the exact bytes, an unsatisfiable range is refused', async ({ page, harness }) => {
    const { video } = harness.seed;
    await openHostedPage(page, harness);
    const url = objectUrl(harness, video.objectId);
    const whole = Buffer.from(await (await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(video.objectId)}`)).arrayBuffer());
    expect(sha256Hex(whole)).toBe(video.digest);

    const slice = await page.evaluate(async ({ url }) => {
      const response = await fetch(url, { headers: { Range: 'bytes=100-1123' } });
      const bytes = new Uint8Array(await response.arrayBuffer());
      const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
      return { status: response.status, contentRange: response.headers.get('content-range'), acceptRanges: response.headers.get('accept-ranges'), length: bytes.length, digest: Array.from(digest, (b) => b.toString(16).padStart(2, '0')).join('') };
    }, { url });
    expect(slice.status).toBe(206);
    expect(slice.contentRange).toBe(`bytes 100-1123/${whole.length}`);
    expect(slice.length).toBe(1024);
    expect(slice.digest).toBe(createHash('sha256').update(whole.subarray(100, 1124)).digest('hex'));

    const tail = await pageFetch(page, url, { headers: { Range: 'bytes=-64' } });
    expect(tail.status).toBe(206);
    expect(tail.headers['content-range']).toBe(`bytes ${whole.length - 64}-${whole.length - 1}/${whole.length}`);
    const beyond = await pageFetch(page, url, { headers: { Range: `bytes=${whole.length + 10}-` } });
    expect(beyond.status).toBe(416);
  });

  test('a 60 MB download keeps its digest and the gateway streams it in bounded memory', async ({ page, harness }) => {
    const { big } = harness.seed;
    await openHostedPage(page, harness);
    const { result, growthBytes, baselineBytes } = await harness.withRssSampling(() => page.evaluate(async ({ url }) => {
      const response = await fetch(url);
      const bytes = new Uint8Array(await response.arrayBuffer());
      const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
      return { status: response.status, length: bytes.length, contentLength: response.headers.get('content-length'), digest: `sha256:${Array.from(digest, (b) => b.toString(16).padStart(2, '0')).join('')}` };
    }, { url: objectUrl(harness, big.objectId) }));
    expect(result.status).toBe(200);
    expect(result.length).toBe(BIG_DOWNLOAD_BYTES);
    expect(result.contentLength).toBe(String(BIG_DOWNLOAD_BYTES));
    expect(result.digest).toBe(big.digest);
    reportRss('60 MB download', baselineBytes, growthBytes);
    expect(growthBytes).toBeLessThan(GATEWAY_RSS_GROWTH_LIMIT);
  });

  test('a 200 MB upload from the page keeps its digest and the gateway streams it in bounded memory', async ({ page, harness }) => {
    await openHostedPage(page, harness);
    const { result, growthBytes, baselineBytes } = await harness.withRssSampling(() => page.evaluate(async ({ url, bytes, projectUrl }) => {
      const chunk = new Uint8Array(1024 * 1024);
      const parts: Uint8Array[] = [];
      for (let i = 0; i < bytes / chunk.length; i++) {
        const part = new Uint8Array(chunk.length);
        for (let offset = 0; offset < part.length; offset += 65536) crypto.getRandomValues(part.subarray(offset, offset + 65536));
        parts.push(part);
      }
      const blob = new Blob(parts as BlobPart[], { type: 'application/octet-stream' });
      const expected = new Uint8Array(await crypto.subtle.digest('SHA-256', await blob.arrayBuffer()));
      const response = await fetch(`${url}${projectUrl}`, { method: 'POST', headers: { 'Content-Type': 'application/octet-stream', 'Idempotency-Key': crypto.randomUUID(), 'X-Original-Name': 'upload-200mb.bin' }, body: blob });
      const body = await response.json();
      return { status: response.status, digest: body?.data?.digest, size: body?.data?.size, expected: `sha256:${Array.from(expected, (b) => b.toString(16).padStart(2, '0')).join('')}` };
    }, { url: harness.gatewayBase, bytes: BIG_UPLOAD_BYTES, projectUrl: `/v1/projects/${harness.seed.projectId}/objects` }));
    expect(result.status).toBe(201);
    expect(result.size).toBe(BIG_UPLOAD_BYTES);
    expect(result.digest).toBe(result.expected);
    reportRss('200 MB upload', baselineBytes, growthBytes);
    expect(growthBytes).toBeLessThan(GATEWAY_RSS_GROWTH_LIMIT);
    // The Runtime holds exactly those bytes.
    const stored = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(result.digest)}`, { method: 'HEAD' });
    expect(stored.status).toBe(200);
    expect(stored.headers.get('content-length')).toBe(String(BIG_UPLOAD_BYTES));
  });
});

// ---------------------------------------------------------------------------------------------
// 4. Restarts

test.describe('restarts', () => {
  test.afterEach(async ({ harness }) => { await harness.resetToHealthy(); });

  test('the Runtime comes back on a new port with the same realm, data and credential', async ({ harness }) => {
    const { oldPort, oldInstanceId } = await harness.restartRuntime();
    expect(harness.runtimePort).not.toBe(oldPort);
    expect(harness.runtimeInstanceId).not.toBe(oldInstanceId);
    const realm = await harness.runtimeJson('GET', '/v1/realm');
    expect(realm.status).toBe(200);
    expect(JSON.stringify(realm.body)).toContain(harness.realmId);
    const projects = await harness.runtimeJson('GET', '/v1/projects?limit=100');
    expect(projects.body.items.map((item: any) => item.project_id)).toContain(harness.seed.projectId);
    const image = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(harness.seed.image.objectId)}`);
    expect(sha256Hex(Buffer.from(await image.arrayBuffer()))).toBe(harness.seed.image.digest);
  });

  // known-failure: reigh-app | 2026-10-30 | the gateway reads discovery once at start and keeps that endpoint (scripts/reigh-loopback-gateway.ts:160-161, :181), so after a Runtime restart on a new port every request is a 502; fixed by Plan A A2 (D2)
  test.fail('the gateway keeps serving after the Runtime restarts on a new port (it re-reads discovery)', async ({ harness }) => {
    await harness.restartRuntime();
    const response = await harness.gatewayRequest('/v1/health');
    expect(response.status).toBe(200);
    expect(response.json().runtime_instance_id).toBe(harness.runtimeInstanceId);
  });

  // known-failure: reigh-app | 2026-10-30 | the App has no connection resolver, so it cannot follow a Runtime restart; today a changed instance only fences the client (src/integrations/runtime/client.ts:70, 'relaunch workspace'); fixed by Plan A A2 (D4)
  test.fail('App: a Runtime restart on a new port continues with the draft kept', async ({ page, harness }) => {
    await openApp(page, harness);
    await expectConnected(page);
    await page.evaluate(() => { (window as unknown as { __noReload: boolean }).__noReload = true; });
    await harness.restartRuntime();
    await harness.restartGateway(); // stands in for the gateway re-reading discovery until A2 makes it do so itself
    await expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected', { timeout: 20_000 });
    await expect(page.getByText(/relaunch workspace/i)).toHaveCount(0);
    await expect(page.locator('[data-testid="timeline-unsaved-indicator"]')).toBeVisible();
    expect(await page.evaluate(() => (window as unknown as { __noReload?: boolean }).__noReload)).toBe(true);
  });

  test('a stopped gateway refuses connections (Node and the page); started again it serves on the same fixed port', async ({ page, harness }) => {
    await openHostedPage(page, harness);
    const before = harness.gatewayBase;
    await harness.stopGateway();
    await expect(rawRequest({ port: harness.gatewayPort, path: '/v1/connect', headers: { Origin: harness.origin } })).rejects.toMatchObject({ code: 'ECONNREFUSED' });
    const fromPage = await page.evaluate(async (url) => { try { await fetch(url); return 'responded'; } catch { return 'failed'; } }, `${before}/v1/health`);
    expect(fromPage).toBe('failed');

    const started = await harness.startGateway();
    expect(new URL(started.base).port).toBe(String(GATEWAY_PORT));
    const health = await pageFetch(page, `${started.base}/v1/health`);
    expect(health.status).toBe(200);
    expect(json(health).runtime_instance_id).toBe(harness.runtimeInstanceId);
    const projects = await harness.gatewayRequest('/v1/projects?limit=100');
    expect(projects.json().items.map((item: any) => item.project_id)).toContain(harness.seed.projectId);
  });

  // known-failure: reigh-app | 2026-10-30 | nothing in the App reconnects: no resolver, no /v1/connect call (client.ts:33), and the gateway hands out a new random capability on every start (reigh-loopback-gateway.ts:47) that only a fresh /v1/connect could deliver; fixed by Plan A A1 + A2
  test.fail('App: a gateway restart reconnects by itself', async ({ page, harness }) => {
    await openApp(page, harness);
    await expectConnected(page);
    await page.evaluate(() => { (window as unknown as { __noReload: boolean }).__noReload = true; });
    await harness.restartGateway();
    await expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected', { timeout: 20_000 });
    expect(await page.evaluate(() => (window as unknown as { __noReload?: boolean }).__noReload)).toBe(true);
  });
});

// ---------------------------------------------------------------------------------------------
// 5. Security

test.describe('security', () => {
  test('another origin is refused by the gateway (Node) and cannot read anything from a page', async ({ page, harness }) => {
    const refused = await harness.gatewayRequest('/v1/projects?limit=100', { origin: harness.otherOrigin });
    expect(refused.status).toBe(403);
    expect(refused.json().error).toBe('hosted_origin_required');
    expect(refused.headers['access-control-allow-origin']).toBeUndefined();
    expect(refused.text).not.toContain(harness.seed.projectId);
    const sameSite = await harness.gatewayRequest('/v1/projects?limit=100', { origin: `https://${'reigh.test'}.evil.test:${harness.originPort}` });
    expect(sameSite.status).toBe(403);
    const plainHttp = await harness.gatewayRequest('/v1/projects?limit=100', { origin: harness.origin.replace('https:', 'http:') });
    expect(plainHttp.status).toBe(403);

    // A page on another origin: the browser may send the request, but the page can read nothing back.
    await page.goto(`${harness.otherOrigin}/__blank.html`);
    const outcomes = await page.evaluate(async (base) => {
      const results: Record<string, string> = {};
      try { await fetch(`${base}/v1/projects?limit=100`); results.cors = 'responded'; } catch { results.cors = 'blocked'; }
      try { const response = await fetch(`${base}/v1/projects?limit=100`, { mode: 'no-cors' }); results.noCors = `${response.type}/${response.status}`; } catch { results.noCors = 'blocked'; }
      return results;
    }, harness.gatewayBase);
    expect(outcomes.cors).toBe('blocked');
    expect(['blocked', 'opaque/0']).toContain(outcomes.noCors);
    const fromEvil = harness.audit().filter((entry) => entry.origin === harness.otherOrigin);
    expect(fromEvil.every((entry) => entry.status === 403)).toBe(true);
    // The no-cors request carries no Origin and a foreign Referer: it must not have reached the Runtime either.
    expect(harness.audit().filter((entry) => entry.origin === null && entry.path.startsWith('/v1/projects') && entry.status === 200)).toHaveLength(0);
  });

  test('a rebinding Host is refused on the session routes', async ({ harness }) => {
    const port = harness.gatewayPort;
    for (const host of [`evil.test:${port}`, `127.0.0.1.evil.test:${port}`, '127.0.0.1', 'localhost', `127.0.0.1:${port + 1}`, `[::1]:${port}`, `reigh.test:${port}`]) {
      const refused = await harness.gatewayRequest('/v1/health', { host });
      expect(refused.status, `Host ${host}`).toBe(403);
      expect(refused.json().error).toBe('invalid_host');
    }
    expect((await harness.gatewayRequest('/v1/health', { host: `127.0.0.1:${port}` })).status).toBe(200);
  });

  test('a missing, wrong or truncated capability is refused', async ({ harness }) => {
    const port = harness.gatewayPort;
    const headers = { Origin: harness.origin };
    const other = `/session/${'A'.repeat(43)}/api/runtime/v1/health`;
    for (const requestPath of ['/v1/health', '/api/runtime/v1/health', other, `${harness.gatewayPrefix.replace(/.$/, '')}/v1/health`, '/session//api/runtime/v1/health', `/session/${harness.gatewayPrefix.split('/')[2].slice(0, 20)}/api/runtime/v1/health`]) {
      const response = await rawRequest({ port, path: requestPath, headers });
      expect(response.status, requestPath).toBe(401);
      expect(response.json().error).toBe('session_required');
    }
    const astrid = await rawRequest({ port, path: other.replace('/api/runtime', '/api/astrid'), headers });
    expect(astrid.status).toBe(401);
  });

  test('admin, worker, credential and unlisted routes are refused with the right capability and origin', async ({ harness }) => {
    const refusals: Array<[string, string]> = [
      ['POST', '/v1/credentials'], ['GET', '/v1/credentials'],
      ['POST', '/v1/doctor'], ['GET', '/v1/doctor'], ['POST', '/v1/backup'], ['POST', '/v1/restore'], ['POST', '/v1/export'],
      ['POST', '/v1/realm/tombstone'], ['POST', '/v1/realm/purge'], ['POST', '/v1/realm/recover'],
      ['POST', '/v1/tasks/claim'], ['POST', '/v1/attempts/x/complete'], ['GET', '/v1/executors'], ['POST', '/v1/executors/register'],
      ['POST', '/v1/recovery/x'], ['POST', '/v1/control/local-worker/start'],
      ['DELETE', '/v1/projects/abc'], ['PUT', '/v1/projects'], ['GET', '/v1/health/../doctor'],
      ['GET', '/v1/projects/%2e%2e/doctor'], ['GET', '/v1/projects/a%252fb'], ['GET', '/v1/projects/a%2fb'], ['GET', '//v1/health'],
    ];
    for (const [method, requestPath] of refusals) {
      const response = await harness.gatewayRequest(requestPath, { method, headers: method === 'GET' ? {} : { 'Content-Type': 'application/json' }, body: method === 'GET' ? undefined : '{}' });
      expect(response.status, `${method} ${requestPath}`).toBe(404);
      expect(response.json().error).toBe('route_not_allowed');
    }
    // The gateway answered every one itself (404) and the Runtime is still healthy for allowed routes.
    expect((await harness.runtimeJson('GET', '/v1/projects?limit=1')).status).toBe(200);
  });

  test('browser credentials, a foreign Referer and the Private Network preflight', async ({ harness }) => {
    const withAuthorization = await harness.gatewayRequest('/v1/health', { headers: { Authorization: `Bearer ${harness.productToken}` } });
    expect(withAuthorization.status).toBe(403);
    expect(withAuthorization.json().error).toBe('browser_credentials_forbidden');
    const withCookie = await harness.gatewayRequest('/v1/health', { headers: { Cookie: 'a=b' } });
    expect(withCookie.status).toBe(403);

    // A media-style request without Origin is accepted only from the hosted origin's Referer.
    const asMedia = (referer?: string) => harness.gatewayRequest(`/v1/objects/${encodeURIComponent(harness.seed.image.objectId)}`, { origin: null, headers: referer ? { Referer: referer } : {} });
    expect((await asMedia(`${harness.origin}/`)).status).toBe(200);
    expect((await asMedia(`${harness.otherOrigin}/`)).status).toBe(403);
    expect((await asMedia()).status).toBe(403);
    expect((await harness.gatewayRequest('/v1/projects', { origin: null, method: 'POST', headers: { Referer: `${harness.origin}/`, 'Content-Type': 'application/json' }, body: '{"name":"x"}' })).status).toBe(403);

    const preflight = (origin: string, requestHeaders: string) => harness.gatewayRequest('/v1/projects', {
      method: 'OPTIONS', origin,
      headers: { 'Access-Control-Request-Method': 'POST', 'Access-Control-Request-Headers': requestHeaders, 'Access-Control-Request-Private-Network': 'true' },
    });
    const allowed = await preflight(harness.origin, 'content-type, idempotency-key');
    expect(allowed.status).toBe(204);
    expect(allowed.headers['access-control-allow-private-network']).toBe('true');
    expect(allowed.headers['access-control-allow-origin']).toBe(harness.origin);
    const foreign = await preflight(harness.otherOrigin, 'content-type');
    expect(foreign.status).toBe(403);
    expect(foreign.headers['access-control-allow-private-network']).toBeUndefined();
    expect((await preflight(harness.origin, 'authorization')).status).toBe(403);
    expect((await preflight(harness.origin, 'x-forwarded-for')).status).toBe(403);
  });

  test('from the hosted page, a request carrying an Authorization header cannot be sent', async ({ page, harness }) => {
    await openHostedPage(page, harness);
    const blocked = await page.evaluate(async (base) => {
      try { await fetch(`${base}/v1/projects`, { headers: { Authorization: 'Bearer owner' } }); return 'responded'; } catch { return 'blocked'; }
    }, harness.gatewayBase);
    expect(blocked).toBe('blocked');
  });
});

// ---------------------------------------------------------------------------------------------
// 6. Speed table (reported, never judged)

test('speed table: each step through the gateway against the Runtime directly', async ({ harness }, testInfo) => {
  test.setTimeout(300_000);
  const { projectId, timelineId, image, video, big } = harness.seed;
  const idem = () => randomBytes(8).toString('hex');
  const viaGateway = (pathUnderBase: string, init: { method?: string; headers?: Record<string, string>; body?: Buffer | string } = {}) => harness.gatewayRequest(pathUnderBase, init);
  const viaRuntime = (pathUnderBase: string, init: { method?: string; headers?: Record<string, string>; body?: Buffer | string } = {}) =>
    rawRequest({ port: harness.runtimePort, path: pathUnderBase, method: init.method, headers: { Authorization: `Bearer ${harness.productToken}`, ...init.headers }, body: init.body });
  const sides = { runtime: viaRuntime, gateway: viaGateway } as const;
  const SMALL = 9;
  const jsonHeaders = { 'Content-Type': 'application/json' };

  for (const via of ['runtime', 'gateway'] as const) {
    const call = sides[via];
    await speed.time('handshake (POST)', via, SMALL, async () => {
      const response = await call('/v1/handshake', { method: 'POST', headers: jsonHeaders, body: JSON.stringify({ protocol: 'workspace.v1', client_name: 'journey', client_version: '1', requested_scopes: ['handshake'] }) });
      expect(response.status).toBe(200);
    });
    await speed.time('list projects', via, SMALL, async () => { expect((await call('/v1/projects?limit=100')).status).toBe(200); });
    await speed.time('read timeline (inspect)', via, SMALL, async () => {
      expect((await call(`/v1/projects/${projectId}/timelines/${timelineId}/inspect`, { method: 'POST', headers: jsonHeaders, body: '{}' })).status).toBe(200);
    });
    await speed.time('save timeline (publish revision)', via, SMALL, async () => {
      const head = await currentHead(harness);
      const response = await call(`/v1/projects/${projectId}/timelines/${timelineId}/composition-revisions`, { method: 'POST', headers: { ...jsonHeaders, 'Idempotency-Key': idem() }, body: JSON.stringify(compositionPublication(harness.seed, head, `speed ${via}`, 30)) });
      expect(response.status, response.text).toBe(200);
    });
    await speed.time('image GET (small)', via, SMALL, async () => {
      const response = await call(`/v1/objects/${encodeURIComponent(image.objectId)}`);
      expect(response.status).toBe(200);
    });
    await speed.time('video Range read (64 KiB)', via, SMALL, async () => {
      const response = await call(`/v1/objects/${encodeURIComponent(video.objectId)}`, { headers: { Range: 'bytes=0-65535' } });
      expect(response.status).toBe(206);
    });
    await speed.time(`video full GET (${(video.size / 1048576).toFixed(1)} MB)`, via, SMALL, async () => {
      const response = await call(`/v1/objects/${encodeURIComponent(video.objectId)}`);
      expect(response.status).toBe(200);
    }, video.size);
    // Big transfers: three downloads and two uploads per side. With fewer than 20 samples p95 is the slowest sample.
    let digestOk = true;
    await speed.time('60 MB download', via, 3, async () => {
      const response = await call(`/v1/objects/${encodeURIComponent(big.objectId)}`);
      expect(response.status).toBe(200);
      digestOk &&= response.body.length === BIG_DOWNLOAD_BYTES;
      lastDownload = response.body;
    }, BIG_DOWNLOAD_BYTES);
    expect(digestOk).toBe(true);
    expect(sha256Hex(lastDownload!)).toBe(big.digest);
    lastDownload = undefined;
  }

  // Uploads: a fresh 200 MB body per repetition (the store is content-addressed, so a repeat would dedupe).
  const payload = randomBytes(BIG_UPLOAD_BYTES);
  for (const via of ['runtime', 'gateway'] as const) {
    const call = sides[via];
    const bodies: Array<{ body: Buffer; digest: string }> = [];
    for (let rep = 0; rep < 2; rep++) {
      randomBytes(64).copy(payload, 0);
      bodies.push({ body: Buffer.from(payload), digest: sha256Hex(payload) });
    }
    await speed.time('200 MB upload', via, 2, async (rep) => {
      const response = await call(`/v1/projects/${projectId}/objects`, { method: 'POST', headers: { 'Content-Type': 'application/octet-stream', 'Idempotency-Key': idem(), 'X-Original-Name': `speed-${via}-${rep}.bin` }, body: bodies[rep].body });
      expect(response.status, response.text.slice(0, 300)).toBe(201);
      expect(response.json().data.digest).toBe(bodies[rep].digest);
    }, BIG_UPLOAD_BYTES);
  }

  const table = speed.render();
  console.log(`\n${table}\n`);
  const outDir = testInfo.project.outputDir;
  mkdirSync(outDir, { recursive: true });
  const file = path.join(outDir, 'direct-measurements.json');
  writeFileSync(file, JSON.stringify(speed.toJSON(), null, 2));
  await testInfo.attach('direct-measurements.json', { path: file, contentType: 'application/json' });
  await testInfo.attach('direct-measurements.txt', { body: table, contentType: 'text/plain' });
});
