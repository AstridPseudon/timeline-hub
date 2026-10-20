import { expect, test as base, type Page, type CDPSession } from '@playwright/test';
import type { PlayerRef } from '@remotion/player';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { CAPTURE_TIMELINE, TONES, createManagedTones, publishCaptureFixture, type Backend } from './player-audio-fixture';
import { audibleEdges, decodeMonitor, privateMonitor, requireAudibleDuration } from './player-audio-monitor';
import { editorUrl, resetFakeRuntimeBaseline } from './support';

// Opt-in diagnostic: preserve every PCM sample on the existing source-to-gain edge.
const nativeCursorWorklet = `
// Identity transformer only: returning false adds no active-source or tail-time hold.
class NativeCursor extends AudioWorkletProcessor {
  constructor({processorOptions: {reference}}) {
    super();
    this.reference = reference;
    this.cursor = null;
    this.maxError = 0;
  }
  process(inputs, outputs) {
    const input = inputs[0];
    const output = outputs[0];
    if (!input.length) {
      for (const channel of output) channel.fill(0);
      this.port.postMessage({contextFrame: currentFrame, frames: output[0].length, inputChannels: 0, outputChannels: output.length, outputIdentity: output.every(channel => channel.every(value => value === 0)), sourceStart: null, sourceEnd: this.cursor, maxError: this.maxError});
      return false;
    }
    if (input.length !== output.length) throw new Error('Channel count changed');
    for (let c = 0; c < input.length; c++) output[c].set(input[c]);
    const size = input[0].length;
    const firstInput = this.cursor === null;
    if (this.cursor === null) {
      const first = input[0].findIndex(value => value !== 0);
      // The known PCM source starts with sample0=0 and sample1!=0. There is
      // no phase fitting, search, dropped sample or source-time adjustment.
      if (first !== -1) this.cursor = 1 - first;
    }
    const start = this.cursor;
    if (start !== null) {
      for (let i = 0; i < size; i++) for (let c = 0; c < input.length; c++) {
        const expected = this.reference[c][start + i] ?? 0;
        this.maxError = Math.max(this.maxError, Math.abs(input[c][i] - expected));
      }
      this.cursor += size;
    }
    this.port.postMessage({contextFrame: currentFrame, frames: size, inputChannels: input.length, outputChannels: output.length,
      outputIdentity: input.every((channel, c) => channel.every((value, i) => Object.is(value, output[c][i]))), sourceStart: start, sourceEnd: this.cursor, maxError: this.maxError,
      firstInput: firstInput && start !== null ? input.map(channel => Array.from(channel)) : undefined});
    return false;
  }
}
registerProcessor('native-cursor', NativeCursor);
`;

type NativeCursorRecord = { contextFrame: number; frames: number; inputChannels: number; outputChannels: number; outputIdentity: boolean; sourceStart: number | null; sourceEnd: number | null; maxError: number; firstInput?: number[][] };

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
      media: { currentTime: number; paused: boolean; seeking: boolean; readyState: number; muted: boolean; volume: number; playbackRate: number }[];
      contexts: { currentTime: number; state: AudioContextState; output: AudioTimestamp }[];
    }[];
    __captureEvents: Record<string, unknown>[];
    __captureContexts: BaseAudioContext[];
    __captureSources: { node: MediaElementAudioSourceNode; element: HTMLMediaElement; context: AudioContext; connections: Set<AudioNode> }[];
    __captureCursorSetup?: Record<string, unknown>;
    __captureCursor?: { records: NativeCursorRecord[]; sampleRate: number; sourceLength: number; errors: string[] };
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

