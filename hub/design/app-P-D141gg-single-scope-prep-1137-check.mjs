import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [originalPath, packetPath, ...rest] = process.argv.slice(2);
const mode = rest[0] ?? 'verify';
assert(originalPath && packetPath, 'usage: check.mjs ORIGINAL_DISPATCH_JSON PACKET_JSON [verify]');
assert(['verify', 'emit'].includes(mode), `unsupported mode: ${mode}`);

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'));
const originalDocument = readJson(originalPath);
const original = originalDocument.dispatches[2];
assert(original, 'dispatches[2] is required');
const packet = existsSync(packetPath) ? readJson(packetPath) : null;
const assignedEvidence = path.dirname(packetPath);
const originalSourceManifest = readJson(path.join(path.dirname(originalPath), 'source-manifest.json'));

const builderPath = original.argv.find((value) => value.endsWith('/scripts/testing/d66-plain-stack.mjs'));
assert(builderPath, 'original executable argv must identify the builder path');
const builderBytes = readFileSync(builderPath);
const builderSha = sha256(builderBytes);
const builderRelative = path.relative(original.cwd, builderPath);
const git = (cwd, args) => execFileSync('git', ['-C', cwd, ...args], { encoding: 'utf8' }).trim();
const sourceState = (role) => {
  const expected = original.pins[role];
  const checkout = original.checkouts[role];
  const root = git(checkout, ['rev-parse', '--show-toplevel']);
  const state = {
    checkout,
    root,
    head: git(checkout, ['rev-parse', 'HEAD']),
    tree: git(checkout, ['rev-parse', 'HEAD^{tree}']),
    branch: (() => { try { return git(checkout, ['symbolic-ref', '--quiet', '--short', 'HEAD']); } catch { return null; } })(),
    dirty: Boolean(git(checkout, ['status', '--porcelain=v1', '--untracked-files=all'])),
  };
  assert.equal(checkout, original.checkouts[role], `${role} exact checkout changed`);
  assert.equal(state.head, expected.head, `${role} HEAD drifted from original recipe`);
  assert.equal(state.tree, expected.tree, `${role} tree drifted from original recipe`);
  assert.equal(state.branch, null, `${role} checkout must remain detached`);
  assert.equal(state.dirty, false, `${role} checkout must remain clean`);
  return { expected, actual: state, equal: true };
};

const sources = Object.fromEntries(Object.keys(original.pins).map((role) => [role, sourceState(role)]));
const originalBuilderMetadata = originalSourceManifest.before[builderPath];
assert(originalBuilderMetadata, 'original source manifest must record the builder path');
const originalBuilderBlob = originalSourceManifest.builder_blob;
const actualBuilderBlob = git(original.cwd, ['rev-parse', `${original.pins.app.head}:${builderRelative}`]);
assert.equal(builderSha, originalBuilderMetadata.sha256, 'builder file changed');
assert.equal(builderBytes.length, originalBuilderMetadata.bytes, 'builder byte count changed');
assert.equal(actualBuilderBlob, originalBuilderBlob, 'builder Git blob changed');

const builder = await import(pathToFileURL(builderPath).href);
const pins = Object.fromEntries(Object.entries(original.pins).map(([role, value]) => [role, {
  checkout: value.checkout,
  head: value.head,
  tree: value.tree,
}]));
const checkouts = { ...original.checkouts };
const purePlan = builder.buildSubmitPlan({ name: original.selector, target: original.target, pins, checkouts });
assert.deepEqual(purePlan.pins, pins, 'pure buildSubmitPlan changed source pins');
assert.deepEqual(purePlan.checkouts, checkouts, 'pure buildSubmitPlan changed exact checkouts');
const pureRecipes = {
  preflight: builder.serviceRecipe({ name: original.selector, pins, checkouts, preflight: true }),
  normal: builder.serviceRecipe({ name: original.selector, pins, checkouts }),
};
assert.deepEqual(pureRecipes, original.recipes, 'pure serviceRecipe changed original command bytes');

