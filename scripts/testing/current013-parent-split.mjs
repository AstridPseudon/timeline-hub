#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import { accessSync, constants, existsSync, readFileSync, realpathSync, statSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

export const CURRENT013_PARENT_SPLIT_AGENT = '8130a401bf44a518d5a40ae274d398b8c560be55';
export const CURRENT013_PARENT_SPLIT_AGENT_TREE = '236c3e57e0265c52b81ba8085de3193026176bff';
export const CURRENT013_PARENT_SPLIT_RUNTIME = '2c4ac180c2220bdad966bc01e95ad230e99ce26a';
export const CURRENT013_PARENT_SPLIT_RUNTIME_TREE = '7ab412cc4bcbe517efcfa806e092336390312e18';
export const PUBLIC13_ARCHIVE_SHA256 = '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738';

function fail(message) { throw new Error(`[current013/parent-split] ${message}`); }
function required(env, name) {
  const value = env[name]?.trim();
  if (!value) fail(`${name} is required`);
  return value;
}
function requiredPath(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value) || !existsSync(value) || !statSync(value).isDirectory()) fail(`${name} must be an absolute directory`);
  return realpathSync(value);
}
function requiredExecutable(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value) || !existsSync(value) || !statSync(value).isFile()) fail(`${name} must be an executable file`);
  try { accessSync(value, constants.X_OK); } catch { fail(`${name} must be executable`); }
  return value;
}
function git(root, ...args) {
  try { return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim(); }
  catch (error) { fail(`git ${args.join(' ')} failed in ${root}: ${error.message}`); }
}
function sha256(file) { return createHash('sha256').update(readFileSync(file)).digest('hex'); }
function safeArchive(file) {
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8' }).trim().split('\n').filter((member) => member && !member.endsWith('/'));
  if (members.length !== 77 || new Set(members).size !== members.length || members.some((member) => !member.startsWith('package/') || member.split('/').includes('..'))) {
    fail('public13 Composition archive must contain exactly 77 safe regular files');
  }
}

export function readCurrent013ParentSplitInputs(env = process.env, appRoot = process.cwd()) {
  const appTree = required(env, 'TIMELINE_CURRENT013_APP_TREE');
  const agentSha = required(env, 'TIMELINE_CURRENT013_AGENT_SHA');
  const runtimeSha = required(env, 'TIMELINE_CURRENT013_RUNTIME_SHA');
  if (![appTree, agentSha, runtimeSha].every((value) => /^[0-9a-f]{40}$/.test(value))) fail('source identities must be full lowercase SHA values');
  if (agentSha !== CURRENT013_PARENT_SPLIT_AGENT) fail(`requires Agent ${CURRENT013_PARENT_SPLIT_AGENT}`);
  if (runtimeSha !== CURRENT013_PARENT_SPLIT_RUNTIME) fail(`requires Runtime ${CURRENT013_PARENT_SPLIT_RUNTIME}`);
  if (!path.isAbsolute(appRoot)) fail('App root must be absolute');
  return Object.freeze({
    app: realpathSync(appRoot), appTree, agentSha, runtimeSha,
    agent: requiredPath(env, 'ASTRID_CHECKOUT'), runtime: requiredPath(env, 'ASTRID_RUNTIME_CHECKOUT'),
    runtimeProducer: requiredPath(env, 'TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT'),
    agentPython: requiredExecutable(env, 'ASTRID_PYTHON'), runtimePython: requiredExecutable(env, 'ASTRID_RUNTIME_PYTHON'),
  });
}

