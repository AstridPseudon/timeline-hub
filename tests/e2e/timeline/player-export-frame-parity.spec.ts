import { expect, test, type Page, type TestInfo } from '@playwright/test';
import { readFile, stat, writeFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import {
  assertPinnedFrameParityFixture,
  PARITY_FPS,
  PARITY_FRAMES,
  PARITY_HEIGHT,
  PARITY_WIDTH,
  publishFrameParityFixture,
} from './viewing-parity/fixture';
import {
  assertFrameWithinBound,
  capturePlayerFrame,
  compareRgbFrames,
  decodeExportFrame,
  type FrameComparison,
} from './viewing-parity/frames';
import {
  EDITOR_SETTLE_MS,
  browserEvidencePath,
  collectPageLogs,
  editorUrl,
  resetFakeRuntimeBaseline,
  TIMELINE_SLUG,
} from './support';

const execFileAsync = promisify(execFile);
const EDITOR_URL = editorUrl({ timeline: TIMELINE_SLUG, params: { localBrowserRender: '1' } });

async function openParityEditor(page: Page): Promise<void> {
  await page.goto(EDITOR_URL, { waitUntil: 'domcontentloaded', timeout: 45_000 });
  await page.getByRole('button', { name: 'Render', exact: true }).waitFor({ state: 'visible', timeout: 45_000 });
  await page.waitForTimeout(EDITOR_SETTLE_MS);
  await expect(page.locator('[data-testid="video-editor-preview-surface"]')).toBeVisible();
  await expect(page.getByTestId('preview-revision-label')).toBeVisible();
}

async function renderAndDownload(page: Page, testInfo: TestInfo): Promise<string> {
  const renderButton = page.getByRole('button', { name: /^Render(?: \d+%)?$/ });
  await expect(renderButton).toBeEnabled();
  await renderButton.click();
  const downloadLink = page.getByRole('link', { name: 'Download', exact: true });
  const blocker = page.locator('[data-video-editor-render-blocker="true"]');
  await expect.poll(async () => {
    if (await downloadLink.isVisible()) return 'done';
    const blockerText = (await blocker.textContent().catch(() => null))?.trim();
    if (blockerText) return `error:${blockerText}`;
    return 'pending';
  }, { timeout: 180_000, message: 'normal App Remotion export did not complete' }).toBe('done');
  const downloadPromise = page.waitForEvent('download', { timeout: 30_000 });
  await downloadLink.click();
  const download = await downloadPromise;
  const output = browserEvidencePath(testInfo, 'viewing-parity/final-export.mp4');
  await download.saveAs(output);
  expect((await stat(output)).size).toBeGreaterThan(1_000);
  expect((await readFile(output)).subarray(4, 8).toString('ascii')).toBe('ftyp');
  return output;
}

async function assertExportShape(exportPath: string): Promise<void> {
  const { stdout } = await execFileAsync('ffprobe', [
    '-v', 'error', '-show_streams', '-show_format', '-of', 'json', exportPath,
  ]);
  const metadata = JSON.parse(stdout) as { streams?: Array<Record<string, unknown>> };
  const video = metadata.streams?.find((stream) => stream.codec_type === 'video');
  const audio = metadata.streams?.find((stream) => stream.codec_type === 'audio');
  expect(video).toMatchObject({ width: PARITY_WIDTH, height: PARITY_HEIGHT, r_frame_rate: `${PARITY_FPS}/1` });
  expect(audio).toMatchObject({ codec_type: 'audio', sample_rate: '44100', channels: 2 });
}

async function runPositiveComparison(page: Page, testInfo: TestInfo): Promise<FrameComparison[]> {
  const fixture = await publishFrameParityFixture();
  await openParityEditor(page);
  await expect(page.getByTestId('preview-revision-label')).toHaveText(`Committed ${fixture.headRevisionId}`);
  const exportPath = await renderAndDownload(page, testInfo);
  await assertExportShape(exportPath);
  await assertPinnedFrameParityFixture(fixture);

  const comparisons: FrameComparison[] = [];
  for (const frame of PARITY_FRAMES) {
    const player = await capturePlayerFrame(page, frame, testInfo, 'positive');
    const exported = await decodeExportFrame(exportPath, frame);
    const comparison = compareRgbFrames(player, exported, frame);
    assertFrameWithinBound(comparison);
    comparisons.push(comparison);
  }
  await writeFile(browserEvidencePath(testInfo, 'viewing-parity/comparisons.json'), `${JSON.stringify({
    revision: fixture.headRevisionId,
    graphDigest: fixture.graphDigest,
    fps: PARITY_FPS,
    dimensions: [PARITY_WIDTH, PARITY_HEIGHT],
    frames: PARITY_FRAMES,
    comparisons,
  }, null, 2)}\n`);
  return comparisons;
}

test.describe('App Player versus final export frame parity', () => {
  test.use({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1, acceptDownloads: true });

  test.beforeEach(async () => {
    expect(await resetFakeRuntimeBaseline()).toBeNull();
  });

  test('compares native-size actual Player frames with decoded normal Remotion export frames', async ({ page }, testInfo) => {
    test.setTimeout(240_000);
    const logs = collectPageLogs(page);
    await runPositiveComparison(page, testInfo);
    expect(logs).toEqual([]);
  });

  test('picture-only one-host patch is reported as a mismatch', async ({ page }, testInfo) => {
    test.setTimeout(240_000);
    const logs = collectPageLogs(page);
    const fixture = await publishFrameParityFixture();
    await openParityEditor(page);
    await expect(page.getByTestId('preview-revision-label')).toHaveText(`Committed ${fixture.headRevisionId}`);
    const exportPath = await renderAndDownload(page, testInfo);
    await assertExportShape(exportPath);
    await assertPinnedFrameParityFixture(fixture);

    const selectedFrame = 52;
    await capturePlayerFrame(page, selectedFrame, testInfo, 'negative-before-patch');
    await page.locator('[data-testid="video-editor-preview-surface"] .__remotion-player > div > div').evaluate((element) => {
      const patch = document.createElement('div');
      patch.dataset.testOnlyPictureMismatch = 'true';
      Object.assign(patch.style, {
        position: 'absolute',
        inset: '0',
        background: 'rgb(255, 0, 255)',
        zIndex: '2147483647',
      });
      element.appendChild(patch);
    });
    const patched = await capturePlayerFrame(page, selectedFrame, testInfo, 'negative-patched');
    const exported = await decodeExportFrame(exportPath, selectedFrame);
    const comparison = compareRgbFrames(patched, exported, selectedFrame);
    expect(comparison.pixelsOutsideBound).toBeGreaterThan(0);
    expect(comparison.outsideBoundFraction).toBeGreaterThan(0.001);
    expect(comparison.maxChannelError).toBeGreaterThan(2);
    expect(logs).toEqual([]);
    await writeFile(browserEvidencePath(testInfo, 'viewing-parity/negative-comparison.json'), `${JSON.stringify({
      revision: fixture.headRevisionId,
      graphDigest: fixture.graphDigest,
      selectedFrame,
      comparison,
      expected: 'picture-only Player patch must exceed the strict RGB comparator bound',
    }, null, 2)}\n`);
  });
});
