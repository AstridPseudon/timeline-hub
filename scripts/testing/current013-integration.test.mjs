import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readCurrent013Inputs, CURRENT013_RUNTIME } from './current013-integration.mjs';

function env() {
  return {
    TIMELINE_CURRENT013_APP_TREE: 'a'.repeat(40),
    TIMELINE_CURRENT013_AGENT_SHA: 'b'.repeat(40),
    TIMELINE_CURRENT013_RUNTIME_SHA: CURRENT013_RUNTIME.commit,
    ASTRID_CHECKOUT: '/home/user/peteromallet/astrid-agent',
    ASTRID_RUNTIME_CHECKOUT: '/home/user/banodoco/banodoco-workspace-runtime',
    TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT: '/home/user/banodoco/banodoco-workspace-runtime',
    ASTRID_PYTHON: '/usr/bin/python',
    ASTRID_RUNTIME_PYTHON: '/usr/bin/python',
  };
}

test('requires the exact App tree and does not infer a moving source path', () => {
  const values = env();
  delete values.TIMELINE_CURRENT013_APP_TREE;
  assert.throws(() => readCurrent013Inputs(values), /TIMELINE_CURRENT013_APP_TREE is required/);
});

test('accepts an App snapshot identity by tree and pins Runtime to the published SHA', () => {
  const input = readCurrent013Inputs(env());
  assert.equal(input.appTree, 'a'.repeat(40));
  assert.equal(input.runtimeSha, CURRENT013_RUNTIME.commit);
});

test('refuses a different Runtime publication before any child launch', () => {
  const values = env();
  values.TIMELINE_CURRENT013_RUNTIME_SHA = 'c'.repeat(40);
  assert.throws(() => readCurrent013Inputs(values), /must be the published Runtime/);
});

