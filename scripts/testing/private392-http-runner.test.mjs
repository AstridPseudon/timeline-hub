import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';

const runner = path.resolve('scripts/testing/private392-http-runner.sh');
const source = readFileSync(runner, 'utf8');

test('private392 runner retains Vitest status and cleans its root on failure', () => {
  assert.doesNotMatch(source, /exec\s+node_modules\/\.bin\/vitest/);
  assert.match(source, /trap cleanup EXIT/);
  assert.match(source, /trap 'exit 129' HUP/);
  assert.match(source, /trap 'exit 130' INT/);
  assert.match(source, /trap 'exit 143' TERM/);
  assert.match(source, /node_modules\/\.bin\/vitest run[\s\S]*\|\| status=\$\?/);
  assert.match(source, /exit "\$status"/);

  const root = mkdtempSync(path.join(tmpdir(), 'private392-cleanup-witness-'));
  const childScript = String.raw`RUN_ROOT=$1
mkdir -p "$RUN_ROOT/created"
cleanup() { rm -rf -- "$RUN_ROOT"; }
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
status=0
sh -c 'exit 37' || status=$?
test "$status" -eq 37
exit "$status"
`;
  const child = spawnSync('sh', ['-eu', '-c', childScript, 'cleanup-witness', root], { encoding: 'utf8' });

  try {
    assert.equal(child.status, 37, child.stderr);
    assert.equal(existsSync(root), false, 'failure path left RUN_ROOT behind');
  } finally {
    if (existsSync(root)) rmSync(root, { recursive: true, force: true });
  }
});
