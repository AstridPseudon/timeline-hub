import { expect, type Page, type TestInfo } from '@playwright/test';
import { execFile } from 'node:child_process';
import { mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import type { ManagedOutput, Task } from '../../../src/integrations/runtime/generated';
import type { DirectHarness } from '../local/support/harness';
import { assertTaskAuthority, record } from './viewing-parity/authority';
import { waitForRenderAdmission } from './viewing-parity/admission';
import { assertDownloadTransfer, observeDownloadTransfer } from './viewing-parity/download';
import { collectPageDiagnostics } from './viewing-parity/diagnostics';
import { test as parityTest, readyRenderCapability, sourceVersions } from './viewing-parity/harness';
import { mediaHash, readFrameMarker, VIDEO_START_FRAME } from './viewing-parity/media';
import {
  assertPinnedFrameParityFixture, PARITY_FPS, PARITY_FRAMES, PARITY_HEIGHT, PARITY_WIDTH,
  readRuntimeJson, type FrameParityFixture,
} from './viewing-parity/fixture';
import {
  assertFrameWithinBound, capturePlayerFrame, compareRgbFrames, decodeExportFrame,
} from './viewing-parity/frames';

const exec = promisify(execFile);

const test = parityTest.extend<{ pageLogs: ReturnType<typeof collectPageDiagnostics> }>({
  pageLogs: [async ({ page, harness, fixture }, provide, testInfo) => {
    const logs = collectPageDiagnostics(page, harness.doorBase, fixture.projectId);
    await logs.observeMediaErrors();
    try { await provide(logs); } finally {
      logs.stop();
      if (testInfo.status !== testInfo.expectedStatus) logs.discardResult();
      const diagnostics = await logs.result();
      await saveEvidence(testInfo, 'page-diagnostics', diagnostics);
      expect(diagnostics.failures).toEqual([]);
    }
  }, { auto: true }],
});

async function saveEvidence(testInfo: TestInfo, name: string, value: unknown): Promise<void> {
  await mkdir(testInfo.outputPath('viewing-parity'), { recursive: true });
  await writeFile(testInfo.outputPath(`viewing-parity/${name}.json`), `${JSON.stringify(value, null, 2)}\n`);
}

async function openParityEditor(page: Page, harness: DirectHarness, fixture: FrameParityFixture): Promise<void> {
  const params = new URLSearchParams({ runtime: '1', runtimeProject: fixture.projectId, runtimeTimeline: fixture.timelineId });
  await page.goto(`${harness.origin}/tools/video-editor?${params}`, { waitUntil: 'domcontentloaded', timeout: 45_000 });
  const connect = page.getByRole('button', { name: 'Connect', exact: true });
  await expect.poll(async () => await connect.isVisible()
    || await page.locator('[data-testid="runtime-connection-status"][data-state="connected"]').isVisible(),
  { timeout: 45_000 }).toBe(true);
  if (await connect.isVisible()) await connect.click();
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByTestId('preview-revision-label')).toHaveText(`Committed ${fixture.headRevisionId}`);
  await expect(page.getByTestId('video-editor-preview-surface')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Render', exact: true })).toBeEnabled();
}

async function renderAndDownload(page: Page, harness: DirectHarness, fixture: FrameParityFixture, testInfo: TestInfo) {
  const versions = await sourceVersions(testInfo.project.metadata.viewingParityBrowserProfile);
  await assertPinnedFrameParityFixture(harness, fixture);
  const capability = await readyRenderCapability(harness);
  const polls: string[] = [];
  const legacyWrites: string[] = [];
  const onRequest = (request: import('@playwright/test').Request) => {
    const path = new URL(request.url()).pathname;
    if (request.method() === 'GET' && /\/v1\/tasks\/[^/?]+$/.test(path)) polls.push(request.url());
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(request.method())
      && /\/(?:composition-revisions|documents)(?:\/|$)/.test(path)) legacyWrites.push(`${request.method()} ${path}`);
  };
  page.on('request', onRequest);
  try {
    const admissionUrl = `${new URL(harness.doorBase).origin}/api/astrid/v1/tasks`;
    const response = await waitForRenderAdmission(page, admissionUrl,
      () => page.getByRole('button', { name: 'Render', exact: true }).click({ timeout: 30_000 }));
    expect([200, 201]).toContain(response.status());
    const request = response.request().postDataJSON();
    expect(request).toMatchObject({ project: fixture.projectId, capability_id: 'rendering.render',
      capability_digest: capability.definition_digest, input_object_ids: [], spec: { params: {
        timeline_ref: fixture.timelineId, selector: 'rendering.remotion', canonical_project_id: fixture.projectId,
        canonical_parent_document_id: fixture.timelineId, canonical_head_revision_id: fixture.headRevisionId,
        canonical_occurrence_ids: [fixture.occurrenceId],
      } } });
    expect(request.spec.params.expected_version).toBeGreaterThan(0);
    expect(request.spec.inputs).toBeUndefined();
    const admitted = (await response.json()).data as Task;
    expect(admitted.task_id).toBeTruthy();
    const taskPath = `/v1/tasks/${encodeURIComponent(admitted.task_id)}`;
    const initial = await readRuntimeJson<Task>(harness, taskPath);
    const frozen = assertTaskAuthority(initial, fixture, capability.definition_digest);
    const snapshotResponse = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(String(frozen.snapshot.digest))}`);
    expect(snapshotResponse.status).toBe(200);
    const snapshotBytes = new Uint8Array(await snapshotResponse.arrayBuffer());
    expect(mediaHash(snapshotBytes)).toBe(frozen.authority.snapshot_digest);
    const snapshot = record(JSON.parse(Buffer.from(snapshotBytes).toString('utf8')));
    const assets = Object.values(record(record(snapshot.registry).assets)).map(record);
    expect(Object.fromEntries(assets.map(asset => [asset.media_id, `sha256:${asset.content_sha256}`])))
      .toEqual(Object.fromEntries(fixture.media.map(pin => [pin.objectId, pin.digest])));

    const downloadLink = page.getByRole('link', { name: 'Download', exact: true });
    const blocker = page.locator('[data-video-editor-render-blocker="true"]');
    await expect.poll(async () => {
      const task = await readRuntimeJson<Task>(harness, taskPath);
      if (['failed', 'cancelled'].includes(task.state)) return `error:task-${task.state}`;
      const error = (await blocker.allTextContents()).join('\n').trim();
      if (error) return `error:${error}`;
      return task.state === 'succeeded' && await downloadLink.isVisible() ? 'done' : 'pending';
    }, { timeout: 240_000, message: 'mounted App Render action must finish through the real generic pack host' }).toBe('done');
    expect(polls.some(url => url.endsWith(taskPath)), 'App must poll its admitted task').toBe(true);
    expect(legacyWrites, 'Render must not publish through a legacy writer').toEqual([]);
    const completed = await readRuntimeJson<Task>(harness, taskPath);
    expect(completed.spec).toEqual(initial.spec);
    expect(assertTaskAuthority(completed, fixture, capability.definition_digest)).toEqual(frozen);
    const outputs = await readRuntimeJson<{ items: ManagedOutput[] }>(harness, `${taskPath}/managed-outputs?limit=50`);
    expect(outputs.items.filter(item => item.filename.endsWith('.mp4'))).toHaveLength(1);
    const video = outputs.items.find(item => item.filename.endsWith('.mp4'));
    expect(video, 'real task must own its MP4 output association').toBeDefined();
    expect(video).toMatchObject({ task_id: admitted.task_id, project_id: fixture.projectId, media_type: 'video/mp4' });
    expect(outputs.items.filter(item => item.filename.endsWith('.provenance.json'))).toHaveLength(1);
    const provenanceOutput = outputs.items.find(item => item.filename.endsWith('.provenance.json'));
    expect(provenanceOutput, 'real renderer provenance sidecar').toBeDefined();
    const provenanceResponse = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(provenanceOutput!.object_id)}`);
    expect(provenanceResponse.status).toBe(200);
    const provenanceBytes = new Uint8Array(await provenanceResponse.arrayBuffer());
    expect(mediaHash(provenanceBytes)).toBe(provenanceOutput!.digest);
    const provenance = JSON.parse(Buffer.from(provenanceBytes).toString('utf8'));
    expect(provenance.canonical_timeline).toEqual(frozen.authority);
    expect(provenance.engine).toBe('rendering.remotion');
    expect(record(provenance.backend_fragments)['rendering.remotion']).toMatchObject({
      renderer: 'remotion', composition_id: 'TimelineComposition', project_dir: versions.remotionProject,
    });

    const downloadHref = await downloadLink.getAttribute('href');
    expect(downloadHref).toBe(`${new URL(harness.doorBase).origin}/api/astrid/v1/objects/${encodeURIComponent(video!.object_id)}`);
    const transferObserver = observeDownloadTransfer(page, harness.doorBase, fixture.projectId, video!);
    const downloading = page.waitForEvent('download', { timeout: 30_000 });
    let download: import('@playwright/test').Download;
    let downloadTransfer: Awaited<ReturnType<typeof transferObserver.finish>>;
    try {
      await downloadLink.click();
      download = await downloading;
      downloadTransfer = await transferObserver.finish();
    } finally { transferObserver.stop(); }
    await mkdir(testInfo.outputPath('viewing-parity'), { recursive: true });
    const exportPath = testInfo.outputPath('viewing-parity/final-export.mp4');
    await download.saveAs(exportPath);
    expect(await download.failure()).toBeNull();
    expect((await stat(exportPath)).size).toBeGreaterThan(1_000);
    expect((await stat(exportPath)).size).toBe(video!.size);
    const bytes = await readFile(exportPath);
    assertDownloadTransfer(downloadTransfer, harness.doorBase, fixture.projectId, video!, bytes, download.url(), new URL(page.url()).origin);
    expect(bytes.subarray(4, 8).toString('ascii')).toBe('ftyp');
    expect(mediaHash(bytes), 'UI download must be the admitted task output').toBe(video!.digest);
    const { stdout, stderr: probeStderr } = await exec('ffprobe', ['-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', exportPath]);
    expect(probeStderr).toBe('');
    const metadata = JSON.parse(stdout) as { streams: Array<Record<string, unknown>>; format: Record<string, unknown> };
    expect(metadata.streams.find(stream => stream.codec_type === 'video')).toMatchObject({ codec_name: 'h264',
      width: PARITY_WIDTH, height: PARITY_HEIGHT, r_frame_rate: `${PARITY_FPS}/1`, nb_read_frames: '165' });
    // Normal Agent output_policy uses 48kHz AAC; the managed source is 44.1kHz.
    expect(metadata.streams.find(stream => stream.codec_type === 'audio')).toMatchObject({ codec_name: 'aac', sample_rate: '48000', channels: 2 });
    await assertPinnedFrameParityFixture(harness, fixture);
    expect(await sourceVersions(testInfo.project.metadata.viewingParityBrowserProfile)).toEqual(versions);
    const { stdout: ffmpeg } = await exec('ffmpeg', ['-version']);
    await saveEvidence(testInfo, 'real-render', { versions, ffmpeg: ffmpeg.split('\n')[0], capability,
      taskId: admitted.task_id, authority: frozen, outputs: outputs.items, provenance, metadata, downloadHash: mediaHash(bytes),
      downloadTransfer: { ...downloadTransfer, object: { ...downloadTransfer.object, bytes: undefined,
        size: downloadTransfer.object.bytes.length, digest: mediaHash(downloadTransfer.object.bytes) } }, polls, legacyWrites });
    return { exportPath, taskId: admitted.task_id, authority: frozen, versions, capabilityDigest: capability.definition_digest,
      result: { initial, completed, fixture, capabilityDigest: capability.definition_digest, video: video!,
        provenanceOutput: provenanceOutput!, provenanceBytes, downloadBytes: bytes, downloadFailure: await download.failure(),
        downloadHref: downloadHref!, downloadUrl: download.url(), downloadTransfer, metadata, probeStderr, remotionProject: versions.remotionProject } };
  } finally { page.off('request', onRequest); }
}

