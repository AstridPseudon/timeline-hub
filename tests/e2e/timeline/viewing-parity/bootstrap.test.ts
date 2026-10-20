import assert from 'node:assert/strict';
import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { EventEmitter } from 'node:events';
import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { PassThrough } from 'node:stream';
import { test } from 'node:test';
import { startRealPackHost } from './bootstrap';

const READY = { status: 'ready', host_pid: 456, host_status: 'ready', host_ready_capabilities: ['rendering.render'] };
const STOPPED = { status: 'stopped', host_pid: 456 };

// Unit protocol peer only: no Python, Runtime, credentials, sockets or real host.
class Helper extends EventEmitter {
  stdin = new PassThrough();
  stdout = new PassThrough();
  stderr = new PassThrough();
  signals: string[] = [];
  input = '';
  closed = false;
  constructor(onStop?: (helper: Helper) => void) {
    super();
    this.stdin.on('data', chunk => { this.input += chunk.toString(); });
    this.stdin.on('finish', () => {
      if (onStop) onStop(this);
      else { this.send(STOPPED); this.close(0); }
    });
  }
  send(value: unknown) { this.stdout.write(`${JSON.stringify(value)}\n`); }
  close(code: number | null) {
    if (this.closed) return;
    this.closed = true;
    this.stdout.end();
    this.stderr.end();
    setImmediate(() => this.emit('close', code));
  }
  kill(signal: string) { this.signals.push(signal); this.close(null); return true; }
}

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), 'viewing-host-unit-'));
  const source = join(root, 'frozen-agent');
  const helperPath = join(source, 'tests/packs/rendering/real_pack_host.py');
  await mkdir(join(helperPath, '..'), { recursive: true });
  await writeFile(helperPath, '# Unit path fixture; never executed.\n');
  const env = {
    ASTRID_CHECKOUT: source, ASTRID_PYTHON: '/parent/python',
    PATH: '/parent/node/bin', ASTRID_REMOTION_BROWSER_EXECUTABLE: '/parent/browser',
    ASTRID_REMOTION_PROJECT_DIR: '/parent/remotion', ASTRID_RUNTIME_CHECKOUT: '/parent/runtime',
    PYTHONPATH: 'parent-pythonpath', PRIVATE_CREDENTIAL: 'do-not-print',
  };
  const runtimeEnv = { PYTHONPATH: '/parent/runtime:/frozen/agent', PYTHONUNBUFFERED: '1' };
  const harness = {
    tmp: root, realmDir: join(root, 'realm'), supportDir: join(root, 'support'),
    runtimeInstanceId: 'instance-exact', runtimeEnv: () => runtimeEnv,
  };
  function options(helper: Helper, onStart = () => helper.send(READY)) {
    const calls: Parameters<typeof spawn>[] = [];
    const spawnHelper = ((...args: Parameters<typeof spawn>) => {
      calls.push(args);
      setImmediate(onStart);
      return helper as unknown as ChildProcessWithoutNullStreams;
    }) as typeof spawn;
    return { env, spawn: spawnHelper, startupTimeoutMs: 100, stopTimeoutMs: 100, calls };
  }
  return { root, source, helperPath, env, runtimeEnv, harness, options,
    cleanup: () => rm(root, { recursive: true, force: true }) };
}

test('passes exact harness argv and parent environment; waits for catalog readiness; stop is idempotent', async () => {
  const f = await fixture();
  try {
    const helper = new Helper();
    const options = f.options(helper);
    let release!: () => void;
    const catalog = new Promise<void>(resolve => { release = resolve; });
    let entered!: () => void;
    const checkingCatalog = new Promise<void>(resolve => { entered = resolve; });
    let returned = false;
    const pending = startRealPackHost(f.harness, () => { entered(); return catalog; }, options)
      .then(value => { returned = true; return value; });
    await checkingCatalog;
    assert.equal(returned, false);
    release();
    const session = await pending;
    assert.deepEqual(options.calls, [[f.env.ASTRID_PYTHON, [f.helperPath,
      '--realm-dir', f.harness.realmDir, '--support-dir', f.harness.supportDir,
      '--discovery-file', join(f.harness.supportDir, 'discovery.json'),
      '--source-checkout', f.source, '--runtime-instance-id', f.harness.runtimeInstanceId,
    ], { cwd: f.root, env: { ...f.env, ...f.runtimeEnv }, stdio: 'pipe', detached: false }]]);
    const first = session.stop();
    assert.equal(session.stop(), first);
    await first;
    assert.equal(helper.input, 'stop\n');
    assert.deepEqual(helper.signals, []);
    assert.equal(helper.closed, true);
  } finally { await f.cleanup(); }
});

