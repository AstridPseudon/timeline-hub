import assert from 'node:assert/strict';
import {test} from 'node:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';

const root = fileURLToPath(new URL('../../', import.meta.url));
const script = path.join(root, 'scripts/patches/remotion-4.0.509-audio-resume.mjs');
const targets = [
  ['CJS', 'dist/cjs/audio/shared-audio-tags.js', '(0, wait_until_actually_resumed_js_1.waitUntilActuallyResumed)(ctxAndGain.audioContext, logLevel, abortController.signal)'],
  ['ESM', 'dist/esm/index.mjs', 'waitUntilActuallyResumed(ctxAndGain.audioContext, logLevel, abortController.signal)'],
];
const sourceRoot = process.env.REMOTION_SOURCE_ROOT ?? path.join(root, 'node_modules/remotion');
const deferred = () => {
  let resolve, reject;
  const promise = new Promise((yes, no) => {resolve = yes; reject = no;});
  return {promise, resolve, reject};
};
const flush = async () => {for (let n = 0; n < 12; n++) await Promise.resolve();};

// Extract the actual generated owner callback, leaving predicate, ramp, nodes,
// native-return promise, rejection handler and finally behavior intact.
function callbackBody(source, form) {
  const start = form === 'CJS'
    ? 'const resume = (0, react_1.useCallback)(() => {'
    : 'const resume = useCallback10(() => {';
  const offset = source.indexOf(start);
  assert.notEqual(offset, -1);
  const end = source.indexOf('}, [ctxAndGain, _experimentalKeepAudioContextAlive, logLevel]);', offset);
  assert.notEqual(end, -1);
  return source.slice(offset + start.length, end);
}

function harness(source, form) {
  const native = deferred(), pendingOutput = [], warnings = [];
  const isResuming = {current: null};
  const nextResumeAttemptId = {current: 0};
  const audioContextIsPlayingEventually = {current: false};
  const audioContext = {currentTime: 0};
  const ctxAndGain = {audioContext, resume: () => native.promise,
    gainNode: {gain: {cancelScheduledValues() {}, setValueAtTime() {}, linearRampToValueAtTime() {}}}};
  const wait = (context) => {
    assert.equal(context, audioContext);
    const output = deferred();
    pendingOutput.push(output);
    return output.promise;
  };
  const Log = {warn: (...args) => warnings.push(args)};
  const resume = new Function('ctxAndGain', 'audioContextIsPlayingEventually',
    'nodesToResume', 'isResuming', 'nextResumeAttemptId', 'logLevel', 'waitUntilActuallyResumed',
    'wait_until_actually_resumed_js_1', 'Log', 'log_js_1', '_experimentalKeepAudioContextAlive',
    `return function(){${callbackBody(source, form)}}`)(ctxAndGain,
      audioContextIsPlayingEventually, {current: new Map()}, isResuming, nextResumeAttemptId,
      'warn', wait, {waitUntilActuallyResumed: wait}, Log, {Log}, false);
  return {native, pendingOutput, warnings, isResuming, resume,
    outputAdvances() {audioContext.currentTime += 0.1; pendingOutput.forEach(output => output.resolve());}};
}

async function fulfillmentInvariant(source, form) {
  const h = harness(source, form);
  const nativeReturn = h.resume();
  const sharedWait = h.isResuming.current?.promise;
  assert.ok(sharedWait);
  let released = false;
  sharedWait.then(() => {released = true;});
  // This real race is the red criterion: output can appear ready while the
  // native resume operation is unresolved. Only already-created waits see it.
  h.outputAdvances();
  await flush();
  assert.equal(released, false, 'apparent output readiness cannot release before native fulfillment');
  assert.equal(h.pendingOutput.length, 0, 'output sampling must start after native fulfillment');
  assert.equal(h.isResuming.current?.promise, sharedWait);
  h.native.resolve();
  await nativeReturn;
  await flush();
  assert.equal(h.pendingOutput.length, 1);
  assert.equal(released, false, 'native fulfillment alone is not output readiness');
  h.outputAdvances();
  await sharedWait;
  await flush();
  assert.equal(released, true);
  assert.equal(h.isResuming.current, null);
}