async function assertRenderUnchanged(harness: DirectHarness, fixture: FrameParityFixture,
  render: Awaited<ReturnType<typeof renderAndDownload>>) {
  await assertPinnedFrameParityFixture(harness, fixture);
  const task = await readRuntimeJson<Task>(harness, `/v1/tasks/${encodeURIComponent(render.taskId)}`);
  expect(assertTaskAuthority(task, fixture, render.capabilityDigest)).toEqual(render.authority);
  expect(await sourceVersions(render.versions.playerBrowser.profile)).toEqual(render.versions);
}

async function compareAllFrames(page: Page, exportPath: string, testInfo: TestInfo) {
  const comparisons = [];
  const decodedFrames = [];
  for (const frame of PARITY_FRAMES) {
    const player = await capturePlayerFrame(page, frame, testInfo, 'positive');
    const exported = await decodeExportFrame(exportPath, frame);
    const comparison = compareRgbFrames(player, exported, frame);
    assertFrameWithinBound(comparison);
    comparisons.push(comparison);
    decodedFrames.push({ frame, decoded: exported });
  }
  await saveEvidence(testInfo, 'comparisons', { fps: PARITY_FPS, dimensions: [PARITY_WIDTH, PARITY_HEIGHT], comparisons });
  return { comparisons, decodedFrames };
}

