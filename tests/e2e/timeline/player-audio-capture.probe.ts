import { expect, test as base, type Page } from '@playwright/test';
import type { PlayerRef } from '@remotion/player';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { CAPTURE_TIMELINE, TONES, createManagedTones, publishCaptureFixture, type Backend } from './player-audio-fixture';
import { audibleEdges, decodeMonitor, privateMonitor, requireAudibleDuration } from './player-audio-monitor';
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

// Trace DOM inspection can itself grant activation; keep API traces and the
// explicit media/frame/context observations without inspecting live DOM frames.
test.use({ trace: { mode: 'retain-on-failure', snapshots: false, screenshots: false } });

declare global {
  interface Window {
    __capturePlayer: PlayerRef;
    __captureBackends: { elements: string[]; buffers: number; audibleBuffers: number };
    __captureFrames: {
      frame: number;
      time: number;
      media: { currentTime: number; paused: boolean; seeking: boolean; readyState: number }[];
      contexts: { currentTime: number; state: AudioContextState; output: AudioTimestamp }[];
    }[];
    __captureEvents: Record<string, unknown>[];
    __captureContexts: BaseAudioContext[];
  }
}

// Playwright's page.evaluate grants user activation through CDP. Inspection and
// transport setup must not unlock the audio device before the measured click.
async function evaluateWithoutGesture<T, A = undefined>(page: Page, fn: (arg: A) => T, arg?: A): Promise<T> {
  const session = await page.context().newCDPSession(page);
  try {
    const { result, exceptionDetails } = await session.send('Runtime.evaluate', {
      expression: `(${fn.toString()})(${JSON.stringify(arg) ?? 'undefined'})`,
      userGesture: false, returnByValue: true, awaitPromise: true,
    });
    if (exceptionDetails) throw new Error(exceptionDetails.exception?.description ?? exceptionDetails.text);
    return result.value as T;
  } finally { await session.detach(); }
}

// Locator actions also inspect the DOM with activation enabled. Dispatch the
// actual mouse gesture directly so no inspection can wake a pending resume.
async function clickPlay(page: Page) {
  const point = await evaluateWithoutGesture(page, () => {
    const button = document.querySelector('.astrid-preview-transport button[aria-label="Play"]');
    if (!button) throw new Error('Missing Play button');
    const rect = button.getBoundingClientRect();
    return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
  });
  const session = await page.context().newCDPSession(page);
  try {
    await session.send('Input.dispatchMouseEvent', { type: 'mousePressed', ...point, button: 'left', clickCount: 1 });
    await session.send('Input.dispatchMouseEvent', { type: 'mouseReleased', ...point, button: 'left', clickCount: 1 });
  } finally { await session.detach(); }
}

