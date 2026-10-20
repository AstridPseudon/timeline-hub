import { expect } from '@playwright/test';
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import {
  test, captureReadiness, clickPlay, evaluateWithoutGesture, findPlayer,
  observedGraph, observeCapture, observeFrames,
} from './player-audio-browser';
import { CAPTURE_TIMELINE, publishCaptureFixture } from './player-audio-fixture';
import { audibleEdges, decodeMonitor } from './player-audio-monitor';
import { phaseGainTable, phaseSourcePcm, phaseSourceWav } from './player-audio-phase';
import { measureColdPhase, measureFlatCalibration, qualifyPhysicalPhase } from './player-audio-phase-qualification';
import { editorUrl, FAKE_RUNTIME_ORIGIN, PROJECT_SLUG, fakeRuntimeAuthHeaders, resetFakeRuntimeBaseline } from './support';

const exec = promisify(execFile);
const sha = (bytes: Uint8Array) => createHash('sha256').update(bytes).digest('hex');
async function preflight(stage: string, measurement = true) {
  const { stdout } = await exec('python', [process.env.PLAYER_AUDIO_PHASE_PREFLIGHT!, ...(measurement ? ['--measurement'] : [])]);
  return { stage, ...JSON.parse(stdout) };
}

test.use({ trace: { mode: 'retain-on-failure', snapshots: false, screenshots: false } });

