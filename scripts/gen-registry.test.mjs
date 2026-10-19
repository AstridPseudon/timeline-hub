import assert from 'node:assert/strict';
import {mkdirSync, readFileSync, rmSync, writeFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {test} from 'node:test';

const packageRoot = fileURLToPath(new URL('..', import.meta.url));
const registryPath = join(packageRoot, 'typescript', 'src', 'registry.generated.ts');

test('registry discovery includes a temporary installed theme descriptor', () => {
  const themeName = `timeline-theme-m0-generator-${process.pid}`;
  const themeDir = join(packageRoot, 'node_modules', '@banodoco', themeName);
  const effectDir = join(themeDir, 'src', 'effects', 'temporary-card');
  const original = readFileSync(registryPath, 'utf8');

  mkdirSync(effectDir, {recursive: true});
  writeFileSync(join(themeDir, 'package.json'), JSON.stringify({name: `@banodoco/${themeName}`}));
  writeFileSync(join(themeDir, 'theme.json'), JSON.stringify({id: 'm0-generator'}));
  writeFileSync(join(effectDir, 'component.tsx'), 'export default function TemporaryCard() { return null; }\n');

  try {
    const result = spawnSync(process.execPath, ['--import', 'tsx', 'scripts/gen-registry.ts'], {
      cwd: packageRoot,
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, result.stderr);
    const generated = readFileSync(registryPath, 'utf8');
    assert.match(generated, /temporary-card/);
    assert.match(generated, new RegExp(`@banodoco/${themeName}/src/effects/temporary-card/component`));
  } finally {
    rmSync(themeDir, {recursive: true, force: true});
    writeFileSync(registryPath, original);
  }

  const check = spawnSync(process.execPath, ['--import', 'tsx', 'scripts/gen-registry.ts', '--check'], {
    cwd: packageRoot,
    encoding: 'utf8',
  });
  assert.equal(check.status, 0, check.stderr);
  assert.equal(readFileSync(registryPath, 'utf8'), original);
});