async function nativeTelemetry(page: Page, browserSession: CDPSession, outputPath: (name: string) => string) {
  const session = await page.context().newCDPSession(page);
  const media: { type: string; payload: unknown }[] = [];
  session.on('Media.playerEventsAdded', payload => media.push({ type: 'playerEventsAdded', payload }));
  session.on('Media.playerPropertiesChanged', payload => media.push({ type: 'playerPropertiesChanged', payload }));
  session.on('Media.playerMessagesLogged', payload => media.push({ type: 'playerMessagesLogged', payload }));
  session.on('Media.playerErrorsRaised', payload => media.push({ type: 'playerErrorsRaised', payload }));
  await session.send('Media.enable');
  const { categories } = await browserSession.send('Tracing.getCategories');
  const selected = categories.filter(category => /audio|media/.test(category));
  if (!selected.length) throw new Error('No installed native audio trace categories');
  const completed = new Promise<{ stream?: string }>(resolve => browserSession.once('Tracing.tracingComplete', resolve));
  await browserSession.send('Tracing.start', { categories: selected.join(','), transferMode: 'ReturnAsStream' });
  return async () => {
    try {
      await writeFile(outputPath('native-media-events.json'), JSON.stringify({ categories, selected, media }, null, 2));
      await browserSession.send('Tracing.end');
      const { stream } = await completed;
      if (!stream) throw new Error('Native audio trace has no stream');
      const chunks: Buffer[] = [];
      try {
        for (;;) {
          const chunk = await browserSession.send('IO.read', { handle: stream, size: 1024 * 1024 });
          chunks.push(Buffer.from(chunk.data, chunk.base64Encoded ? 'base64' : 'utf8'));
          if (chunk.eof) break;
        }
      } finally { await browserSession.send('IO.close', { handle: stream }); }
      await writeFile(outputPath('native-audio-trace.json'), Buffer.concat(chunks));
    } finally { await session.detach(); }
  };
}

