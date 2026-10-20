/**
 * Extension timeline overlays and keybindings, across desktop (mouse) and tablet (touch).
 *
 * This is the real-browser half of the overlay contract. The jsdom suites bind the host, marker
 * layer, pointer arbitration and pinch refusal to DOM contracts; this spec drives the REAL
 * scene-phase-markers fixture extension end to end against a live dev server:
 *
 *   - the overlay mounts while the extension is enabled and unmounts when it is disabled,
 *   - passive timeline gestures (clip select/drag, ruler scrub) behave identically while
 *     overlays are mounted but unclaimed,
 *   - marker drag commits exactly once and lands on the frame grid,
 *   - marker content geometry tracks `startLeft + time * pps` across zoom and scroll (the
 *     ruler-strip translateX(-scrollLeft) contract),
 *   - drag-to-edge auto-scrolls the edit area,
 *   - disabling the extension MID-DRAG terminates the session cleanly (no commit, no stuck
 *     gesture owner, editor stays interactive), by mouse on desktop only (the tablet touch-teardown
 *     step went with upstream 8efc4cd6, which retired the dock and the mode bar it drove),
 *   - a second-finger pinch is refused while a marker owns the gesture and works again once the
 *     claim is released (touch marker-versus-pinch), and a tap on a clip then opens its sheet,
 *   - a keybinding and the command palette both run the extension's command against the live
 *     playhead and the write survives the Runtime round trip.
 *
 * One command: `npm run test:e2e:timeline` (boots the dev server + fake Runtime
 * via `playwright.config.ts` webServer entries).
 */
import { expect, test, type BrowserContext, type Page } from '@playwright/test';
import { CLIP_BODY_SELECTOR } from '../../../src/tools/video-editor/lib/timeline-dom.ts';
import {
  EDITOR_URL,
  collectPageLogs,
  countSelectedClips,
  createTouchInput,
  openEditor,
  pickFreeDraggableClip,
  publishFakeRuntimeComposition,
  readFakeRuntimeComposition,
  resetFakeRuntimeBaseline,
  type TouchInput,
} from './support';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SCENE_PHASE_EXTENSION_ID = 'haus.astrid.scene-phase-markers';
const MARK_PHASE_COMMAND_LABEL = 'Mark Scene Phase at Playhead';
const EDIT_AREA_SELECTOR = '.timeline-canvas-edit-area';
const STRIP_SELECTOR = '[data-testid="timeline-extension-ruler-overlay-strip"]';
const DISABLE_TOGGLE_SELECTOR = `[data-video-editor-dev-local-toggle="${SCENE_PHASE_EXTENSION_ID}"]`;
const SCENE_MARKER_LAYER_SELECTOR =
  `[data-testid="timeline-marker-layer"][data-marker-layer-key="${SCENE_PHASE_EXTENSION_ID}:scene-markers-overlay"]`;

/** Stable marker fixture rendered on the ruler by the scene-phase-markers extension. */
const MARKERS = [
  { id: 'e2e-marker-a', time: 1 },
  { id: 'e2e-marker-b', time: 3 },
  { id: 'e2e-marker-c', time: 5 },
];

function sceneMarkerLayer(page: Page) {
  return page.locator(SCENE_MARKER_LAYER_SELECTOR);
}

/** The seeded scene markers, wherever they render; other extensions' layers carry markers of their own. */
function seededSceneMarkers(page: Page) {
  return page.locator(MARKERS.map((marker) => `[data-marker-id="${marker.id}"]`).join(', '));
}

// ---------------------------------------------------------------------------
// Harness helpers
// ---------------------------------------------------------------------------

/**
 * Seed the scene-phase-markers data on top of the seeded timeline, as a second writer would: a new head
 * published to the Runtime with `config.app[<extension id>].sceneMarkers` set. The shared hard reset
 * replaces the whole composition (dropping `app`), so seeding must always happen after it.
 */
async function seedSceneMarkers(markers: Array<{ id: string; time: number }> = MARKERS): Promise<string | null> {
  try {
    await publishFakeRuntimeComposition(({ config }) => {
      config.app = {
        ...(config.app ?? {}),
        [SCENE_PHASE_EXTENSION_ID]: { sceneMarkers: markers },
      };
    });
    return null;
  } catch (error) {
    return `[seed] ${(error as Error).message}`;
  }
}

/**
 * Open the editor. Clears the dev-local disable store and editor zoom preference once per page
 * session so each test starts from a known state while a later Vite reload preserves the disabled
 * state that the test intentionally established.
 */
async function openMarkerEditor(page: Page): Promise<void> {
  await page.addInitScript(() => {
    try {
      // This helper creates a fresh route visit independently of openEditor.
      // Mark setup complete so first-run onboarding cannot cover the editor.
      window.localStorage.setItem('astrid-setup-complete', 'true');
      const initializedKey = 'astrid.e2e.extension-overlays.initialized';
      if (window.sessionStorage.getItem(initializedKey) !== '1') {
        window.localStorage.removeItem('astrid.dev-extensions.disabled');
        window.localStorage.removeItem('video-editor:preferences:demo-timeline');
        window.sessionStorage.setItem(initializedKey, '1');
      }
    } catch {
      // storage unavailable — defaults apply
    }
  });
  await page.goto(EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 45_000 });
  await page.getByRole('button', { name: 'Render', exact: true }).waitFor({ state: 'visible', timeout: 45_000 });
}

interface RulerMetrics {
  /** Pixels per second, measured from two adjacent ruler labels. */
  pps: number;
  /** Ruler content origin (`startLeft`), derived from the time-0 label. */
  startLeft: number;
  scrollLeft: number;
  scrollWidth: number;
  clientWidth: number;
}

