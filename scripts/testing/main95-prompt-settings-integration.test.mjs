import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtempSync, mkdirSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { after, test } from 'node:test';
import { assertOwnedReadyComposition, assertOwnedReadyGraphRoot, assertPinnedImportedModule } from './main95-prompt-settings-integration.mjs';

const scratch = mkdtempSync(path.join(os.tmpdir(), 'main95-module-guard-'));
after(() => rmSync(scratch, { recursive: true, force: true }));

const graph = path.join(scratch, 'node_modules');
const appRoot = path.join(scratch, 'app');
const packageRoot = path.join(graph, '@remotion/media');
const packageFile = path.join(packageRoot, 'package.json');
const moduleFile = path.join(packageRoot, 'dist/esm/index.mjs');
mkdirSync(path.dirname(moduleFile), { recursive: true });
mkdirSync(appRoot);
symlinkSync(graph, path.join(appRoot, 'node_modules'));
writeFileSync(packageFile, JSON.stringify({
  name: '@remotion/media',
  version: '4.0.509',
  type: 'module',
  exports: { '.': { import: './dist/esm/index.mjs' } },
}));
writeFileSync(moduleFile, 'export const fixture = true;\n');

function digest(file) {
  return `sha256:${createHash('sha256').update(readFileSync(file)).digest('hex')}`;
}

const expectedHash = digest(moduleFile);

const ownedGraph = '/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules';
const ownedReady = '/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/READY';
const validComposition = '- Composition input: `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77/77 regular archive members; every installed member was byte-identical.';

test('accepts the owned normal-lock READY record and derives its root from graph realpath', () => {
  assert.equal(assertOwnedReadyGraphRoot({ graph: ownedGraph, readyFile: ownedReady }), path.dirname(realpathSync(ownedGraph)));
});

test('refuses a READY record whose graph root is not the graph realpath', () => {
  const wrongGraph = path.join(scratch, 'wrong-node_modules');
  mkdirSync(wrongGraph);
  assert.throws(() => assertOwnedReadyGraphRoot({ graph: wrongGraph, readyFile: ownedReady }), /missing the owned graph root/);
});

test('accepts the exact Composition READY record including its member-count suffix', () => {
  assert.deepEqual(assertOwnedReadyComposition({ ready: `${validComposition}\n` }), {
    archive: 'vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz',
    sha256: 'sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738',
    regularMembers: 77,
    declaredMembers: 77,
  });
});

test('refuses a READY record with the wrong Composition version', () => {
  const ready = validComposition.replace('banodoco-timeline-composition-0.0.13.tgz', 'banodoco-timeline-composition-0.0.12.tgz');
  assert.throws(() => assertOwnedReadyComposition({ ready }), /names .* expected the approved Composition archive/);
});

test('refuses a READY record with the wrong Composition archive hash', () => {
  const ready = validComposition.replace('9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738', '0000000000000000000000000000000000000000000000000000000000000000');
  assert.throws(() => assertOwnedReadyComposition({ ready }), /has Composition hash/);
});

test('refuses a READY record with the wrong Composition member count', () => {
  const ready = validComposition.replace('77/77', '76/77');
  assert.throws(() => assertOwnedReadyComposition({ ready }), /certifies 76\/77 regular archive members/);
});

test('refuses a READY record missing the Composition member-count suffix', () => {
  const ready = validComposition.replace(', 77/77 regular archive members; every installed member was byte-identical.', '');
  assert.throws(() => assertOwnedReadyComposition({ ready }), /invalid Composition input record/);
});

test('accepts a valid pinned imported module and its exact bytes', async () => {
  const probeFile = path.join(appRoot, 'esm-probe.mjs');
  writeFileSync(probeFile, [
    "const url = import.meta.resolve('@remotion/media');",
    "const imported = await import('@remotion/media');",
    "if (imported.fixture !== true) throw new Error('unexpected ESM export');",
    'export default url;',
  ].join('\n'));
  const resolvedUrl = (await import(`${pathToFileURL(probeFile).href}?positive`)).default;
  assert.match(resolvedUrl, /@remotion\/media\/dist\/esm\/index\.mjs/);

  const checked = assertPinnedImportedModule({
    graph,
    packageName: '@remotion/media',
    packageFile,
    expectedVersion: '4.0.509',
    moduleFile,
    expectedHash,
  });
  assert.equal(checked.moduleFile, moduleFile);
  assert.equal(checked.moduleHash, expectedHash);
  assert.equal(checked.version, '4.0.509');
});

test('refuses a module resolved from the wrong package', () => {
  const wrongPackageFile = path.join(graph, 'remotion/package.json');
  mkdirSync(path.dirname(wrongPackageFile), { recursive: true });
  writeFileSync(wrongPackageFile, JSON.stringify({ name: 'remotion', version: '4.0.509' }));
  assert.throws(() => assertPinnedImportedModule({
    graph,
    packageName: '@remotion/media',
    packageFile: wrongPackageFile,
    expectedVersion: '4.0.509',
    moduleFile,
    expectedHash,
  }), /resolved to the wrong package/);
});

test('refuses a package version outside the pinned lock identity', () => {
  writeFileSync(packageFile, JSON.stringify({
    name: '@remotion/media',
    version: '4.0.508',
  }));
  assert.throws(() => assertPinnedImportedModule({
    graph,
    packageName: '@remotion/media',
    packageFile,
    expectedVersion: '4.0.509',
    moduleFile,
    expectedHash,
  }), /resolved version 4\.0\.508, expected 4\.0\.509/);
  writeFileSync(packageFile, JSON.stringify({
    name: '@remotion/media',
    version: '4.0.509',
    type: 'module',
    exports: { '.': { import: './dist/esm/index.mjs' } },
  }));
});

test('refuses changed imported-module bytes', () => {
  writeFileSync(moduleFile, 'export const fixture = false;\n');
  assert.throws(() => assertPinnedImportedModule({
    graph,
    packageName: '@remotion/media',
    packageFile,
    expectedVersion: '4.0.509',
    moduleFile,
    expectedHash,
  }), /module hash changed/);
  writeFileSync(moduleFile, 'export const fixture = true;\n');
});

test('refuses an imported-module source target outside the owned package', () => {
  const outsideModule = path.join(scratch, 'outside.mjs');
  writeFileSync(outsideModule, readFileSync(moduleFile));
  assert.throws(() => assertPinnedImportedModule({
    graph,
    packageName: '@remotion/media',
    packageFile,
    expectedVersion: '4.0.509',
    moduleFile: outsideModule,
    expectedHash,
  }), /source target escaped its package/);
});