test.describe('ordinary media: mounted App Player versus real task export', () => {
  test('normal App Render action downloads a valid native-size MP4 without a parity comparison', async ({ page, harness, fixture, pageLogs }, testInfo) => {
    await openParityEditor(page, harness, fixture);
    const render = await renderAndDownload(page, harness, fixture, testInfo);
    const firstFrame = await decodeExportFrame(render.exportPath, 0);
    expect(firstFrame.width).toBe(PARITY_WIDTH);
    expect(firstFrame.height).toBe(PARITY_HEIGHT);
    expect(firstFrame.bytes).toHaveLength(PARITY_WIDTH * PARITY_HEIGHT * 3);
    await assertRenderUnchanged(harness, fixture, render);
    await saveEvidence(testInfo, 'normal-render-action', {
      proof: 'normal App Render route and downloaded MP4 only; no Player/frame/audio parity or source-policy claim',
      revision: fixture.headRevisionId, taskId: render.taskId, authority: render.authority,
      firstFrame: { width: firstFrame.width, height: firstFrame.height, hash: mediaHash(firstFrame.bytes) },
    });
    await pageLogs.completeResult({ ...render.result, decodedFrames: [{ frame: 0, decoded: firstFrame }] });
    expect((await pageLogs.result()).failures).toEqual([]);
  });

  test('fixture readiness seeks actual managed Player video and captures native frames without export', async ({ page, browser, harness, fixture, pageLogs }, testInfo) => {
    const requests: Array<{ url: string; status: number }> = [];
    page.on('response', response => {
      if (decodeURIComponent(response.url()).includes(fixture.sourceVideoMediaId)) requests.push({ url: response.url(), status: response.status() });
    });
    await openParityEditor(page, harness, fixture);
    const captures = [];
    for (const frame of [...PARITY_FRAMES, 135]) {
      const capture = await capturePlayerFrame(page, frame, testInfo, `fixture-${captures.length}`);
      const marker = frame >= VIDEO_START_FRAME ? readFrameMarker(capture.bytes) : null;
      if (frame >= VIDEO_START_FRAME) expect(marker).toBe(frame - VIDEO_START_FRAME);
      captures.push({ frame, hash: mediaHash(capture.bytes), marker });
    }
    expect(new Set(captures.filter(capture => capture.frame >= VIDEO_START_FRAME).map(capture => capture.hash)).size).toBe(5);
    expect(requests.some(request => [200, 206].includes(request.status)), 'actual App managed video fetch').toBe(true);
    await assertPinnedFrameParityFixture(harness, fixture);
    expect((await pageLogs.result()).failures).toEqual([]);
    await saveEvidence(testInfo, 'fixture-readiness', { proof: 'fixture readiness only; no export comparison',
      fixture, versions: await sourceVersions(testInfo.project.metadata.viewingParityBrowserProfile), browser: browser.version(), captures, requests });
  });

  test('compares native-size actual Player frames with decoded real CPU Remotion task output', async ({ page, harness, fixture, pageLogs }, testInfo) => {
    await openParityEditor(page, harness, fixture);
    const render = await renderAndDownload(page, harness, fixture, testInfo);
    const { exportPath } = render;
    const { comparisons, decodedFrames } = await compareAllFrames(page, exportPath, testInfo);
    await assertRenderUnchanged(harness, fixture, render);
    await pageLogs.completeResult({ ...render.result, decodedFrames, comparisons });
    expect((await pageLogs.result()).failures).toEqual([]);
  });

  test('picture-only one-host patch is reported as a mismatch after the full passing baseline', async ({ page, harness, fixture, pageLogs }, testInfo) => {
    await openParityEditor(page, harness, fixture);
    const render = await renderAndDownload(page, harness, fixture, testInfo);
    const { exportPath } = render;
    const { comparisons, decodedFrames } = await compareAllFrames(page, exportPath, testInfo);
    const selectedFrame = 52;
    const before = await capturePlayerFrame(page, selectedFrame, testInfo, 'negative-before-patch');
    const exported = await decodeExportFrame(exportPath, selectedFrame);
    const baseline = compareRgbFrames(before, exported, selectedFrame);
    assertFrameWithinBound(baseline);
    const exportHash = mediaHash(await readFile(exportPath));
    await page.locator('[data-testid="video-editor-preview-surface"] .__remotion-player').evaluate(element => {
      const patch = document.createElement('div');
      patch.dataset.testOnlyPictureMismatch = 'true';
      Object.assign(patch.style, { position: 'absolute', inset: '0', background: 'rgb(255, 0, 255)', zIndex: '2147483647' });
      element.appendChild(patch);
    });
    const patched = await capturePlayerFrame(page, selectedFrame, testInfo, 'negative-patched');
    const comparison = compareRgbFrames(patched, exported, selectedFrame);
    expect(() => assertFrameWithinBound(comparison)).toThrow(/frame 52: \d+\/230400 pixels exceed 2\/255; max channel error=/);
    await assertRenderUnchanged(harness, fixture, render);
    expect(mediaHash(await readFile(exportPath))).toBe(exportHash);
    expect(comparison.pixelsOutsideBound).toBeGreaterThan(0);
    expect(comparison.outsideBoundFraction).toBeGreaterThan(0.001);
    expect(comparison.maxChannelError).toBeGreaterThan(2);
    await saveEvidence(testInfo, 'negative-comparison', { revision: fixture.headRevisionId, selectedFrame, baseline, exportHash, comparison });
    await pageLogs.completeResult({ ...render.result, decodedFrames, comparisons });
    expect((await pageLogs.result()).failures).toEqual([]);
  });
});