/**
 * Derive the timeline's live time→pixel geometry from the ruler labels
 * (`translateX(tick.left + 6)` on each major label) instead of importing
 * internals. Both label and marker coordinates live in the same
 * ruler-translated content space, so `startLeft + time * pps` is directly
 * comparable to a marker's strip-relative content x.
 */
async function rulerMetrics(page: Page): Promise<RulerMetrics> {
  return page.evaluate((editAreaSelector) => {
    const parse = (text: string): number => {
      // Touch rulers label whole seconds (`m:ss`), pointer rulers hundredths (`m:ss.cc`).
      const match = /^(\d+):(\d\d)(?:\.(\d\d))?$/.exec(text);
      if (!match) return 0;
      return Number(match[1]) * 60 + Number(match[2]) + Number(match[3] ?? 0) / 100;
    };
    const ruler = document.querySelector('[data-testid="timeline-ruler"]');
    const rulerX = ruler?.getBoundingClientRect().x ?? 0;
    const scrollArea = document.querySelector(editAreaSelector);
    const scrollLeft = scrollArea?.scrollLeft ?? 0;
    const labels = Array.from(document.querySelectorAll('[data-testid="timeline-ruler"] span'))
      .map((el) => ({ text: el.textContent?.trim() ?? '', x: el.getBoundingClientRect().x }))
      .filter((label) => /^\d+:\d\d(?:\.\d\d)?$/.test(label.text))
      .sort((a, b) => a.x - b.x);

    let pps = 0;
    let startLeft = 0;
    if (labels.length >= 2) {
      const first = labels[0];
      const second = labels[1];
      const dt = parse(second.text) - parse(first.text);
      const dx = second.x - first.x;
      pps = dt > 0 ? dx / dt : 0;
      startLeft = first.x - rulerX + scrollLeft - 6 - parse(first.text) * pps;
    }

    return {
      pps,
      startLeft,
      scrollLeft,
      scrollWidth: scrollArea?.scrollWidth ?? 0,
      clientWidth: scrollArea?.clientWidth ?? 0,
    };
  }, EDIT_AREA_SELECTOR);
}

/** Count of major `m:ss.ff` labels currently visible on the ruler. */
async function rulerLabelCount(page: Page): Promise<number> {
  return page.evaluate(() => {
    const ruler = document.querySelector('[data-testid="timeline-ruler"]');
    if (!ruler) return 0;
    return Array.from(ruler.querySelectorAll('span'))
      .filter((el) => /^\d+:\d\d(?:\.\d\d)?$/.test(el.textContent?.trim() ?? ''))
      .length;
  });
}

/**
 * Resolve after the browser has painted `count` more frames. Gesture streams and settle checks wait
 * on the browser's own frame clock instead of a wall-clock sleep.
 */
async function nextFrames(page: Page, count = 2): Promise<void> {
  await page.evaluate(async (frames) => {
    for (let index = 0; index < frames; index += 1) {
      await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
    }
  }, count);
}

/**
 * Marker content x in the ruler strip's own coordinate space. The strip is
 * translated `translateX(-scrollLeft)` by the host, so this value is
 * scroll-independent and must equal `startLeft + time * pps`.
 */
async function markerContentX(page: Page, markerId: string): Promise<number | null> {
  return page.evaluate(({ stripSelector, id }) => {
    const marker = document.querySelector(`[data-marker-id="${id}"]`);
    const strip = document.querySelector(stripSelector);
    if (!marker || !strip) return null;
    return marker.getBoundingClientRect().x - strip.getBoundingClientRect().x;
  }, { stripSelector: STRIP_SELECTOR, id: markerId });
}

/** Marker viewport x (page-relative), or null when not rendered. */
async function markerViewportX(page: Page, markerId: string): Promise<number | null> {
  return page.evaluate((id) => {
    const marker = document.querySelector(`[data-marker-id="${id}"]`);
    return marker ? marker.getBoundingClientRect().x : null;
  }, markerId);
}

async function markerTime(page: Page, markerId: string): Promise<number | null> {
  const value = await page.getAttribute(`[data-marker-id="${markerId}"]`, 'data-marker-time');
  return value === null ? null : Number(value);
}

/** Wait until `observe()` reports a time within `tolerance` of `expected`; a miss reports the last value. */
async function expectTimeToReach(
  observe: () => Promise<number | null>,
  expected: number,
  message: string,
  tolerance = 0.06,
): Promise<void> {
  await expect.poll(async () => {
    const current = await observe();
    return current !== null && Math.abs(current - expected) <= tolerance ? expected : current;
  }, { message, timeout: 15_000 }).toBe(expected);
}

/** The marker's rendered `data-marker-time` reaches `expected` (± tolerance). */
function waitForDomMarkerTime(page: Page, markerId: string, expected: number): Promise<void> {
  return expectTimeToReach(() => markerTime(page, markerId), expected, `marker ${markerId} DOM time`);
}

/** The scene markers in the Runtime's persisted head composition (`config.app`), not the editor's copy. */
async function readPersistedSceneMarkers(): Promise<Array<{ id: string; time: number }>> {
  const { config } = await readFakeRuntimeComposition();
  const app = config.app?.[SCENE_PHASE_EXTENSION_ID];
  return Array.isArray(app?.sceneMarkers) ? app.sceneMarkers : [];
}

