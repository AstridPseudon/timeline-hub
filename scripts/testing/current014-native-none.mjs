#!/usr/bin/env node

/**
 * Central App014 native-None qualification launcher.
 *
 * The browser cases remain the real current-root three-products lane. This
 * wrapper only freezes the exact source/cohort and the producer artifacts
 * before and after that lane.
 */
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import {
  accessSync, constants, existsSync, lstatSync, readFileSync, realpathSync, statSync, symlinkSync, unlinkSync,
} from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

export const CURRENT014 = Object.freeze({
  appParent: '67e26ef349b5a9e3a08d67acab0ae37a5cfda98f',
  agent: '3c4f6de4fa777323b3386c01c7266b619b86af6d',
  agentTree: 'aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c',
  runtime: '202074110717146fc7f08af2306a8dd7f695b0b1',
  runtimeTree: 'ee39286bd0eb27d4075074cc4785d6d15e33f243',
  producer: 'a0dca16975dfe8f5e762703b99d9791a16cf7fd7',
  producerTree: '4b7dd0fe44be973c344bab3de568eaf0bdd28476',
  version: '0.2.14',
  producerVersion: 'sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0',
  schemaDigest: 'sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59',
  rawSchema: 'sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d',
  artifactManifest: 'sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815',
  componentManifest: 'sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5',
  artifactCount: 75,
  schemaDefs: 55,
  schemaOps: 29,
});

export const CURRENT014_COMPOSITION = Object.freeze({
  appArchive: 'banodoco-timeline-composition-0.0.13.tgz',
  appSha256: 'sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
  agentArchive: 'banodoco-timeline-composition-0.0.12.tgz',
  agentSha256: 'sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3',
  fileCount: 77,
});

const FULL_SHA = /^[a-f0-9]{40}$/;
const DIGEST = /^sha256:[a-f0-9]{64}$/;
const APP_METADATA = 'src/integrations/runtime/generated-contract-metadata.ts';
const AGENT_METADATA = 'astrid_runtime_client/contract_metadata.py';

function fail(message) { throw new Error(`[current014] ${message}`); }

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
  if (!existsSync(value) || !statSync(value).isDirectory()) fail(`${name} must name an existing directory: ${value}`);
  return realpathSync(value);
}

function requiredExecutable(env, name) {
  const value = required(env, name);
  if (!path.isAbsolute(value) || !existsSync(value) || !statSync(value).isFile()) fail(`${name} must name an absolute executable file`);
  try { accessSync(value, constants.X_OK); } catch { fail(`${name} must be executable: ${value}`); }
  return value;
}

function git(root, ...args) {
  try { return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim(); }
  catch (error) { fail(`git ${args.join(' ')} failed in ${root}: ${error.message}`); }
}

function sha256File(file) { return `sha256:${createHash('sha256').update(readFileSync(file)).digest('hex')}`; }

function jsonFile(file) {
  try { return JSON.parse(readFileSync(file, 'utf8')); }
  catch (error) { fail(`cannot read JSON ${file}: ${error.message}`); }
}

export function readCurrent014Inputs(env = process.env, appRoot = process.cwd()) {
  const appTree = requiredSha(env, 'TIMELINE_CURRENT014_APP_TREE');
  const appParent = requiredSha(env, 'TIMELINE_CURRENT014_APP_PARENT_SHA');
  if (appParent !== CURRENT014.appParent) fail(`TIMELINE_CURRENT014_APP_PARENT_SHA must be ${CURRENT014.appParent}`);
  const agent = requiredPath(env, 'ASTRID_CHECKOUT');
  const runtime = requiredPath(env, 'ASTRID_RUNTIME_CHECKOUT');
  const producer = requiredPath(env, 'TIMELINE_CURRENT014_RUNTIME_PRODUCER_CHECKOUT');
  const agentPython = requiredExecutable(env, 'ASTRID_PYTHON');
  const runtimePython = requiredExecutable(env, 'ASTRID_RUNTIME_PYTHON');
  if (env.ASTRID_APP_DIRECT_DIST) fail('ASTRID_APP_DIRECT_DIST is forbidden; the current-root build helper must decide dist freshness');
  if (env.ASTRID_PUBLIC_CHECKOUT) fail('ASTRID_PUBLIC_CHECKOUT is forbidden; public package overlays are not a producer source');
  if (!path.isAbsolute(appRoot)) fail(`App root must be absolute: ${appRoot}`);
  return Object.freeze({ app: realpathSync(appRoot), appTree, appParent, agent, runtime, producer, agentPython, runtimePython });
}

function checkHead(root, expected, label) {
  const actual = git(root, 'rev-parse', 'HEAD');
  if (actual !== expected) fail(`${label} HEAD changed: expected ${expected}, got ${actual}`);
  return actual;
}

function checkTree(root, expected, label) {
  const actual = git(root, 'rev-parse', 'HEAD^{tree}');
  if (actual !== expected) fail(`${label} tree changed: expected ${expected}, got ${actual}`);
  return actual;
}

