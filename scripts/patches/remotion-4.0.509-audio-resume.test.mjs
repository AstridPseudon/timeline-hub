import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFile, mkdir, mkdtemp, readFile, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const SCRIPT = fileURLToPath(new URL('./remotion-4.0.509-audio-resume.mjs', import.meta.url));
const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const REMOTION_SOURCE_ROOT = process.env.REMOTION_SOURCE_ROOT ?? join(REPO_ROOT, 'node_modules', 'remotion');
const PLAYER_SOURCE_ROOT = process.env.PLAYER_SOURCE_ROOT ?? join(REPO_ROOT, 'node_modules', '@remotion', 'player');
const VERSION = '4.0.509';
const TARGETS = [
  {
    relativePath: 'dist/cjs/audio/shared-audio-tags.js',
    originalSha256: '471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c',
    patchedSha256: '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
  },
  {
    relativePath: 'dist/esm/index.mjs',
    originalSha256: '9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8',
    patchedSha256: '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/cjs/use-player-methods.js',
    originalSha256: 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    patchedSha256: '6bb73dd46e710761ef8ad6d16be3cb103c7e5c2bcbf8342f39c28586717cf0c5',
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/esm/index.mjs',
    originalSha256: 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    patchedSha256: '0b98ec41a8f69dfe75ca46ca4eb16794eef65848f282e9459705ca5dfc6d0581',
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/cjs/use-playback.js',
    originalSha256: '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    patchedSha256: '18a5d6551196a67630be4dc53f6adb18e8e300b71ae9990a1d2f00d80728afbf',
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/cjs/PlayerUI.js',
    originalSha256: '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    patchedSha256: '05e0dd2c4c98ecd95b32e18af8385680bc83324f92fbc36e3de438e9bfb04ffa',
  },
];

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function run(action, root) {
  return spawnSync(process.execPath, [SCRIPT, action, '--root', root], {
    encoding: 'utf8',
  });
}

function assertSuccess(result) {
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
}

async function fixture(t) {
  const root = await mkdtemp(join(tmpdir(), 'remotion-audio-resume-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const packageRoot = join(root, 'node_modules', 'remotion');
  await mkdir(packageRoot, { recursive: true });
  await writeFile(
    join(packageRoot, 'package.json'),
    JSON.stringify({ name: 'remotion', version: VERSION }),
  );

  const playerRoot = join(root, 'node_modules', '@remotion', 'player');
  await mkdir(playerRoot, { recursive: true });
  await writeFile(join(playerRoot, 'package.json'), JSON.stringify({ name: '@remotion/player', version: VERSION }));

  // Copy only the target files. Revert in this isolated fixture so tests
  // always begin with exact pristine bytes, even after the installed package
  // has been patched by its single owner.
  for (const target of TARGETS) {
    const source = join(target.packageName ? PLAYER_SOURCE_ROOT : REMOTION_SOURCE_ROOT, target.relativePath);
    const destination = join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath);
    await mkdir(dirname(destination), { recursive: true });
    await copyFile(source, destination);
  }
  assertSuccess(run('--revert', root));
  for (const target of TARGETS) {
    assert.equal(
      sha256(await readFile(join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath))),
      target.originalSha256,
      `${target.relativePath} fixture must start with exact pristine bytes`,
    );
  }
  return { root, packageRoot };
}

test('six-file fixture: check is readonly; apply is exact/idempotent; revert restores pristine bytes', async (t) => {
  const { root, packageRoot } = await fixture(t);
  const paths = TARGETS.map((target) => join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath));
  const pristineBytes = await Promise.all(paths.map((path) => readFile(path)));

  assertSuccess(run('--check', root));
  assert.deepEqual(await Promise.all(paths.map((path) => readFile(path))), pristineBytes);

  assertSuccess(run('--apply', root));
  for (let index = 0; index < paths.length; index += 1) {
    assert.equal(sha256(await readFile(paths[index])), TARGETS[index].patchedSha256);
  }

  const beforeIdempotentApply = await Promise.all(paths.map((path) => stat(path)));
  assertSuccess(run('--apply', root));
  const afterIdempotentApply = await Promise.all(paths.map((path) => stat(path)));
  assert.deepEqual(
    afterIdempotentApply.map(({ ino }) => ino),
    beforeIdempotentApply.map(({ ino }) => ino),
    'idempotent apply must not rewrite already-patched files',
  );

  assertSuccess(run('--check', root));
  assertSuccess(run('--revert', root));
  assert.deepEqual(await Promise.all(paths.map((path) => readFile(path))), pristineBytes);
});