/** Read the playhead's ruler-content x position, including the label gutter. */
async function readPlayheadTransformX(page: Page): Promise<number | null> {
  return page.evaluate(() => {
    const playhead = document.querySelector('[data-testid="timeline-playhead"]');
    const transform = playhead?.getAttribute('style') ?? '';
    const match = /translateX\(([\d.]+)px\)/.exec(transform);
    return match ? Number(match[1]) : null;
  });
}

function waitForPersistedMarkerTime(markerId: string, expected: number): Promise<void> {
  return expectTimeToReach(
    async () => (await readPersistedSceneMarkers()).find((entry) => entry.id === markerId)?.time ?? null,
    expected,
    `persisted marker ${markerId} time`,
  );
}

/** Mouse drag on a ruler marker: down at its center, move `dx`, release. */
async function dragMarkerBy(page: Page, markerId: string, dx: number): Promise<void> {
  const marker = page.locator(`[data-marker-id="${markerId}"]`);
  await marker.waitFor({ state: 'visible', timeout: 15_000 });
  const box = await marker.boundingBox();
  if (!box) {
    throw new Error(`marker ${markerId} has no bounding box`);
  }
  const cx = box.x + box.width / 2;
  const cy = box.y + box.height / 2;
  await page.mouse.move(cx, cy);
  await page.mouse.down();
  await page.mouse.move(cx + dx, cy, { steps: 8 });
  await page.mouse.up();
}

/** Touch drag on a ruler marker via raw CDP touch input. */
async function touchDragMarker(
  touch: TouchInput,
  page: Page,
  markerId: string,
  dx: number,
): Promise<void> {
  const marker = page.locator(`[data-marker-id="${markerId}"]`);
  await marker.waitFor({ state: 'visible', timeout: 15_000 });
  const box = await marker.boundingBox();
  if (!box) {
    throw new Error(`marker ${markerId} has no bounding box`);
  }
  const x = box.x + box.width / 2;
  const y = box.y + box.height / 2;
  await touch.touchDrag(x, y, x + dx, y, { steps: 14 });
}

type CdpSession = Awaited<ReturnType<BrowserContext['newCDPSession']>>;

/**
 * Finger 1: touchStart on the marker, then cross the 4 px activation threshold so the marker owns
 * the gesture. Returns the point the finger rests at; the finger stays down until the caller ends it.
 */
async function touchClaimMarker(
  cdp: CdpSession,
  page: Page,
  markerId: string,
): Promise<{ x: number; y: number }> {
  const marker = page.locator(`[data-marker-id="${markerId}"]`);
  await marker.waitFor({ state: 'visible', timeout: 15_000 });
  const box = await marker.boundingBox();
  if (!box) {
    throw new Error(`marker ${markerId} has no bounding box`);
  }
  const x = box.x + box.width / 2;
  const y = box.y + box.height / 2;
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y }] });
  for (let i = 1; i <= 3; i += 1) {
    await cdp.send('Input.dispatchTouchEvent', {
      type: 'touchMove',
      touchPoints: [{ x: x + i * 6, y }],
    });
    await nextFrames(page, 1);
  }
  await expect(marker).toHaveAttribute('data-marker-dragging', 'true', { timeout: 5_000 });
  return { x: x + 18, y };
}

/**
 * Touch marker-versus-pinch: finger 1 claims a marker drag, then finger 2 attempts a two-finger
 * pinch on the edit area. The host's claim must make the pinch handler refuse to initialize or
 * continue, so the scale must not change.
 */
async function touchDragMarkerThenPinch(
  context: BrowserContext,
  page: Page,
  markerId: string,
  editAreaCenterY: number,
): Promise<void> {
  const cdp = await context.newCDPSession(page);
  // A pinch before this may have zoomed the marker out of view; a finger can only take a
  // marker it can reach, so bring it a third of the way into the timeline first.
  await page.evaluate(([selector, id]) => {
    const area = document.querySelector(selector) as HTMLElement | null;
    const marker = document.querySelector(`[data-marker-id="${id}"]`);
    if (!area || !marker) return;
    const areaRect = area.getBoundingClientRect();
    const markerRect = marker.getBoundingClientRect();
    if (markerRect.left < areaRect.left || markerRect.right > areaRect.right) {
      area.scrollLeft += markerRect.left - areaRect.left - areaRect.width / 3;
    }
  }, [EDIT_AREA_SELECTOR, markerId] as const);
  await page.waitForTimeout(200);
  const finger1 = await touchClaimMarker(cdp, page, markerId);
  const areaCenterX = await page.evaluate((selector) => {
    const rect = document.querySelector(selector)?.getBoundingClientRect();
    return rect ? rect.x + rect.width / 2 : 0;
  }, EDIT_AREA_SELECTOR);

  // Finger 2: a pinch attempt on the edit area while the marker owns the claim.
  await cdp.send('Input.dispatchTouchEvent', {
    type: 'touchStart',
    touchPoints: [finger1, { x: areaCenterX - 40, y: editAreaCenterY }],
  });
  for (let i = 1; i <= 8; i += 1) {
    const spread = 40 + i * 8;
    await cdp.send('Input.dispatchTouchEvent', {
      type: 'touchMove',
      touchPoints: [finger1, { x: areaCenterX - spread, y: editAreaCenterY }],
    });
    await nextFrames(page, 1);
  }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await nextFrames(page, 2);
}

/** Scroll the edit area back to the left edge (content origin). */
async function resetScrollLeft(page: Page): Promise<void> {
  await page.evaluate((selector) => {
    const area = document.querySelector(selector);
    if (area) area.scrollLeft = 0;
  }, EDIT_AREA_SELECTOR);
  await expect.poll(() => page.evaluate(
    (selector) => document.querySelector(selector)?.scrollLeft ?? -1,
    EDIT_AREA_SELECTOR,
  )).toBe(0);
}

