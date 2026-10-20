import { expect } from '@playwright/test';
import { execFile, spawn, type ChildProcess } from 'node:child_process';
import { chmod, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { cpus, hostname, loadavg, tmpdir } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';

const exec = promisify(execFile);
export const SAMPLE_RATE = 48_000;

async function stop(child: ChildProcess) {
  if (!child.pid || child.exitCode !== null || child.signalCode !== null) return;
  const exited = new Promise<void>(resolve => child.once('exit', () => resolve()));
  child.kill('SIGTERM');
  const timer = setTimeout(() => child.kill('SIGKILL'), 3000);
  try { await exited; } finally { clearTimeout(timer); }
}

export async function privateMonitor() {
  // Snapshot checkout names can exceed the Unix socket path limit.
  const directory = await mkdtemp(join(tmpdir(), 'player-pulse-'));
  await chmod(directory, 0o700);
  const env = {
    ...process.env,
    XDG_RUNTIME_DIR: directory, PULSE_RUNTIME_PATH: directory, PULSE_STATE_PATH: directory,
    PULSE_SERVER: `unix:${directory}/native`, PULSE_SINK: 'player',
  };
  // No default.pa, hardware detection, system daemon, shared socket or state.
  const daemon = spawn('pulseaudio', [
    '-n', '--daemonize=no', '--use-pid-file=no', '--exit-idle-time=-1', '--log-target=stderr',
    `--load=module-native-protocol-unix socket=${directory}/native auth-anonymous=1 auth-cookie-enabled=0`,
    '--load=module-null-sink sink_name=player rate=48000 channels=2 channel_map=front-left,front-right',
  ], { env, stdio: ['ignore', 'ignore', 'pipe'] });
  let daemonLog = '';
  daemon.stderr.on('data', bytes => { daemonLog += bytes.toString(); });
  const inspect = async () => ({
    epochMs: Date.now(),
    sinks: (await exec('pactl', ['list', 'short', 'sinks'], { env })).stdout,
    inputs: (await exec('pactl', ['list', 'short', 'sink-inputs'], { env })).stdout,
    outputs: (await exec('pactl', ['list', 'short', 'source-outputs'], { env })).stdout,
  });
  try {
    await expect.poll(async () => {
      if (daemon.exitCode !== null) throw new Error(daemonLog);
      try { return (await exec('pactl', ['list', 'short', 'sinks'], { env })).stdout; } catch { return ''; }
    }, { timeout: 10_000 }).toContain('player');
    return {
      directory, env, inspect,
      async drain(diagnosticsPath: string, browserCpu: () => Promise<unknown>) {
        // Consume this invocation's monitor, never write audio
        // to its sink. Leave the ordinary WAV recorder and Pulse defaults alone.
        const structured = async () => {
          const [sinks, sources, inputs, outputs] = await Promise.all(
            ['sinks', 'sources', 'sink-inputs', 'source-outputs'].map(async kind =>
              JSON.parse((await exec('pactl', ['--format=json', 'list', kind], { env })).stdout)),
          );
          return { epochMs: Date.now(), sinks, sources, inputs, outputs };
        };
        const beforeConsumer = await structured();
        const ticksPerSecond = Number((await exec('getconf', ['CLK_TCK'])).stdout);
        const processStart = (await exec('ps', ['-eo', 'pid,ppid,comm,pcpu,cputimes', '--sort=-pcpu'])).stdout;
        const args = [
          '-hide_banner', '-nostdin', '-stats_period', '0.1', '-progress', 'pipe:1',
          '-f', 'pulse', '-sample_rate', String(SAMPLE_RATE), '-channels', '2',
          '-i', 'player.monitor', '-f', 'null', '-',
        ];
        const spawnedAtMs = Date.now();
        const consumer = spawn('ffmpeg', args, { env, stdio: ['ignore', 'pipe', 'pipe'] });
        let log = ''; let progress = ''; let spawnError: Error | undefined;
        consumer.stderr.on('data', bytes => { log += bytes.toString(); });
        consumer.stdout.on('data', bytes => { progress += bytes.toString(); });
        consumer.on('error', error => { spawnError = error; });
        const assertActive = () => {
          if (spawnError || consumer.exitCode !== null || consumer.signalCode !== null) {
            throw new Error(`Monitor consumer stopped: ${spawnError ?? consumer.exitCode ?? consumer.signalCode}\n${log}`);
          }
        };
        const telemetryErrors: string[] = [];
        const deadline = setTimeout(() => {
          void close().catch(error => { telemetryErrors.push(`deadline cleanup: ${String(error)}`); });
        }, 120_000);
        const samples: unknown[] = [];
        const snapshots: unknown[] = [];
        const inspectSafely = async <T>(name: string, operation: Promise<T>): Promise<T | null> => {
          try { return await operation; } catch (error) {
            telemetryErrors.push(`${name}: ${String(error)}`);
            return null;
          }
        };
        const sample = async () => {
          const [host, pulse, ffmpegConsumer, browser] = await Promise.all([
            inspectSafely('host', readFile('/proc/stat', 'utf8')),
            inspectSafely('pulse', readFile(`/proc/${daemon.pid}/stat`, 'utf8')),
            readFile(`/proc/${consumer.pid}/stat`, 'utf8').catch(() => null),
            inspectSafely('browser', browserCpu()),
          ]);
          samples.push({ epochMs: Date.now(), load: loadavg(), host: host?.split('\n')[0], pulse, ffmpegConsumer, browser });
        };
        let sampling = true;
        const samplingDone = (async () => {
          while (sampling) {
            await sample();
            if (sampling) await new Promise(resolve => setTimeout(resolve, 500));
          }
        })();
        void samplingDone.catch(() => {});
        const snapshot = async (stage: string) => {
          assertActive();
          const state = await structured();
          snapshots.push({ stage, ...state });
          const source = state.sources.find((source: { name: string }) => source.name === 'player.monitor');
          const output = state.outputs.find((output: { properties: Record<string, string> }) =>
            output.properties['application.process.id'] === String(consumer.pid));
          expect(source, 'same private player.monitor source').toBeDefined();
          expect(output, 'consumer owns a Pulse source output').toBeDefined();
          expect(output.source).toBe(source.index);
          expect(output.corked).toBe(false);
          expect(state.inputs.some((input: { properties: Record<string, string> }) =>
            input.properties['application.process.id'] === String(consumer.pid)), 'consumer contributes no sink input').toBe(false);
          assertActive();
        };
        let closing: Promise<unknown> | undefined;
        const close = () => closing ??= (async () => {
          clearTimeout(deadline);
          sampling = false;
          await inspectSafely('stop consumer', stop(consumer));
          await inspectSafely('sampling', samplingDone);
          await inspectSafely('final sample', sample());
          const afterConsumer = await inspectSafely('after consumer', structured());
          const diagnostics = {
            pid: consumer.pid, args, spawnedAtMs, completedAtMs: Date.now(), ticksPerSecond,
            beforeConsumer, snapshots, afterConsumer, samples, processStart,
            processEnd: (await inspectSafely('process end', exec('ps', ['-eo', 'pid,ppid,comm,pcpu,cputimes', '--sort=-pcpu'])))?.stdout,
            exitCode: consumer.exitCode, signalCode: consumer.signalCode, log, progress, daemonLog, telemetryErrors,
          };
          await writeFile(diagnosticsPath, JSON.stringify(diagnostics, null, 2));
          expect(consumer.exitCode !== null || consumer.signalCode !== null || !consumer.pid, 'consumer process terminated').toBe(true);
          expect(afterConsumer, 'consumer cleanup inspection available').not.toBeNull();
          expect(afterConsumer?.outputs.some((output: { properties: Record<string, string> }) =>
            output.properties['application.process.id'] === String(consumer.pid)), 'consumer source output cleaned up').toBe(false);
          return diagnostics;
        })();
        try {
          await expect.poll(() => {
            assertActive();
            return log.includes('Output #0') && [...progress.matchAll(/out_time_us=(\d+)/g)].some(match => Number(match[1]) > 0);
          }, { timeout: 10_000 }).toBe(true);
          await snapshot('ready-before-warm');
          return { snapshot, close };
        } catch (error) {
          await close().catch(cleanupError => { console.error('MONITOR_CONSUMER_CLEANUP', cleanupError); });
          throw error;
        }
      },
      async record(path: string, play: () => Promise<void>, gain = 1, browserCpu: () => Promise<unknown> = async () => null) {
        // This live monitor belongs to one browser only. Its recorder gain
        // plants a defect after Player mixing, without changing any inputs.
        let log = '';
        const spawnedAtMs = Date.now();
        let outputDeclaredAtMs: number | undefined;
        const recorder = spawn('ffmpeg', [
          '-hide_banner', '-y', '-f', 'pulse', '-sample_rate', String(SAMPLE_RATE), '-channels', '2',
          '-i', 'player.monitor', '-af', `volume=${gain},atrim=end_sample=288000`, '-c:a', 'pcm_s16le', path,
        ], { env, stdio: ['pipe', 'ignore', 'pipe'] });
        const deadline = setTimeout(() => recorder.kill('SIGTERM'), 15_000);
        recorder.stderr.on('data', bytes => {
          log += bytes.toString();
          if (!outputDeclaredAtMs && log.includes('Output #0')) outputDeclaredAtMs = Date.now();
        });
        const completed = new Promise<void>((resolve, reject) => {
          recorder.once('error', reject);
          recorder.once('exit', code => code === 0 ? resolve() : reject(new Error(`ffmpeg ${code}: ${log}`)));
        });
        // Attach the rejection handler before readiness polling.
        void completed.catch(() => {});
        const samples: unknown[] = [];
        const sample = async () => {
          const [host, pulse, ffmpeg, browser] = await Promise.all([
            readFile('/proc/stat', 'utf8'),
            readFile(`/proc/${daemon.pid}/stat`, 'utf8').catch(() => null),
            readFile(`/proc/${recorder.pid}/stat`, 'utf8').catch(() => null),
            browserCpu(),
          ]);
          samples.push({ epochMs: Date.now(), load: loadavg(), host: host.split('\n')[0], pulse, ffmpeg, browser });
        };
        const processStart = (await exec('ps', ['-eo', 'pid,ppid,comm,pcpu,cputimes', '--sort=-pcpu'])).stdout;
        const ticksPerSecond = Number((await exec('getconf', ['CLK_TCK'])).stdout);
        let sampling = true;
        const samplingDone = (async () => {
          while (sampling) {
            await sample();
            if (sampling) await new Promise(resolve => setTimeout(resolve, 500));
          }
        })();
        void samplingDone.catch(() => {});
        let audioBeforePlay: Awaited<ReturnType<typeof inspect>> | undefined;
        let playRequestedAtMs: number | undefined;
        let playCompletedAtMs: number | undefined;
        try {
          await expect.poll(() => log, { timeout: 10_000 }).toContain('Output #0');
          audioBeforePlay = await inspect();
          playRequestedAtMs = Date.now();
          await play();
          playCompletedAtMs = Date.now();
          await completed;
          expect(log).not.toMatch(/corrupt|non.monoton|overrun|underrun|dropp/i);
        } finally {
          clearTimeout(deadline);
          sampling = false;
          await stop(recorder);
          await samplingDone;
          await sample();
          const processEnd = (await exec('ps', ['-eo', 'pid,ppid,comm,pcpu,cputimes', '--sort=-pcpu'])).stdout;
          // Keep raw clocks/logs even on errors; Pulse's input timestamp is not
          // assumed to be a calibrated physical output latency.
          const diagnostics = {
            hostname: hostname(), cpuCount: cpus().length, ticksPerSecond,
            spawnedAtMs, outputDeclaredAtMs, playRequestedAtMs, playCompletedAtMs, audioBeforePlay,
            completedAtMs: Date.now(), pulseInputStartSeconds: Number(log.match(/start: ([\d.]+)/)?.[1]),
            processStart, processEnd, samples, recorderLog: log, daemonLog,
          };
          await writeFile(`${path}.diagnostics.json`, JSON.stringify(diagnostics, null, 2));
        }
      },
      async close() {
        await stop(daemon);
        await rm(directory, { recursive: true, force: true });
      },
    };
  } catch (error) {
    await stop(daemon);
    await rm(directory, { recursive: true, force: true });
    throw new Error(`Private Pulse startup failed: ${error instanceof Error ? error.message : String(error)}\n${daemonLog}`);
  }
}

export async function decodeMonitor(path: string) {
  const { stdout } = await exec('ffprobe', ['-v', 'error', '-show_streams', '-of', 'json', path]);
  const probe = JSON.parse(stdout).streams;
  expect(probe).toHaveLength(1);
  expect(probe[0]).toMatchObject({ codec_name: 'pcm_s16le', sample_rate: String(SAMPLE_RATE), channels: 2 });
  const { stdout: raw } = await exec('ffmpeg', ['-v', 'error', '-i', path, '-map', '0:a:0', '-f', 's16le', 'pipe:1'], { encoding: 'buffer', maxBuffer: 4 * 1024 * 1024 });
  expect(raw.length % 4).toBe(0);
  expect(raw.length / 4).toBe(6 * SAMPLE_RATE);
  const pcm = new Int16Array(raw.buffer, raw.byteOffset, raw.length / 2);
  return monitorSamples(pcm);
}

export function monitorSamples(pcm: Int16Array) {
  return {
    pcm,
    sampleCount: pcm.length / 2,
    rms(start = 0, end = 6, channel = 0) {
      let sum = 0;
      const first = Math.floor(start * SAMPLE_RATE);
      const last = Math.min(pcm.length / 2, Math.floor(end * SAMPLE_RATE));
      for (let sample = first; sample < last; sample++) sum += (pcm[sample * 2 + channel] / 32768) ** 2;
      return Math.sqrt(sum / (last - first));
    },
    spectrum(frequency: number, start: number, end: number, channel = 0) {
      let sin = 0; let cos = 0;
      const first = Math.floor(start * SAMPLE_RATE);
      const last = Math.floor(end * SAMPLE_RATE);
      for (let sample = first; sample < last; sample++) {
        const phase = 2 * Math.PI * frequency * sample / SAMPLE_RATE;
        const value = pcm[sample * 2 + channel] / 32768;
        sin += value * Math.sin(phase); cos += value * Math.cos(phase);
      }
      return { amplitude: 2 * Math.hypot(sin, cos) / (last - first), phase: Math.atan2(sin, cos) };
    },
  };
}

export function audibleEdges(capture: ReturnType<typeof monitorSamples>) {
  const active: number[] = [];
  for (let step = 0; step < 300; step++) {
    if (capture.rms(step * 0.02, (step + 1) * 0.02) > 0.004) active.push(step);
  }
  return { active, onset: active[0] * 0.02, offset: (active.at(-1)! + 1) * 0.02 };
}

export function requireAudibleDuration(duration: number, check: typeof expect.soft = expect) {
  check(duration, 'three-second live media duration').toBeGreaterThan(2.88);
  check(duration).toBeLessThan(3.12);
}
