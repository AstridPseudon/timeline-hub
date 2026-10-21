import assert from 'node:assert/strict';
import {cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import {tmpdir} from 'node:os';
import {dirname, join, relative, resolve} from 'node:path';
import {test} from 'node:test';
import {buildRemotionPrimitives, primitivesPath} from './build-remotion-primitives.mjs';

test('calculation projection rebuilds from exported pinned dependency leaves and refuses stale output', async () => {
  const root = mkdtempSync(join(tmpdir(), 'composition-primitives-'));
  const packagePath = createRequire(import.meta.url).resolve('remotion/package.json');
  const installed = dirname(packagePath);
  const dependency = join(root, 'node_modules/remotion');
  const output = join(root, primitivesPath);
  try {
    writeFileSync(join(root, 'package.json'), '{"type":"module"}');
    const linked = join(root, 'linked');
    mkdirSync(join(linked, 'node_modules'), {recursive: true});
    writeFileSync(join(linked, 'package.json'), '{}');
    symlinkSync(installed, join(linked, 'node_modules/remotion'), 'dir');
    const metadata = await buildRemotionPrimitives(linked);
    const linkedOutput = join(linked, primitivesPath);
    const original = readFileSync(linkedOutput, 'utf8');
    assert.deepEqual(Object.values(metadata.outputs).flatMap(entry => entry.imports), []);
    const leaves = Object.keys(metadata.inputs).filter(path => path.endsWith('.js'));
    assert.equal(leaves.length, 10);
    assert.ok(leaves.every(path => resolve(path).startsWith(join(installed, 'dist/cjs/'))));
    writeFileSync(linkedOutput, 'throw new Error("stale projection");');
    await buildRemotionPrimitives(linked);
    assert.equal(readFileSync(linkedOutput, 'utf8'), original);

    // From here on mutate only a private real package, never the installed leaf.
    mkdirSync(dependency, {recursive: true});
    cpSync(packagePath, join(dependency, 'package.json'));
    for (const path of leaves) {
      const target = join(dependency, relative(installed, resolve(path)));
      mkdirSync(dirname(target), {recursive: true});
      cpSync(resolve(path), target);
    }
    await buildRemotionPrimitives(root);
    const jsonPath = join(dependency, 'package.json');
    const json = JSON.parse(readFileSync(jsonPath, 'utf8'));
    writeFileSync(jsonPath, JSON.stringify({...json, version: '4.0.508'}));
    await assert.rejects(buildRemotionPrimitives(root), /Expected Remotion 4.0.509/);
    assert.equal(existsSync(output), false);
    writeFileSync(jsonPath, JSON.stringify(json));
    await buildRemotionPrimitives(root);
    rmSync(join(dependency, 'dist/cjs/spring/spring-utils.js'));
    await assert.rejects(buildRemotionPrimitives(root), /Build failed/);
    assert.equal(existsSync(output), false);
    const hidden = join(root, 'hidden');
    mkdirSync(join(hidden, 'node_modules/remotion'), {recursive: true});
    writeFileSync(join(hidden, 'package.json'), '{}');
    writeFileSync(join(hidden, 'node_modules/remotion/package.json'), JSON.stringify({...json, exports: {}}));
    mkdirSync(dirname(join(hidden, primitivesPath)), {recursive: true});
    writeFileSync(join(hidden, primitivesPath), original);
    await assert.rejects(buildRemotionPrimitives(hidden), /not defined by "exports"/);
    assert.equal(existsSync(join(hidden, primitivesPath)), false);
  } finally {
    rmSync(root, {recursive: true, force: true});
  }
});
