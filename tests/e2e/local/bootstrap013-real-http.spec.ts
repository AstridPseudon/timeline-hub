import { expect } from '@playwright/test';
import { ASTRID_PYTHON } from './support/astrid.ts';
import { APP_ENTRY_ROUTE, expectConnected, openApp, test as appTest, waitForAudit } from './support/app.ts';
import type { DirectHarness } from './support/harness.ts';
import { pinnedRuntimeEditCommandOps } from '../../../src/integrations/runtime/__tests__/pinnedRuntimeEditCommandContract.ts';

const CEILING = 90_000;

const expectedPayload = {
  slug: 'main',
  name: 'Main',
  config: {
    output: {
      resolution: '1280x720',
      fps: 30,
      file: 'output.mp4',
      background: null,
      background_scale: null,
    },
    clips: [],
    tracks: [
      { id: 'V1', kind: 'visual', label: 'V1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
      { id: 'A1', kind: 'audio', label: 'A1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
    ],
  },
  registry: { assets: {} },
  clips: [],
  occurrences: [],
};

async function rawCanonical(harness: DirectHarness, projectId: string, timelineId: string) {
  const base = `/v1/projects/${projectId}/timelines/${timelineId}`;
  const timeline = await harness.doorRequest(base);
  expect(timeline.status, timeline.text).toBe(200);
  const timelineBody = timeline.json();
  expect(timelineBody.head_revision_id, timeline.text).toBeTruthy();
  const revision = await harness.doorRequest(`${base}/composition-revisions/${timelineBody.head_revision_id}`);
  expect(revision.status, revision.text).toBe(200);
  return { timeline: timelineBody, revision: revision.json() };
}

appTest('real App initializer publishes accepted defaults and survives Runtime restart over the door', async ({ page, harness }) => {
  // This is the current production startup profile. The native bootstrap module is deliberately not imported or called.
  await harness.enableTimelineAuthoring(ASTRID_PYTHON);
  const auditedBefore = harness.audit().length;
  const supported = pinnedRuntimeEditCommandOps();
  expect(supported.has('timeline.init')).toBe(false);

  await openApp(page, harness);
  await expectConnected(page);
  await page.getByRole('button', { name: 'New project' }).click();
  const projectName = `HTTP defaults ${Date.now()}`;
  await page.locator('#project-name').fill(projectName);
  await page.getByRole('button', { name: 'Create Project' }).click();
  await expect(page).toHaveURL(/\/tools\/video-editor\?project=[^&]+&timeline=[^&]+/, { timeout: CEILING });
  await expect(page.getByRole('combobox', { name: 'Select project' })).toContainText(projectName, { timeout: CEILING });

  const selected = new URL(page.url()).searchParams;
  const projectId = selected.get('project');
  const timelineId = selected.get('timeline');
  expect(projectId).toBeTruthy();
  expect(timelineId).toBeTruthy();
  const scope = { projectId: projectId!, timelineId: timelineId! };
  const publishPath = `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/composition-revisions`;
  const commitPath = `/v1/projects/${scope.projectId}/timelines/${scope.timelineId}/commit`;

  const accepted = await waitForAudit(harness, (entry) => entry.method === 'POST' && entry.path === publishPath, CEILING);
  expect(accepted, 'the real initializer must publish through the Runtime HTTP door').toHaveLength(1);
  expect(accepted[0].status).toBe(200);
  const requests = harness.audit().slice(auditedBefore);
  expect(requests.filter((entry) => entry.method === 'POST' && entry.path === commitPath), 'native init must not be emitted').toEqual([]);
  expect(requests.filter((entry) => entry.method === 'POST' && entry.path.endsWith('/composition-revisions'))).toHaveLength(1);

  const first = await rawCanonical(harness, scope.projectId, scope.timelineId);
  expect(first.timeline).toMatchObject({ project_id: scope.projectId, timeline_id: scope.timelineId, head_revision_id: first.revision.revision_id });
  expect(first.revision).toMatchObject({ project_id: scope.projectId, timeline_id: scope.timelineId, payload: expectedPayload });
  expect(first.revision.payload).toEqual(expectedPayload);
  const firstHead = first.timeline.head_revision_id;
  const firstRevision = {
    revision_id: first.revision.revision_id,
    content_digest: first.revision.content_digest,
    payload: first.revision.payload,
  };

  const previousInstance = harness.runtimeInstanceId;
  const restarted = await harness.restartRuntime();
  expect(restarted.oldInstanceId).toBe(previousInstance);
  expect(harness.runtimeInstanceId).not.toBe(previousInstance);
  await page.goto(`${harness.origin}${APP_ENTRY_ROUTE}?project=${encodeURIComponent(scope.projectId)}&timeline=${encodeURIComponent(scope.timelineId)}`);
  await expectConnected(page);

  const after = await rawCanonical(harness, scope.projectId, scope.timelineId);
  expect(after.timeline.head_revision_id).toBe(firstHead);
  expect({
    revision_id: after.revision.revision_id,
    content_digest: after.revision.content_digest,
    payload: after.revision.payload,
  }).toEqual(firstRevision);
  expect(harness.audit().slice(auditedBefore).filter((entry) => entry.method === 'POST' && entry.path === publishPath)).toHaveLength(1);
  expect(harness.audit().slice(auditedBefore).filter((entry) => entry.method === 'POST' && entry.path === commitPath)).toEqual([]);
});
