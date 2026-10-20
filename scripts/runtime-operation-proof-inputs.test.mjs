import assert from 'node:assert/strict';
import { test } from 'node:test';
import { parseProofInputs, RUNTIME_HEAD } from './runtime-operation-proof-inputs.mjs';

const inputs = {
  agentCheckout: '/retained/agent', agentPython: '/venv/agent/bin/python', agentHead: 'a'.repeat(40),
  runtimeCheckout: '/retained/runtime', runtimePython: '/venv/runtime/bin/python', runtimeHead: RUNTIME_HEAD,
  appTree: 'b'.repeat(40), dependencyRoot: '/private12/node_modules', cacheRoot: '/worker/cache',
};

test('proof inputs require the exact published pair, source tree and private cache explicitly', () => {
  assert.deepEqual(parseProofInputs(inputs), inputs);
  for (const field of Object.keys(inputs)) {
    const missing = { ...inputs }; delete missing[field];
    assert.throws(() => parseProofInputs(missing), undefined, field);
  }
  assert.throws(() => parseProofInputs({ ...inputs, runtimeHead: 'c'.repeat(40) }));
  assert.throws(() => parseProofInputs({ ...inputs, agentHead: 'pending' }));
  assert.throws(() => parseProofInputs({ ...inputs, dependencyRoot: 'node_modules' }));
});
