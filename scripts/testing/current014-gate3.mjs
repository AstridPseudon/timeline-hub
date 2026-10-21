#!/usr/bin/env node

/**
 * Manager-gated Gate3 caller for the existing mounted native-None case.
 *
 * This is a source/preflight wrapper only. It deliberately delegates to the
 * real three-products suite and does not add a fixture, UI surface, or
 * acceptance path. The older current013 wrappers remain historical and keep
 * their original source tuple.
 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import {
  accessSync, constants, existsSync, lstatSync, readFileSync, realpathSync, statSync,
} from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export const CURRENT014_GATE3 = Object.freeze({
  agent: Object.freeze({
    commit: '6efc81500a0e0688c2bb41e736503f0fc3e04abb',
    tree: '2ed2b8a12b5b3391ca221ba6ff05390f71a73556',
  }),
  runtime: Object.freeze({
    commit: '95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c',
    tree: 'd3a290b407fa61e6ab2d476f50c068073f70df00',
    producerVersion: 'sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac',
    schemaDigest: 'sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816',
    componentManifest: 'sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5',
    artifactCount: 76,
  }),
  composition: Object.freeze({
    archive: 'banodoco-timeline-composition-0.0.13.tgz',
    sha256: 'sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
    bytes: 58477,
    fileCount: 77,
    version: '0.0.13',
    packageResolved: 'file:vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz',
  }),
  vendorAstridCommit: '091aa23ec83ea05ffd3b0115a640230d51c8c429',
});

const FULL_SHA = /^[a-f0-9]{40}$/;
const APP_METADATA = 'src/integrations/runtime/generated-contract-metadata.ts';
const AGENT_METADATA = 'astrid_runtime_client/contract_metadata.py';
const TEST_SOURCE = 'tests/e2e/local/three-products.spec.ts';
const CASE_TITLE = 'M2 native None single:';

function fail(message) {
  throw new Error(`[current014/gate3] ${message}`);
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

function requiredFile(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value) || !statSync(value).isFile()) fail(`${name} must name a file: ${value}`);
  return realpathSync(value);
}

function requiredExecutable(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value) || !statSync(value).isFile()) fail(`${name} must name a file: ${value}`);
  try { accessSync(value, constants.X_OK); } catch { fail(`${name} must be executable: ${value}`); }
  return value;
}

function git(root, ...args) {
  try {
    return execFileSync('git', ['-C', root, ...args], {
      encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 10_000,
    }).trim();
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

function checkClean(root, label) {
  const status = git(root, 'status', '--porcelain', '--untracked-files=normal');
  if (status) fail(`${label} source is dirty:\n${status}`);
}

function checkMetadata(root, label, fileName) {
  const file = path.join(root, fileName);
  const source = readFileSync(file, 'utf8');
  const value = (name) => {
    const match = source.match(new RegExp(`${name}\\s*=\\s*["']([^"']+)["']`));
    if (!match) fail(`${label} metadata is missing ${name}: ${file}`);
    return match[1];
  };
  if (value('SCHEMA_DIGEST') !== CURRENT014_GATE3.runtime.schemaDigest) fail(`${label} schema digest is not current Runtime95`);
  if (value('COMPONENT_MANIFEST_SHA256') !== CURRENT014_GATE3.runtime.componentManifest) fail(`${label} component manifest is not current Runtime95`);
  if (label === 'App' && value('CONTRACT_VERSION') !== '0.2.14') fail('App contract version is not 0.2.14');
  return sha256File(file);
}

function checkRuntimeLock(root, label) {
  const file = path.join(root, 'runtime.lock.json');
  const lock = jsonFile(file);
  if (lock.source_commit !== CURRENT014_GATE3.runtime.commit) fail(`${label} Runtime lock source is not Runtime95`);
  if (lock.producer_version !== CURRENT014_GATE3.runtime.producerVersion) fail(`${label} Runtime lock version is not the all76 artifact`);
  return sha256File(file);
}

function checkCompositionArchive(root, label, relativeDirectory) {
  const file = path.join(root, relativeDirectory, CURRENT014_GATE3.composition.archive);
  if (!existsSync(file)) fail(`${label} Composition archive is missing: ${file}`);
  if (statSync(file).size !== CURRENT014_GATE3.composition.bytes) fail(`${label} Composition archive byte count is not 58477`);
  if (sha256File(file) !== CURRENT014_GATE3.composition.sha256) fail(`${label} Composition archive digest is not public13/9412`);
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8' }).trim().split('\n')
    .filter((member) => member && !member.endsWith('/'));
  if (members.length !== CURRENT014_GATE3.composition.fileCount || new Set(members).size !== members.length) {
    fail(`${label} Composition archive must contain exactly 77 regular files`);
  }
  if (members.some((member) => !member.startsWith('package/') || member.slice('package/'.length).split('/').includes('..'))) {
    fail(`${label} Composition archive contains an unsafe member`);
  }
  return { digest: sha256File(file), bytes: statSync(file).size, fileCount: members.length };
}

function checkCompositionPackage(root) {
  const packageJson = jsonFile(path.join(root, 'package.json'));
  const lock = jsonFile(path.join(root, 'package-lock.json'));
  if (packageJson.dependencies?.['@banodoco/timeline-composition'] !== CURRENT014_GATE3.composition.packageResolved) {
    fail('App package.json does not pin Composition13 by local archive');
  }
  const entry = lock.packages?.['node_modules/@banodoco/timeline-composition'];
  if (entry?.version !== CURRENT014_GATE3.composition.version || entry?.resolved !== CURRENT014_GATE3.composition.packageResolved) {
    fail('App package-lock.json does not pin the same Composition13 archive');
  }
}

function checkGraph(env) {
  const graph = requiredPath(env, 'TIMELINE_CURRENT014_GATE3_GRAPH_NODE_MODULES');
  if (lstatSync(env.TIMELINE_CURRENT014_GATE3_GRAPH_NODE_MODULES).isSymbolicLink()) {
    fail('effective graph must be a physical directory, not a symlink');
  }
  if (path.basename(graph) !== 'node_modules') fail('effective graph must be its physical node_modules directory');
  if (graph === '/home/user/work/app/node_modules' || graph.startsWith('/home/user/work/runtimes/')) {
    fail('effective graph resolves into a shared dependency install');
  }
  const composition = path.join(graph, '@banodoco/timeline-composition');
  if (!existsSync(composition) || jsonFile(path.join(composition, 'package.json')).version !== CURRENT014_GATE3.composition.version) {
    fail('effective graph does not expose Composition13');
  }
  const compositionReal = realpathSync(composition);
  if (compositionReal.startsWith('/home/user/work/app/node_modules') || compositionReal.startsWith('/home/user/work/runtimes/')) {
    fail('effective graph Composition resolves into a shared dependency install');
  }
  const ready = requiredFile(env, 'TIMELINE_CURRENT014_GATE3_GRAPH_READY');
  const lease = requiredFile(env, 'TIMELINE_CURRENT014_GATE3_GRAPH_LEASE');
  if (!readFileSync(ready, 'utf8').includes('READY')) fail(`effective graph is not marked READY: ${ready}`);
  if (/\b(?:RELEASED|EXPIRED)\b/.test(readFileSync(lease, 'utf8'))) fail(`effective graph lease is not active: ${lease}`);
}

export function readCurrent014Gate3Inputs(env = process.env, appRoot = process.cwd()) {
  const appSha = requiredSha(env, 'TIMELINE_CURRENT014_GATE3_APP_SHA');
  const appTree = requiredSha(env, 'TIMELINE_CURRENT014_GATE3_APP_TREE');
  const agentSha = requiredSha(env, 'TIMELINE_CURRENT014_GATE3_AGENT_SHA');
  const runtimeSha = requiredSha(env, 'TIMELINE_CURRENT014_GATE3_RUNTIME_SHA');
  if (agentSha !== CURRENT014_GATE3.agent.commit) fail(`Agent must be ${CURRENT014_GATE3.agent.commit}`);
  if (runtimeSha !== CURRENT014_GATE3.runtime.commit) fail(`Runtime must be ${CURRENT014_GATE3.runtime.commit}`);
  if (!path.isAbsolute(appRoot)) fail(`App root must be absolute: ${appRoot}`);
  if (env.ASTRID_APP_DIRECT_DIST) fail('ASTRID_APP_DIRECT_DIST is forbidden; use the normal hosted build helper');
  checkGraph(env);
  return Object.freeze({
    app: realpathSync(appRoot), appSha, appTree, agentSha, runtimeSha,
    agent: requiredPath(env, 'ASTRID_CHECKOUT'), runtime: requiredPath(env, 'ASTRID_RUNTIME_CHECKOUT'),
    runtimeProducer: requiredPath(env, 'TIMELINE_CURRENT014_GATE3_RUNTIME_PRODUCER_CHECKOUT'),
    agentPython: requiredExecutable(env, 'ASTRID_PYTHON'),
    runtimePython: requiredExecutable(env, 'ASTRID_RUNTIME_PYTHON'),
    graph: realpathSync(requiredPath(env, 'TIMELINE_CURRENT014_GATE3_GRAPH_NODE_MODULES')),
  });
}

export function checkCurrent014Gate3Sources(input) {
  if (git(input.app, 'rev-parse', '--show-toplevel') !== input.app) fail(`App root is not the current checkout: ${input.app}`);
  if (git(input.app, 'rev-parse', 'HEAD') !== input.appSha) fail(`App source commit changed: expected ${input.appSha}`);
  if (git(input.app, 'rev-parse', 'HEAD^{tree}') !== input.appTree) fail(`App source tree changed: expected ${input.appTree}`);
  if (git(input.agent, 'rev-parse', 'HEAD') !== input.agentSha || git(input.agent, 'rev-parse', 'HEAD^{tree}') !== CURRENT014_GATE3.agent.tree) fail('Agent source identity changed');
  if (git(input.runtime, 'rev-parse', 'HEAD') !== input.runtimeSha || git(input.runtime, 'rev-parse', 'HEAD^{tree}') !== CURRENT014_GATE3.runtime.tree) fail('Runtime source identity changed');
  if (git(input.runtimeProducer, 'rev-parse', 'HEAD') !== CURRENT014_GATE3.runtime.commit || git(input.runtimeProducer, 'rev-parse', 'HEAD^{tree}') !== CURRENT014_GATE3.runtime.tree) fail('Runtime producer source identity changed');
  for (const [root, label] of [[input.app, 'App'], [input.agent, 'Agent'], [input.runtime, 'Runtime'], [input.runtimeProducer, 'Runtime producer']]) checkClean(root, label);
  checkRuntimeLock(input.app, 'App');
  checkRuntimeLock(input.agent, 'Agent');
  checkMetadata(input.app, 'App', APP_METADATA);
  checkMetadata(input.agent, 'Agent', AGENT_METADATA);
  const manifest = jsonFile(path.join(input.runtimeProducer, 'contract/artifacts.json'));
  if (manifest.producer_version !== CURRENT014_GATE3.runtime.producerVersion || Object.keys(manifest.artifacts ?? {}).length !== CURRENT014_GATE3.runtime.artifactCount) {
    fail('Runtime producer is not the all76 artifact manifest');
  }
  checkCompositionArchive(input.app, 'App', 'vendor/artifacts');
  checkCompositionArchive(input.agent, 'Agent', 'remotion/artifacts');
  checkCompositionPackage(input.app);
  const provenance = jsonFile(path.join(input.app, 'vendor/astrid-browser/provenance.json'));
  if (provenance.astrid_commit !== CURRENT014_GATE3.vendorAstridCommit) fail('App Astrid vendor provenance moved');
  const testSource = readFileSync(path.join(input.app, TEST_SOURCE), 'utf8');
  if (!testSource.includes(`nativeNoneTest('${CASE_TITLE}`) || !testSource.includes('expectFreshPreviewUnavailable')) {
    fail('Gate3 test path no longer contains the existing native-None unavailable-preview case');
  }
  return Object.freeze({ appTree: input.appTree, appSha: input.appSha, agent: CURRENT014_GATE3.agent, runtime: CURRENT014_GATE3.runtime, composition: CURRENT014_GATE3.composition, graph: input.graph });
}

export function runCurrent014Gate3() {
  if (process.env.TIMELINE_CURRENT014_GATE3_RUN !== '1'
    || process.env.TIMELINE_CURRENT014_GATE3_MANAGER_APPROVED !== '1'
    || process.env.TIMELINE_CURRENT014_GATE3_CURRENT_FULL_TERMINAL !== '1') {
    fail('set the manager-approved run and current-full-terminal gates before invoking Gate3');
  }
  const input = readCurrent014Gate3Inputs();
  const before = checkCurrent014Gate3Sources(input);
  console.log('[current014/gate3] source preflight passed; caller is M2 native None single');
  let status = 1;
  try {
    status = spawnSync('npm', ['run', 'test:e2e:three-products', '--', '--grep', `^${CASE_TITLE}`], {
      cwd: input.app,
      env: {
        ...process.env,
        ASTRID_CHECKOUT: input.agent,
        ASTRID_RUNTIME_CHECKOUT: input.runtime,
        ASTRID_PYTHON: input.agentPython,
        ASTRID_RUNTIME_PYTHON: input.runtimePython,
        TIMELINE_BUNDLE_AGENT_HEAD: input.agentSha,
        TIMELINE_BUNDLE_RUNTIME_HEAD: input.runtimeSha,
        VITE_TIMELINE_COMPOSITION_ROOT: path.join(input.graph, '@banodoco/timeline-composition'),
      },
      stdio: 'inherit', shell: false,
    }).status ?? 1;
  } finally {
    const after = checkCurrent014Gate3Sources(input);
    if (JSON.stringify(after) !== JSON.stringify(before)) fail('current014 Gate3 sources changed during the browser gate');
    console.log('[current014/gate3] source postflight passed');
  }
  process.exitCode = status;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runCurrent014Gate3();
