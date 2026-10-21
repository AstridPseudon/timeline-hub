import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { after, test } from 'node:test';
import {
  CURRENT014_AGENT,
  CURRENT014_APP,
  CURRENT014_PUBLIC13,
  CURRENT014_ROW_TESTS,
  CURRENT014_RUNTIME,
  readCurrent014Inputs,
} from './current014-integration.mjs';

const scratch = mkdtempSync(path.join(os.tmpdir(), 'current014-wrapper-'));
after(() => rmSync(scratch, { recursive: true, force: true }));
const roots = Object.fromEntries(['app', 'agent', 'runtime', 'producer'].map((name) => {
  const root = path.join(scratch, name);
  mkdirSync(root);
  return [name, root];
}));

function env() {
  return {
    TIMELINE_CURRENT014_APP_TREE: 'a'.repeat(40),
    TIMELINE_CURRENT014_PIN_COMMIT: CURRENT014_APP.pinCommit,
    TIMELINE_CURRENT014_PIN_TREE: CURRENT014_APP.pinTree,
    TIMELINE_CURRENT014_AGENT_SHA: CURRENT014_AGENT.commit,
    TIMELINE_CURRENT014_RUNTIME_SHA: CURRENT014_RUNTIME.commit,
    ASTRID_CHECKOUT: roots.agent,
    ASTRID_RUNTIME_CHECKOUT: roots.runtime,
    TIMELINE_CURRENT014_RUNTIME_PRODUCER_CHECKOUT: roots.producer,
    ASTRID_NODE_EXECUTABLE: process.execPath,
    TIMELINE_CURRENT014_VITEST_RUNNER: new URL('./current014-integration.test.mjs', import.meta.url).pathname,
  };
}

test('binds the approved Main014 identities and keeps the current App tree explicit', () => {
  const input = readCurrent014Inputs(env(), roots.app);
  assert.equal(input.appTree, 'a'.repeat(40));
  assert.equal(input.agentSha, '6efc81500a0e0688c2bb41e736503f0fc3e04abb');
  assert.equal(input.runtimeSha, '95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c');
  assert.equal(CURRENT014_APP.pinCommit, '10fa2ff9a8216604aa39e3584f89dc9e7a09080a');
  assert.equal(CURRENT014_APP.pinTree, '01fd2a04ff0c383ec5281043c7e5a4c843d1d835');
  assert.equal(CURRENT014_PUBLIC13.files, 77);
});

test('requires every source path and full identity', () => {
  for (const name of Object.keys(env())) {
    const values = env();
    delete values[name];
    assert.throws(() => readCurrent014Inputs(values, roots.app), new RegExp(`${name} is required`));
  }
  for (const name of ['TIMELINE_CURRENT014_APP_TREE', 'TIMELINE_CURRENT014_AGENT_SHA', 'TIMELINE_CURRENT014_RUNTIME_SHA']) {
    assert.throws(() => readCurrent014Inputs({ ...env(), [name]: '2ed2' }, roots.app), /full 40-character/);
  }
});

test('refuses a mismatched cohort, pin selector, relative path, or direct dist', () => {
  assert.throws(() => readCurrent014Inputs({ ...env(), TIMELINE_CURRENT014_AGENT_SHA: 'b'.repeat(40) }, roots.app), /must be 6efc815/);
  assert.throws(() => readCurrent014Inputs({ ...env(), TIMELINE_CURRENT014_RUNTIME_SHA: 'b'.repeat(40) }, roots.app), /must be 95bd3c5f/);
  assert.throws(() => readCurrent014Inputs({ ...env(), TIMELINE_CURRENT014_PIN_COMMIT: 'b'.repeat(40) }, roots.app), /PIN_COMMIT must be 10fa2ff9/);
  assert.throws(() => readCurrent014Inputs({ ...env(), TIMELINE_CURRENT014_PIN_TREE: 'b'.repeat(40) }, roots.app), /PIN_TREE must be 01fd2a04/);
  assert.throws(() => readCurrent014Inputs({ ...env(), ASTRID_CHECKOUT: '.' }, roots.app), /absolute path/);
  assert.throws(() => readCurrent014Inputs({ ...env(), ASTRID_APP_DIRECT_DIST: '/stale/dist' }, roots.app), /DIRECT_DIST is forbidden/);
});

test('row lane preserves all existing ordinary, parent, and bootstrap assertion files', () => {
  assert.deepEqual(CURRENT014_ROW_TESTS, [
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
  assert.equal(CURRENT014_RUNTIME.rawSchema, 'sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d');
  assert.equal(CURRENT014_APP.generated['src/integrations/runtime/generated.ts'].startsWith('sha256:'), true);
});
