import { expect, test } from '@playwright/test';
import { CLIP_BODY_SELECTOR } from '../../../src/tools/video-editor/lib/timeline-dom.ts';
import { openEditor, resetFakeRuntimeBaseline, seedEditorPreferences } from './support';

/**
 * On narrow layouts (single-pane phone, condensed) the right panel floats over the editor. It starts
 * closed there, so the preview and the timeline are what a user sees first; once the user opens it, it
 * must still never sit on top of the timeline toolbar: a covered Zoom button cannot be clicked by a
 * user either, and Playwright's actionability check fails on exactly that.
 */
const VIEWPORTS = [
  { name: 'condensed desktop', width: 500, height: 760, touch: false },
  { name: 'phone', width: 390, height: 844, touch: true },
] as const;

for (const viewport of VIEWPORTS) {
  test.describe(viewport.name, () => {
    test.use({
      viewport: { width: viewport.width, height: viewport.height },
      ...(viewport.touch ? { hasTouch: true, isMobile: true, deviceScaleFactor: 2 } : {}),
    });

    test('starts with the right panel closed, so the preview and the timeline are reachable', async ({ page }) => {
      test.setTimeout(150_000);
      await resetFakeRuntimeBaseline();
      await openEditor(page);

      const dock = page.getByTestId('video-editor-right-panel-dock');
      await expect(dock).toHaveAttribute('data-responsive', 'true');
      await expect(dock).toHaveAttribute('data-open', 'false');

      // Nothing floats over the preview, the ruler or the first clip: each one is the topmost element
      // at its own centre, so a tap there reaches it.
      for (const selector of [
        '[data-testid="video-editor-preview-surface"]',
        '[data-testid="timeline-ruler"]',
        '[data-clip-id="clip-hero"]',
      ]) {
        const target = page.locator(selector).first();
        await expect(target, selector).toBeVisible();
        const reachable = await target.evaluate((element) => {
          const box = element.getBoundingClientRect();
          const top = document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
          return top !== null && element.contains(top);
        });
        expect(reachable, `${selector} is not covered`).toBe(true);
      }
    });

    test('Zoom in and Zoom out stay clickable while the right panel is open', async ({ page }) => {
      test.setTimeout(150_000);
      await resetFakeRuntimeBaseline();
      await seedEditorPreferences(page, { selectedRightPanelId: 'host:properties' });
      await openEditor(page);

      const dock = page.getByTestId('video-editor-right-panel-dock');
      await expect(dock).toHaveAttribute('data-responsive', 'true');
      await expect(dock).toHaveAttribute('data-open', 'true');

      const zoomIn = page.getByRole('button', { name: 'Zoom in timeline' });
      const zoomOut = page.getByRole('button', { name: 'Zoom out timeline' });
      const dockBox = await dock.boundingBox();
      const zoomInBox = await zoomIn.boundingBox();
      const zoomOutBox = await zoomOut.boundingBox();
      expect(dockBox && zoomInBox && zoomOutBox).toBeTruthy();
      expect(dockBox!.y, 'dock starts below the toolbar').toBeGreaterThanOrEqual(zoomInBox!.y + zoomInBox!.height);
      expect(dockBox!.y, 'dock starts below the toolbar').toBeGreaterThanOrEqual(zoomOutBox!.y + zoomOutBox!.height);

      // Actionability fails with "intercepts pointer events" if anything covers the button.
      const contentWidth = () => page.locator('.timeline-canvas-edit-area').evaluate((element) => element.scrollWidth);
      const before = await contentWidth();
      await zoomIn.click();
      await expect.poll(contentWidth).toBeGreaterThan(before);
      const zoomedIn = await contentWidth();
      await zoomOut.click();
      await expect.poll(contentWidth).toBeLessThan(zoomedIn);
    });
  });
}

/**
 * On touch the create tools (new text, new effect, new animation) live in shell chrome that never scrolls:
 * the playback row on the phone's single-pane layout, the toolbar's mode-switcher slot on tablet. They are
 * on screen the moment the editor opens, fully inside the viewport, on top of whatever is at their centre,
 * and over no part of the timeline.
 */
const TOUCH_DEVICES = [
  { name: 'phone', width: 390, height: 844, host: 'playback-row' },
  { name: 'tablet portrait', width: 834, height: 1194, host: 'toolbar' },
  { name: 'tablet landscape', width: 1180, height: 820, host: 'toolbar' },
] as const;
const CREATE_TOOL_LABELS = ['New text at playhead', 'Create new effect', 'Create animation'] as const;

