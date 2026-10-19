import { expect, test as base, type Page } from '@playwright/test';
import type { PlayerRef } from '@remotion/player';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { CAPTURE_TIMELINE, TONES, createManagedTones, publishCaptureFixture, type Backend } from './player-audio-fixture';
import { decodeMonitor, privateMonitor } from './player-audio-monitor';
import { editorUrl, resetFakeRuntimeBaseline } from './support';

type Monitor = Awaited<ReturnType<typeof privateMonitor>>;
const test = base.extend<object, { monitor: Monitor }>({
  monitor: [async ({ playwright: _playwright }, use) => {
    const monitor = await privateMonitor();
    try { await use(monitor); } finally { await monitor.close(); }
  }, { scope: 'worker' }],
  browser: [async ({ playwright, launchOptions, monitor }, use) => {
    const browser = await playwright.chromium.launch({ ...launchOptions, env: monitor.env });
    try { await use(browser); } finally { await browser.close(); }
  }, { scope: 'worker' }],
});

declare global {
  interface Window {
    __capturePlayer: PlayerRef;
    __captureBackends: { elements: string[]; buffers: number };
    __captureFrames: { frame: number; time: number }[];
  }
}

async function findPlayer(page: Page) {
  // React's ref is inspected only by this harness. Product code needs no debug
  // API, and playback/volume/mute still use the mounted real Player methods.
  await page.evaluate(() => {
    type Fiber = { return?: Fiber; memoizedState?: Hook };
    type Hook = { memoizedState?: { current?: PlayerRef }; next?: Hook };
    const label = document.querySelector('[data-testid="preview-revision-label"]');
    if (!label) throw new Error('Missing actual Player preview');
    const key = Object.keys(label).find(key => key.startsWith('__reactFiber$'));
    let fiber: Fiber | undefined = key ? (label as unknown as Record<string, Fiber>)[key] : undefined;
    for (let depth = 0; fiber && depth < 100; depth++, fiber = fiber.return) {
      let hook = fiber.memoizedState;
      for (let index = 0; hook && index < 100; index++, hook = hook.next) {
        const ref = hook.memoizedState?.current;
        if (ref && typeof ref.seekTo === 'function' && typeof ref.setVolume === 'function') {
          window.__capturePlayer = ref;
          return;
        }
      }
    }
    throw new Error('Mounted Remotion PlayerRef not found');
  });
}

// Soft integrity assertions retain a failing test verdict while collecting the
// remaining backend/control recordings. Empty capture is still a hard stop.
function audibleMetrics(capture: Awaited<ReturnType<typeof decodeMonitor>>, frequencies: number[]) {
  const active: number[] = [];
  for (let step = 0; step < 300; step++) {
    if (capture.rms(step * 0.02, (step + 1) * 0.02) > 0.004) active.push(step);
  }
  expect(active.length, 'silent/empty capture').toBeGreaterThan(135);
  const onset = active[0] * 0.02;
  const offset = (active.at(-1)! + 1) * 0.02;
  console.log('CAPTURE_TIMING', JSON.stringify({ onset, offset, activeBlocks: active.length }));
  expect.soft(offset - onset, 'three-second live media duration').toBeGreaterThan(2.88);
  expect.soft(offset - onset).toBeLessThan(3.12);
  // One onset for the whole capture; no per-source shifting or realignment.
  const start = onset + 0.5;
  const end = onset + 2.5;
  for (let time = start; time < end; time += 0.005) {
    expect.soft(capture.rms(time, time + 0.005), 'dropped/silent interior block').toBeGreaterThan(0.004);
  }
  const left = capture.rms(start, end);
  const right = capture.rms(start, end, 1);
  expect.soft(right / left, 'missing/rebalanced stereo channel').toBeGreaterThan(0.70);
  expect.soft(right / left).toBeLessThan(0.80);
  const phaseSteps: number[] = [];
  const amplitudes = frequencies.map(frequency => {
    const windows = Array.from({ length: 20 }, (_, index) => start + index * 0.1);
    const bands = windows.map(time => capture.spectrum(frequency, time, time + 0.1));
    const levels = bands.map(band => band.amplitude);
    const jumps = bands.slice(1).map((band, index) => {
      const delta = band.phase - bands[index].phase;
      return Math.abs(Math.atan2(Math.sin(delta), Math.cos(delta)));
    });
    const phaseStep = Math.max(...jumps);
    expect.soft(phaseStep, `sample/phase discontinuity in ${frequency} Hz backend`).toBeLessThan(0.1);
    phaseSteps.push(phaseStep);
    for (const level of levels) expect.soft(level, `dropped ${frequency} Hz backend block`).toBeGreaterThan(0.04);
    const amplitude = levels.reduce((sum, value) => sum + value, 0) / levels.length;
    expect.soft(amplitude, `missing ${frequency} Hz backend`).toBeGreaterThan(0.04);
    const otherChannel = windows.reduce((sum, time) => sum + capture.spectrum(frequency, time, time + 0.1, 1).amplitude, 0) / windows.length;
    expect.soft(otherChannel / amplitude).toBeGreaterThan(0.70);
    expect.soft(otherChannel / amplitude).toBeLessThan(0.80);
    return amplitude;
  });
  return { sampleCount: capture.sampleCount, onset, offset, left, right, amplitudes, phaseSteps };
}

