import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  APP13, AGENT13, RUNTIME13, COMPOSITION13, CHROME155, CONTROL, NODE20,
  MISSING_OWNER_PORTS, OWNER_PORTS,
  assertCandidateTuple, assertCompletedAppConsumer, assertNode20, assertOwnedShortTemp, assertOwnerPorts,
} from './tab-audio.controller.mjs';

test('READY controller identifies the integrated App13 and pending normal13 tuple', () => {
  assertCandidateTuple({ app: APP13, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 });
  assert.equal(APP13.source, 'ea38656fe62950440b36cafee780698cff2c3f9c');
  assert.equal(APP13.status, 'adopted');
  assert.equal(AGENT13.status, 'pending-normal13-owner-merge');
  assert.equal(RUNTIME13.status, 'pending-host-proof');
  assert.equal(CONTROL.physicalMixClaim, false);
  assert.equal(CONTROL.app13Consumer, 'adopted');
  assert.equal(CONTROL.ownLeafOnly, true);
  assert.equal(CONTROL.all77BytesPinned, true);
});

test('controller rejects a changed source tuple before capture', () => {
  assert.throws(() => assertCandidateTuple({ app: { ...APP13, tree: 'changed' }, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 }), /app13 candidate tuple changed/);
});

test('readiness reports the current flat owner-port blockers', () => {
  assert.deepEqual(MISSING_OWNER_PORTS.map(({ owner, port }) => `${owner}/${port}`), [
    'App/stored-cap8488',
    'Runtime/public13-one-root-host-catalog',
    'App/native-frame-fixture',
    'App/player-tab-audio-instrument',
    'Agent/public13-normal-pin',
  ]);
  assert.equal(OWNER_PORTS.find(({ port }) => port === 'stored-cap8488')?.source, '6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214');
  assert.equal(OWNER_PORTS.find(({ port }) => port === 'public13-one-root-host-catalog')?.source, RUNTIME13.source);
  assert.equal(OWNER_PORTS.some(({ port }) => port === 'track-inspector-preservation'), true);
  assert.throws(() => assertOwnerPorts(), /missing owner ports: App\/stored-cap8488 .* Runtime\/public13-one-root-host-catalog .* Agent\/public13-normal-pin/);
});

test('integrated App13 source remains a separate source guard', () => {
  assert.equal(APP13.status, 'adopted');
  assert.equal(APP13.source, 'ea38656fe62950440b36cafee780698cff2c3f9c');
  assert.equal(APP13.tree, '8bd8f741f7c8b28b8682aa960a658417f70c8522');
});

test('Chrome155 identity uses the complete executable and tree pins', () => {
  assert.match(CHROME155.sha256, /^[a-f0-9]{64}$/);
  assert.equal(CHROME155.treeSha256, '5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e');
  assert.equal(CHROME155.treeFileCount, 255);
});

test('Node identity rejects an unqualified executable', () => {
  assert.throws(() => assertNode20('/opt/node22/bin/node'), /selected Node must be v20\.19\.4/);
  assert.equal(NODE20.version, 'v20.19.4');
  assert.match(NODE20.sha256, /^[a-f0-9]{64}$/);
});

test('Node identity accepts the retained admitted executable and full hash', () => {
  assert.deepEqual(assertNode20(NODE20.executable), {
    version: NODE20.version,
    executable: NODE20.executable,
    sha256: NODE20.sha256,
  });
});

test('short owned temp calibration leaves no directory behind', () => {
  const directory = assertOwnedShortTemp();
  assert.equal(directory.startsWith('/tmp/timeline-tab-audio-'), true);
});