async function rejectionInvariant(source, form) {
  const h = harness(source, form), error = new Error('native resume rejected');
  const nativeReturn = h.resume(), sharedWait = h.isResuming.current?.promise;
  h.native.reject(error);
  await nativeReturn; // Existing public behavior swallows logged native failure.
  await sharedWait;   // Existing failure behavior releases rather than deadlocks.
  await flush();
  assert.equal(h.isResuming.current, null);
  assert.equal(h.warnings.length, 1);
  assert.equal(h.warnings[0].at(-1), error);
}

test('Remotion 4.0.509 CJS and ESM native-fulfillment fence (original red, patched green)', async t => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'remotion-resume-semantic-'));
  try {
    const original = new Map();
    for (const [form, relative, waitName] of targets) {
      const installed = fs.readFileSync(path.join(sourceRoot, relative), 'utf8');
      const before = `${waitName}.then(resolve);`;
      const after = `resumePromise.then(() => ${waitName}.then(resolve), () => {});`;
      // Allow rerunning after installation; reconstruct ONLY the exact guarded
      // one-line delta. The guard script still validates full-file fingerprints.
      const pristine = installed.includes(after) ? installed.replace(after, before) : installed;
      original.set(form, pristine);
      const file = path.join(fixture, 'node_modules/remotion', relative);
      fs.mkdirSync(path.dirname(file), {recursive: true});
      fs.writeFileSync(file, pristine);
    }
    fs.copyFileSync(path.join(sourceRoot, 'package.json'), path.join(fixture, 'node_modules/remotion/package.json'));
    for (const relative of ['package.json', 'dist/cjs/use-player-methods.js', 'dist/esm/index.mjs', 'dist/cjs/use-playback.js', 'dist/cjs/PlayerUI.js']) {
      const destination = path.join(fixture, 'node_modules/@remotion/player', relative);
      fs.mkdirSync(path.dirname(destination), {recursive: true});
      fs.copyFileSync(path.join(root, 'node_modules/@remotion/player', relative), destination);
    }
    execFileSync(process.execPath, [script, '--apply', '--root', fixture], {encoding: 'utf8'});
    for (const [form, relative, waitName] of targets) {
      const before = `${waitName}.then(resolve);`;
      const after = `resumePromise.then(() => ${waitName}.then(resolve), () => {});`;
      const pristine = original.get(form), patched = fs.readFileSync(path.join(fixture, 'node_modules/remotion', relative), 'utf8');
      await t.test(`${form}: exact D3 delta only`, () => {
        assert.equal(pristine.split(before).length - 1, 1);
        assert.equal(patched, pristine.replace(before, after));
      });
      await t.test(`${form}: original MUST fail fulfillment invariant`, async () => {
        await assert.rejects(fulfillmentInvariant(pristine, form), /apparent output readiness cannot release before native fulfillment/);
      });
      await t.test(`${form}: candidate waits native then fresh output advance`, () => fulfillmentInvariant(patched, form));
      await t.test(`${form}: rejection behavior retained in both forms`, async () => {
        await rejectionInvariant(pristine, form);
        await rejectionInvariant(patched, form);
      });
    }
  } finally {
    fs.rmSync(fixture, {recursive: true, force: true});
  }
});

