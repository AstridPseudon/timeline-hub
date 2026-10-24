import assert from 'node:assert/strict';
import test from 'node:test';
import { exactCheckoutPath, validateSelectedSource } from './d66-plain-stack.mjs';

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
  assert.equal(exactCheckoutPath('agent', 'a'.repeat(40)), '/home/user/work/wt/agt-pin-aaaaaaaa');
  assert.equal(exactCheckoutPath('runtime', 'b'.repeat(40), '/tmp/checkouts'), '/tmp/checkouts/rt-pin-bbbbbbbb');
});
