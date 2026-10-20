import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  APP13, AGENT13, RUNTIME13, COMPOSITION13, CHROME155, CONTROL,
  assertCandidateTuple, assertCompletedAppConsumer, assertOwnedShortTemp,
} from './tab-audio.controller.mjs';

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

test('readiness remains closed while App13 consumer adoption is pending', () => {
  assert.throws(() => assertCompletedAppConsumer(process.cwd()), /App13 consumer adoption is pending/);
});

test('Chrome155 identity uses the complete executable and tree pins', () => {
  assert.match(CHROME155.sha256, /^[a-f0-9]{64}$/);
  assert.equal(CHROME155.treeSha256, '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e');
  assert.equal(CHROME155.treeFileCount, 255);
});

test('short owned temp calibration leaves no directory behind', () => {
  const directory = assertOwnedShortTemp();
  assert.equal(directory.startsWith('/tmp/timeline-tab-audio-'), true);
});
