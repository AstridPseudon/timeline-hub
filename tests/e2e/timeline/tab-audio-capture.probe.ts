import { expect, test } from '@playwright/test';
import { execFile } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import { assertCaptureCapabilities, assertCaptureOutcome, assertTone } from './tab-audio-capture.analysis.mjs';
import { editorUrl, resetFakeRuntimeBaseline } from './support';

const exec = promisify(execFile);
const TONE_HZ = 880;
const VISUAL_EVENT_MS = 1_500;
const CAPTURE_MS = 4_000;

declare global {
  interface Window {
    __tabAudioChunk: (base64: string) => Promise<void>;
    __tabAudioProbe: {
      mimeType: string;
      tracks: Array<{ kind: string; readyState: string; settings: MediaTrackSettings }>;
      chunks: string[];
      fixture: { toneHz: number; visualEventMs: number; captureMs: number; startedAt: number; visualEventAt: number };
    };
  }
}

async function readFfprobe(path: string) {
  const { stdout } = await exec('ffprobe', [
    '-v', 'error', '-show_streams', '-show_packets', '-of', 'json', path,
  ], { maxBuffer: 32 * 1024 * 1024 });
  return JSON.parse(stdout) as { streams: unknown[]; packets: unknown[] };
}

async function readAudio(path: string, stream: { index: number; sample_rate: string; channels: number }) {
  const { stdout } = await exec('ffmpeg', [
    '-v', 'error', '-i', path, '-map', `0:${stream.index}`, '-f', 'f32le', 'pipe:1',
  ], { encoding: 'buffer', maxBuffer: 32 * 1024 * 1024 });
  if (stdout.byteLength % Float32Array.BYTES_PER_ELEMENT !== 0) throw new Error('Decoded audio was not f32-aligned');
  return assertTone(new Float32Array(stdout.buffer, stdout.byteOffset, stdout.byteLength / Float32Array.BYTES_PER_ELEMENT), {
    sampleRate: Number(stream.sample_rate), channels: Number(stream.channels), frequency: TONE_HZ,
  });
}

test('captures whole-tab video and tab audio in one Chrome155 MediaRecorder clock', async ({ page }, testInfo) => {
  test.setTimeout(120_000);
  expect(await resetFakeRuntimeBaseline()).toBeNull();
  await page.goto(editorUrl({ timeline: 'audio-reactive-colour-timeline' }), { waitUntil: 'domcontentloaded' });
  await expect(page.getByRole('button', { name: 'Play', exact: true }).first()).toBeVisible({ timeout: 90_000 });

  const chunks: Buffer[] = [];
  await page.exposeFunction('__tabAudioChunk', (base64: string) => chunks.push(Buffer.from(base64, 'base64')));
  await page.evaluate(({ toneHz, visualEventMs, captureMs }) => {
    const button = document.createElement('button');
    button.id = 'tab-audio-probe-start';
    button.textContent = 'Start tab-audio probe';
    button.style.cssText = 'position:fixed;top:8px;left:8px;z-index:2147483647;background:#203040;color:white;padding:12px';
    const marker = document.createElement('div');
    marker.id = 'tab-audio-probe-marker';
    marker.textContent = 'TAB-AUDIO-PROBE: PRE-EVENT';
    marker.style.cssText = 'position:fixed;right:8px;bottom:8px;z-index:2147483647;background:#203040;color:white;padding:18px;font:24px monospace';
    document.body.append(button, marker);
    button.onclick = async () => {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: true,
        preferCurrentTab: true,
      } as DisplayMediaStreamOptions);
      const mimeType = 'video/webm;codecs=vp8,opus';
      if (!MediaRecorder.isTypeSupported(mimeType)) throw new Error(`Unsupported recorder MIME: ${mimeType}`);
      const recorder = new MediaRecorder(stream, { mimeType });
      const audio = new AudioContext();
      await audio.resume();
      const oscillator = audio.createOscillator();
      const gain = audio.createGain();
      gain.gain.value = 0.2;
      oscillator.frequency.value = toneHz;
      oscillator.connect(gain).connect(audio.destination);
      const startedAt = performance.now();
      let visualEventAt = Number.NaN;
      const fixture = { toneHz, visualEventMs, captureMs, startedAt, visualEventAt };
      window.__tabAudioProbe = {
        mimeType,
        tracks: stream.getTracks().map((track) => ({ kind: track.kind, readyState: track.readyState, settings: track.getSettings() })),
        chunks: [],
        fixture,
      };
      recorder.ondataavailable = async (event) => {
        if (event.data.size === 0) return;
        const bytes = new Uint8Array(await event.data.arrayBuffer());
        let binary = '';
        for (const byte of bytes) binary += String.fromCharCode(byte);
        await window.__tabAudioChunk(btoa(binary));
      };
      const animate = (now: number) => {
        if (Number.isNaN(visualEventAt) && now - startedAt >= visualEventMs) {
          visualEventAt = now;
          fixture.visualEventAt = now;
          marker.textContent = 'TAB-AUDIO-PROBE: KNOWN-VISUAL-EVENT';
          marker.style.background = '#a02020';
        }
        if (now - startedAt < captureMs) requestAnimationFrame(animate);
      };
      recorder.start(100);
      oscillator.start();
      requestAnimationFrame(animate);
      await new Promise((resolve) => setTimeout(resolve, captureMs));
      oscillator.stop();
      await audio.close();
      recorder.stop();
      await new Promise<void>((resolve) => recorder.addEventListener('stop', () => resolve(), { once: true }));
      stream.getTracks().forEach((track) => track.stop());
      button.dataset.result = 'complete';
    };
    button.click();
  }, { toneHz: TONE_HZ, visualEventMs: VISUAL_EVENT_MS, captureMs: CAPTURE_MS });
  await expect(page.locator('#tab-audio-probe-start')).toHaveAttribute('data-result', 'complete', { timeout: 20_000 });

  const probe = await page.evaluate(() => window.__tabAudioProbe);
  const capabilities = assertCaptureCapabilities(probe.tracks, { mimeType: probe.mimeType });
  expect(probe.fixture.toneHz).toBe(TONE_HZ);
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
  const tone = await readAudio(output, audioStream);
  await testInfo.attach('tab-audio-probe-outcome', {
    body: JSON.stringify({
      requested: { video: true, audio: true, preferCurrentTab: true },
      fixture: probe.fixture,
      capabilities,
      outcome,
      tone,
      rawPtsOnly: true,
      note: 'No audio/video offset, per-clip alignment, normalization, resampling, or parity claim is made.',
    }, null, 2),
    contentType: 'application/json',
  });
});
