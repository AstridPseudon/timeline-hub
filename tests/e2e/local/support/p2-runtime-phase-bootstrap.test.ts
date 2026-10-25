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
const MAX_REQUESTS = 8;
const MAX_EVENTS = 128;
const MAX_BYTES = 64 * 1024;
const MAX_PHASE_COUNT = 32;
const PRIVATE_VALUE = /(?:bearer\s|private|marker|content-type|raw[_-]?body|authorization|password|secret|token|credential|stack(?:trace)?|traceback|exception)/i;

function exactKeys(value: Record<string, unknown>, keys: string[]): void {
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort());
}

function record(value: unknown, label: string): Record<string, unknown> {
  assert.ok(value && typeof value === 'object' && !Array.isArray(value), label);
  return value as Record<string, unknown>;
}

function assertFiniteNumber(value: unknown, label: string, { nonnegative = false } = {}): asserts value is number {
  assert.equal(typeof value, 'number', label);
  assert.ok(Number.isFinite(value), label);
  if (nonnegative) assert.ok(value >= 0, label);
}

function assertNumberOrNull(value: unknown, label: string): void {
  if (value !== null) assertFiniteNumber(value, label);
}

function assertInteger(value: unknown, label: string, { minimum = 0, maximum }: { minimum?: number; maximum?: number } = {}): asserts value is number {
  assert.equal(typeof value, 'number', label);
  assert.ok(Number.isInteger(value) && value >= minimum, label);
  if (maximum !== undefined) assert.ok(value <= maximum, label);
}

function assertSafeIdentifier(value: unknown, label: string): void {
  assert.equal(typeof value, 'string', label);
  assert.match(value, /^(?:[A-Za-z_][A-Za-z0-9_]*|<[^<>\r\n]{1,64}>)$/, label);
  assert.doesNotMatch(value, PRIVATE_VALUE, label);
}

function assertTimestamp(value: unknown, label: string): void {
  assertFiniteNumber(value, label, { nonnegative: true });
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
    const state = record(row, `${phase} state`);
    const unsupportedArrival = reviewed && phase === 'arrival';
    exactKeys(state, unsupportedArrival ? ['status', 'count', 'start_ms', 'end_ms', 'reason'] : ['status', 'count', 'start_ms', 'end_ms']);
    assertInteger(state.count, `${phase}.count`, { maximum: MAX_PHASE_COUNT });
    if (unsupportedArrival) {
      assert.equal(state.status, 'unsupported');
      assert.equal(state.count, 0);
      assert.equal(state.start_ms, null);
      assert.equal(state.end_ms, null);
      assert.equal(state.reason, 'no earlier socket/server-accept hook');
      continue;
    }
    if (state.count === 0) {
      assert.equal(state.status, 'UNKNOWN');
      assert.equal(state.start_ms, null);
      assert.equal(state.end_ms, null);
    } else {
      assert.ok(state.status === 'observed' || state.status === 'raised');
      assertTimestamp(state.start_ms, `${phase}.start_ms`);
      assertNumberOrNull(state.end_ms, `${phase}.end_ms`);
      if (state.end_ms !== null) assert.ok(state.end_ms >= state.start_ms, `${phase}.end_ms`);
      if (state.status === 'raised') assert.notEqual(state.end_ms, null, `${phase}.raised end`);
    }
  }
}