test('fails closed for absent or non-frozen source selection without spawning', async () => {
  const f = await fixture();
  try {
    for (const source of [undefined, 'relative-agent', join(f.root, 'missing')]) {
      const options = f.options(new Helper());
      options.env = { ...f.env, ASTRID_CHECKOUT: source } as typeof f.env;
      await assert.rejects(startRealPackHost(f.harness, async () => {}, options), /frozen|absent/);
      assert.equal(options.calls.length, 0);
    }
  } finally { await f.cleanup(); }
});

for (const scenario of ['failed', 'malformed', 'invalid-ready', 'eof', 'exit', 'spawn-error', 'oversize'] as const) {
  test(`rejects ${scenario} and cleans the owned helper without exposing output`, async () => {
    const f = await fixture();
    try {
      const helper = new Helper(peer => { peer.send(READY); peer.send(STOPPED); peer.close(0); });
      const options = f.options(helper, () => {
        helper.stderr.write('do-not-print credentials and arbitrary diagnostics');
        if (scenario === 'failed') helper.send({ status: 'failed', secret: 'do-not-print' });
        if (scenario === 'malformed') helper.stdout.write('do-not-print\n');
        if (scenario === 'invalid-ready') helper.send({ ...READY, host_ready_capabilities: [], secret: 'do-not-print' });
        if (scenario === 'eof') helper.stdout.end();
        if (scenario === 'exit') helper.close(1);
        if (scenario === 'spawn-error') { helper.emit('error', new Error('do-not-print')); helper.close(-1); }
        if (scenario === 'oversize') helper.stdout.write('x'.repeat(70_000));
      });
      if (scenario === 'eof') helper.stdin.removeAllListeners('finish');
      await assert.rejects(startRealPackHost(f.harness, async () => { assert.fail('catalog must not be checked'); }, options),
        error => error instanceof Error && !error.message.includes('do-not-print'));
      assert.equal(helper.closed, true);
      assert.ok(helper.signals.every(signal => signal === 'SIGTERM'));
    } finally { await f.cleanup(); }
  });
}

test('catalog refusal cleans the ready helper and redacts external exceptions', async () => {
  const f = await fixture();
  try {
    const helper = new Helper();
    await assert.rejects(startRealPackHost(f.harness, async () => { throw new Error('do-not-print'); }, f.options(helper)),
      /Runtime rendering capability readiness check failed$/);
    assert.equal(helper.closed, true);
    assert.equal(helper.input, 'stop\n');
  } finally { await f.cleanup(); }
});

for (const mode of ['missing-ack', 'wrong-pid', 'bad-exit', 'timeout', 'ack-without-exit'] as const) {
  test(`stop propagates ${mode} cleanup failure`, async () => {
    const f = await fixture();
    try {
      const helper = new Helper(peer => {
        if (mode === 'timeout') return;
        if (mode === 'wrong-pid') peer.send({ ...STOPPED, host_pid: 999 });
        else if (mode !== 'missing-ack') peer.send(STOPPED);
        if (mode !== 'ack-without-exit') peer.close(mode === 'bad-exit' ? 1 : 0);
      });
      const options = { ...f.options(helper), stopTimeoutMs: 15 };
      const session = await startRealPackHost(f.harness, async () => {}, options);
      const stopping = session.stop();
      await assert.rejects(stopping, /cleanup failed|cleanup timed out/);
      assert.equal(session.stop(), stopping);
      assert.equal(helper.closed, true);
      assert.deepEqual(helper.signals, mode === 'timeout' || mode === 'ack-without-exit' ? ['SIGTERM'] : []);
    } finally { await f.cleanup(); }
  });
}

test('startup timeout closes stdin, waits for cleanup and reaps only the helper', async () => {
  const f = await fixture();
  try {
    const helper = new Helper();
    const options = { ...f.options(helper, () => {}), startupTimeoutMs: 15, stopTimeoutMs: 15 };
    await assert.rejects(startRealPackHost(f.harness, async () => {}, options), /readiness timed out/);
    assert.equal(helper.closed, true);
    assert.equal(helper.input, 'stop\n');
  } finally { await f.cleanup(); }
});

test('abort during startup cleans helper; pre-aborted startup never spawns', async () => {
  const f = await fixture();
  try {
    const controller = new AbortController();
    const helper = new Helper(peer => { peer.send(READY); peer.send(STOPPED); peer.close(0); });
    const options = { ...f.options(helper, () => controller.abort()), signal: controller.signal };
    await assert.rejects(startRealPackHost(f.harness, async () => {}, options), /startup aborted/);
    assert.equal(helper.closed, true);
    const before = options.calls.length;
    await assert.rejects(startRealPackHost(f.harness, async () => {}, options), /startup aborted/);
    assert.equal(options.calls.length, before);
  } finally { await f.cleanup(); }
});
