import { expect, test as base, type Page } from '@playwright/test';
import type { PlayerRef } from '@remotion/player';
import { createHash } from 'node:crypto';
import { readFile, realpath } from 'node:fs/promises';
import { privateMonitor } from './player-audio-monitor';

export type Monitor = Awaited<ReturnType<typeof privateMonitor>>;
export const test = base.extend<object, { monitor: Monitor }>({
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
export async function evaluateWithoutGesture<T, A = undefined>(page: Page, fn: (arg: A) => T, arg?: A): Promise<T> {
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
export async function clickPlay(page: Page) {
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

export async function findPlayer(page: Page) {
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

// The idle diagnostic stays available without this opt-in. Expected bytes come
// from the reviewed installer and frozen package, before the browser is launched.
export async function observedGraph() {
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

export const observeCapture = ({ fallback }: { fallback: boolean }) => {
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
};

export const observeFrames = () => {
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
};

export const captureReadiness = () => ({
  epochMs: performance.timeOrigin + performance.now(), timeOrigin: performance.timeOrigin, visibility: document.visibilityState,
  muted: window.__capturePlayer.isMuted(), userActivation: navigator.userActivation.hasBeenActive,
  media: Array.from(document.querySelectorAll('audio[src], video')).map(element => {
    const media = element as HTMLMediaElement;
    return { src: media.currentSrc, readyState: media.readyState, currentTime: media.currentTime, seeking: media.seeking, paused: media.paused, error: media.error?.message, buffered: Array.from({ length: media.buffered.length }, (_, index) => [media.buffered.start(index), media.buffered.end(index)]) };
  }),
  contexts: window.__captureContexts.map(context => ({ state: context.state, currentTime: context.currentTime, sampleRate: context.sampleRate, baseLatency: (context as AudioContext).baseLatency, outputLatency: (context as AudioContext).outputLatency })),
});