/** The scene-phase-markers row's enable/disable toggle in the Extension Manager dialog. */
function sceneExtensionToggle(page: Page) {
  return page.locator(DISABLE_TOGGLE_SELECTOR);
}

/**
 * Open the Extension Manager the way a user does: the right dock's Extensions tab, then Manage. The
 * dock must be open (it is by default on desktop widths). The tab only becomes selectable while an
 * enabled extension contributes a panel, which the fixture catalog's overlay-layers extension does.
 */
async function openExtensionManager(page: Page): Promise<void> {
  const tab = page.getByRole('tab', { name: 'Extensions' });
  await tab.click({ timeout: 8_000 });
  await expect(tab).toHaveAttribute('aria-selected', 'true');
  await page.getByRole('button', { name: 'Manage extensions' }).click({ timeout: 8_000 });
  await sceneExtensionToggle(page).waitFor({ state: 'attached', timeout: 10_000 });
}

/** Close the Extension Manager dialog and give the editor back its pointer events. */
async function closeExtensionManager(page: Page): Promise<void> {
  await page.getByRole('dialog', { name: 'Extensions' }).getByRole('button', { name: 'Close' }).click({ timeout: 8_000 });
  await expect(sceneExtensionToggle(page)).toHaveCount(0);
}

/** Flip the scene-phase-markers toggle exactly once: retrying a toggle is state-reversing. */
async function flipSceneExtensionToggle(page: Page, expectedLabel: string): Promise<void> {
  const toggle = sceneExtensionToggle(page);
  await toggle.evaluate((element) => {
    (element as HTMLElement).click();
  });
  await expect(toggle).toHaveAttribute('aria-label', expectedLabel, { timeout: 5_000 });
}

/**
 * Disable the scene-phase-markers extension while a marker owns the pointer. A real second pointer
 * cannot reach the manager: the dragging pointer holds capture on the marker button (which retargets
 * every pointer event) and the manager is a modal dialog, so this walks the same path with DOM-level
 * clicks (dock tab -> Manage -> toggle). That still exercises the real store -> page memo ->
 * lifecycle -> host teardown path. Desktop only: the touch editor mounts no dock.
 */
async function disableExtensionMidDrag(page: Page): Promise<void> {
  const domClick = (selector: string) => page.locator(selector).evaluate((element) => {
    (element as HTMLElement).click();
  });
  await domClick('[role="tab"][data-surface-tab="extensions"]');
  const manage = page.locator('button[aria-label="Manage extensions"]');
  await manage.waitFor({ state: 'attached', timeout: 10_000 });
  await manage.evaluate((element) => {
    (element as HTMLElement).click();
  });
  await sceneExtensionToggle(page).waitFor({ state: 'attached', timeout: 10_000 });
  await flipSceneExtensionToggle(page, `Enable ${SCENE_PHASE_EXTENSION_ID}`);
}

// The shared reset hook in support.ts registers for the first spec file a worker loads only, so this spec
// resets after each test itself: its saved markers and seeded heads must not reach the next spec.
test.afterEach(async () => {
  expect(await resetFakeRuntimeBaseline()).toBeNull();
});

// ---------------------------------------------------------------------------
// Desktop (mouse)
// ---------------------------------------------------------------------------

