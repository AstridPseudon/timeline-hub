#!/usr/bin/env node

import { createHash, randomBytes } from 'node:crypto';
import { open, readFile, rename, rm, stat } from 'node:fs/promises';
import { basename, dirname, join, resolve } from 'node:path';

const EXPECTED_VERSION = '4.0.509';
const TARGETS = [
  {
    relativePath: 'dist/cjs/audio/shared-audio-tags.js',
    originalSha256: '471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c',
    patchedSha256: '949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8',
    originalLine: '(0, wait_until_actually_resumed_js_1.waitUntilActuallyResumed)(ctxAndGain.audioContext, logLevel, abortController.signal).then(resolve);',
    patchedLine: 'resumePromise.then(() => (0, wait_until_actually_resumed_js_1.waitUntilActuallyResumed)(ctxAndGain.audioContext, logLevel, abortController.signal).then(resolve), () => {});',
  },
  {
    relativePath: 'dist/esm/index.mjs',
    originalSha256: '9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8',
    patchedSha256: '5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28',
    originalLine: 'waitUntilActuallyResumed(ctxAndGain.audioContext, logLevel, abortController.signal).then(resolve);',
    patchedLine: 'resumePromise.then(() => waitUntilActuallyResumed(ctxAndGain.audioContext, logLevel, abortController.signal).then(resolve), () => {});',
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/cjs/use-player-methods.js',
    originalSha256: 'ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46',
    patchedSha256: '6bb73dd46e710761ef8ad6d16be3cb103c7e5c2bcbf8342f39c28586717cf0c5',
    patches: [
      [
        'const usePlayerMethods = () => {',
        `const pendingPlayerStarts = new WeakMap();
const playerPlaybackOrigins = new WeakMap();
const usePlayerMethods = () => {`,
      ],
      [
        '    const audioTagsContext = (0, react_1.useContext)(remotion_1.Internals.SharedAudioTagsContext);',
        `    const audioTagsContext = (0, react_1.useContext)(remotion_1.Internals.SharedAudioTagsContext);
    const { setPlayerMuted } = (0, react_1.useContext)(remotion_1.Internals.SetMediaVolumeContext);`,
      ],
      [
        '    const seek = (0, react_1.useCallback)((newFrame) => {',
        `    const cancelPendingStart = (0, react_1.useCallback)(() => {
        const pending = pendingPlayerStarts.get(timelineImperativeContext.imperativePlaying);
        if (!pending) return;
        pendingPlayerStarts.delete(timelineImperativeContext.imperativePlaying);
        pending.abort();
        timelineImperativeContext.imperativePlaying.current = false;
        try { Promise.resolve(audioContext?.suspend()).catch(() => {}); } catch { /* Already cancelled. */ }
        emitter.dispatchPause();
    }, [audioContext, emitter, timelineImperativeContext]);
    (0, react_1.useEffect)(() => () => cancelPendingStart(), [cancelPendingStart]);
    const seek = (0, react_1.useCallback)((newFrame) => {
        cancelPendingStart();`,
      ],
      [
        `        config,
        emitter,
        setTimelinePosition,`,
        `        cancelPendingStart,
        config,
        emitter,
        setTimelinePosition,`,
      ],
      [
        `        audioContext === null || audioContext === void 0 ? void 0 : audioContext.resume();
        /**
         * Play silent audio tags to warm them up for autoplay
         */
        if (audioTagsContext && audioTagsContext.numberOfAudioTags > 0 && e) {
            audioTagsContext.playAllAudios();
        }
        /**
         * Play audios and videos directly here so they can benefit from
         * being triggered by a click
         */
        timelineImperativeContext.audioAndVideoTags.current.forEach((tag) => tag.play('player play() was called and playing audio from a click'));
        timelineImperativeContext.imperativePlaying.current = true;
        setPlaying(true);
        playStart.current = getCurrentFrame();
        emitter.dispatchPlay();`,
        `        const pending = new AbortController();
        pendingPlayerStarts.set(timelineImperativeContext.imperativePlaying, pending);
        playStart.current = getCurrentFrame();
        // Resume in the gesture, but keep media and the frame clock stopped until output is ready.
        const failStartup = () => {
            if (pendingPlayerStarts.get(timelineImperativeContext.imperativePlaying) === pending) cancelPendingStart();
        };
        let ready;
        try {
            Promise.resolve(audioContext?.resume()).catch(failStartup);
            ready = audioContext?.getIsResumingAudioContext() ?? Promise.resolve('resumed');
        } catch {
            failStartup();
            return;
        }
        Promise.resolve(ready).then((result) => {
            if (pending.signal.aborted) return;
            if (result === 'cancelled') {
                cancelPendingStart();
                return;
            }
            if (result === 'failed') {
                audioContext?.suspend();
                setPlayerMuted(true);
            }
            const start = () => {
                if (pending.signal.aborted) return;
                pendingPlayerStarts.delete(timelineImperativeContext.imperativePlaying);
                if (audioContext?.audioContext && config) {
                    const changed = (0, set_global_time_anchor_js_1.setGlobalTimeAnchor)({
                        audioContext: audioContext.audioContext,
                        audioSyncAnchor: audioContext.audioSyncAnchor,
                        absoluteTimeInSeconds: getCurrentFrame() / config.fps,
                        globalPlaybackRate: playbackRate,
                        logLevel,
                        force: true,
                    });
                    if (changed) audioContext.audioSyncAnchorEmitter.dispatch('changed');
                }
                playerPlaybackOrigins.set(timelineImperativeContext.imperativePlaying, performance.now());
                timelineImperativeContext.imperativePlaying.current = true;
                setPlaying(true);
                if (result !== 'failed' && audioTagsContext && audioTagsContext.numberOfAudioTags > 0 && e) {
                    audioTagsContext.playAllAudios();
                }
                timelineImperativeContext.audioAndVideoTags.current.forEach((tag) => tag.play('player play() was called and playing audio from a click'));
                emitter.dispatchPlay();
            };
            if (bufferingContext.buffering.current) {
                const listener = bufferingContext.listenForResume(() => {
                    listener.remove();
                    pending.signal.removeEventListener('abort', remove);
                    start();
                });
                const remove = () => listener.remove();
                pending.signal.addEventListener('abort', remove, { once: true });
            } else {
                start();
            }
        }).catch(failStartup);`,
      ],
      [
        `        audioContext,
        audioTagsContext,`,
        `        audioContext,
        audioTagsContext,
        bufferingContext,
        cancelPendingStart,
        setPlayerMuted,
        playbackRate,
        logLevel,`,
      ],
      [
        '    const pause = (0, react_1.useCallback)(() => {',
        `    const pause = (0, react_1.useCallback)(() => {
        cancelPendingStart();`,
      ],
      [
        '    const pauseAndReturnToPlayStart = (0, react_1.useCallback)(() => {',
        `    const pauseAndReturnToPlayStart = (0, react_1.useCallback)(() => {
        cancelPendingStart();`,
      ],
      [
        '[audioContext, emitter, setPlaying, timelineImperativeContext]);',
        '[audioContext, cancelPendingStart, emitter, setPlaying, timelineImperativeContext]);',
      ],
      [
        `        config,
        emitter,
        setPlaying,`,
        `        cancelPendingStart,
        config,
        emitter,
        setPlaying,`,
      ],
      [
        'const emitter_context_js_1 = require("./emitter-context.js");',
        `const set_global_time_anchor_js_1 = require("./set-global-time-anchor.js");
const emitter_context_js_1 = require("./emitter-context.js");`,
      ],
      [
        '    const config = remotion_1.Internals.useUnsafeVideoConfig();',
        `    const config = remotion_1.Internals.useUnsafeVideoConfig();
    const { playbackRate } = remotion_1.Internals.usePlaybackRate();
    const logLevel = remotion_1.Internals.useLogLevel();`,
      ],
      [
        `    const play = (0, react_1.useCallback)((e) => {
        var _a;
        if (timelineImperativeContext.imperativePlaying.current) {`,
        `    const play = (0, react_1.useCallback)((e) => {
        var _a;
        if (timelineImperativeContext.imperativePlaying.current || pendingPlayerStarts.has(timelineImperativeContext.imperativePlaying)) {`,
      ],
      [
        `    const toggle = (0, react_1.useCallback)((e) => {
        if (timelineImperativeContext.imperativePlaying.current) {`,
        `    const toggle = (0, react_1.useCallback)((e) => {
        if (timelineImperativeContext.imperativePlaying.current || pendingPlayerStarts.has(timelineImperativeContext.imperativePlaying)) {`,
      ],
      [
        '    const isBuffering = (0, react_1.useCallback)(() => {',
        `    const takePlaybackStartTime = (0, react_1.useCallback)(() => {
        const origin = playerPlaybackOrigins.get(timelineImperativeContext.imperativePlaying);
        playerPlaybackOrigins.delete(timelineImperativeContext.imperativePlaying);
        return origin ?? performance.now();
    }, [timelineImperativeContext]);
    const isBuffering = (0, react_1.useCallback)(() => {`,
      ],
      [
        `
            isBuffering,`,
        `
            isBuffering,
            takePlaybackStartTime,`,
      ],
      [
        `
        isBuffering,`,
        `
        isBuffering,
        takePlaybackStartTime,`,
      ],
      [
        '    const takePlaybackStartTime = (0, react_1.useCallback)(() => {',
        `    const isStarting = (0, react_1.useCallback)(() => pendingPlayerStarts.has(timelineImperativeContext.imperativePlaying), [timelineImperativeContext]);
    const takePlaybackStartTime = (0, react_1.useCallback)(() => {`,
      ],
      [
        `
            isBuffering,
            takePlaybackStartTime,`,
        `
            isBuffering,
            takePlaybackStartTime,
            isStarting,`,
      ],
      [
        `
        isBuffering,
        takePlaybackStartTime,`,
        `
        isBuffering,
        takePlaybackStartTime,
        isStarting,`,
      ],
    ],
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/esm/index.mjs',
    originalSha256: 'd3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12',
    patchedSha256: '0b98ec41a8f69dfe75ca46ca4eb16794eef65848f282e9459705ca5dfc6d0581',
    patches: [
      [
        'var usePlayerMethods = () => {',
        `var pendingPlayerStarts = new WeakMap();
var playerPlaybackOrigins = new WeakMap();
var usePlayerMethods = () => {`,
      ],
      [
        '  const audioTagsContext = useContext3(Internals5.SharedAudioTagsContext);',
        `  const audioTagsContext = useContext3(Internals5.SharedAudioTagsContext);
  const { setPlayerMuted } = useContext3(Internals5.SetMediaVolumeContext);`,
      ],
      [
        '  const seek = useCallback((newFrame) => {',
        `  const cancelPendingStart = useCallback(() => {
    const pending = pendingPlayerStarts.get(timelineImperativeContext.imperativePlaying);
    if (!pending) return;
    pendingPlayerStarts.delete(timelineImperativeContext.imperativePlaying);
    pending.abort();
    timelineImperativeContext.imperativePlaying.current = false;
    try { Promise.resolve(audioContext?.suspend()).catch(() => {}); } catch { /* Already cancelled. */ }
    emitter.dispatchPause();
  }, [audioContext, emitter, timelineImperativeContext]);
  useEffect(() => () => cancelPendingStart(), [cancelPendingStart]);
  const seek = useCallback((newFrame) => {
    cancelPendingStart();`,
      ],
      [
        `    config,
    emitter,
    setTimelinePosition,`,
        `    cancelPendingStart,
    config,
    emitter,
    setTimelinePosition,`,
      ],
      [
        `    audioContext?.resume();
    if (audioTagsContext && audioTagsContext.numberOfAudioTags > 0 && e) {
      audioTagsContext.playAllAudios();
    }
    timelineImperativeContext.audioAndVideoTags.current.forEach((tag) => tag.play("player play() was called and playing audio from a click"));
    timelineImperativeContext.imperativePlaying.current = true;
    setPlaying(true);
    playStart.current = getCurrentFrame();
    emitter.dispatchPlay();`,
        `    const pending = new AbortController();
    pendingPlayerStarts.set(timelineImperativeContext.imperativePlaying, pending);
    playStart.current = getCurrentFrame();
    // Resume in the gesture, but keep media and the frame clock stopped until output is ready.
    const failStartup = () => {
      if (pendingPlayerStarts.get(timelineImperativeContext.imperativePlaying) === pending) cancelPendingStart();
    };
    let ready;
    try {
      Promise.resolve(audioContext?.resume()).catch(failStartup);
      ready = audioContext?.getIsResumingAudioContext() ?? Promise.resolve('resumed');
    } catch {
      failStartup();
      return;
    }
    Promise.resolve(ready).then((result) => {
      if (pending.signal.aborted) return;
      if (result === 'cancelled') {
        cancelPendingStart();
        return;
      }
      if (result === 'failed') {
        audioContext?.suspend();
        setPlayerMuted(true);
      }
      const start = () => {
        if (pending.signal.aborted) return;
        pendingPlayerStarts.delete(timelineImperativeContext.imperativePlaying);
        if (audioContext?.audioContext && config) {
          const changed = setGlobalTimeAnchor({
            audioContext: audioContext.audioContext,
            audioSyncAnchor: audioContext.audioSyncAnchor,
            absoluteTimeInSeconds: getCurrentFrame() / config.fps,
            globalPlaybackRate: playbackRate,
            logLevel,
            force: true,
          });
          if (changed) audioContext.audioSyncAnchorEmitter.dispatch('changed');
        }
        playerPlaybackOrigins.set(timelineImperativeContext.imperativePlaying, performance.now());
        timelineImperativeContext.imperativePlaying.current = true;
        setPlaying(true);
        if (result !== 'failed' && audioTagsContext && audioTagsContext.numberOfAudioTags > 0 && e) {
          audioTagsContext.playAllAudios();
        }
        timelineImperativeContext.audioAndVideoTags.current.forEach((tag) => tag.play('player play() was called and playing audio from a click'));
        emitter.dispatchPlay();
      };
      if (bufferingContext.buffering.current) {
        const listener = bufferingContext.listenForResume(() => {
          listener.remove();
          pending.signal.removeEventListener('abort', remove);
          start();
        });
        const remove = () => listener.remove();
        pending.signal.addEventListener('abort', remove, { once: true });
      } else {
        start();
      }
    }).catch(failStartup);`,
      ],
      [
        `    audioContext,
    audioTagsContext,`,
        `    audioContext,
    audioTagsContext,
    bufferingContext,
    cancelPendingStart,
    setPlayerMuted,
    playbackRate,
    logLevel,`,
      ],
      [
        '  const pause = useCallback(() => {',
        `  const pause = useCallback(() => {
    cancelPendingStart();`,
      ],
      [
        '  const pauseAndReturnToPlayStart = useCallback(() => {',
        `  const pauseAndReturnToPlayStart = useCallback(() => {
    cancelPendingStart();`,
      ],
      [
        '[audioContext, emitter, setPlaying, timelineImperativeContext]);',
        '[audioContext, cancelPendingStart, emitter, setPlaying, timelineImperativeContext]);',
      ],
      [
        `    config,
    emitter,
    setPlaying,`,
        `    cancelPendingStart,
    config,
    emitter,
    setPlaying,`,
      ],
      [
        '  const config = Internals5.useUnsafeVideoConfig();',
        `  const config = Internals5.useUnsafeVideoConfig();
  const { playbackRate } = Internals5.usePlaybackRate();
  const logLevel = Internals5.useLogLevel();`,
      ],
      [
        `  const play = useCallback((e) => {
    if (timelineImperativeContext.imperativePlaying.current) {`,
        `  const play = useCallback((e) => {
    if (timelineImperativeContext.imperativePlaying.current || pendingPlayerStarts.has(timelineImperativeContext.imperativePlaying)) {`,
      ],
      [
        `  const toggle = useCallback((e) => {
    if (timelineImperativeContext.imperativePlaying.current) {`,
        `  const toggle = useCallback((e) => {
    if (timelineImperativeContext.imperativePlaying.current || pendingPlayerStarts.has(timelineImperativeContext.imperativePlaying)) {`,
      ],
      [
        '  const isBuffering = useCallback(() => {',
        `  const takePlaybackStartTime = useCallback(() => {
    const origin = playerPlaybackOrigins.get(timelineImperativeContext.imperativePlaying);
    playerPlaybackOrigins.delete(timelineImperativeContext.imperativePlaying);
    return origin ?? performance.now();
  }, [timelineImperativeContext]);
  const isBuffering = useCallback(() => {`,
      ],
      [
        `
      isBuffering,`,
        `
      isBuffering,
      takePlaybackStartTime,`,
      ],
      [
        `
    isBuffering,`,
        `
    isBuffering,
    takePlaybackStartTime,`,
      ],
      [
        'const { pause, emitter, isPlaying } = usePlayerMethods();',
        'const { pause, emitter, isPlaying, takePlaybackStartTime } = usePlayerMethods();',
      ],
      [
        'let startedTime = performance.now();',
        'let startedTime = takePlaybackStartTime();',
      ],
      [
        `    isPlaying,
    sharedAudioContext,`,
        `    isPlaying,
    takePlaybackStartTime,
    sharedAudioContext,`,
      ],
      [
        '  const takePlaybackStartTime = useCallback(() => {',
        `  const isStarting = useCallback(() => pendingPlayerStarts.has(timelineImperativeContext.imperativePlaying), [timelineImperativeContext]);
  const takePlaybackStartTime = useCallback(() => {`,
      ],
      [
        `
      isBuffering,
      takePlaybackStartTime,`,
        `
      isBuffering,
      takePlaybackStartTime,
      isStarting,`,
      ],
      [
        `
    isBuffering,
    takePlaybackStartTime,`,
        `
    isBuffering,
    takePlaybackStartTime,
    isStarting,`,
      ],
      [
        'const { pause, emitter, isPlaying, takePlaybackStartTime } = usePlayerMethods();',
        'const { pause, emitter, isPlaying, takePlaybackStartTime, isStarting } = usePlayerMethods();',
      ],
      [
        `    if (!playing) {
`,
        `    if (!playing) {
      if (isStarting()) return;
`,
      ],
      [
        `    takePlaybackStartTime,
    sharedAudioContext,`,
        `    takePlaybackStartTime,
    isStarting,
    sharedAudioContext,`,
      ],
      [
        `    if (player.isPlaying()) {
      player.pause();`,
        `    if (player.isPlaying() || player.isStarting()) {
      player.pause();`,
      ],
    ],
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/cjs/use-playback.js',
    originalSha256: '6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0',
    patchedSha256: '18a5d6551196a67630be4dc53f6adb18e8e300b71ae9990a1d2f00d80728afbf',
    patches: [
      [
        'const { pause, emitter, isPlaying } = (0, use_player_methods_js_1.usePlayerMethods)();',
        'const { pause, emitter, isPlaying, takePlaybackStartTime } = (0, use_player_methods_js_1.usePlayerMethods)();',
      ],
      [
        'let startedTime = performance.now();',
        'let startedTime = takePlaybackStartTime();',
      ],
      [
        `        isPlaying,
        sharedAudioContext,`,
        `        isPlaying,
        takePlaybackStartTime,
        sharedAudioContext,`,
      ],
      [
        'const { pause, emitter, isPlaying, takePlaybackStartTime } = (0, use_player_methods_js_1.usePlayerMethods)();',
        'const { pause, emitter, isPlaying, takePlaybackStartTime, isStarting } = (0, use_player_methods_js_1.usePlayerMethods)();',
      ],
      [
        `        if (!playing) {
`,
        `        if (!playing) {
            if (isStarting()) return;
`,
      ],
      [
        `        takePlaybackStartTime,
        sharedAudioContext,`,
        `        takePlaybackStartTime,
        isStarting,
        sharedAudioContext,`,
      ],
    ],
  },
  {
    packageName: '@remotion/player',
    relativePath: 'dist/cjs/PlayerUI.js',
    originalSha256: '5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb',
    patches: [
      [
        `        if (player.isPlaying()) {
            player.pause();`,
        `        if (player.isPlaying() || player.isStarting()) {
            player.pause();`,
      ],
    ],
    patchedSha256: '05e0dd2c4c98ecd95b32e18af8385680bc83324f92fbc36e3de438e9bfb04ffa',
  },
];

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function replaceExactlyOnce(bytes, from, to, label) {
  const text = bytes.toString('utf8');
  const occurrences = text.split(from).length - 1;
  if (occurrences !== 1) {
    throw new Error(`${label}: expected one exact patch line, found ${occurrences}`);
  }
  return Buffer.from(text.replace(from, to), 'utf8');
}

