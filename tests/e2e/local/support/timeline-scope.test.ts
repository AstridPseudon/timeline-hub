import assert from 'node:assert/strict';
import test from 'node:test';
import { timelineBase, timelineFromList, waitForCreatedProjectUrl } from './timeline-scope.ts';
import type { Page } from '@playwright/test';

test('timeline paths keep seeded and created-project scopes explicit', () => {
  assert.equal(timelineBase({ projectId: 'seeded-project', timelineId: 'seeded-timeline' }),
    '/v1/projects/seeded-project/timelines/seeded-timeline');
  assert.equal(timelineBase({ projectId: 'created-project', timelineId: 'created-timeline' }),
    '/v1/projects/created-project/timelines/created-timeline');
});

test('timeline list lookup requires the exact selected resource', () => {
  const page = { items: [
    { timeline_id: 'other-timeline', is_shot: false },
    { timeline_id: 'created-timeline', is_shot: false },
  ] };
  assert.equal(timelineFromList(page, 'created-timeline')?.timeline_id, 'created-timeline');
  assert.equal(timelineFromList(page, 'missing-timeline'), undefined);
});

test('a completed click and an existing project URL cannot select the new project scope', async () => {
  const previousProject = '36498405a10c4b2ab9a5412eaf22a9a5';
  const createdProject = '4dcb2321f23d451091785dec01757b74';
  const timeline = 'd0022034-8d26-5584-8a06-ff87ba3b3d6b';
  let current = new URL(`https://astrid.test/tools/video-editor?project=${previousProject}`);
  let navigated!: () => void;
  let matches!: (url: URL) => boolean;
  const page: Pick<Page, 'waitForURL' | 'url'> = {
    url: () => current.href,
    waitForURL: async (predicate) => {
      matches = typeof predicate === 'function' ? predicate : (url) => typeof predicate === 'string'
        ? url.href === predicate : predicate.test(url.href);
      if (!matches(current)) await new Promise<void>((resolve) => { navigated = resolve; });
    },
  };

  // The old broad URL assertion already passes before the async modal handler navigates.
  await Promise.resolve(); // Playwright click completion, not addNewProject completion.
  assert.match(current.href, /\/tools\/video-editor\?project=/);
  const earlyProjectId = new URL(page.url()).searchParams.get('project');
  let settled = false;
  const selected = waitForCreatedProjectUrl(page, createdProject, { timeout: 90_000 })
    .then((url) => { settled = true; return url; });
  await new Promise<void>((resolve) => setImmediate(resolve));
  assert.equal(settled, false);
  assert.equal(matches(new URL(`https://astrid.test/tools/video-editor?project=${previousProject}&timeline=${timeline}`)), false);
  assert.equal(matches(new URL(`https://astrid.test/other?project=${createdProject}`)), false);

  current = new URL(`https://astrid.test/tools/video-editor?project=${createdProject}&timeline=${timeline}`);
  assert.equal(matches(current), true);
  navigated();
  const selectedUrl = await selected;
  assert.equal(earlyProjectId, previousProject);
  assert.notEqual(earlyProjectId, selectedUrl.searchParams.get('project'));
  assert.deepEqual({ projectId: selectedUrl.searchParams.get('project'), timelineId: selectedUrl.searchParams.get('timeline') },
    { projectId: createdProject, timelineId: timeline });
});