test.describe('timeline extension overlays (desktop)', () => {
  test.use({ viewport: { width: 1600, height: 1000 } });

  test('overlay lifecycle, passive parity, geometry, drag, auto-scroll, disable mid-drag', async ({ page }, testInfo) => {
    test.setTimeout(240_000);

    const logs: string[] = [];
    const resetError = await resetFakeRuntimeBaseline();
    if (resetError) logs.push(resetError);
    const seedError = await seedSceneMarkers();
    if (seedError) logs.push(seedError);
    logs.push(...collectPageLogs(page));

    const shot = (name: string) => page.screenshot({
      path: testInfo.outputPath(`desktop-${name}.png`),
      animations: 'disabled',
      timeout: 20_000,
    });

    // --- 1. the overlay follows the EXTENSION's enablement, not a URL param ---
    // The overlay host mounts whenever an enabled dev-local extension declares a `timelineOverlay`
    // contribution. Disabling that extension unmounts its layer.
    await openEditor(page);
    await test.step('host mounts with an enabled overlay extension (no URL param)', async () => {
      const markerLayer = sceneMarkerLayer(page);
      await expect(markerLayer).toBeVisible({ timeout: 20_000 });
      await expect(markerLayer).toHaveAttribute('data-marker-count', '3');
    });

    await test.step('disabling the overlay extension unmounts its layer', async () => {
      await openExtensionManager(page);
      await flipSceneExtensionToggle(page, `Enable ${SCENE_PHASE_EXTENSION_ID}`);
      await expect(sceneMarkerLayer(page)).toHaveCount(0, { timeout: 10_000 });
      await expect(seededSceneMarkers(page)).toHaveCount(0);
      // Re-enable so the next step starts from a known state.
      await flipSceneExtensionToggle(page, `Disable ${SCENE_PHASE_EXTENSION_ID}`);
      await closeExtensionManager(page);
    });

    // --- 2. enabled extension + seeded markers mount on the ruler ---------
    await openMarkerEditor(page);
    const markerLayer = sceneMarkerLayer(page);
    await expect(markerLayer).toBeVisible({ timeout: 20_000 });
    await expect(markerLayer).toHaveAttribute('data-marker-count', '3');
    await expect(page.locator('[data-marker-id="e2e-marker-a"]')).toBeVisible();
    await expect(page.locator('[data-marker-id="e2e-marker-b"]')).toBeVisible();
    await expect(page.locator('[data-marker-id="e2e-marker-c"]')).toBeVisible();
    await shot('mounted');

    // --- 3. passive parity: no overlay claim, gestures unchanged ----------
    await test.step('clip select works while overlays are mounted but unclaimed', async () => {
      await page.locator(`${EDIT_AREA_SELECTOR} ${CLIP_BODY_SELECTOR}`).first().click({ timeout: 8_000 });
      expect(await countSelectedClips(page)).toBeGreaterThanOrEqual(1);
    });

    await test.step('clip drag works while overlays are mounted but unclaimed', async () => {
      // Pick a clip with free space to its right: the timeline snaps an
      // overlapping drop back to the clip's origin, so a blind +48px drag on
      // a packed neighbour would measure the packing rule, not the gesture.
      const freeClip = await pickFreeDraggableClip(page);
      expect(freeClip, 'expected a draggable clip').not.toBeNull();
      const clip = page.locator(`${EDIT_AREA_SELECTOR} ${CLIP_BODY_SELECTOR}[data-clip-id="${freeClip!.id}"]`);
      const before = await clip.boundingBox();
      if (!before) throw new Error('no clip to drag');
      await page.mouse.move(before.x + before.width / 2, before.y + before.height / 2);
      await page.mouse.down();
      await page.mouse.move(before.x + before.width / 2 + 48, before.y + before.height / 2, { steps: 6 });
      await page.mouse.up();
      await expect.poll(
        async () => Math.abs(((await clip.boundingBox())?.x ?? before.x) - before.x),
        { message: `clip x moved from ${before.x}`, timeout: 15_000 },
      ).toBeGreaterThan(25);
    });

    await test.step('ruler scrub (playhead drag) works while overlays are mounted but unclaimed', async () => {
      const beforeTransform = await page.getAttribute('[data-testid="timeline-playhead"]', 'style');
      const ruler = await page.locator('[data-testid="timeline-ruler"]').boundingBox();
      if (!ruler) throw new Error('no ruler');
      await page.mouse.move(ruler.x + 220, ruler.y + 15);
      await page.mouse.down();
      await page.mouse.move(ruler.x + 340, ruler.y + 15, { steps: 5 });
      await page.mouse.up();
      await expect.poll(
        () => page.getAttribute('[data-testid="timeline-playhead"]', 'style'),
        { message: 'playhead moved by the ruler scrub', timeout: 15_000 },
      ).not.toBe(beforeTransform);
    });
    await shot('passive');

    // --- 4. marker geometry at default zoom --------------------------------
    const metrics0 = await rulerMetrics(page);
    await test.step('ruler metrics are measurable', async () => {
      expect(metrics0.pps, `pps=${metrics0.pps}`).toBeGreaterThan(10);
    });

    await test.step('marker content x equals startLeft + time * pps', async () => {
      for (const marker of MARKERS) {
        const contentX = await markerContentX(page, marker.id);
        const expected = metrics0.startLeft + marker.time * metrics0.pps;
        expect(
          contentX !== null && Math.abs(contentX - expected),
          `${marker.id} contentX=${contentX} expected=${expected}`,
        ).toBeLessThan(4);
      }
    });

    // --- 5. marker drag commits once, on the frame grid --------------------
    await test.step('marker drag commits a frame-snapped time', async () => {
      // +2s at the live pps → exactly 2s, frame-exact at any fps.
      const dx = Math.round(2 * metrics0.pps);
      await dragMarkerBy(page, 'e2e-marker-a', dx);
      const expected = 1 + 2;
      await waitForDomMarkerTime(page, 'e2e-marker-a', expected);
      await waitForPersistedMarkerTime('e2e-marker-a', expected);
    });
    await shot('dragged');

    // --- 6. scale + scroll geometry ----------------------------------------
    await test.step('zoom in: marker content x tracks the new pps', async () => {
      const zoomIn = page.locator('button[aria-label="Zoom in timeline"]').first();
      for (let i = 0; i < 4; i += 1) {
        await zoomIn.click({ timeout: 5_000 });
      }
      await expect.poll(
        async () => (await rulerMetrics(page)).pps,
        { message: `pps after zooming in from ${metrics0.pps}`, timeout: 15_000 },
      ).toBeGreaterThan(metrics0.pps * 2);
      const metrics1 = await rulerMetrics(page);
      for (const marker of MARKERS) {
        const currentTime = await markerTime(page, marker.id);
        const contentX = await markerContentX(page, marker.id);
        const expected = metrics1.startLeft + (currentTime ?? marker.time) * metrics1.pps;
        expect(
          contentX !== null && Math.abs(contentX - expected),
          `${marker.id} contentX=${contentX} expected=${expected} at pps=${metrics1.pps}`,
        ).toBeLessThan(4);
      }
      // Zoomed far enough that the content overflows the edit area (scrollable).
      expect(metrics1.scrollWidth, `scrollWidth=${metrics1.scrollWidth} clientWidth=${metrics1.clientWidth}`)
        .toBeGreaterThan(metrics1.clientWidth + 100);
    });

    await test.step('scroll: marker viewport x shifts by -scrollLeft, content x is stable', async () => {
      const before = await markerContentX(page, 'e2e-marker-b');
      const viewportBefore = await markerViewportX(page, 'e2e-marker-b');
      const scrollDelta = 200;
      await page.evaluate(({ selector, delta }) => {
        const area = document.querySelector(selector);
        if (area) area.scrollLeft = delta;
      }, { selector: EDIT_AREA_SELECTOR, delta: scrollDelta });
      await expect.poll(
        async () => (await rulerMetrics(page)).scrollLeft,
        { message: 'edit area scrollLeft', timeout: 15_000 },
      ).toBeGreaterThanOrEqual(scrollDelta - 2);
      // The marker strip is translated on the same frame the scroll lands.
      await expect.poll(
        async () => {
          const viewportAfter = await markerViewportX(page, 'e2e-marker-b');
          return viewportAfter !== null && viewportBefore !== null
            ? Math.abs(viewportAfter - viewportBefore + scrollDelta)
            : null;
        },
        { message: `marker viewport x ${viewportBefore} shifts by -${scrollDelta}`, timeout: 15_000 },
      ).toBeLessThan(4);

      // Content x is scroll-independent.
      const afterContent = await markerContentX(page, 'e2e-marker-b');
      expect(afterContent !== null && Math.abs(afterContent - (before ?? 0)), `${before} -> ${afterContent}`).toBeLessThan(2);
    });

    // --- 7. drag-to-edge auto-scroll ---------------------------------------
    await test.step('dragging a marker into the edge zone auto-scrolls the edit area', async () => {
      const area = await page.evaluate((selector) => {
        const rect = document.querySelector(selector)?.getBoundingClientRect();
        return rect ? { right: rect.right, top: rect.top, height: rect.height } : null;
      }, EDIT_AREA_SELECTOR);
      if (!area) throw new Error('no edit area');
      const marker = page.locator('[data-marker-id="e2e-marker-c"]');
      const box = await marker.boundingBox();
      if (!box) throw new Error('marker-c has no bounding box');
      const startX = box.x + box.width / 2;
      const startY = box.y + box.height / 2;
      const beforeScroll = await page.evaluate((selector) => document.querySelector(selector)?.scrollLeft ?? 0, EDIT_AREA_SELECTOR);

      await page.mouse.move(startX, startY);
      await page.mouse.down();
      // Drag into the 40px right-edge zone, then hold while rAF auto-scrolls.
      await page.mouse.move(area.right - 10, startY, { steps: 10 });
      await expect.poll(
        () => page.evaluate((selector) => document.querySelector(selector)?.scrollLeft ?? 0, EDIT_AREA_SELECTOR),
        { message: `scrollLeft from ${beforeScroll} while held at the edge`, timeout: 15_000 },
      ).toBeGreaterThan(beforeScroll + 20);
      await page.mouse.up();

      // The marker followed the scrolled content and the release committed it past its start.
      await expect.poll(
        async () => (await readPersistedSceneMarkers()).find((entry) => entry.id === 'e2e-marker-c')?.time ?? null,
        { message: 'persisted marker-c time after the edge drag', timeout: 15_000 },
      ).toBeGreaterThan(5);
    });
    await shot('autoscroll');

    // --- 8. disable mid-drag ------------------------------------------------
    await test.step('disabling the extension mid-drag terminates the session cleanly', async () => {
      // Auto-scroll moved marker C, and the earlier geometry step moved A near
      // B. Reseed/reload so the disable step cannot hit A's overlapping target
      // when it intends to exercise B's drag lifecycle.
      const reseedError = await seedSceneMarkers();
      if (reseedError) throw new Error(reseedError);
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 45_000 });
      await expect(sceneMarkerLayer(page)).toBeVisible({ timeout: 20_000 });
      await expect(sceneMarkerLayer(page)).toHaveAttribute('data-marker-count', '3');

      // Bring the view back to the content origin so the marker is clickable.
      await resetScrollLeft(page);
      const marker = page.locator('[data-marker-id="e2e-marker-b"]');
      await expect(marker).toBeVisible({ timeout: 10_000 });

      await nextFrames(page, 3);
      await resetScrollLeft(page);
      const box = await marker.boundingBox();
      if (!box) throw new Error('marker-b has no bounding box');
      const cx = box.x + box.width / 2;
      const cy = box.y + box.height / 2;
      const hit = await page.evaluate(({ x, y }) => {
        const target = document.elementFromPoint(x, y);
        return {
          markerId: target?.closest<HTMLElement>('[data-marker-id]')?.getAttribute('data-marker-id') ?? null,
          target: target?.outerHTML.slice(0, 300) ?? null,
        };
      }, { x: cx, y: cy });
      expect(hit.markerId, JSON.stringify({ hit, box })).toBe('e2e-marker-b');

      await page.mouse.move(cx, cy);
      await page.mouse.down();
      await page.mouse.move(cx + 12, cy, { steps: 3 }); // cross the 4px activation threshold
      await expect(marker).toHaveAttribute('data-marker-dragging', 'true', { timeout: 5_000 });

      // Disable while the marker owns the claim → host teardown cancels the session.
      await disableExtensionMidDrag(page);
      await page.mouse.move(cx + 24, cy, { steps: 3 });
      await page.mouse.up();

      await expect(sceneMarkerLayer(page)).toHaveCount(0, { timeout: 10_000 });
      await expect(seededSceneMarkers(page)).toHaveCount(0);
      expect(logs.filter((line) => line.startsWith('[pageerror]')), [...new Set(logs)].join(' | ')).toEqual([]);
      // The torn-down session committed nothing: the Runtime still holds the seeded markers.
      expect(await readPersistedSceneMarkers()).toEqual(MARKERS);

      // The editor itself is still interactive — the gesture owner was released.
      await closeExtensionManager(page);
      await page.locator(`${EDIT_AREA_SELECTOR} ${CLIP_BODY_SELECTOR}`).first().click({ timeout: 8_000 });
      expect(await countSelectedClips(page)).toBeGreaterThanOrEqual(1);
    });
    await shot('disabled');
  });

  test('B key marks a phase at the live playhead: scrub, then mark', async ({ page }, testInfo) => {
    test.setTimeout(180_000);

    // Capture logs by reference: collectPageLogs registers page listeners on
    // the SAME array we assert against, so the final assertion is not vacuous.
    const logs: string[] = [];
    const resetError = await resetFakeRuntimeBaseline();
    if (resetError) logs.push(resetError);
    // resetFakeRuntimeBaseline preserves config.app, so explicitly clear any
    // scene markers a previous spec left in the Runtime's persisted config.
    const clearError = await seedSceneMarkers([]);
    if (clearError) logs.push(clearError);
    logs.push(...collectPageLogs(page));

    const shot = (name: string) => page.screenshot({
      path: testInfo.outputPath(`desktop-bkey-${name}.png`),
      animations: 'disabled',
      timeout: 20_000,
    });

    // Start clean: no seeded markers. The overlay host is mounted, so the
    // marker layer exists but carries 0 markers.
    await openMarkerEditor(page);
    const markerLayer = sceneMarkerLayer(page);
    await expect(markerLayer).toBeVisible({ timeout: 20_000 });
    await expect(markerLayer).toHaveAttribute('data-marker-count', '0');

    // Focus the owning editor shell explicitly. Clicking a non-focusable clip
    // surface does not guarantee the key event target is inside the scoped
    // shell, which is required for instance-owned shortcuts.
    await page.locator(`${EDIT_AREA_SELECTOR} ${CLIP_BODY_SELECTOR}`).first().click({ timeout: 8_000 });
    await page.locator('[data-testid="timeline-ruler"]').evaluate((ruler) => {
      ruler.closest<HTMLElement>('[tabindex="-1"]')?.focus({ preventScroll: true });
    });
    await expect.poll(() => page.evaluate(() => {
      const active = document.activeElement;
      const shell = document.querySelector('[data-testid="timeline-ruler"]')
        ?.closest<HTMLElement>('[tabindex="-1"]');
      return Boolean(active && shell?.contains(active));
    })).toBe(true);

    // Scrub the ruler to a NONZERO playhead: the canvas publishes it into
    // the provider-owned timeline view store through handleSetTime. The B
    // command must read that published value — proving the host→store→
    // command path, not a defaulted 0s marker.
    const ruler = await page.locator('[data-testid="timeline-ruler"]').boundingBox();
    if (!ruler) throw new Error('no ruler');
    const initialPlayheadX = await readPlayheadTransformX(page);
    if (initialPlayheadX === null) throw new Error('playhead has no translateX position');
    // The composed marker layers own the ruler's top 20px. Scrub through the
    // host-owned bottom strip so the gesture reaches the playhead surface. The
    // pointer-down must also be right of the label gutter (the zero-time
    // playhead transform); starting inside it never reaches the ruler handler.
    const scrubY = ruler.y + ruler.height - 3;
    await page.mouse.move(ruler.x + initialPlayheadX + 40, scrubY);
    await page.mouse.down();
    await page.mouse.move(ruler.x + initialPlayheadX + 380, scrubY, { steps: 8 });
    await page.mouse.up();
    await expect.poll(
      async () => {
        const scrubbed = await readPlayheadTransformX(page);
        return scrubbed === null ? null : scrubbed - initialPlayheadX;
      },
      { message: `playhead transform from ${initialPlayheadX}px after the scrub`, timeout: 15_000 },
    ).toBeGreaterThan(40);

    // Press B: the command must read the playhead from the provider-owned
    // timeline view store (renderer-independent) and write a marker at the
    // scrubbed time, NOT at 0s.
    await page.keyboard.press('b');
    await expect(markerLayer).toHaveAttribute('data-marker-count', '1', { timeout: 10_000 });
    await expect(markerLayer.locator('[data-marker-id]')).toHaveCount(1);
    await expect(markerLayer.locator('[data-marker-id]').first()).toBeVisible();
    await shot('marked');

    // The marker must be persisted through project-data (the Runtime head's config.app)
    // at the scrubbed time. The editor saves asynchronously, so poll.
    await expect.poll(async () => (await readPersistedSceneMarkers()).length, { timeout: 15_000 }).toBe(1);
    const persisted = await readPersistedSceneMarkers();
    expect(persisted[0]!.time, JSON.stringify(persisted)).toBeGreaterThan(0);

    // The same command from the command palette: it lists the extension's command by its label and
    // runs it against the same live playhead, so a second marker lands at the same time.
    await page.keyboard.press('ControlOrMeta+Shift+P');
    const commandInput = page.getByPlaceholder('Type a command…');
    await expect(commandInput).toBeVisible();
    await commandInput.fill(MARK_PHASE_COMMAND_LABEL);
    await page.getByRole('option', { name: new RegExp(MARK_PHASE_COMMAND_LABEL) }).click();
    await expect(markerLayer).toHaveAttribute('data-marker-count', '2', { timeout: 10_000 });
    await expect.poll(async () => (await readPersistedSceneMarkers()).length, { timeout: 15_000 }).toBe(2);
    const afterPalette = await readPersistedSceneMarkers();
    expect(afterPalette.map((marker) => marker.time), JSON.stringify(afterPalette))
      .toEqual([persisted[0]!.time, persisted[0]!.time]);

    // Reload: the markers must survive the round trip and re-render.
    await page.reload({ waitUntil: 'domcontentloaded', timeout: 45_000 });
    await expect(sceneMarkerLayer(page)).toBeVisible({ timeout: 20_000 });
    await expect(sceneMarkerLayer(page)).toHaveAttribute('data-marker-count', '2');
    await expect(sceneMarkerLayer(page).locator('[data-marker-id]')).toHaveCount(2);
    await shot('reloaded');

    expect(logs.filter((line) => line.startsWith('[pageerror]')), [...new Set(logs)].join(' | ')).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// Tablet (touch)
// ---------------------------------------------------------------------------

test.describe('timeline extension overlays (tablet)', () => {
  test.use({
    viewport: { width: 834, height: 1194 },
    hasTouch: true,
    isMobile: true,
    deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
      + ' (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });

  test('touch marker drag, marker-versus-pinch arbitration, then the clip sheet', async ({ context, page }, testInfo) => {
    test.setTimeout(240_000);

    const logs: string[] = [];
    const resetError = await resetFakeRuntimeBaseline();
    if (resetError) logs.push(resetError);
    const seedError = await seedSceneMarkers();
    if (seedError) logs.push(seedError);
    logs.push(...collectPageLogs(page));

    await openMarkerEditor(page);
    const touch = await createTouchInput(context, page);

    const shot = (name: string) => page.screenshot({
      path: testInfo.outputPath(`tablet-${name}.png`),
      animations: 'disabled',
      timeout: 20_000,
    });

    const markerLayer = sceneMarkerLayer(page);
    await expect(markerLayer).toBeVisible({ timeout: 20_000 });
    await expect(markerLayer).toHaveAttribute('data-marker-count', '3');
    await shot('mounted');

    // --- 1. touch marker drag commits once ---------------------------------
    await test.step('touch marker drag commits a frame-snapped time', async () => {
      await expect.poll(() => rulerLabelCount(page), { message: 'ruler labels to derive pps from' })
        .toBeGreaterThanOrEqual(2);
      const metrics = await rulerMetrics(page);
      expect(metrics.pps, `pps=${metrics.pps}`).toBeGreaterThan(10);
      // +2.5s at the live pps → 5.5s, frame-exact at any fps.
      const dx = Math.round(2.5 * metrics.pps);
      await touchDragMarker(touch, page, 'e2e-marker-b', dx);
      await waitForDomMarkerTime(page, 'e2e-marker-b', 5.5);
      await waitForPersistedMarkerTime('e2e-marker-b', 5.5);
    });
    await shot('dragged');

    // --- 2. pinch works while no overlay owns the gesture ------------------
    const editAreaCenterY = await page.evaluate((selector) => {
      const rect = document.querySelector(selector)?.getBoundingClientRect();
      return rect ? rect.top + rect.height / 2 : 0;
    }, EDIT_AREA_SELECTOR);
    const areaCenterX = await page.evaluate((selector) => {
      const rect = document.querySelector(selector)?.getBoundingClientRect();
      return rect ? rect.x + rect.width / 2 : 0;
    }, EDIT_AREA_SELECTOR);
    const clipWidth = () => page.evaluate(
      (clipBodySelector) => document.querySelector(clipBodySelector)?.getBoundingClientRect().width ?? 0,
      CLIP_BODY_SELECTOR as string,
    );

    await test.step('two-finger pinch zooms while no overlay owns the gesture', async () => {
      const before = await clipWidth();
      await touch.pinch(areaCenterX, editAreaCenterY, 50, 130, 12);
      const after = await clipWidth();
      expect(after, `clip width ${before} -> ${after}`).toBeGreaterThan(before * 1.5);
    });

    // --- 3. pinch is refused while a marker owns the gesture ----------------
    await test.step('a second-finger pinch is refused while a marker drag owns the claim', async () => {
      const before = await clipWidth();
      await touchDragMarkerThenPinch(context, page, 'e2e-marker-c', editAreaCenterY);
      const after = await clipWidth();
      expect(
        Math.abs(after - before),
        `clip width ${before} -> ${after} (pinch must be refused during the marker drag)`,
      ).toBeLessThan(1);
    });

    // --- 4. releasing the claim restores pinch ------------------------------
    await test.step('pinch works again once the marker claim is released', async () => {
      const before = await clipWidth();
      await touch.pinch(areaCenterX, editAreaCenterY, 40, 100, 10);
      const after = await clipWidth();
      expect(after, `clip width ${before} -> ${after}`).toBeGreaterThan(before * 1.2);
    });

    // --- 5. the editor is still the touch editor after the drags -------------
    await test.step('after the marker drags the editor rests in browse: a tap on a clip opens its sheet', async () => {
      // Earlier steps moved markers b and c and zoomed the timeline. Reseed and reload so the tap
      // lands on a clip at the content origin.
      const reseedError = await seedSceneMarkers();
      if (reseedError) throw new Error(reseedError);
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 45_000 });
      await expect(markerLayer).toBeVisible({ timeout: 20_000 });
      await expect(markerLayer).toHaveAttribute('data-marker-count', '3');
      await resetScrollLeft(page);

      const clip = await page.locator(`${EDIT_AREA_SELECTOR} ${CLIP_BODY_SELECTOR}`).first().boundingBox();
      if (!clip) throw new Error('no clip to tap');
      await touch.tap(clip.x + clip.width / 2, clip.y + clip.height / 2);
      expect(await countSelectedClips(page)).toBeGreaterThanOrEqual(1);
      await expect(page.getByTestId('timeline-clip-sheet')).toBeVisible({ timeout: 5_000 });
    });

    expect(logs.filter((line) => line.startsWith('[pageerror]')), [...new Set(logs)].join(' | ')).toEqual([]);
    await shot('sheet');
  });
});