async function preflight(projectRoot) {
  // Read and classify every package and target before any caller can write.
  return Promise.all(
    TARGETS.map(async (target) => {
      const packageName = target.packageName ?? 'remotion';
      const packageRoot = resolve(projectRoot, 'node_modules', packageName);
      const packageJson = JSON.parse(await readFile(join(packageRoot, 'package.json'), 'utf8'));
      if (packageJson.name !== packageName || packageJson.version !== EXPECTED_VERSION) {
        throw new Error(
          `Refusing Remotion ${packageJson.name ?? '(unnamed)'}@${packageJson.version ?? '(unknown)'}; expected ${packageName}@${EXPECTED_VERSION}`,
        );
      }
      const absolutePath = join(packageRoot, target.relativePath);
      const [bytes, fileStat] = await Promise.all([readFile(absolutePath), stat(absolutePath)]);
      const digest = sha256(bytes);
      let state;
      if (digest === target.originalSha256) state = 'pristine';
      else if (digest === target.patchedSha256) state = 'patched';
      else {
        throw new Error(
          `Refusing unknown content at ${absolutePath} (sha256 ${digest}); no files were written`,
        );
      }
      return { ...target, absolutePath, bytes, mode: fileStat.mode & 0o777, state };
    }),
  );
}

function transformedBytes(entry, direction) {
  const toPatched = direction === 'apply';
  const patches = entry.patches ?? [[entry.originalLine, entry.patchedLine]];
  const bytes = (toPatched ? patches : [...patches].reverse()).reduce(
    (current, [before, after]) => replaceExactlyOnce(
      current, toPatched ? before : after, toPatched ? after : before, entry.absolutePath,
    ), entry.bytes,
  );
  const expectedDigest = toPatched ? entry.patchedSha256 : entry.originalSha256;
  const actualDigest = sha256(bytes);
  if (actualDigest !== expectedDigest) {
    throw new Error(
      `${entry.absolutePath}: transformed bytes did not match expected sha256 ${expectedDigest} (got ${actualDigest})`,
    );
  }
  return bytes;
}

