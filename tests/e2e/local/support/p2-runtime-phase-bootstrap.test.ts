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
const NORMAL_HELPER_SHA256 = 'a17a92115661fcef13b49169504ad8726e6f6c0cdce66b195128b14477fa76a4';
const REVIEWED_HELPER_SHA256 = '6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760';
const NORMAL_PHASES = ['dispatch_queue', 'handler_entry', 'authorization', 'coordinator_admission', 'coordinator_lock', 'provider', 'accept', 'receipt', 'http_response'];
const REVIEWED_PHASES = ['arrival', ...NORMAL_PHASES];

function exactKeys(value: Record<string, unknown>, keys: string[]): void {
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort());
}

function assertFiniteNumber(value: unknown, label: string, { nonnegative = false } = {}): asserts value is number {
  assert.equal(typeof value, 'number', label);
  assert.ok(Number.isFinite(value), label);
  if (nonnegative) assert.ok(value >= 0, label);
}

function assertNumberOrNull(value: unknown, label: string): void {
  if (value !== null) assertFiniteNumber(value, label);
}

function assertNoPrivateKeys(value: unknown): void {
  if (!value || typeof value !== 'object') return;
  for (const [key, child] of Object.entries(value)) {
    if (!REVIEWED_PHASES.includes(key)) {
      assert.doesNotMatch(key, /^(?:body|raw_body|headers?|authorization|auth|url|stack|traceback|exception|credentials?|token|password|secret|idempotency_key)$/i);
    }
    assertNoPrivateKeys(child);
  }
}

function assertPhaseMap(phases: unknown, reviewed: boolean): void {
  assert.ok(phases && typeof phases === 'object' && !Array.isArray(phases));
  const rows = phases as Record<string, unknown>;
  const phaseNames = reviewed ? REVIEWED_PHASES : NORMAL_PHASES;
  exactKeys(rows, phaseNames);
  for (const phase of phaseNames) {
    const row = rows[phase];
    assert.ok(row && typeof row === 'object' && !Array.isArray(row));
    const state = row as Record<string, unknown>;
    const unsupportedArrival = reviewed && phase === 'arrival' && state.status === 'unsupported';
    exactKeys(state, unsupportedArrival ? ['status', 'count', 'start_ms', 'end_ms', 'reason'] : ['status', 'count', 'start_ms', 'end_ms']);
    assert.ok(['UNKNOWN', 'observed', 'raised', ...(unsupportedArrival ? ['unsupported'] : [])].includes(state.status as string));
    assert.equal(typeof state.count, 'number');
    assert.ok(Number.isInteger(state.count) && state.count >= 0 && state.count <= 32);
    assertNumberOrNull(state.start_ms, `${phase}.start_ms`);
    assertNumberOrNull(state.end_ms, `${phase}.end_ms`);
    if (unsupportedArrival) assert.equal(state.reason, 'no earlier socket/server-accept hook');
  }
}

function assertRetention(value: unknown): void {
  assert.ok(value && typeof value === 'object' && !Array.isArray(value));
  const retention = value as Record<string, unknown>;
  exactKeys(retention, ['format_version', 'mode', 'rolling', 'final_request', 'output']);
  assert.equal(retention.format_version, 2);
  assert.equal(retention.mode, 'rolling_plus_final_request');
  const rolling = retention.rolling as Record<string, unknown>;
  assert.ok(rolling && typeof rolling === 'object' && !Array.isArray(rolling));
  exactKeys(rolling, ['capacity_events', 'events_seen', 'events_retained', 'capacity_dropped_events', 'complete', 'incomplete_limit']);
  for (const key of ['capacity_events', 'events_seen', 'events_retained', 'capacity_dropped_events']) {
    assert.equal(typeof rolling[key], 'number');
    assert.ok(Number.isInteger(rolling[key]) && (rolling[key] as number) >= 0);
  }
  assert.equal(rolling.capacity_events, 128);
  assert.equal(typeof rolling.complete, 'boolean');
  assert.equal(rolling.incomplete_limit, null);
  const output = retention.output as Record<string, unknown>;
  assert.ok(output && typeof output === 'object' && !Array.isArray(output));
  exactKeys(output, ['max_bytes', 'bytes', 'events']);
  assert.equal(output.max_bytes, 64 * 1024);
  for (const key of ['bytes', 'events']) {
    assert.equal(typeof output[key], 'number');
    assert.ok(Number.isInteger(output[key]) && (output[key] as number) >= 0);
  }
  assert.equal(retention.final_request, null);
}

