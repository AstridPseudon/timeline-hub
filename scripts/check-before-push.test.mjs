import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const source = readFileSync(fileURLToPath(new URL('./check-before-push', import.meta.url)), 'utf8');

test('pre-push keeps fixture Git commands out of the parent repository', () => {
  const base = mkdtempSync(path.join(tmpdir(), 'astrid-pre-push-env-'));
  const parent = path.join(base, 'parent');
  const fixture = path.join(base, 'fixture.git');
  const bin = path.join(base, 'bin');
  const env = { ...process.env };
  // The regression itself must also be safe when launched from a Git hook.
  for (const name of execFileSync('git', ['rev-parse', '--local-env-vars'], { encoding: 'utf8' }).trim().split('\n')) delete env[name];
  const git = (...args) => execFileSync('git', args, { cwd: parent, env, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  try {
    mkdirSync(path.join(parent, 'scripts'), { recursive: true });
    mkdirSync(bin);
    git('init', '-q');
    git('config', 'user.name', 'Parent Owner');
    git('config', 'user.email', 'parent@example.invalid');
    writeFileSync(path.join(parent, 'scripts/check-before-push'), source, { mode: 0o755 });
    git('add', '.');
    git('commit', '-qm', 'parent');
    const before = { head: git('rev-parse', 'HEAD'), config: readFileSync(path.join(parent, '.git/config'), 'utf8') };
    // Run the real hook driver, replacing only its expensive guard/test commands.
    writeFileSync(path.join(bin, 'node'), '#!/bin/sh\nexit 0\n', { mode: 0o755 });
    writeFileSync(path.join(bin, 'npm'), '#!/bin/sh\nset -eu\ngit init --bare -q "$FIXTURE_REPO"\ngit --git-dir="$FIXTURE_REPO" config user.name "Fixture Owner"\n', { mode: 0o755 });
    execFileSync('bash', [path.join(parent, 'scripts/check-before-push')], {
      cwd: parent,
      env: { ...env, PATH: `${bin}:${env.PATH}`, FIXTURE_REPO: fixture, GIT_DIR: path.join(parent, '.git'), GIT_WORK_TREE: parent, GIT_INDEX_FILE: path.join(parent, '.git/index') },
      stdio: 'pipe',
    });
    assert.equal(git('rev-parse', 'HEAD'), before.head);
    assert.equal(readFileSync(path.join(parent, '.git/config'), 'utf8'), before.config);
    assert.equal(git('config', 'core.bare'), 'false');
    assert.equal(git('status', '--porcelain'), '');
    assert.equal(execFileSync('git', ['--git-dir', fixture, 'config', 'user.name'], { env, encoding: 'utf8' }).trim(), 'Fixture Owner');
  } finally {
    rmSync(base, { recursive: true, force: true });
  }
});