function checkClean(root, label) {
  const status = git(root, 'status', '--porcelain', '--untracked-files=normal');
  if (status) fail(`${label} source is dirty:\n${status}`);
}

function checkLock(root, label) {
  const lock = jsonFile(path.join(root, 'runtime.lock.json'));
  if (lock.producer !== 'astrid-runtime') fail(`${label} Runtime lock producer is ${lock.producer}`);
  if (lock.source_commit !== CURRENT014.producer) fail(`${label} Runtime producer source pin is ${lock.source_commit}`);
  if (lock.producer_version !== CURRENT014.producerVersion) fail(`${label} Runtime artifact pin is ${lock.producer_version}`);
  return { sourceCommit: lock.source_commit, producerVersion: lock.producer_version, file: sha256File(path.join(root, 'runtime.lock.json')) };
}

function checkMetadata(root, label, fileName) {
  const file = path.join(root, fileName);
  const source = readFileSync(file, 'utf8');
  const get = (name) => {
    const match = source.match(new RegExp(`${name}\\s*=\\s*["']([^"']+)["']`));
    if (!match) fail(`${label} metadata is missing ${name}`);
    return match[1];
  };
  if (get('CONTRACT_VERSION') !== CURRENT014.version) fail(`${label} contract is not ${CURRENT014.version}`);
  if (get('SCHEMA_DIGEST') !== CURRENT014.schemaDigest) fail(`${label} schema is not ${CURRENT014.schemaDigest}`);
  if (get('COMPONENT_MANIFEST_SHA256') !== CURRENT014.componentManifest) fail(`${label} component manifest is not ${CURRENT014.componentManifest}`);
  return { file: sha256File(file), contract: CURRENT014.version, schema: CURRENT014.schemaDigest, componentManifest: CURRENT014.componentManifest };
}

function checkProducerArtifacts(root) {
  const schemaFile = path.join(root, 'contract/schemas/edit-command.json');
  if (sha256File(schemaFile) !== CURRENT014.rawSchema) fail(`producer raw command schema is not ${CURRENT014.rawSchema}`);
  const schema = jsonFile(schemaFile);
  if (Object.keys(schema.$defs ?? {}).length !== CURRENT014.schemaDefs) fail(`producer command schema has ${Object.keys(schema.$defs ?? {}).length} defs, expected ${CURRENT014.schemaDefs}`);
  if ((schema.$defs?.EditCommand?.allOf ?? []).length !== CURRENT014.schemaOps) fail(`producer command schema has ${(schema.$defs?.EditCommand?.allOf ?? []).length} ops, expected ${CURRENT014.schemaOps}`);
  const file = path.join(root, 'contract/artifacts.json');
  if (sha256File(file) !== CURRENT014.artifactManifest) fail(`producer artifact manifest digest changed`);
  const manifest = jsonFile(file);
  if (manifest.producer !== 'astrid-runtime' || manifest.version !== CURRENT014.producerVersion) fail('producer artifact manifest identity changed');
  const entries = Object.entries(manifest.artifacts ?? {});
  if (entries.length !== CURRENT014.artifactCount) fail(`producer artifact manifest has ${entries.length} entries, expected ${CURRENT014.artifactCount}`);
  for (const [relative, digest] of entries) {
    const artifact = path.join(root, relative);
    if (!existsSync(artifact) || !statSync(artifact).isFile()) fail(`producer artifact is missing: ${relative}`);
    if (sha256File(artifact) !== digest) fail(`producer artifact digest changed: ${relative}`);
  }
  return { file: CURRENT014.artifactManifest, artifactCount: entries.length, rawSchema: CURRENT014.rawSchema, schemaDefs: CURRENT014.schemaDefs, schemaOps: CURRENT014.schemaOps };
}

