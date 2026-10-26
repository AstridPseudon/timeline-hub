import { readFileSync, statfsSync, writeFileSync } from 'node:fs';
import { expect } from '@playwright/test';
import { EDITOR_TOUR_VERSION } from '../../../src/shared/lib/editorTourVersion.ts';
import { browserEvidencePath } from './support/evidence.ts';
import { test } from './support/app.ts';

test.describe.configure({ mode: 'serial' });

test.afterEach(async ({ page }) => {
  await page.evaluate(async () => {
    const saved = (window as any).__n4Archive;
    if (saved?.name) await (await navigator.storage.getDirectory()).removeEntry(saved.name).catch(() => {});
    delete (window as any).__n4Archive;
  }).catch(() => {});
});

test('CLI-imported archive exports and imports into a fresh project, then plays', async ({ page, harness }, testInfo) => {
  test.setTimeout(0);
  const descriptor = harness.attachment;
  expect(descriptor, 'N4 needs the isolated CLI-imported realm descriptor').toBeTruthy();
  const imported = JSON.parse(readFileSync(descriptor!.resultFile, 'utf8')) as {
    status?: string;
    project_id?: string;
    timeline_ids?: string[];
    archive_bytes: number;
  };
  expect(imported.status).toBe('passed');
  expect(imported.project_id).toBe(descriptor!.projectId);
  expect(imported.timeline_ids).toContain(descriptor!.timelineId);
  const sourceArchiveBytes = Number(imported.archive_bytes);
  expect(sourceArchiveBytes).toBeGreaterThan(0);
  expect(descriptor!.sourceArchiveBytes).toBe(sourceArchiveBytes);
  expect(descriptor!.freeBytesBefore).toBeGreaterThan(0);
  const diskFreeBefore = Number(descriptor!.freeBytesBefore);

  const blockedPorts = new Set(['17340', '2222']);
  const observedRequests: string[] = [];
  const forbiddenRequests: string[] = [];
  const sandboxDoor = new URL(descriptor!.doorEndpoint);
  expect(['http:', 'https:']).toContain(sandboxDoor.protocol);
  expect(sandboxDoor.hostname).toBe('127.0.0.1');
  expect(blockedPorts.has(sandboxDoor.port), 'sandbox door must use its own dynamic port').toBe(false);
  expect(harness.origin).toBe(descriptor!.hostedOrigin);
  const appMode = process.env.N4_APP_MODE ?? 'hosted';
  const appOrigin = appMode === 'hosted' ? harness.origin : process.env.N4_LOCAL_APP_ORIGIN;
  expect(appOrigin, 'local flow requires N4_LOCAL_APP_ORIGIN').toBeTruthy();
  const allowedOrigins = new Set([appOrigin!, harness.origin, sandboxDoor.origin]);
  await page.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    observedRequests.push(`${route.request().method()} ${url.href}`);
    if (blockedPorts.has(url.port) || !allowedOrigins.has(url.origin)) {
      forbiddenRequests.push(url.href);
      await route.abort('blockedbyclient');
      return;
    }
    await route.continue();
  });

  // Use a real OPFS-backed file handle so the product exercises its streaming File System Access path.
  // This keeps the archive file-backed in Chromium instead of materializing a multi-gigabyte Blob.
  await page.addInitScript(({ localOrigin, tourKey }) => {
    if (window.location.origin === localOrigin) localStorage.setItem(tourKey, '1');
    const nativeInputClick = HTMLInputElement.prototype.click;
    HTMLInputElement.prototype.click = function () {
      // Keep the product's Import button and change handler, while supplying the
      // OPFS-backed File below instead of opening an OS file chooser.
      if (this.getAttribute('aria-label') === 'Import timeline archive') return;
      nativeInputClick.call(this);
    };
    Object.defineProperty(window, 'showSaveFilePicker', {
      configurable: true,
      value: async () => {
        const name = `n4-${crypto.randomUUID()}.astrid`;
        const root = await navigator.storage.getDirectory();
        const handle = await root.getFileHandle(name, { create: true });
        (window as any).__n4Archive = { name, handle };
        return handle;
      },
    });
  }, { localOrigin: appOrigin!, tourKey: `astrid-editor-tour-v${EDITOR_TOUR_VERSION}` });
  const query = new URLSearchParams({ project: descriptor!.projectId, timeline: descriptor!.timelineId });
  await page.goto(`${appOrigin}/tools/video-editor?${query}`);
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  await expect(page.getByRole('combobox', { name: 'Select timeline' })).toBeVisible();
  const picker = page.getByRole('combobox', { name: 'Select timeline' });
  await expect(picker).toBeVisible();
  await picker.click();
  await expect(page.getByRole('option').first()).toBeVisible();
  const cliPickerEvidence = browserEvidencePath(testInfo, 'timeline-transfer/cli-imported-picker.png');
  await page.screenshot({ path: cliPickerEvidence, fullPage: true });
  await page.keyboard.press('Escape');
  await expect(page.getByRole('option')).toHaveCount(0);

  await picker.click();
  const exportStarted = await page.evaluate(() => performance.now());
  await page.getByRole('button', { name: 'Export timeline', exact: true }).click();
  await expect(page.getByText(/^Exported /)).toBeVisible({ timeout: 600_000 });
  const archive = await page.evaluate(async () => {
    const saved = (window as any).__n4Archive;
    if (!saved?.handle) throw new Error('export did not open the OPFS destination');
    const file = await saved.handle.getFile();
    return { name: saved.name, size: file.size };
  });
  const exportCompleteEvidence = browserEvidencePath(testInfo, 'timeline-transfer/ui-export-complete.png');
  await page.screenshot({ path: exportCompleteEvidence, fullPage: true });
  const exportElapsedMs = await page.evaluate((started) => performance.now() - started, exportStarted);
  const archiveInfo = archive as { name: string; size: number };
  expect(archiveInfo.name).toMatch(/^n4-.*\.astrid$/i);
  expect(archiveInfo.size).toBeGreaterThan(0);
  if (sourceArchiveBytes >= 1024 ** 3) expect(archiveInfo.size).toBeGreaterThanOrEqual(1024 ** 3);
  const diskAfterExport = statfsSync(descriptor!.dataRoot);
  const diskFreeAfterExport = Number(diskAfterExport.bavail) * Number(diskAfterExport.bsize);
  expect(diskFreeAfterExport, 'sandbox must retain at least 2 GiB free during the browser transfer').toBeGreaterThanOrEqual(2 * 1024 ** 3);

  // Import into a separate empty project in the same sandbox Runtime. The fixture creates it before this test.
  const targetProjectId = descriptor!.transferProjectId;
  const targetProjectName = descriptor!.transferProjectName;
  if (!targetProjectId || !targetProjectName) throw new Error('N4 descriptor must include the Runtime-created empty UI import project');
  const projectPicker = page.getByRole('combobox', { name: 'Select project' });
  await projectPicker.click();
  await page.getByRole('option', { name: new RegExp(targetProjectName, 'i') }).click();
  await expect.poll(() => new URL(page.url()).searchParams.get('project')).toBe(targetProjectId);
  await picker.click();
  await expect(page.getByRole('button', { name: 'Import timeline…', exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Import timeline…', exact: true }).click();
  const importStarted = await page.evaluate(() => performance.now());
  const input = page.getByLabel('Import timeline archive');
  await page.evaluate(async () => {
    const saved = (window as any).__n4Archive;
    if (!saved?.handle) throw new Error('OPFS export handle was not retained');
    const file = await saved.handle.getFile();
    const transfer = new DataTransfer();
    transfer.items.add(file);
    const input = document.querySelector<HTMLInputElement>('input[aria-label="Import timeline archive"]');
    if (!input) throw new Error('timeline import file input is missing');
    input.files = transfer.files;
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });
  await expect(input).toHaveCount(1);
  await expect.poll(() => {
    const timelineId = new URL(page.url()).searchParams.get('timeline');
    return timelineId && timelineId !== descriptor!.timelineId ? timelineId : null;
  }, { message: 'the editor selects a new timeline imported into the fresh project', timeout: 600_000 }).toBeTruthy();
  await expect(page.getByText(/^Imported /)).toBeVisible({ timeout: 600_000 });
  const importElapsedMs = await page.evaluate((started) => performance.now() - started, importStarted);
  await expect.poll(() => new URL(page.url()).searchParams.get('project')).toBe(targetProjectId);
  const roundTripTimelineId = new URL(page.url()).searchParams.get('timeline');
  expect(roundTripTimelineId).toBeTruthy();
  expect(roundTripTimelineId).not.toBe(descriptor!.timelineId);
  const savedTimeline = await harness.runtimeJson('GET', `/v1/projects/${encodeURIComponent(targetProjectId)}/timelines/${encodeURIComponent(roundTripTimelineId!)}/composition-revisions?limit=1`);
  expect(savedTimeline.body.items.some((row: any) => row.is_current_head && row.revision_id)).toBe(true);
  const diskAfterImport = statfsSync(descriptor!.dataRoot);
  const diskFreeAfterImport = Number(diskAfterImport.bavail) * Number(diskAfterImport.bsize);
  expect(diskFreeAfterImport, 'sandbox must retain at least 2 GiB free after UI import').toBeGreaterThanOrEqual(2 * 1024 ** 3);

  await picker.click();
  await expect(page.getByRole('option')).toHaveCount(1);
  const roundTripPickerEvidence = browserEvidencePath(testInfo, 'timeline-transfer/ui-round-trip-picker.png');
  await page.screenshot({ path: roundTripPickerEvidence, fullPage: true });
  await page.keyboard.press('Escape');
  await expect(page.getByRole('option')).toHaveCount(0);

  const position = page.getByRole('slider', { name: 'Playback position' });
  await expect(position).toBeVisible();
  await expect(page.locator('[data-testid="preview-panel"]')).toBeVisible();
  const before = await position.getAttribute('aria-valuenow');
  await page.getByRole('button', { name: 'Play', exact: true }).click();
  await expect.poll(async () => position.getAttribute('aria-valuenow'), {
    message: 'playback frame advances on the CLI-imported timeline', timeout: 15_000,
  }).not.toBe(before);
  await page.getByRole('button', { name: 'Pause', exact: true }).click();
  const playbackEvidence = browserEvidencePath(testInfo, 'timeline-transfer/ui-round-trip-playback.png');
  await page.screenshot({ path: playbackEvidence, fullPage: true });

  const memory = await page.evaluate(async () => {
    const measure = (performance as any).measureUserAgentSpecificMemory;
    if (typeof measure !== 'function') return null;
    const value = await measure.call(performance);
    return { bytes: value.bytes, measurement: 'current after transfer, not peak RSS', label: 'Chromium browser memory estimate' };
  }).catch(() => null);
  const evidence = {
    status: 'passed',
    project_id: descriptor!.projectId,
    imported_into_project_id: targetProjectId,
    imported_timeline_id: descriptor!.timelineId,
    imported_timeline_ids: imported.timeline_ids,
    app_mode: appMode,
    app_origin: appOrigin,
    hosted_origin: harness.origin,
    door_endpoint: descriptor!.doorEndpoint,
    cli_picker_screenshot: cliPickerEvidence,
    export_complete_screenshot: exportCompleteEvidence,
    round_trip_picker_screenshot: roundTripPickerEvidence,
    playback_screenshot: playbackEvidence,
    archive_file: `OPFS:${archiveInfo.name}`,
    archive_size_bytes: archiveInfo.size,
    disk_free_bytes_before: diskFreeBefore,
    disk_free_bytes_after_export: diskFreeAfterExport,
    disk_free_bytes_after_import: diskFreeAfterImport,
    export_elapsed_ms: exportElapsedMs,
    import_elapsed_ms: importElapsedMs,
    ui_import_selected_timeline: new URL(page.url()).searchParams.get('timeline'),
    ui_import_selected_project: new URL(page.url()).searchParams.get('project'),
    browser_memory: memory ?? { status: 'unavailable', bytes: null, label: 'Browser memory API unavailable; no point-in-time estimate was collected.' },
    browser_peak_memory: { status: 'unmeasured', label: 'Aggregate Chromium process peak memory was not collected; N4 performance assessment remains pending.' },
    performance_status: 'pending-aggregate-browser-peak-memory-measurement',
    allowed_origins: [...allowedOrigins],
    playback_position_before: before,
    playback_position_after: await position.getAttribute('aria-valuenow'),
    forbidden_ports: [...blockedPorts],
    requests: observedRequests,
  };
  writeFileSync(browserEvidencePath(testInfo, 'timeline-transfer/result.json'), `${JSON.stringify(evidence, null, 2)}\n`);
  await page.evaluate(async () => {
    const saved = (window as any).__n4Archive;
    if (saved?.name) await (await navigator.storage.getDirectory()).removeEntry(saved.name);
    delete (window as any).__n4Archive;
  });
  expect(forbiddenRequests, `blocked external/owner endpoint requests: ${forbiddenRequests.join(', ')}`).toEqual([]);
});
