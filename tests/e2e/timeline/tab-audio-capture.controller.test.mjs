import assert from 'node:assert/strict';
import {test} from 'node:test';
import {chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync, symlinkSync, linkSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {tmpdir} from 'node:os';
import {
  assertFingerprintUnchanged,
  assertPhysicalGraph,
  assertGrant,
  assertSocketPathBudget,
  allocateTaskTempDir,
  BROWSER_EXECUTABLE,
  BROWSER_VERSION,
  assertRunMode,
  cleanupTaskTempDir,
  hashTree,
  isolatedEnvironment,
  TASK_TEMP_PREFIX,
  TASK_TEMP_ROOT,
  WORKER_STATE_ROOT,
  PROFILE,
  RUN_MODE,
  NODE_EXECUTABLE,
  NODE_EXECUTABLE_SHA256,
} from './tab-audio-capture.controller.mjs';

const fingerprint = {
  sourceSha: 'a'.repeat(40),
  sourceTree: 'b'.repeat(40),
  runMode: RUN_MODE,
  fullTrackedHash: 'c'.repeat(64),
  inputHash: 'd'.repeat(64),
  packageGraphHash: 'e'.repeat(64),
  node: {version: 'v20.19.4', executable: NODE_EXECUTABLE, executableSha256: NODE_EXECUTABLE_SHA256},
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
    runMode: RUN_MODE,
    fullTrackedHash: fingerprint.fullTrackedHash,
    inputHash: fingerprint.inputHash,
    packageGraphHash: fingerprint.packageGraphHash,
    finalSha: fingerprint.sourceSha,
    nodeVersion: fingerprint.node.version,
    nodeExecutable: NODE_EXECUTABLE,
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

test('grant binds the actual stereo run mode and retained Node executable', () => {
  assert.doesNotThrow(() => assertGrant(grant(), fingerprint, fingerprint.sourceSha));
  assert.throws(() => assertGrant({...grant(), runMode: 'mono'}, fingerprint, fingerprint.sourceSha), /stereo run mode/);
  assert.throws(() => assertGrant({...grant(), nodeExecutable: '/tmp/old-node'}, fingerprint, fingerprint.sourceSha), /Node identity/);
});

test('Playwright environment refuses a mono run for the stereo probe', () => {
  const previous = process.env.TAB_AUDIO_RUN_MODE;
  try {
    process.env.TAB_AUDIO_RUN_MODE = 'mono';
    assert.throws(() => assertRunMode(), /TAB_AUDIO_RUN_MODE=stereo/);
    process.env.TAB_AUDIO_RUN_MODE = RUN_MODE;
    assert.doesNotThrow(() => assertRunMode());
  } finally {
    if (previous === undefined) delete process.env.TAB_AUDIO_RUN_MODE;
    else process.env.TAB_AUDIO_RUN_MODE = previous;
  }
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

test('physical graph accepts internal file links and rejects shared leaves, cycles and external hardlinks', () => {
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
    assert.doesNotThrow(() => assertPhysicalGraph(root));
    const outside = mkdtempSync(join(tmpdir(), 'tab-private-external-hardlink-'));
    try {
      linkSync(join(root, 'file'), join(outside, 'shared'));
      assert.throws(() => assertPhysicalGraph(root), /unshared files/);
    } finally {
      rmSync(outside, {recursive: true, force: true});
    }
  } finally {
    rmSync(root, {recursive: true, force: true});
  }
});

test('postflight rejects whole private graph or discovery identity changes', () => {
  for (const field of ['privateGraph', 'discovery']) {
    assert.throws(() => assertFingerprintUnchanged(fingerprint, {...fingerprint, [field]: null}), new RegExp(field));
  }
});

test('Chrome gets one short owned temp while caches and output stay in this worker folder', () => {
  const previous = process.env.PLAYWRIGHT_OUTPUT_DIR;
  const previousTaskTemp = process.env.TAB_AUDIO_TASK_TMPDIR;
  const taskTempDir = allocateTaskTempDir();
  const preexistingTempDir = mkdtempSync(join(TASK_TEMP_ROOT, TASK_TEMP_PREFIX));
  try {
    delete process.env.PLAYWRIGHT_OUTPUT_DIR;
    process.env.TAB_AUDIO_TASK_TMPDIR = taskTempDir;
    const isolated = isolatedEnvironment();
    assert.equal(isolated.TMPDIR, taskTempDir);
    assert.equal(isolated.TMP, taskTempDir);
    assert.equal(isolated.TEMP, taskTempDir);
    assert.ok(isolated.TMPDIR.startsWith(`${TASK_TEMP_ROOT}/${TASK_TEMP_PREFIX}`));
    const socketBudget = assertSocketPathBudget(WORKER_STATE_ROOT, taskTempDir);
    assert.equal(socketBudget.oldPath, `${WORKER_STATE_ROOT}/com.google.Chrome.12345678901234567890/SingletonSocket`);
    assert.equal(socketBudget.newPath, `${taskTempDir}/com.google.Chrome.12345678901234567890/SingletonSocket`);
    assert.ok(socketBudget.oldLength > 108);
    assert.ok(socketBudget.newLength < 108);
    for (const key of ['XDG_CACHE_HOME', 'XDG_CONFIG_HOME', 'PWTEST_CACHE_DIR', 'PLAYWRIGHT_OUTPUT_DIR']) {
      assert.ok(isolated[key].startsWith(`${WORKER_STATE_ROOT}/`));
    }
    assert.equal(isolated.NODE_PATH, '');
    assert.equal(isolated.TAB_AUDIO_RUN_MODE, RUN_MODE);
    process.env.PLAYWRIGHT_OUTPUT_DIR = '/outside-worker/output';
    assert.throws(() => isolatedEnvironment(), /own worker folder/);
    assert.throws(() => cleanupTaskTempDir(preexistingTempDir), /not allocated by this process/);
    assert.ok(existsSync(preexistingTempDir));
  } finally {
    if (previous === undefined) delete process.env.PLAYWRIGHT_OUTPUT_DIR;
    else process.env.PLAYWRIGHT_OUTPUT_DIR = previous;
    if (previousTaskTemp === undefined) delete process.env.TAB_AUDIO_TASK_TMPDIR;
    else process.env.TAB_AUDIO_TASK_TMPDIR = previousTaskTemp;
    cleanupTaskTempDir(taskTempDir);
    rmSync(preexistingTempDir, {recursive: true, force: true});
  }
});

test('hashTree sorts complete relative paths before hashing directory-prefix siblings', () => {
  const root = mkdtempSync(join(tmpdir(), 'tab-private-tree-order-'));
  try {
    mkdirSync(join(root, 'a'));
    writeFileSync(join(root, 'a', 'z.txt'), 'nested');
    writeFileSync(join(root, 'a.txt'), 'sibling');
    assert.deepEqual(hashTree(root), {sha256: '8c84a47ff6d2cc90f918befafc12fffa49067d15daf5941674749c00a0cd5539', fileCount: 2});
  } finally {
    rmSync(root, {recursive: true, force: true});
  }
});
