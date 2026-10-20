/**
 * Shared support for the direct journey (Plan A): the Chromium resolution, the worker-scoped fixtures, and the App
 * helpers that drive the hosted page. Moved out of direct-journey.spec.ts without changes (card F2-A).
 */
import { chromium, expect, test as base, type Browser, type Page, type Request } from '@playwright/test';
import { existsSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { DirectHarness, DOOR_PORT, startDirectHarness } from './harness.ts';
import type { TimelineConfig } from '../../../../src/tools/video-editor/types/index.ts';
import type { TimelineDraftRecord } from '../../../../src/tools/video-editor/data/timelineDraftIndexedDb.ts';
import type { OutboxRecord } from '../../../../src/tools/video-editor/commands/commitOutbox.ts';

export const UI = {
  status: '[data-testid="runtime-connection-status"]',
  panel: '[data-testid="runtime-not-connected"]',
  copySetup: 'Copy setup steps for your agent',
  copySteps: 'Copy steps for your agent',
  connect: 'Connect',
  reload: 'Reload',
};

/** The workspace route a visitor opens on the hosted origin. `/` itself is the public landing page in the WEB build (src/app/routes.tsx:77). */
export const APP_ENTRY_ROUTE = '/tools/video-editor';

function resolveChromium(): string | undefined {
  if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) return process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  if (existsSync(chromium.executablePath())) return chromium.executablePath();
  // The installed Playwright may expect a newer browser build than the one in the image; use what is there.
  const browsers = process.env.PLAYWRIGHT_BROWSERS_PATH ?? '/opt/pw-browsers';
  const found = existsSync(browsers) ? readdirSync(browsers).filter((name) => /^chromium-\d+$/.test(name)).sort().pop() : undefined;
  const candidate = found ? path.join(browsers, found, 'chrome-linux', 'chrome') : undefined;
  return candidate && existsSync(candidate) ? candidate : undefined;
}

export const test = base.extend<object, { harness: DirectHarness; browser: Browser }>({
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

export async function currentHead(harness: DirectHarness): Promise<string> {
  const timelines = await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions?limit=1`);
  return timelines.body.items.find((item: any) => item.is_current_head).revision_id;
}

export async function waitForAudit(harness: DirectHarness, predicate: (entry: ReturnType<DirectHarness['audit']>[number]) => boolean, timeoutMs = 3000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const hit = harness.audit().filter(predicate);
    if (hit.length || Date.now() > deadline) return hit;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
}

/** Opens the App at the hosted origin with nothing in the URL and returns the requests it made to the door. */
export async function openApp(page: Page, harness: DirectHarness) {
  const doorRequests: string[] = [];
  page.on('request', (request) => { if (request.url().startsWith(`http://127.0.0.1:${DOOR_PORT}/`)) doorRequests.push(`${request.method()} ${request.url()}`); });
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}`);
  return doorRequests;
}

export const expectConnected = (page: Page) => expect(page.locator(UI.status)).toHaveAttribute('data-state', 'connected');

/** The editor's first track-name field: the smallest real edit the App offers on the seeded timeline. */
export const firstTrackName = (page: Page) => page.getByRole('textbox', { name: 'Track name' }).first();

/** Waits for the editor to show the seeded project's timeline (the editor picks the only project by itself). */
export async function openSeededTimeline(page: Page, harness: DirectHarness) {
  await expect(page.getByRole('combobox', { name: 'Select project' })).toContainText(harness.seed.projectName);
  await expect(page.getByRole('combobox', { name: 'Select timeline' })).toBeVisible();
  await expect(firstTrackName(page)).toBeVisible();
}

/** Opens the production embedded canonical ShotEditorView from the parent editor's shot-group label. */
export async function openEmbeddedCanonicalShot(page: Page, occurrenceId: string, shotName: string) {
  const label = page.locator('[data-shot-group-key]').filter({ hasText: shotName }).first();
  await expect(label).toBeVisible();
  await label.dblclick();
  const dialog = page.getByRole('dialog');
  await expect(dialog.locator(`[data-canonical-occurrence-id="${occurrenceId}"]`)).toBeVisible();
  return dialog;
}

/** The visible native header input inside an embedded ShotEditorView.
 * The mounted timeline also contains track labels and combobox inputs, so the
 * production desktop header width identifies the shot-name field precisely.
 */
export const embeddedShotNameInput = (dialog: import('@playwright/test').Locator) => (
  dialog.locator('input[class*="w-[200px]"]:visible').first()
);

export async function editFirstTrackName(page: Page, name: string) {
  const field = firstTrackName(page);
  await field.fill(name);
  await field.press('Enter');
  await field.blur();
}

/** Hold command delivery before the Runtime sees it; persisted request identity remains product-owned. */
export async function holdCommandRequests(page: Page) {
  const commits = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
  const requests: Request[] = [];
  let release!: (send: boolean) => void;
  const gate = new Promise<boolean>((resolve) => { release = resolve; });
  const intercept = async (route: import('@playwright/test').Route) => {
    if (route.request().method() !== 'POST') return route.fallback();
    requests.push(route.request());
    const send = await gate;
    // Reload may have already cancelled the held browser request.
    await (send ? route.continue() : route.abort('connectionreset')).catch(() => {});
  };
  await page.route(commits, intercept);
  return {
    requests,
    async release(send = false) {
      await page.unroute(commits, intercept);
      release(send);
    },
  };
}

/**
 * Holds every save of a composition revision in flight, so the Runtime never receives it and an edit stays an unsaved
 * draft by construction. The editor autosaves 500 ms after an edit, so without this a restart that follows the edit
 * only keeps the draft when it happens to win that race. Returns the release (later saves go through).
 */
export async function holdTimelineSaves(page: Page) {
  const saves = /\/timelines\/[^/]+\/composition-revisions$/;
  await page.route(saves, (route) => (route.request().method() === 'POST' ? new Promise<void>(() => {}) : route.fallback()));
  return () => page.unroute(saves);
}

export async function revisionBody(harness: DirectHarness, revisionId: string) {
  return (await harness.runtimeJson('GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}/composition-revisions/${revisionId}`)).body;
}

