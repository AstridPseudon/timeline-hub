import assert from 'node:assert/strict';
import {cpSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {spawnSync} from 'node:child_process';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {test} from 'node:test';

const sourceRoot = fileURLToPath(new URL('..', import.meta.url));

test('package generation ignores installed host themes and checks all local registries', () => {
  const packageRoot = mkdtempSync(join(tmpdir(), 'composition-registry-'));
  for (const path of ['scripts', 'typescript/src', 'package.json']) {
    cpSync(join(sourceRoot, path), join(packageRoot, path), {recursive: true});
  }
  const generated = ['registry', 'effects', 'animations', 'animation-metadata', 'transitions']
    .map(name => join(packageRoot, 'typescript', 'src', `${name}.generated.ts`));
  const themeDir = join(packageRoot, 'node_modules', '@banodoco', `timeline-theme-test-${process.pid}`);
  const originals = generated.map(path => readFileSync(path, 'utf8'));
  mkdirSync(join(themeDir, 'src', 'effects', 'host-only'), {recursive: true});
  writeFileSync(join(themeDir, 'package.json'), JSON.stringify({name: '@banodoco/timeline-theme-test'}));
  writeFileSync(join(themeDir, 'theme.json'), JSON.stringify({id: 'test'}));
  writeFileSync(join(themeDir, 'src', 'effects', 'host-only', 'component.tsx'), 'export default () => null;');
  const run = (...args) => spawnSync(process.execPath, ['--import', import.meta.resolve('tsx'), 'scripts/gen-registry.ts', ...args], {
    cwd: packageRoot, encoding: 'utf8',
  });
  try {
    const result = run();
    assert.equal(result.status, 0, result.stderr);
    generated.forEach((path, index) => assert.equal(readFileSync(path, 'utf8'), originals[index]));
    const pureMetadata = readFileSync(generated[3], 'utf8');
    assert.match(pureMetadata, /export const ANIMATION_DEFAULTS/);
    assert.match(pureMetadata, /export const ANIMATION_META/);
    assert.doesNotMatch(pureMetadata, /builtins\/animations\/.*\/component/);
    assert.doesNotMatch(pureMetadata, /from ['"].*(?:react|remotion)/);
    for (const path of generated) {
      writeFileSync(path, readFileSync(path, 'utf8') + '// drift\n');
      const stale = run('--check');
      assert.equal(stale.status, 1);
      assert.match(stale.stderr, /is stale/);
      writeFileSync(path, originals[generated.indexOf(path)]);
    }
    assert.equal(run('--check').status, 0);
  } finally {
    rmSync(packageRoot, {recursive: true, force: true});
  }
});
