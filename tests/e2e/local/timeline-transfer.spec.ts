import { readFileSync, writeFileSync } from 'node:fs';
import { expect } from '@playwright/test';
import { browserEvidencePath } from '../../timeline/support.ts';
import { test } from './support/app.ts';

test.describe.configure({ mode: 'serial' });

test('CLI-imported timeline is selectable and plays in the hosted editor', async ({ page, harness }, testInfo) => {
  const descriptor = harness.attachment;
  expect(descriptor, 'N4 needs the isolated CLI-imported realm descriptor').toBeTruthy();
  const imported = JSON.parse(readFileSync(descriptor!.resultFile, 'utf8')) as {
    status?: string;
    project_id?: string;
    timeline_ids?: string[];
  };
  expect(imported.status).toBe('passed');
  expect(imported.project_id).toBe(descriptor!.projectId);
  expect(imported.timeline_ids).toContain(descriptor!.timelineId);

  const blockedPorts = new Set(['17340', '2222']);
  const observedRequests: string[] = [];
  const forbiddenRequests: string[] = [];
  await page.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    observedRequests.push(`${route.request().method()} ${url.href}`);
    if (blockedPorts.has(url.port)) {
      forbiddenRequests.push(url.href);
      await route.abort('blockedbyclient');
      return;
    }
    await route.continue();
  });

  const query = new URLSearchParams({ project: descriptor!.projectId, timeline: descriptor!.timelineId });
  await page.goto(`${harness.origin}/tools/video-editor?${query}`);
  await expect(page.locator('[data-testid="runtime-connection-status"]')).toHaveAttribute('data-state', 'connected');
  const picker = page.getByRole('combobox', { name: 'Select timeline' });
  await expect(picker).toBeVisible();
  await picker.click();
  await expect(page.getByRole('option').first()).toBeVisible();
  const pickerEvidence = browserEvidencePath(testInfo, 'timeline-transfer/cli-imported-picker.png');
  await page.screenshot({ path: pickerEvidence, fullPage: true });
  await page.keyboard.press('Escape');
  await expect(page.getByRole('option')).toHaveCount(0);

  const position = page.getByRole('slider', { name: 'Playback position' });
  await expect(position).toBeVisible();
  const before = await position.getAttribute('aria-valuenow');
  await page.getByRole('button', { name: 'Play', exact: true }).click();
  await expect.poll(async () => position.getAttribute('aria-valuenow'), {
    message: 'playback frame advances on the CLI-imported timeline', timeout: 15_000,
  }).not.toBe(before);
  await page.getByRole('button', { name: 'Pause', exact: true }).click();
  const playbackEvidence = browserEvidencePath(testInfo, 'timeline-transfer/cli-imported-playback.png');
  await page.screenshot({ path: playbackEvidence, fullPage: true });

  const evidence = {
    status: 'passed',
    project_id: descriptor!.projectId,
    imported_timeline_id: descriptor!.timelineId,
    imported_timeline_ids: imported.timeline_ids,
    hosted_origin: harness.origin,
    door_endpoint: descriptor!.doorEndpoint,
    picker_screenshot: pickerEvidence,
    playback_screenshot: playbackEvidence,
    playback_position_before: before,
    playback_position_after: await position.getAttribute('aria-valuenow'),
    forbidden_ports: [...blockedPorts],
    requests: observedRequests,
  };
  writeFileSync(browserEvidencePath(testInfo, 'timeline-transfer/result.json'), `${JSON.stringify(evidence, null, 2)}\n`);
  expect(forbiddenRequests).toEqual([]);
});
