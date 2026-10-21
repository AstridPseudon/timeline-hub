#!/usr/bin/env node
import assert from 'node:assert/strict';
import {existsSync, readFileSync, realpathSync, rmSync} from 'node:fs';
import {dirname, join, relative, resolve} from 'node:path';

const [taskRoot, ...cases] = process.argv.slice(2);
assert(taskRoot && cases.length > 0 && cases.length % 3 === 0,
  'usage: fixture.mjs TASK_ROOT LABEL OLD1134_ROOT NESTED_ROOT [...]');
const actualTaskRoot = realpathSync(taskRoot);
assert.equal(actualTaskRoot, taskRoot, 'fixture root must be an existing real directory');
console.log(`using task-owned fixture root: ${taskRoot}`);

function importPath(source, fromFile, suffix) {
  const match = source.match(new RegExp(`from ['"]([^'"]+/${suffix})['"]`));
  assert(match, `${fromFile}: missing ${suffix} import`);
  return resolve(dirname(fromFile), `${match[1]}.tsx`);
}

function sourceClosure(layoutRoot, sourceLabel) {
  const remotionRoot = existsSync(join(layoutRoot, 'remotion')) ? join(layoutRoot, 'remotion') : layoutRoot;
  const liveSceneClip = resolve(remotionRoot, 'src', 'LiveSceneClip.tsx');
  const liveSource = readFileSync(liveSceneClip, 'utf8');
  const sceneSurface = importPath(liveSource, liveSceneClip, 'SceneSurface');
  const sceneSource = readFileSync(sceneSurface, 'utf8');
  const runtime = resolve(dirname(sceneSurface), './runtime.ts');
  const diagnostics = resolve(dirname(sceneSurface), './diagnostics.ts');
  assert(existsSync(sceneSurface), `${sourceLabel}: SceneSurface unresolved: ${sceneSurface}`);
  assert(existsSync(runtime), `${sourceLabel}: runtime unresolved: ${runtime}`);
  assert(existsSync(diagnostics), `${sourceLabel}: diagnostics unresolved: ${diagnostics}`);
  assert(sceneSource.includes("from './runtime'"), `${sourceLabel}: SceneSurface runtime edge missing`);
  assert(sceneSource.includes("from './diagnostics'"), `${sourceLabel}: SceneSurface diagnostics edge missing`);
  return {
    liveSceneClip,
    sceneSurface,
    runtime,
    diagnostics,
    relativePaths: [liveSceneClip, sceneSurface, runtime, diagnostics].map(path => relative(layoutRoot, path)),
  };
}

function expectFailure(layoutRoot, sourceLabel) {
  const remotionRoot = existsSync(join(layoutRoot, 'remotion')) ? join(layoutRoot, 'remotion') : layoutRoot;
  const liveSceneClip = resolve(remotionRoot, 'src', 'LiveSceneClip.tsx');
  const liveSource = readFileSync(liveSceneClip, 'utf8');
  const sceneSurface = importPath(liveSource, liveSceneClip, 'SceneSurface');
  assert(!existsSync(sceneSurface), `${sourceLabel}: old1134 unexpectedly resolved ${sceneSurface}`);
  console.log(`${sourceLabel} old1134: FAIL as expected (${sceneSurface})`);
}

try {
  for (let index = 0; index < cases.length; index += 3) {
    const [sourceLabel, oldLayout, nestedLayout] = cases.slice(index, index + 3);
    expectFailure(oldLayout, sourceLabel);
    const closure = sourceClosure(nestedLayout, sourceLabel);
    console.log(`${sourceLabel} corrected nested: PASS ${JSON.stringify(closure.relativePaths)}`);
  }
} finally {
  const cleanupRoot = realpathSync(taskRoot);
  assert.equal(cleanupRoot, actualTaskRoot, 'refusing cleanup: fixture root realpath changed');
  assert.equal(relative(realpathSync('/tmp'), cleanupRoot).startsWith('..'), false, 'refusing cleanup: fixture escaped tmpdir');
  rmSync(cleanupRoot, {recursive: true, force: true});
  console.log(`removed exact task-owned fixture root: ${cleanupRoot}`);
}
