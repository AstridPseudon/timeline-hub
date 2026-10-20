import { expect, test as base } from '@playwright/test';
import { createServer, type Server } from 'node:http';
import { execFile } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import {
  assertCaptureCapabilities,
  assertCaptureOutcome,
  assertTone,
  CONTROLLED_AUDIO,
  createSyntheticPcmWav,
  diagnoseVisualEvent,
} from './tab-audio-capture.analysis.mjs';

const exec = promisify(execFile);
const VISUAL_EVENT_MS = 1_500;
const CAPTURE_MS = 4_000;

declare global {
  interface Window {
    __tabAudioProbe: {
      mimeType: string;
      tracks: Array<{ kind: string; readyState: string; settings: MediaTrackSettings }>;
      chunks: string[];
      fixture: {
        webAudioFrequency: number;
        htmlAudioFrequency: number;
        visualEventMs: number;
        captureMs: number;
        startedAt: number;
        visualEventAt: number;
      };
    };
  }
}

type ProbeFixtures = { fixtureUrl: string };

function probeHtml() {
  const webAudioFrequency = JSON.stringify(CONTROLLED_AUDIO.webAudioFrequency);
  const webAudioAmplitude = JSON.stringify(CONTROLLED_AUDIO.webAudioAmplitude);
  const htmlAudioFrequency = JSON.stringify(CONTROLLED_AUDIO.htmlAudioFrequency);
  return `<!doctype html>
<html><head><meta charset="utf-8"><title>Tab audio capability probe</title></head>
<body style="margin:0;background:#101820;color:white;font:16px sans-serif">
  <button id="tab-audio-probe-start" type="button">Start tab-audio probe</button>
  <audio id="tab-audio-probe-wav" preload="auto" src="/synthetic.wav"></audio>
  <div id="tab-audio-probe-marker" style="position:fixed;right:8px;bottom:8px;background:#203040;color:white;padding:18px;font:24px monospace">
    TAB-AUDIO-PROBE: PRE-EVENT
  </div>
  <script>
    const button = document.getElementById('tab-audio-probe-start');
    const marker = document.getElementById('tab-audio-probe-marker');
    const htmlAudio = document.getElementById('tab-audio-probe-wav');
    button.addEventListener('click', () => {
      void (async () => {
        let stream;
        let audio;
        let oscillator;
        let recorder;
        try {
          stream = await navigator.mediaDevices.getDisplayMedia({
            video: true,
            audio: true,
            preferCurrentTab: true,
          });
          const mimeType = 'video/webm;codecs=vp8,opus';
          if (!MediaRecorder.isTypeSupported(mimeType)) throw new Error('Unsupported recorder MIME: ' + mimeType);
          recorder = new MediaRecorder(stream, { mimeType });
          audio = new AudioContext();
          await audio.resume();
          oscillator = audio.createOscillator();
          const gain = audio.createGain();
          gain.gain.value = ${webAudioAmplitude};
          oscillator.frequency.value = ${webAudioFrequency};
          oscillator.connect(gain).connect(audio.destination);
          const startedAt = performance.now();
          let visualEventAt = Number.NaN;
          const fixture = {
            webAudioFrequency: ${webAudioFrequency},
            htmlAudioFrequency: ${htmlAudioFrequency},
            visualEventMs: ${VISUAL_EVENT_MS},
            captureMs: ${CAPTURE_MS},
            startedAt,
            visualEventAt,
          };
          window.__tabAudioProbe = {
            mimeType,
            tracks: stream.getTracks().map((track) => ({ kind: track.kind, readyState: track.readyState, settings: track.getSettings() })),
            chunks: [],
            fixture,
          };

          // Keep each dataavailable payload in recorder order before handing it
          // to the test. This does not alter the encoded timestamps.
          const encodedChunks = [];
          let nextChunkIndex = 0;
          let delivery = Promise.resolve();
          recorder.ondataavailable = (event) => {
            const index = nextChunkIndex;
            nextChunkIndex += 1;
            delivery = delivery.then(async () => {
              if (event.data.size === 0) return;
              const bytes = new Uint8Array(await event.data.arrayBuffer());
              let binary = '';
              for (const byte of bytes) binary += String.fromCharCode(byte);
              encodedChunks[index] = btoa(binary);
            });
          };
          const recorderStopped = new Promise((resolve, reject) => {
            recorder.addEventListener('stop', () => resolve(), { once: true });
            recorder.addEventListener('error', () => reject(new Error('MediaRecorder emitted an error')), { once: true });
          });
          const animate = (now) => {
            if (Number.isNaN(visualEventAt) && now - startedAt >= ${VISUAL_EVENT_MS}) {
              visualEventAt = now;
              fixture.visualEventAt = now;
              marker.textContent = 'TAB-AUDIO-PROBE: KNOWN-VISUAL-EVENT';
              marker.style.background = '#a02020';
            }
            if (now - startedAt < ${CAPTURE_MS}) requestAnimationFrame(animate);
          };
          // Both sources start after the real user click, and share this one
          // tab MediaRecorder stream and its native per-stream PTS.
          await htmlAudio.play();
          recorder.start(100);
          oscillator.start();
          requestAnimationFrame(animate);
          await new Promise((resolve) => setTimeout(resolve, ${CAPTURE_MS}));
          oscillator.stop();
          recorder.stop();
          await recorderStopped;
          await delivery;
          window.__tabAudioProbe.chunks = encodedChunks.filter((chunk) => chunk !== undefined);
          button.dataset.result = 'complete';
        } catch (error) {
          button.dataset.error = error instanceof Error ? error.message : String(error);
          button.dataset.result = 'error';
        } finally {
          if (audio) await audio.close();
          if (stream) stream.getTracks().forEach((track) => track.stop());
        }
      })();
    }, { once: true });
  </script>
</body></html>`;
}

