import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  APP13, AGENT13, RUNTIME13, RUNTIME13_ARTIFACT, COMPOSITION13, CHROME155, CONTROL, NODE20,
  VIEWING_QUALIFICATIONS,
  MISSING_OWNER_PORTS, OWNER_PORTS,
  assertCandidateTuple, assertRuntimeArtifact, assertCompletedAppConsumer, assertNode20, assertOwnedShortTemp, assertOwnerPorts,
} from './tab-audio.controller.mjs';

test('READY controller identifies the integrated App13 and verified normal13 tuple', () => {
  assertCandidateTuple({ app: APP13, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 });
  assert.equal(APP13.source, 'ea38656fe62950440b36cafee780698cff2c3f9c');
  assert.equal(APP13.status, 'adopted');
  assert.equal(AGENT13.status, 'verified');
  assert.equal(RUNTIME13.status, 'qualified-viewing');
  assert.equal(RUNTIME13.ownerAck, 'pending');
  assertRuntimeArtifact();
  assert.notEqual(RUNTIME13.source, RUNTIME13_ARTIFACT.source);
  assert.equal(CONTROL.physicalMixClaim, false);
  assert.equal(CONTROL.app13Consumer, 'adopted');
  assert.equal(CONTROL.ownLeafOnly, true);
  assert.equal(CONTROL.all77BytesPinned, true);
});
test('controller rejects a changed source tuple before capture', () => {
  assert.throws(() => assertCandidateTuple({ app: { ...APP13, tree: 'changed' }, agent: AGENT13, runtime: RUNTIME13, composition: COMPOSITION13 }), /app13 candidate tuple changed/);
  assert.throws(() => assertCandidateTuple({ app: APP13, agent: AGENT13,
    runtime: { ...RUNTIME13, source: RUNTIME13_ARTIFACT.source, tree: RUNTIME13_ARTIFACT.tree }, composition: COMPOSITION13 }),
  /runtime13 candidate tuple changed/);
  assert.throws(() => assertRuntimeArtifact({ ...RUNTIME13_ARTIFACT, version: 'sha256:wrong' }), /artifact producer facts changed/);
});

test('readiness reports the current flat owner-port status', () => {
  assert.deepEqual(MISSING_OWNER_PORTS, []);
  assert.equal(OWNER_PORTS.find(({ port }) => port === 'complete-cap-current-join')?.source, 'a8283307a7a5537a95988031b385ef28df7524ea');
  assert.equal(OWNER_PORTS.find(({ port }) => port === 'native-frame-fixture')?.source, 'f084855eff0c40a464a166297d43536458ee4ca4');
  assert.equal(OWNER_PORTS.find(({ port }) => port === 'player-tab-audio-instrument')?.source, '379c19509ddb4f100d192c0e52d1307abc3c7a00');
  assert.equal(OWNER_PORTS.find(({ port }) => port === 'public13-normal-pin')?.source, '6f0cdc7df95fe3c9b2d491d6fcb39b754fa212bd');
  assert.equal(OWNER_PORTS.some(({ port }) => port === 'track-inspector-preservation'), true);
  assert.deepEqual(assertOwnerPorts(), OWNER_PORTS);
});

test('one-root host catalog is a Viewing-owned qualification with source and test evidence', () => {
  assert.deepEqual(VIEWING_QUALIFICATIONS, [{
    owner: 'Viewing',
    port: 'public13-one-root-host-catalog',
    status: 'qualified',
    source: RUNTIME13.source,
    tree: RUNTIME13.tree,
    sourceTuple: {
      agent: { source: AGENT13.source, tree: AGENT13.tree },
      runtime: { source: RUNTIME13.source, tree: RUNTIME13.tree },
    },
    evidence: {
      central: { test: 'central14650', result: 'PASS', passed: 1 },
      oneRootHost: { test: 'one-root-host', result: 'PASS', passed: 1, duration: '44.14s' },
    },
  }]);
  assert.equal(OWNER_PORTS.some(({ port }) => port === 'public13-one-root-host-catalog'), false);
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

