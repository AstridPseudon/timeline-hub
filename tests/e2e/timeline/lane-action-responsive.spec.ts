import { expect, test } from '@playwright/test';
import {
  browserEvidencePath,
  collectNetworkIssues,
  collectPageLogs,
  editorUrl,
  publishTranscriptSegments,
  resetFakeRuntimeBaseline,
} from './support';

/**
 * The host-rendered `DataLaneActionDescriptor` chrome at the narrowest width, where every layout
 * branch is exercised at once: the sticky `min-w-20` action rail (it grows to fit its one-line label)
 * must not hide the lane's chips, the fixed portal menu must clamp to the viewport, and the trigger
 * must own the hit. The rail's width does not depend on the viewport and the only width-dependent host
 * branch is below 640 px, so wider viewports add no distinct layout coverage; menu keyboard handling
 * and invocation are `DataLaneList.test.tsx`.
 */
const VIEWPORT = { width: 390, height: 844 } as const;

// The shared reset hook in support.ts registers for the first spec file a worker loads only, so a spec resets
// for itself: before, so it starts pristine, and after, so its seeded transcript never reaches the next spec.
test.beforeEach(async () => {
  expect(await resetFakeRuntimeBaseline()).toBeNull();
});
test.afterEach(async () => {
  expect(await resetFakeRuntimeBaseline()).toBeNull();
});

test('keeps the host lane-action affordance visible at phone width', async ({ page }, testInfo) => {
  await page.setViewportSize(VIEWPORT);
  const logs = collectPageLogs(page);
  const networkIssues = collectNetworkIssues(page);
  // Segments inside the carrier clip's trimmed range, so the lane has chips under the action rail.
  await publishTranscriptSegments([
    { start: 0.5, end: 2.5, text: 'Fixture segment one' },
    { start: 2.5, end: 4.5, text: 'Fixture segment two' },
  ]);
  await page.addInitScript(() => localStorage.removeItem('astrid.dev-extensions.disabled'));
  await page.goto(editorUrl(), { waitUntil: 'domcontentloaded', timeout: 45_000 });

  const row = page.locator('[data-lane-kind="astrid.transcript"]');
  const trigger = row.getByTestId('data-lane-actions-trigger');
  await expect(trigger).toBeVisible({ timeout: 20_000 });
  await page.locator('.timeline-canvas-edit-area').evaluate((scroller) => {
    scroller.scrollTop = scroller.scrollHeight;
  });
  await expect(trigger).toBeInViewport();
  const declaredActions = Number(/^Actions \((\d+)\)$/.exec((await trigger.textContent())?.trim() ?? '')?.[1]);
  expect(declaredActions, 'the trigger announces how many actions the lane declares').toBeGreaterThan(0);

  const triggerBox = await trigger.boundingBox();
  const scrollerBox = await page.locator('.timeline-canvas-edit-area').boundingBox();
  expect(triggerBox).not.toBeNull();
  expect(scrollerBox).not.toBeNull();
  expect(triggerBox!.x).toBeGreaterThanOrEqual(Math.max(0, scrollerBox!.x) - 1);
  expect(
    triggerBox!.x + triggerBox!.width,
    JSON.stringify({ triggerBox, scrollerBox, viewport: VIEWPORT }),
  ).toBeLessThanOrEqual(
    Math.min(VIEWPORT.width, scrollerBox!.x + scrollerBox!.width) + 1,
  );

  // The rail is an opaque, full-width strip that ends at the trigger, and the chip beside it stays
  // readable instead of running underneath.
  const rail = row.getByTestId('data-lane-action-rail');
  const chip = row.getByTestId('transcript-lane-chip').first();
  await expect(chip).toBeVisible();
  const [railBox, chipBox, railBackground] = await Promise.all([
    rail.boundingBox(),
    chip.boundingBox(),
    rail.evaluate((element) => getComputedStyle(element).backgroundColor),
  ]);
  expect(railBox).not.toBeNull();
  expect(chipBox).not.toBeNull();
  expect(railBackground).not.toBe('rgba(0, 0, 0, 0)');
  expect(railBox!.width).toBeGreaterThanOrEqual(79);
  expect(railBox!.x).toBeLessThanOrEqual(triggerBox!.x);
  expect(
    railBox!.x + railBox!.width,
    JSON.stringify({ railBox, triggerBox, viewport: VIEWPORT }),
  ).toBeGreaterThanOrEqual(triggerBox!.x + triggerBox!.width);
  const visibleChipLeft = Math.max(chipBox!.x, scrollerBox!.x);
  const visibleChipRight = Math.min(chipBox!.x + chipBox!.width, railBox!.x);
  expect(
    visibleChipRight - visibleChipLeft,
    JSON.stringify({ chipBox, railBox, triggerBox, viewport: VIEWPORT }),
  ).toBeGreaterThan(20);
  expect(visibleChipRight).toBeLessThanOrEqual(triggerBox!.x - 1);

  // The trigger owns the hit at its own center.
  const triggerCenter = {
    x: triggerBox!.x + triggerBox!.width / 2,
    y: triggerBox!.y + triggerBox!.height / 2,
  };
  const hit = await page.evaluate(({ x, y }) => {
    const target = document.elementFromPoint(x, y);
    return {
      trigger: target?.closest('[data-testid="data-lane-actions-trigger"]') !== null,
      target: target?.outerHTML.slice(0, 300) ?? null,
    };
  }, triggerCenter);
  expect(hit.trigger, JSON.stringify({ hit, triggerBox, scrollerBox })).toBe(true);

  // The menu lists exactly the declared actions, every one enabled and inside the viewport.
  await trigger.click();
  const menu = page.getByRole('menu', { name: 'Transcript actions' });
  await expect(menu).toBeVisible();
  const menuItems = menu.getByRole('menuitem');
  await expect(menuItems).toHaveCount(declaredActions);
  for (const item of await menuItems.all()) {
    await expect(item).toBeVisible();
    await expect(item).toBeEnabled();
    const itemBox = await item.boundingBox();
    expect(itemBox, await item.textContent() ?? 'menu item').not.toBeNull();
    expect(itemBox!.x).toBeGreaterThanOrEqual(0);
    expect(itemBox!.x + itemBox!.width).toBeLessThanOrEqual(VIEWPORT.width + 1);
  }
  const menuBox = await menu.boundingBox();
  expect(menuBox).not.toBeNull();
  expect(menuBox!.x).toBeGreaterThanOrEqual(0);
  expect(menuBox!.x + menuBox!.width).toBeLessThanOrEqual(VIEWPORT.width + 1);
  await menuItems.first().focus();
  await expect(menuItems.first()).toBeFocused();
  await page.keyboard.press('ArrowDown');
  await expect(menuItems.nth(1)).toBeFocused();
  await page.screenshot({ path: browserEvidencePath(testInfo, 'chrome-acceptance/24-lane-actions-phone.png'), fullPage: true });
  // A failed load shows up twice: as the browser's generic console line (filtered here) and as the
  // http / requestfailed entry, which is asserted below with no exception.
  expect(logs.filter((line) => !line.includes('Failed to load resource:')), [...new Set(logs)].join(' | ')).toEqual([]);
  expect(networkIssues, [...new Set(networkIssues)].join(' | ')).toEqual([]);
});
