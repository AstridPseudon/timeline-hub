#!/usr/bin/env node

/**
 * Offline source preflight for the matched parent-media browser gate.
 *
 * This composes already-approved source units; it does not implement a media
 * producer, change the command contract, or launch the gate. The manager may
 * run the optional collection step after the exact source pair is composed.
 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import {
  accessSync, constants, existsSync, readFileSync, realpathSync, statSync,
} from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

export const PARENT_MEDIA_DELIVERY = Object.freeze({
  commit: '2fb03f7e2a8d70ca552c6417387f03e81686791f',
  parent: '780c502368cb6eb379cf3848af7009067c7cd744',
  approvedRowCommit: '6c3d53a281ea326fe274a9d082f5a1e7a3489300',
  approvedRowTree: '0b8cfa7981eb357cf66347daf5042337079247fb',
  paths: Object.freeze([
    'src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx',
    'src/tools/video-editor/hooks/useAssetManagement.ts',
    'src/tools/video-editor/hooks/useExternalDrop.test.tsx',
    'src/tools/video-editor/hooks/useExternalDrop.ts',
    'src/tools/video-editor/lib/external-drop-utils.ts',
    'tests/e2e/local/support/run-parent-manual-drop-evidence.sh',
  ]),
});

export const PARENT_MEDIA_CONSTRUCTION = Object.freeze({
  commit: '32e997454b76378ba04505f894cd60fcddfe95b6',
  paths: Object.freeze([
    'src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx',
    'src/tools/video-editor/hooks/useTimelineState.ts',
  ]),
});

export const PARENT_MEDIA_DRIVER = Object.freeze({
  commit: '780c502368cb6eb379cf3848af7009067c7cd744',
  tree: '8eed52bb7f8555c7765a8b485e00920bbf906639',
  evidencePaths: Object.freeze([
    'src/integrations/runtime/mediaImport.test.ts',
    'tests/e2e/local/support/app.ts',
    'tests/e2e/local/three-products.spec.ts',
  ]),
});

export const PARENT_MEDIA_RUNTIME = Object.freeze({
  agentCommit: '3c4f6de4fa777323b3386c01c7266b619b86af6d',
  agentTree: 'aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c',
  runtimeCommit: '202074110717146fc7f08af2306a8dd7f695b0b1',
  runtimeTree: 'ee39286bd0eb27d4075074cc4785d6d15e33f243',
  producerCommit: 'a0dca16975dfe8f5e762703b99d9791a16cf7fd7',
  producerTree: '4b7dd0fe44be973c344bab3de568eaf0bdd28476',
  artifactVersion: 'sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0',
  manifestSha256: 'ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815',
  schemaSha256: '6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d',
  artifactCount: 75,
});

export const PARENT_MEDIA_PUBLIC13 = Object.freeze({
  archiveSha256: '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
  archive: 'banodoco-timeline-composition-0.0.13.tgz',
  regularFileCount: 77,
});

export const PARENT_MEDIA_ROW_TESTS = Object.freeze([
  ...PARENT_MEDIA_DELIVERY.paths,
  ...PARENT_MEDIA_DRIVER.evidencePaths,
  ...PARENT_MEDIA_CONSTRUCTION.paths,
]);

const FULL_SHA = /^[a-f0-9]{40}$/;

function fail(message) {
  throw new Error(`[current014/parent-media] ${message}`);
}

function required(env, name) {
  const value = env[name]?.trim();
  if (!value) fail(`${name} is required; no moving-repo default is allowed`);
  return value;
}

function requiredSha(env, name) {
  const value = required(env, name);
  if (!FULL_SHA.test(value)) fail(`${name} must be a full 40-character lowercase SHA`);
  return value;
}

function requiredDirectory(env, name, { privateNodeModules = false } = {}) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value) || !statSync(value).isDirectory()) fail(`${name} must name an existing directory`);
  const resolved = realpathSync(value);
  if (privateNodeModules) {
    const shared = ['/home/user/work/app/node_modules']
      .filter((candidate) => existsSync(candidate))
      .map((candidate) => realpathSync(candidate));
    if (shared.includes(resolved)) fail(`${name} resolves to the shared App install`);
  }
  return resolved;
}

function requiredFile(env, name, { executable = false } = {}) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value) || !statSync(value).isFile()) fail(`${name} must name an existing file`);
  if (executable) {
    try { accessSync(value, constants.X_OK); } catch { fail(`${name} must name an executable file`); }
  }
  return value;
}

function git(root, ...args) {
  try {
    return execFileSync('git', ['-C', root, ...args], {
      encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (error) {
    fail(`git ${args.join(' ')} failed in ${root}: ${error.message}`);
  }
}

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function sha256File(file) {
  return sha256(readFileSync(file));
}

function assertExact(actual, expected, label) {
  if (actual !== expected) fail(`${label} is ${actual}, expected ${expected}`);
}

export function readParentMediaInputs(env = process.env, appRoot = process.cwd()) {
  const appTree = requiredSha(env, 'TIMELINE_PARENT_MEDIA_APP_TREE');
  assertExact(requiredSha(env, 'TIMELINE_PARENT_MEDIA_DELIVERY_SHA'), PARENT_MEDIA_DELIVERY.commit, 'delivery source');
  assertExact(requiredSha(env, 'TIMELINE_PARENT_MEDIA_CONSTRUCTION_SHA'), PARENT_MEDIA_CONSTRUCTION.commit, 'HOME construction source');
  assertExact(requiredSha(env, 'TIMELINE_PARENT_MEDIA_DRIVER_SHA'), PARENT_MEDIA_DRIVER.commit, 'current driver source');
  if (!path.isAbsolute(appRoot)) fail(`App root must be absolute: ${appRoot}`);
  const app = realpathSync(appRoot);
  return Object.freeze({
    app,
    appTree,
    agent: requiredDirectory(env, 'ASTRID_CHECKOUT'),
    runtime: requiredDirectory(env, 'ASTRID_RUNTIME_CHECKOUT'),
    runtimeProducer: requiredDirectory(env, 'TIMELINE_PARENT_MEDIA_RUNTIME_PRODUCER_CHECKOUT'),
    agentPython: requiredFile(env, 'ASTRID_PYTHON', { executable: true }),
    runtimePython: requiredFile(env, 'ASTRID_RUNTIME_PYTHON', { executable: true }),
    privateNodeModules: requiredDirectory(env, 'PRIVATE13_NODE_MODULES', { privateNodeModules: true }),
    chromium: requiredFile(env, 'PLAYWRIGHT_CHROMIUM_EXECUTABLE', { executable: true }),
    browsersPath: requiredDirectory(env, 'PLAYWRIGHT_BROWSERS_PATH'),
    node: requiredFile(env, 'TIMELINE_PARENT_MEDIA_NODE', { executable: true }),
    viteBin: requiredFile(env, 'TIMELINE_PARENT_MEDIA_VITE_BIN'),
    playwrightCli: requiredFile(env, 'TIMELINE_PARENT_MEDIA_PLAYWRIGHT_CLI'),
    shortTmpDir: requiredDirectory(env, 'TIMELINE_PARENT_MEDIA_SHORT_TMPDIR'),
    childTmpDir: requiredDirectory(env, 'TIMELINE_PARENT_MEDIA_CHILD_TMPDIR'),
  });
}

function checkClean(root, label) {
  const status = git(root, 'status', '--porcelain=v1', '--untracked-files=all');
  if (status) fail(`${label} source is dirty:\n${status}`);
}

function checkPinnedCheckout(root, commit, tree, label) {
  assertExact(git(root, 'rev-parse', 'HEAD'), commit, `${label} source`);
  assertExact(git(root, 'rev-parse', 'HEAD^{tree}'), tree, `${label} tree`);
  checkClean(root, label);
}

function checkAncestor(root, ancestor, label) {
  try {
    execFileSync('git', ['-C', root, 'merge-base', '--is-ancestor', ancestor, 'HEAD'], { stdio: 'ignore' });
  } catch { fail(`${label} ${ancestor} is not an ancestor of the composed App source`); }
}

function checkBlob(root, source, file, label) {
  const expected = git(root, 'rev-parse', `${source}:${file}`);
  const actual = git(root, 'hash-object', file);
  assertExact(actual, expected, `${label} ${file}`);
}

function checkDriverCleanup(app) {
  const wrapper = path.join(app, 'tests/e2e/local/support/run-parent-manual-drop-evidence.sh');
  const source = readFileSync(wrapper, 'utf8');
  for (const marker of [
    "trap 'exit_handler' EXIT HUP INT TERM",
    'record_evidence',
    'evidence_recorded=1',
    'rm -rf -- "$run_root"',
    "--grep 'M2 real mounted manual video drop'",
  ]) if (!source.includes(marker)) fail(`parent evidence wrapper is missing cleanup/selector guard: ${marker}`);
}

export function checkParentMediaSources(input) {
  if (git(input.app, 'rev-parse', '--show-toplevel') !== input.app) fail(`App root is not the current checkout: ${input.app}`);
  assertExact(git(input.app, 'rev-parse', 'HEAD^{tree}'), input.appTree, 'App source tree');
  checkClean(input.app, 'App');
  checkAncestor(input.app, PARENT_MEDIA_DRIVER.commit, 'current 780 driver');
  checkAncestor(input.app, PARENT_MEDIA_DELIVERY.commit, 'approved current delivery');
  checkAncestor(input.app, PARENT_MEDIA_CONSTRUCTION.commit, 'approved HOME construction');
  for (const file of PARENT_MEDIA_DELIVERY.paths) checkBlob(input.app, PARENT_MEDIA_DELIVERY.commit, file, 'delivery');
  for (const file of PARENT_MEDIA_CONSTRUCTION.paths) checkBlob(input.app, PARENT_MEDIA_CONSTRUCTION.commit, file, 'construction');
  for (const file of PARENT_MEDIA_DRIVER.evidencePaths) checkBlob(input.app, PARENT_MEDIA_DRIVER.commit, file, '622/780 evidence driver');
  checkDriverCleanup(input.app);
  return Object.freeze({ appTree: input.appTree, rowTests: PARENT_MEDIA_ROW_TESTS });
}

function checkPublic13Archive(app) {
  const file = path.join(app, 'vendor/artifacts', PARENT_MEDIA_PUBLIC13.archive);
  if (!existsSync(file)) fail(`public13 Composition archive is missing: ${file}`);
  assertExact(sha256File(file), PARENT_MEDIA_PUBLIC13.archiveSha256, 'public13 Composition archive');
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8' }).trim().split('\n')
    .filter((member) => member && !member.endsWith('/'));
  if (members.length !== PARENT_MEDIA_PUBLIC13.regularFileCount || new Set(members).size !== members.length
    || members.some((member) => !member.startsWith('package/') || member.split('/').includes('..'))) {
    fail(`public13 Composition archive must contain exactly ${PARENT_MEDIA_PUBLIC13.regularFileCount} safe regular files`);
  }
}

function checkRuntimeArtifacts(agent, runtime, runtimeProducer) {
  checkPinnedCheckout(agent, PARENT_MEDIA_RUNTIME.agentCommit, PARENT_MEDIA_RUNTIME.agentTree, 'Agent');
  checkPinnedCheckout(runtime, PARENT_MEDIA_RUNTIME.runtimeCommit, PARENT_MEDIA_RUNTIME.runtimeTree, 'Runtime');
  checkPinnedCheckout(runtimeProducer, PARENT_MEDIA_RUNTIME.producerCommit, PARENT_MEDIA_RUNTIME.producerTree, 'Runtime producer');
  const file = path.join(runtime, 'contract/artifacts.json');
  const manifest = JSON.parse(readFileSync(file, 'utf8'));
  if (manifest.producer !== 'astrid-runtime') fail('Runtime artifact manifest has an unexpected producer');
  assertExact(sha256File(file), PARENT_MEDIA_RUNTIME.manifestSha256, 'Runtime artifact manifest');
  assertExact(manifest.version, PARENT_MEDIA_RUNTIME.artifactVersion, 'Runtime artifact version');
  assertExact(Object.keys(manifest.artifacts ?? {}).length, PARENT_MEDIA_RUNTIME.artifactCount, 'Runtime artifact count');
  for (const [relative, expected] of Object.entries(manifest.artifacts)) {
    const runtimeFile = path.join(runtime, relative);
    const producerFile = path.join(runtimeProducer, relative);
    if (!existsSync(runtimeFile) || !existsSync(producerFile)) fail(`Runtime artifact is missing: ${relative}`);
    assertExact(`sha256:${sha256File(runtimeFile)}`, expected, `Runtime artifact ${relative}`);
    assertExact(sha256File(runtimeFile), sha256File(producerFile), `Runtime/producer artifact ${relative}`);
  }
  const runtimeSchema = path.join(runtime, 'contract/schemas/edit-command.json');
  const agentSchema = path.join(agent, 'astrid/core/timeline/schema/edit-command.schema.json');
  assertExact(sha256File(runtimeSchema), PARENT_MEDIA_RUNTIME.schemaSha256, 'Runtime schema');
  assertExact(sha256File(runtimeSchema), sha256File(agentSchema), 'Agent/Runtime schema');
}

function checkOwnedExecutables(input) {
  for (const [label, executable] of [
    ['Agent Python', input.agentPython],
    ['Runtime Python', input.runtimePython],
  ]) {
    const result = spawnSync(executable, ['--version'], { stdio: 'ignore', shell: false });
    if (result.status !== 0) fail(`${label} guard failed (exit ${result.status ?? 'signal'})`);
  }
  const privateVite = path.relative(input.privateNodeModules, input.viteBin);
  if (privateVite.startsWith('..') || path.isAbsolute(privateVite) || privateVite !== '.bin/vite') {
    fail(`Vite must be the private graph bin: ${input.privateNodeModules}/.bin/vite`);
  }
  const privateChromium = path.relative(input.browsersPath, input.chromium);
  if (privateChromium.startsWith('..') || path.isAbsolute(privateChromium)) {
    fail(`Chromium must be inside the private browser path: ${input.browsersPath}`);
  }
}

export function checkParentMediaDependencies(input) {
  checkPublic13Archive(input.app);
  checkRuntimeArtifacts(input.agent, input.runtime, input.runtimeProducer);
  checkOwnedExecutables(input);
  const nodeVersion = spawnSync(input.node, [input.viteBin, '--version'], { cwd: input.app, stdio: 'pipe', shell: false });
  if (nodeVersion.status !== 0) fail(`Node+Vite guard failed (exit ${nodeVersion.status ?? 'signal'})`);
  if (input.childTmpDir === input.shortTmpDir) fail('short-child TMPDIR must be separate from the normal private TMPDIR');
  return Object.freeze({ public13: PARENT_MEDIA_PUBLIC13, runtime: PARENT_MEDIA_RUNTIME });
}

export function collectParentMedia(input) {
  const result = spawnSync(input.node, [input.playwrightCli, 'test', '--config', 'playwright.three-products.config.ts',
    '--grep', 'M2 real mounted manual video drop', '--list', 'tests/e2e/local/three-products.spec.ts'], {
    cwd: input.app,
    env: {
      ...process.env,
      NODE_PATH: '',
      PLAYWRIGHT_BROWSERS_PATH: input.browsersPath,
      TMPDIR: input.childTmpDir,
    },
    stdio: 'inherit', shell: false,
  });
  if (result.status !== 0) fail(`parent-media collection failed (exit ${result.status ?? 'signal'})`);
}

export function runParentMediaPreflight() {
  if (process.env.TIMELINE_PARENT_MEDIA_PREFLIGHT !== '1') fail('set TIMELINE_PARENT_MEDIA_PREFLIGHT=1 for manager-approved preflight');
  const input = readParentMediaInputs();
  const source = checkParentMediaSources(input);
  const dependencies = checkParentMediaDependencies(input);
  if (process.env.TIMELINE_PARENT_MEDIA_COLLECT === '1') collectParentMedia(input);
  console.log(`[current014/parent-media] source ready tree=${source.appTree} public13=${dependencies.public13.archiveSha256} artifacts=${dependencies.runtime.artifactCount}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runParentMediaPreflight();
