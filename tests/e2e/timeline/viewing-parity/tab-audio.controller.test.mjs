import assert from 'node:assert/strict';
import { test } from 'node:test';
import { APP13, AGENT13, RUNTIME13, COMPOSITION13, CONTROL, assertCandidateTuple } from './tab-audio.controller.mjs';

test('READY controller identifies the exact pending App13 candidate and matching Agent13 tuple', () => {
  assertCandidateTuple({ app: APP13, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 });
  assert.equal(APP13.status, 'pending-consumer-adoption');
  assert.equal(CONTROL.physicalMixClaim, false);
  assert.equal(CONTROL.app13Consumer, 'pending');
  assert.equal(CONTROL.ownLeafOnly, true);
  assert.equal(CONTROL.all77BytesPinned, true);
});

test('controller rejects a changed source tuple before capture', () => {
  assert.throws(() => assertCandidateTuple({ app: { ...APP13, tree: 'changed' }, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 }), /app13 candidate tuple changed/);
});