export function checkCurrent013ParentSplitSources(input, env = process.env) {
  if (git(input.app, 'rev-parse', 'HEAD^{tree}') !== input.appTree) fail('App tree changed');
  if (git(input.agent, 'rev-parse', 'HEAD') !== input.agentSha || git(input.agent, 'rev-parse', 'HEAD^{tree}') !== CURRENT013_PARENT_SPLIT_AGENT_TREE) fail('Agent HEAD/tree is not the approved Agent8130 source');
  if (git(input.runtime, 'rev-parse', 'HEAD') !== input.runtimeSha || git(input.runtime, 'rev-parse', 'HEAD^{tree}') !== CURRENT013_PARENT_SPLIT_RUNTIME_TREE) fail('Runtime HEAD/tree is not the approved Runtime source');
  for (const [root, label] of [[input.app, 'App'], [input.agent, 'Agent'], [input.runtime, 'Runtime'], [input.runtimeProducer, 'Runtime producer']]) {
    if (git(root, 'status', '--porcelain', '--untracked-files=normal')) fail(`${label} source is dirty`);
  }
  const manifest = JSON.parse(readFileSync(path.join(input.runtimeProducer, 'contract/artifacts.json'), 'utf8'));
  if (Object.keys(manifest.artifacts ?? {}).length !== 75) fail('Runtime producer artifact manifest is not all75');
  const archive = path.join(input.app, 'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz');
  if (!existsSync(archive) || sha256(archive) !== PUBLIC13_ARCHIVE_SHA256) fail('public13 archive is not 9412');
  safeArchive(archive);
  const privateModules = realpathSync(required(env, 'PRIVATE13_NODE_MODULES'));
  if (privateModules === realpathSync('/home/user/work/app/node_modules')) fail('private13 node_modules resolves to a shared install');
  const ready = required(env, 'TIMELINE_CURRENT013_PRIVATE13_READY');
  if (!existsSync(ready)) fail(`private13 readiness marker is missing: ${ready}`);
  const browser = required(env, 'PLAYWRIGHT_CHROMIUM_EXECUTABLE');
  if (!path.isAbsolute(browser) || !existsSync(browser)) fail('Chromium executable is missing');
  return { appTree: input.appTree, agentTree: CURRENT013_PARENT_SPLIT_AGENT_TREE, runtimeTree: CURRENT013_PARENT_SPLIT_RUNTIME_TREE, archive: PUBLIC13_ARCHIVE_SHA256, artifactCount: 75 };
}

export function parentSplitCacheIdentity(input) {
  const hash = (file) => createHash('sha256').update(readFileSync(new URL(file, import.meta.url))).digest('hex');
  return `parent-split-tree${input.appTree}-agent${input.agentSha}-runtime${input.runtimeSha}-public13-${PUBLIC13_ARCHIVE_SHA256}-all75-all77-runner${hash('./current013-parent-split.mjs')}`;
}

export function runCurrent013ParentSplit() {
  if (process.env.TIMELINE_CURRENT013_RUN !== '1') fail('set TIMELINE_CURRENT013_RUN=1 only for the manager-approved gate');
  const input = readCurrent013ParentSplitInputs();
  checkCurrent013ParentSplitSources(input);
  if (process.env.TIMELINE_CURRENT013_CACHE_ID !== parentSplitCacheIdentity(input)) fail('TIMELINE_CURRENT013_CACHE_ID does not identify this exact split source/pair');
  const before = checkCurrent013ParentSplitSources(input);
  let status = 1;
  try {
    status = spawnSync('npm', ['run', 'test:e2e:three-products', '--', '--config', 'playwright.parent-split.config.ts'], {
      cwd: input.app,
      env: { ...process.env, ASTRID_CHECKOUT: input.agent, ASTRID_RUNTIME_CHECKOUT: input.runtime,
        ASTRID_PYTHON: input.agentPython, ASTRID_RUNTIME_PYTHON: input.runtimePython,
        TIMELINE_BUNDLE_AGENT_HEAD: input.agentSha, TIMELINE_BUNDLE_RUNTIME_HEAD: input.runtimeSha },
      stdio: 'inherit', shell: false,
    }).status ?? 1;
  } finally {
    const after = checkCurrent013ParentSplitSources(input);
    if (JSON.stringify(after) !== JSON.stringify(before)) fail('source checks changed during the browser gate');
  }
  process.exitCode = status;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runCurrent013ParentSplit();