function assertRetention(value: unknown): void {
  const retention = record(value, 'retention');
  exactKeys(retention, ['format_version', 'mode', 'rolling', 'final_request', 'output']);
  assert.equal(retention.format_version, 2);
  assert.equal(retention.mode, 'rolling_plus_final_request');
  const rolling = record(retention.rolling, 'retention.rolling');
  exactKeys(rolling, ['capacity_events', 'events_seen', 'events_retained', 'capacity_dropped_events', 'complete', 'incomplete_limit']);
  assertInteger(rolling.capacity_events, 'capacity_events');
  assertInteger(rolling.events_seen, 'events_seen');
  assertInteger(rolling.events_retained, 'events_retained');
  assertInteger(rolling.capacity_dropped_events, 'capacity_dropped_events');
  assert.equal(rolling.capacity_events, MAX_EVENTS);
  const rollingCount = Math.min(rolling.events_seen, rolling.capacity_events);
  assert.ok(rolling.events_retained <= rollingCount);
  assert.equal(rolling.capacity_dropped_events, Math.max(0, rolling.events_seen - rolling.capacity_events));
  assert.equal(typeof rolling.complete, 'boolean');
  if (rolling.complete) {
    assert.equal(rolling.events_retained, rollingCount);
    assert.equal(rolling.incomplete_limit, null);
  } else {
    const limit = record(rolling.incomplete_limit, 'rolling.incomplete_limit');
    assertDropLimit(limit, 'rolling.incomplete_limit');
    assert.equal(limit.dropped_events, rollingCount - rolling.events_retained);
  }
  const output = record(retention.output, 'retention.output');
  exactKeys(output, ['max_bytes', 'bytes', 'events']);
  assertInteger(output.max_bytes, 'output.max_bytes');
  assertInteger(output.bytes, 'output.bytes', { maximum: MAX_BYTES });
  assertInteger(output.events, 'output.events');
  assert.equal(output.max_bytes, MAX_BYTES);
  assert.equal(output.bytes === 0, output.events === 0);
  assert.ok(output.events <= rolling.events_seen);
  assert.ok(rolling.events_retained <= output.events);
  if (retention.final_request === null) return;
  const finalRequest = record(retention.final_request, 'retention.final_request');
  exactKeys(finalRequest, ['request', 'outcome', 'events_seen', 'events_retained', 'complete', 'incomplete_limit']);
  assertInteger(finalRequest.request, 'final_request.request', { minimum: 1, maximum: MAX_REQUESTS });
  assert.ok(['complete', 'failed', 'pending'].includes(finalRequest.outcome as string));
  assertInteger(finalRequest.events_seen, 'final_request.events_seen');
  assertInteger(finalRequest.events_retained, 'final_request.events_retained');
  assert.ok(finalRequest.events_retained <= finalRequest.events_seen);
  assert.ok(finalRequest.events_retained <= output.events);
  assert.equal(typeof finalRequest.complete, 'boolean');
  if (finalRequest.complete) assert.equal(finalRequest.incomplete_limit, null);
  else {
    const limit = record(finalRequest.incomplete_limit, 'final_request.incomplete_limit');
    assertDropLimit(limit, 'final_request.incomplete_limit', true);
    assert.ok(limit.required_bytes >= limit.retained_bytes);
    assert.equal(limit.required_bytes, limit.retained_bytes + limit.dropped_bytes);
  }
}

function assertDropLimit(limit: Record<string, unknown>, label: string, requestLimit = false): void {
  exactKeys(limit, requestLimit
    ? ['reason', 'limit_bytes', 'required_bytes', 'retained_bytes', 'dropped_events', 'dropped_bytes']
    : ['reason', 'limit_bytes', 'dropped_events', 'dropped_bytes']);
  assert.equal(limit.reason, 'max_bytes', label);
  assertInteger(limit.limit_bytes, `${label}.limit_bytes`);
  assert.equal(limit.limit_bytes, MAX_BYTES);
  assertInteger(limit.dropped_events, `${label}.dropped_events`, { minimum: 1 });
  assertInteger(limit.dropped_bytes, `${label}.dropped_bytes`, { minimum: 1 });
  if (requestLimit) {
    assertInteger(limit.required_bytes, `${label}.required_bytes`);
    assertInteger(limit.retained_bytes, `${label}.retained_bytes`);
    assert.ok(limit.required_bytes >= limit.retained_bytes);
  }
}