// Run both distributed hook implementations, with two callers sharing the
// Player's actual imperative ref (transport and playback/media-session hooks).
function playerHarness(source, form, {buffered = true, context = true, state = 'suspended', failure, hooks, clock = performance, onPlaying = () => {}, mount = hook => [hook(), hook()]} = {}) {
  const events = [], waits = [], cleanups = [], listeners = new Set(), nativeTimes = [];
  const fail = operation => {
    if (failure !== operation) return;
    failure = null;
    throw new Error(`${operation} failed`);
  };
  const timeline = {frameRef: {current: {test: 0}}, imperativePlaying: {current: false},
    audioAndVideoTags: {current: [{play() {nativeTimes.push(clock.now()); events.push('native');}}]}};
  const audio = {
    audioContext: {currentTime: 0.15, state,
      createBufferSource() {assert.fail('startup must not inject an audio source');}},
    audioSyncAnchor: {value: 0},
    audioSyncAnchorEmitter: {dispatch() {events.push('anchor-changed');}},
    resume() {
      fail('resume'); events.push('resume'); waits.push(deferred());
      if (failure === 'resume-rejection') {failure = null; return Promise.reject(new Error('resume rejected'));}
      return Promise.resolve();
    },
    suspend() {
      events.push('suspend'); fail('suspend');
      if (failure === 'suspend-rejection') {failure = null; return Promise.reject(new Error('suspend rejected'));}
    },
    getIsResumingAudioContext() {fail('getIsResumingAudioContext'); return waits.at(-1).promise;},
  };
  const buffering = {buffering: {current: !buffered}, listenForResume(fn) {
    listeners.add(fn); return {remove: () => listeners.delete(fn)};
  }};
  const emitter = {dispatchPlay() {events.push('play');}, dispatchPause() {events.push('pause');}, dispatchSeek(frame) {events.push(['seek', frame]);}};
  const setters = {setPlaying(value) {events.push(['playing', value]); onPlaying(value);}, setFrame(fn) {timeline.frameRef.current = fn(timeline.frameRef.current);}};
  const core = {
    Timeline: {useTimelineSetFrame: () => setters.setFrame, clampFrameToCompositionRange: (frame, duration) => Math.min(duration - 1, Math.max(0, frame))},
    TimelinePosition: {clampFrameToCompositionRange: (frame, duration) => Math.min(duration - 1, Math.max(0, frame))},
    SetTimelineContext: setters, SharedAudioContext: context ? audio : null,
    SharedAudioTagsContext: {numberOfAudioTags: 1, playAllAudios() {events.push('warm-tags');}},
    SetMediaVolumeContext: {setPlayerMuted(value) {events.push(['muted', value]);}},
    BufferingContextReact: buffering,
    usePlaybackRate: () => ({playbackRate: 1}), useLogLevel: () => 'warn',
    useVideo: () => ({id: 'test', durationInFrames: 120}),
    useUnsafeVideoConfig: () => ({id: 'test', durationInFrames: 120, fps: 30}),
  };
  const react = hooks ?? {useContext: value => value, useRef: current => ({current}), useCallback: fn => fn,
    useMemo: fn => fn(), useEffect: fn => cleanups.push(fn())};
  const start = source.indexOf(form === 'CJS' ? 'const pendingPlayerStarts' : 'var pendingPlayerStarts');
  const originalStart = source.indexOf(form === 'CJS' ? 'const usePlayerMethods =' : 'var usePlayerMethods =');
  const end = source.indexOf(form === 'CJS' ? 'exports.usePlayerMethods =' : '// src/browser-mediasession.ts', originalStart);
  assert.ok(originalStart >= 0 && end > originalStart);
  const body = source.slice(start < 0 ? originalStart : start, end);
  const anchor = args => {
    assert.equal(args.force, true);
    assert.equal(args.absoluteTimeInSeconds, timeline.frameRef.current.test / 30);
    assert.equal(args.globalPlaybackRate, 1);
    args.audioSyncAnchor.value = args.audioContext.currentTime - args.absoluteTimeInSeconds;
    events.push('anchor'); return true;
  };
  const hook = new Function('react_1', 'remotion_1', 'emitter_context_js_1', 'timeline_imperative_context_js_1',
    'useContext3', 'Internals5', 'useRemotionEnvironment', 'PlayerEventEmitterContext',
    'useRef2', 'useCallback', 'useMemo2', 'getTimelineImperativeContext', 'useEffect', 'setGlobalTimeAnchor', 'set_global_time_anchor_js_1', 'performance',
    `${body};return usePlayerMethods;`)(react, {Internals: core, useRemotionEnvironment: () => ({isPlayer: true})},
      {PlayerEventEmitterContext: emitter}, {getTimelineImperativeContext: () => timeline},
      react.useContext, core, () => ({isPlayer: true}), emitter, react.useRef,
      react.useCallback, react.useMemo, () => timeline, react.useEffect, anchor, {setGlobalTimeAnchor: anchor}, clock);
  const [methods, other] = mount(hook);
  return {methods, other, events, waits, timeline, listeners, nativeTimes,
    unmount() {cleanups.forEach(fn => fn?.());},
    unblock() {buffering.buffering.current = false; [...listeners].forEach(fn => fn());}};
}

