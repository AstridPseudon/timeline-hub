import assert from 'node:assert/strict';
import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { test } from 'node:test';
import { failure, fixture, repo } from './fixture.mjs';

// Run explicitly with a PowerShell 7 executable on POSIX. Native Windows
// PowerShell 5.1 also needs qualification on Windows before release.
const powershell = process.env.ASTRID_TEST_PWSH || 'pwsh';
async function scenario(fn) {
  const context = await fixture();
  try {
    const harness = await context.powershell();
    await fn(context, (args = [], env = {}) => context.run(powershell, ['-NoProfile', '-NonInteractive', '-File', harness, ...args], env));
  } finally { await context.cleanup(); }
}
function alive(result) {
  assert.equal(result.code, 0, result.stderr);
  assert.match(result.stdout, /SHELL-ALIVE/);
  assert.match(result.stdout, /PREFERENCE: Continue/);
}

test('PowerShell tolerates native stderr, forwards arguments and avoids Python shims/registry', () => scenario(async (context, run) => {
  context.manifest.agent.repo = path.join(context.root, 'source with spaces');
  context.manifest.runtime.repo = pathToFileURL(path.join(context.root, 'runtime source')).href;
  const flags = ['--update', '--data-root', '/a path/with spaces', 'embedded"quote', 'trailing slash\\'];
  const result = await run(flags);
  alive(result);
  assert.match(result.stdout, /Astrid is ready\./);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
  assert.equal(await readFile(context.env.MOCK_FETCHED, 'utf8'), context.env.ASTRID_INSTALL_MANIFEST_URL);
  const calls = await context.calls();
  assert.deepEqual(calls.find((args) => args[0] === 'python'), ['python', 'install', '3.11.13', '--no-bin', '--no-registry']);
  const core = calls.at(-1);
  for (const name of ['runtime', 'agent']) {
    assert.ok(core.includes(`git+${pathToFileURL(path.join(context.root, name === 'agent' ? 'source with spaces' : 'runtime source')).href}@${context.manifest[name].sha}`));
  }
  assert.deepEqual(core.slice(-flags.length), flags);
  assert.match(await readFile(context.env.MOCK_LOG, 'utf8'), /native progress on stderr/);
}));

test('PowerShell defaults to hosted manifest and exact hosted source pins', () => scenario(async (context, run) => {
  const result = await run([], { ASTRID_INSTALL_MANIFEST_URL: '' });
  alive(result);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
  assert.equal(await readFile(context.env.MOCK_FETCHED, 'utf8'), 'https://astrid.haus/install-manifest.json');
  const core = (await context.calls()).at(-1);
  for (const name of ['runtime', 'agent']) assert.ok(core.includes(`https://github.com/banodoco/astrid-${name}/archive/${context.manifest[name].sha}.tar.gz`));
}));

for (const repoValue of ['relative/path', '', null, 'https://example.com/source', 'file://remote/tmp/repo', 'file:///tmp/repo?branch=main', 'file:///tmp/repo#main', 'file://user@localhost/tmp/repo', 'file://localhost:123/tmp/repo', 'file://localhost:-1/tmp/repo', 'file://localhost', String.raw`\\server\share\repo`]) {
  test(`PowerShell rejects invalid developer source ${JSON.stringify(repoValue)} without closing iex shell`, () => scenario(async (context, run) => {
    context.manifest.agent.repo = repoValue;
    const result = await run();
    alive(result);
    assert.equal((result.stdout.match(/Astrid could not get ready\./g) || []).length, 1);
    assert.equal((result.stdout.match(/Details:/g) || []).length, 1);
    assert.equal((await context.calls()).filter((args) => args.includes('--with')).length, 0);
  }));
}

test('PowerShell rejects invalid commit pins before core', () => scenario(async (context, run) => {
  context.manifest.agent.sha = 'ABCDEF'.repeat(6) + 'ABCD';
  const result = await run();
  alive(result);
  assert.match(result.stdout, /CAUGHT: Astrid could not get ready\./);
  assert.equal((await context.calls()).filter((args) => args.includes('--with')).length, 0);
}));

test('PowerShell rejects mismatching bootstrap pins without preparing Python', () => scenario(async (context, run) => {
  context.manifest.tools.uv.version = '0.8.22';
  const result = await run();
  alive(result);
  assert.match(result.stdout, /CAUGHT: Astrid could not get ready\./);
  assert.deepEqual(await context.calls(), []);
}));

for (const env of [{ MOCK_FETCH_EXIT: '7' }, { MOCK_PYTHON_EXIT: '17' }]) {
  test(`PowerShell reports one pre-core failure for ${JSON.stringify(env)} and keeps iex shell`, () => scenario(async (context, run) => {
    const result = await run([], env);
    alive(result);
    assert.equal((result.stdout.match(/Astrid could not get ready\./g) || []).length, 1);
    assert.equal((result.stdout.match(/Details:/g) || []).length, 1);
  }));
}

test('PowerShell preserves one core failure paragraph and keeps iex shell', () => scenario(async (context, run) => {
  const result = await run([], { MOCK_CORE_EXIT: '23' });
  alive(result);
  assert.ok(result.stdout.includes(`CAUGHT: ${failure}`));
  assert.equal(result.stdout.split(failure).length - 1, 1);
  assert.equal((result.stdout.match(/Details:/g) || []).length, 1);
  assert.doesNotMatch(result.stdout, /Astrid could not get ready/);
}));