function assertSampling(value: unknown): void {
  const sampling = record(value, 'sampling');
  exactKeys(sampling, ['sampling_interval_ms', 'sample_total', 'lost_samples', 'observer_cpu_ms', 'observer_cpu_scope', 'observer_cpu_attribution', 'top_inclusive_frames', 'sample_membership', 'dispatch_wall_denominator_ms', 'counter_limits', 'sampler_errors']);
  assertFiniteNumber(sampling.sampling_interval_ms, 'sampling_interval_ms', { nonnegative: true });
  assert.equal(sampling.sampling_interval_ms, 20);
  assertInteger(sampling.sample_total, 'sample_total');
  assertInteger(sampling.lost_samples, 'lost_samples');
  assertFiniteNumber(sampling.observer_cpu_ms, 'observer_cpu_ms', { nonnegative: true });
  assert.equal(sampling.observer_cpu_scope, 'capture-wide');
  assert.equal(sampling.observer_cpu_attribution, 'sampler CPU covers the whole capture and is not attributed to this request');
  assert.equal(sampling.sample_membership, 'each safe frame identity is counted at most once per sample');
  assertNumberOrNull(sampling.dispatch_wall_denominator_ms, 'dispatch_wall_denominator_ms');
  if (sampling.dispatch_wall_denominator_ms !== null) assert.ok(sampling.dispatch_wall_denominator_ms > 0);
  assert.ok(Array.isArray(sampling.sampler_errors));
  for (const error of sampling.sampler_errors) assertSafeIdentifier(error, 'sampler_errors');
  const limits = record(sampling.counter_limits, 'counter_limits');
  exactKeys(limits, ['max_requests', 'max_events', 'max_bytes', 'top_frames']);
  assert.deepEqual(limits, { max_requests: 8, max_events: 128, max_bytes: 64 * 1024, top_frames: 10 });
  assert.ok(Array.isArray(sampling.top_inclusive_frames));
  assert.ok(sampling.top_inclusive_frames.length <= 10);
  const seenFrames = new Set<string>();
  for (const frame of sampling.top_inclusive_frames) {
    const row = record(frame, 'top_inclusive_frames row');
    exactKeys(row, ['file', 'function', 'line', 'sample_count', 'sample_total', 'sample_share', 'dispatch_wall_share']);
    assert.equal(typeof row.file, 'string');
    assert.match(row.file, /^<(?:runtime|agent|stdlib)>\/[A-Za-z0-9_./<>-]+$/);
    assert.doesNotMatch(row.file, PRIVATE_VALUE);
    assertSafeIdentifier(row.function, 'frame.function');
    assertInteger(row.line, 'frame.line', { minimum: 1 });
    assertInteger(row.sample_count, 'frame.sample_count', { minimum: 1 });
    assertInteger(row.sample_total, 'frame.sample_total');
    assert.equal(row.sample_total, sampling.sample_total);
    assert.ok(row.sample_count <= row.sample_total);
    assertFiniteNumber(row.sample_share, 'sample_share', { nonnegative: true });
    assert.ok(row.sample_share <= 1);
    assert.equal(row.sample_total === 0, false);
    assert.ok(Math.abs(row.sample_share - row.sample_count / row.sample_total) < 1e-12);
    assertNumberOrNull(row.dispatch_wall_share, 'dispatch_wall_share');
    if (row.dispatch_wall_share !== null) {
      assert.ok(row.dispatch_wall_share >= 0);
      assert.ok(sampling.dispatch_wall_denominator_ms !== null);
      assert.ok(Math.abs(row.dispatch_wall_share - (row.sample_count * 20 / sampling.dispatch_wall_denominator_ms)) < 1e-12);
    }
    const identity = `${row.file}\0${row.function}\0${row.line}`;
    assert.equal(seenFrames.has(identity), false);
    seenFrames.add(identity);
  }
}

