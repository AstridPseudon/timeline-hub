/**
 * Timeline layout-geometry regression spec.
 *
 * Pixel screenshots drift across machines (fonts, GPU rasterization, subpixel
 * rounding) without the layout actually changing, so they are a poor
 * regression signal for this repo's CI mix. Layout *geometry* — element rects,
 * counts, structural flags — is stable across machines once rounded to a small
 * grid, and it is what actually encodes "did the timeline's shape change".
 * This spec snapshots that geometry for the same four device contexts the
 * other timeline-devices specs cover (desktop, phone, tablet portrait, tablet
 * landscape) and compares it against a committed baseline with a pixel
 * tolerance.
 *
 * To regenerate the baseline after an intentional layout change:
 *
 *   PLAYWRIGHT_TIMELINE_DEVICES=1 \
 *   PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
 *   REGENERATE_LAYOUT_BASELINE=1 \
 *   npx playwright test tests/e2e/timeline/layout-geometry --project=timeline-devices --workers=1
 *
 * That run writes `tests/e2e/timeline/layout-baseline.json` and exits without
 * asserting — eyeball the numbers (preview heights > 150, editArea > 80, etc.)
 * before committing them. Ordinary runs (no `REGENERATE_LAYOUT_BASELINE`)
 * assert the live geometry against the committed file with an ±8px tolerance
 * per dimension (counts and flags must match exactly). On mismatch the failure
 * message prints the live and baseline objects side by side and points back at
 * this command.
 */
import { existsSync, mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { expect, test, type Page } from '@playwright/test';
import {
  CLIP_BODY_SELECTOR,
  EDIT_AREA_SELECTOR,
} from '../../../src/tools/video-editor/lib/timeline-dom.ts';
import {
  BASELINE_CLIPS,
  BASELINE_TRACKS,
  openEditor,
  readFakeRuntimeComposition,
  resetFakeRuntimeBaseline,
} from './support';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BASELINE_PATH = join(__dirname, 'layout-baseline.json');
const REGENERATE = process.env.REGENERATE_LAYOUT_BASELINE === '1';

/** Round to the nearest 4px grid — absorbs subpixel/font rendering drift. */
const GRID = 4;

interface Rect { x: number; y: number; w: number; h: number }

interface GeometrySnapshot {
  viewport: { w: number; h: number };
  rects: {
    preview: Rect | null;
    editArea: Rect | null;
    trackLabelColumn: Rect | null;
    ruler: Rect | null;
    firstClip: Rect | null;
  };
  counts: {
    tracks: number;
    modeUiElements: number;
  };
  flags: {
    armedBarPresent: boolean;
    gutterPadding: string | null;
  };
}

interface Context {
  name: string;
  viewport: { width: number; height: number };
  touch: boolean;
}

const CONTEXTS: Context[] = [
  { name: 'desktop', viewport: { width: 1600, height: 1000 }, touch: false },
  { name: 'phone', viewport: { width: 420, height: 820 }, touch: true },
  { name: 'tabletPortrait', viewport: { width: 834, height: 1194 }, touch: true },
  { name: 'tabletLandscape', viewport: { width: 1180, height: 820 }, touch: true },
];

/** Collect the geometry snapshot from a settled, live editor page. */
async function collectGeometry(page: Page): Promise<GeometrySnapshot> {
  return page.evaluate(({ clipBodySelector, editAreaSelector, grid }) => {
    const snapValue = (value: number) => Math.round(value / grid) * grid;
    const rect = (el: Element | null) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: snapValue(r.x), y: snapValue(r.y), w: snapValue(r.width), h: snapValue(r.height) };
    };

    const preview = document.querySelector('[data-testid="video-editor-preview-surface"]');
    const editArea = document.querySelector(editAreaSelector);
    const trackLabelColumn = document.querySelector('[data-track-id]');
    const ruler = document.querySelector('[data-testid="timeline-ruler"]');
    const firstClip = document.querySelector(clipBodySelector);
    // The touch mode switcher is gone everywhere; none of these may render.
    const removedModeUi = document.querySelectorAll(
      '[data-timeline-mode-switcher], [aria-label="Phone timeline mode bar"], [aria-label="Timeline mode switcher"]',
    );
    const armedBar = document.querySelector('[data-armed-gesture]');

    const gutterPadding = editArea
      ? getComputedStyle(editArea).getPropertyValue('--label-width').trim() || null
      : null;

    return {
      viewport: { w: window.innerWidth, h: window.innerHeight },
      rects: {
        preview: rect(preview),
        editArea: rect(editArea),
        trackLabelColumn: rect(trackLabelColumn),
        ruler: rect(ruler),
        firstClip: rect(firstClip),
      },
      counts: {
        tracks: document.querySelectorAll('[data-track-id]').length,
        modeUiElements: removedModeUi.length,
      },
      flags: {
        armedBarPresent: Boolean(armedBar),
        gutterPadding,
      },
    };
  }, {
    clipBodySelector: CLIP_BODY_SELECTOR as string,
    editAreaSelector: EDIT_AREA_SELECTOR as string,
    grid: GRID,
  });
}

/** ±8px per dimension for rects/viewport; exact match for counts and flags. */
const TOLERANCE_PX = 8;

