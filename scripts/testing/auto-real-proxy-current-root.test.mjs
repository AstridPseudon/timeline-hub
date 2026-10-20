import assert from 'node:assert/strict';
import { chmodSync, lstatSync, mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { after, test } from 'node:test';
import { REAL_PROXY_RUNTIME, prepareNodeModulesOverlay, readRealProxyInputs } from './auto-real-proxy-current-root.mjs';

const scratch = mkdtempSync(path.join(os.tmpdir(), 'auto-real-proxy-current-root-'));
after(() => rmSync(scratch, { recursive: true, force: true }));
const roots = Object.fromEntries(['app', 'agent', 'runtime', 'producer', 'deps', 'private'].map((name) => [name, path.join(scratch, name)]));
for (const root of Object.values(roots)) mkdirSync(root, { recursive: true });
const browser = path.join(scratch, 'chrome');
writeFileSync(browser, '#!/bin/sh\nprintf Chromium\n');
chmodSync(browser, 0o755);

function values() {
  return {
    TIMELINE_AUTO_REAL_PROXY_APP_SHA: 'a'.repeat(40),
    TIMELINE_AUTO_REAL_PROXY_APP_TREE: 'b'.repeat(40),
    TIMELINE_AUTO_REAL_PROXY_AGENT_SHA: 'c'.repeat(40),
    TIMELINE_AUTO_REAL_PROXY_AGENT_TREE: 'd'.repeat(40),
    TIMELINE_AUTO_REAL_PROXY_RUNTIME_SHA: REAL_PROXY_RUNTIME.commit,
    TIMELINE_AUTO_REAL_PROXY_RUNTIME_TREE: REAL_PROXY_RUNTIME.tree,
    TIMELINE_AUTO_REAL_PROXY_RUNNER_SHA256: 'sha256:' + 'e'.repeat(64),
    ASTRID_CHECKOUT: roots.agent,
    ASTRID_RUNTIME_CHECKOUT: roots.runtime,
    TIMELINE_AUTO_REAL_PROXY_RUNTIME_PRODUCER_CHECKOUT: roots.producer,
    TIMELINE_AUTO_REAL_PROXY_DEPENDENCY_ROOT: roots.deps,
    TIMELINE_AUTO_REAL_PROXY_PRIVATE_ROOT: roots.private,
    ASTRID_PYTHON: process.execPath,
    ASTRID_RUNTIME_PYTHON: process.execPath,
    PLAYWRIGHT_CHROMIUM_EXECUTABLE: browser,
  };
}

test('requires every literal source, runner, dependency, and browser input', () => {
  for (const name of Object.keys(values())) {
    const input = values();
    delete input[name];
    assert.throws(() => readRealProxyInputs(input, roots.app), new RegExp(`${name} is required`));
  }
});

test('pins Runtime 2c4 and rejects stale public/direct overrides', () => {
  assert.throws(() => readRealProxyInputs({ ...values(), TIMELINE_AUTO_REAL_PROXY_RUNTIME_SHA: 'f'.repeat(40) }, roots.app), /published 2c4/);
  assert.throws(() => readRealProxyInputs({ ...values(), ASTRID_PUBLIC_CHECKOUT: roots.agent }, roots.app), /overrides are forbidden/);
  assert.throws(() => readRealProxyInputs({ ...values(), ASTRID_APP_DIRECT_DIST: path.join(scratch, 'dist') }, roots.app), /overrides are forbidden/);
});

test('overlay copies Vite and Rollup resolvers while linking the rest read-only', () => {
  const source = path.join(scratch, 'overlay-deps');
  const app = path.join(scratch, 'overlay-app');
  const privateRoot = path.join(scratch, 'overlay-private');
  mkdirSync(path.join(source, 'vite'), { recursive: true });
  mkdirSync(path.join(source, 'rollup'), { recursive: true });
  mkdirSync(path.join(source, '@rollup', 'plugin'), { recursive: true });
  writeFileSync(path.join(source, 'vite', 'package.json'), '{}');
  writeFileSync(path.join(source, 'rollup', 'package.json'), '{}');
  writeFileSync(path.join(source, '@rollup', 'plugin', 'package.json'), '{}');
  mkdirSync(app, { recursive: true });
  mkdirSync(privateRoot, { recursive: true });
  const shared = path.join(scratch, 'shared-node-modules');
  mkdirSync(shared, { recursive: true });
  symlinkSync(shared, path.join(app, 'node_modules'), 'junction');
  const restore = prepareNodeModulesOverlay(app, source, privateRoot);
  try {
    assert.equal(lstatSync(path.join(app, 'node_modules/vite')).isSymbolicLink(), false);
    assert.equal(lstatSync(path.join(app, 'node_modules/rollup')).isSymbolicLink(), false);
    assert.equal(lstatSync(path.join(app, 'node_modules/@rollup/plugin')).isSymbolicLink(), true);
    assert.equal(lstatSync(path.join(app, 'node_modules/.vite')).isSymbolicLink(), false);
  } finally { restore(); }
});