async function startupInvariant(source, form) {
  const h = playerHarness(source, form);
  h.methods.play({});
  assert.equal(h.events.includes('native'), false, 'native source must wait for output readiness');
  assert.equal(h.methods.isPlaying(), false, 'pending readiness is not playing');
  assert.equal(h.events.some(event => Array.isArray(event) && event[0] === 'playing'), false);
  h.waits[0].resolve('resumed');
  await flush();
  assert.deepEqual(h.events, ['resume', 'anchor', 'anchor-changed', ['playing', true], 'warm-tags', 'native', 'play']);
  const origin = h.other.takePlaybackStartTime();
  assert.ok(origin <= h.nativeTimes[0], 'frame origin is established before the source starts');
  const playback = form === 'CJS'
    ? fs.readFileSync(path.join(root, 'node_modules/@remotion/player/dist/cjs/use-playback.js'), 'utf8') : source;
  const expression = playback.match(/let startedTime = ([^;]+);/)[1];
  const actualOrigin = new Function('takePlaybackStartTime', 'performance', `return ${expression}`)(() => origin, {now: () => origin + 100});
  assert.equal(actualOrigin, origin, 'playback consumes the ready origin instead of resetting it later');
  assert.ok(h.methods.takePlaybackStartTime() >= origin, 'later loop restarts use a fresh origin');
}