function checkArchive(root, label, archive, expectedDigest) {
  const file = path.join(root, archive);
  if (!existsSync(file) || sha256File(file) !== expectedDigest) fail(`${label} Composition archive digest changed`);
  const members = execFileSync('tar', ['-tzf', file], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim().split('\n')
    .filter((member) => member && !member.endsWith('/'));
  if (members.length !== CURRENT014_COMPOSITION.fileCount || new Set(members).size !== members.length) fail(`${label} Composition archive must contain exactly ${CURRENT014_COMPOSITION.fileCount} regular files`);
  if (members.some((member) => !member.startsWith('package/') || member.slice('package/'.length).split('/').includes('..'))) fail(`${label} Composition archive contains an unsafe member`);
  return { archive, digest: expectedDigest, fileCount: members.length };
}

function runVendorCheck(input, root, command, label) {
  const script = command === 'node' ? path.join(input.app, 'scripts/vendor-lock.mjs') : path.join(input.agent, 'scripts/vendor_lock.py');
  const result = spawnSync(command, [script, 'check', path.join(root, 'runtime.lock.json'), '--producer', input.producer], { cwd: root, env: process.env, stdio: 'inherit', shell: false });
  if (result.status !== 0) fail(`${label} normal Runtime vendor-lock check failed (exit ${result.status ?? 'signal'})`);
}

export function checkCurrent014Sources(input, { vendor = true } = {}) {
  if (git(input.app, 'rev-parse', '--show-toplevel') !== input.app) fail(`App root is not the current checkout: ${input.app}`);
  const appTree = checkTree(input.app, input.appTree, 'App');
  if (git(input.app, 'rev-parse', 'HEAD^') !== input.appParent) fail(`App source parent is not the committed staged branch ${input.appParent}`);
  checkHead(input.agent, CURRENT014.agent, 'Agent');
  const agentTree = checkTree(input.agent, CURRENT014.agentTree, 'Agent');
  checkHead(input.runtime, CURRENT014.runtime, 'Runtime');
  const runtimeTree = checkTree(input.runtime, CURRENT014.runtimeTree, 'Runtime');
  checkHead(input.producer, CURRENT014.producer, 'Runtime producer');
  const producerTree = checkTree(input.producer, CURRENT014.producerTree, 'Runtime producer');
  checkClean(input.app, 'App'); checkClean(input.agent, 'Agent'); checkClean(input.runtime, 'Runtime'); checkClean(input.producer, 'Runtime producer');
  const appLock = checkLock(input.app, 'App'); const agentLock = checkLock(input.agent, 'Agent');
  const appMetadata = checkMetadata(input.app, 'App', APP_METADATA); const agentMetadata = checkMetadata(input.agent, 'Agent', AGENT_METADATA);
  const producerArtifacts = checkProducerArtifacts(input.producer);
  const appComposition = checkArchive(input.app, 'App', `vendor/artifacts/${CURRENT014_COMPOSITION.appArchive}`, CURRENT014_COMPOSITION.appSha256);
  const agentComposition = checkArchive(input.agent, 'Agent', `remotion/artifacts/${CURRENT014_COMPOSITION.agentArchive}`, CURRENT014_COMPOSITION.agentSha256);
  if (vendor) { runVendorCheck(input, input.app, 'node', 'App'); runVendorCheck(input, input.agent, input.agentPython, 'Agent'); }
  return Object.freeze({ app: { tree: appTree, parent: input.appParent, lock: appLock, metadata: appMetadata, composition: appComposition }, agent: { commit: CURRENT014.agent, tree: agentTree, lock: agentLock, metadata: agentMetadata, composition: agentComposition }, runtime: { commit: CURRENT014.runtime, tree: runtimeTree }, producer: { commit: CURRENT014.producer, tree: producerTree, artifacts: producerArtifacts } });
}

function usePrivateNodeModules(input) {
  const privateModules = requiredPath(process.env, 'TIMELINE_CURRENT014_PRIVATE13_NODE_MODULES');
  const localModules = path.join(input.app, 'node_modules');
  if (lstatSync(localModules).isSymbolicLink()) {
    const shared = realpathSync(localModules);
    if (shared === privateModules) return;
    // This is the central snapshot's disposable link, never the shared install.
    unlinkSync(localModules);
    symlinkSync(privateModules, localModules);
  }
}

export function runCurrent014NativeNone() {
  if (process.env.TIMELINE_CURRENT014_RUN !== '1') fail('set TIMELINE_CURRENT014_RUN=1 only for the exact App014 cohort');
  const input = readCurrent014Inputs();
  const before = checkCurrent014Sources(input);
  usePrivateNodeModules(input);
  const listed = spawnSync('node_modules/.bin/playwright', ['test', '--config', 'playwright.three-products.config.ts', '--grep', 'M2 native None', '--list'], { cwd: input.app, env: process.env, stdio: 'pipe', shell: false });
  if (listed.status !== 0) fail(`native-None discovery failed:\n${listed.stderr.toString()}`);
  const discovered = listed.stdout.toString().split('\n').filter((line) => line.includes('M2 native None'));
  if (discovered.length !== 2) fail(`expected exactly two native-None tests, discovered ${discovered.length}`);
  console.log('[current014] exact source/artifact preflight passed; running the two native-None cases');
  const childEnv = { ...process.env, ASTRID_CHECKOUT: input.agent, ASTRID_RUNTIME_CHECKOUT: input.runtime, ASTRID_PYTHON: input.agentPython, ASTRID_RUNTIME_PYTHON: input.runtimePython, TIMELINE_BUNDLE_AGENT_HEAD: CURRENT014.agent, TIMELINE_BUNDLE_RUNTIME_HEAD: CURRENT014.runtime };
  let status = 1;
  try { status = spawnSync('node_modules/.bin/playwright', ['test', '--config', 'playwright.three-products.config.ts', '--grep', 'M2 native None'], { cwd: input.app, env: childEnv, stdio: 'inherit', shell: false }).status ?? 1; }
  finally { const after = checkCurrent014Sources(input); if (JSON.stringify(after) !== JSON.stringify(before)) fail('source checks changed between the start and end of the browser gate'); console.log('[current014] exact source/artifact postflight passed'); }
  process.exitCode = status;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) runCurrent014NativeNone();