async function findPlayer(page: Page) {
  // React's ref is inspected only by this harness. Product code needs no debug
  // API, and playback/volume/mute still use the mounted real Player methods.
  await evaluateWithoutGesture(page, () => {
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
  const { active, onset, offset } = audibleEdges(capture);
  expect(active.length, 'silent/empty capture').toBeGreaterThan(135);
  console.log('CAPTURE_TIMING', JSON.stringify({ onset, offset, activeBlocks: active.length }));
  requireAudibleDuration(offset - onset, expect.soft);
  // One onset for the whole capture; no per-source shifting or realignment.
  const start = onset + 0.5;
  const end = onset + 2.5;
  let silentBlocks = 0;
  for (let time = start; time < end; time += 0.005) {
    const rms = capture.rms(time, time + 0.005);
    if (rms <= 0.004) silentBlocks++;
    expect.soft(rms, 'dropped/silent interior block').toBeGreaterThan(0.004);
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
  return { sampleCount: capture.sampleCount, onset, offset, left, right, amplitudes, phaseSteps, silentBlocks };
}

function gainDifferenceDb(actual: number, reference: number) {
  return 20 * Math.log10(actual / reference);
}

function requireUnchangedGain(actual: number, reference: number) {
  const db = gainDifferenceDb(actual, reference);
  if (Math.abs(db) > 0.5) throw new Error(`captured output gain mismatch: ${db.toFixed(3)} dB`);
}

// The idle diagnostic stays available without this opt-in. Expected bytes come
// from the reviewed installer and frozen package, before the browser is launched.
async function observedGraph() {
  if (process.env.PLAYER_AUDIO_OBSERVE !== '1') return null;
  const expected = JSON.parse(await readFile(process.env.PLAYER_AUDIO_EXPECTED_GRAPH!, 'utf8'));
  const hashes = Object.fromEntries(await Promise.all(Object.keys(expected.hashes).map(async path =>
    [path, createHash('sha256').update(await readFile(path)).digest('hex')])));
  const compositionFiles = Object.fromEntries(await Promise.all(Object.keys(expected.compositionFiles).map(async path =>
    [path, createHash('sha256').update(await readFile(`node_modules/@banodoco/timeline-composition/${path}`)).digest('hex')])));
  const versions = Object.fromEntries(await Promise.all(Object.keys(expected.versions).map(async name =>
    [name, JSON.parse(await readFile(`node_modules/${name}/package.json`, 'utf8')).version])));
  const graph = { hashes, compositionFiles, versions, nodeModulesResolvedPath: await realpath('node_modules') };
  expect(graph).toEqual(expected);
  return graph;
}

for (const mode of ['mixed output controls', 'amplified fade timing', 'amplified fade timing first gesture without warm-up', 'startup cancellation and replay'] as const) {
  test(`captures real Player ${mode}`, async ({ browser, context, monitor }, testInfo) => {
    test.setTimeout(360_000);
    expect(await resetFakeRuntimeBaseline()).toBeNull();
    const directory = await mkdtemp(join(tmpdir(), 'player-audio-media-'));
    const results: Record<string, unknown> = { beforeGraph: await observedGraph(), environment: {
      repeatIndex: testInfo.repeatEachIndex, browser: browser.version(), node: process.version,
      launchOptions: testInfo.project.use.launchOptions,
      packageLockSha256: createHash('sha256').update(await readFile('package-lock.json')).digest('hex'),
      player: JSON.parse(await readFile('node_modules/@remotion/player/package.json', 'utf8')).version,
      react: JSON.parse(await readFile('node_modules/react/package.json', 'utf8')).version,
      playerEsmSha256: createHash('sha256').update(await readFile('node_modules/@remotion/player/dist/esm/index.mjs')).digest('hex'),
      remotionEsmSha256: createHash('sha256').update(await readFile('node_modules/remotion/dist/esm/index.mjs')).digest('hex'),
      composition: JSON.parse(await readFile('node_modules/@banodoco/timeline-composition/package.json', 'utf8')).version,
    } };
    const cdp = await browser.newBrowserCDPSession();
    try {
      const objects = await createManagedTones(directory);
      results.objects = objects;
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
        let consumer: Awaited<ReturnType<Monitor['drain']>> | undefined;
        try {
          await page.addInitScript(({ fallback }) => {
            window.__captureBackends = { elements: [], buffers: 0, audibleBuffers: 0 };
            window.__captureEvents = [{ type: 'init', epochMs: performance.timeOrigin + performance.now(), userActivation: navigator.userActivation.hasBeenActive }];
            window.__captureContexts = [];
            for (const type of ['click', 'playing', 'waiting', 'stalled', 'canplay', 'seeking', 'seeked', 'pause', 'ended', 'visibilitychange']) {
              document.addEventListener(type, event => {
                const media = event.target instanceof HTMLMediaElement ? event.target : null;
                window.__captureEvents.push({ type, epochMs: performance.timeOrigin + performance.now(), src: media?.currentSrc, currentTime: media?.currentTime, readyState: media?.readyState, visibility: document.visibilityState, playerFrame: window.__capturePlayer?.getCurrentFrame() });
              }, true);
            }
            const observeContext = (context: AudioContext) => {
              if (window.__captureContexts.includes(context)) return;
              window.__captureContexts.push(context);
              context.addEventListener('statechange', () => {
                window.__captureEvents.push({
                  type: 'context-state', epochMs: performance.timeOrigin + performance.now(),
                  contextState: context.state, contextTime: context.currentTime,
                  output: context.getOutputTimestamp(), playerFrame: window.__capturePlayer?.getCurrentFrame(),
                  media: Array.from(document.querySelectorAll('audio[src], video')).map(element => ({
                    currentTime: (element as HTMLMediaElement).currentTime,
                    paused: (element as HTMLMediaElement).paused,
                  })),
                });
              });
            };
            const nativePlay = HTMLMediaElement.prototype.play;
            HTMLMediaElement.prototype.play = function () {
              window.__captureEvents.push({
                type: 'media-play-call', epochMs: performance.timeOrigin + performance.now(),
                src: this.currentSrc || this.src, currentTime: this.currentTime,
                playerFrame: window.__capturePlayer?.getCurrentFrame(),
                contexts: window.__captureContexts.map(context => ({
                  state: context.state, currentTime: context.currentTime,
                  output: (context as AudioContext).getOutputTimestamp(),
                })),
              });
              return nativePlay.call(this);
            };
            const suspend = AudioContext.prototype.suspend;
            AudioContext.prototype.suspend = function () {
              observeContext(this);
              window.__captureEvents.push({ type: 'context-suspend-call', epochMs: performance.timeOrigin + performance.now(), contextState: this.state, contextTime: this.currentTime, stack: new Error().stack });
              return suspend.call(this);
            };
            const resume = AudioContext.prototype.resume;
            AudioContext.prototype.resume = function () {
              observeContext(this);
              window.__captureEvents.push({ type: 'context-resume-call', epochMs: performance.timeOrigin + performance.now(), contextState: this.state, contextTime: this.currentTime });
              return resume.call(this);
            };
            const mediaSource = AudioContext.prototype.createMediaElementSource;
            AudioContext.prototype.createMediaElementSource = function (element) {
              window.__captureBackends.elements.push(element.src);
              observeContext(this);
              return mediaSource.call(this, element);
            };
            const bufferSource = AudioContext.prototype.createBufferSource;
            AudioContext.prototype.createBufferSource = function () {
              const id = ++window.__captureBackends.buffers;
              observeContext(this);
              const source = bufferSource.call(this);
              const start = source.start.bind(source);
              const stop = source.stop.bind(source);
              const disconnect = source.disconnect;
              let silent: boolean | undefined;
              source.start = (...args: Parameters<typeof start>) => {
                const buffer = source.buffer;
                silent = !buffer || Array.from({ length: buffer.numberOfChannels }, (_, channel) => channel)
                  .every(channel => buffer.getChannelData(channel).every(value => value === 0));
                if (!silent) window.__captureBackends.audibleBuffers++;
                window.__captureEvents.push({ type: 'buffer-start', id, silent, epochMs: performance.timeOrigin + performance.now(), args, contextTime: this.currentTime, contextState: this.state, bufferDuration: buffer?.duration });
                start(...args);
              };
              source.stop = (...args: Parameters<typeof stop>) => {
                window.__captureEvents.push({ type: 'buffer-stop', id, silent, epochMs: performance.timeOrigin + performance.now() });
                stop(...args);
              };
              source.disconnect = function (this: AudioBufferSourceNode, ...args: unknown[]) {
                window.__captureEvents.push({ type: 'buffer-disconnect', id, silent, epochMs: performance.timeOrigin + performance.now() });
                Reflect.apply(disconnect, this, args);
              };
              return source;
            };
            if (fallback) Object.defineProperty(window, 'VideoDecoder', { value: undefined });
          }, { fallback: options.fallback ?? false });
          await page.goto(editorUrl({ timeline: CAPTURE_TIMELINE }), { waitUntil: 'domcontentloaded' });
          await expect.poll(() => evaluateWithoutGesture(page, () => {
            const button = document.querySelector('.astrid-preview-transport button[aria-label="Play"]');
            return Boolean(button?.getBoundingClientRect().width);
          }), { timeout: 90_000 }).toBe(true);
          await findPlayer(page);
          await evaluateWithoutGesture(page, ({ volume, muted }) => {
            window.__capturePlayer.pause();
            window.__capturePlayer.seekTo(0);
            window.__capturePlayer.setVolume(volume);
            if (muted) window.__capturePlayer.mute(); else window.__capturePlayer.unmute();
          }, { volume: options.volume ?? 1, muted: options.muted ?? false });
          await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.getCurrentFrame())).toBe(0);
          // Audio premount must be ready before starting the monitor and gesture.
          if (backends.some(backend => backend !== 'video')) {
            await expect.poll(() => evaluateWithoutGesture(page, () => {
              const elements = [...document.querySelectorAll<HTMLAudioElement>('audio[src]')];
              return elements.length > 0 && elements.every(element => element.readyState >= 2);
            }), { timeout: 20_000 }).toBe(true);
          }
          if (backends.includes('video') && !options.fallback) {
            await expect(page.locator('[data-preview-decoded-frame="true"]')).toHaveCount(1, { timeout: 20_000 });
          }
          // Observe the private sink before any gesture and throughout the WAV
          // measurement. This consumer adds no sink input or browser audio.
          if (process.env.PLAYER_AUDIO_OBSERVE === '1') {
            consumer = await monitor.drain(testInfo.outputPath(`${name}-consumer.json`), () => cdp.send('SystemInfo.getProcessInfo'));
          }
          results[`${name}-before-first-gesture`] = await evaluateWithoutGesture(page, () => ({
            epochMs: performance.timeOrigin + performance.now(), frame: window.__capturePlayer.getCurrentFrame(),
            muted: window.__capturePlayer.isMuted(), userActivation: navigator.userActivation.hasBeenActive,
            media: [...document.querySelectorAll('audio,video')].map(element => {
              const media = element as HTMLMediaElement;
              return { src: media.currentSrc, readyState: media.readyState, currentTime: media.currentTime, paused: media.paused };
            }),
            contexts: window.__captureContexts.map(context => ({ state: context.state, currentTime: context.currentTime, output: (context as AudioContext).getOutputTimestamp() })),
          }));
          // Keep the original warm-rewind and first-gesture cases.
          if (mode !== 'amplified fade timing first gesture without warm-up') {
            results[`${name}-monitor-before-warmup`] = await monitor.inspect();
            await clickPlay(page);
            await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.getCurrentFrame()), { timeout: 15_000 }).toBeGreaterThan(35);
            if (options.fallback) expect(await page.locator('video').count()).toBeGreaterThan(0);
            await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.isPlaying()), { timeout: 15_000 }).toBe(false);
            await evaluateWithoutGesture(page, () => {
              window.__capturePlayer.pause();
              window.__capturePlayer.seekTo(0);
            });
          }

          if (mode === 'startup cancellation and replay') {
            for (const action of ['pause', 'seek'] as const) {
              await evaluateWithoutGesture(page, action => {
                document.addEventListener('click', () => {
                  if (action === 'seek') window.__capturePlayer.seekTo(30);
                  window.__capturePlayer.pause();
                }, { once: true });
              }, action);
              await clickPlay(page);
              await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.isPlaying())).toBe(false);
              // Observe the aborted promise after the normal output-readiness window.
              await page.waitForTimeout(250);
              const cancelled = await evaluateWithoutGesture(page, () => ({
                playing: window.__capturePlayer.isPlaying(), frame: window.__capturePlayer.getCurrentFrame(),
                media: Array.from(document.querySelectorAll('audio[src], video')).map(element => ({
                  paused: (element as HTMLMediaElement).paused, currentTime: (element as HTMLMediaElement).currentTime,
                })),
              }));
              results[`cancel-${action}`] = cancelled;
              expect(cancelled.playing).toBe(false);
              expect(cancelled.frame).toBe(action === 'seek' ? 30 : 0);
              expect(cancelled.media.every(media => media.paused)).toBe(true);
              await evaluateWithoutGesture(page, () => window.__capturePlayer.seekTo(0));
            }
            // Also stop an established clock, then seek and replay from zero.
            await clickPlay(page);
            await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.getCurrentFrame())).toBeGreaterThan(10);
            await evaluateWithoutGesture(page, () => window.__capturePlayer.pause());
            const paused = await evaluateWithoutGesture(page, () => ({
              frame: window.__capturePlayer.getCurrentFrame(),
              times: Array.from(document.querySelectorAll('audio[src], video')).map(element => (element as HTMLMediaElement).currentTime),
            }));
            await page.waitForTimeout(250);
            const stopped = await evaluateWithoutGesture(page, () => ({
              frame: window.__capturePlayer.getCurrentFrame(),
              times: Array.from(document.querySelectorAll('audio[src], video')).map(element => (element as HTMLMediaElement).currentTime),
            }));
            results.pause = { paused, stopped };
            expect(stopped.frame).toBe(paused.frame);
            for (let index = 0; index < paused.times.length; index++) {
              expect(Math.abs(stopped.times[index] - paused.times[index])).toBeLessThan(1 / 30);
            }
            await evaluateWithoutGesture(page, () => window.__capturePlayer.seekTo(0));
          }

          await evaluateWithoutGesture(page, () => {
            window.__captureFrames = [];
            window.__capturePlayer.addEventListener('frameupdate', event => {
              // Observe both clocks without seeking media or changing its gain.
              window.__captureFrames.push({
                frame: event.detail.frame, time: performance.now(),
                media: Array.from(document.querySelectorAll('audio[src], video')).map(element => {
                  const media = element as HTMLMediaElement;
                  return { currentTime: media.currentTime, paused: media.paused, seeking: media.seeking, readyState: media.readyState };
                }),
                contexts: window.__captureContexts.map(context => ({
                  currentTime: context.currentTime, state: context.state,
                  output: (context as AudioContext).getOutputTimestamp(),
                })),
              });
            });
          });
          await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.getCurrentFrame())).toBe(0);
          if (backends.some(backend => backend !== 'video')) {
            await expect.poll(() => evaluateWithoutGesture(page, () => {
              const elements = [...document.querySelectorAll<HTMLAudioElement>('audio[src]')];
              return elements.length > 0 && elements.every(element => element.readyState >= 2);
            }), { timeout: 20_000 }).toBe(true);
          }
          if (backends.includes('video') && !options.fallback) {
            await expect(page.locator('[data-preview-decoded-frame="true"]')).toHaveCount(1, { timeout: 20_000 });
          }
          const readiness = await evaluateWithoutGesture(page, () => ({
            epochMs: performance.timeOrigin + performance.now(), timeOrigin: performance.timeOrigin, visibility: document.visibilityState,
            muted: window.__capturePlayer.isMuted(), userActivation: navigator.userActivation.hasBeenActive,
            media: Array.from(document.querySelectorAll('audio[src], video')).map(element => {
              const media = element as HTMLMediaElement;
              return { src: media.currentSrc, readyState: media.readyState, currentTime: media.currentTime, seeking: media.seeking, paused: media.paused, error: media.error?.message, buffered: Array.from({ length: media.buffered.length }, (_, index) => [media.buffered.start(index), media.buffered.end(index)]) };
            }),
            contexts: window.__captureContexts.map(context => ({ state: context.state, currentTime: context.currentTime, sampleRate: context.sampleRate, baseLatency: (context as AudioContext).baseLatency, outputLatency: (context as AudioContext).outputLatency })),
          }));
          results[name] = { revision: revision.headRevisionId, readiness, monitorBeforeCapture: await monitor.inspect() };
          console.log('PLAYER_READINESS', name, JSON.stringify(readiness));
          if (mode === 'amplified fade timing first gesture without warm-up') {
            expect(readiness.userActivation, 'capture must precede the first user gesture').toBe(false);
          }
          expect(readiness.muted, 'no automatic mute hidden by a reset after warm-up').toBe(options.muted ?? false);
          await consumer?.snapshot('before-measurement');
          const path = testInfo.outputPath(`${name}.wav`);
          try {
            await monitor.record(path, () => clickPlay(page), options.captureGain, () => cdp.send('SystemInfo.getProcessInfo'));
            await consumer?.snapshot('after-measurement');
          } finally {
            const recording = JSON.parse(await readFile(`${path}.diagnostics.json`, 'utf8'));
            const events = await evaluateWithoutGesture(page, () => window.__captureEvents);
            results[name] = { ...results[name] as object, revision: revision.headRevisionId, readiness, recording, events };
            await testInfo.attach(`${name}-recording-diagnostics`, { body: JSON.stringify(results[name], null, 2), contentType: 'application/json' });
          }
          await evaluateWithoutGesture(page, () => window.__capturePlayer.pause());
          const frames = await evaluateWithoutGesture(page, () => window.__captureFrames);
          const moving = frames.filter(frame => frame.frame > 0);
          const first = moving[0];
          const last = moving.at(-1);
          if (!first || !last) throw new Error('Player did not advance during capture');
          const drift = (last.time - first.time) / 1000 - (last.frame - first.frame) / 30;
          const sourceLeads = moving.filter(frame => frame.frame >= 10 && frame.frame <= 80)
            .flatMap(frame => frame.media.filter(media => !media.paused && !media.seeking)
              .map(media => media.currentTime - frame.frame / 30)).sort((a, b) => a - b);
          const sourceLeadMedian = sourceLeads[Math.floor(sourceLeads.length / 2)];
          const sourceStarts = await evaluateWithoutGesture(page, () => window.__captureEvents.filter(event => event.type === 'media-play-call')) as Array<{
            epochMs: number; src: string; playerFrame: number; currentTime: number;
            contexts: Array<{ state: AudioContextState; currentTime: number; output: AudioTimestamp }>;
          }>;
          const measuredStarts = sourceStarts.filter(event => event.epochMs >= readiness.epochMs && decodeURIComponent(event.src).includes(objects.amplified));
          if (options.fade) {
            expect(measuredStarts.length, 'actual amplified source start observations').toBeGreaterThan(0);
            const firstStart = measuredStarts[0];
            expect(firstStart.playerFrame).toBe(0);
            expect(firstStart.currentTime).toBeLessThan(1 / 30);
            expect(firstStart.contexts.length).toBeGreaterThan(0);
            for (const context of firstStart.contexts) {
              expect(context.state, 'context ready before native source starts').toBe('running');
              expect(context.output.contextTime, 'fresh output before native source starts').toBeGreaterThan(0);
              expect(context.output.performanceTime).toBeGreaterThan(0);
            }
          }
          const clock = { first, last, measuredStarts, drift, sourceLeadMedian, sourceLeadMin: sourceLeads[0], sourceLeadMax: sourceLeads.at(-1), events: moving.length, finalFrame: Math.max(...frames.map(frame => frame.frame)) };
          if (options.fade) {
            expect(sourceLeads.length, 'source/frame clock observations').toBeGreaterThan(30);
            expect.soft(Math.abs(sourceLeadMedian), 'native source and authored gain frame must agree within one frame').toBeLessThan(1 / 30);
          }
          console.log('PLAYER_CLOCK', name, JSON.stringify(clock));
          expect(clock.finalFrame).toBeGreaterThanOrEqual(118);
          expect.soft(Math.abs(clock.drift), 'Player wall clock drift during capture').toBeLessThan(0.12);
          const capture = await decodeMonitor(path);
          for (const backend of backends) {
            expect(requests.some(request => decodeURIComponent(request.url).includes(objects[backend]) && [200, 206].includes(request.status)), `managed ${backend} fetched`).toBe(true);
          }
          const backendState = await evaluateWithoutGesture(page, () => window.__captureBackends);
          results[name] = { ...results[name] as object, clock, frames, backendState, requests };
          if (backends.includes('amplified')) expect(backendState.elements.some(url => decodeURIComponent(url).includes(objects.amplified))).toBe(true);
          if (backends.includes('native')) expect(backendState.elements.some(url => decodeURIComponent(url).includes(objects.native))).toBe(false);
          if (backends.includes('video') && !options.fallback && !options.muted) {
            expect(backendState.buffers).toBeGreaterThan(0);
            expect(backendState.audibleBuffers, 'video audio uses real non-silent buffers').toBeGreaterThan(0);
          }
          expect(errors).toEqual([]);
          expect(await page.getByTestId('preview-media-error').count()).toBe(0);
          const metrics = options.muted ? { sampleCount: capture.sampleCount, left: capture.rms(), right: capture.rms(0, 6, 1) } : audibleMetrics(capture, backends.map(backend => TONES[backend]));
          results[name] = { ...results[name] as object, ...metrics };
          console.log('PLAYER_CAPTURE', name, JSON.stringify(metrics));
          return { capture, metrics };
        } finally {
          results[name] = { ...results[name] as object, lifecycleEvents: await evaluateWithoutGesture(page, () => window.__captureEvents).catch(() => null) };
          try { if (consumer) results[`${name}-consumer`] = await consumer.close(); } finally { await page.close(); }
        }
      };

      if (mode.startsWith('amplified fade timing') || mode === 'startup cancellation and replay') {
        const faded = await run('amplified-fade', ['amplified'], { fade: true });
        if (!('onset' in faded.metrics)) throw new Error('Missing fade onset');
        const fadeOnset = faded.metrics.onset;
        const plateau = faded.capture.rms(fadeOnset + 1, fadeOnset + 2);
        const early = faded.capture.rms(fadeOnset + 0.06, fadeOnset + 0.16) / plateau;
        const late = faded.capture.rms(fadeOnset + 2.8, fadeOnset + 2.9) / plateau;
        results.fadeEnvelope = { plateau, early, late };
        expect(early).toBeLessThan(0.6);
        expect(late).toBeLessThan(0.6);
        return;
      }
      for (const backend of Object.keys(TONES) as Backend[]) await run(backend, [backend]);
      await run('video-native-fallback', ['video'], { fallback: true });
      const backends = Object.keys(TONES) as Backend[];
      const mixed = await run('mixed', backends);
      const half = await run('mixed-player-half', backends, { volume: 0.5 });
      expect.soft(gainDifferenceDb(half.metrics.left, mixed.metrics.left)).toBeCloseTo(-6.0206, 0);
      const muted = await run('mixed-player-muted', backends, { muted: true });
      expect(muted.metrics.left).toBeLessThan(0.0001);
      expect(muted.metrics.right).toBeLessThan(0.0001);
      const planted = await run('mixed-capture-half', backends, { captureGain: 0.5 });
      expect.soft(gainDifferenceDb(planted.metrics.left, mixed.metrics.left)).toBeCloseTo(-6.0206, 0);
      expect.soft(() => requireUnchangedGain(planted.metrics.left, mixed.metrics.left)).toThrow(/captured output gain mismatch: -6\./);
      // An independent unmodified playback must pass the same comparator.
      const repeated = await run('mixed-repeat', backends);
      requireUnchangedGain(repeated.metrics.left, mixed.metrics.left);
    } finally {
      results.afterGraph = await observedGraph();
      const metricsPath = testInfo.outputPath('player-capture-metrics.json');
      await writeFile(metricsPath, JSON.stringify(results, null, 2));
      await testInfo.attach('player-capture-metrics', { path: metricsPath, contentType: 'application/json' });
      await cdp.detach();
      await rm(directory, { recursive: true, force: true });
    }
  });
}
