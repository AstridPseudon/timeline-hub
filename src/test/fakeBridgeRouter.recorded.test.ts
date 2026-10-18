// Testing plan C2.2 / R-4: the fake is trusted only for operations whose REAL-daemon responses it reproduces.
// For each recorded case the fake implements, it must answer with the recorded status and the same JSON shape
// (same keys recursively, same value types). Operations the fake implements with no recorded case are listed
// at the bottom so they stay visibly untrusted.
import { describe, expect, it } from 'vitest';

import { createFakeBridgeRouter, type FakeBridgeRouter } from '@/test/fakeBridgeRouter.ts';
import { filled, jsonShape, PLACEHOLDER_VALUES, type RecordedResponse } from '@/test/recordedResponses.ts';

const BASE = 'http://bridge.fake/api/astrid';

/** Free-form subtrees that echo caller-supplied content (the task `spec`); only their presence is compared. */
const ECHOED_SPEC = new Set(['$.spec.spec', '$.data.spec.spec', '$.receipt.result.task.spec.spec']);

async function send(router: FakeBridgeRouter, fixture: RecordedResponse, body: unknown = fixture.request.body) {
  const response = await router.handle(new Request(`${BASE}${fixture.request.path}`, {
    method: fixture.request.method,
    headers: { 'Content-Type': 'application/json', 'Idempotency-Key': 'task' },
    body: body === null ? undefined : JSON.stringify(body),
  }));
  return { status: response.status, body: await response.json() as unknown };
}

/**
 * An admission the App itself could send. The fake validates the App's stricter request dialect
 * (`spec.family/params/output_policy`), so the recorded request (`spec: {prompt}`) is answered 422, not
 * 201: the fake is narrower than the daemon on requests, which is the safe direction. Its RESPONSES are
 * what is held to the fixture here.
 */
function appAdmissionRequest(fixture: RecordedResponse): Record<string, unknown> {
  const recorded = fixture.request.body as Record<string, unknown>;
  return {
    project: 'demo-project',
    capability_id: recorded.capability_id,
    capability_digest: recorded.capability_digest,
    schema_version: '1',
    input_object_ids: recorded.input_object_ids,
    spec: { family: 'image_generation', params: {}, output_policy: {} },
    storage_estimate: { scratch_bytes: 0, output_bytes: 0 },
    settlement_effect: {},
  };
}

describe('fakeBridgeRouter reproduces the recorded real-daemon responses', () => {
  it('task_admission_201: the App-shaped admission answers with the recorded status and shape', async () => {
    const fixture = filled('task_admission_201');
    const actual = await send(createFakeBridgeRouter(), fixture, appAdmissionRequest(fixture));
    expect(actual.status).toBe(fixture.status);
    expect(jsonShape(actual.body, ECHOED_SPEC)).toEqual(jsonShape(fixture.body, ECHOED_SPEC));
  });

  it('task_read_200: GET /v1/tasks/:id answers with the recorded status and shape', async () => {
    const admission = filled('task_admission_201');
    const read = filled('task_read_200');
    const router = createFakeBridgeRouter();
    const admitted = await send(router, admission, appAdmissionRequest(admission));
    const taskId = (admitted.body as { data: { task_id: string } }).data.task_id;

    const actual = await send(router, { ...read, request: { ...read.request, path: `/v1/tasks/${taskId}` } });

    expect(actual.status).toBe(read.status);
    expect(jsonShape(actual.body, ECHOED_SPEC)).toEqual(jsonShape(read.body, ECHOED_SPEC));
  });

  it('not_found_404: an unknown task answers with the recorded status and error shape', async () => {
    const fixture = filled('not_found_404');
    const actual = await send(createFakeBridgeRouter(), fixture);
    expect(actual.status).toBe(fixture.status);
    expect(jsonShape(actual.body)).toEqual(jsonShape(fixture.body));
  });

  it('validation_error_422: an invalid admission answers with the recorded status and error shape', async () => {
    const fixture = filled('validation_error_422');
    const actual = await send(createFakeBridgeRouter(), fixture);
    expect(actual.status).toBe(fixture.status);
    expect(jsonShape(actual.body)).toEqual(jsonShape(fixture.body));
    expect((actual.body as { code?: string }).code).toBe((fixture.body as { code: string }).code);
  });
});

describe('operations the fake implements without a recorded real-daemon response (untrusted)', () => {
  // Not held to a fixture; do not invent one. Record them from a real daemon before relying on them.
  const UNCOVERED = [
    'GET /v1/health', 'GET /v1/capabilities', 'GET /v1/projects', 'GET /v1/projects/:id/tasks',
    'POST /v1/tasks/:id/cancel', 'POST /v1/projects/:id/objects', 'GET /v1/projects/:id/objects',
    'GET /v1/objects/:id', 'GET /v1/projects/:id/generations', 'GET /v1/generations/:id',
    'GET /v1/generations/:id/variants',
  ];

  it('has no recorded case for events, managed outputs, composition publish or invalid cursors', async () => {
    const router = createFakeBridgeRouter();
    for (const path of [`/v1/events?limit=2`, `/v1/tasks/${PLACEHOLDER_VALUES.task_id}/managed-outputs`]) {
      const response = await router.handle(new Request(`${BASE}${path}`));
      // The fake has no route for these: it must fail loudly (404), never answer with an invented body.
      expect(response.status, path).toBe(404);
    }
    expect(UNCOVERED.length).toBeGreaterThan(0);
  });
});