/** Read the real browser outbox without creating, claiming or modifying an owner. */
export async function commandOutboxes(page: Page, timelineId: string): Promise<OutboxRecord[]> {
  // Playwright's by-value result decoder intentionally omits __proto__ keys;
  // carry the browser's JSON bytes across the inspection boundary instead.
  const encoded = await page.evaluate(async (id) => {
    if (!(await indexedDB.databases()).some((db) => db.name === 'astrid.command-outbox')) return '[]';
    return new Promise<string>((resolve, reject) => {
      const opening = indexedDB.open('astrid.command-outbox');
      opening.onerror = () => reject(opening.error);
      opening.onsuccess = () => {
        const db = opening.result;
        const tx = db.transaction('owners', 'readonly');
        const read = tx.objectStore('owners').getAll();
        tx.oncomplete = () => { db.close(); resolve(JSON.stringify((read.result as OutboxRecord[]).filter((record) => record.scope.timelineId === id))); };
        tx.onabort = () => { db.close(); reject(tx.error); };
      };
    });
  }, timelineId);
  return JSON.parse(encoded) as OutboxRecord[];
}

/** Actual pointerdown/move/drop: scale comes from the two rendered parent clips. */
export async function dragTimelineClip(page: Page, clipId: string, referenceId: string, from: number, to: number, referenceAt: number, beforeDrop?: () => void | Promise<void>) {
  const clip = page.locator(`.clip-action[data-clip-id="${clipId}"]`).first();
  const reference = page.locator(`.clip-action[data-clip-id="${referenceId}"]`).first();
  await expect(clip).toBeVisible();
  await expect(reference).toBeVisible();
  const box = await clip.boundingBox();
  const other = await reference.boundingBox();
  if (!box || !other || referenceAt === from) throw new Error('Cannot measure timeline clip scale');
  const pixelsPerSecond = (other.x - box.x) / (referenceAt - from);
  expect(pixelsPerSecond).toBeGreaterThan(0);
  const x = box.x + Math.min(box.width / 2, 24);
  const y = box.y + box.height / 2;
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x + (to - from) * pixelsPerSecond, y, { steps: 12 });
  await beforeDrop?.();
  await page.mouse.up();
}

/** Read the legacy one-slot draft without creating or modifying recovery state. */
export async function timelineDraft(page: Page, timelineId: string): Promise<(TimelineDraftRecord & { draft: { config?: TimelineConfig } }) | null> {
  return page.evaluate(async (id) => {
    if (!(await indexedDB.databases()).some((db) => db.name === 'astrid.timeline-drafts')) return null;
    return new Promise<(TimelineDraftRecord & { draft: { config?: TimelineConfig } }) | null>((resolve, reject) => {
      const opening = indexedDB.open('astrid.timeline-drafts');
      opening.onerror = () => reject(opening.error);
      opening.onsuccess = () => {
        const db = opening.result;
        const tx = db.transaction('timeline-drafts', 'readonly');
        const read = tx.objectStore('timeline-drafts').get(id);
        tx.oncomplete = () => { db.close(); resolve(read.result ?? null); };
        tx.onabort = () => { db.close(); reject(tx.error); };
      };
    });
  }, timelineId);
}