function gainDifferenceDb(actual: number, reference: number) {
  return 20 * Math.log10(actual / reference);
}

function requireUnchangedGain(actual: number, reference: number) {
  const db = gainDifferenceDb(actual, reference);
  if (Math.abs(db) > 0.5) throw new Error(`captured output gain mismatch: ${db.toFixed(3)} dB`);
}

for (const mode of ['mixed output controls', 'amplified fade timing'] as const) {
  test(`captures real Player ${mode}`, async ({ context, monitor }, testInfo) => {
    test.setTimeout(360_000);
    expect(await resetFakeRuntimeBaseline()).toBeNull();
    const directory = await mkdtemp(join(tmpdir(), 'player-audio-media-'));
    const results: Record<string, unknown> = {};
    try {
      const objects = await createManagedTones(directory);
      let fixtureKey = '';
      let revision: Awaited<ReturnType<typeof publishCaptureFixture>>;
      const run = async (name: string, backends: Backend[], options: { volume?: number; muted?: boolean; captureGain?: number; fallback?: boolean; fade?: boolean } = {}) => {
        const key = JSON.stringify([backends, options.fade ?? false]);
        if (!revision || key !== fixtureKey) {
          revision = await publishCaptureFixture(objects, backends, options.fade);
          fixtureKey = key;
        }
        const page = await context.newPage();
        const requests: Array<{ url: string; status: number }> = [];
        const errors: string[] = [];
        page.on('console', message => {
          if (['warning', 'error'].includes(message.type())) console.log('PLAYER_CONSOLE', name, message.text());
        });
        page.on('pageerror', error => errors.push(error.message));
        page.on('response', response => {
          if (Object.values(objects).some(id => decodeURIComponent(response.url()).includes(id))) {
            requests.push({ url: response.url(), status: response.status() });
          }
        });
        try {
          await page.addInitScript(({ fallback }) => {
            window.__captureBackends = { elements: [], buffers: 0 };
            const mediaSource = AudioContext.prototype.createMediaElementSource;
            AudioContext.prototype.createMediaElementSource = function (element) {
              window.__captureBackends.elements.push(element.src);
              return mediaSource.call(this, element);
            };
            const bufferSource = AudioContext.prototype.createBufferSource;
            AudioContext.prototype.createBufferSource = function () {
              window.__captureBackends.buffers++;
              return bufferSource.call(this);
            };
            if (fallback) Object.defineProperty(window, 'VideoDecoder', { value: undefined });
          }, { fallback: options.fallback ?? false });
          await page.goto(editorUrl({ timeline: CAPTURE_TIMELINE }), { waitUntil: 'domcontentloaded' });
          const play = page.getByRole('button', { name: 'Play', exact: true }).first();
          await expect(play).toBeVisible({ timeout: 90_000 });
          await findPlayer(page);
          await page.evaluate(({ volume, muted }) => {
            window.__capturePlayer.pause();
            window.__capturePlayer.seekTo(0);
            window.__capturePlayer.setVolume(volume);
            if (muted) window.__capturePlayer.mute(); else window.__capturePlayer.unmute();
          }, { volume: options.volume ?? 1, muted: options.muted ?? false });
          await expect.poll(() => page.evaluate(() => window.__capturePlayer.getCurrentFrame())).toBe(0);
          // Audio premount must be ready before starting the monitor and gesture.
          if (backends.some(backend => backend !== 'video')) {
            await expect.poll(() => page.locator('audio[src]').evaluateAll(elements => elements.length > 0 && elements.every(element => (element as HTMLAudioElement).readyState >= 2)), { timeout: 20_000 }).toBe(true);
          }
          if (backends.includes('video') && !options.fallback) {
            await expect(page.locator('[data-preview-decoded-frame="true"]')).toHaveCount(1, { timeout: 20_000 });
          }
          // Warm the real browser output device/decoder with this same Player,
          // then rewind. Startup device latency is outside the measured run.
          await play.click();
          await expect.poll(() => page.evaluate(() => window.__capturePlayer.getCurrentFrame()), { timeout: 15_000 }).toBeGreaterThan(35);
          if (options.fallback) expect(await page.locator('video').count()).toBeGreaterThan(0);
          await expect.poll(() => page.evaluate(() => window.__capturePlayer.isPlaying()), { timeout: 15_000 }).toBe(false);

          await page.evaluate(() => {
            window.__capturePlayer.pause();
            window.__capturePlayer.seekTo(0);
            window.__captureFrames = [];
            window.__capturePlayer.addEventListener('frameupdate', event => {
              window.__captureFrames.push({ frame: event.detail.frame, time: performance.now() });
            });
          });
          await expect.poll(() => page.evaluate(() => window.__capturePlayer.getCurrentFrame())).toBe(0);
          const path = testInfo.outputPath(`${name}.wav`);
          await monitor.record(path, () => play.click(), options.captureGain);
          await page.evaluate(() => window.__capturePlayer.pause());
          const frames = await page.evaluate(() => window.__captureFrames);
          const moving = frames.filter(frame => frame.frame > 0);
          const first = moving[0];
          const last = moving.at(-1);
          if (!first || !last) throw new Error('Player did not advance during capture');
          const drift = (last.time - first.time) / 1000 - (last.frame - first.frame) / 30;
          const clock = { first, last, drift, events: moving.length, finalFrame: Math.max(...frames.map(frame => frame.frame)) };
          console.log('PLAYER_CLOCK', name, JSON.stringify(clock));
          expect(clock.finalFrame).toBeGreaterThanOrEqual(118);
          expect.soft(Math.abs(clock.drift), 'Player wall clock drift during capture').toBeLessThan(0.12);
          const capture = await decodeMonitor(path);
          for (const backend of backends) {
            expect(requests.some(request => decodeURIComponent(request.url).includes(objects[backend]) && [200, 206].includes(request.status)), `managed ${backend} fetched`).toBe(true);
          }
          const backendState = await page.evaluate(() => window.__captureBackends);
          results[name] = { revision: revision.headRevisionId, clock, backendState, requests };
          if (backends.includes('amplified')) expect(backendState.elements.some(url => decodeURIComponent(url).includes(objects.amplified))).toBe(true);
          if (backends.includes('native')) expect(backendState.elements.some(url => decodeURIComponent(url).includes(objects.native))).toBe(false);
          if (backends.includes('video') && !options.fallback && !options.muted) expect(backendState.buffers).toBeGreaterThan(0);
          expect(errors).toEqual([]);
          expect(await page.getByTestId('preview-media-error').count()).toBe(0);
          const metrics = options.muted ? { sampleCount: capture.sampleCount, left: capture.rms(), right: capture.rms(0, 6, 1) } : audibleMetrics(capture, backends.map(backend => TONES[backend]));
          results[name] = { revision: revision.headRevisionId, ...metrics, clock, backendState, requests };
          console.log('PLAYER_CAPTURE', name, JSON.stringify(metrics));
          return { capture, metrics };
        } finally { await page.close(); }
      };

      if (mode === 'amplified fade timing') {
        const faded = await run('amplified-fade', ['amplified'], { fade: true });
        if (!('onset' in faded.metrics)) throw new Error('Missing fade onset');
        const fadeOnset = faded.metrics.onset;
        const plateau = faded.capture.rms(fadeOnset + 1, fadeOnset + 2);
        expect(faded.capture.rms(fadeOnset + 0.06, fadeOnset + 0.16) / plateau).toBeLessThan(0.6);
        expect(faded.capture.rms(fadeOnset + 2.8, fadeOnset + 2.9) / plateau).toBeLessThan(0.6);
        return;
      }
      for (const backend of Object.keys(TONES) as Backend[]) await run(backend, [backend]);
      await run('video-native-fallback', ['video'], { fallback: true });
      const backends = Object.keys(TONES) as Backend[];
      const mixed = await run('mixed', backends);
      const half = await run('mixed-player-half', backends, { volume: 0.5 });
      expect(gainDifferenceDb(half.metrics.left, mixed.metrics.left)).toBeCloseTo(-6.0206, 0);
      const muted = await run('mixed-player-muted', backends, { muted: true });
      expect(muted.metrics.left).toBeLessThan(0.0001);
      expect(muted.metrics.right).toBeLessThan(0.0001);
      const planted = await run('mixed-capture-half', backends, { captureGain: 0.5 });
      expect(gainDifferenceDb(planted.metrics.left, mixed.metrics.left)).toBeCloseTo(-6.0206, 0);
      expect(() => requireUnchangedGain(planted.metrics.left, mixed.metrics.left)).toThrow(/captured output gain mismatch: -6\./);
      // An independent unmodified playback must pass the same comparator.
      const repeated = await run('mixed-repeat', backends);
      requireUnchangedGain(repeated.metrics.left, mixed.metrics.left);
    } finally {
      await testInfo.attach('player-capture-metrics', { body: JSON.stringify(results, null, 2), contentType: 'application/json' });
      await rm(directory, { recursive: true, force: true });
    }
  });
}