test('PowerShell preserves output after uninstall removes bootstrap', () => scenario(async (context, run) => {
  const result = await run(['--uninstall'], { MOCK_REMOVE_BOOTSTRAP: '1' });
  alive(result);
  assert.match(result.stdout, /Astrid was uninstalled\./);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
}));

test('PowerShell -File reports a nonzero process status on a pre-core failure', () => scenario(async (context) => {
  const result = await context.run(powershell, ['-NoProfile', '-NonInteractive', '-File', path.join(repo, 'public/install.ps1')]);
  assert.notEqual(result.code, 0);
  assert.match(result.stderr, /Astrid could not get ready/);
}));

test('PowerShell drains simultaneous multi-megabyte native output without deadlock', () => scenario(async (context, run) => {
  const result = await run([], { MOCK_VOLUME_BYTES: '4194304' });
  alive(result);
  assert.match(result.stdout, /Astrid is ready\./);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
  const log = await readFile(context.env.MOCK_LOG, 'utf8');
  assert.ok(log.includes('o'.repeat(4194304)));
  assert.ok(log.includes('e'.repeat(4194304)));
}));


test('PowerShell handles stderr progress from native uv bootstrap setup', () => scenario(async (context, run) => {
  await rm(path.join(context.env.LOCALAPPDATA, 'Astrid/bootstrap/uv.exe'));
  context.env.SystemRoot = path.join(context.root, 'system root');
  context.env.MOCK_SOURCE_UV = path.join(context.bootstrap, 'uv');
  context.env.MOCK_BOOTSTRAP_ARGS = path.join(context.root, 'bootstrap-args.json');
  const executable = path.join(context.env.SystemRoot, 'System32/WindowsPowerShell/v1.0/powershell.exe');
  await mkdir(path.dirname(executable), { recursive: true });
  await writeFile(executable, `#!/usr/bin/env python3
import json, os, pathlib, shutil, sys
pathlib.Path(os.environ['MOCK_BOOTSTRAP_ARGS']).write_text(json.dumps(sys.argv[1:]))
print('bootstrap progress on stderr', file=sys.stderr)
shutil.copy2(os.environ['MOCK_SOURCE_UV'], pathlib.Path(os.environ['UV_UNMANAGED_INSTALL']) / 'uv.exe')
`, { mode: 0o755 });
  const result = await run();
  alive(result);
  assert.match(result.stdout, /Astrid is ready\./);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
  const args = JSON.parse(await readFile(context.env.MOCK_BOOTSTRAP_ARGS, 'utf8'));
  assert.deepEqual(args.slice(0, 5), ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File']);
  assert.match(args[5], /uv\.ps1$/);
  assert.match(await readFile(context.env.MOCK_LOG, 'utf8'), /bootstrap progress on stderr/);
}));

for (const coreExit of ['0', '23']) {
  test(`PowerShell -File fetches real HTTP manifest and reports core status ${coreExit}`, () => scenario(async (context) => {
    const server = createServer((_request, response) => {
      response.writeHead(200, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify(context.manifest));
    });
    await new Promise((resolve, reject) => {
      server.once('error', reject);
      server.listen(Number(process.env.ASTRID_TEST_INSTALLER_HTTP_PORT || 0), '127.0.0.1', resolve);
    });
    try {
      const flags = ['--update', '--data-root', '/a path/with spaces', 'embedded"quote', 'trailing slash\\'];
      const result = await context.run(powershell, ['-NoProfile', '-NonInteractive', '-File', path.join(repo, 'public/install.ps1'), ...flags], {
        ASTRID_INSTALL_MANIFEST_URL: `http://127.0.0.1:${server.address().port}/install-manifest.json`,
        ...(coreExit === '0' ? {} : { MOCK_CORE_EXIT: coreExit }),
      });
      if (coreExit === '0') {
        assert.equal(result.code, 0, result.stderr);
        assert.match(result.stdout, /Astrid is ready\./);
      } else {
        assert.notEqual(result.code, 0);
        assert.match(result.stderr, /Astrid could not finish/);
        assert.doesNotMatch(result.stderr, /Astrid could not get ready/);
      }
      assert.deepEqual((await context.calls()).at(-1).slice(-flags.length), flags);
    } finally {
      await new Promise((resolve) => server.close(resolve));
    }
  }));
}

test('PowerShell also accepts uv version output without build metadata', () => scenario(async (_context, run) => {
  const result = await run([], { MOCK_UV_VERSION: 'uv 0.11.32' });
  alive(result);
  assert.match(result.stdout, /Astrid is ready\./);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
}));

test('PowerShell accepts localhost file URLs as local pinned repositories', () => scenario(async (context, run) => {
  const local = pathToFileURL(path.join(context.root, 'local source with spaces')).href;
  context.manifest.agent.repo = local.replace('file:///', 'file://localhost/');
  const result = await run();
  alive(result);
  assert.match(result.stdout, /Astrid is ready\./);
  assert.doesNotMatch(result.stdout, /CAUGHT:/);
  assert.ok((await context.calls()).at(-1).includes(`git+${local}@${context.manifest.agent.sha}`));
}));
