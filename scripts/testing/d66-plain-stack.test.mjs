import assert from 'node:assert/strict';
import test from 'node:test';
import { exactCheckoutPath, serviceRecipe, validatePinnedSource, validatePinnedSources, validateSelectedSource } from './d66-plain-stack.mjs';

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