function assertCaptureEvent(event: Record<string, unknown>, reviewed: boolean): void {
  assertNoPrivateKeys(event);
  const phase = event.phase;
  assert.equal(event.schema_version, 1);
  assertInteger(event.request, 'request', { minimum: 1, maximum: MAX_REQUESTS });
  if (phase !== 'summary' || reviewed) assertFiniteNumber(event.at_ms, 'at_ms', { nonnegative: true });
  if (phase === 'summary') {
    exactKeys(event, reviewed
      ? ['schema_version', 'request', 'phase', 'last_phase', 'phases', 'durations_ms', 'utc', 'at_ms', 'capture_anchor', 'capture_namespace', 'pid', 'birth_ticks', 'method', 'route_template', 'idempotency_key_sha256', 'dispatch_start_ms', 'sampling', 'unknown_boundaries', 'unsupported_boundaries', 'truncated', 'retention']
      : ['schema_version', 'request', 'phase', 'last_phase', 'phases', 'durations_ms', 'unknown_boundaries', 'truncated', 'retention']);
    assert.equal(typeof event.last_phase, 'string');
    assert.ok([...NORMAL_PHASES, 'UNKNOWN'].includes(event.last_phase as string));
    assertPhaseMap(event.phases, reviewed);
    const durations = record(event.durations_ms, 'durations_ms');
    const durationKeys = reviewed
      ? ['dispatch_queue_ms', 'handler_ms', 'dispatch_total_ms', 'dispatch_to_completion_wall_ms', 'provider_wall_ms', 'response_write_wall_ms', 'execution_lock_wait_ms', 'caller_receipt_ms']
      : ['dispatch_queue_ms', 'handler_ms', 'dispatch_total_ms', 'provider_wall_ms', 'response_write_wall_ms', 'execution_lock_wait_ms', 'caller_receipt_ms'];
    exactKeys(durations, durationKeys);
    for (const [key, value] of Object.entries(durations)) {
      assertNumberOrNull(value, `duration ${key}`);
      if (value !== null) assert.ok(value >= 0, `duration ${key}`);
    }
    if (durations.dispatch_total_ms !== null && durations.dispatch_queue_ms !== null && durations.handler_ms !== null) {
      assert.ok(Math.abs(durations.dispatch_total_ms - (durations.dispatch_queue_ms + durations.handler_ms)) < 1e-9);
    }
    if (reviewed) assert.equal(durations.dispatch_to_completion_wall_ms, durations.dispatch_total_ms);
    assert.equal(typeof event.truncated, 'boolean');
    assertRetention(event.retention);
    const unknown = record(event.unknown_boundaries, 'unknown_boundaries');
    exactKeys(unknown, reviewed
      ? ['client_request_to_server_receive', 'request_body_receive', 'execution_lock_wait', 'caller_receipt']
      : ['client_request_to_server_receive', 'execution_lock_wait', 'caller_receipt']);
    assert.equal(unknown.client_request_to_server_receive, reviewed ? 'unsupported: no earlier socket/server-accept hook' : 'outside Runtime process');
    if (reviewed) assert.equal(unknown.request_body_receive, 'unsupported: no body-read hook; body time is not separately measured');
    assert.equal(unknown.execution_lock_wait, 'phase hook has no exact threading.Lock.acquire boundary');
    assert.equal(unknown.caller_receipt, 'outside Runtime process');
    if (reviewed) {
      assert.match(event.utc as string, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
      const anchor = record(event.capture_anchor, 'capture_anchor');
      exactKeys(anchor, ['utc', 'at_ms']);
      assert.match(anchor.utc as string, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
      assert.equal(anchor.at_ms, 0);
      assert.match(event.capture_namespace as string, /^pid-\d+-birth-(?:\d+|unknown)-capture-\d+$/);
      assertInteger(event.pid, 'pid', { minimum: 1 });
      if (event.birth_ticks !== null) assertInteger(event.birth_ticks, 'birth_ticks');
      assert.equal(event.method, 'POST');
      assert.equal(event.route_template, '/v1/projects/{project_id}/timelines/{timeline_id}/commit');
      assert.match(event.idempotency_key_sha256 as string, /^[0-9a-f]{64}$/);
      assertNumberOrNull(event.dispatch_start_ms, 'dispatch_start_ms');
      if (event.dispatch_start_ms !== null) assert.ok(event.dispatch_start_ms >= 0);
      assertSampling(event.sampling);
      const unsupported = record(event.unsupported_boundaries, 'unsupported_boundaries');
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
  assertInteger(event.count, 'event.count', { minimum: 1, maximum: MAX_PHASE_COUNT });
  if (phase === 'http_response') {
    assert.equal(typeof event.status, 'number');
    assert.ok(Number.isInteger(event.status) && (event.status as number) >= 100 && (event.status as number) <= 599);
  }
  if (reviewed) {
    assert.match(event.utc as string, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
    assert.match(event.capture_namespace as string, /^pid-\d+-birth-(?:\d+|unknown)-capture-\d+$/);
    if (['dispatch_queue', 'coordinator_lock', 'handler_entry'].includes(phase as string)) {
      assert.equal(event.namespace, phase);
      assertInteger(event.pid, 'event.pid', { minimum: 1 });
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
