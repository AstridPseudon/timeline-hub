import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { test } from 'node:test';
import { failure, fixture, repo } from './fixture.mjs';

async function scenario(fn) {
  const context = await fixture();
  try { await fn(context); } finally { await context.cleanup(); }
}
const run = (context, args = [], env = {}) => context.run('/bin/sh', [path.join(repo, 'public/install'), ...args], env);

test('POSIX uses developer manifest, XDG bootstrap, exact local commits and Python without external shims', () => scenario(async (context) => {
  context.manifest.agent.repo = path.join(context.root, 'source with spaces');
  context.manifest.runtime.repo = pathToFileURL(path.join(context.root, 'runtime source')).href;
  const result = await run(context, ['--update', '--data-root', '/a path/with spaces']);
  assert.equal(result.code, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'Astrid is ready.');
  assert.equal(await readFile(context.env.MOCK_FETCHED, 'utf8'), context.env.ASTRID_INSTALL_MANIFEST_URL);
  const calls = await context.calls();
  assert.deepEqual(calls.find((args) => args[0] === 'python'), ['python', 'install', '3.11.13', '--no-bin']);
  const core = calls.at(-1);
  for (const name of ['runtime', 'agent']) {
    assert.ok(core.includes(`git+${pathToFileURL(path.join(context.root, name === 'agent' ? 'source with spaces' : 'runtime source')).href}@${context.manifest[name].sha}`));
  }
  assert.deepEqual(core.slice(-3), ['--update', '--data-root', '/a path/with spaces']);
}));

test('POSIX defaults to hosted manifest and pinned source archive URLs', () => scenario(async (context) => {
  const result = await run(context, [], { ASTRID_INSTALL_MANIFEST_URL: '' });
  assert.equal(result.code, 0, result.stderr);
  assert.equal(await readFile(context.env.MOCK_FETCHED, 'utf8'), 'https://astrid.haus/install-manifest.json');
  const core = (await context.calls()).at(-1);
  for (const name of ['runtime', 'agent']) assert.ok(core.includes(`https://github.com/banodoco/astrid-${name}/archive/${context.manifest[name].sha}.tar.gz`));
}));

for (const repoValue of ['relative/path', '', null, 'https://example.com/source', 'file://remote/tmp/repo', 'file:///tmp/repo?branch=main', 'file:///tmp/repo#main', 'file://user@localhost/tmp/repo', 'file://localhost:123/tmp/repo', 'file://localhost:-1/tmp/repo', 'file://localhost']) {
  test(`POSIX rejects invalid developer source ${JSON.stringify(repoValue)} before core`, () => scenario(async (context) => {
    context.manifest.agent.repo = repoValue;
    const result = await run(context);
    assert.equal(result.code, 1);
    assert.equal((result.stderr.match(/Astrid could not get ready\./g) || []).length, 1);
    assert.equal((await context.calls()).filter((args) => args.includes('--with')).length, 0);
  }));
}

test('POSIX rejects invalid commit pins before core', () => scenario(async (context) => {
  context.manifest.agent.sha = 'main';
  assert.equal((await run(context)).code, 1);
  assert.equal((await context.calls()).filter((args) => args.includes('--with')).length, 0);
}));

test('POSIX rejects a mismatching manifest tool pin', () => scenario(async (context) => {
  context.manifest.tools.uv.version = '0.8.22';
  assert.equal((await run(context)).code, 1);
  assert.equal((await context.calls()).filter((args) => args.includes('--with')).length, 0);
}));

for (const env of [{ MOCK_FETCH_EXIT: '7' }, { MOCK_PYTHON_EXIT: '17' }]) {
  test(`POSIX reports one pre-core failure for ${JSON.stringify(env)}`, () => scenario(async (context) => {
    const result = await run(context, [], env);
    assert.equal(result.code, 1);
    assert.equal((result.stderr.match(/Astrid could not get ready\./g) || []).length, 1);
    assert.equal((result.stderr.match(/Details:/g) || []).length, 1);
  }));
}

test('POSIX preserves the core failure paragraph and nonzero status once', () => scenario(async (context) => {
  const result = await run(context, [], { MOCK_CORE_EXIT: '23' });
  assert.equal(result.code, 23);
  assert.equal((result.stdout.match(new RegExp(failure.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length, 1);
  assert.equal((result.stdout.match(/Details:/g) || []).length, 1);
  assert.doesNotMatch(result.stderr, /Astrid could not get ready/);
}));

test('POSIX preserves success output when uninstall removes bootstrap', () => scenario(async (context) => {
  const result = await run(context, ['--uninstall'], { MOCK_REMOVE_BOOTSTRAP: '1' });
  assert.equal(result.code, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'Astrid was uninstalled.');
}));

test('POSIX also accepts uv version output without build metadata', () => scenario(async (context) => {
  const result = await run(context, [], { MOCK_UV_VERSION: 'uv 0.11.32' });
  assert.equal(result.code, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'Astrid is ready.');
}));

test('POSIX accepts localhost file URLs as local pinned repositories', () => scenario(async (context) => {
  const local = pathToFileURL(path.join(context.root, 'local source with spaces')).href;
  context.manifest.agent.repo = local.replace('file:///', 'file://localhost/');
  const result = await run(context);
  assert.equal(result.code, 0, result.stderr);
  assert.equal(result.stdout.trim(), 'Astrid is ready.');
  assert.ok((await context.calls()).at(-1).includes(`git+${local}@${context.manifest.agent.sha}`));
}));
