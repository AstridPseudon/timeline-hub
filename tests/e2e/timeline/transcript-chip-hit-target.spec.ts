import { expect, test } from '@playwright/test';
import { editorUrl } from './support.ts';

const EXPECTED_CAPTIONS = 4;
const EXPECTED_RENDERED_SEGMENTS = 5;
const EDITOR_URL = editorUrl({ params: { transcriptLaneFixture: 'render-matrix' } });

test.describe('transcript overlap hit targets', () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  test('keeps four overlapping Unicode chips readable and independently selectable', async ({ page }, testInfo) => {
    test.setTimeout(90_000);
    await page.addInitScript(() => localStorage.removeItem('astrid.dev-extensions.disabled'));
    await page.goto(EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 45_000 });

    const transcriptRow = page.locator('[data-lane-kind="astrid.transcript"]');
    await expect(transcriptRow).toBeVisible({ timeout: 30_000 });
    await page.locator('.timeline-canvas-edit-area').evaluate((scroller) => {
      scroller.scrollTop = scroller.scrollHeight;
    });
    const chips = transcriptRow.getByTestId('transcript-lane-occurrence');
    // The matrix includes one intentional whitespace-only source segment to
    // prove the materializer's empty-text filter. The lane keeps that source
    // visible as a diagnostic `(no text)` chip; the four meaningful Unicode
    // chips below are the hit-target contract under test.
    await expect(chips).toHaveCount(EXPECTED_RENDERED_SEGMENTS, { timeout: 20_000 });

    const chipData = await chips.evaluateAll((elements) => elements.map((element) => ({
      id: element.getAttribute('data-item-id'),
      label: element.getAttribute('aria-label'),
      rect: (() => {
        const { left, right, top, bottom, width, height } = element.getBoundingClientRect();
        return { left, right, top, bottom, width, height };
      })(),
      style: {
        top: (element as HTMLElement).style.top,
        height: (element as HTMLElement).style.height,
      },
    })));
    expect(chipData.every(({ id, label }) => Boolean(id && label && label.includes('Transcript segment: ')))).toBe(true);
    const diagnosticChipData = chipData.filter(({ label }) => label?.includes('(no text)'));
    expect(diagnosticChipData).toHaveLength(1);
    const meaningfulChipData = chipData.filter(({ label }) => !label?.includes('(no text)'));
    expect(meaningfulChipData).toHaveLength(EXPECTED_CAPTIONS);
    expect(chipData.every(({ rect }) => rect.width > 0 && rect.height > 0)).toBe(true);
    const rowBox = await transcriptRow.boundingBox();
    expect(rowBox).not.toBeNull();
    expect(chipData.every(({ rect }) => (
      rect.top >= rowBox!.y - 1
      && rect.bottom <= rowBox!.y + rowBox!.height + 1
    ))).toBe(true);
    expect(new Set(meaningfulChipData.map(({ style }) => `${style.top}:${style.height}`)).size).toBeGreaterThan(1);
    for (let leftIndex = 0; leftIndex < meaningfulChipData.length; leftIndex += 1) {
      for (let rightIndex = leftIndex + 1; rightIndex < meaningfulChipData.length; rightIndex += 1) {
        const left = meaningfulChipData[leftIndex]!.rect;
        const right = meaningfulChipData[rightIndex]!.rect;
        const horizontallyOverlaps = left.left < right.right && right.left < left.right;
        if (!horizontallyOverlaps) continue;
        expect(
          left.bottom <= right.top + 0.5 || right.bottom <= left.top + 0.5,
          `overlapping interval hit targets must not overlap vertically: ${JSON.stringify({ left, right })}`,
        ).toBe(true);
      }
    }

    for (const { label } of chipData) {
      // A chip shows its text in a hoverable tooltip while it is hovered or focused, and that tooltip can sit over
      // the next chip. Dismiss it the way a reader does (Escape, pointer away) so the click lands on the chip itself.
      await page.keyboard.press('Escape');
      await page.mouse.move(0, 0);
      await expect(page.getByRole('tooltip')).toHaveCount(0);
      // A later chip can sit over the middle of an earlier one (the diagnostic chip lies under its neighbour), so each
      // chip is clicked at its own left edge, which no later chip covers.
      await page.getByLabel(label!, { exact: true }).click({ position: { x: 2, y: 8 } });
      await expect(page.getByLabel(label!, { exact: true })).toHaveAttribute('aria-pressed', 'true');
    }
    await testInfo.attach('transcript-overlap-hit-targets', {
      body: await page.screenshot(),
      contentType: 'image/png',
    });
  });
});
