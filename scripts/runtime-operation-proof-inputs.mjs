import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync, realpathSync } from 'node:fs';
import { isAbsolute, join, relative, sep } from 'node:path';

export const RUNTIME_HEAD = '2c4ac180c2220bdad966bc01e95ad230e99ce26a';
const ARTIFACT = 'sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56';
const json = file => JSON.parse(readFileSync(file, 'utf8'));
const git = (root, ...args) => execFileSync('git', ['-C', root, ...args], { encoding: 'utf8' }).trim();
const inside = (root, path) => { const suffix = relative(root, path); return suffix === '' || (!suffix.startsWith(`..${sep}`) && suffix !== '..' && !isAbsolute(suffix)); };

// The service must name these inputs in its command; request-test does not forward caller env.
export function parseProofInputs(value) {
  assert(value && typeof value === 'object' && !Array.isArray(value), 'proof inputs must be an object');
  for (const field of ['agentCheckout', 'agentPython', 'runtimeCheckout', 'runtimePython', 'dependencyRoot', 'cacheRoot']) {
    assert(typeof value[field] === 'string' && isAbsolute(value[field]), `${field} must be an explicit absolute path`);
  }
  for (const field of ['agentHead', 'appTree']) assert.match(value[field] ?? '', /^[0-9a-f]{40}$/, `${field} must be an exact SHA`);
  assert.equal(value.runtimeHead, RUNTIME_HEAD, 'only the published Runtime 0.2.13 producer is supported');
  return { ...value };
}

export function assertProofSources(inputs, appRoot) {
  for (const [root, revision, selector] of [
    [appRoot, inputs.appTree, 'HEAD^{tree}'],
    [inputs.agentCheckout, inputs.agentHead, 'HEAD'],
    [inputs.runtimeCheckout, inputs.runtimeHead, 'HEAD'],
  ]) {
    assert.equal(git(root, 'rev-parse', selector), revision, 'source identity moved');
    assert.equal(git(root, 'status', '--porcelain', '--untracked-files=all'), '', 'source must be a clean service snapshot or retained checkout');
  }
  for (const root of [appRoot, inputs.agentCheckout]) {
    const lock = json(join(root, 'runtime.lock.json'));
    assert.equal(lock.source_commit, RUNTIME_HEAD, 'normal matched Runtime pin required');
    assert.equal(lock.producer_version, ARTIFACT, 'Runtime artifact mismatch');
  }
  assert.equal(realpathSync(join(appRoot, 'node_modules')), realpathSync(inputs.dependencyRoot));
  for (const [name, version] of [
    ['@banodoco/timeline-composition', '0.0.12'], ['react', '18.3.1'], ['react-dom', '18.3.1'],
    ['remotion', '4.0.509'], ['@remotion/player', '4.0.509'], ['@remotion/media', '4.0.509'], ['@remotion/layout-utils', '4.0.509'],
  ]) assert.equal(json(join(inputs.dependencyRoot, name, 'package.json')).version, version, name);
  const cache = realpathSync(inputs.cacheRoot); // Must already exist; never create under borrowed dependencies.
  for (const root of [appRoot, inputs.agentCheckout, inputs.runtimeCheckout, inputs.dependencyRoot,
    '/home/user/work/app/node_modules', '/home/user/work/venv-agent', '/home/user/work/venv-runtime']) {
    assert(!inside(realpathSync(root), cache), 'cacheRoot must be outside source, shared dependencies and venvs');
  }
}
