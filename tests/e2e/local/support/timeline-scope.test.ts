import assert from 'node:assert/strict';
import test from 'node:test';
import { isCreatedProjectResponse, readCreatedProjectResponse, timelineBase, timelineFromList, waitForCreatedProjectResponse } from './timeline-scope.ts';
import type { Request, Response } from '@playwright/test';

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

test('context response observation matches the real project-create wire shape', async () => {
  const submittedName = ' Direct Journey 927865 ';
  const normalizedName = submittedName.trim();
  const bridgeBase = 'https://astrid.test/api/astrid';
  const request = {
    method: () => 'POST',
    postData: () => JSON.stringify({
      name: normalizedName,
      slug: 'direct-journey-927865',
      metadata: { aspect_ratio: '16:9' },
    }),
  } as unknown as Request;
  const response = {
    request: () => request,
    status: () => 201,
    url: () => 'https://astrid.test/api/astrid/v1/projects',
    json: async () => ({
      data: {
        project_id: 'created-project', slug: 'direct-journey-927865', name: normalizedName,
        metadata: { aspect_ratio: '16:9' }, version: 1,
        created_at: '2026-10-20T00:00:00.000Z', updated_at: '2026-10-20T00:00:00.000Z', archived: false,
      },
      receipt: {
        receipt_id: 'receipt-project-create', command_kind: 'project.create', idempotency_key: 'key-project-create',
        request_hash: 'hash-project-create', project_id: 'created-project', project_seq: [1, 1], event_ids: ['event-project-create'],
        result: {}, created_at: '2026-10-20T00:00:00.000Z',
      },
    }),
  } as unknown as Response;
  let observedEvent = '';
  // This fixture exposes only the context event surface. The old page-level
  // waiter therefore cannot observe this real service-worker-routed response.
  const context = {
    waitForEvent: async (event: string, options: { predicate: (candidate: Response) => boolean }) => {
      observedEvent = event;
      assert.equal(options.predicate(response), true);
      return response;
    },
  };

  const created = await waitForCreatedProjectResponse(context, submittedName, bridgeBase, { timeout: 90_000 });
  assert.equal(observedEvent, 'response');
  assert.equal(created, response);
  assert.deepEqual(await readCreatedProjectResponse(response, submittedName, bridgeBase), {
    data: { project_id: 'created-project', name: normalizedName },
    receipt: {
      receipt_id: 'receipt-project-create', command_kind: 'project.create', idempotency_key: 'key-project-create',
      request_hash: 'hash-project-create', project_id: 'created-project', project_seq: [1, 1], event_ids: ['event-project-create'],
      result: {}, created_at: '2026-10-20T00:00:00.000Z',
    },
  });

  const responseAt = (url: string) => ({ ...response, url: () => url }) as unknown as Response;
  assert.equal(isCreatedProjectResponse(responseAt('https://other.test/api/astrid/v1/projects'), submittedName, bridgeBase), false);
  assert.equal(isCreatedProjectResponse(responseAt('https://astrid.test/api/runtime/v1/projects'), submittedName, bridgeBase), false);
  assert.equal(isCreatedProjectResponse({ ...response, request: () => ({ ...request, method: () => 'GET' }) } as unknown as Response, submittedName, bridgeBase), false);
  assert.equal(isCreatedProjectResponse(response, 'another project', bridgeBase), false);
  assert.equal(isCreatedProjectResponse({ ...response, status: () => 200 } as unknown as Response, submittedName, bridgeBase), false);
  assert.equal(isCreatedProjectResponse({ ...response, request: () => ({ ...request, postData: () => '{' }) } as unknown as Response, submittedName, bridgeBase), false);
  await assert.rejects(
    readCreatedProjectResponse({ ...response, json: async () => ({ data: { project_id: 'created-project' } }) } as unknown as Response, submittedName, bridgeBase),
    /data and receipt/,
  );
});