const digest = (value) => sha256(Buffer.from(value));
const expectedNormal = `${original.suites.normal}-single-scope-2`;
const expectedSuites = { normal: expectedNormal, preflight: `${expectedNormal}-preflight` };
const expectedRows = Object.fromEntries(Object.entries(pureRecipes).map(([phase, command]) => [
  phase, `app ${expectedSuites[phase]} ${command}\n`,
]));
const futureRoot = path.join(assignedEvidence, 'future-native', expectedNormal);
const expectedPaths = {
  output: path.join(futureRoot, 'output'),
  plan: path.join(futureRoot, 'submit-plan.json'),
  lock: path.join(futureRoot, 'submit-plan.json.lock'),
  stdout: path.join(futureRoot, 'native-submit.stdout.log'),
  stderr: path.join(futureRoot, 'native-submit.stderr.log'),
};
const expectedEnvironment = {
  ...original.environment,
  D66_SUBMIT_SUITE: expectedNormal,
  D66_SUBMIT_PLAN_PATH: expectedPaths.plan,
  D66_OUTPUT_DIR: expectedPaths.output,
};
const expectedPacket = {
  schema: 'd141gg-single-scope-source-packet-v1',
  selector: original.selector,
  attempt_scope: 'single-scope-2',
  target: original.target,
  pins: original.pins,
  checkouts: original.checkouts,
  recipes: pureRecipes,
  suites: expectedSuites,
  rows: expectedRows,
  command_sha256: Object.fromEntries(Object.entries(pureRecipes).map(([phase, value]) => [phase, digest(value)])),
  row_sha256: Object.fromEntries(Object.entries(expectedRows).map(([phase, value]) => [phase, digest(value)])),
  environment: expectedEnvironment,
  argv: original.argv,
  cwd: original.cwd,
  environment_unset: original.environment_unset,
  operational_environment: original.operational_environment,
  paths: expectedPaths,
  registration: false,
  native_side_effects: false,
};
const candidate = packet ?? expectedPacket;
assert.equal(candidate.schema, expectedPacket.schema);
for (const key of ['selector', 'attempt_scope', 'target', 'pins', 'checkouts', 'recipes', 'suites', 'rows',
  'command_sha256', 'row_sha256', 'environment', 'argv', 'cwd', 'environment_unset',
  'operational_environment', 'paths', 'registration', 'native_side_effects']) {
  assert.deepEqual(candidate[key], expectedPacket[key], `packet field mismatch: ${key}`);
}
assert(!Object.hasOwn(candidate, 'body_ids'), 'body IDs must be absent');
assert(!Object.hasOwn(candidate, 'normal') && !Object.hasOwn(candidate, 'preflight'), 'native result IDs must be absent');
assert(!Object.hasOwn(candidate, 'request_id') && !Object.hasOwn(candidate, 'artifact_id'), 'native IDs must be absent');
for (const phase of ['normal', 'preflight']) {
  assert.equal(digest(candidate.recipes[phase]), candidate.command_sha256[phase], `${phase} command digest mismatch`);
  assert.equal(digest(candidate.rows[phase]), candidate.row_sha256[phase], `${phase} row digest mismatch`);
  assert.equal(candidate.rows[phase], `app ${candidate.suites[phase]} ${candidate.recipes[phase]}\n`, `${phase} row binding mismatch`);
}
for (const role of Object.keys(original.pins)) {
  assert.deepEqual(candidate.pins[role], original.pins[role], `${role} source tuple changed`);
  assert.equal(candidate.environment[`D66_${role.toUpperCase()}_SHA`], original.environment[`D66_${role.toUpperCase()}_SHA`]);
  assert.equal(candidate.environment[`D66_${role.toUpperCase()}_TREE`], original.environment[`D66_${role.toUpperCase()}_TREE`]);
  assert.equal(candidate.environment[`D66_${role.toUpperCase()}_CHECKOUT`], original.environment[`D66_${role.toUpperCase()}_CHECKOUT`]);
}
for (const key of ['argv', 'cwd', 'environment_unset', 'operational_environment']) {
  assert.deepEqual(candidate[key], original[key], `${key} changed`);
}
for (const [key, value] of Object.entries(expectedPaths)) {
  assert(path.isAbsolute(value), `${key} must be absolute`);
  assert(value.startsWith(futureRoot + path.sep), `${key} escaped future namespace`);
  assert(!existsSync(value), `${key} unexpectedly exists; no native artifact/output may be created`);
}
const registryPath = path.resolve(path.dirname(originalPath), '../../../tests/suites.conf');
const newRows = readFileSync(registryPath, 'utf8').split('\n').filter((line) => line.split(/\s+/, 3)[1] === expectedNormal || line.split(/\s+/, 3)[1] === expectedSuites.preflight);
assert.deepEqual(newRows, [], 'new suite namespace must not be registered');

if (mode === 'emit') {
  writeFileSync(packetPath, `${JSON.stringify(expectedPacket, null, 2)}\n`);
  writeFileSync(path.join(assignedEvidence, 'source-manifest.json'), `${JSON.stringify({
    schema: 'd141gg-single-scope-source-manifest-v1',
    original_recipe_path: originalPath,
    original_source_manifest_path: path.join(path.dirname(originalPath), 'source-manifest.json'),
    original_recipe: original,
    pure_builder: { path: builderPath, sha256: builderSha, blob: actualBuilderBlob, bytes: builderBytes.length,
      expected_sha256: originalBuilderMetadata.sha256, expected_blob: originalBuilderBlob },
    sources,
    original_command_row_metadata: { recipes: original.recipes, suites: original.suites,
      rows: original.rows, command_sha256: original.command_sha256, row_sha256: original.row_sha256 },
    new_command_row_metadata: { recipes: pureRecipes, suites: expectedSuites, rows: expectedRows,
      command_sha256: expectedPacket.command_sha256, row_sha256: expectedPacket.row_sha256 },
    namespace: { future_root: futureRoot, paths: expectedPaths, registration: false, native_ids: false },
  }, null, 2)}\n`);
  writeFileSync(path.join(assignedEvidence, 'controls.json'), `${JSON.stringify({
    schema: 'd141gg-source-controls-v1',
    source_ready: true,
    pure_builder: true,
    source_tuple_conserved: true,
    agent_head_loaded_from_original_recipe: sources.agent.actual.head,
    agent_head_matches_original_recipe_pin: sources.agent.actual.head === original.pins.agent.head,
    original_command_row_conserved: true,
    new_namespace: { suites: expectedSuites, rows_sha256: expectedPacket.row_sha256, registration: false },
    paths_absent: true,
    body_ids_absent: true,
    builder: { path: builderPath, sha256: builderSha, blob: actualBuilderBlob },
  }, null, 2)}\n`);
}

if (mode === 'verify') assert(packet, 'packet JSON is required in verify mode');

console.log(JSON.stringify({
  status: 'PASS',
  selector: original.selector,
  attempt_scope: candidate.attempt_scope,
  source_controls: sources,
  builder: { path: builderPath, sha256: builderSha, blob: actualBuilderBlob, bytes: builderBytes.length },
  original_command_sha256: original.command_sha256,
  original_row_sha256: original.row_sha256,
  new_command_sha256: candidate.command_sha256,
  new_row_sha256: candidate.row_sha256,
  registration: false,
  native_ids: false,
  future_paths_absent: true,
}, null, 2));
