import { expect, test, type CDPSession } from '@playwright/test';
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import { cpus, hostname, loadavg } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';
import { privateMonitor } from './player-audio-monitor';

const exec = promisify(execFile);
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

async function inspect<T>(session: CDPSession, fn: () => T): Promise<Awaited<T>> {
  const { result, exceptionDetails } = await session.send('Runtime.evaluate', {
    expression: `(${fn.toString()})()`, userGesture: false, returnByValue: true, awaitPromise: true,
  });
  if (exceptionDetails) throw new Error(exceptionDetails.exception?.description ?? exceptionDetails.text);
  return result.value;
}

async function graph() {
  const paths = [
    'package.json', 'package-lock.json', 'vendor/artifacts/banodoco-timeline-composition-0.0.8.tgz',
    'node_modules/remotion/dist/cjs/audio/shared-audio-tags.js',
    'node_modules/remotion/dist/esm/index.mjs',
    'node_modules/@remotion/player/dist/cjs/use-player-methods.js',
    'node_modules/@remotion/player/dist/esm/index.mjs',
    'node_modules/@remotion/player/dist/cjs/use-playback.js',
    'node_modules/@remotion/player/dist/cjs/PlayerUI.js',
  ];
  const compositionRoot = 'node_modules/@banodoco/timeline-composition';
  const compositionFiles: Record<string, string> = {};
  const walk = async (directory: string) => {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = join(directory, entry.name);
      if (entry.isDirectory()) await walk(path);
      else compositionFiles[path.slice(compositionRoot.length + 1)] = createHash('sha256').update(await readFile(path)).digest('hex');
    }
  };
  await walk(compositionRoot);
  const hashes = Object.fromEntries(await Promise.all(paths.map(async path =>
    [path, createHash('sha256').update(await readFile(path)).digest('hex')])));
  const versions = Object.fromEntries(await Promise.all([
    '@banodoco/timeline-composition', '@remotion/player', 'remotion', 'react', 'react-dom', '@playwright/test',
  ].map(async name => [name, JSON.parse(await readFile(`node_modules/${name}/package.json`, 'utf8')).version])));
  return { hashes, compositionFiles, versions, node: process.version };
}

declare global {
  interface Window {
    __platform: {
      snapshot: () => Record<string, unknown>;
      cleanup: () => Promise<void>;
      report: Record<string, unknown>;
    };
  }
}