test('unknown content refuses before any target is written', async (t) => {
  const { root, packageRoot } = await fixture(t);
  const firstPath = join(packageRoot, TARGETS[0].relativePath);
  const secondPath = join(packageRoot, TARGETS[1].relativePath);
  const firstBefore = await readFile(firstPath);
  const secondBefore = Buffer.concat([
    await readFile(secondPath),
    Buffer.from('\n// unknown fixture content\n'),
  ]);
  await writeFile(secondPath, secondBefore);

  const result = run('--apply', root);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /unknown content/i);
  assert.deepEqual(await readFile(firstPath), firstBefore);
  assert.deepEqual(await readFile(secondPath), secondBefore);
});

test('unknown version refuses before any target is written', async (t) => {
  const { root, packageRoot } = await fixture(t);
  const packageJsonPath = join(packageRoot, 'package.json');
  const paths = TARGETS.map((target) => join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath));
  const before = await Promise.all(paths.map((path) => readFile(path)));
  await writeFile(packageJsonPath, JSON.stringify({ name: 'remotion', version: '4.0.504' }));

  const result = run('--apply', root);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /expected remotion@4\.0\.509/i);
  assert.deepEqual(await Promise.all(paths.map((path) => readFile(path))), before);
});

for (const target of TARGETS.filter(target => target.packageName)) {
  test(`unknown Player content ${target.relativePath} refuses before any target is written`, async t => {
    const { root } = await fixture(t);
    const paths = TARGETS.map(target => join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath));
    const damaged = join(root, 'node_modules', target.packageName, target.relativePath);
    await writeFile(damaged, Buffer.concat([await readFile(damaged), Buffer.from('\n// unknown\n')]));
    const before = await Promise.all(paths.map(path => readFile(path)));
    const result = run('--apply', root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /unknown content/);
    assert.deepEqual(await Promise.all(paths.map(path => readFile(path))), before);
  });
}

test('unknown Player version refuses before any target is written', async t => {
  const { root } = await fixture(t);
  const paths = TARGETS.map(target => join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath));
  const before = await Promise.all(paths.map(path => readFile(path)));
  await writeFile(join(root, 'node_modules/@remotion/player/package.json'), JSON.stringify({ name: '@remotion/player', version: '4.0.504' }));
  const result = run('--apply', root);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /expected @remotion\/player@4\.0\.509/);
  assert.deepEqual(await Promise.all(paths.map(path => readFile(path))), before);
});

test('upgrade from the original resume patch applies Player startup without changing old hashes', async t => {
  const { root } = await fixture(t);
  for (const target of TARGETS.filter(target => !target.packageName)) {
    await copyFile(join(REMOTION_SOURCE_ROOT, target.relativePath), join(root, 'node_modules/remotion', target.relativePath));
  }
  assertSuccess(run('--apply', root));
  for (const target of TARGETS) {
    assert.equal(sha256(await readFile(join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath))), target.patchedSha256);
  }
});

test('a failed second rename rolls back the first target and removes staged files', async t => {
  const { root } = await fixture(t);
  const paths = TARGETS.map(target => join(root, 'node_modules', target.packageName ?? 'remotion', target.relativePath));
  const before = await Promise.all(paths.map(path => readFile(path)));
  const preload = join(root, 'fail-rename.mjs');
  await writeFile(preload, `import fs from 'node:fs/promises';
import {syncBuiltinESMExports} from 'node:module';
const rename = fs.rename;
let calls = 0;
fs.rename = async (...args) => {
  if (++calls === 2) throw new Error('planted second rename failure');
  return rename(...args);
};
syncBuiltinESMExports();
`);
  const result = spawnSync(process.execPath, ['--import', preload, SCRIPT, '--apply', '--root', root], {encoding: 'utf8'});
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /planted second rename failure/);
  assert.deepEqual(await Promise.all(paths.map(path => readFile(path))), before);
  const {readdir} = await import('node:fs/promises');
  assert.equal((await readdir(join(root, 'node_modules'), {recursive: true})).some(name => name.endsWith('.tmp')), false);
});
