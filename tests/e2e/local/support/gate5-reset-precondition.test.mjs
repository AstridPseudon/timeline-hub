import assert from 'node:assert/strict';
import test from 'node:test';
import { assertGate5ResetPrecondition } from './gate5-reset-precondition.ts';

// Offline control only: these request/response/outbox objects are mocked and do not prove a browser or Runtime journey.
const base = { revisionId: 'revision-before', publicationId: 'publication-before' };
const scope = { projectId: 'project-f2', timelineId: 'timeline-f2' };
const request = {
  api_version: 1, project_id: scope.projectId, timeline_id: scope.timelineId,
  base_revision_id: base.revisionId,
  base_publication_id: base.publicationId,
  commands: [{ op: 'clip.move', select: 'parent/clip:f2-app-clip', args: { on: 5 } }],
};
const data = {
  status: 'accepted', base_revision_id: base.revisionId, base_publication_id: base.publicationId,
  previous_revision_id: base.revisionId, previous_publication_id: base.publicationId,
  accepted_revision_id: 'revision-after', commands: request.commands,
  canonical_document: { project_id: scope.projectId, timeline_id: scope.timelineId,
    parent_revision: { revision_id: 'revision-after', payload: { clips: [{ id: 'f2-app-clip', at: 5 }] } } },
};
const response = { data, receipt: { receipt_id: 'publication-after', command_kind: 'timeline.commit', idempotency_key: 'setup-key', project_id: scope.projectId, result: data } };
const settled = [{ pending: null, intents: [] }];
const authoritativeHead = { revision_id: 'revision-after', publication_id: 'publication-after' };
const authoritativeRevision = { project_id: scope.projectId, timeline_id: scope.timelineId, revision_id: 'revision-after', payload: { clips: [{ id: 'f2-app-clip', at: 5 }] } };
const valid = {
  request, requestIdentity: request, responseRequest: request, requestIdempotencyKey: 'setup-key',
  responseStatus: 200, responseBody: response, expectedBase: base, expectedScope: scope,
  clipId: 'f2-app-clip', expectedPosition: 5, settledOutboxes: settled, authoritativeHead, authoritativeRevision,
};

const responseFor = (nextData) => ({ ...response, data: nextData, receipt: { ...response.receipt, result: nextData } });

test('Gate5 requires the real 0→5 response before the original reset', () => {
  assert.doesNotThrow(() => assertGate5ResetPrecondition(valid));
});

test('the isolated 0-start cannot satisfy a 5→0 reset precondition without a setup mutation', () => {
  const oldStartData = { ...data, canonical_document: { parent_revision: { revision_id: 'revision-after', payload: { clips: [{ id: 'f2-app-clip', at: 0 }] } } } };
  assert.throws(() => assertGate5ResetPrecondition({
    ...valid, responseStatus: 200, responseBody: { data: oldStartData, receipt: { receipt_id: 'publication-old', result: oldStartData } },
    request: { ...request, commands: [{ ...request.commands[0], args: { on: 0 } }] },
  }), /requested position mismatch/);
});

test('Gate5 fails closed for non-200, missing response, invalid receipt, and mismatched position', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: 409 }), /response status 409/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: undefined, responseBody: undefined }), /response status/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, expectedPosition: 4 }), /requested position mismatch/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: { ...response, receipt: { ...response.receipt, result: {} } } }), /receipt does not match/);
  const mismatchedData = { ...data, canonical_document: { project_id: scope.projectId, timeline_id: scope.timelineId,
    parent_revision: { revision_id: 'revision-after', payload: { clips: [{ id: 'f2-app-clip', at: 4 }] } } } };
  assert.throws(() => assertGate5ResetPrecondition({
    ...valid, responseBody: responseFor(mismatchedData),
  }), /canonical position mismatch/);
});

test('Gate5 rejects unrelated responses and wrong scope, head, base, previous, key, or command identity', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseRequest: {} }), /not for the setup request/);
  const wrongScopeRequest = { ...request, project_id: 'other-project' };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: wrongScopeRequest, requestIdentity: wrongScopeRequest, responseRequest: wrongScopeRequest }), /project scope/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeHead: { revision_id: 'other', publication_id: authoritativeHead.publication_id } }), /authoritative head/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: { ...request, base_revision_id: 'other' }, requestIdentity: request, responseRequest: request }), /base revision/);
  const wrongPrevious = { ...data, previous_revision_id: 'other' };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseBody: responseFor(wrongPrevious) }), /previous head/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, requestIdempotencyKey: 'other-key' }), /idempotency/);
  const wrongCommand = { ...request, commands: [{ ...request.commands[0], op: 'track.create' }] };
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, request: wrongCommand, requestIdentity: wrongCommand, responseRequest: wrongCommand }), /not a clip move/);
});

test('Gate5 rejects an authoritative readback with the wrong scope or position', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeRevision: { ...authoritativeRevision, timeline_id: 'other-timeline' } }), /authoritative revision scope/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, authoritativeRevision: { ...authoritativeRevision, payload: { clips: [{ id: 'f2-app-clip', at: 4 }] } } }), /authoritative position/);
});
