#!/usr/bin/env node

/**
 * Central current013 real-HTTP initializer launcher.
 *
 * This is deliberately a source-guarded launcher around the one focused
 * initializer journey; it does not broaden the browser gate to another suite.
 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import {
  accessSync, constants, existsSync, readFileSync, realpathSync, statSync,
} from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

export const CURRENT013_RUNTIME = Object.freeze({
  serverCommit: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
  producerCommit: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
  tree: '7ab412cc4bcbe517efcfa806e092336390312e18',
  version: '0.2.13',
  producerVersion: 'sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56',
  schemaDigest: 'sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4',
  componentManifest: 'sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5',
  artifactCount: 75,
});

export const CURRENT013_AGENT = Object.freeze({
  commit: '8130a401bf44a518d5a40ae274d398b8c560be55',
  tree: '236c3e57e0265c52b81ba8085de3193026176bff',
  lock: 'sha256:c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311',
});

export const CURRENT013_COMPOSITION = Object.freeze({
  archive: 'banodoco-timeline-composition-0.0.13.tgz',
  sha256: 'sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
  fileCount: 77,
});

const FULL_SHA = /^[a-f0-9]{40}$/;
const DIGEST = /^sha256:[a-f0-9]{64}$/;
const APP_METADATA = 'src/integrations/runtime/generated-contract-metadata.ts';
const AGENT_METADATA = 'astrid_runtime_client/contract_metadata.py';
const REAL_HTTP_TEST = 'tests/e2e/local/bootstrap013-real-http.spec.ts';
const DEFAULT_PRIVATE13_NODE_MODULES = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-public13-full-environment-custody-repair/private13/node_modules';
const DEFAULT_PRIVATE13_READY = '/home/user/work/wt/app-m3-public13-full-environment-custody-repair/notes/public13-protected-env-READY';
const PRIVATE13_ARCHIVE_SHA256 = '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738';
const PRIVATE13_COMPOSITION_TREE_SHA256 = '5ce2600247eba0be40cd8c643a8ad35c20248e089cb31a41f7ae2585e4f96a7c';
const PRIVATE13_DIRECT_PACKAGES = [
  '@banodoco/timeline-composition', '@banodoco/timeline-ops', '@banodoco/timeline-schema',
  '@playwright/test', '@remotion/layout-utils', '@remotion/media', '@remotion/player', '@remotion/three',
  'react', 'react-dom', 'remotion', 'vite',
];

function fail(message) {
  throw new Error(`[current013] ${message}`);
}

function private13Paths(env = process.env) {
  const leaf = (env.TIMELINE_CURRENT013_PRIVATE13_NODE_MODULES ?? DEFAULT_PRIVATE13_NODE_MODULES).trim();
  const ready = (env.TIMELINE_CURRENT013_PRIVATE13_READY ?? DEFAULT_PRIVATE13_READY).trim();
  if (!path.isAbsolute(leaf) || !path.isAbsolute(ready)) fail('private13 graph and READY paths must be absolute');
  return Object.freeze({ leaf, ready });
}

function compositionTreeDigest(root) {
  const digest = createHash('sha256');
  const files = execFileSync('find', [root, '-type', 'f', '-print'], { encoding: 'utf8' }).trim().split('\n').filter(Boolean).sort();
  for (const file of files) {
    digest.update(path.relative(root, file));
    digest.update(readFileSync(file));
  }
  return digest.digest('hex');
}

function checkDirectPackages(leaf) {
  const appPackage = jsonFile(path.join(process.cwd(), 'package.json'));
  const appLock = jsonFile(path.join(process.cwd(), 'package-lock.json'));
  const direct = { ...(appPackage.dependencies ?? {}), ...(appPackage.devDependencies ?? {}) };
  for (const name of PRIVATE13_DIRECT_PACKAGES) {
    if (!(name in direct)) fail(`private13 direct package is not an App dependency: ${name}`);
  }
  const resolved = {};
  for (const name of Object.keys(direct)) {
    const packageFile = path.join(leaf, name, 'package.json');
    if (!existsSync(packageFile)) fail(`private13 direct package is missing: ${name}`);
    const packageJson = jsonFile(packageFile);
    const lockEntry = appLock.packages?.[`node_modules/${name}`];
    const lockVersion = lockEntry?.version
      ?? (lockEntry?.link && lockEntry.resolved ? appLock.packages?.[lockEntry.resolved]?.version : undefined);
    if (!lockVersion || packageJson.name !== name || packageJson.version !== lockVersion) {
      fail(`private13 direct package identity mismatch for ${name}: ${packageJson.name}@${packageJson.version}, expected ${name}@${lockVersion}`);
    }
    const actual = realpathSync(path.dirname(packageFile));
    if (!actual.startsWith(`${leaf}${path.sep}`)) fail(`private13 direct package escapes owned graph: ${name} -> ${actual}`);
    resolved[name] = { version: packageJson.version, path: actual };
  }
  return resolved;
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

function requiredPath(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value)) fail(`${name} does not exist: ${value}`);
  if (!statSync(value).isDirectory()) fail(`${name} must name a directory: ${value}`);
  return realpathSync(value);
}

function requiredExecutable(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value) || !statSync(value).isFile()) fail(`${name} must name a file: ${value}`);
  try { accessSync(value, constants.X_OK); }
  catch { fail(`${name} must be executable: ${value}`); }
  // Invoking the supplied venv entry point preserves its sys.prefix.
  return value;
}

function git(root, ...args) {
  try {
    return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  } catch (error) {
    fail(`git ${args.join(' ')} failed in ${root}: ${error.message}`);
  }
}

function sha256File(file) {
  return `sha256:${createHash('sha256').update(readFileSync(file)).digest('hex')}`;
}

function jsonFile(file) {
  try { return JSON.parse(readFileSync(file, 'utf8')); }
  catch (error) { fail(`cannot read JSON ${file}: ${error.message}`); }
}

export function readCurrent013Inputs(env = process.env, appRoot = process.cwd()) {
  const appTree = requiredSha(env, 'TIMELINE_CURRENT013_APP_TREE');
  const agentSha = requiredSha(env, 'TIMELINE_CURRENT013_AGENT_SHA');
  const runtimeSha = requiredSha(env, 'TIMELINE_CURRENT013_RUNTIME_SHA');
  if (agentSha !== CURRENT013_AGENT.commit) {
    fail(`TIMELINE_CURRENT013_AGENT_SHA must be the frozen Agent ${CURRENT013_AGENT.commit}`);
  }
  if (runtimeSha !== CURRENT013_RUNTIME.serverCommit) {
    fail(`TIMELINE_CURRENT013_RUNTIME_SHA must be the frozen Runtime server ${CURRENT013_RUNTIME.serverCommit}`);
  }
  if (!path.isAbsolute(appRoot)) fail(`App root must be absolute: ${appRoot}`);
  const app = realpathSync(appRoot);
  const agent = requiredPath(env, 'ASTRID_CHECKOUT');
  const runtime = requiredPath(env, 'ASTRID_RUNTIME_CHECKOUT');
  const runtimeProducer = requiredPath(env, 'TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT');
  const agentPython = requiredExecutable(env, 'ASTRID_PYTHON');
  const runtimePython = requiredExecutable(env, 'ASTRID_RUNTIME_PYTHON');
  if (env.ASTRID_APP_DIRECT_DIST) {
    fail('ASTRID_APP_DIRECT_DIST is forbidden; the existing current three-products default build helper must decide dist freshness');
  }
  return Object.freeze({ app, appTree, agent, agentSha, runtime, runtimeSha, runtimeProducer, agentPython, runtimePython });
}

function checkHead(root, expected, label) {
  const actual = git(root, 'rev-parse', 'HEAD');
  if (actual !== expected) fail(`${label} HEAD changed: expected ${expected}, got ${actual}`);
  return actual;
}

function checkClean(root, label) {
  const status = git(root, 'status', '--porcelain', '--untracked-files=normal');
  if (status) fail(`${label} source is dirty:\n${status}`);
}

function checkLock(root, label) {
  const file = path.join(root, 'runtime.lock.json');
  const lock = jsonFile(file);
  if (lock.producer !== 'astrid-runtime') fail(`${label} Runtime lock producer is ${lock.producer}, expected astrid-runtime`);
  if (lock.source_commit !== CURRENT013_RUNTIME.producerCommit) fail(`${label} Runtime artifact producer pin is ${lock.source_commit}, expected ${CURRENT013_RUNTIME.producerCommit}`);
  if (lock.producer_version !== CURRENT013_RUNTIME.producerVersion) fail(`${label} Runtime artifact pin is ${lock.producer_version}, expected ${CURRENT013_RUNTIME.producerVersion}`);
  const digest = sha256File(file);
  if (label === 'Agent' && process.env.CURRENT013_LAUNCHER_TEST !== '1' && digest !== CURRENT013_AGENT.lock) {
    fail(`${label} runtime.lock.json is ${digest}, expected ${CURRENT013_AGENT.lock}`);
  }
  return { file: digest, sourceCommit: lock.source_commit, producerVersion: lock.producer_version };
}

function checkMetadata(root, label, metadataFile) {
  const file = path.join(root, metadataFile);
  const source = readFileSync(file, 'utf8');
  const get = (name) => {
    const match = source.match(new RegExp(`${name}\\s*=\\s*["']([^"']+)["']`));
    if (!match) fail(`${label} metadata is missing ${name}: ${file}`);
    return match[1];
  };
  const schemaDigest = get('SCHEMA_DIGEST');
  const componentManifest = get('COMPONENT_MANIFEST_SHA256');
  if (schemaDigest !== CURRENT013_RUNTIME.schemaDigest) fail(`${label} schema is ${schemaDigest}, expected ${CURRENT013_RUNTIME.schemaDigest}`);
  if (componentManifest !== CURRENT013_RUNTIME.componentManifest) fail(`${label} component manifest is ${componentManifest}, expected ${CURRENT013_RUNTIME.componentManifest}`);
  if (label === 'App' && get('CONTRACT_VERSION') !== CURRENT013_RUNTIME.version) fail(`App contract is not ${CURRENT013_RUNTIME.version}`);
  return { file: sha256File(file), schemaDigest, componentManifest };
}

function checkRuntimeManifest(root) {
  const file = path.join(root, 'contract/artifacts.json');
  const manifest = jsonFile(file);
  if (manifest.producer !== 'astrid-runtime') fail(`Runtime manifest producer is ${manifest.producer}`);
  if (manifest.version !== CURRENT013_RUNTIME.producerVersion) fail(`Runtime manifest version is ${manifest.version}, expected ${CURRENT013_RUNTIME.producerVersion}`);
  const count = Object.keys(manifest.artifacts ?? {}).length;
  if (count !== CURRENT013_RUNTIME.artifactCount) fail(`Runtime manifest has ${count} artifacts, expected ${CURRENT013_RUNTIME.artifactCount}`);
  return { file: sha256File(file), version: manifest.version, artifactCount: count };
}

function checkCompositionArchive(root, label) {
  let file = path.join(root, 'remotion/artifacts', CURRENT013_COMPOSITION.archive);
  if (label === 'App') file = path.join(root, 'vendor/artifacts', CURRENT013_COMPOSITION.archive);
  if (!existsSync(file)) fail(`${label} Composition archive is missing: ${file}`);
  const digest = sha256File(file);
  if (digest !== CURRENT013_COMPOSITION.sha256) fail(`${label} Composition archive is ${digest}, expected ${CURRENT013_COMPOSITION.sha256}`);
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim().split('\n')
    .filter((member) => member && !member.endsWith('/'));
  if (members.length !== CURRENT013_COMPOSITION.fileCount || new Set(members).size !== members.length) {
    fail(`${label} Composition archive must contain exactly ${CURRENT013_COMPOSITION.fileCount} regular files, found ${members.length}`);
  }
  if (members.some((member) => !member.startsWith('package/') || member.slice('package/'.length).split('/').includes('..'))) {
    fail(`${label} Composition archive contains an unsafe member`);
  }
  return { file: digest, fileCount: members.length };
}

function checkPrivate13() {
  const { leaf, ready } = private13Paths();
  if (!existsSync(leaf) || !statSync(leaf).isDirectory()) {
    fail(`protected public13 node_modules leaf is missing: ${leaf}`);
  }
  if (realpathSync(leaf) !== leaf) {
    fail(`protected public13 node_modules leaf moved or became a symlink: ${leaf}`);
  }
  const readyRecord = readFileSync(ready, 'utf8');
  if (!readyRecord.includes(leaf) || !readyRecord.includes('all 77 archive files') || !readyRecord.includes('Runtime source `2c4ac180')) {
    fail(`protected public13 READY record is not the authoritative 77-file Runtime-2c4 environment: ${ready}`);
  }
  const composition = path.join(leaf, '@banodoco/timeline-composition');
  const sharedModules = process.env.TIMELINE_CURRENT013_SHARED_NODE_MODULES
    ?? path.join(process.cwd(), 'node_modules');
  if (realpathSync(composition) === realpathSync(path.join(sharedModules, '@banodoco/timeline-composition'))) {
    fail('protected public13 Composition resolves to the App shared install');
  }
  const files = execFileSync('find', [composition, '-type', 'f', '-print'], { encoding: 'utf8' }).trim().split('\n').filter(Boolean);
  if (files.length !== CURRENT013_COMPOSITION.fileCount) fail(`protected public13 Composition has ${files.length} files, expected ${CURRENT013_COMPOSITION.fileCount}`);
  const archive = path.join(process.cwd(), 'vendor/artifacts', CURRENT013_COMPOSITION.archive);
  if (sha256File(archive) !== `sha256:${PRIVATE13_ARCHIVE_SHA256}`) fail(`protected public13 archive is not ${PRIVATE13_ARCHIVE_SHA256}`);
  if (compositionTreeDigest(composition) !== PRIVATE13_COMPOSITION_TREE_SHA256) fail('protected public13 Composition payload bytes changed');
  const packageJson = jsonFile(path.join(composition, 'package.json'));
  if (packageJson.name !== '@banodoco/timeline-composition' || packageJson.version !== '0.0.13') fail('protected public13 Composition package is not 0.0.13');
  if (!existsSync(path.join(composition, 'dist/animations.generated.js'))) fail('protected public13 generated animations are missing');
  const direct = checkDirectPackages(leaf);
  const vite = path.join(leaf, '.bin/vite');
  requiredExecutable({ VITE: vite }, 'VITE');
  if (!realpathSync(vite).startsWith(`${leaf}${path.sep}`)) fail(`protected public13 Vite resolves outside the owned graph: ${realpathSync(vite)}`);
  execFileSync(process.execPath, ['--version'], { stdio: ['ignore', 'pipe', 'pipe'] });
  execFileSync(vite, ['--version'], { stdio: ['ignore', 'pipe', 'pipe'] });
  return Object.freeze({ leaf, ready, compositionFiles: files.length, compositionTree: PRIVATE13_COMPOSITION_TREE_SHA256, archive: PRIVATE13_ARCHIVE_SHA256, direct, node: process.execPath, vite });
}

function runVendorCheck(input, root, command, label) {
  const script = command === 'node' ? path.join(input.app, 'scripts/vendor-lock.mjs') : path.join(input.agent, 'scripts/vendor_lock.py');
  const lock = path.join(root, 'runtime.lock.json');
  const result = spawnSync(command, [script, 'check', lock, '--producer', input.runtimeProducer], {
    cwd: root, env: process.env, stdio: 'inherit', shell: false,
  });
  if (result.status !== 0) fail(`${label} normal Runtime vendor-lock check failed (exit ${result.status ?? 'signal'})`);
}

export function checkCurrent013Sources(input, { vendor = true } = {}) {
  if (git(input.app, 'rev-parse', '--show-toplevel') !== input.app) fail(`App root is not the current checkout: ${input.app}`);
  if (git(input.app, 'rev-parse', 'HEAD^{tree}') !== input.appTree) fail(`App source tree changed: expected ${input.appTree}`);
  const agentTree = git(input.agent, 'rev-parse', 'HEAD^{tree}');
  const runtimeTree = git(input.runtime, 'rev-parse', 'HEAD^{tree}');
  const producerTree = git(input.runtimeProducer, 'rev-parse', 'HEAD^{tree}');
  if (agentTree !== CURRENT013_AGENT.tree) fail(`Agent source tree is ${agentTree}, expected ${CURRENT013_AGENT.tree}`);
  if (runtimeTree !== CURRENT013_RUNTIME.tree) fail(`Runtime source tree is ${runtimeTree}, expected ${CURRENT013_RUNTIME.tree}`);
  checkHead(input.agent, input.agentSha, 'Agent');
  checkHead(input.runtime, input.runtimeSha, 'Runtime');
  checkHead(input.runtimeProducer, CURRENT013_RUNTIME.producerCommit, 'Runtime artifact producer');
  checkClean(input.app, 'App');
  checkClean(input.agent, 'Agent');
  checkClean(input.runtime, 'Runtime');
  checkClean(input.runtimeProducer, 'Runtime producer');
  const appLock = checkLock(input.app, 'App');
  const agentLock = checkLock(input.agent, 'Agent');
  const appMetadata = checkMetadata(input.app, 'App', APP_METADATA);
  const agentMetadata = checkMetadata(input.agent, 'Agent', AGENT_METADATA);
  const runtimeManifest = checkRuntimeManifest(input.runtimeProducer);
  const appComposition = checkCompositionArchive(input.app, 'App');
  if (vendor) {
    runVendorCheck(input, input.app, 'node', 'App');
    runVendorCheck(input, input.agent, input.agentPython, 'Agent');
  }
  return Object.freeze({
    app: { root: input.app, tree: input.appTree, lock: appLock, metadata: appMetadata, composition: appComposition },
    agent: { root: input.agent, commit: input.agentSha, tree: agentTree, lock: agentLock, metadata: agentMetadata },
    runtime: { root: input.runtime, commit: input.runtimeSha, tree: runtimeTree },
    runtimeProducer: { root: input.runtimeProducer, commit: CURRENT013_RUNTIME.producerCommit, tree: producerTree, manifest: runtimeManifest },
  });
}

export function runCurrent013Integration() {
  if (process.env.TIMELINE_CURRENT013_RUN !== '1') {
    fail('set TIMELINE_CURRENT013_RUN=1 only when the manager has supplied the final exact pair');
  }
  const input = readCurrent013Inputs();
  const private13 = process.env.CURRENT013_LAUNCHER_TEST === '1' ? null : checkPrivate13();
  const private13PathsFromEnv = private13Paths();
  const before = checkCurrent013Sources(input);
  console.log(`[current013] exact source preflight passed; running ${REAL_HTTP_TEST}`);
  const childEnv = {
    ...process.env,
    ASTRID_CHECKOUT: input.agent,
    ASTRID_RUNTIME_CHECKOUT: input.runtime,
    ASTRID_PYTHON: input.agentPython,
    ASTRID_RUNTIME_PYTHON: input.runtimePython,
    TIMELINE_BUNDLE_AGENT_HEAD: input.agentSha,
    TIMELINE_BUNDLE_RUNTIME_HEAD: input.runtimeSha,
    PRIVATE13_NODE_MODULES: private13PathsFromEnv.leaf,
    VITE_TIMELINE_COMPOSITION_ROOT: path.join(private13PathsFromEnv.leaf, '@banodoco/timeline-composition'),
  };
  let status = 1;
  try {
    status = spawnSync('npm', ['exec', '--', 'playwright', 'test', '--config', 'playwright.direct.config.ts', REAL_HTTP_TEST], { cwd: input.app, env: childEnv, stdio: 'inherit', shell: false }).status ?? 1;
  } finally {
    const after = checkCurrent013Sources(input);
    if (JSON.stringify(after) !== JSON.stringify(before)) fail('source checks changed between the start and end of the browser gate');
    if (private13 && JSON.stringify(checkPrivate13()) !== JSON.stringify(private13)) fail('protected public13 environment changed during the browser gate');
    console.log('[current013] exact source postflight passed');
  }
  process.exitCode = status;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runCurrent013Integration();

