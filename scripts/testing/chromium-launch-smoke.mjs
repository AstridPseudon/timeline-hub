import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { chromium } from 'playwright';

const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
if (!executablePath) throw new Error('PLAYWRIGHT_CHROMIUM_EXECUTABLE is required');

const browserHash = createHash('sha256');
for await (const chunk of createReadStream(executablePath)) browserHash.update(chunk);
console.log('[chromium-smoke] executable', executablePath);
console.log('[chromium-smoke] sha256', browserHash.digest('hex'));
console.log('[chromium-smoke] tmpdir', process.env.TMPDIR ?? '');
console.log('[chromium-smoke] xdg-cache', process.env.XDG_CACHE_HOME ?? '');
console.log('[chromium-smoke] xdg-config', process.env.XDG_CONFIG_HOME ?? '');

const browser = await chromium.launch({
  executablePath,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--no-proxy-server'],
});
try {
  const page = await browser.newPage();
  await page.goto('data:text/html,<title>Timeline%20Chromium%20launch%20smoke</title><main>launch-ok</main>');
  if (await page.title() !== 'Timeline Chromium launch smoke') throw new Error('unexpected smoke page title');
  if (await page.locator('main').textContent() !== 'launch-ok') throw new Error('unexpected smoke page body');
  await page.close();
  console.log('[chromium-smoke] PASS page launch, DOM assertion, page close');
} finally {
  await browser.close();
}
console.log('[chromium-smoke] PASS browser close');