test('pinned Player startup readiness, cancellation and replay in CJS and ESM', async t => {
  const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'remotion-player-semantic-'));
  try {
    const files = [
      ['remotion', sourceRoot, ['package.json', ...targets.map(([, relative]) => relative)]],
      ['@remotion/player', path.join(root, 'node_modules/@remotion/player'), ['package.json', 'dist/cjs/use-player-methods.js', 'dist/esm/index.mjs', 'dist/cjs/use-playback.js', 'dist/cjs/PlayerUI.js']],
    ];
    for (const [name, source, relatives] of files) for (const relative of relatives) {
      const destination = path.join(fixture, 'node_modules', name, relative);
      fs.mkdirSync(path.dirname(destination), {recursive: true});
      fs.copyFileSync(path.join(source, relative), destination);
    }
    execFileSync(process.execPath, [script, '--revert', '--root', fixture]);
    const originals = new Map(['CJS', 'ESM'].map(form => [form, fs.readFileSync(path.join(fixture, 'node_modules/@remotion/player', form === 'CJS' ? 'dist/cjs/use-player-methods.js' : 'dist/esm/index.mjs'), 'utf8')]));
    execFileSync(process.execPath, [script, '--apply', '--root', fixture]);
    for (const form of ['CJS', 'ESM']) {
      const source = fs.readFileSync(path.join(fixture, 'node_modules/@remotion/player', form === 'CJS' ? 'dist/cjs/use-player-methods.js' : 'dist/esm/index.mjs'), 'utf8');
      await t.test(`${form}: original starts source before readiness (red)`, async () => {
        await assert.rejects(startupInvariant(originals.get(form), form), /native source must wait for output readiness/);
      });
      await t.test(`${form}: context readiness precedes both media and frame clock`, () => startupInvariant(source, form));
      for (const operation of ['pause', 'seek', 'pauseAndReturnToPlayStart', 'toggle', 'unmount']) {
        await t.test(`${form}: ${operation} cancels across hook instances; replay cannot release stale start`, async () => {
          const h = playerHarness(source, form);
          h.methods.play({});
          if (operation === 'unmount') h.unmount();
          else h.other[operation](20);
          assert.equal(h.methods.isPlaying(), false);
          h.methods.play({});
          h.waits[0].resolve('resumed');
          await flush();
          assert.equal(h.events.includes('native'), false);
          h.waits[1].resolve('resumed');
          await flush();
          assert.equal(h.events.filter(event => event === 'native').length, 1);
        });
      }
      await t.test(`${form}: buffering gates startup; pause removes its listener`, async () => {
        const h = playerHarness(source, form, {buffered: false});
        h.methods.play({}); h.waits[0].resolve('resumed'); await flush();
        assert.equal(h.listeners.size, 1);
        assert.equal(h.events.includes('native'), false);
        h.other.pause(); assert.equal(h.listeners.size, 0);
        h.unblock(); await flush(); assert.equal(h.events.includes('native'), false);
        h.methods.play({}); h.waits[1].resolve('resumed'); await flush();
        assert.equal(h.events.filter(event => event === 'native').length, 1);
      });
      await t.test(`${form}: duplicate play, warm replay and last-frame rewind`, async () => {
        const h = playerHarness(source, form);
        h.methods.play({}); h.other.play({}); assert.equal(h.waits.length, 1);
        h.waits[0].resolve('resumed'); await flush(); h.other.pause();
        h.timeline.frameRef.current.test = 119;
        h.methods.play({}); assert.equal(h.methods.getCurrentFrame(), 0);
        h.waits[1].resolve('resumed'); await flush();
        assert.equal(h.events.filter(event => event === 'native').length, 2);
      });
      await t.test(`${form}: failure retains muted continuation; cancellation stays stopped`, async () => {
        const h = playerHarness(source, form);
        h.methods.play({}); h.waits[0].resolve('cancelled'); await flush();
        assert.equal(h.methods.isPlaying(), false); assert.equal(h.events.includes('native'), false);
        h.methods.play({}); h.waits[1].resolve('failed'); await flush();
        assert.ok(h.events.some(event => Array.isArray(event) && event[0] === 'muted' && event[1] === true));
        assert.equal(h.events.includes('native'), true);
        assert.equal(h.events.includes('warm-tags'), false);
      });
      await t.test(`${form}: closed context retains failed-context fallback without creating a source`, async () => {
        const h = playerHarness(source, form, {state: 'closed'});
        h.methods.play({});
        h.waits[0].resolve('failed'); await flush();
        assert.equal(h.events.includes('native'), true);
        assert.ok(h.events.some(event => Array.isArray(event) && event[0] === 'muted' && event[1] === true));
      });
      await t.test(`${form}: rejected readiness cancels playback`, async () => {
        const h = playerHarness(source, form);
        h.methods.play({}); h.waits[0].reject(new Error('readiness rejected')); await flush();
        assert.equal(h.methods.isPlaying(), false); assert.equal(h.methods.isStarting(), false);
        assert.equal(h.events.includes('native'), false);
      });
      for (const failure of ['resume', 'resume-rejection', 'getIsResumingAudioContext']) {
        await t.test(`${form}: ${failure} failure clears pending startup and permits replay`, async () => {
          const h = playerHarness(source, form, {failure});
          assert.doesNotThrow(() => h.methods.play({}));
          await flush();
          assert.equal(h.methods.isStarting(), false);
          assert.equal(h.methods.isPlaying(), false);
          assert.equal(h.events.includes('native'), false);
          h.methods.play({}); h.waits.at(-1).resolve('resumed'); await flush();
          assert.equal(h.events.filter(event => event === 'native').length, 1);
          assert.equal(h.methods.isStarting(), false);
        });
      }
      for (const failure of ['suspend', 'suspend-rejection']) {
        await t.test(`${form}: cancellation survives ${failure} failure`, async () => {
          const h = playerHarness(source, form, {failure});
          h.methods.play({}); assert.doesNotThrow(() => h.other.toggle());
          h.waits[0].resolve('resumed'); await flush();
          assert.equal(h.methods.isStarting(), false); assert.equal(h.events.includes('native'), false);
        });
      }
      await t.test(`${form}: stale rejected readiness cannot cancel a newer play`, async () => {
        const h = playerHarness(source, form);
        h.methods.play({}); h.other.toggle(); h.methods.play({});
        h.waits[0].reject(new Error('old readiness rejected')); await flush();
        assert.equal(h.methods.isStarting(), true);
        assert.equal(h.events.includes('native'), false);
        h.waits[1].resolve('resumed'); await flush();
        assert.equal(h.events.filter(event => event === 'native').length, 1);
      });
      await t.test(`${form}: public PlayerUI toggle cancels pending startup`, async () => {
        const h = playerHarness(source, form);
        const ui = form === 'CJS' ? fs.readFileSync(path.join(root, 'node_modules/@remotion/player/dist/cjs/PlayerUI.js'), 'utf8') : source;
        const marker = form === 'CJS' ? 'const toggle = (0, react_1.useCallback)((e) => {' : 'const toggle = useCallback10((e) => {';
        const start = ui.indexOf(marker);
        const end = ui.indexOf('}, [play, player]);', start);
        assert.ok(start >= 0 && end > start);
        const toggle = new Function('player', 'play', `return e => {${ui.slice(start + marker.length, end)}}`)(h.methods, h.methods.play);
        toggle({}); assert.equal(h.other.isStarting(), true);
        toggle({}); assert.equal(h.other.isStarting(), false);
        h.waits[0].resolve('resumed'); await flush();
        assert.equal(h.events.includes('native'), false);
      });
      await t.test(`${form}: native-only without an AudioContext still starts`, async () => {
        const h = playerHarness(source, form, {context: false});
        h.methods.play({}); await flush(); assert.equal(h.events.includes('native'), true);
      });
    }
  } finally {fs.rmSync(fixture, {recursive: true, force: true});}
});


