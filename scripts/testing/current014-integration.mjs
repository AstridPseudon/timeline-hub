#!/usr/bin/env node

/**
 * Main014 current-source preflight.
 *
 * The App pin is owned by HOME. This wrapper verifies a manager-supplied
 * current App snapshot with the approved pin bytes in its private working
 * overlay; it never edits the App lock or generated files. `preflight` is
 * offline and collection-only. `rows` runs only the existing row-local unit
 * assertions. Browser/socket qualification remains a manager gate.
 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import {
  accessSync, constants, existsSync, readFileSync, realpathSync, statSync,
} from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

export const CURRENT014_APP = Object.freeze({
  pinCommit: '10fa2ff9a8216604aa39e3584f89dc9e7a09080a',
  pinTree: '01fd2a04ff0c383ec5281043c7e5a4c843d1d835',
  pinParent: 'f54cd98ed91de213763b196e4ed770b557897a8b',
  lock: 'sha256:770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e',
  generated: Object.freeze({
    'src/integrations/runtime/generated-contract-metadata.ts': 'sha256:4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044',
    'src/integrations/runtime/generated.ts': 'sha256:c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d',
    'src/integrations/runtime/timeline-commit-types.ts': 'sha256:f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564',
  }),
});

export const CURRENT014_AGENT = Object.freeze({
  commit: '6efc81500a0e0688c2bb41e736503f0fc3e04abb',
  tree: '2ed2b8a12b5b3391ca221ba6ff05390f71a73556',
  schema: 'sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d',
  metadata: 'sha256:cdedeb72880102ff6557320d908eac9068470b5088256c4441514e9d7db40514',
});

export const CURRENT014_RUNTIME = Object.freeze({
  commit: '95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c',
  tree: 'd3a290b407fa61e6ab2d476f50c068073f70df00',
  schema: 'sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816',
  rawSchema: 'sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d',
  manifest: 'sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d',
  producer: 'sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac',
  version: '0.2.14',
  artifactCount: 76,
});

export const CURRENT014_PUBLIC13 = Object.freeze({
  archive: 'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz',
  bytes: 58477,
  sha256: 'sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
  files: 77,
});

export const CURRENT014_ROW_TESTS = Object.freeze([
  'src/tools/video-editor/commands/ordinaryMoveMember.test.ts',
  'src/tools/video-editor/commands/ordinaryRealBatch.test.ts',
  'src/tools/video-editor/commands/ordinaryScalarMember.test.ts',
  'src/tools/video-editor/commands/ordinaryStructuralMember.test.ts',
  'src/tools/video-editor/commands/ordinaryTrimMember.test.ts',
  'src/tools/video-editor/commands/parentClipAddCapture.test.ts',
  'src/tools/video-editor/commands/parentClipSwapCapture.test.ts',
  'src/tools/video-editor/commands/bootstrapCapture.test.ts',
  'src/integrations/runtime/createDefaultTimeline.test.ts',
]);

const FULL_SHA = /^[a-f0-9]{40}$/;
const DIGEST = /^sha256:[a-f0-9]{64}$/;
const APP_METADATA = 'src/integrations/runtime/generated-contract-metadata.ts';
const AGENT_METADATA = 'astrid_runtime_client/contract_metadata.py';
const AGENT_SCHEMA = 'astrid/core/timeline/schema/edit-command.schema.json';
const RUNTIME_SCHEMA = 'contract/schemas/edit-command.json';
const PIN_FILES = Object.freeze(['runtime.lock.json', ...Object.keys(CURRENT014_APP.generated)]);

function fail(message) {
  throw new Error(`[current014] ${message}`);
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
  return value;
}

function requiredFile(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value)) fail(`${name} must be an absolute path`);
  if (!existsSync(value) || !statSync(value).isFile()) fail(`${name} must name a file: ${value}`);
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

function sha256File(file) {
  return `sha256:${createHash('sha256').update(readFileSync(file)).digest('hex')}`;
}

function jsonFile(file) {
  try { return JSON.parse(readFileSync(file, 'utf8')); }
  catch (error) { fail(`cannot read JSON ${file}: ${error.message}`); }
}

export function readCurrent014Inputs(env = process.env, appRoot = process.cwd()) {
  const appTree = requiredSha(env, 'TIMELINE_CURRENT014_APP_TREE');
  const pinCommit = requiredSha(env, 'TIMELINE_CURRENT014_PIN_COMMIT');
  const pinTree = requiredSha(env, 'TIMELINE_CURRENT014_PIN_TREE');
  const agentSha = requiredSha(env, 'TIMELINE_CURRENT014_AGENT_SHA');
  const runtimeSha = requiredSha(env, 'TIMELINE_CURRENT014_RUNTIME_SHA');
  if (pinCommit !== CURRENT014_APP.pinCommit) fail(`TIMELINE_CURRENT014_PIN_COMMIT must be ${CURRENT014_APP.pinCommit}`);
  if (pinTree !== CURRENT014_APP.pinTree) fail(`TIMELINE_CURRENT014_PIN_TREE must be ${CURRENT014_APP.pinTree}`);
  if (agentSha !== CURRENT014_AGENT.commit) fail(`TIMELINE_CURRENT014_AGENT_SHA must be ${CURRENT014_AGENT.commit}`);
  if (runtimeSha !== CURRENT014_RUNTIME.commit) fail(`TIMELINE_CURRENT014_RUNTIME_SHA must be ${CURRENT014_RUNTIME.commit}`);
  if (!path.isAbsolute(appRoot)) fail(`App root must be absolute: ${appRoot}`);
  const app = realpathSync(appRoot);
  const agent = requiredPath(env, 'ASTRID_CHECKOUT');
  const runtime = requiredPath(env, 'ASTRID_RUNTIME_CHECKOUT');
  const runtimeProducer = requiredPath(env, 'TIMELINE_CURRENT014_RUNTIME_PRODUCER_CHECKOUT');
  const node = requiredExecutable(env, 'ASTRID_NODE_EXECUTABLE');
  const vitestRunner = requiredFile(env, 'TIMELINE_CURRENT014_VITEST_RUNNER');
  if (env.ASTRID_APP_DIRECT_DIST) fail('ASTRID_APP_DIRECT_DIST is forbidden; the current source must decide build freshness');
  return Object.freeze({ app, appTree, pinCommit, pinTree, agent, agentSha, runtime, runtimeSha, runtimeProducer, node, vitestRunner });
}

function checkHead(root, expected, label) {
  const actual = git(root, 'rev-parse', 'HEAD');
  if (actual !== expected) fail(`${label} HEAD changed: expected ${expected}, got ${actual}`);
  return actual;
}

function checkTree(root, expected, label) {
  const actual = git(root, 'rev-parse', 'HEAD^{tree}');
  if (actual !== expected) fail(`${label} source tree changed: expected ${expected}, got ${actual}`);
  return actual;
}

function checkClean(root, label) {
  const status = git(root, 'status', '--porcelain', '--untracked-files=normal');
  if (status) fail(`${label} source is dirty:\n${status}`);
}

function checkAppOverlay(root) {
  const status = git(root, 'status', '--porcelain', '--untracked-files=normal');
  const unexpected = status.split('\n').filter(Boolean).filter((line) => !PIN_FILES.includes(line.slice(3)));
  if (unexpected.length) fail(`App overlay contains non-pin changes:\n${unexpected.join('\n')}`);
}

function checkMetadata(root, label, metadataFile) {
  const file = path.join(root, metadataFile);
  const source = readFileSync(file, 'utf8');
  const get = (name) => {
    const match = source.match(new RegExp(`${name}\\s*=\\s*["']([^"']+)["']`));
    if (!match) fail(`${label} metadata is missing ${name}: ${file}`);
    return match[1];
  };
  if (get('CONTRACT_VERSION') !== CURRENT014_RUNTIME.version) fail(`${label} contract is not ${CURRENT014_RUNTIME.version}`);
  if (get('SCHEMA_DIGEST') !== CURRENT014_RUNTIME.schema) fail(`${label} schema is not ${CURRENT014_RUNTIME.schema}`);
  if (get('COMPONENT_MANIFEST_SHA256') !== 'sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5') {
    fail(`${label} component manifest is not the Main014 artifact`);
  }
  return sha256File(file);
}

function checkLock(root) {
  const file = path.join(root, 'runtime.lock.json');
  const lock = jsonFile(file);
  if (Object.keys(lock.files ?? {}).length !== 13) fail('App Runtime lock must contain exactly 13 entries');
  if (lock.producer !== 'astrid-runtime') fail(`App Runtime lock producer is ${lock.producer}`);
  if (lock.source_commit !== CURRENT014_RUNTIME.commit) fail(`App Runtime lock source is ${lock.source_commit}, expected ${CURRENT014_RUNTIME.commit}`);
  if (lock.producer_version !== CURRENT014_RUNTIME.producer) fail(`App Runtime lock artifact is ${lock.producer_version}, expected ${CURRENT014_RUNTIME.producer}`);
  const digest = sha256File(file);
  if (digest !== CURRENT014_APP.lock) fail(`App Runtime lock bytes are ${digest}, expected ${CURRENT014_APP.lock}`);
  for (const [relative, expected] of Object.entries(CURRENT014_APP.generated)) {
    const actual = sha256File(path.join(root, relative));
    if (actual !== expected) fail(`${relative} is ${actual}, expected approved HOME pin bytes ${expected}`);
  }
  return { digest, generated: { ...CURRENT014_APP.generated } };
}

function checkRuntimeManifest(root) {
  const file = path.join(root, 'contract/artifacts.json');
  if (sha256File(file) !== CURRENT014_RUNTIME.manifest) fail('Runtime artifact manifest bytes changed');
  const manifest = jsonFile(file);
  if (manifest.producer !== 'astrid-runtime' || manifest.version !== CURRENT014_RUNTIME.producer) {
    fail('Runtime artifact manifest producer/version mismatch');
  }
  if (Object.keys(manifest.artifacts ?? {}).length !== CURRENT014_RUNTIME.artifactCount) {
    fail(`Runtime artifact manifest must contain ${CURRENT014_RUNTIME.artifactCount} entries`);
  }
  return { digest: CURRENT014_RUNTIME.manifest, artifactCount: Object.keys(manifest.artifacts).length };
}

function checkPublic13Archive(root) {
  const file = path.join(root, CURRENT014_PUBLIC13.archive);
  if (!existsSync(file)) fail(`public13 Composition archive is missing: ${file}`);
  if (statSync(file).size !== CURRENT014_PUBLIC13.bytes || sha256File(file) !== CURRENT014_PUBLIC13.sha256) {
    fail('public13 Composition archive bytes do not match the approved immutable artifact');
  }
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
    .trim().split('\n').filter((member) => member && !member.endsWith('/'));
  if (members.length !== CURRENT014_PUBLIC13.files || new Set(members).size !== members.length) {
    fail(`public13 Composition archive must contain exactly ${CURRENT014_PUBLIC13.files} regular files`);
  }
  return { digest: CURRENT014_PUBLIC13.sha256, files: members.length };
}

function checkBootstrapRollback(root) {
  const source = readFileSync(path.join(root, 'src/integrations/runtime/createDefaultTimeline.ts'), 'utf8');
  if (!source.includes('publishParentComposition(')) {
    fail('HOME bootstrap rollback is missing the published parent-composition initializer');
  }
  if (source.includes('timeline.init')) {
    fail('native timeline.init is live in the current App bootstrap path; isolate it to staged14 only');
  }
}

function runVendorCheck(input) {
  const script = path.join(input.app, 'scripts/vendor-lock.mjs');
  const result = spawnSync(input.node, [script, 'check', path.join(input.app, 'runtime.lock.json'), '--producer', input.runtimeProducer], {
    cwd: input.app, env: process.env, stdio: 'inherit', shell: false,
  });
  if (result.status !== 0) fail(`normal Runtime vendor-lock check failed (exit ${result.status ?? 'signal'})`);
}

function runPublic13Guards(input) {
  const result = spawnSync(input.node, [
    '--test', '--test-concurrency=1', 'config/vite/timelineCompositionPackage.test.mjs',
  ], {
    cwd: input.app,
    env: {
      ...process.env,
      ASTRID_CHECKOUT: input.agent,
      ASTRID_PUBLIC_CHECKOUT: input.agent,
      VITEST_CACHE_DIR: path.join(input.app, '.current014-vitest-cache'),
    },
    stdio: 'inherit', shell: false,
  });
  if (result.status !== 0) fail(`Node+Vite public13 guards failed (exit ${result.status ?? 'signal'})`);
}

function runRowTests(input, { collectOnly }) {
  const vitest = path.join(input.app, 'node_modules/vitest/vitest.mjs');
  const args = ['--require', input.vitestRunner, vitest, collectOnly ? 'list' : 'run', '--config', 'config/testing/vitest.config.ts', '--configLoader=runner', '--no-cache', '--maxWorkers=1', '--no-file-parallelism', ...CURRENT014_ROW_TESTS];
  const result = spawnSync(input.node, args, {
    cwd: input.app,
    env: { ...process.env, VITEST_CACHE_DIR: path.join(input.app, '.current014-vitest-cache') },
    stdio: 'inherit', shell: false,
  });
  if (result.status !== 0) fail(`current014 row ${collectOnly ? 'collection' : 'assertion'} lane failed (exit ${result.status ?? 'signal'})`);
}

export function checkCurrent014Sources(input, { public13 = true, vendor = true } = {}) {
  if (git(input.app, 'rev-parse', '--show-toplevel') !== input.app) fail(`App root is not the current checkout: ${input.app}`);
  checkTree(input.app, input.appTree, 'App');
  checkHead(input.agent, input.agentSha, 'Agent');
  checkTree(input.agent, CURRENT014_AGENT.tree, 'Agent');
  checkHead(input.runtime, input.runtimeSha, 'Runtime');
  checkTree(input.runtime, CURRENT014_RUNTIME.tree, 'Runtime');
  checkHead(input.runtimeProducer, input.runtimeSha, 'Runtime producer');
  checkTree(input.runtimeProducer, CURRENT014_RUNTIME.tree, 'Runtime producer');
  checkClean(input.agent, 'Agent');
  checkClean(input.runtime, 'Runtime');
  checkClean(input.runtimeProducer, 'Runtime producer');
  checkAppOverlay(input.app);
  checkBootstrapRollback(input.app);
  const lock = checkLock(input.app);
  const appMetadata = checkMetadata(input.app, 'App', APP_METADATA);
  const agentMetadata = checkMetadata(input.agent, 'Agent', AGENT_METADATA);
  const agentSchema = sha256File(path.join(input.agent, AGENT_SCHEMA));
  const runtimeSchema = sha256File(path.join(input.runtime, RUNTIME_SCHEMA));
  if (agentSchema !== CURRENT014_AGENT.schema || runtimeSchema !== CURRENT014_RUNTIME.rawSchema || agentSchema !== runtimeSchema) {
    fail('Agent/Runtime raw edit-command schema bytes do not match Main014');
  }
  const runtimeManifest = checkRuntimeManifest(input.runtimeProducer);
  const public13Archive = checkPublic13Archive(input.app);
  if (vendor) runVendorCheck(input);
  if (public13) runPublic13Guards(input);
  return Object.freeze({
    app: { root: input.app, tree: input.appTree, lock, metadata: appMetadata, public13: public13Archive },
    agent: { root: input.agent, commit: input.agentSha, tree: CURRENT014_AGENT.tree, metadata: agentMetadata },
    runtime: { root: input.runtime, commit: input.runtimeSha, tree: CURRENT014_RUNTIME.tree },
    runtimeProducer: { root: input.runtimeProducer, commit: input.runtimeSha, tree: CURRENT014_RUNTIME.tree, manifest: runtimeManifest },
  });
}

export function runCurrent014Preflight() {
  if (process.env.TIMELINE_CURRENT014_RUN !== '1') fail('set TIMELINE_CURRENT014_RUN=1 only for the manager-reviewed exact cohort');
  const input = readCurrent014Inputs();
  const before = checkCurrent014Sources(input);
  runRowTests(input, { collectOnly: true });
  const after = checkCurrent014Sources(input);
  if (JSON.stringify(after) !== JSON.stringify(before)) fail('source checks changed during current014 preflight');
  console.log('[current014] exact source, normal lock, public13, and row collection guards passed');
}

export function runCurrent014Rows() {
  if (process.env.TIMELINE_CURRENT014_RUN !== '1') fail('set TIMELINE_CURRENT014_RUN=1 only for the manager-reviewed exact cohort');
  const input = readCurrent014Inputs();
  const before = checkCurrent014Sources(input);
  runRowTests(input, { collectOnly: false });
  const after = checkCurrent014Sources(input);
  if (JSON.stringify(after) !== JSON.stringify(before)) fail('source checks changed during current014 row assertions');
  console.log('[current014] exact source and existing ordinary/parent/bootstrap assertions passed');
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const mode = process.argv[2] ?? 'preflight';
  if (mode === 'preflight') runCurrent014Preflight();
  else if (mode === 'rows') runCurrent014Rows();
  else fail(`unknown mode ${mode}; expected preflight or rows`);
}
