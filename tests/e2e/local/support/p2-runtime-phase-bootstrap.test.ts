import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, statSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { AstridCli } from './astrid.ts';
import { P2_PHASE_CAPTURE_FILE, p2CommitPhaseCaptureConfig, RUNTIME_CHECKOUT, startDirectHarness } from './harness.ts';

const python = process.env.ASTRID_RUNTIME_PYTHON ?? 'python3';
const runtimeCheckout = RUNTIME_CHECKOUT;
const bootstrapDirectory = path.resolve('scripts/testing');

function readCapture(sink: string): string {
  const text = readFileSync(sink, 'utf8');
  assert.ok(text.length <= 64 * 1024);
  for (const line of text.trim().split('\n')) {
    const event = JSON.parse(line) as Record<string, unknown>;
    assert.ok(Object.keys(event).every((key) => ['schema_version', 'request', 'phase', 'state', 'at_ms', 'count', 'status', 'last_phase', 'phases', 'truncated'].includes(key)));
    assert.equal(typeof event.phase, 'string');
  }
  return text;
}

function readBootstrappedWatchdog(root: string, seconds?: string): { seconds: number; stack_sink: string } {
  const config = p2CommitPhaseCaptureConfig(path.join(root, seconds ? `watchdog-${seconds}` : 'watchdog-default'))!;
  mkdirSync(config.directory, { recursive: true, mode: 0o700 });
  const run = spawnSync(python, ['-c', [
    'import json, sys, sitecustomize',
    "sys.argv = ['-m', 'start']",
    'sitecustomize._start_capture()',
    "print(json.dumps({'seconds': sitecustomize._capture.watchdog_seconds, 'stack_sink': str(sitecustomize._capture.watchdog_sink)}))",
    'sitecustomize._capture.stop()',
  ].join(';')], {
    env: {
      ...process.env,
      PYTHONPATH: [bootstrapDirectory, runtimeCheckout].join(path.delimiter),
      ASTRID_P2_COMMIT_PHASE_CAPTURE: undefined,
      ASTRID_P2_COMMIT_PHASE_CAPTURE_SINK: config.sink,
      ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER: config.helper,
      ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS: seconds,
    },
    encoding: 'utf8',
  });
  assert.equal(run.status, 0, `${run.stdout}\n${run.stderr}`);
  return JSON.parse(run.stdout.trim()) as { seconds: number; stack_sink: string };
}

test('D78 bootstrap passes the selected watchdog to the existing helper and preserves its private stack name', () => {
  const root = mkdtempSync(path.join(tmpdir(), 'p2-runtime-watchdog-options-'));
  assert.deepEqual(readBootstrappedWatchdog(root), {
    seconds: 20,
    stack_sink: path.join(root, 'watchdog-default', 'p2-commit-phase.stacks.txt'),
  });
  assert.deepEqual(readBootstrappedWatchdog(root, '2'), {
    seconds: 2,
    stack_sink: path.join(root, 'watchdog-2', 'p2-commit-phase.stacks.txt'),
  });
});

test('P2 Runtime observer bootstrap is opt-in, source-pinned, bounded, and flushed on exit paths', async () => {
  const root = mkdtempSync(path.join(tmpdir(), 'p2-runtime-bootstrap-'));
  const disabledSink = path.join(root, 'disabled', P2_PHASE_CAPTURE_FILE);
  const disabled = spawnSync(python, ['-c', 'import sys; assert sys.gettrace() is None'], {
    env: { ...process.env, PYTHONPATH: bootstrapDirectory, ASTRID_P2_COMMIT_PHASE_CAPTURE: undefined, ASTRID_P2_COMMIT_PHASE_CAPTURE_SINK: undefined, ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER: undefined },
    encoding: 'utf8',
  });
  assert.equal(disabled.status, 0, `${disabled.stdout}\n${disabled.stderr}`);
  assert.equal(statSync(path.dirname(disabledSink), { throwIfNoEntry: false }), undefined);

  const unmatched = p2CommitPhaseCaptureConfig(path.join(root, 'unmatched'))!;
  const unmatchedRun = spawnSync(python, ['-c', 'import sys; assert sys.gettrace() is None'], {
    env: {
      ...process.env,
      PYTHONPATH: bootstrapDirectory,
      ASTRID_P2_COMMIT_PHASE_CAPTURE: '1',
      ASTRID_P2_COMMIT_PHASE_CAPTURE_SINK: unmatched.sink,
      ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER: unmatched.helper,
    },
    encoding: 'utf8',
  });
  assert.equal(unmatchedRun.status, 0, `${unmatchedRun.stdout}\n${unmatchedRun.stderr}`);
  assert.equal(statSync(unmatched.directory, { throwIfNoEntry: false }), undefined);

  const runtimeLogDir = mkdtempSync(path.join(tmpdir(), 'p2-runtime-cli-smoke-'));
  const previousLogDir = process.env.D66_RUNTIME_LOG_DIR;
  const previousWatchdog = process.env.ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS;
  process.env.D66_RUNTIME_LOG_DIR = runtimeLogDir;
  process.env.ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS = '2';
  let harness: Awaited<ReturnType<typeof startDirectHarness>> | undefined;
  try {
    harness = await startDirectHarness();
    assert.equal(harness.lifecycleObservation?.launchModule, 'runtime_protocol.cli');
    assert.equal(harness.lifecycleObservation?.actualModule, 'runtime_protocol.cli');
    const astrid = await AstridCli.create(harness);
    const timeline = await harness.runtimeJson<{ head_publication_id: string }>(
      'GET', `/v1/projects/${harness.seed.projectId}/timelines/${harness.seed.timelineId}`,
    );
    assert.equal(timeline.status, 200);
    const accepted = await astrid.commitCaptured(
      harness.seed.projectId,
      harness.seed.timelineId,
      { revision_id: harness.seed.headRevisionId, publication_id: timeline.body.head_publication_id },
      { kind: 'track', id: 'p2-real-worker-proof' },
      'p2-real-worker-proof',
    );
    assert.equal(accepted.data.status, 'accepted');
  } finally {
    await harness?.stop();
    if (previousLogDir === undefined) delete process.env.D66_RUNTIME_LOG_DIR;
    else process.env.D66_RUNTIME_LOG_DIR = previousLogDir;
    if (previousWatchdog === undefined) delete process.env.ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS;
    else process.env.ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS = previousWatchdog;
  }

  const config = p2CommitPhaseCaptureConfig(runtimeLogDir);
  assert.ok(config);
  assert.equal(statSync(config.sink).mode & 0o777, 0o600);
  assert.equal(statSync(config.directory).mode & 0o777, 0o700);
  assert.equal(config.helper, path.join(runtimeCheckout, 'tests/helpers/p2_commit_phase_capture.py'));
  const smokeText = readCapture(config.sink);
  assert.match(smokeText, /"phase":"handler_entry"/);
  assert.match(smokeText, /"phase":"authorization"/);
  assert.match(smokeText, /"phase":"provider"/);
  assert.match(smokeText, /"phase":"receipt"/);
  assert.match(smokeText, /"phase":"http_response"/);
  assert.equal(readFileSync(config.sink, 'utf8').includes('p2_commit_phase_capture.py'), false);
});