test('real React 18 StrictMode rerenders preserve pending readiness; another hook can cancel it', async () => {
  const React = await import('react');
  const {createRoot} = await import('react-dom/client');
  const {JSDOM} = await import('jsdom');
  const dom = new JSDOM('<div id="root"></div>');
  const previous = {window: globalThis.window, document: globalThis.document, act: globalThis.IS_REACT_ACT_ENVIRONMENT};
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const renderer = createRoot(document.getElementById('root'));
  const rerenders = React.createContext(0);
  let render, idleSuspensions = 0;
  const playback = fs.readFileSync(path.join(root, 'node_modules/@remotion/player/dist/cjs/use-playback.js'), 'utf8');
  const idleStart = playback.indexOf('        if (!playing) {');
  const idleEnd = playback.indexOf('        if ((sharedAudioContext', idleStart);
  assert.ok(idleStart > 0 && idleEnd > idleStart);
  const idleEffect = new Function('isStarting', 'sharedAudioContext', `var _a; const playing = false; ${playback.slice(idleStart, idleEnd)}`);
  try {
    const source = fs.readFileSync(path.join(root, 'node_modules/@remotion/player/dist/cjs/use-player-methods.js'), 'utf8');
    const h = playerHarness(source, 'CJS', {
      hooks: {...React, useContext(value) {React.useContext(rerenders); return value;}},
      mount(hook) {
        const methods = [];
        function Caller({index}) {
          const tick = React.useContext(rerenders);
          methods[index] = hook();
          React.useEffect(() => idleEffect(methods[index].isStarting, {suspend() {idleSuspensions++;}}), [tick]);
          return null;
        }
        render = value => React.createElement(React.StrictMode, null,
          React.createElement(rerenders.Provider, {value},
            React.createElement(Caller, {index: 0}), React.createElement(Caller, {index: 1})));
        React.act(() => renderer.render(render(0)));
        return methods;
      },
    });
    const suspendedBeforeStart = idleSuspensions;
    React.act(() => h.methods.play({}));
    assert.equal(h.other.isStarting(), true);
    React.act(() => renderer.render(render(1)));
    assert.equal(idleSuspensions, suspendedBeforeStart, 'paused effect rerender must not suspend pending context readiness');
    assert.equal(h.events.includes('native'), false);
    await React.act(async () => {h.waits[0].resolve('resumed'); await flush();});
    assert.equal(h.events.filter(event => event === 'native').length, 1);
    React.act(() => h.other.pause());
    React.act(() => h.methods.play({}));
    React.act(() => renderer.render(render(2)));
    React.act(() => h.other.seek(20));
    await React.act(async () => {h.waits[1].resolve('resumed'); await flush();});
    assert.equal(h.events.filter(event => event === 'native').length, 1);
    React.act(() => h.methods.play({}));
    React.act(() => renderer.unmount());
    await React.act(async () => {h.waits[2].resolve('resumed'); await flush();});
    assert.equal(h.events.filter(event => event === 'native').length, 1);
  } finally {
    React.act(() => renderer.unmount());
    dom.window.close();
    globalThis.window = previous.window;
    globalThis.document = previous.document;
    globalThis.IS_REACT_ACT_ENVIRONMENT = previous.act;
  }
});


