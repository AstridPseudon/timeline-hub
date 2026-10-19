import { expect, test, type Page, type TestInfo } from '@playwright/test';
import { readFile, stat, writeFile } from 'node:fs/promises';
import { mediaHash, readFrameMarker, VIDEO_START_FRAME } from './viewing-parity/media';
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
  // The fake Runtime has no ACP catalogs. Seed only these unrelated chat
  // lists so strict console checks still catch actual media/Player failures.
  await page.route('**/api/astrid/acp/agents', route => route.fulfill({ json: { agents: [] } }));
  await page.route('**/api/astrid/acp/models', route => route.fulfill({ json: { currentModel: null, providers: [] } }));
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

  test('fixture readiness seeks actual managed Player video and captures native frames without export', async ({ page, browser }, testInfo) => {
    test.setTimeout(120_000);
    const logs = collectPageLogs(page);
    const fixture = await publishFrameParityFixture();
    const requests: Array<{ url: string; status: number }> = [];
    page.on('response', response => {
      if (decodeURIComponent(response.url()).includes(fixture.sourceVideoMediaId)) {
        requests.push({ url: response.url(), status: response.status() });
      }
    });
    await openParityEditor(page);
    await expect(page.getByTestId('preview-revision-label')).toHaveText(`Committed ${fixture.headRevisionId}`);
    const captures: Array<{ frame: number; hash: string; marker: number | null }> = [];
    // Revisit a previous video frame as well: a stale ready flag cannot satisfy
    // the marker check when seeking backwards from the last source frame.
    for (const frame of [...PARITY_FRAMES, 135]) {
      const capture = await capturePlayerFrame(page, frame, testInfo, `fixture-${captures.length}`);
      const marker = frame >= VIDEO_START_FRAME ? readFrameMarker(capture.bytes) : null;
      if (frame >= VIDEO_START_FRAME) expect(marker).toBe(frame - VIDEO_START_FRAME);
      captures.push({ frame, hash: mediaHash(capture.bytes), marker });
    }
    expect(new Set(captures.filter(capture => capture.frame >= VIDEO_START_FRAME).map(capture => capture.hash)).size).toBe(5);
    expect(requests.some(request => [200, 206].includes(request.status)), 'managed video bytes fetched by actual App').toBe(true);
    await assertPinnedFrameParityFixture(fixture);
    expect(logs).toEqual([]);
    const { stdout: ffmpegVersion } = await execFileAsync('ffmpeg', ['-version']);
    const metrics = {
      proof: 'fixture readiness and native Player capture only; no export or parity claim',
      revision: fixture.headRevisionId, graphDigest: fixture.graphDigest,
      sourceVideoMediaId: fixture.sourceVideoMediaId, sourceVideoMetadata: fixture.sourceVideoMetadata,
      sourceAudioMediaId: fixture.sourceAudioMediaId, sourceImageMediaIds: fixture.sourceImageMediaIds,
      fps: `${PARITY_FPS}/1`, dimensions: [PARITY_WIDTH, PARITY_HEIGHT], deviceScaleFactor: 1,
      browser: browser.version(), node: process.version, ffmpeg: ffmpegVersion.split('\n')[0],
      captures, requests,
    };
    const path = browserEvidencePath(testInfo, 'viewing-parity/fixture-readiness.json');
    await writeFile(path, `${JSON.stringify(metrics, null, 2)}\n`);
    console.log('FRAME_FIXTURE_READINESS', path, JSON.stringify(metrics));
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
    const before = await capturePlayerFrame(page, selectedFrame, testInfo, 'negative-before-patch');
    const exported = await decodeExportFrame(exportPath, selectedFrame);
    const baseline = compareRgbFrames(before, exported, selectedFrame);
    assertFrameWithinBound(baseline);
    const exportHash = mediaHash(await readFile(exportPath));
    await page.locator('[data-testid="video-editor-preview-surface"] .__remotion-player').evaluate((element) => {
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
    const comparison = compareRgbFrames(patched, exported, selectedFrame);
    expect(() => assertFrameWithinBound(comparison)).toThrow(/frame 52: \d+\/230400 pixels exceed 2\/255; max channel error=/);
    await assertPinnedFrameParityFixture(fixture);
    expect(mediaHash(await readFile(exportPath))).toBe(exportHash);
    expect(comparison.pixelsOutsideBound).toBeGreaterThan(0);
    expect(comparison.outsideBoundFraction).toBeGreaterThan(0.001);
    expect(comparison.maxChannelError).toBeGreaterThan(2);
    expect(logs).toEqual([]);
    await writeFile(browserEvidencePath(testInfo, 'viewing-parity/negative-comparison.json'), `${JSON.stringify({
      revision: fixture.headRevisionId,
      graphDigest: fixture.graphDigest,
      selectedFrame,
      baseline,
      exportHash,
      comparison,
      expected: 'picture-only Player patch must exceed the strict RGB comparator bound',
    }, null, 2)}\n`);
  });
});