for (const device of TOUCH_DEVICES) {
  test.describe(`create tools on ${device.name}`, () => {
    test.use({
      viewport: { width: device.width, height: device.height },
      hasTouch: true,
      isMobile: true,
      deviceScaleFactor: 2,
    });

    test('create tools reachable without scrolling', async ({ page }) => {
      test.setTimeout(150_000);
      await resetFakeRuntimeBaseline();
      await openEditor(page);

      const cluster = page.getByTestId('timeline-tool-buttons');
      await expect(cluster).toHaveCount(1);
      await expect(cluster).toHaveAttribute('data-create-tools-host', device.host);

      // Nothing was scrolled to get here.
      const scroll = await page.evaluate(() => ({
        editArea: document.querySelector('.timeline-canvas-edit-area')?.scrollTop ?? -1,
        window: window.scrollY,
      }));
      expect(scroll, 'edit area and window are unscrolled at open').toEqual({ editArea: 0, window: 0 });

      const boxes = await page.evaluate(({ labels, clipSelector }) => {
        const intersects = (a: DOMRect, b: DOMRect) => (
          a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top
        );
        const covered: Array<{ name: string; rect: DOMRect }> = [];
        const note = (name: string, element: Element | null) => {
          if (element) covered.push({ name, rect: element.getBoundingClientRect() });
        };
        note('ruler', document.querySelector('[data-testid="timeline-ruler"]'));
        note('edit area', document.querySelector('.timeline-canvas-edit-area'));
        document.querySelectorAll(clipSelector).forEach((clip) => note('clip', clip));
        document.querySelectorAll('[data-pane-control]').forEach((tab) => {
          const rect = tab.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) note('pane tab', tab);
        });

        return labels.map((label) => {
          const button = document.querySelector(`[aria-label="${label}"]`);
          if (!button) return { label, missing: true as const };
          const rect = button.getBoundingClientRect();
          const top = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
          return {
            label,
            missing: false as const,
            w: rect.width,
            h: rect.height,
            background: getComputedStyle(button).backgroundColor,
            inViewport: rect.left >= 0 && rect.top >= 0
              && rect.right <= window.innerWidth && rect.bottom <= window.innerHeight,
            topmost: top !== null && button.contains(top),
            overlaps: covered.filter((entry) => intersects(rect, entry.rect)).map((entry) => entry.name),
          };
        });
      }, { labels: [...CREATE_TOOL_LABELS], clipSelector: CLIP_BODY_SELECTOR as string });

      for (const box of boxes) {
        expect(box.missing, `${box.label} is rendered`).toBe(false);
        if (box.missing) continue;
        expect(box.w, `${box.label} width`).toBeGreaterThanOrEqual(40);
        expect(box.h, `${box.label} height`).toBeGreaterThanOrEqual(40);
        expect(box.background, `${box.label} is painted with its tone, not left transparent`).not.toBe('rgba(0, 0, 0, 0)');
        expect(box.inViewport, `${box.label} lies inside the viewport`).toBe(true);
        expect(box.topmost, `${box.label} is the topmost element at its centre`).toBe(true);
        expect(box.overlaps, `${box.label} covers nothing of the timeline or the pane tabs`).toEqual([]);
      }

      // The toolbar keeps its shape with the tools in it.
      const groups = await page.evaluate(() => {
        const history = document.querySelector('[data-toolbar-group="history"]')?.getBoundingClientRect();
        const view = document.querySelector('[data-toolbar-group="view"]')?.getBoundingClientRect();
        const toolbar = document.querySelector('[data-toolbar-group="history"]')?.parentElement?.getBoundingClientRect();
        return history && view && toolbar
          ? { historyTop: history.top, viewTop: view.top, toolbarHeight: toolbar.height }
          : null;
      });
      expect(groups, 'toolbar groups are rendered').not.toBeNull();
      // History and view never split across lines: they share a top.
      expect(Math.abs(groups!.historyTop - groups!.viewTop), 'history and view share a line').toBeLessThan(2);
      if (device.name === 'phone') {
        // The phone's toolbar stays one 44px-button line; the tools went to the playback row instead.
        expect(groups!.toolbarHeight, 'phone toolbar stays one line').toBeLessThanOrEqual(56);
      }

      // A tap on New text places a clip at the playhead, and still nothing scrolled.
      const clipCount = () => page.locator(CLIP_BODY_SELECTOR as string).count();
      const clipsBefore = await clipCount();
      const textBox = await page.getByRole('button', { name: 'New text at playhead' }).boundingBox();
      expect(textBox).not.toBeNull();
      await page.touchscreen.tap(textBox!.x + textBox!.width / 2, textBox!.y + textBox!.height / 2);
      await expect.poll(clipCount).toBeGreaterThan(clipsBefore);
      const after = await page.evaluate(() => ({
        editArea: document.querySelector('.timeline-canvas-edit-area')?.scrollTop ?? -1,
        window: window.scrollY,
      }));
      expect(after, 'adding text did not scroll anything').toEqual({ editArea: 0, window: 0 });
    });
  });
}