async function stageFile(targetPath, bytes, mode) {
  const tempPath = join(
    dirname(targetPath),
    `.${basename(targetPath)}.remotion-audio-resume-${process.pid}-${randomBytes(6).toString('hex')}.tmp`,
  );
  const handle = await open(tempPath, 'wx', mode);
  try {
    await handle.writeFile(bytes);
    await handle.chmod(mode);
    await handle.sync();
  } catch (error) {
    await handle.close();
    await rm(tempPath, { force: true });
    throw error;
  }
  await handle.close();
  return tempPath;
}

async function replaceAtomically(targetPath, bytes, mode) {
  const tempPath = await stageFile(targetPath, bytes, mode);
  try {
    await rename(tempPath, targetPath);
  } catch (error) {
    await rm(tempPath, { force: true });
    throw error;
  }
}

async function changeFiles(projectRoot, entries, direction) {
  const sourceState = direction === 'apply' ? 'pristine' : 'patched';
  const updated = entries
    .filter((entry) => entry.state === sourceState)
    .map((entry) => ({ ...entry, nextBytes: transformedBytes(entry, direction) }));
  if (updated.length === 0) return false;

  // Stage every new file before the first rename. All content/version guards
  // have already passed for all files.
  const staged = [];
  try {
    for (const entry of updated) {
      staged.push({ ...entry, tempPath: await stageFile(entry.absolutePath, entry.nextBytes, entry.mode) });
    }
  } catch (error) {
    await Promise.all(staged.map(({ tempPath }) => rm(tempPath, { force: true })));
    throw error;
  }

  const committed = [];
  try {
    for (const entry of staged) {
      await rename(entry.tempPath, entry.absolutePath);
      committed.push(entry);
    }
    const finalEntries = await preflight(projectRoot);
    const wanted = direction === 'apply' ? 'patched' : 'pristine';
    if (finalEntries.some((entry) => entry.state !== wanted)) {
      throw new Error('Post-write verification did not reach the requested exact state');
    }
  } catch (error) {
    const rollbackErrors = [];
    for (const entry of [...committed].reverse()) {
      try {
        await replaceAtomically(entry.absolutePath, entry.bytes, entry.mode);
      } catch (rollbackError) {
        rollbackErrors.push(rollbackError.message);
      }
    }
    await Promise.all(
      staged
        .filter((entry) => !committed.includes(entry))
        .map(({ tempPath }) => rm(tempPath, { force: true })),
    );
    const suffix = rollbackErrors.length ? `; rollback errors: ${rollbackErrors.join('; ')}` : '';
    throw new Error(`${error.message}${suffix}`);
  }
  return true;
}

