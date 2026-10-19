import { expect, test } from '@playwright/test';
import { editorUrl, resetFakeRuntimeBaseline } from './support';

test('probe real Player tab output', async ({ page }) => {
  test.setTimeout(120_000);
  expect(await resetFakeRuntimeBaseline()).toBeNull();
  await page.goto(editorUrl({ timeline: 'audio-reactive-colour-timeline' }));
  await expect(page.getByRole('button', { name: 'Play', exact: true }).first()).toBeVisible({ timeout: 90_000 });
  await page.evaluate(() => {
    const button = document.createElement('button');
    button.id = 'capture-probe';
    button.textContent = 'Capture probe';
    button.style.cssText = 'position:fixed;top:0;left:0;z-index:99999';
    button.onclick = async () => {
      try {
        const stream = await navigator.mediaDevices.getDisplayMedia({
          video: true, audio: true, preferCurrentTab: true,
        } as DisplayMediaStreamOptions);
        button.dataset.result = JSON.stringify(stream.getTracks().map(track => ({ kind: track.kind, label: track.label, settings: track.getSettings() })));
        stream.getTracks().forEach(track => track.stop());
      } catch (error) {
        button.dataset.result = String(error);
      }
    };
    document.body.append(button);
  });
  await page.locator('#capture-probe').click();
  await expect.poll(() => page.locator('#capture-probe').getAttribute('data-result'), { timeout: 10_000 }).not.toBeNull();
  console.log('TAB_CAPTURE_PROBE', await page.locator('#capture-probe').getAttribute('data-result'));
});
