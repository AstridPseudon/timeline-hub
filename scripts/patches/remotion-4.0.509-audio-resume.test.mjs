import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const SCRIPT = path.join(ROOT, 'scripts/patches/remotion-4.0.509-audio-resume.mjs');
const ACTUAL_ROOT = process.env.REMOTION_509_CHECK_ROOT || ROOT;
const HAS_ACTUAL_INSTALL = fs.existsSync(path.join(ACTUAL_ROOT, 'node_modules/remotion/package.json'));
const TARGETS = [
  'dist/cjs/audio/shared-audio-tags.js',
  'dist/esm/index.mjs',
];

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function run(action, root) {
  return spawnSync(process.execPath, [SCRIPT, action, '--root', root], { encoding: 'utf8' });
}

function fixture(version) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'remotion-509-guard-'));
  const packageRoot = path.join(root, 'node_modules/remotion');
  fs.mkdirSync(packageRoot, { recursive: true });
  fs.writeFileSync(
    path.join(packageRoot, 'package.json'),
    JSON.stringify({ name: 'remotion', version }),
  );
  return { root, packageRoot };
}

test(
  'the installed 4.0.509 CJS and ESM fence passes check/apply without file changes',
  { skip: !HAS_ACTUAL_INSTALL },
  () => {
    const files = TARGETS.map((relative) => path.join(ACTUAL_ROOT, 'node_modules/remotion', relative));
    const before = files.map((file) => sha256(fs.readFileSync(file)));
    for (const action of ['--check', '--apply']) {
      const result = run(action, ACTUAL_ROOT);
      assert.equal(result.status, 0, result.stdout + result.stderr);
      assert.match(result.stdout, /remotion@4\.0\.509/);
    }
    assert.deepEqual(files.map((file) => sha256(fs.readFileSync(file))), before);
  },
);

test('unknown Remotion file bytes refuse before either file is changed', (t) => {
  const { root, packageRoot } = fixture('4.0.509');
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const files = TARGETS.map((relative) => {
    const file = path.join(packageRoot, relative);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, 'unknown fixture bytes for ' + relative + '\n');
    return file;
  });
  const before = files.map((file) => fs.readFileSync(file));
  const result = run('--apply', root);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /unknown content/i);
  assert.deepEqual(files.map((file) => fs.readFileSync(file)), before);
});

test('unknown Remotion version refuses before target files are read or written', (t) => {
  const { root, packageRoot } = fixture('4.0.508');
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const result = run('--apply', root);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /expected remotion@4\.0\.509/i);
  assert.deepEqual(
    fs.readdirSync(packageRoot),
    ['package.json'],
    'version preflight must stop before touching either CJS or ESM file',
  );
});
