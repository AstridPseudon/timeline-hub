import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import {
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

const GRAPH_FILE_COUNT = 77;

function shell(command, cwd, env = {}) {
  return execFileSync('bash', ['-c', command], {
    cwd,
    env: { ...process.env, ...env },
    stdio: ['ignore', 'pipe', 'pipe'],
    encoding: 'utf8',
  });
}

function graphDigest(root) {
  const hash = createHash('sha256');
  const visit = (current) => {
    for (const name of readdirSync(current).sort()) {
      const entry = path.join(current, name);
      const stat = lstatSync(entry);
      assert.equal(stat.isSymbolicLink(), false, 'protected graph must not contain a symlink: ' + entry);
      if (stat.isDirectory()) {
        hash.update('dir:' + path.relative(root, entry) + '\n');
        visit(entry);
      } else {
        hash.update('file:' + path.relative(root, entry) + '\n');
        hash.update(readFileSync(entry));
      }
    }
  };
  visit(root);
  return hash.digest('hex');
}

function makeFixture() {
  const root = mkdtempSync(path.join(os.tmpdir(), 'public-trim-graph-'));
  const sharedModules = path.join(root, 'shared', 'node_modules');
  const protectedRoot = path.join(root, 'protected');
  const protectedModules = path.join(protectedRoot, 'node_modules');
  const snapshot = path.join(root, 'snapshot');
  mkdirSync(sharedModules, { recursive: true });
  mkdirSync(protectedModules, { recursive: true });
  mkdirSync(snapshot, { recursive: true });
  for (let index = 0; index < GRAPH_FILE_COUNT; index += 1) {
    const relative = path.join('package', 'file-' + String(index).padStart(2, '0') + '.js');
    for (const modules of [sharedModules, protectedModules]) {
      const file = path.join(modules, relative);
      mkdirSync(path.dirname(file), { recursive: true });
      writeFileSync(file, modules === protectedModules ? 'protected-' + index + '\n' : 'shared-' + index + '\n');
    }
  }
  writeFileSync(path.join(protectedRoot, 'READY'), 'graph=private13\n');
  writeFileSync(path.join(protectedRoot, 'LEASE'), 'status=READY\ngraph=private13\n');
  symlinkSync(sharedModules, path.join(snapshot, 'node_modules'), 'dir');
  return { root, protectedRoot, protectedModules, sharedModules, snapshot };
}

function graphGuard(snapshot, protectedRoot, protectedModules) {
  return shell(
    [
      'set -Eeuo pipefail',
      'test "$(realpath node_modules)" = "' + protectedModules + '"',
      'test ! -L "' + protectedModules + '"',
      'test -f "' + path.join(protectedRoot, 'READY') + '"',
      'test -f "' + path.join(protectedRoot, 'LEASE') + '"',
      'rg -q "status=READY" "' + path.join(protectedRoot, 'LEASE') + '"',
    ].join('; '),
    snapshot,
  );
}

function attachThenGuard(snapshot, protectedRoot, protectedModules) {
  return shell(
    [
      'set -Eeuo pipefail',
      'test -d "' + protectedModules + '"',
      'test ! -L "' + protectedModules + '"',
      'rm -f node_modules',
      'ln -s "' + protectedModules + '" node_modules',
      'test "$(realpath node_modules)" = "' + protectedModules + '"',
      'test ! -L "' + protectedModules + '"',
      'test -f "' + path.join(protectedRoot, 'READY') + '"',
      'test -f "' + path.join(protectedRoot, 'LEASE') + '"',
      'rg -q "status=READY" "' + path.join(protectedRoot, 'LEASE') + '"',
    ].join('; '),
    snapshot,
  );
}

test('public Trim attaches the protected physical graph before its existing guard', () => {
  const fixture = makeFixture();
  try {
    const before = graphDigest(fixture.protectedRoot);
    assert.equal(realpathSync(path.join(fixture.snapshot, 'node_modules')), fixture.sharedModules);
    assert.throws(
      () => graphGuard(fixture.snapshot, fixture.protectedRoot, fixture.protectedModules),
      /Command failed|status 1/,
      'the default shared snapshot link must be refused',
    );
    attachThenGuard(fixture.snapshot, fixture.protectedRoot, fixture.protectedModules);
    assert.equal(realpathSync(path.join(fixture.snapshot, 'node_modules')), fixture.protectedModules);
    assert.equal(readdirSync(fixture.protectedModules, { recursive: true }).filter((entry) => entry.endsWith('.js')).length, GRAPH_FILE_COUNT);
    assert.equal(graphDigest(fixture.protectedRoot), before, 'attaching the graph must not mutate protected bytes');
  } finally {
    rmSync(fixture.root, { recursive: true, force: true });
  }
});