function parseArgs(argv) {
  let action;
  let projectRoot = process.cwd();
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--help' || arg === '-h') return { help: true };
    if (['--apply', '--check', '--revert'].includes(arg)) {
      if (action) throw new Error('Choose exactly one of --apply, --check, or --revert');
      action = arg.slice(2);
      continue;
    }
    if (arg === '--root') {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) throw new Error('--root requires a project root path');
      projectRoot = resolve(value);
      index += 1;
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }
  if (!action) throw new Error('Choose one of --apply, --check, or --revert');
  return { action, projectRoot };
}

function usage() {
  return [
    'Usage: node scripts/patches/remotion-4.0.509-audio-resume.mjs --apply|--check|--revert [--root <project-root>]',
    '--check is read-only and accepts only the exact known pristine or patched 4.0.509 files.',
  ].join('\n');
}

async function main(argv = process.argv.slice(2)) {
  const args = parseArgs(argv);
  if (args.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }

  const entries = await preflight(args.projectRoot);
  const states = entries.map((entry) => `${entry.relativePath}=${entry.state}`).join(', ');
  if (args.action === 'check') {
    process.stdout.write(`Read-only preflight passed for remotion@${EXPECTED_VERSION}: ${states}\n`);
    return;
  }

  const changed = await changeFiles(args.projectRoot, entries, args.action);
  const finalEntries = await preflight(args.projectRoot);
  const finalStates = finalEntries.map((entry) => `${entry.relativePath}=${entry.state}`).join(', ');
  process.stdout.write(
    `${changed ? (args.action === 'apply' ? 'Applied' : 'Reverted') : 'Already in requested state'} exact Remotion ${EXPECTED_VERSION} audio-resume patch: ${finalStates}\n`,
  );
}

main().catch((error) => {
  process.stderr.write(`Remotion audio-resume patch refused/failed: ${error.message}\n`);
  process.exitCode = 1;
});