function assertSampling(value: unknown): void {
  assert.ok(value && typeof value === 'object' && !Array.isArray(value));
  const sampling = value as Record<string, unknown>;
  exactKeys(sampling, ['sampling_interval_ms', 'sample_total', 'lost_samples', 'observer_cpu_ms', 'observer_cpu_scope', 'observer_cpu_attribution', 'top_inclusive_frames', 'sample_membership', 'dispatch_wall_denominator_ms', 'counter_limits', 'sampler_errors']);
  assertFiniteNumber(sampling.sampling_interval_ms, 'sampling_interval_ms', { nonnegative: true });
  for (const key of ['sample_total', 'lost_samples']) {
    assert.equal(typeof sampling[key], 'number');
    assert.ok(Number.isInteger(sampling[key]) && (sampling[key] as number) >= 0);
  }
  assertFiniteNumber(sampling.observer_cpu_ms, 'observer_cpu_ms', { nonnegative: true });
  assert.equal(sampling.observer_cpu_scope, 'capture-wide');
  assert.equal(sampling.observer_cpu_attribution, 'sampler CPU covers the whole capture and is not attributed to this request');
  assert.equal(sampling.sample_membership, 'each safe frame identity is counted at most once per sample');
  assertNumberOrNull(sampling.dispatch_wall_denominator_ms, 'dispatch_wall_denominator_ms');
  assert.ok(Array.isArray(sampling.sampler_errors));
  for (const error of sampling.sampler_errors) assert.equal(typeof error, 'string');
  const limits = sampling.counter_limits as Record<string, unknown>;
  assert.ok(limits && typeof limits === 'object' && !Array.isArray(limits));
  exactKeys(limits, ['max_requests', 'max_events', 'max_bytes', 'top_frames']);
  assert.deepEqual(limits, { max_requests: 8, max_events: 128, max_bytes: 64 * 1024, top_frames: 10 });
  assert.ok(Array.isArray(sampling.top_inclusive_frames));
  for (const frame of sampling.top_inclusive_frames) {
    assert.ok(frame && typeof frame === 'object' && !Array.isArray(frame));
    const row = frame as Record<string, unknown>;
    exactKeys(row, ['file', 'function', 'line', 'sample_count', 'sample_total', 'sample_share', 'dispatch_wall_share']);
    assert.match(row.file as string, /^<(?:runtime|agent|stdlib)>\//);
    assert.equal(typeof row.function, 'string');
    assert.equal(typeof row.line, 'number');
    assert.ok(Number.isInteger(row.line) && (row.line as number) > 0);
    assert.equal(typeof row.sample_count, 'number');
    assert.ok(Number.isInteger(row.sample_count) && (row.sample_count as number) >= 0);
    assert.equal(typeof row.sample_total, 'number');
    assert.ok(Number.isInteger(row.sample_total) && (row.sample_total as number) >= 0);
    assertFiniteNumber(row.sample_share, 'sample_share', { nonnegative: true });
    assertNumberOrNull(row.dispatch_wall_share, 'dispatch_wall_share');
  }
}

function assertCaptureEvent(event: Record<string, unknown>, reviewed: boolean): void {
  assertNoPrivateKeys(event);
  const phase = event.phase;
  assert.equal(event.schema_version, 1);
  assert.equal(typeof event.request, 'number');
  assert.ok(Number.isInteger(event.request) && (event.request as number) >= 1 && (event.request as number) <= 8);
  if (phase !== 'summary' || reviewed) assertFiniteNumber(event.at_ms, 'at_ms', { nonnegative: true });
  if (phase === 'summary') {
    exactKeys(event, reviewed
      ? ['schema_version', 'request', 'phase', 'last_phase', 'phases', 'durations_ms', 'utc', 'at_ms', 'capture_anchor', 'capture_namespace', 'pid', 'birth_ticks', 'method', 'route_template', 'idempotency_key_sha256', 'dispatch_start_ms', 'sampling', 'unknown_boundaries', 'unsupported_boundaries', 'truncated', 'retention']
      : ['schema_version', 'request', 'phase', 'last_phase', 'phases', 'durations_ms', 'unknown_boundaries', 'truncated', 'retention']);
    assert.equal(typeof event.last_phase, 'string');
    assert.ok([...NORMAL_PHASES, 'UNKNOWN'].includes(event.last_phase as string));
    assertPhaseMap(event.phases, reviewed);
    const durations = event.durations_ms as Record<string, unknown>;
    assert.ok(durations && typeof durations === 'object' && !Array.isArray(durations));
    const durationKeys = reviewed
      ? ['dispatch_queue_ms', 'handler_ms', 'dispatch_total_ms', 'dispatch_to_completion_wall_ms', 'provider_wall_ms', 'response_write_wall_ms', 'execution_lock_wait_ms', 'caller_receipt_ms']
      : ['dispatch_queue_ms', 'handler_ms', 'dispatch_total_ms', 'provider_wall_ms', 'response_write_wall_ms', 'execution_lock_wait_ms', 'caller_receipt_ms'];
    exactKeys(durations, durationKeys);
    for (const value of Object.values(durations)) assertNumberOrNull(value, 'duration');
    assert.equal(typeof event.truncated, 'boolean');
    assertRetention(event.retention);
    const unknown = event.unknown_boundaries as Record<string, unknown>;
    assert.ok(unknown && typeof unknown === 'object' && !Array.isArray(unknown));
    exactKeys(unknown, reviewed
      ? ['client_request_to_server_receive', 'request_body_receive', 'execution_lock_wait', 'caller_receipt']
      : ['client_request_to_server_receive', 'execution_lock_wait', 'caller_receipt']);
    assert.equal(unknown.client_request_to_server_receive, reviewed ? 'unsupported: no earlier socket/server-accept hook' : 'outside Runtime process');
    assert.equal(unknown.execution_lock_wait, 'phase hook has no exact threading.Lock.acquire boundary');
    assert.equal(unknown.caller_receipt, 'outside Runtime process');
    if (reviewed) {
      assert.match(event.utc as string, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
      const anchor = event.capture_anchor as Record<string, unknown>;
      assert.ok(anchor && typeof anchor === 'object' && !Array.isArray(anchor));
      exactKeys(anchor, ['utc', 'at_ms']);
      assert.match(anchor.utc as string, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
      assert.equal(anchor.at_ms, 0);
      assert.equal(typeof event.capture_namespace, 'string');
      assert.equal(typeof event.pid, 'number');
      assert.ok(Number.isInteger(event.pid) && (event.pid as number) > 0);
      if (event.birth_ticks !== null) assert.ok(Number.isInteger(event.birth_ticks) && (event.birth_ticks as number) >= 0);
      assert.equal(event.method, 'POST');
      assert.equal(event.route_template, '/v1/projects/{project_id}/timelines/{timeline_id}/commit');
      assert.match(event.idempotency_key_sha256 as string, /^[0-9a-f]{64}$/);
      assertNumberOrNull(event.dispatch_start_ms, 'dispatch_start_ms');
      assertSampling(event.sampling);
      const unsupported = event.unsupported_boundaries as Record<string, unknown>;
      assert.ok(unsupported && typeof unsupported === 'object' && !Array.isArray(unsupported));
      exactKeys(unsupported, ['network_arrival_ms', 'request_body_receive_ms', 'execution_lock_wait_ms', 'caller_receipt_ms']);
      assert.deepEqual(unsupported, { network_arrival_ms: null, request_body_receive_ms: null, execution_lock_wait_ms: null, caller_receipt_ms: null });
    }
    return;
  }
  assert.ok(typeof phase === 'string' && NORMAL_PHASES.includes(phase));
  const expectedKeys = ['schema_version', 'request', 'phase', 'state', 'at_ms', 'count', ...(phase === 'http_response' ? ['status'] : [])];
  if (reviewed && ['dispatch_queue', 'coordinator_lock', 'handler_entry'].includes(phase as string)) {
    expectedKeys.push('namespace', 'capture_namespace', 'pid', 'birth_ticks', 'utc', 'method', 'route_template', 'idempotency_key_sha256');
  } else if (reviewed) {
    expectedKeys.push('utc', 'capture_namespace');
  }
  exactKeys(event, expectedKeys);
  assert.ok(['start', 'end', 'raised'].includes(event.state as string));
  assert.equal(typeof event.count, 'number');
  assert.ok(Number.isInteger(event.count) && (event.count as number) >= 1 && (event.count as number) <= 32);
  if (phase === 'http_response') {
    assert.equal(typeof event.status, 'number');
    assert.ok(Number.isInteger(event.status) && (event.status as number) >= 100 && (event.status as number) <= 599);
  }
  if (reviewed) {
    assert.match(event.utc as string, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
    assert.equal(typeof event.capture_namespace, 'string');
    if (['dispatch_queue', 'coordinator_lock', 'handler_entry'].includes(phase as string)) {
      assert.equal(event.namespace, phase);
      assert.equal(typeof event.pid, 'number');
      assert.equal(event.method, 'POST');
      assert.equal(event.route_template, '/v1/projects/{project_id}/timelines/{timeline_id}/commit');
      assert.match(event.idempotency_key_sha256 as string, /^[0-9a-f]{64}$/);
    }
  }
}

test('D105 launch ownership gives each retained DirectHarness start a distinct sink while keeping ordinal one unchanged', () => {
  const root = mkdtempSync(path.join(tmpdir(), 'p2-runtime-launch-ordinal-'));
  const first = p2CommitPhaseCaptureConfig(root, 1)!;
  const second = p2CommitPhaseCaptureConfig(root, 2)!;
  assert.equal(path.basename(first.sink), P2_PHASE_CAPTURE_FILE);
  assert.equal(path.basename(second.sink), 'p2-commit-phase-2.jsonl');
  assert.notEqual(first.sink, second.sink);
});

function readCapture(sink: string, helperSha256: string): string {
  const text = readFileSync(sink, 'utf8');
  assert.ok(text.length <= 64 * 1024);
  const reviewed = helperSha256 === REVIEWED_HELPER_SHA256;
  assert.ok(helperSha256 === NORMAL_HELPER_SHA256 || reviewed, `unexpected P2 helper identity: ${helperSha256}`);
  const events = text.trim().split('\n').map((line) => JSON.parse(line) as Record<string, unknown>);
  assert.ok(events.length > 0);
  for (const event of events) assertCaptureEvent(event, reviewed);
  assert.equal(text.includes('p2_commit_phase_capture.py'), false);
  assert.equal(text.includes('Bearer '), false);
  assert.equal(text.includes('Content-Type'), false);
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
  if (config.helperSha256 === NORMAL_HELPER_SHA256) {
    assert.equal(config.helper, path.join(runtimeCheckout, 'tests/helpers/p2_commit_phase_capture.py'));
  } else {
    assert.equal(config.helperSha256, REVIEWED_HELPER_SHA256);
    assert.equal(path.basename(config.helper), 'p2_commit_phase_capture.py');
  }
  const smokeText = readCapture(config.sink, config.helperSha256);
  assert.match(smokeText, /"phase":"handler_entry"/);
  assert.match(smokeText, /"phase":"authorization"/);
  assert.match(smokeText, /"phase":"provider"/);
  assert.match(smokeText, /"phase":"receipt"/);
  assert.match(smokeText, /"phase":"http_response"/);
  assert.equal(readFileSync(config.sink, 'utf8').includes('p2_commit_phase_capture.py'), false);
});