function startProbeServer(): Server {
  const html = Buffer.from(probeHtml());
  const wav = createSyntheticPcmWav();
  return createServer((request, response) => {
    if (request.method !== 'GET') {
      response.writeHead(405, {'content-type': 'text/plain; charset=utf-8'});
      response.end('Method Not Allowed');
    } else if (request.url === '/') {
      response.writeHead(200, {'content-type': 'text/html; charset=utf-8'});
      response.end(html);
    } else if (request.url === '/synthetic.wav') {
      response.writeHead(200, {'content-type': 'audio/wav', 'content-length': wav.length});
      response.end(wav);
    } else {
      response.writeHead(404, {'content-type': 'text/plain; charset=utf-8'});
      response.end('Not Found');
    }
  });
}

function listen(server: Server): Promise<void> {
  return new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => resolve());
  });
}

function close(server: Server): Promise<void> {
  return new Promise((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve());
  });
}

const test = base.extend<ProbeFixtures>({
  // Playwright reads fixture dependencies from the destructuring pattern; this fixture has none.
  // eslint-disable-next-line no-empty-pattern
  fixtureUrl: async ({}, provide) => {
    const server = startProbeServer();
    await listen(server);
    try {
      const address = server.address();
      if (!address || typeof address === 'string') throw new Error('Probe server did not expose an ephemeral address');
      await provide(`http://127.0.0.1:${address.port}/`);
    } finally {
      server.closeAllConnections();
      await close(server);
    }
  },
});

async function readFfprobe(path: string) {
  const { stdout } = await exec('ffprobe', [
    '-v', 'error', '-show_streams', '-show_packets', '-of', 'json', path,
  ], { maxBuffer: 32 * 1024 * 1024 });
  return JSON.parse(stdout) as { streams: unknown[]; packets: unknown[] };
}

async function readDecodedAudio(path: string, stream: { index: number }) {
  const { stdout } = await exec('ffmpeg', [
    '-v', 'error', '-i', path, '-map', `0:${stream.index}`, '-f', 'f32le', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: 32 * 1024 * 1024 });
  if (stdout.byteLength % Float32Array.BYTES_PER_ELEMENT !== 0) throw new Error('Decoded audio was not f32-aligned');
  return new Float32Array(stdout.buffer, stdout.byteOffset, stdout.byteLength / Float32Array.BYTES_PER_ELEMENT);
}

