import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, statSync } from 'node:fs';
import { spawn, spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { P2_PHASE_CAPTURE_FILE, p2CommitPhaseCaptureConfig, RUNTIME_CHECKOUT } from './harness.ts';

const python = process.env.ASTRID_RUNTIME_PYTHON ?? 'python3';
const runtimeCheckout = RUNTIME_CHECKOUT;
const bootstrapDirectory = path.resolve('scripts/testing');

function captureEnvironment(output: string, ordinal = 1): NodeJS.ProcessEnv {
  const config = p2CommitPhaseCaptureConfig(output, ordinal);
  assert.ok(config);
  mkdirSync(config.directory, { recursive: true, mode: 0o700 });
  return {
    ...process.env,
    PYTHONPATH: [bootstrapDirectory, runtimeCheckout].join(path.delimiter),
    ASTRID_P2_COMMIT_PHASE_CAPTURE: '1',
    ASTRID_P2_COMMIT_PHASE_CAPTURE_SINK: config.sink,
    ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER: config.helper,
  };
}

const emitEventAndExit = `
import sitecustomize
import sys
assert sitecustomize._capture is not None
assert sys.gettrace() is not None
import runtime_protocol.cli
assert sys.gettrace() is not None
request = sitecustomize._capture._new_request()
assert request == 1
sitecustomize._capture._begin(request, "handler_entry")
sitecustomize._capture._end(request, "handler_entry")
`;

const emitEventAndWait = `${emitEventAndExit}
print("ready", flush=True)
import signal
def finish(*_):
    sitecustomize._capture.stop()
    raise SystemExit(0)
signal.signal(signal.SIGTERM, finish)
print("armed", flush=True)
import time
time.sleep(30)
`;

function readCapture(sink: string): string {
  const text = readFileSync(sink, 'utf8');
  assert.ok(text.length <= 64 * 1024);
  for (const line of text.trim().split('\n')) {
    const event = JSON.parse(line) as Record<string, unknown>;
    assert.ok(Object.keys(event).every((key) => ['schema_version', 'request', 'phase', 'state', 'at_ms', 'count', 'status', 'last_phase', 'phases', 'truncated'].includes(key)));
    assert.equal(typeof event.phase, 'string');
  }
  assert.match(text, /"phase":"summary"/);
  return text;
}

test('P2 Runtime observer bootstrap is opt-in, source-pinned, bounded, and flushed on exit paths', async () => {
  const root = mkdtempSync(path.join(tmpdir(), 'p2-runtime-bootstrap-'));
  const normal = p2CommitPhaseCaptureConfig(path.join(root, 'normal'))!;
  const normalRun = spawnSync(python, ['-c', emitEventAndExit], { env: captureEnvironment(normal.directory), encoding: 'utf8' });
  assert.equal(normalRun.status, 0, `${normalRun.stdout}\n${normalRun.stderr}`);
  assert.equal(statSync(normal.sink).mode & 0o777, 0o600);
  assert.equal(statSync(normal.directory).mode & 0o777, 0o700);
  assert.equal(normal.helper, path.join(runtimeCheckout, 'tests/helpers/p2_commit_phase_capture.py'));
  const normalText = readCapture(normal.sink);
  assert.match(normalText, /"phase":"handler_entry"/);
  assert.match(normalText, /"phase":"summary"/);
  assert.equal(readFileSync(normal.sink, 'utf8').includes('p2_commit_phase_capture.py'), false);

  const failed = p2CommitPhaseCaptureConfig(path.join(root, 'failed'))!;
  const failedRun = spawnSync(python, ['-c', `${emitEventAndExit}\nraise RuntimeError('private failure text')`], { env: captureEnvironment(failed.directory), encoding: 'utf8' });
  assert.notEqual(failedRun.status, 0);
  assert.doesNotMatch(readCapture(failed.sink), /private failure text/);

  const disabledSink = path.join(root, 'disabled', P2_PHASE_CAPTURE_FILE);
  const disabled = spawnSync(python, ['-c', 'import sys; assert sys.gettrace() is None'], {
    env: { ...process.env, PYTHONPATH: bootstrapDirectory, ASTRID_P2_COMMIT_PHASE_CAPTURE: undefined, ASTRID_P2_COMMIT_PHASE_CAPTURE_SINK: undefined, ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER: undefined },
    encoding: 'utf8',
  });
  assert.equal(disabled.status, 0, `${disabled.stdout}\n${disabled.stderr}`);
  assert.equal(statSync(path.dirname(disabledSink), { throwIfNoEntry: false }), undefined);

  const teardown = p2CommitPhaseCaptureConfig(path.join(root, 'teardown'), 2)!;
  const child = spawn(python, ['-c', emitEventAndWait], { env: captureEnvironment(teardown.directory, 2), stdio: ['ignore', 'pipe', 'pipe'] });
  await new Promise<void>((resolve, reject) => {
    let stdout = '';
    child.stdout?.on('data', (chunk) => {
      stdout += String(chunk);
      if (stdout.includes('armed')) resolve();
    });
    child.once('error', reject);
  });
  child.kill('SIGTERM');
  const exitCode = await new Promise<number | null>((resolve) => child.once('exit', (code) => resolve(code)));
  assert.equal(exitCode, 0);
  assert.equal(statSync(teardown.sink).mode & 0o777, 0o600);
  readCapture(teardown.sink);
});
