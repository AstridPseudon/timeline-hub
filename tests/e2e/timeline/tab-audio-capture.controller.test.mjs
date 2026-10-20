import assert from 'node:assert/strict';
import {test} from 'node:test';
import {
  assertFingerprintUnchanged,
  assertGrant,
  BROWSER_EXECUTABLE,
  BROWSER_VERSION,
  PROFILE,
  renderGraphFingerprint,
} from './tab-audio-capture.controller.mjs';

const fingerprint = {
  sourceSha: 'a'.repeat(40),
  sourceTree: 'b'.repeat(40),
  fullTrackedHash: 'c'.repeat(64),
  inputHash: 'd'.repeat(64),
  packageGraphHash: 'e'.repeat(64),
  node: {version: 'v20.19.4', executableSha256: 'f'.repeat(64)},
  browser: {tree: {sha256: '1'.repeat(64)}, executableSha256: '2'.repeat(64)},
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
    '@banodoco/timeline-composition': {version: '0.0.8', tree: {sha256: '9'.repeat(64), fileCount: 77}},
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

test('render graph fingerprint resolves the package root and all frozen files', () => {
  assert.deepEqual(renderGraphFingerprint(), {
    '@remotion/player/dist/cjs/PlayerUI.js': '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    '@remotion/player/dist/cjs/use-player-methods.js': 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    '@remotion/player/dist/cjs/use-playback.js': '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    '@remotion/player/dist/esm/index.mjs': 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    'remotion/dist/esm/index.mjs': '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
    'remotion/dist/cjs/audio/shared-audio-tags.js': '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
  });
});
