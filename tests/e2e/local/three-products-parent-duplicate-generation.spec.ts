/**
 * Focused source proposal for the existing parent generation-duplication
 * consumer. This deliberately stops at the real refusal boundary while the
 * current cohort has neither a generation-backed Runtime fixture nor a live
 * catalog duplication carrier.
 *
 * The trigger is the production ClipAction context menu. Once the existing
 * catalog producer and fixture are available, the same case should continue
 * through the native prepared-media session and assert the accepted path
 * described below; it must not seed a synthetic MediaSelection or call a
 * command/compiler helper directly.
 */
import { expect, type Page } from '@playwright/test';
import {
  commandOutboxes,
  expectConnected,
  openApp,
  openSeededTimeline,
  test as appTest,
} from './support/app.ts';
import { harnessUnavailableReason, type ThreeProductsSeed } from './support/harness.ts';

const COMMITS = /\/v1\/projects\/[^/]+\/timelines\/[^/]+\/commit$/;
const LEGACY_SAVES = /\/timelines\/[^/]+\/composition-revisions$/;
const CEILING = { timeout: 90_000 };

type Traffic = {
  commits: string[];
  legacySaves: string[];
};

/** The actual UI trigger: right-click a generation-backed timeline clip. */
async function openGenerationDuplicateMenu(page: Page): Promise<{ clipId: string; menuItem: ReturnType<Page['getByText']> }> {
  const clips = page.locator('.clip-action[data-clip-id]');
  const count = await clips.count();
  for (let index = 0; index < count; index += 1) {
    const clip = clips.nth(index);
    const clipId = await clip.getAttribute('data-clip-id');
    if (!clipId) continue;
    await clip.click({ button: 'right' });
    const menuItem = page.getByText('Duplicate generation', { exact: true });
    if (await menuItem.isVisible().catch(() => false)) return { clipId, menuItem };
    await page.keyboard.press('Escape');
  }

  throw new Error(
    'parent generation-duplication journey is blocked: the existing e2e seed has no generation-backed catalog clip; '
    + 'do not add synthetic generationId/mediaSelection fields here. Extend the existing catalog fixture/carrier first.',
  );
}

function observeTraffic(page: Page): Traffic {
  const traffic: Traffic = { commits: [], legacySaves: [] };
  page.on('request', (request) => {
    if (request.method() !== 'POST') return;
    const pathname = new URL(request.url()).pathname;
    if (COMMITS.test(pathname)) traffic.commits.push(pathname);
    if (LEGACY_SAVES.test(pathname)) traffic.legacySaves.push(pathname);
  });
  return traffic;
}

const test = appTest.extend<object, { seed3: ThreeProductsSeed }>({
  seed3: [async ({ harness }, use) => { await use(await harness.seedThreeProducts()); }, { scope: 'worker', timeout: 240_000 }],
});

test.beforeAll(() => {
  const reason = harnessUnavailableReason();
  if (reason) throw new Error(`parent generation-duplication journey cannot run: ${reason}`);
});

test.describe.configure({ mode: 'serial' });

test('M2 parent generation duplication: bounded refusal has no placement or legacy write', async ({ page, harness, seed3 }) => {
  const traffic = observeTraffic(page);
  await openApp(page, harness);
  await expectConnected(page);
  await openSeededTimeline(page, harness);

  const trigger = await openGenerationDuplicateMenu(page);
  await trigger.menuItem.click();

  // Current source truth: duplicateGenerationAsset is the frozen bridge
  // refusal. A future catalog carrier may advance beyond this point, but this
  // proposal must never turn that unavailable path into an accepted result.
  await expect(page.getByText('Failed to duplicate generation', { exact: true })).toBeVisible(CEILING);
  expect(traffic.commits).toEqual([]);
  expect(traffic.legacySaves).toEqual([]);
  await expect.poll(async () => (await commandOutboxes(page, seed3.timelineId)).every((owner) => !owner.pending && !owner.intents.length), CEILING).toBe(true);

  /*
   * Once the existing catalog producer returns an original five-field
   * MediaSelection and the native carrier supports exact afterClipId order,
   * extend this one case (without changing the trigger) to assert:
   *
   * - one allocated duplicate clip/asset identity is present in the accepted
   *   clip.add-media command and remains identical after reload;
   * - a producer await with a changed localGeneration or displayed base/head
   *   refuses before preparation/enqueue and leaves the catalogued duplicate
   *   unplaced;
   * - native placement is accepted with the original verified selection;
   * - reload, guarded Runtime undo, lost acknowledgement, restart and exact
   *   idempotent retry preserve the original request key/body and identity;
   * - no POST reaches the legacy composition-revision writer.
   *
   * Those assertions are intentionally not fabricated here: the current
   * seed, adapter and afterClipId carrier cannot produce the accepted path.
   */
});
