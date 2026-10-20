import { expect, test as base } from '@playwright/test';
import { createServer, type Server } from 'node:http';
import { execFile, spawn, type ChildProcess } from 'node:child_process';
import { chmod, mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';
import {
  assertCaptureCapabilities,
  assertRawPts,
  assertStereoTones,
  CONTROLLED_AUDIO,
  createSyntheticPcmWav,
  nativeAudioChannelDiagnostic,
} from './tab-audio-capture.analysis.mjs';

const exec = promisify(execFile);
const CAPTURE_MS = 4_000;
const SAMPLE_RATE = 48_000;

declare global {
  interface Window {
    __privatePulseProbe: {
      mimeType: string;
      tracks: Array<{ kind: string; readyState: string; settings: MediaTrackSettings; capabilities: MediaTrackCapabilities }>;
      chunks: string[];
      fixture: { leftFrequency: number; rightFrequency: number; sampleRate: number };
    };
  }
}

async function stopOwned(child: ChildProcess) {
  if (!child.pid || child.exitCode !== null || child.signalCode !== null) return;
  const exited = new Promise<void>((resolve) => child.once('exit', () => resolve()));
  child.kill('SIGTERM');
  const timer = setTimeout(() => child.kill('SIGKILL'), 3_000);
  try { await exited; } finally { clearTimeout(timer); }
}

async function privatePulse() {
  if (process.getuid?.() === 0) throw new Error('Root/system mode is forbidden for the private Pulse diagnostic');
  const directory = await mkdtemp(join(tmpdir(), 'timeline-private-pulse-'));
  await chmod(directory, 0o700);
  const inherited = {...process.env};
  for (const key of ['PULSE_SERVER', 'PULSE_SINK', 'PULSE_RUNTIME_PATH', 'PULSE_STATE_PATH', 'PULSE_COOKIE']) delete inherited[key];
  const env: NodeJS.ProcessEnv = {
    ...inherited,
    XDG_RUNTIME_DIR: directory,
    PULSE_RUNTIME_PATH: directory,
    PULSE_STATE_PATH: directory,
    PULSE_SERVER: `unix:${directory}/native`,
    PULSE_SINK: 'player',
  };
  const daemon = spawn('pulseaudio', [
    '-n', '--daemonize=no', '--use-pid-file=no', '--exit-idle-time=-1', '--log-target=stderr',
    `--load=module-native-protocol-unix socket=${directory}/native auth-anonymous=1 auth-cookie-enabled=0`,
    '--load=module-null-sink sink_name=player rate=48000 channels=2 format=float32le channel_map=front-left,front-right',
  ], { env, stdio: ['ignore', 'ignore', 'pipe'] });
  let daemonLog = '';
  daemon.stderr.on('data', (bytes) => { daemonLog += bytes.toString(); });
  const inspect = async () => {
    const [sinks, sources, inputs, outputs] = await Promise.all(
      ['sinks', 'sources', 'sink-inputs', 'source-outputs'].map(async (kind) =>
        JSON.parse((await exec('pactl', ['--format=json', 'list', kind], { env })).stdout)),
    );
    return { epochMs: Date.now(), sinks, sources, inputs, outputs };
  };
  try {
    await expect.poll(async () => {
      if (daemon.exitCode !== null) throw new Error(daemonLog);
      try { return (await exec('pactl', ['list', 'short', 'sinks'], { env })).stdout; } catch { return ''; }
    }, { timeout: 10_000 }).toContain('player');
    return {
      env,
      async record(path: string, play: () => Promise<void>) {
        const beforeWarm = await inspect();
        let log = '';
        const recorder = spawn('ffmpeg', [
          '-hide_banner', '-y', '-f', 'pulse', '-sample_rate', String(SAMPLE_RATE), '-channels', '2',
          '-i', 'player.monitor', '-c:a', 'pcm_f32le', path,
        ], { env, stdio: ['ignore', 'ignore', 'pipe'] });
        recorder.stderr.on('data', (bytes) => { log += bytes.toString(); });
        const completed = new Promise<void>((resolve, reject) => {
          recorder.once('error', reject);
          recorder.once('exit', (code, signal) => code === 0 ? resolve() : reject(new Error(`ffmpeg ${code ?? signal}: ${log}`)));
        });
        void completed.catch(() => {});
        try {
          await expect.poll(() => log, { timeout: 10_000 }).toContain('Output #0');
          await play();
          await new Promise((resolve) => setTimeout(resolve, CAPTURE_MS));
        } finally {
          await stopOwned(recorder);
          await completed.catch(() => {});
          await writeFile(`${path}.diagnostics.json`, JSON.stringify({
            beforeWarm,
            recorderPid: recorder.pid,
            recorderLog: log,
            daemonLog,
            completedAtMs: Date.now(),
          }, null, 2));
        }
        return { beforeWarm, recorderLog: log };
      },
      async close() {
        await stopOwned(daemon);
        await rm(directory, { recursive: true, force: true });
      },
    };
  } catch (error) {
    await stopOwned(daemon);
    await rm(directory, { recursive: true, force: true });
    throw new Error(`Private Pulse startup failed: ${error instanceof Error ? error.message : String(error)}\n${daemonLog}`);
  }
}

function probeHtml() {
  const webFrequency = JSON.stringify(CONTROLLED_AUDIO.webAudioFrequency);
  const webAmplitude = JSON.stringify(CONTROLLED_AUDIO.webAudioAmplitude);
  return `<!doctype html><button id="start">Start</button>
<audio id="fixture" preload="auto" src="/synthetic.wav"></audio>
<div id="state">PRE-WARM</div><script>
const button=document.querySelector('#start'); const fixture=document.querySelector('#fixture');
button.addEventListener('click',()=>void (async()=>{let stream,audio,osc,recorder; try {
stream=await navigator.mediaDevices.getDisplayMedia({video:true,audio:true,preferCurrentTab:true});
const mimeType='video/webm;codecs=vp8,opus'; if(!MediaRecorder.isTypeSupported(mimeType)) throw new Error('unsupported recorder MIME');
recorder=new MediaRecorder(stream,{mimeType}); audio=new AudioContext(); await audio.resume();
osc=audio.createOscillator(); const gain=audio.createGain(); gain.gain.value=${webAmplitude}; osc.frequency.value=${webFrequency}; osc.connect(gain).connect(audio.destination);
window.__privatePulseProbe={mimeType,tracks:stream.getTracks().map(track=>({kind:track.kind,readyState:track.readyState,settings:track.getSettings(),capabilities:track.getCapabilities()})),chunks:[],fixture:{leftFrequency:${CONTROLLED_AUDIO.leftFrequency},rightFrequency:${CONTROLLED_AUDIO.rightFrequency},sampleRate:${SAMPLE_RATE}}};
const chunks=[]; let chunkIndex=0; let delivery=Promise.resolve();
recorder.ondataavailable=event=>{const index=chunkIndex++; delivery=delivery.then(async()=>{if(event.data.size) chunks[index]=new Uint8Array(await event.data.arrayBuffer());});};
const stopped=new Promise((resolve,reject)=>{recorder.addEventListener('stop',resolve,{once:true}); recorder.addEventListener('error',()=>reject(new Error('MediaRecorder error')),{once:true});});
await fixture.play(); recorder.start(100); osc.start(); document.querySelector('#state').textContent='WARMED'; await new Promise(resolve=>setTimeout(resolve,${CAPTURE_MS})); osc.stop(); recorder.stop(); await stopped; await delivery;
window.__privatePulseProbe.chunks=chunks.filter(Boolean).map(bytes=>{let binary=''; for(const byte of bytes) binary+=String.fromCharCode(byte); return btoa(binary);}); button.dataset.result='complete';
}catch(error){button.dataset.error=error instanceof Error?error.message:String(error); button.dataset.result='error';}finally{if(audio) await audio.close(); if(stream) stream.getTracks().forEach(track=>track.stop());}})(),{once:true});
</script>`;
}

function fixtureServer(): Server {
  const html = Buffer.from(probeHtml());
  const wav = createSyntheticPcmWav({ leftFrequency: CONTROLLED_AUDIO.leftFrequency, rightFrequency: CONTROLLED_AUDIO.rightFrequency });
  return createServer((request, response) => {
    if (request.url === '/') { response.writeHead(200, {'content-type': 'text/html'}); response.end(html); return; }
    if (request.url === '/synthetic.wav') { response.writeHead(200, {'content-type': 'audio/wav', 'content-length': wav.length}); response.end(wav); return; }
    response.writeHead(404); response.end();
  });
}

function listen(server: Server) {
  return new Promise<void>((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', () => resolve()); });
}

async function closeServer(server: Server) {
  server.closeAllConnections();
  await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
}

async function ffprobe(path: string) {
  const { stdout } = await exec('ffprobe', ['-v', 'error', '-show_streams', '-show_packets', '-of', 'json', path]);
  return JSON.parse(stdout) as { streams: Array<Record<string, unknown>>; packets: Array<Record<string, unknown>> };
}

async function decodeFloat(path: string, streamIndex: number) {
  const { stdout } = await exec('ffmpeg', ['-v', 'error', '-i', path, '-map', `0:${streamIndex}`, '-f', 'f32le', 'pipe:1'], { encoding: 'buffer' });
  if (stdout.length % Float32Array.BYTES_PER_ELEMENT) throw new Error('PCM output is not float32-aligned');
  return new Float32Array(stdout.buffer, stdout.byteOffset, stdout.length / Float32Array.BYTES_PER_ELEMENT);
}

async function recordChannels(path: string, frequency: { left: number; right: number }) {
  const probe = await ffprobe(path);
  const stream = probe.streams.find((item) => item.codec_type === 'audio');
  if (!stream) throw new Error('Missing audio stream');
  const diagnostic = nativeAudioChannelDiagnostic(stream.channels);
  if (diagnostic.status !== 'supported') return { diagnostic, stereo: false };
  const samples = await decodeFloat(path, Number(stream.index));
  return { diagnostic, stereo: assertStereoTones(samples, {
    sampleRate: Number(stream.sample_rate), channels: Number(stream.channels),
    leftFrequency: frequency.left, rightFrequency: frequency.right,
  }) };
}

type Fixtures = { url: string; pulse: Awaited<ReturnType<typeof privatePulse>> };
const test = base.extend<Fixtures>({
  // This fixture starts only in the centrally granted run; offline collection never imports Playwright.
  // eslint-disable-next-line no-empty-pattern
  pulse: [async ({}, use) => { const pulse = await privatePulse(); try { await use(pulse); } finally { await pulse.close(); } }, { scope: 'worker' }],
  url: [async ({ pulse: _pulse }, use) => {
    const server = fixtureServer(); await listen(server);
    try { const address = server.address(); if (!address || typeof address === 'string') throw new Error('fixture server address missing'); await use(`http://127.0.0.1:${address.port}/`); }
    finally { await closeServer(server); }
  }, { scope: 'worker' }],
  browser: [async ({ playwright, launchOptions, pulse }, use) => {
    const browser = await playwright.chromium.launch({ ...launchOptions, env: pulse.env });
    try { await use(browser); } finally { await browser.close(); }
  }, { scope: 'worker' }],
});

test('records native private Pulse monitor before warm and preserves GDM channel refusal', async ({ page, url, pulse }, testInfo) => {
  test.setTimeout(120_000);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  const monitorPath = testInfo.outputPath('private-pulse-monitor.wav');
  const monitor = await pulse.record(monitorPath, async () => {
    await page.locator('#start').click();
    await expect(page.locator('#start')).toHaveAttribute('data-result', 'complete', { timeout: 20_000 });
  });
  const probe = await page.evaluate(() => window.__privatePulseProbe);
  const chunks = probe.chunks.map((chunk) => Buffer.from(chunk, 'base64'));
  const muxPath = testInfo.outputPath('private-pulse-gdm.webm');
  await mkdir(testInfo.outputDir, { recursive: true }); await writeFile(muxPath, Buffer.concat(chunks));
  const capabilities = assertCaptureCapabilities(probe.tracks, { mimeType: probe.mimeType });
  const muxProbe = await ffprobe(muxPath); const rawPts = assertRawPts(muxProbe);
  const muxAudio = muxProbe.streams.find((item) => item.codec_type === 'audio');
  if (!muxAudio) throw new Error('GDM mux has no audio stream');
  const gdm = nativeAudioChannelDiagnostic(muxAudio.channels);
  const gdmStereo = gdm.status === 'supported' ? await recordChannels(muxPath, { left: CONTROLLED_AUDIO.leftFrequency, right: CONTROLLED_AUDIO.rightFrequency }) : null;
  const monitorStereo = await recordChannels(monitorPath, { left: CONTROLLED_AUDIO.leftFrequency, right: CONTROLLED_AUDIO.rightFrequency });
  await testInfo.attach('private-pulse-stereo-result', { body: JSON.stringify({
    requested: { video: true, audio: true, preferCurrentTab: true },
    beforeWarm: monitor.beforeWarm,
    gdm: { capabilities, rawPts, channelDiagnostic: gdm, stereo: gdmStereo, retainedMux: gdm.status === 'supported' },
    separatePulseMonitor: monitorStereo,
    honestBoundary: gdm.status === 'supported' ? 'GDM mux stereo detector is eligible for review' : 'GDM remained mono; separate Pulse monitor channel capability only',
    claimsExcluded: ['Player parity', 'export parity', 'A/V phase', 'per-clip alignment', 'upmix/downmix', 'codec conversion', 'threshold changes'],
  }, null, 2), contentType: 'application/json' });
  expect(monitor.beforeWarm.inputs.some((input: {properties?: Record<string, string>}) => input.properties?.['application.process.id'])).toBe(false);
});
