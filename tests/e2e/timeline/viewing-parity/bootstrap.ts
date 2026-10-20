import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { stat } from 'node:fs/promises';
import { delimiter, isAbsolute, join } from 'node:path';
import type { DirectHarness } from '../../local/support/harness';

export interface PackHostSession {
  stop(): Promise<void>;
}

interface BootstrapOptions {
  env?: NodeJS.ProcessEnv;
  spawn?: typeof spawn;
  signal?: AbortSignal;
  startupTimeoutMs?: number;
  stopTimeoutMs?: number;
}

/** Requires an owner-approved helper in the parent's frozen ASTRID_CHECKOUT.
 * The Agent owns launch authority and host cleanup, including SIGTERM cleanup.
 * This adapter owns only its direct helper child, never a reported host PID.
 */
export async function startRealPackHost(
  harness: Pick<DirectHarness, 'tmp' | 'realmDir' | 'supportDir' | 'runtimeInstanceId' | 'runtimeEnv'>,
  checkReady: () => Promise<unknown>,
  options: BootstrapOptions = {},
): Promise<PackHostSession> {
  const env = { ...(options.env ?? process.env), ...harness.runtimeEnv() };
  const source = env.ASTRID_CHECKOUT;
  const python = env.ASTRID_PYTHON;
  if (!source || !isAbsolute(source) || !python || !isAbsolute(python)) {
    throw new Error('Pack-host bootstrap requires frozen absolute ASTRID_CHECKOUT and ASTRID_PYTHON');
  }
  const helper = join(source, 'tests/packs/rendering/real_pack_host.py');
  if (!(await stat(helper).catch(() => null))?.isFile()) {
    throw new Error('Approved Agent pack-host helper is absent from frozen ASTRID_CHECKOUT');
  }
  if (options.signal?.aborted) throw new Error('Pack-host startup aborted');
  env.PYTHONPATH = [source, env.PYTHONPATH].filter(Boolean).join(delimiter);
  const startupDeadline = performance.now() + (options.startupTimeoutMs ?? 210_000);
  let child: ChildProcessWithoutNullStreams;
  try {
    child = (options.spawn ?? spawn)(python, ['-m', 'tests.packs.rendering.real_pack_host',
      '--realm-dir', harness.realmDir, '--support-dir', harness.supportDir,
      '--discovery-file', join(harness.supportDir, 'discovery.json'),
      '--source-checkout', source, '--runtime-instance-id', harness.runtimeInstanceId,
    ], { cwd: source, env, stdio: 'pipe', detached: false }) as ChildProcessWithoutNullStreams;
  } catch {
    throw new Error('Pack-host helper could not be spawned');
  }

  const stopTimeout = options.stopTimeoutMs ?? 30_000;
  const changed = new Set<() => void>();
  const notify = () => { for (const wake of changed) wake(); };
  let failure: Error | undefined;
  let protocolFailure = false;
  let ready = false;
  let stopped = false;
  let closed = false;
  let exitCode: number | null = null;
  let hostPid: number | undefined;
  let buffer = '';
  let bytes = 0;
  let stopping: Promise<void> | undefined;
  const fail = (message: string, protocol = true) => {
    failure ??= new Error(message);
    protocolFailure ||= protocol;
    notify();
  };
  const aborted = () => fail('Pack-host startup aborted', false);
  options.signal?.addEventListener('abort', aborted, { once: true });
  // Abort could have arrived between the pre-spawn check and listener setup.
  if (options.signal?.aborted) aborted();

  child.on('error', () => fail('Pack-host helper process failed'));
  child.stdin.on('error', () => fail('Pack-host helper input failed'));
  child.stdout.on('error', () => fail('Pack-host helper output failed'));
  child.stderr.on('error', () => fail('Pack-host helper diagnostics failed'));
  child.stderr.resume(); // Drain without retaining or exposing credential-bearing diagnostics.
  child.stdout.setEncoding('utf8');
  child.stdout.on('data', (chunk: string) => {
    bytes += Buffer.byteLength(chunk);
    if (bytes > 65_536) { fail('Pack-host helper output exceeded limit'); return; }
    buffer += chunk;
    let newline: number;
    while ((newline = buffer.indexOf('\n')) >= 0) {
      const line = buffer.slice(0, newline);
      buffer = buffer.slice(newline + 1);
      try {
        if (Buffer.byteLength(line) > 16_384) throw new Error();
        const value: unknown = JSON.parse(line);
        if (!value || typeof value !== 'object') throw new Error();
        const message = value as Record<string, unknown>;
        if (message.status === 'ready' && !ready && !stopped
          && Number.isSafeInteger(message.host_pid) && Number(message.host_pid) > 0
          && message.host_status === 'ready' && Array.isArray(message.host_ready_capabilities)
          && message.host_ready_capabilities.includes('rendering.render')) {
          hostPid = Number(message.host_pid);
          ready = true;
        } else if (message.status === 'stopped' && !stopped && message.host_pid === hostPid && ready) {
          stopped = true;
        } else {
          fail(message.status === 'failed' ? 'Pack-host helper reported failure' : 'Invalid pack-host helper status');
        }
      } catch {
        fail('Malformed pack-host helper output');
      }
      notify();
    }
    if (buffer.length > 16_384) fail('Pack-host helper line exceeded limit');
  });
  child.stdout.on('end', () => {
    if (buffer || !stopped) fail('Pack-host helper output ended before stopped acknowledgement');
  });
  child.once('close', (code: number | null) => {
    closed = true;
    exitCode = code;
    if (!ready) fail('Pack-host helper exited before ready');
    notify();
  });

  function waitUntil(done: () => boolean, deadline: number, label: string, checkFailure = true): Promise<void> {
    return new Promise((resolve, reject) => {
      const finish = (error?: Error) => {
        clearTimeout(timer);
        changed.delete(wake);
        if (error) reject(error); else resolve();
      };
      const wake = () => {
        if (checkFailure && failure) finish(failure);
        else if (performance.now() >= deadline) finish(new Error(label));
        else if (done()) finish();
        else if (checkFailure && closed) finish(new Error('Pack-host helper exited during startup'));
      };
      const timer = setTimeout(() => finish(new Error(label)), Math.max(0, deadline - performance.now()));
      changed.add(wake);
      wake();
    });
  }

  function stop(): Promise<void> {
    stopping ??= (async () => {
      options.signal?.removeEventListener('abort', aborted);
      if (!closed) {
        try { child.stdin.end('stop\n'); } catch { fail('Pack-host helper input failed'); }
        try {
          await waitUntil(() => closed, performance.now() + stopTimeout, 'Pack-host helper cleanup timed out', false);
        } catch {
          // Only the direct helper receives this signal. The approved Agent
          // helper must clean its owned host on SIGTERM, including during launch.
          child.kill('SIGTERM');
          await waitUntil(() => closed, performance.now() + stopTimeout, 'Pack-host helper did not exit after SIGTERM', false);
          throw new Error('Pack-host helper cleanup timed out; SIGTERM was required');
        }
      }
      if (protocolFailure || !stopped || exitCode !== 0) throw new Error('Pack-host helper cleanup failed');
    })();
    return stopping;
  }

  try {
    await waitUntil(() => ready, startupDeadline, 'Pack-host helper readiness timed out');
    let catalogReady = false;
    void Promise.resolve().then(checkReady).then(() => { catalogReady = true; notify(); },
      () => fail('Runtime rendering capability readiness check failed', false));
    await waitUntil(() => catalogReady, startupDeadline, 'Runtime rendering capability readiness timed out');
    if (stopped || closed) throw new Error('Pack-host helper stopped during startup');
    options.signal?.removeEventListener('abort', aborted);
    return { stop };
  } catch (error) {
    try { await stop(); } catch {
      throw new Error(`${(error as Error).message}; pack-host startup cleanup failed`);
    }
    throw error;
  }
}