test('amplified first-cold physical phase then explicit flat calibration', async ({ browser, context, monitor }, testInfo) => {
  test.setTimeout(180_000);
  expect(process.env.PLAYER_AUDIO_PHASE_PHYSICAL).toBe('1');
  expect(process.env.PLAYER_AUDIO_OBSERVE).toBe('1');
  expect(process.env.PLAYER_AUDIO_CAPTURE).toBeUndefined();
  expect(testInfo.repeatEachIndex).toBe(0);
  const source = phaseSourcePcm();
  const wav = phaseSourceWav(source);
  const results: Record<string, unknown> = {
    scope: 'one amplified cold diagnostic, then flat calibration; no original-baseline or Gate 6 qualification',
    sourceSha256: sha(wav), pcmSha256: sha(new Uint8Array(source.buffer)),
    beforeGraph: await observedGraph(), browser: browser.version(), node: process.version,
    launchOptions: testInfo.project.use.launchOptions,
  };
  await writeFile(testInfo.outputPath('source.wav'), wav);
  await writeFile(testInfo.outputPath('source.pcm16'), new Uint8Array(source.buffer));
  const cdp = await browser.newBrowserCDPSession();
  let cold: ReturnType<typeof measureColdPhase> | undefined;
  let calibration: ReturnType<typeof measureFlatCalibration> | undefined;
  try {
    expect(await resetFakeRuntimeBaseline()).toBeNull();
    const id = `sha256:${sha(wav)}`;
    const response = await fetch(`${FAKE_RUNTIME_ORIGIN}/v1/projects/${PROJECT_SLUG}/objects`, {
      method: 'POST', headers: {
        ...fakeRuntimeAuthHeaders(), 'Content-Type': 'audio/wav',
        'Idempotency-Key': id, 'X-Original-Name': 'amplified-phase.wav',
      }, body: wav,
    });
    expect(response.status).toBe(201);
    expect((await response.json()).data.object_id).toBe(id);
    // publishCaptureFixture reads only the selected backend's object.
    const objects = { native: id, amplified: id, video: id };
    for (const name of ['cold', 'flat-calibration'] as const) {
      const faded = name === 'cold';
      const revision = await publishCaptureFixture(objects, ['amplified'], faded);
      // Explicit new-page calibration after cold: same browser/Pulse monitor,
      // new mounted root and its App-owned context; no in-page reset or warm-up.
      const page = await context.newPage();
      const requests: Array<{ url: string; status: number }> = [];
      const errors: string[] = [];
      const moduleResponses: Array<{ url: string; status: number }> = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('response', response => {
        if (response.request().resourceType() === 'script') moduleResponses.push({ url: response.url(), status: response.status() });
        if (decodeURIComponent(response.url()).includes(id)) requests.push({ url: response.url(), status: response.status() });
      });
      page.on('console', message => {
        if (['warning', 'error'].includes(message.type())) console.log('PLAYER_CONSOLE', name, message.text());
      });
      let consumer: Awaited<ReturnType<typeof monitor.drain>> | undefined;
      const cell: Record<string, unknown> = { revision: revision.headRevisionId, faded, object: id, moduleResponses };
      results[name] = cell;
      try {
        await page.addInitScript(observeCapture, { fallback: false });
        await page.goto(editorUrl({ timeline: CAPTURE_TIMELINE }), { waitUntil: 'domcontentloaded' });
        await expect.poll(() => evaluateWithoutGesture(page, () => {
          const button = document.querySelector('.astrid-preview-transport button[aria-label="Play"]');
          return Boolean(button?.getBoundingClientRect().width);
        }), { timeout: 90_000 }).toBe(true);
        await findPlayer(page);
        // Baseline's initial setup, once per mounted root, before any gesture.
        await evaluateWithoutGesture(page, () => {
          window.__capturePlayer.pause();
          window.__capturePlayer.seekTo(0);
          window.__capturePlayer.setVolume(1);
          window.__capturePlayer.unmute();
        });
        await expect.poll(() => evaluateWithoutGesture(page, () => window.__capturePlayer.getCurrentFrame())).toBe(0);
        await expect.poll(() => evaluateWithoutGesture(page, () => {
          const elements = [...document.querySelectorAll<HTMLAudioElement>('audio[src]')];
          return elements.length > 0 && elements.every(element => element.readyState >= 2);
        }), { timeout: 20_000 }).toBe(true);
        consumer = await monitor.drain(testInfo.outputPath(`${name}-consumer.json`), () => cdp.send('SystemInfo.getProcessInfo'));
        await evaluateWithoutGesture(page, observeFrames);
        const readiness = await evaluateWithoutGesture(page, captureReadiness);
        cell.readiness = readiness;
        cell.monitorBeforeCapture = await monitor.inspect();
        expect(readiness.userActivation, 'cold root unactivated before its measured gesture').toBe(false);
        expect(readiness.muted, 'no automatic mute hidden by a reset').toBe(false);
        expect(readiness.visibility).toBe('visible');
        expect(readiness.media.length).toBeGreaterThan(0);
        cell.preflight = await preflight(`${name}-before-measurement`);
        cell.beforeGraph = await observedGraph();
        await consumer.snapshot('before-measurement');
        const path = testInfo.outputPath(`${name}.wav`);
        try {
          await monitor.record(path, () => clickPlay(page), 1, () => cdp.send('SystemInfo.getProcessInfo'));
          await consumer.snapshot('after-measurement');
        } finally {
          cell.recording = JSON.parse(await readFile(`${path}.diagnostics.json`, 'utf8'));
          cell.events = await evaluateWithoutGesture(page, () => window.__captureEvents);
          cell.frames = await evaluateWithoutGesture(page, () => window.__captureFrames);
          cell.afterGraph = await observedGraph();
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
        const starts = await evaluateWithoutGesture(page, () => window.__captureEvents.filter(event => event.type === 'media-play-call')) as Array<{
          epochMs: number; src: string; playerFrame: number; currentTime: number;
          contexts: Array<{ state: AudioContextState; currentTime: number; output: AudioTimestamp }>;
        }>;
        const measuredStarts = starts.filter(event => event.epochMs >= readiness.epochMs && decodeURIComponent(event.src).includes(id));
        const clock = {
          first, last, drift, sourceLeads, sourceLeadMedian, sourceLeadMin: sourceLeads[0], sourceLeadMax: sourceLeads.at(-1),
          measuredStarts, events: moving.length, finalFrame: Math.max(...frames.map(frame => frame.frame)),
          withinOriginalDomBound: sourceLeads.length > 30 && Math.abs(sourceLeadMedian) < 1 / 30,
        };
        cell.clock = clock;
        // Preserve the baseline DOM bounds alongside the independent physical
        // result. Soft failure still permits the later calibration to be saved.
        expect.soft(sourceLeads.length, 'source/frame clock observations').toBeGreaterThan(30);
        expect.soft(Math.abs(sourceLeadMedian), 'native source and authored gain frame must agree within one frame').toBeLessThan(1 / 30);
        expect.soft(clock.finalFrame).toBeGreaterThanOrEqual(118);
        expect.soft(Math.abs(clock.drift), 'Player wall clock drift during capture').toBeLessThan(0.12);
        expect.soft(measuredStarts.length, 'actual amplified source start observations').toBeGreaterThan(0);
        for (const firstStart of measuredStarts.slice(0, 1)) {
          expect.soft(firstStart.playerFrame).toBe(0);
          expect.soft(firstStart.currentTime).toBeLessThan(1 / 30);
          expect.soft(firstStart.contexts.length).toBeGreaterThan(0);
          for (const context of firstStart.contexts) {
            expect.soft(context.state, 'context ready before native source starts').toBe('running');
            expect.soft(context.output.contextTime, 'fresh output before native source starts').toBeGreaterThan(0);
            expect.soft(context.output.performanceTime).toBeGreaterThan(0);
          }
        }
        const capture = await decodeMonitor(path);
        const { onset, offset, active } = audibleEdges(capture);
        cell.capture = { onset, offset, activeBlocks: active.length, sha256: sha(await readFile(path)), sampleCount: capture.sampleCount };
        // Silent/missing input is inconclusive; it must not invent a valid onset.
        if (Number.isFinite(onset) && onset <= 2) {
          if (faded) cold = measureColdPhase(capture.pcm, source, phaseGainTable('amplified'), onset);
          else calibration = measureFlatCalibration(capture.pcm, source, onset);
        }
        cell.physical = faded ? cold : calibration;
        const backendState = await evaluateWithoutGesture(page, () => window.__captureBackends);
        cell.backendState = backendState;
        cell.requests = requests;
        cell.errors = errors;
        expect.soft(requests.some(request => [200, 206].includes(request.status)), 'managed amplified fetched').toBe(true);
        expect.soft(backendState.elements.some(url => decodeURIComponent(url).includes(id))).toBe(true);
        expect.soft(errors).toEqual([]);
        expect.soft(await page.getByTestId('preview-media-error').count()).toBe(0);
      } finally {
        cell.lifecycleEvents = await evaluateWithoutGesture(page, () => window.__captureEvents).catch(() => null);
        try { if (consumer) cell.consumer = await consumer.close(); } finally { await page.close(); }
      }
    }
  } catch (error) {
    results.executionFailure = String(error);
    throw error;
  } finally {
    results.verdict = cold && !results.executionFailure ? qualifyPhysicalPhase(cold, calibration) : 'inconclusive';
    const coldCell = results.cold as { clock?: { withinOriginalDomBound: boolean } } | undefined;
    // Persist every observation even if a graph check or capture failed.
    try {
      results.afterGraph = await observedGraph();
      results.postflight = await preflight('after-or-failure', false);
    } catch (error) {
      results.verdict = 'inconclusive';
      results.postflightFailure = String(error);
    } finally {
      results.domViolatesWhilePhysicalCompatible = results.verdict === 'compatible' && coldCell?.clock?.withinOriginalDomBound === false;
      const path = testInfo.outputPath('phase-physical-metrics.json');
      await writeFile(path, JSON.stringify(results, null, 2));
      await testInfo.attach('phase-physical-metrics', { path, contentType: 'application/json' });
      await cdp.detach();
    }
  }
  expect(results.verdict, 'instrument must qualify before phase attribution').not.toBe('inconclusive');
  expect(results.verdict, 'strict physical gain/source phase bound').toBe('compatible');
});
