import assert from 'node:assert/strict';
import test from 'node:test';
import { assertGate5ResetPrecondition } from './gate5-reset-precondition.ts';

// Offline control only: these request/response/outbox objects are mocked and do not prove a browser or Runtime journey.
const base = { revisionId: 'revision-before', publicationId: 'publication-before' };
const request = {
  base_revision_id: base.revisionId,
  base_publication_id: base.publicationId,
  commands: [{ op: 'clip.move', select: 'parent/clip:f2-app-clip', args: { on: 5 } }],
};
const data = {
  status: 'accepted', accepted_revision_id: 'revision-after',
  canonical_document: { parent_revision: { revision_id: 'revision-after', payload: { clips: [{ id: 'f2-app-clip', at: 5 }] } } },
};
const response = { data, receipt: { receipt_id: 'publication-after', result: data } };
const settled = [{ pending: null, intents: [] }];
const valid = {
  request, responseStatus: 200, responseBody: response, expectedBase: base,
  clipId: 'f2-app-clip', expectedPosition: 5, settledOutboxes: settled,
};

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

test('Gate5 fails closed for non-200, missing response, and mismatched position', () => {
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: 409 }), /response status 409/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, responseStatus: undefined, responseBody: undefined }), /response status/);
  assert.throws(() => assertGate5ResetPrecondition({ ...valid, expectedPosition: 4 }), /requested position mismatch/);
  const mismatchedData = { ...data, canonical_document: { parent_revision: { revision_id: 'revision-after', payload: { clips: [{ id: 'f2-app-clip', at: 4 }] } } } };
  assert.throws(() => assertGate5ResetPrecondition({
    ...valid, responseBody: { ...response, data: mismatchedData, receipt: { ...response.receipt, result: mismatchedData } },
  }), /canonical position mismatch/);
});