function diffRect(name: string, actual: Rect | null, expected: Rect | null): string[] {
  const issues: string[] = [];
  if ((actual === null) !== (expected === null)) {
    issues.push(`${name}: presence mismatch (actual=${JSON.stringify(actual)}, expected=${JSON.stringify(expected)})`);
    return issues;
  }
  if (actual === null || expected === null) return issues;
  for (const key of ['x', 'y', 'w', 'h'] as const) {
    if (Math.abs(actual[key] - expected[key]) > TOLERANCE_PX) {
      issues.push(`${name}.${key}: actual=${actual[key]} expected=${expected[key]} (tolerance ${TOLERANCE_PX}px)`);
    }
  }
  return issues;
}

function diffSnapshot(actual: GeometrySnapshot, expected: GeometrySnapshot): string[] {
  const issues: string[] = [];

  for (const key of ['w', 'h'] as const) {
    if (Math.abs(actual.viewport[key] - expected.viewport[key]) > TOLERANCE_PX) {
      issues.push(`viewport.${key}: actual=${actual.viewport[key]} expected=${expected.viewport[key]}`);
    }
  }

  for (const key of Object.keys(actual.rects) as (keyof GeometrySnapshot['rects'])[]) {
    issues.push(...diffRect(`rects.${key}`, actual.rects[key], expected.rects[key]));
  }

  for (const key of Object.keys(actual.counts) as (keyof GeometrySnapshot['counts'])[]) {
    if (actual.counts[key] !== expected.counts[key]) {
      issues.push(`counts.${key}: actual=${actual.counts[key]} expected=${expected.counts[key]}`);
    }
  }

  for (const key of Object.keys(actual.flags) as (keyof GeometrySnapshot['flags'])[]) {
    if (actual.flags[key] !== expected.flags[key]) {
      issues.push(`flags.${key}: actual=${JSON.stringify(actual.flags[key])} expected=${JSON.stringify(expected.flags[key])}`);
    }
  }

  return issues;
}

function readBaseline(): Record<string, GeometrySnapshot> {
  if (!existsSync(BASELINE_PATH)) return {};
  return JSON.parse(readFileSync(BASELINE_PATH, 'utf8'));
}

/**
 * The geometry baseline is only meaningful on *exactly* the known 3-track / 4-clip fixture. The shared
 * `beforeEach` hard reset restores the seed (and verifies it against the pristine fixture); this reads the
 * persisted head back from the Runtime and fails with its own useful message if it is anything else.
 */
async function assertGeometryFixture(): Promise<void> {
  const { config } = await readFakeRuntimeComposition();
  expect(config.tracks, 'geometry fixture: persisted tracks').toEqual(BASELINE_TRACKS);
  expect(config.clips, 'geometry fixture: persisted clips').toEqual(BASELINE_CLIPS);
}

const collected: Record<string, GeometrySnapshot> = {};

test.describe('timeline layout geometry', () => {
  for (const ctx of CONTEXTS) {
    test.describe(ctx.name, () => {
      test.use({
        viewport: ctx.viewport,
        ...(ctx.touch ? { hasTouch: true, isMobile: true, deviceScaleFactor: 2 } : {}),
      });

      test(`${ctx.name}: geometry snapshot ${REGENERATE ? '(regenerating baseline)' : 'matches baseline'}`, async (
        { page },
      ) => {
        test.setTimeout(120_000);

        // Reset here, as the other touch specs do: `support.ts` registers its shared reset hook only for
        // the first spec file a worker loads, so after another file in the same worker this one would
        // read that file's last edit.
        const resetError = await resetFakeRuntimeBaseline();
        expect(resetError, resetError ?? '').toBeNull();
        await assertGeometryFixture();
        await openEditor(page);

        const snapshot = await collectGeometry(page);
        collected[ctx.name] = snapshot;

        if (REGENERATE) {
          // Sanity floor so a broken/blank page can't silently seed a bogus
          // baseline — see the header comment for the eyeball checklist.
          expect(snapshot.rects.editArea?.h ?? 0, JSON.stringify(snapshot)).toBeGreaterThan(80);
          return;
        }

        const baseline = readBaseline();
        const expected = baseline[ctx.name];
        expect(expected, `no baseline entry for "${ctx.name}" in ${BASELINE_PATH}`).toBeTruthy();

        const issues = diffSnapshot(snapshot, expected);
        expect(
          issues,
          'layout changed — if intentional, regenerate tests/e2e/timeline/layout-baseline.json '
            + '(see spec header for the command)\n\n'
            + `actual:\n${JSON.stringify(snapshot, null, 2)}\n\n`
            + `baseline:\n${JSON.stringify(expected, null, 2)}\n\n`
            + `diffs:\n${issues.join('\n')}`,
        ).toEqual([]);
      });
    });
  }

  test.afterAll(() => {
    if (!REGENERATE) return;
    if (Object.keys(collected).length !== CONTEXTS.length) return; // partial run; don't clobber the baseline
    mkdirSync(dirname(BASELINE_PATH), { recursive: true });
    writeFileSync(BASELINE_PATH, `${JSON.stringify(collected, null, 2)}\n`);
  });
});
