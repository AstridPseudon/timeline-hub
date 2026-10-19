import { expect } from '@playwright/test';
import { execFile, spawn, type ChildProcess } from 'node:child_process';
import { chmod, mkdtemp, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { promisify } from 'node:util';

const exec = promisify(execFile);
export const SAMPLE_RATE = 48_000;

async function stop(child: ChildProcess) {
  if (child.exitCode !== null || child.signalCode !== null) return;
  const exited = new Promise<void>(resolve => child.once('exit', () => resolve()));
  child.kill('SIGTERM');
  const timer = setTimeout(() => child.kill('SIGKILL'), 3000);
  try { await exited; } finally { clearTimeout(timer); }
}

export async function privateMonitor() {
  const directory = await mkdtemp(join(process.cwd(), '.player-pulse-'));
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
  try {
    await expect.poll(async () => {
      if (daemon.exitCode !== null) throw new Error(daemonLog);
      try { return (await exec('pactl', ['list', 'short', 'sinks'], { env })).stdout; } catch { return ''; }
    }, { timeout: 10_000 }).toContain('player');
    return {
      directory, env,
      async record(path: string, play: () => Promise<void>, gain = 1) {
        // This live monitor belongs to one browser only. Its recorder gain
        // plants a defect after Player mixing, without changing any inputs.
        let log = '';
        const recorder = spawn('ffmpeg', [
          '-hide_banner', '-y', '-f', 'pulse', '-sample_rate', String(SAMPLE_RATE), '-channels', '2',
          '-i', 'player.monitor', '-af', `volume=${gain},atrim=end_sample=288000`, '-c:a', 'pcm_s16le', path,
        ], { env, stdio: ['pipe', 'ignore', 'pipe'] });
        const deadline = setTimeout(() => recorder.kill('SIGTERM'), 15_000);
        recorder.stderr.on('data', bytes => { log += bytes.toString(); });
        const completed = new Promise<void>((resolve, reject) => {
          recorder.once('error', reject);
          recorder.once('exit', code => code === 0 ? resolve() : reject(new Error(`ffmpeg ${code}: ${log}`)));
        });
        // Attach the rejection handler before readiness polling.
        void completed.catch(() => {});
        try {
          await expect.poll(() => log, { timeout: 10_000 }).toContain('Output #0');
          await play();
          await completed;
          expect(log).not.toMatch(/corrupt|non.monoton|overrun|underrun|dropp/i);
        } finally { clearTimeout(deadline); await stop(recorder); }
      },
      async close() {
        await stop(daemon);
        await rm(directory, { recursive: true, force: true });
      },
    };
  } catch (error) {
    await stop(daemon);
    await rm(directory, { recursive: true, force: true });
    throw error;
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
