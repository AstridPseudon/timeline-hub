import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { after, test } from 'node:test';
import { readReadyMarker, readInputs, RUNTIME } from './main574-public13-editing.mjs';

const root = mkdtempSync(path.join(os.tmpdir(), 'main574-public13-preflight-'));
after(() => rmSync(root, { recursive: true, force: true }));
const marker = path.join(root, 'READY');
const dirs = ['app', 'agent', 'runtime', 'producer'];
for (const name of dirs) mkdirSync(path.join(root, name));
const base = { ASTRID_CHECKOUT: path.join(root, 'agent'), ASTRID_RUNTIME_CHECKOUT: path.join(root, 'runtime'), TIMELINE_MAIN574_PUBLIC13_RUNTIME_PRODUCER_CHECKOUT: path.join(root, 'producer'), ASTRID_PYTHON: process.execPath, ASTRID_RUNTIME_PYTHON: process.execPath, TIMELINE_MAIN574_PUBLIC13_READY_MARKER: marker };

test('missing READY marker is a hard refusal', () => {
  assert.throws(() => readReadyMarker({ ...base, TIMELINE_MAIN574_PUBLIC13_READY_MARKER: path.join(root, 'missing') }), /READY marker is missing/);
});

test('READY requires every final literal head and tree', () => {
  writeFileSync(marker, 'AppSHA: ' + 'a'.repeat(40) + '\nAppTree: ' + 'b'.repeat(40) + '\n');
  assert.throws(() => readReadyMarker(base), /AgentSHA/);
  writeFileSync(marker, ['AppSHA', 'AppTree', 'AgentSHA', 'AgentTree', 'RuntimeSHA', 'RuntimeTree'].map((name, i) => `${name}: ${String.fromCharCode(97 + i).repeat(40)}`).join('\n'));
  assert.deepEqual(readReadyMarker(base), { AppSHA: 'a'.repeat(40), AppTree: 'b'.repeat(40), AgentSHA: 'c'.repeat(40), AgentTree: 'd'.repeat(40), RuntimeSHA: 'e'.repeat(40), RuntimeTree: 'f'.repeat(40) });
});

test('inputs require exact source paths and reject direct/public overrides', () => {
  assert.doesNotThrow(() => readInputs(base));
  assert.equal(RUNTIME.version, '0.2.13');
  assert.throws(() => readInputs({ ...base, ASTRID_PUBLIC_CHECKOUT: '/tmp/public' }), /overrides/);
  assert.throws(() => readInputs({ ...base, ASTRID_APP_DIRECT_DIST: '/tmp/dist' }), /overrides/);
});
