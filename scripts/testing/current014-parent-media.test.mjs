import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {
  PARENT_MEDIA_CONSTRUCTION, PARENT_MEDIA_DELIVERY, PARENT_MEDIA_DRIVER,
  PARENT_MEDIA_ROW_TESTS, PARENT_MEDIA_RUNTIME, readParentMediaInputs,
} from './current014-parent-media.mjs';

const scratch = mkdtempSync(path.join(os.tmpdir(), 'current014-parent-media-'));
test.after(() => rmSync(scratch, { recursive: true, force: true }));
const roots = Object.fromEntries(['app', 'agent', 'runtime', 'producer', 'modules', 'browsers', 'short', 'child'].map((name) => {
  const root = path.join(scratch, name);
  mkdirSync(root);
  return [name, root];
}));
const executable = path.join(scratch, 'node');
writeFileSync(executable, 'node');
const env = {
  TIMELINE_PARENT_MEDIA_APP_TREE: 'a'.repeat(40),
  TIMELINE_PARENT_MEDIA_DELIVERY_SHA: PARENT_MEDIA_DELIVERY.commit,
  TIMELINE_PARENT_MEDIA_CONSTRUCTION_SHA: PARENT_MEDIA_CONSTRUCTION.commit,
  TIMELINE_PARENT_MEDIA_DRIVER_SHA: PARENT_MEDIA_DRIVER.commit,
  ASTRID_CHECKOUT: roots.agent,
  ASTRID_RUNTIME_CHECKOUT: roots.runtime,
  TIMELINE_PARENT_MEDIA_RUNTIME_PRODUCER_CHECKOUT: roots.producer,
  ASTRID_PYTHON: process.execPath,
  ASTRID_RUNTIME_PYTHON: process.execPath,
  PRIVATE13_NODE_MODULES: roots.modules,
  PLAYWRIGHT_CHROMIUM_EXECUTABLE: process.execPath,
  PLAYWRIGHT_BROWSERS_PATH: roots.browsers,
  TIMELINE_PARENT_MEDIA_NODE: process.execPath,
  TIMELINE_PARENT_MEDIA_VITE_BIN: executable,
  TIMELINE_PARENT_MEDIA_PLAYWRIGHT_CLI: executable,
  TIMELINE_PARENT_MEDIA_SHORT_TMPDIR: roots.short,
  TIMELINE_PARENT_MEDIA_CHILD_TMPDIR: roots.child,
};

test('binds the exact approved delivery, construction, driver and private014 cohort', () => {
  const input = readParentMediaInputs(env, roots.app);
  assert.equal(input.appTree, env.TIMELINE_PARENT_MEDIA_APP_TREE);
  assert.equal(input.agent, roots.agent);
  assert.equal(PARENT_MEDIA_RUNTIME.artifactCount, 75);
  assert.equal(PARENT_MEDIA_ROW_TESTS.includes('tests/e2e/local/three-products.spec.ts'), true);
});

test('requires exact source SHAs and never accepts a moving source default', () => {
  for (const name of ['TIMELINE_PARENT_MEDIA_APP_TREE', 'TIMELINE_PARENT_MEDIA_DELIVERY_SHA',
    'TIMELINE_PARENT_MEDIA_CONSTRUCTION_SHA', 'TIMELINE_PARENT_MEDIA_DRIVER_SHA']) {
    const values = { ...env };
    delete values[name];
    assert.throws(() => readParentMediaInputs(values, roots.app), new RegExp(`${name} is required`));
  }
  assert.throws(() => readParentMediaInputs({ ...env, TIMELINE_PARENT_MEDIA_DELIVERY_SHA: 'a'.repeat(40) }, roots.app), /delivery source/);
  assert.throws(() => readParentMediaInputs({ ...env, TIMELINE_PARENT_MEDIA_CONSTRUCTION_SHA: 'b'.repeat(40) }, roots.app), /HOME construction source/);
});

test('keeps private node graph and short-child paths separate from shared state', () => {
  assert.notEqual(readParentMediaInputs(env, roots.app).privateNodeModules, '/home/user/work/app/node_modules');
  assert.notEqual(readParentMediaInputs(env, roots.app).shortTmpDir, readParentMediaInputs(env, roots.app).childTmpDir);
  assert.throws(() => readParentMediaInputs({ ...env, PRIVATE13_NODE_MODULES: '/home/user/work/app/node_modules' }, roots.app), /shared App install/);
});
