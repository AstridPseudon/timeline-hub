#!/usr/bin/env node

/**
 * Source-pinned launcher for the MAIN574/public13 editing browser gate.
 *
 * The marker is the manager's authority.  This wrapper never discovers an
 * actor, realm, or moving checkout, and never starts a child before the
 * marker and every source identity have passed.
 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import { accessSync, constants, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, rmSync, statSync, symlinkSync, unlinkSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export const READY_MARKER = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/root-main574-public13-READY';
export const RUNTIME = Object.freeze({
  version: '0.2.13',
  commit: '2c4ac180c2220bdad966bc01e95ad230e99ce26a',
  producerVersion: 'sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56',
  schemaDigest: 'sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4',
  componentManifest: 'sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5',
  artifactCount: 75,
});
export const COMPOSITION = Object.freeze({
  appArchive: 'banodoco-timeline-composition-0.0.13.tgz',
  appSha256: '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
  agentArchive: 'banodoco-timeline-composition-0.0.12.tgz',
  agentSha256: '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3',
  fileCount: 77,
});

const SHA = /^[0-9a-f]{40}$/;
const DIGEST = /^sha256:[0-9a-f]{64}$/;
const APP_METADATA = 'src/integrations/runtime/generated-contract-metadata.ts';
const AGENT_METADATA = 'astrid_runtime_client/contract_metadata.py';

function fail(message) { throw new Error(`[main574-public13] ${message}`); }
function required(env, name) {
  const value = env[name]?.trim();
  if (!value) fail(`${name} is required; no moving-repo default is allowed`);
  return value;
}
function sha(env, name) {
  const value = required(env, name);
  if (!SHA.test(value)) fail(`${name} must be a literal lowercase 40-character SHA`);
  return value;
}
function sourcePath(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be absolute`);
  if (!existsSync(value) || !statSync(value).isDirectory()) fail(`${name} must name an existing directory`);
  return realpathSync(value);
}
function executable(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value) || !existsSync(value) || !statSync(value).isFile()) fail(`${name} must name an absolute executable file`);
  try { accessSync(value, constants.X_OK); } catch { fail(`${name} must be executable`); }
  return value;
}
function git(root, ...args) {
  try { return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim(); }
  catch (error) { fail(`git ${args.join(' ')} failed in ${root}: ${error.message}`); }
}
function json(file, label) {
  try { return JSON.parse(readFileSync(file, 'utf8')); }
  catch (error) { fail(`${label} is not valid JSON: ${error.message}`); }
}
function digest(file) { return createHash('sha256').update(readFileSync(file)).digest('hex'); }
function markerPath(env) { return env.TIMELINE_MAIN574_PUBLIC13_READY_MARKER?.trim() || READY_MARKER; }

export function readReadyMarker(env = process.env) {
  const file = markerPath(env);
  if (!existsSync(file)) fail(`manager READY marker is missing: ${file}`);
  const fields = {};
  for (const line of readFileSync(file, 'utf8').split(/\r?\n/)) {
    const match = /^(App|Root|Agent|Runtime)(SHA|Tree):\s*([0-9a-f]{40})$/.exec(line.trim());
    if (match) {
      const key = `${match[1] === 'Root' ? 'App' : match[1]}${match[2]}`;
      if (fields[key] && fields[key] !== match[3]) fail(`READY marker has conflicting ${key} identities`);
      fields[key] = match[3];
    }
  }
  for (const key of ['AppSHA', 'AppTree', 'AgentSHA', 'AgentTree', 'RuntimeSHA', 'RuntimeTree']) {
    if (!fields[key] || !SHA.test(fields[key])) fail(`READY marker lacks literal ${key}`);
  }
  return Object.freeze(fields);
}

export function readInputs(env = process.env, appRoot = process.cwd()) {
  const ready = readReadyMarker(env);
  const app = realpathSync(appRoot);
  const agent = sourcePath(env, 'ASTRID_CHECKOUT');
  const runtime = sourcePath(env, 'ASTRID_RUNTIME_CHECKOUT');
  const producer = sourcePath(env, 'TIMELINE_MAIN574_PUBLIC13_RUNTIME_PRODUCER_CHECKOUT');
  const agentPython = executable(env, 'ASTRID_PYTHON');
  const runtimePython = executable(env, 'ASTRID_RUNTIME_PYTHON');
  if (env.ASTRID_PUBLIC_CHECKOUT || env.ASTRID_APP_DIRECT_DIST) fail('public/direct dist overrides are forbidden');
  return Object.freeze({ app, agent, runtime, producer, agentPython, runtimePython, ready });
}

function clean(root, label) {
  const status = git(root, 'status', '--porcelain', '--untracked-files=normal');
  if (status) fail(`${label} source is dirty:\n${status}`);
}
function metadata(root, file, label) {
  const text = readFileSync(path.join(root, file), 'utf8');
  const value = (name) => text.match(new RegExp(`${name}\\s*=\\s*["']([^"']+)["']`))?.[1] ?? fail(`${label} metadata lacks ${name}`);
  const result = { contractVersion: value('CONTRACT_VERSION'), schemaDigest: value('SCHEMA_DIGEST'), componentManifest: value('COMPONENT_MANIFEST_SHA256') };
  if (result.contractVersion !== RUNTIME.version || result.schemaDigest !== RUNTIME.schemaDigest || result.componentManifest !== RUNTIME.componentManifest) fail(`${label} metadata does not match Runtime 0.2.13`);
  return result;
}
function lock(root, label) {
  const file = path.join(root, 'runtime.lock.json');
  const value = json(file, `${label} runtime.lock.json`);
  if (value.source_commit !== RUNTIME.commit || value.producer_version !== RUNTIME.producerVersion) fail(`${label} Runtime lock is not the published 0.2.13 source`);
  if (Object.keys(value.files ?? {}).length !== (label === 'App' ? 13 : 15)) fail(`${label} Runtime lock file count is unexpected`);
  return { sha256: digest(file), sourceCommit: value.source_commit, producerVersion: value.producer_version };
}
function archive(root, relative, expected, label) {
  const file = path.join(root, relative);
  if (!existsSync(file) || digest(file) !== expected) fail(`${label} Composition archive identity mismatch`);
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8' }).trim().split('\n').filter((entry) => entry && !entry.endsWith('/'));
  if (members.length !== COMPOSITION.fileCount || new Set(members).size !== members.length || members.some((entry) => !entry.startsWith('package/'))) fail(`${label} Composition archive must have exactly 77 safe regular members`);
  return { sha256: expected, fileCount: members.length };
}
function source(root, expectedHead, expectedTree, label) {
  if (git(root, 'rev-parse', 'HEAD') !== expectedHead) fail(`${label} HEAD is stale or synthetic`);
  if (git(root, 'rev-parse', 'HEAD^{tree}') !== expectedTree) fail(`${label} tree does not match the READY marker`);
  clean(root, label);
  return { head: expectedHead, tree: expectedTree };
}

export function checkSources(input) {
  const { ready } = input;
  const result = {
    app: source(input.app, ready.AppSHA, ready.AppTree, 'App'),
    agent: source(input.agent, ready.AgentSHA, ready.AgentTree, 'Agent'),
    runtime: source(input.runtime, ready.RuntimeSHA, ready.RuntimeTree, 'Runtime'),
    producer: source(input.producer, ready.RuntimeSHA, ready.RuntimeTree, 'Runtime producer'),
    appLock: lock(input.app, 'App'),
    agentLock: lock(input.agent, 'Agent'),
    appMetadata: metadata(input.app, APP_METADATA, 'App'),
    agentMetadata: metadata(input.agent, AGENT_METADATA, 'Agent'),
    appComposition: archive(input.app, `vendor/artifacts/${COMPOSITION.appArchive}`, COMPOSITION.appSha256, 'App'),
    agentComposition: archive(input.agent, `remotion/artifacts/${COMPOSITION.agentArchive}`, COMPOSITION.agentSha256, 'Agent'),
  };
  const manifest = json(path.join(input.producer, 'contract/artifacts.json'), 'Runtime artifact manifest');
  if (manifest.version !== RUNTIME.producerVersion || Object.keys(manifest.artifacts ?? {}).length !== RUNTIME.artifactCount) fail('Runtime artifact manifest is not the published 75-artifact manifest');
  result.manifest = { version: manifest.version, artifactCount: Object.keys(manifest.artifacts).length, sha256: digest(path.join(input.producer, 'contract/artifacts.json')) };
  return Object.freeze(result);
}

function privateEnv(input, env) {
  const root = required(env, 'TIMELINE_MAIN574_PUBLIC13_PRIVATE_ROOT');
  if (!path.isAbsolute(root)) fail('TIMELINE_MAIN574_PUBLIC13_PRIVATE_ROOT must be absolute');
  mkdirSync(root, { recursive: true });
  const output = path.join(root, 'browser-artifacts');
  mkdirSync(output, { recursive: true });
  return {
    ...env,
    TMPDIR: path.join(root, 'tmp'),
    XDG_CACHE_HOME: path.join(root, 'xdg-cache'),
    npm_config_cache: path.join(root, 'npm-cache'),
    PWTEST_CACHE_DIR: path.join(root, 'playwright-cache'),
    PLAYWRIGHT_OUTPUT_DIR: output,
    TSX_DISABLE_CACHE: '1',
    VITEST_CACHE_DIR: path.join(root, 'vitest-cache'),
    TIMELINE_BUNDLE_AGENT_HEAD: input.ready.AgentSHA,
    TIMELINE_BUNDLE_RUNTIME_HEAD: input.ready.RuntimeSHA,
  };
}

function preparePrivateNodeModules(appRoot, privateRoot) {
  const link = path.join(appRoot, 'node_modules');
  if (!lstatSync(link).isSymbolicLink()) fail('App node_modules must remain the shared dependency symlink');
  const shared = realpathSync(link);
  const overlay = path.join(privateRoot, 'node_modules');
  rmSync(overlay, { recursive: true, force: true });
  mkdirSync(overlay, { recursive: true });
  for (const name of readdirSync(shared)) {
    if (name === '.vite' || name === '.vite-temp') continue;
    const source = path.join(shared, name);
    const destination = path.join(overlay, name);
    if (name.startsWith('@')) {
      mkdirSync(destination, { recursive: true });
      for (const child of readdirSync(source)) symlinkSync(path.join(source, child), path.join(destination, child), 'junction');
    } else symlinkSync(source, destination, 'junction');
  }
  mkdirSync(path.join(overlay, '.vite'), { recursive: true });
  mkdirSync(path.join(overlay, '.vite-temp'), { recursive: true });
  unlinkSync(link);
  symlinkSync(overlay, link, 'junction');
  return () => {
    unlinkSync(link);
    symlinkSync(shared, link, 'junction');
    rmSync(overlay, { recursive: true, force: true });
  };
}

export function runLane(lane, env = process.env, appRoot = process.cwd()) {
  if (env.TIMELINE_MAIN574_PUBLIC13_RUN !== '1') fail('set TIMELINE_MAIN574_PUBLIC13_RUN=1 only after the manager READY marker exists');
  if (!['native', 'cold-open', 'labels'].includes(lane)) fail(`unknown lane ${lane}`);
  const input = readInputs(env, appRoot);
  const before = checkSources(input);
  const childEnv = privateEnv(input, env);
  const restoreModules = preparePrivateNodeModules(input.app, childEnv.TIMELINE_MAIN574_PUBLIC13_PRIVATE_ROOT);
  const command = lane === 'native'
    ? ['npm', ['run', 'test:e2e:three-products', '--', '--grep', 'M1 real']]
    : ['npm', ['exec', '--', 'playwright', 'test', '--config', 'playwright.track-label.config.ts', '--grep', lane === 'cold-open' ? 'M2 cold-open' : 'M2 real label']];
  let status = 1;
  try { status = spawnSync(command[0], command[1], { cwd: input.app, env: childEnv, stdio: 'inherit', shell: false }).status ?? 1; }
  finally {
    try {
      restoreModules();
      const after = checkSources(input);
      if (JSON.stringify(before) !== JSON.stringify(after)) fail('source identity or guarded artifact bytes changed during the browser lane');
    } catch (error) {
      try { restoreModules(); } catch { /* preserve the first useful failure */ }
      throw error;
    }
  }
  process.exitCode = status;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runLane(process.argv[2] ?? 'native');
