import assert from 'node:assert/strict';
import {test} from 'node:test';
import {chmodSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync, symlinkSync, linkSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {tmpdir} from 'node:os';
import {
  assertFingerprintUnchanged,
  assertPhysicalGraph,
  assertGrant,
  BROWSER_EXECUTABLE,
  BROWSER_VERSION,
  hashTree,
  PROFILE,
} from './tab-audio-capture.controller.mjs';

const fingerprint = {
  sourceSha: 'a'.repeat(40),
  sourceTree: 'b'.repeat(40),
  fullTrackedHash: 'c'.repeat(64),
  inputHash: 'd'.repeat(64),
  packageGraphHash: 'e'.repeat(64),
  node: {version: 'v20.19.4', executableSha256: 'f'.repeat(64)},
  browser: {tree: {sha256: '1'.repeat(64)}, executableSha256: '2'.repeat(64)},
  privateGraph: {root: '/private/fixture/node_modules', tree: {sha256: 'a'.repeat(64), fileCount: 123}},
  discovery: {testCount: 1, sha256: 'b'.repeat(64)},
  packages: {
    '@playwright/test': {version: '1.60.0', tree: {sha256: '3'.repeat(64)}},
    playwright: {version: '1.60.0', tree: {sha256: '4'.repeat(64)}},
    'playwright-core': {version: '1.60.0', tree: {sha256: 'a'.repeat(64)}},
    react: {version: '18.3.1', tree: {sha256: '5'.repeat(64)}},
    'react-dom': {version: '18.3.1', tree: {sha256: '6'.repeat(64)}},
    remotion: {version: '4.0.509', tree: {sha256: '7'.repeat(64)}},
    '@remotion/player': {version: '4.0.509', tree: {sha256: '8'.repeat(64)}},
    '@remotion/media': {version: '4.0.509', tree: {sha256: 'b'.repeat(64)}},
    '@remotion/web-renderer': {version: '4.0.509', tree: {sha256: 'c'.repeat(64)}},
    '@remotion/layout-utils': {version: '4.0.509', tree: {sha256: 'd'.repeat(64)}},
    '@banodoco/timeline-composition': {version: '0.0.12', tree: {sha256: '9'.repeat(64), fileCount: 77}},
  },
};
fingerprint.renderGraphHashes = {
  '@remotion/player/dist/cjs/PlayerUI.js': '1'.repeat(64),
  '@remotion/player/dist/cjs/use-player-methods.js': '2'.repeat(64),
  '@remotion/player/dist/cjs/use-playback.js': '3'.repeat(64),
  '@remotion/player/dist/esm/index.mjs': '4'.repeat(64),
  'remotion/dist/esm/index.mjs': '5'.repeat(64),
  'remotion/dist/cjs/audio/shared-audio-tags.js': '6'.repeat(64),
};

function grant() {
  return {
    approved: true,
    profile: PROFILE,
    browserExecutable: BROWSER_EXECUTABLE,
    browserVersion: BROWSER_VERSION,
    backendOrder: ['tab', 'private-pulse'],
    sourceSha: fingerprint.sourceSha,
    sourceTree: fingerprint.sourceTree,
    fullTrackedHash: fingerprint.fullTrackedHash,
    inputHash: fingerprint.inputHash,
    packageGraphHash: fingerprint.packageGraphHash,
    finalSha: fingerprint.sourceSha,
    nodeVersion: fingerprint.node.version,
    nodeExecutableSha256: fingerprint.node.executableSha256,
    browserTreeSha256: fingerprint.browser.tree.sha256,
    browserExecutableSha256: fingerprint.browser.executableSha256,
    packages: fingerprint.packages,
    renderGraphHashes: fingerprint.renderGraphHashes,
    privateGraph: fingerprint.privateGraph,
    discovery: fingerprint.discovery,
    environmentApprovalReference: 'manager-grant',
  };
}

test('grant requires final SHA to match the actual committed source, not only an environment value', () => {
  assert.doesNotThrow(() => assertGrant(grant(), fingerprint, fingerprint.sourceSha));
  assert.throws(() => assertGrant({...grant(), finalSha: '9'.repeat(40)}, fingerprint, fingerprint.sourceSha), /committed source SHA/);
  assert.throws(() => assertGrant(grant(), fingerprint, '9'.repeat(40)), /committed source SHA/);
});

test('grant rejects changed full source, selected input, browser, or package identity', () => {
  for (const field of ['sourceTree', 'fullTrackedHash', 'inputHash', 'packageGraphHash']) {
    assert.throws(() => assertGrant({...grant(), [field]: '9'.repeat(field.includes('Tree') ? 40 : 64)}, fingerprint, fingerprint.sourceSha), new RegExp(field));
  }
  assert.throws(() => assertGrant({...grant(), browserTreeSha256: '9'.repeat(64)}, fingerprint, fingerprint.sourceSha), /Chrome155 tree/);
  assert.throws(() => assertGrant({...grant(), packages: {}}, fingerprint, fingerprint.sourceSha), /package graph/);
  assert.throws(() => assertGrant({...grant(), renderGraphHashes: {}}, fingerprint, fingerprint.sourceSha), /Remotion\/Player render graph/);
});

test('postflight rejects a dependency graph change', () => {
  assert.doesNotThrow(() => assertFingerprintUnchanged(fingerprint, fingerprint));
  assert.throws(() => assertFingerprintUnchanged(fingerprint, {
    ...fingerprint,
    inputHash: '9'.repeat(64),
  }), /inputHash/);
  assert.throws(() => assertFingerprintUnchanged(fingerprint, {
    ...fingerprint,
    browser: {...fingerprint.browser, tree: {sha256: '9'.repeat(64)}},
  }), /browser/);
});

test('hashTree uses canonical whole-tuple framing for physical fixtures', () => {
  const root = mkdtempSync(join(tmpdir(), 'tab-audio-hash-tree-'));
  const executable = join(root, 'bin', 'run.sh');
  const regular = join(root, 'alpha.txt');
  try {
    mkdirSync(dirname(executable));
    writeFileSync(regular, 'alpha\n');
    writeFileSync(executable, '#!/bin/sh\n');
    chmodSync(regular, 0o644);
    chmodSync(executable, 0o755);

    const expected = {sha256: '8a79f98987096e97cc953ecbd5af33617f60b15ab9280fa50e5a3e9b803b3218', fileCount: 2};
    // This vector is the pre-fix per-tuple concatenation for the same fixture.
    const legacyPerTupleFraming = '54b43f4ffd704bcedefb2f7ab19c47de86b67672100b9f9106524fea964b6a64';
    assert.deepEqual(hashTree(root), expected);
    assert.notEqual(hashTree(root).sha256, legacyPerTupleFraming);

    writeFileSync(regular, 'changed\n');
    assert.notEqual(hashTree(root).sha256, expected.sha256);
    writeFileSync(regular, readFileSync(regular, 'utf8').replace('changed', 'alpha'));
    chmodSync(regular, 0o755);
    assert.notEqual(hashTree(root).sha256, expected.sha256);
  } finally {
    rmSync(root, {recursive: true, force: true});
  }
});

test('whole private graph and real discovery are mandatory grant bindings', () => {
  assert.throws(() => assertGrant({...grant(), privateGraph: null}, fingerprint, fingerprint.sourceSha), /whole private graph/);
  assert.throws(() => assertGrant({...grant(), discovery: null}, fingerprint, fingerprint.sourceSha), /discovery proof/);
  assert.throws(() => assertGrant(grant(), {...fingerprint, privateGraph: null}, fingerprint.sourceSha), /whole private graph/);
});

test('physical graph accepts internal file links and rejects shared leaves, cycles and hardlinks', () => {
  const root = mkdtempSync(join(tmpdir(), 'tab-private-physical-'));
  try {
    writeFileSync(join(root, 'file'), 'private');
    symlinkSync('file', join(root, 'internal'));
    assert.doesNotThrow(() => assertPhysicalGraph(root));
    symlinkSync(root, join(root, 'cycle'));
    assert.throws(() => assertPhysicalGraph(root), /targets a directory/);
    rmSync(join(root, 'cycle'));
    symlinkSync('/etc/hosts', join(root, 'external'));
    assert.throws(() => assertPhysicalGraph(root), /escapes/);
    rmSync(join(root, 'external'));
    linkSync(join(root, 'file'), join(root, 'hardlink'));
    assert.throws(() => assertPhysicalGraph(root), /unshared files/);
  } finally {
    rmSync(root, {recursive: true, force: true});
  }
});

test('postflight rejects whole private graph or discovery identity changes', () => {
  for (const field of ['privateGraph', 'discovery']) {
    assert.throws(() => assertFingerprintUnchanged(fingerprint, {...fingerprint, [field]: null}), new RegExp(field));
  }
});