// Run the distributed playback effect through React, delaying the playing
// commit's layout phase after native play. The control restores the pristine
// loop's late origin; capture clocks and comparison stay unchanged.
test('real React delayed playing commit retains the native-start origin in CJS and ESM', async t => {
  const React = await import('react');
  const {createRoot} = await import('react-dom/client');
  const {JSDOM} = await import('jsdom');
  const {createRequire} = await import('node:module');
  const require = createRequire(import.meta.url);
  const {calculateNextFrame} = require(path.join(root, 'node_modules/@remotion/player/dist/cjs/calculate-next-frame.js'));
  for (const form of ['CJS', 'ESM']) for (const lateOrigin of [false, true]) {
    await t.test(`${form}: ${lateOrigin ? 'late-effect origin control loses elapsed frames (red)' : 'shared origin survives a 100ms commit delay'}`, async () => {
      const dom = new JSDOM('<div id="root"></div>');
      const previous = {window: globalThis.window, document: globalThis.document, act: globalThis.IS_REACT_ACT_ENVIRONMENT};
      globalThis.window = dom.window;
      globalThis.document = dom.window.document;
      globalThis.IS_REACT_ACT_ENVIRONMENT = true;
      const renderer = createRoot(document.getElementById('root'));
      let now = 1000, notifyPlaying;
      const clock = {now: () => now};
      const rafs = new Map();
      let nextRaf = 0, effectAt;
      const source = fs.readFileSync(path.join(root, 'node_modules/@remotion/player', form === 'CJS' ? 'dist/cjs/use-player-methods.js' : 'dist/esm/index.mjs'), 'utf8');
      const playback = form === 'CJS' ? fs.readFileSync(path.join(root, 'node_modules/@remotion/player/dist/cjs/use-playback.js'), 'utf8') : source;
      const marker = form === 'CJS' ? '(0, react_2.useEffect)(() => {\n        var _a;' : 'useEffect5(() => {';
      const start = playback.indexOf(marker);
      const end = playback.indexOf('}, [', start);
      assert.ok(start > 0 && end > start);
      const body = playback.slice(start + marker.length, end);
      const runEffect = environment => new Function(...Object.keys(environment),
        lateOrigin ? body.replace('takePlaybackStartTime()', 'performance.now()') : body)(...Object.values(environment));
      let h;
      try {
        h = playerHarness(source, form, {
          clock, onPlaying: value => notifyPlaying(value),
          hooks: {...React, useContext: value => value},
          mount(hook) {
            const methods = [];
            function Caller() {
              const [playing, setPlaying] = React.useState(false);
              notifyPlaying = setPlaying;
              const current = hook();
              methods[0] = current;
              React.useLayoutEffect(() => {if (playing) now += 100;}, [playing]);
              React.useEffect(() => {
                if (!playing) return;
                effectAt = now;
                return runEffect({
                  config: {id: 'test', fps: 30, durationInFrames: 120}, playing,
                  sharedAudioContext: {resume() {}, getIsResumingAudioContext: () => null},
                  muted: false, performance: clock, loop: false, playbackRate: 1,
                  inFrame: 0, outFrame: 119, moveToBeginningWhenEnded: false,
                  context: {buffering: {current: false}}, isBackgroundedRef: {current: false},
                  getCurrentFrame: current.getCurrentFrame, isPlaying: current.isPlaying,
                  takePlaybackStartTime: current.takePlaybackStartTime,
                  setFrame(fn) {h.timeline.frameRef.current = fn(h.timeline.frameRef.current);},
                  pause: current.pause, emitter: {dispatchEnded() {}},
                  requestAnimationFrame(fn) {const id = ++nextRaf; rafs.set(id, fn); return id;},
                  cancelAnimationFrame(id) {rafs.delete(id);},
                  calculateNextFrame, calculate_next_frame_js_1: {calculateNextFrame},
                });
              }, [playing]);
              return null;
            }
            React.act(() => renderer.render(React.createElement(React.StrictMode, null, React.createElement(Caller))));
            return [methods[0], methods[0]];
          },
        });
        React.act(() => h.methods.play({}));
        await React.act(async () => {h.waits[0].resolve('resumed'); await flush();});
        assert.equal(h.nativeTimes[0], 1000, 'native play precedes the delayed React commit');
        assert.equal(effectAt, 1100);
        now += 16;
        const callback = rafs.values().next().value;
        assert.equal(typeof callback, 'function');
        React.act(() => callback());
        const elapsedFrames = Math.floor((now - h.nativeTimes[0]) * 30 / 1000);
        if (lateOrigin) {
          assert.equal(h.methods.getCurrentFrame(), 0, 'the pristine loop loses the commit delay');
          assert.equal(elapsedFrames, 3);
        }
        else assert.equal(h.methods.getCurrentFrame(), elapsedFrames, 'effect delay must not move the frame origin after native play');
      } finally {
        React.act(() => renderer.unmount());
        dom.window.close();
        globalThis.window = previous.window;
        globalThis.document = previous.document;
        globalThis.IS_REACT_ACT_ENVIRONMENT = previous.act;
      }
    });
  }
});