async function readVisualRegion(path: string) {
  const { stdout } = await exec('ffmpeg', [
    '-v', 'error', '-i', path, '-map', '0:v:0',
    '-vf', 'crop=500:110:940:790,format=rgb24', '-f', 'rawvideo', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: 32 * 1024 * 1024 });
  return stdout;
}

test('captures whole-tab video and tab audio in one Chrome155 MediaRecorder clock', async ({ page, fixtureUrl }, testInfo) => {
  test.setTimeout(120_000);
  await page.goto(fixtureUrl, { waitUntil: 'domcontentloaded' });
  await page.locator('#tab-audio-probe-start').click();
  await expect(page.locator('#tab-audio-probe-start')).toHaveAttribute('data-result', 'complete', { timeout: 20_000 });

  const probe = await page.evaluate(() => window.__tabAudioProbe);
  const chunks = probe.chunks.map((chunk) => Buffer.from(chunk, 'base64'));
  const capabilities = assertCaptureCapabilities(probe.tracks, { mimeType: probe.mimeType });
  expect(probe.fixture.webAudioFrequency).toBe(CONTROLLED_AUDIO.webAudioFrequency);
  expect(probe.fixture.htmlAudioFrequency).toBe(CONTROLLED_AUDIO.htmlAudioFrequency);
  expect(probe.fixture.visualEventMs).toBe(VISUAL_EVENT_MS);
  expect(Number.isFinite(probe.fixture.visualEventAt)).toBe(true);
  expect(chunks.length).toBeGreaterThan(0);

  const output = testInfo.outputPath('whole-tab.webm');
  await mkdir(testInfo.outputDir, { recursive: true });
  await writeFile(output, Buffer.concat(chunks));
  const ffprobe = await readFfprobe(output);
  const outcome = assertCaptureOutcome(ffprobe, capabilities);
  const audioStream = (ffprobe.streams as Array<{ codec_type?: string; index: number; sample_rate: string; channels: number }>)
    .find((stream) => stream.codec_type === 'audio');
  if (!audioStream) throw new Error('ffprobe output did not identify the captured audio stream');
  const decodedAudio = await readDecodedAudio(output, audioStream);
  const tones = {
    webAudio: assertTone(decodedAudio, {
      sampleRate: Number(audioStream.sample_rate),
      channels: Number(audioStream.channels),
      frequency: CONTROLLED_AUDIO.webAudioFrequency,
    }),
    htmlAudio: assertTone(decodedAudio, {
      sampleRate: Number(audioStream.sample_rate),
      channels: Number(audioStream.channels),
      frequency: CONTROLLED_AUDIO.htmlAudioFrequency,
    }),
  };
  const rawDecodedMarkerData = await readVisualRegion(output);
  const visualMarkerDiagnostic = diagnoseVisualEvent(rawDecodedMarkerData, {
    width: 500,
    height: 110,
    preEventRgb: [32, 48, 64],
    eventRgb: [160, 32, 32],
  });
  await testInfo.attach('tab-audio-probe-marker-rgb24.raw', {
    body: rawDecodedMarkerData,
    contentType: 'application/octet-stream',
  });
  await testInfo.attach('tab-audio-probe-outcome', {
    body: JSON.stringify({
      requested: { video: true, audio: true, preferCurrentTab: true },
      fixture: probe.fixture,
      capabilities,
      outcome,
      tones,
      visualMarkerDiagnostic,
      rawPtsOnly: true,
      note: 'Qualified capability is one live video track plus one live tab-audio track, presence of both declared source tones, and native per-stream PTS. Decoded VP8 marker samples are diagnostic only; no audio/video offset, event phase, per-clip alignment, normalization, resampling, parity, or global-origin claim is made.',
    }, null, 2),
    contentType: 'application/json',
  });
});
