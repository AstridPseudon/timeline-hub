import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { after, test } from 'node:test';
import { assertPinnedImportedModule } from './main95-prompt-settings-integration.mjs';

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
