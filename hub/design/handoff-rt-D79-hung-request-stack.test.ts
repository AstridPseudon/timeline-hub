import assert from 'node:assert/strict';
import { chmodSync, existsSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { join } from 'node:path';
import { test } from 'node:test';
import { HungRequestStackCapture, attachPlaywrightRuntimeLifecycle, linuxProcessInspector, spawnDebugger, type DebuggerTool, type ProcessInspector, type StackTarget } from './hung-request-stack.ts';

const scratch = process.env.D79_TEST_TMPDIR ?? '/tmp';
let directoryNumber = 0;

class FakeClock {
  value = 0;
  next = 1;
  timers = new Map<number, { at: number; callback: () => void }>();
  now = () => this.value;
  setTimeout = (callback: () => void, delayMs: number) => { const id = this.next++; this.timers.set(id, { at: this.value + delayMs, callback }); return id; };
  clearTimeout = (handle: unknown) => { this.timers.delete(Number(handle)); };
  advance = (milliseconds: number) => {
    this.value += milliseconds;
    for (;;) {
      const due = [...this.timers.entries()].filter(([, timer]) => timer.at <= this.value).sort((left, right) => left[1].at - right[1].at)[0];
      if (!due) return;
      this.timers.delete(due[0]);
      due[1].callback();
    }
  };
}

class FakePage {
  listeners = new Map<string, Array<(...args: unknown[]) => void>>();
  on(event: string, listener: (...args: unknown[]) => void) { this.listeners.set(event, [...(this.listeners.get(event) ?? []), listener]); }
  off(event: string, listener: (...args: unknown[]) => void) { this.listeners.set(event, (this.listeners.get(event) ?? []).filter((candidate) => candidate !== listener)); }
  emit(event: string, ...args: unknown[]) { for (const listener of this.listeners.get(event) ?? []) listener(...args); }
}

function evidence(label: string): string {
  return mkdtempSync(join(scratch, `d79-stack-${label}-${process.pid}-${directoryNumber++}-`));
}

function target(overrides: Partial<StackTarget> = {}): StackTarget {
  return { role: 'runtime-daemon', pid: 41, incarnation: 'inc-1', runId: 'run-1', owned: true, supervised: true, ...overrides };
}

function fakeInspector(current: Record<number, string | null>): ProcessInspector {
  return (pid) => current[pid] ?? null;
}

async function settle(): Promise<void> {
  await new Promise<void>((resolve) => setImmediate(resolve));
  await new Promise<void>((resolve) => setTimeout(resolve, 100));
}

async function waitForFile(file: string, timeoutMs = 7_000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  while (!existsSync(file) && Date.now() < deadline) await new Promise<void>((resolve) => setTimeout(resolve, 100));
}

type CapturedTarget = { status?: string; reason?: string; pid?: number; raw_file?: string; frames?: Array<{ file: string; line: number; function?: string }> };
type CapturedRecord = { run_id?: string; targets: CapturedTarget[] };

function readJson(dir: string, file: string): CapturedRecord {
  return JSON.parse(readFileSync(join(dir, file), 'utf8')) as CapturedRecord;
}

test('captures only an actual request with no response, then cleans up response and abort', async () => {
  const clock = new FakeClock();
  const calls: Array<{ tool: DebuggerTool; args: string[] }> = [];
  const capture = new HungRequestStackCapture({
    runId: 'run-1', evidenceDir: evidence('lifecycle'), clock,
    inspect: fakeInspector({ 41: 'inc-1' }),
    resolveTool: async () => ({ name: 'py-spy', path: '/fake/py-spy' }),
    runDebugger: async (tool, args) => { calls.push({ tool, args }); return { status: 'completed', stdout: '  File "/srv/daemon.py", line 31, in serve\n' }; },
  });
  const page = new FakePage();
  const detach = attachPlaywrightRuntimeLifecycle({
    page, capture, isRuntimeRequest: (request) => (request as { kind?: string }).kind === 'runtime', targets: () => [target()],
  });
  const first = { kind: 'runtime' };
  page.emit('request', first);
  clock.advance(19_999);
  await settle();
  assert.equal(calls.length, 0);
  page.emit('response', { request: () => first });
  clock.advance(1);
  await settle();
  assert.equal(calls.length, 0);

  const second = { kind: 'runtime' };
  page.emit('request', second);
  clock.advance(20_000);
  await settle();
  assert.equal(calls.length, 1);
  const third = { kind: 'runtime' };
  page.emit('request', third);
  page.emit('requestfailed', third);
  clock.advance(20_000);
  await settle();
  assert.equal(calls.length, 1);
  assert.equal(capture.pendingCount(), 1);
  capture.abortAll();
  assert.equal(capture.pendingCount(), 0);
  detach();
});

test('captures multiple pending requests independently and deduplicates one daemon target', async () => {
  const clock = new FakeClock();
  const calls: string[][] = [];
  const dir = evidence('multiple');
  const capture = new HungRequestStackCapture({
    runId: 'run-1', evidenceDir: dir, clock, inspect: fakeInspector({ 41: 'inc-1' }),
    resolveTool: async () => ({ name: 'gdb', path: '/fake/gdb' }),
    runDebugger: async (_tool, args) => { calls.push(args); return { status: 'completed', stdout: '#0 serve at daemon.py:7\n' }; },
  });
  const a = capture.beginRequest({ source: 'runtime-commit', targets: [target(), target({ role: 'provider-alias' })] });
  capture.beginRequest({ source: 'runtime-health', targets: [target()] });
  clock.advance(20_000);
  await settle();
  assert.equal(calls.length, 2);
  assert.equal(readJson(dir, `request-${String(a).padStart(4, '0')}.hung.json`).targets.length, 1);
  assert.equal(capture.pendingCount(), 2);
  capture.completeRequest(a, 'response');
  capture.abortAll();
  assert.equal(capture.pendingCount(), 0);
});

test('unknown, unowned, and changed incarnations produce markers without invoking a debugger', async () => {
  for (const [label, item] of [
    ['unknown', target({ pid: 99 })],
    ['unowned', target({ owned: false })],
    ['unsupervised', target({ supervised: false })],
    ['changed', target({ incarnation: 'inc-old' })],
  ] as const) {
    const clock = new FakeClock();
    let called = false;
    const dir = evidence(label);
    const capture = new HungRequestStackCapture({
      runId: 'run-1', evidenceDir: dir, clock,
      inspect: fakeInspector(item.pid === 99 ? {} : { 41: item.incarnation === 'inc-old' ? 'inc-new' : 'inc-1' }),
      resolveTool: async () => ({ name: 'py-spy', path: '/fake/py-spy' }),
      runDebugger: async () => { called = true; return { status: 'completed' }; },
    });
    capture.beginRequest({ source: 'runtime-commit', targets: [item] });
    clock.advance(20_000);
    await settle();
    assert.equal(called, false, label);
    assert.equal(readJson(dir, 'request-0001.hung.json').targets[0].status, 'unavailable');
  }
});

test('missing tool and debugger refusal are truthful and py-spy failure never retries gdb', async () => {
  const clock = new FakeClock();
  const missingDir = evidence('missing-tool');
  let missingCalled = false;
  const missing = new HungRequestStackCapture({
    runId: 'run-1', evidenceDir: missingDir, clock, inspect: fakeInspector({ 41: 'inc-1' }),
    resolveTool: async () => null,
    runDebugger: async () => { missingCalled = true; return { status: 'completed' }; },
  });
  missing.beginRequest({ source: 'runtime-commit', targets: [target()] });
  clock.advance(20_000);
  await settle();
  assert.equal(missingCalled, false);
  assert.equal(readJson(missingDir, 'request-0001.hung.json').targets[0].reason, 'debugger_unavailable');

  const failureDir = evidence('dump-failure');
  const calls: string[] = [];
  const failureClock = new FakeClock();
  const failure = new HungRequestStackCapture({
    runId: 'run-1', evidenceDir: failureDir, clock: failureClock, inspect: fakeInspector({ 41: 'inc-1' }),
    resolveTool: async () => ({ name: 'py-spy', path: '/fake/py-spy' }),
    runDebugger: async (tool) => { calls.push(tool.name); return { status: 'failed', stderr: 'ptrace: Operation not permitted' }; },
  });
  failure.beginRequest({ source: 'runtime-commit', targets: [target()] });
  failureClock.advance(20_000);
  await settle();
  assert.deepEqual(calls, ['py-spy']);
  assert.equal(readJson(failureDir, 'request-0001.hung.json').targets[0].reason, 'permission_failure');
});

test('fake debugger subprocess writes private raw output and safe frame summary', async () => {
  const dir = evidence('fake-subprocess');
  const fakeTool = join(dir, 'fake-gdb');
  writeFileSync(fakeTool, '#!/bin/sh\nprintf \'#0 in serve at daemon.py:7\\n\'\n');
  chmodSync(fakeTool, 0o700);
  const clock = new FakeClock();
  const capture = new HungRequestStackCapture({
    runId: 'run-1', evidenceDir: dir, clock, inspect: fakeInspector({ 41: 'inc-1' }),
    resolveTool: async () => ({ name: 'gdb', path: fakeTool }), runDebugger: spawnDebugger,
  });
  capture.beginRequest({ source: 'runtime-commit', targets: [target()] });
  clock.advance(20_000);
  await settle();
  const result = readJson(dir, 'request-0001.hung.json').targets[0];
  assert.equal(result.status, 'captured');
  assert.deepEqual(result.frames, [{ file: 'daemon.py', line: 7, function: 'serve' }]);
  assert.equal(existsSync(join(dir, result.raw_file)), true);
});

test('owned Python child smoke is bounded; unavailable or ptrace-refused is recorded without changing control flow', async () => {
  const child = spawn('python3', ['-c', 'import time; time.sleep(30)'], { stdio: 'ignore' });
  try {
    assert.ok(child.pid);
    const incarnation = linuxProcessInspector(child.pid!);
    assert.ok(incarnation);
    const clock = new FakeClock();
    const dir = evidence('python-smoke');
    const capture = new HungRequestStackCapture({
      runId: 'run-1', evidenceDir: dir, clock,
      inspect: linuxProcessInspector,
    });
    capture.beginRequest({ source: 'runtime-commit', targets: [{ role: 'owned-python-child', pid: child.pid!, incarnation: incarnation!, runId: 'run-1', owned: true, supervised: true }] });
    clock.advance(20_000);
    await settle();
    await waitForFile(join(dir, 'request-0001.hung.json'));
    const record = readJson(dir, 'request-0001.hung.json');
    assert.equal(record.run_id, 'run-1');
    assert.equal(record.targets[0].pid, child.pid);
  } finally {
    child.kill('SIGTERM');
  }
});
