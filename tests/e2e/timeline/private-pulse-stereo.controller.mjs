import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// This controller is intentionally offline. It validates the selected App
// source and toolchain, but never starts PulseAudio, Chrome, ffmpeg, or a
// socket. The central launcher is the only place allowed to run the probe.
export const APP_ROOT = resolve(process.env.TAB_AUDIO_APP_ROOT ?? '/home/user/work/wt/vw-m3-stereo-owned-state-guard-fix');
export const BASE_CONTROLLER = join(APP_ROOT, 'tests/e2e/timeline/tab-audio-capture.controller.mjs');
const HANDOFF_SOURCE = join(dirname(fileURLToPath(import.meta.url)), 'handoff-vw-m3-private-pulse-stereo-prep-private-pulse-stereo.probe.ts');
const APP_SOURCE = join(APP_ROOT, 'tests/e2e/timeline/private-pulse-stereo.probe.ts');
export const PROBE_SOURCE = existsSync(APP_SOURCE) ? APP_SOURCE : HANDOFF_SOURCE;
export const RUN_MODE = 'stereo';
export const TOOL_NAMES = Object.freeze(['pulseaudio', 'pactl', 'ffmpeg', 'ffprobe']);

function command(name, args) {
  return execFileSync(name, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

export function installedTools() {
  return Object.fromEntries(TOOL_NAMES.map((name) => [name, {
    path: command('which', [name]),
    version: command(name, name === 'pulseaudio' || name === 'pactl' ? ['--version'] : ['-version']).split('\n')[0],
  }]));
}

function assertOffline() {
  if (process.env.TAB_AUDIO_RUN === '1') throw new Error('This preparation controller cannot run the actual capture');
  if (!existsSync(BASE_CONTROLLER)) throw new Error(`Missing proven tab controller: ${BASE_CONTROLLER}`);
  if (!existsSync(PROBE_SOURCE)) throw new Error(`Missing fallback probe source: ${PROBE_SOURCE}`);
  const source = readFileSync(PROBE_SOURCE, 'utf8');
  for (const required of ['finally', 'module-null-sink', 'PULSE_SERVER', 'PULSE_SINK', 'pcm_f32le', 'player.monitor']) {
    if (!source.includes(required)) throw new Error(`Fallback source lost required lifecycle/control: ${required}`);
  }
  for (const forbidden of ['--system', 'set-default-sink', 'PULSE_DEFAULT', "'-ac'", 'aresample', 'pan=']) {
    if (source.includes(forbidden)) throw new Error(`Fallback source contains forbidden coercion/global audio operation: ${forbidden}`);
  }
}

export function prepare() {
  assertOffline();
  const tools = installedTools();
  const base = command('git', ['-C', APP_ROOT, 'rev-parse', 'HEAD']);
  return {
    status: 'READY_FOR_MANAGER_REVIEW',
    runMode: RUN_MODE,
    appRoot: APP_ROOT,
    baseController: BASE_CONTROLLER,
    sourceSha: base,
    tools,
    note: 'Run the proven tab controller fingerprint/preflight in the App worktree; this controller adds only the private-tool and lifecycle checks.',
  };
}

export function preflight() {
  const output = process.env.TAB_AUDIO_PREFLIGHT_PATH;
  if (!output) throw new Error('TAB_AUDIO_PREFLIGHT_PATH is required for offline preflight');
  const result = {...prepare(), status: 'READY_OFFLINE_PREFLIGHT', preflightPath: output};
  writeFileSync(output, JSON.stringify(result, null, 2), { flag: 'wx' });
  return result;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const action = process.argv[2] ?? '--prepare';
  const result = action === '--prepare' ? prepare() : action === '--preflight' ? preflight() : (() => { throw new Error(`Unknown action: ${action}`); })();
  console.log(JSON.stringify(result, null, 2));
}
