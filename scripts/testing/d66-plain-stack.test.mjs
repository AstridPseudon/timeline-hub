import assert from 'node:assert/strict';
import test from 'node:test';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { exactCheckoutPath, receiptCheckout, selectPinnedSources, serviceRecipe, validatePinnedSource, validatePinnedSources, validateSelectedSource } from './d66-plain-stack.mjs';

const state = (overrides = {}) => ({
  root: '/snapshot/agent', head: 'a'.repeat(40), tree: 'b'.repeat(40), branch: null, dirty: false, ...overrides,
});

test('D66 accepts a detached clean checkout matching the normal head and tree', () => {
  assert.deepEqual(validateSelectedSource({
    role: 'agent', selected: '/snapshot/agent', normal: '/home/user/work/agent',
    normalState: state(), selectedState: state(),
  }), {
    checkout: '/snapshot/agent', head: 'a'.repeat(40), tree: 'b'.repeat(40),
    normal_home: '/home/user/work/agent', normal_head: 'a'.repeat(40), normal_tree: 'b'.repeat(40),
  });
});

test('D66 refuses a source that is the mutable normal home', () => {
  assert.throws(() => validateSelectedSource({
    role: 'runtime', selected: '/home/user/work/runtime', normal: '/home/user/work/runtime',
    normalState: state(), selectedState: state({ root: '/home/user/work/runtime' }),
  }), /per-request checkout/);
});

test('D66 refuses a selected source after the normal home advances', () => {
  assert.throws(() => validateSelectedSource({
    role: 'agent', selected: '/snapshot/agent', normal: '/home/user/work/agent',
    normalState: state({ head: 'c'.repeat(40), tree: 'd'.repeat(40) }), selectedState: state(),
  }), /not the current normal head/);
});

test('D66 refuses attached or dirty source checkouts', () => {
  assert.throws(() => validateSelectedSource({
    role: 'agent', selected: '/snapshot/agent', normal: '/home/user/work/agent',
    normalState: state(), selectedState: state({ branch: 'tl/integration' }),
  }), /must be detached/);
  assert.throws(() => validateSelectedSource({
    role: 'runtime', selected: '/snapshot/runtime', normal: '/home/user/work/runtime',
    normalState: state(), selectedState: state({ root: '/snapshot/runtime', dirty: true }),
  }), /dirty/);
});

test('D66 derives the supported detached route from the captured normal head', () => {
  assert.equal(exactCheckoutPath('app', 'c'.repeat(40)), '/home/user/work/wt/app-pin-cccccccc');
  assert.equal(exactCheckoutPath('agent', 'a'.repeat(40)), '/home/user/work/wt/agt-pin-aaaaaaaa');
  assert.equal(exactCheckoutPath('runtime', 'b'.repeat(40), '/tmp/checkouts'), '/tmp/checkouts/rt-pin-bbbbbbbb');
  assert.equal(exactCheckoutPath('composition', 'd'.repeat(40)), '/home/user/work/wt/vw-pin-dddddddd');
});

const pinned = (role, head, tree) => ({
  checkout: `/snapshot/${role}`, normal_home: `/home/user/work/${role}`,
  head, tree, state: state({ root: `/snapshot/${role}`, head, tree }),
});

test('D73 accepts one immutable four-repository tuple and does not consult moving normal heads', () => {
  const sources = {
    app: pinned('app', 'a'.repeat(40), '1'.repeat(40)),
    agent: pinned('agent', 'b'.repeat(40), '2'.repeat(40)),
    runtime: pinned('runtime', 'c'.repeat(40), '3'.repeat(40)),
    composition: pinned('composition', 'd'.repeat(40), '4'.repeat(40)),
  };
  assert.deepEqual(validatePinnedSources({ sources, appRootState: state({ tree: sources.app.tree }) }), sources);
  assert.throws(() => validatePinnedSources({ sources, appRootState: state({ head: 'f'.repeat(40), tree: sources.app.tree }) }), /App service source/);
  // A normal-home movement after this validation is irrelevant: launch uses the tuple above.
  assert.deepEqual(validatePinnedSource({ role: 'agent', selected: sources.agent.checkout,
    normal: sources.agent.normal_home, expectedHead: sources.agent.head, expectedTree: sources.agent.tree,
    selectedState: sources.agent.state }), {
    checkout: sources.agent.checkout, head: sources.agent.head, tree: sources.agent.tree, normal_home: sources.agent.normal_home,
  });
});

