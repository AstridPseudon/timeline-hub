import { expect, test, type Page } from '@playwright/test';
import { editorPath, resetFakeRuntimeBaseline } from './timeline/support';

const COMPOSED_URL = editorPath({ params: { timelineOverlayCanary: '1', transcriptLaneFixture: 'render-matrix' } });

const viewports = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'phone', width: 390, height: 844 },
] as const;

test.describe.configure({ mode: 'serial' });

async function initializeLocalMode(page: Page): Promise<void> {
  await page.addInitScript(() => {
    localStorage.removeItem('astrid.dev-extensions.disabled');
  });
}

async function stabilizeTimeline(page: Page): Promise<void> {
  const stabilizingCss = `
      *, *::before, *::after {
        animation: none !important;
        caret-color: transparent !important;
        transition: none !important;
      }
      .timeline-scroll { scrollbar-width: none !important; }
      .timeline-scroll::-webkit-scrollbar { display: none !important; }
    `;
  // Local bridge discovery can perform one startup navigation while an editor
  // route settles. Retry the idempotent freeze against the final document.
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      await page.addStyleTag({ content: stabilizingCss });
      await page.evaluate(async () => {
        for (const video of document.querySelectorAll('video')) video.pause();
        await document.fonts.ready;
        await Promise.all([...document.images].map((image) => image.decode().catch(() => undefined)));
      });
      break;
    } catch (error) {
      if (attempt === 2 || !String(error).includes('Execution context was destroyed')) throw error;
      await page.waitForLoadState('domcontentloaded');
      await page.waitForTimeout(200);
    }
  }
  const surface = page.locator('.timeline-wrapper');
  await expect(surface).toBeVisible();
  await page.locator('.timeline-canvas-edit-area').evaluate((element) => {
    element.scrollLeft = 0;
    element.scrollTop = element.scrollHeight;
  });
  await page.waitForTimeout(100);
}

async function expectTimelineSnapshot(page: Page, name: string): Promise<void> {
  await stabilizeTimeline(page);
  await expect(page.locator('.timeline-wrapper')).toHaveScreenshot(name, {
    animations: 'disabled',
    caret: 'hide',
    scale: 'css',
    threshold: 0.2,
    maxDiffPixelRatio: 0.005,
  });
}

async function openComposedEditor(page: Page): Promise<void> {
  expect(await resetFakeRuntimeBaseline()).toBeNull();
  await initializeLocalMode(page);
  const response = await page.goto(COMPOSED_URL, { waitUntil: 'domcontentloaded', timeout: 45_000 });
  expect(response?.ok()).toBe(true);
  await expect(page.locator('[data-lane-kind="astrid.transcript"]')).toBeVisible({ timeout: 30_000 });
}

for (const viewport of viewports) {
  test(`matches the composed extension timeline at ${viewport.name} size`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await openComposedEditor(page);
    await expectTimelineSnapshot(page, `composed-${viewport.name}.png`);
  });
}