test('native cursor diagnostic copies every PCM sample and detects source damage', async () => {
  const vm = await import('node:vm');
  const probe = fs.readFileSync(path.join(root, 'tests/e2e/timeline/player-audio-capture.probe.ts'), 'utf8');
  const marker = 'const nativeCursorWorklet = `';
  const start = probe.indexOf(marker);
  const end = probe.indexOf('`;', start);
  assert.ok(start > 0 && end > start);
  const messages = [];
  let Processor;
  const realm = {currentFrame: 0, AudioWorkletProcessor: class {port = {postMessage: message => messages.push(message)};},
    registerProcessor(name, value) {assert.equal(name, 'native-cursor'); Processor = value;}};
  vm.createContext(realm);
  vm.runInContext(probe.slice(start + marker.length, end), realm);
  const reference = [0, 1].map(channel => Float32Array.from({length: 480}, (_, i) => Math.sin(2 * Math.PI * 660 * i / 48000) * (channel ? .75 : 1) / 8));
  for (const damage of [false, true]) {
    const processor = new Processor({processorOptions: {reference}});
    for (let start = -256; start < 768; start += 128) {
      const inputs = reference.map(channel => Float32Array.from({length: 128}, (_, i) => channel[start + i] ?? 0));
      if (damage && start === 128) inputs[0][17] = 1;
      const outputs = inputs.map(() => new Float32Array(128));
      realm.currentFrame = start + 256;
      assert.equal(processor.process([inputs], [outputs]), false, 'identity observer must not hold an active source');
      assert.deepEqual(outputs, inputs, 'all float samples in both channels must pass unchanged');
    }
    assert.equal(processor.maxError === 0, !damage, 'known-source cursor must detect a damaged native sample');
    const empty = reference.map(() => new Float32Array(128).fill(1));
    assert.equal(processor.process([[]], [empty]), false, 'unconnected observer must not keep the graph active');
    assert.ok(empty.every(channel => channel.every(value => value === 0)), 'an unconnected edge provides only silence');
  }
  assert.equal(messages.length, 18, 'every processed quantum remains observable');
  assert.ok(messages.every(record => record.outputIdentity && record.outputChannels === 2));
  const firstInputs = messages.filter(record => record.firstInput);
  assert.equal(firstInputs.length, 2);
  for (const record of firstInputs) assert.deepEqual(Array.from(record.firstInput[0]), Array.from(reference[0].slice(0, 128)));
});


test('native muted observer forwards exactly the original writes', async () => {
  const {JSDOM} = await import('jsdom');
  const dom = new JSDOM('<audio src="/source.wav"></audio>');
  const proto = dom.window.HTMLMediaElement.prototype;
  const descriptor = Object.getOwnPropertyDescriptor(proto, 'muted');
  const writes = [];
  Object.defineProperty(proto, 'muted', {...descriptor, set(value) {writes.push(value); descriptor.set.call(this, value);}});
  dom.window.__captureEvents = [];
  const probe = fs.readFileSync(path.join(root, 'tests/e2e/timeline/player-audio-capture.probe.ts'), 'utf8');
  const start = probe.indexOf("              const descriptor = Object.getOwnPropertyDescriptor(HTMLMediaElement.prototype, 'muted');");
  const end = probe.indexOf('            }\n            const nativePlay', start);
  assert.ok(start > 0 && end > start);
  const body = probe.slice(start, end);
  assert.equal(body.split('set(value: boolean)').length, 2);
  try {
    new Function('HTMLMediaElement', 'window', 'performance', body.replace('set(value: boolean)', 'set(value)'))(dom.window.HTMLMediaElement, dom.window, performance);
    const element = dom.window.document.querySelector('audio');
    element.volume = .7;
    for (const value of [true, false, true]) element.muted = value;
    assert.deepEqual(writes, [true, false, true], 'no added mute reset, omitted write or coerced value');
    assert.deepEqual(dom.window.__captureEvents.map(event => [event.before, event.value, event.after]), [[false, true, true], [true, false, false], [false, true, true]]);
    assert.equal(element.volume, .7);
    assert.equal(element.currentTime, 0);
    assert.equal(element.playbackRate, 1);
  } finally {dom.window.close();}
});