test('D73 refuses stale, missing, tampered, or wrong selected pins before any gesture can run', () => {
  const source = pinned('composition', 'd'.repeat(40), '4'.repeat(40));
  assert.throws(() => validatePinnedSource({ role: 'composition', selected: source.checkout,
    normal: source.normal_home, expectedHead: 'e'.repeat(40), expectedTree: source.tree, selectedState: source.state }), /does not match/);
  assert.throws(() => validatePinnedSource({ role: 'composition', selected: source.checkout,
    normal: source.normal_home, expectedHead: source.head, expectedTree: '5'.repeat(40), selectedState: source.state }), /does not match/);
  assert.throws(() => validatePinnedSource({ role: 'composition', selected: source.normal_home,
    normal: source.normal_home, expectedHead: source.head, expectedTree: source.tree, selectedState: source.state }), /per-request checkout/);
  assert.throws(() => validatePinnedSources({ sources: { app: source } }), /agent exact source is required/);
});

test('D73 service recipe carries full SHA/tree and all four exact checkout paths', () => {
  const pins = {
    app: { head: 'a'.repeat(40), tree: '1'.repeat(40) }, agent: { head: 'b'.repeat(40), tree: '2'.repeat(40) },
    runtime: { head: 'c'.repeat(40), tree: '3'.repeat(40) }, composition: { head: 'd'.repeat(40), tree: '4'.repeat(40) },
  };
  const recipe = serviceRecipe({ name: 'p3', target: 'app-P-D73', pins, checkouts: {
    app: '/snapshot/app', agent: '/snapshot/agent', runtime: '/snapshot/runtime', composition: '/snapshot/composition',
  } });
  for (const role of ['APP', 'AGENT', 'RUNTIME', 'COMPOSITION']) {
    assert.match(recipe, new RegExp(`D66_${role}_SHA='[a-f0-9]{40}'`));
    assert.match(recipe, new RegExp(`D66_${role}_TREE='[a-f0-9]{40}'`));
    assert.match(recipe, new RegExp(`D66_${role}_CHECKOUT='[^']+'`));
  }
  assert.doesNotMatch(recipe, /current normal|gesture|POST|publish/);
});

function runGit(directory, ...args) {
  return execFileSync('git', ['-C', directory, ...args], { encoding: 'utf8' }).trim();
}

function fixtureRepo(directory, name) {
  mkdirSync(directory, { recursive: true });
  runGit(directory, 'init', '-q');
  runGit(directory, 'config', 'user.email', 'd73@example.test');
  runGit(directory, 'config', 'user.name', 'D73 fixture');
  writeFileSync(path.join(directory, `${name}.txt`), `${name}\n`);
  runGit(directory, 'add', '.');
  runGit(directory, 'commit', '-qm', 'fixture');
  return { head: runGit(directory, 'rev-parse', 'HEAD'), tree: runGit(directory, 'rev-parse', 'HEAD^{tree}') };
}

function detachedFixture(normal, checkout) {
  execFileSync('git', ['clone', '-q', normal, checkout]);
  runGit(checkout, 'checkout', '--detach', '-q', 'HEAD');
}

test('D73 dry-preflight selects env paths and parses genuine checkout receipts before launch', () => {
  const base = mkdtempSync(path.join(os.tmpdir(), 'd73-preflight-'));
  const homes = Object.fromEntries(['app', 'agent', 'runtime', 'composition'].map((role) => [role, path.join(base, `${role}-normal`)]));
  const checkouts = Object.fromEntries(Object.keys(homes).map((role) => [role, path.join(base, `${role}-checkout`)]));
  const pins = Object.fromEntries(Object.entries(homes).map(([role, home]) => [role, fixtureRepo(home, role)]));
  for (const role of Object.keys(homes)) detachedFixture(homes[role], checkouts[role]);
  const env = Object.fromEntries(Object.keys(homes).flatMap((role) => [
    [`D66_${role.toUpperCase()}_SHA`, pins[role].head], [`D66_${role.toUpperCase()}_TREE`, pins[role].tree],
    [`D66_${role.toUpperCase()}_CHECKOUT`, `  ${checkouts[role]}  `],
  ]));
  const selected = selectPinnedSources(env, homes, checkouts.app);
  assert.deepEqual(Object.fromEntries(Object.entries(selected).map(([role, source]) => [role, source.checkout])), checkouts);
  writeFileSync(path.join(base, 'created-receipt'), `created ${checkouts.agent} (detached at ${pins.agent.head}, KEEP)\n`);
  writeFileSync(path.join(base, 'exists-receipt'), `exists: ${checkouts.runtime} at ${pins.runtime.head}\n`);
  assert.equal(receiptCheckout(path.join(base, 'created-receipt'), 'agent', pins.agent.head), checkouts.agent);
  assert.equal(receiptCheckout(path.join(base, 'exists-receipt'), 'runtime', pins.runtime.head), checkouts.runtime);
  assert.throws(() => selectPinnedSources({ ...env, D66_AGENT_CHECKOUT: checkouts.runtime }, homes, checkouts.app), /does not match/);
  const missingPinEnv = { ...env };
  delete missingPinEnv.D66_RUNTIME_TREE;
  assert.throws(() => selectPinnedSources(missingPinEnv, homes, checkouts.app), /runtime tree must be a full 40-character SHA/);
});