async function installNativeCursor(page: Page, wavePath: string) {
  const encoded = (await readFile(wavePath)).toString('base64');
  return evaluateWithoutGesture(page, async ({ encoded, moduleSource }) => {
    const setup: Record<string, unknown> = { phase: 'source-parse', userActivation: navigator.userActivation.hasBeenActive };
    window.__captureCursorSetup = setup;
    const bytes = Uint8Array.from(atob(encoded), character => character.charCodeAt(0));
    const wav = new DataView(bytes.buffer);
    const text = (offset: number) => String.fromCharCode(...bytes.slice(offset, offset + 4));
    if (text(0) !== 'RIFF' || text(8) !== 'WAVE') throw new Error('Expected the original PCM WAV');
    let channels = 0, sampleRate = 0, start = 0, length = 0;
    for (let offset = 12; offset + 8 <= bytes.length;) {
      const size = wav.getUint32(offset + 4, true);
      if (text(offset) === 'fmt ') {
        if (wav.getUint16(offset + 8, true) !== 1 || wav.getUint16(offset + 22, true) !== 16) throw new Error('Expected PCM16');
        channels = wav.getUint16(offset + 10, true);
        sampleRate = wav.getUint32(offset + 12, true);
      }
      if (text(offset) === 'data') { start = offset + 8; length = size; }
      offset += 8 + size + size % 2;
    }
    if (channels !== 2 || sampleRate !== 48000 || length !== 144000 * 4) throw new Error('Unexpected original source format');
    const reference = Array.from({ length: channels }, (_, channel) => Float32Array.from(
      { length: length / channels / 2 }, (_, frame) => wav.getInt16(start + (frame * channels + channel) * 2, true) / 32768));
    const sources = window.__captureSources.filter(source => source.element.isConnected && source.connections.size > 0);
    if (sources.length !== 1) throw new Error('Expected one active amplified native source');
    const { node, element, context, connections } = sources[0];
    if (connections.size !== 1 || !element.paused || element.currentTime !== 0 || context.state !== 'suspended') throw new Error('Control must precede measured native playback');
    if (context.sampleRate !== sampleRate) throw new Error('Native source/context rate mismatch');
    const destination = [...connections][0];
    const contextTime = context.currentTime;
    Object.assign(setup, { phase: 'module-load', sampleRate, channels, sourceLength: reference[0].length,
      contextState: context.state, contextTime, mediaTime: element.currentTime, nativeMuted: element.muted, nativeVolume: element.volume });
    const capture = { records: [] as NativeCursorRecord[], sampleRate, sourceLength: reference[0].length, errors: [] as string[] };
    window.__captureCursor = capture;
    try {
      const url = URL.createObjectURL(new Blob([moduleSource], { type: 'text/javascript' }));
      try { await context.audioWorklet.addModule(url); } finally { URL.revokeObjectURL(url); }
      setup.phase = 'node-create';
      const observer = new AudioWorkletNode(context, 'native-cursor', {
        numberOfInputs: 1, numberOfOutputs: 1, outputChannelCount: [channels],
        channelCount: channels, channelCountMode: 'explicit', channelInterpretation: 'discrete', processorOptions: { reference },
      });
      observer.port.onmessage = event => capture.records.push(event.data as NativeCursorRecord);
      observer.onprocessorerror = () => capture.errors.push('Native cursor processor error');
      node.disconnect(destination);
      node.connect(observer);
      observer.connect(destination);
      if (context.state !== 'suspended' || context.currentTime !== contextTime || element.currentTime !== 0 || !element.paused) throw new Error('Observer activated playback');
      Object.assign(setup, { phase: 'installed', contextTimeAfter: context.currentTime, contextStateAfter: context.state });
      return setup;
    } catch (error) {
      setup.error = String(error);
      capture.errors.push(String(error));
      throw error;
    }
  }, { encoded, moduleSource: nativeCursorWorklet });
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
      nativeFlags: process.env.PLAYER_AUDIO_NATIVE_FLAGS === '1', cursorControl: process.env.PLAYER_AUDIO_CURSOR_CONTROL === '1', nativeTrace: process.env.PLAYER_AUDIO_NATIVE_TRACE === '1',
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
        let stopTelemetry: (() => Promise<void>) | undefined;
        try {
          if (process.env.PLAYER_AUDIO_NATIVE_TRACE === '1') stopTelemetry = await nativeTelemetry(page, cdp, name => testInfo.outputPath(name));
          await page.addInitScript(({ fallback, cursorControl, nativeFlags }) => {
            window.__captureBackends = { elements: [], buffers: 0, audibleBuffers: 0 };
            window.__captureEvents = [{ type: 'init', epochMs: performance.timeOrigin + performance.now(), userActivation: navigator.userActivation.hasBeenActive }];
            window.__captureContexts = [];
            window.__captureSources = [];
            for (const type of ['click', 'playing', 'waiting', 'stalled', 'canplay', 'seeking', 'seeked', 'pause', 'ended', 'volumechange', 'visibilitychange']) {
              document.addEventListener(type, event => {
                const media = event.target instanceof HTMLMediaElement ? event.target : null;
                window.__captureEvents.push({ type, epochMs: performance.timeOrigin + performance.now(), src: media?.currentSrc, currentTime: media?.currentTime, readyState: media?.readyState, muted: media?.muted, volume: media?.volume, playbackRate: media?.playbackRate, visibility: document.visibilityState, playerFrame: window.__capturePlayer?.getCurrentFrame() });
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
            if (nativeFlags) {
              const descriptor = Object.getOwnPropertyDescriptor(HTMLMediaElement.prototype, 'muted');
              if (!descriptor?.get || !descriptor.set) throw new Error('No native muted accessor');
              const set = descriptor.set, get = descriptor.get;
              Object.defineProperty(HTMLMediaElement.prototype, 'muted', { ...descriptor, set(value: boolean) {
                const before = get.call(this);
                set.call(this, value);
                window.__captureEvents.push({
                  type: 'native-muted-set', epochMs: performance.timeOrigin + performance.now(),
                  before, value, after: get.call(this), src: this.currentSrc || this.src,
                  currentTime: this.currentTime, volume: this.volume, playbackRate: this.playbackRate,
                  playerFrame: window.__capturePlayer?.getCurrentFrame(),
                });
              } });
            }
            const nativePlay = HTMLMediaElement.prototype.play;
            HTMLMediaElement.prototype.play = function () {
              window.__captureEvents.push({
                type: 'media-play-call', epochMs: performance.timeOrigin + performance.now(),
                src: this.currentSrc || this.src, currentTime: this.currentTime, muted: this.muted, volume: this.volume, playbackRate: this.playbackRate,
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
              const node = mediaSource.call(this, element);
              if (cursorControl) {
                const connections = new Set<AudioNode>();
                const connect = node.connect.bind(node), disconnect = node.disconnect.bind(node);
                node.connect = ((destination: AudioNode | AudioParam, ...ports: number[]) => {
                  const result = Reflect.apply(connect, node, [destination, ...ports]);
                  if (destination instanceof AudioNode) connections.add(destination);
                  return result;
                }) as typeof node.connect;
                node.disconnect = ((...args: unknown[]) => {
                  Reflect.apply(disconnect, node, args);
                  if (!args.length) connections.clear();
                  else if (args[0] instanceof AudioNode) connections.delete(args[0]);
                  else throw new Error('Unobserved source port disconnection');
                }) as typeof node.disconnect;
                window.__captureSources.push({ node, element, context: this, connections });
              }
              return node;
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
          }, { fallback: options.fallback ?? false, cursorControl: process.env.PLAYER_AUDIO_CURSOR_CONTROL === '1', nativeFlags: process.env.PLAYER_AUDIO_NATIVE_FLAGS === '1' });
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
              return { src: media.currentSrc, readyState: media.readyState, currentTime: media.currentTime, paused: media.paused, muted: media.muted, volume: media.volume, playbackRate: media.playbackRate };
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
                  return { currentTime: media.currentTime, paused: media.paused, seeking: media.seeking, readyState: media.readyState, muted: media.muted, volume: media.volume, playbackRate: media.playbackRate };
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
          if (process.env.PLAYER_AUDIO_CURSOR_CONTROL === '1') {
            if (!options.fade || backends.length !== 1 || backends[0] !== 'amplified') throw new Error('Native cursor control requires the original positive amplified fade');
            try { results.nativeCursorSetup = await installNativeCursor(page, join(directory, 'amplified.wav')); } catch (error) {
              results.nativeCursorSetupError = String(error);
              throw error;
            }
          }
          const readiness = await evaluateWithoutGesture(page, () => ({
            epochMs: performance.timeOrigin + performance.now(), timeOrigin: performance.timeOrigin, visibility: document.visibilityState,
            muted: window.__capturePlayer.isMuted(), userActivation: navigator.userActivation.hasBeenActive,
            media: Array.from(document.querySelectorAll('audio[src], video')).map(element => {
              const media = element as HTMLMediaElement;
              return { src: media.currentSrc, readyState: media.readyState, currentTime: media.currentTime, seeking: media.seeking, paused: media.paused, muted: media.muted, volume: media.volume, playbackRate: media.playbackRate, error: media.error?.message, buffered: Array.from({ length: media.buffered.length }, (_, index) => [media.buffered.start(index), media.buffered.end(index)]) };
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
          if (process.env.PLAYER_AUDIO_CURSOR_CONTROL === '1') {
            const cursor = await evaluateWithoutGesture(page, () => window.__captureCursor);
            results.nativeCursor = cursor;
            expect(cursor, 'native input cursor observations').toBeDefined();
            expect.soft(cursor!.errors).toEqual([]);
            expect.soft(cursor!.records.every(record => record.outputChannels === 2 && record.outputIdentity), 'all native output channels/samples pass unchanged').toBe(true);
            expect.soft(cursor!.records.length).toBeGreaterThan(1000);
            expect.soft(cursor!.records.filter(record => record.sourceStart !== null).length, 'actual native PCM quanta').toBeGreaterThan(1000);
            expect.soft(cursor!.records.some(record => record.sourceEnd !== null && record.sourceEnd >= cursor!.sourceLength), 'full original source cursor').toBe(true);
            expect.soft(Math.max(...cursor!.records.map(record => record.maxError)), 'all native input samples match the original managed PCM').toBeLessThan(1 / 32768);
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
          if (process.env.PLAYER_AUDIO_CURSOR_CONTROL === '1') {
            try {
              const diagnostic = await evaluateWithoutGesture(page, () => ({ cursor: window.__captureCursor, setup: window.__captureCursorSetup }));
              results.nativeCursor = diagnostic.cursor ?? results.nativeCursor ?? null;
              results.nativeCursorSetup = diagnostic.setup ?? results.nativeCursorSetup ?? null;
            } catch (error) { results.nativeCursorReadError = String(error); }
          }
          results[name] = { ...results[name] as object, lifecycleEvents: await evaluateWithoutGesture(page, () => window.__captureEvents).catch(() => null) };
          try { if (consumer) results[`${name}-consumer`] = await consumer.close(); } finally {
            try { await stopTelemetry?.(); } finally { await page.close(); }
          }
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