for (const condition of ['IDLE', 'ACTIVE'] as const) {
  test(`native output clock with ${condition} monitor`, async ({ playwright, launchOptions, headless, viewport }, testInfo) => {
    const beforeGraph = await graph();
    const results: Record<string, unknown> = { condition, repeat: testInfo.repeatEachIndex, beforeGraph, launchOptions, headless };
    const samples: unknown[] = [];
    const telemetryErrors: string[] = [];
    const monitor = await privateMonitor();
    let browser: Awaited<ReturnType<typeof playwright.chromium.launch>> | undefined;
    let cdp: CDPSession | undefined;
    let pageCdp: CDPSession | undefined;
    let consumer: Awaited<ReturnType<typeof monitor.drain>> | undefined;
    const safe = async <T>(name: string, operation: () => Promise<T>): Promise<T | null> => {
      try { return await operation(); } catch (error) {
        telemetryErrors.push(`${name}: ${String(error)}`);
        return null;
      }
    };
    const structured = async () => {
      const [sinks, sources, inputs, outputs] = await Promise.all(
        ['sinks', 'sources', 'sink-inputs', 'source-outputs'].map(async kind =>
          JSON.parse((await exec('pactl', ['--format=json', 'list', kind], { env: monitor.env })).stdout)),
      );
      return { epochMs: Date.now(), sinks, sources, inputs, outputs };
    };
    const sample = async () => {
      const [host, processes, pulse, browserProcesses] = await Promise.all([
        safe('host', () => readFile('/proc/stat', 'utf8')),
        safe('processes', async () => (await exec('ps', ['-eo', 'pid,ppid,comm,pcpu,cputimes,args', '--sort=-pcpu'])).stdout),
        safe('pulse', structured),
        safe('browser', async () => cdp ? cdp.send('SystemInfo.getProcessInfo') : null),
      ]);
      const pulsePid = processes?.split('\n').find(line => line.includes(`socket=${monitor.directory}/native`))?.trim().split(/\s+/)[0];
      samples.push({ epochMs: Date.now(), load: loadavg(), host: host?.split('\n')[0], processes, pulse,
        pulsePid, pulseStat: pulsePid ? await safe('pulse stat', () => readFile(`/proc/${pulsePid}/stat`, 'utf8')) : null, browserProcesses });
    };
    let sampling = true;
    const samplingDone = (async () => {
      while (sampling) { await sample(); if (sampling) await delay(250); }
    })();
    void samplingDone.catch(() => {});
    let primaryError: unknown;
    try {
      results.host = { hostname: hostname(), cpuCount: cpus().length, ticksPerSecond: Number((await exec('getconf', ['CLK_TCK'])).stdout) };
      browser = await playwright.chromium.launch({ ...launchOptions, headless, env: monitor.env });
      results.browserVersion = browser.version();
      cdp = await browser.newBrowserCDPSession();
      try { results.commandLine = await cdp.send('Browser.getBrowserCommandLine'); }
      catch (error) { results.commandLine = { unavailable: String(error) }; }
      try {
        const { processInfo } = await cdp.send('SystemInfo.getProcessInfo');
        const browserPid = processInfo.find(process => process.type === 'browser')?.id;
        results.browserPid = browserPid;
        results.processArguments = browserPid
          ? (await readFile(`/proc/${browserPid}/cmdline`, 'utf8')).split('\0').filter(Boolean) : null;
      } catch (error) { results.processArguments = { unavailable: String(error) }; }
      const context = await browser.newContext({ viewport });
      await context.route('**/*', route => route.abort());
      const page = await context.newPage();
      pageCdp = await context.newCDPSession(page);
      await inspect(pageCdp, async () => {
        document.body.innerHTML = '<button id="start" style="width:160px;height:80px">Start native audio</button>';
        const audioContext = new AudioContext();
        const events: Record<string, unknown>[] = [];
        const observations: Record<string, unknown>[] = [];
        const report: Record<string, unknown> = { events, observations };
        const snapshot = () => ({
          epochMs: performance.timeOrigin + performance.now(), now: performance.now(),
          state: audioContext.state, currentTime: audioContext.currentTime,
          output: audioContext.getOutputTimestamp(), sampleRate: audioContext.sampleRate,
          baseLatency: audioContext.baseLatency, outputLatency: audioContext.outputLatency,
          activation: { active: navigator.userActivation.isActive, ever: navigator.userActivation.hasBeenActive },
        });
        const event = (name: string, details: Record<string, unknown> = {}) => events.push({ name, ...snapshot(), ...details });
        audioContext.addEventListener('statechange', () => event('statechange'));
        event('constructed-default-context');
        await AudioContext.prototype.suspend.call(audioContext);
        event('explicit-initial-suspend-fulfilled');
        let source: AudioBufferSourceNode | undefined;
        let sampleTimer: ReturnType<typeof setInterval> | undefined;
        let ended = false;
        let stopped = false;

        // Copied from the frozen candidate's wait-until-actually-resumed.js:
        // same baseline, predicate, rAF checks, 1000ms timeout and final recheck.
        const RESUME_WAIT_TIMEOUT = 1000;
        const waitUntilActuallyResumed = (signal: AbortSignal) => new Promise<string>((resolve) => {
          const startCurrentTime = audioContext.currentTime;
          const start = audioContext.getOutputTimestamp();
          const startOutputPerformanceTime = start.performanceTime;
          const startWallClock = performance.now();
          report.readinessStart = { startCurrentTime, startOutputPerformanceTime, startWallClock, ...snapshot() };
          let animationFrame: number | null = null;
          let timeout: ReturnType<typeof setTimeout> | null = null;
          let settled = false;
          let onAbort: () => void = () => undefined;
          const finish = (result: string) => {
            if (settled) return;
            settled = true;
            if (animationFrame !== null) cancelAnimationFrame(animationFrame);
            if (timeout !== null) clearTimeout(timeout);
            signal.removeEventListener('abort', onAbort);
            report.readiness = { result, elapsedWallClock: performance.now() - startWallClock, ...snapshot() };
            event(`readiness-${result}`);
            resolve(result);
          };
          onAbort = () => finish('cancelled');
          const hasAudiblyStarted = (startPerformanceTime: number | undefined) => {
            const outputTimestamp = audioContext.getOutputTimestamp();
            return (startPerformanceTime !== undefined &&
              outputTimestamp.performanceTime !== undefined &&
              outputTimestamp.performanceTime > startPerformanceTime &&
              outputTimestamp.contextTime !== undefined &&
              outputTimestamp.contextTime > startCurrentTime);
          };
          const check = () => {
            animationFrame = null;
            if (hasAudiblyStarted(startOutputPerformanceTime)) { finish('resumed'); return; }
            animationFrame = requestAnimationFrame(check);
          };
          if (signal.aborted) { finish('cancelled'); return; }
          signal.addEventListener('abort', onAbort, { once: true });
          timeout = setTimeout(() => {
            report.deadlineCheck = snapshot();
            if (hasAudiblyStarted(startOutputPerformanceTime)) { finish('resumed'); return; }
            finish('failed');
          }, RESUME_WAIT_TIMEOUT);
          animationFrame = requestAnimationFrame(check);
        });
        document.getElementById('start')!.addEventListener('click', (click) => {
          event('trusted-click', { trusted: click.isTrusted });
          sampleTimer = setInterval(() => observations.push(snapshot()), 25);
          try {
            source = audioContext.createBufferSource();
            source.buffer = audioContext.createBuffer(1, audioContext.sampleRate, audioContext.sampleRate);
            report.buffer = { channels: source.buffer.numberOfChannels, length: source.buffer.length,
              sampleRate: source.buffer.sampleRate, duration: source.buffer.duration,
              allZero: source.buffer.getChannelData(0).every(value => value === 0), loop: source.loop };
            source.onended = () => { ended = true; event('source-onended', { stopped }); };
            source.connect(audioContext.destination);
            event('source-start-call');
            AudioBufferSourceNode.prototype.start.call(source);
            event('source-start-returned');
            event('native-resume-call');
            const resume = AudioContext.prototype.resume.call(audioContext);
            event('native-resume-returned');
            resume.then(() => {
              event('native-resume-fulfilled');
              return waitUntilActuallyResumed(new AbortController().signal);
            }, error => event('native-resume-rejected', { error: String(error) }))
              .catch(error => event('readiness-error', { error: String(error) }));
          } catch (error) { event('native-start-error', { error: String(error) }); }
        }, { once: true });
        window.__platform = { report, snapshot, cleanup: async () => {
          report.beforeCleanup = { ended, stopped, ...snapshot() };
          if (source) {
            stopped = true;
            event('source-stop-call');
            try { AudioBufferSourceNode.prototype.stop.call(source); event('source-stop-returned'); }
            catch (error) { event('source-stop-error', { error: String(error) }); }
            try { Reflect.apply(AudioNode.prototype.disconnect, source, []); event('source-disconnect-returned'); }
            catch (error) { event('source-disconnect-error', { error: String(error) }); }
          }
          await AudioContext.prototype.close.call(audioContext);
          event('context-close-fulfilled');
          if (sampleTimer !== undefined) clearInterval(sampleTimer);
        } };
      });
      results.beforeConsumer = await inspect(pageCdp, () => window.__platform.snapshot());
      results.pulseBeforeConsumer = await structured();
      if (condition === 'ACTIVE') {
        consumer = await monitor.drain(testInfo.outputPath('consumer.json'), () => cdp!.send('SystemInfo.getProcessInfo'));
        await consumer.snapshot('before-native-click');
      }
      const beforeClick = await inspect(pageCdp, () => window.__platform.snapshot());
      results.beforeClick = beforeClick;
      results.pulseBeforeClick = await structured();
      await writeFile(testInfo.outputPath('platform.json'), JSON.stringify(results, null, 2));
      expect(beforeClick).toMatchObject({ state: 'suspended', currentTime: 0, activation: { active: false, ever: false } });
      if (condition === 'IDLE') {
        const pulse = await structured();
        expect(pulse.inputs).toHaveLength(0);
        expect(pulse.outputs).toHaveLength(0);
        expect(pulse.sources.find((source: { name: string }) => source.name === 'player.monitor').state).toBe('IDLE');
      }
      const point = await inspect(pageCdp, () => {
        const rect = document.getElementById('start')!.getBoundingClientRect();
        return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
      });
      await pageCdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', ...point, button: 'left', clickCount: 1 });
      await pageCdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', ...point, button: 'left', clickCount: 1 });
      // Keep the finite source connected beyond its natural one-second end.
      // start() returning alone is not evidence that its buffer was processed.
      await delay(2500);
      results.native = await inspect(pageCdp, () => window.__platform.report);
      results.afterObservation = await inspect(pageCdp, () => window.__platform.snapshot());
      results.pulseAfterObservation = await structured();
      await consumer?.snapshot('after-native-observation');
      await writeFile(testInfo.outputPath('platform.json'), JSON.stringify(results, null, 2));
      const native = results.native as { readiness?: { result: string }; events: { name: string; trusted?: boolean }[] };
      expect(native.events.find(event => event.name === 'trusted-click')?.trusted).toBe(true);
      expect(native.events.some(event => event.name === 'source-start-returned')).toBe(true);
      expect(native.readiness?.result, 'native output clock predicate within the unchanged 1000ms deadline; no parity claim').toBe('resumed');
    } catch (error) {
      primaryError = error;
      results.failure = String(error);
      throw error;
    } finally {
      if (pageCdp) {
        await safe('native cleanup', () => inspect(pageCdp!, () => window.__platform.cleanup()));
        results.nativeAfterCleanup = await safe('native report', () => inspect(pageCdp!, () => window.__platform.report));
      }
      if (consumer) results.consumer = await safe('consumer cleanup', () => consumer!.close());
      results.pulseAfterCleanup = await safe('pulse cleanup inspection', structured);
      sampling = false;
      await safe('sampling', () => samplingDone);
      await sample();
      results.afterGraph = await safe('after graph', graph);
      results.samples = samples;
      results.telemetryErrors = telemetryErrors;
      await safe('diagnostic write', () => writeFile(testInfo.outputPath('platform.json'), JSON.stringify(results, null, 2)));
      await safe('page CDP detach', async () => { await pageCdp?.detach(); });
      await safe('browser CDP detach', async () => { await cdp?.detach(); });
      await safe('browser close', async () => { await browser?.close(); });
      await safe('monitor close', () => monitor.close());
      // Include teardown errors without replacing the primary clock failure.
      await writeFile(testInfo.outputPath('platform.json'), JSON.stringify(results, null, 2));
      await testInfo.attach('native-platform', { path: testInfo.outputPath('platform.json'), contentType: 'application/json' });
      if (!primaryError) {
        expect(results.afterGraph).toEqual(beforeGraph);
        expect(telemetryErrors).toEqual([]);
      }
    }
  });
}
