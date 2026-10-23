// @vitest-environment jsdom
import { act, fireEvent, render, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import {
  exitEditorTour,
  getEditorTourState,
  setEditorTourBeat,
  skipEditorTourAnimation,
  startEditorTour,
  type EditorTourAct,
  type EditorTourBeat,
} from '@/shared/state/editorTourStore.ts';
import {
  TimelineStoreProvider,
  createTimelineStore,
  type TimelineStoreApi,
} from '@/tools/video-editor/hooks/timelineStore.ts';
import { EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS } from '@/tools/video-editor/tour/anchors.ts';
import { loadTourLiveScene, TOUR_SCENE_SOURCE_FROM } from './tourSceneSource.ts';
import { EDITOR_TOUR_MEDIA } from '../tourMedia.ts';
import { TOUR_CLIP_IDS } from './tourStages.ts';

const fakeLiveScene = { kind: 'fake-live-scene' };
const harness = vi.hoisted(() => ({
  warmups: [] as Array<{ sourceTime: number; onReady?: (info: unknown) => void }>,
  centered: [] as string[],
}));

vi.mock('./tourSceneSource.ts', async (importOriginal) => ({
  ...(await importOriginal<typeof import('./tourSceneSource.ts')>()),
  loadTourLiveScene: vi.fn(async () => fakeLiveScene),
}));
vi.mock('@/tools/video-editor/lib/timeline-viewport-events.ts', () => ({
  requestCenterTimelineClip: (clipId: string) => { harness.centered.push(clipId); },
}));
vi.mock('@astrid/packs/rendering/ui/threejs-live-editor/SceneSurface', () => ({
  SceneSurface: (props: { sourceTime: number; onReady?: (info: unknown) => void }) => {
    harness.warmups.push(props);
    return <div data-testid="warm-scene" data-source-time={props.sourceTime} />;
  },
}));

import { EditorTourTimelineDriver, TOUR_ANCHOR_DWELL_MS } from './EditorTourTimelineDriver.tsx';

function createHarness() {
  const calls: string[] = [];
  const apply = vi.fn((patch: { operations: ReadonlyArray<{ op: string }> }) => {
    calls.push(`apply:${patch.operations[0].op}`);
    return {};
  });
  const previewHandle = {
    seek: vi.fn((time: number) => { calls.push(`seek:${time}`); }),
    play: vi.fn(() => { calls.push('play'); }),
    pause: vi.fn(() => { calls.push('pause'); }),
  };
  const store: TimelineStoreApi = createTimelineStore();
  store.setState((state) => ({
    ...state,
    timelineOps: { apply } as never,
    data: { ...state.data, isLoading: false, data: {} as never },
    playback: { ...state.playback, previewRef: { current: previewHandle } as never },
  }));
  const view = render(
    <TimelineStoreProvider store={store}>
      <EditorTourTimelineDriver />
    </TimelineStoreProvider>,
  );
  return { apply, calls, previewHandle, ...view };
}

const goTo = (act: EditorTourAct, beat: EditorTourBeat) => act_(() => setEditorTourBeat(act, beat));
const act_ = (fn: () => void) => act(() => { fn(); });
const ready = () => getEditorTourState().ready.timeline;

/** The visible live scene's status element, as `SceneSurface` renders it. */
function addScene(phase: 'loading' | 'ready'): HTMLElement {
  const scene = document.createElement('div');
  scene.setAttribute('data-testid', 'astrid-live-scene-entry');
  scene.setAttribute('data-phase', phase);
  document.body.append(scene);
  return scene;
}

describe('EditorTourTimelineDriver', () => {
  let trackRow: HTMLElement;
  let preview: HTMLElement;
  function addDecodedVideo(frame: number, parent = preview, src = EDITOR_TOUR_MEDIA.video.url) {
    const marker = document.createElement('span');
    marker.dataset.previewDecodedFrame = 'true';
    marker.dataset.previewMediaSrc = src;
    marker.dataset.previewPresentedFrame = String(frame);
    parent.append(marker);
    return marker;
  }

  beforeEach(() => {
    harness.warmups.length = 0;
    harness.centered.length = 0;
    // The landed row the driver waits for before it scrolls and plays.
    trackRow = document.createElement('div');
    trackRow.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS.scene);
    document.body.append(trackRow);
    preview = document.createElement('div');
    preview.dataset.editorTour = 'preview';
    document.body.append(preview);
    addDecodedVideo(0);
    act_(() => startEditorTour());
  });

  afterEach(() => {
    trackRow.remove();
    preview.remove();
    document.querySelectorAll(`[${EDITOR_TOUR_TRACK_ATTRIBUTE}]`).forEach((row) => row.remove());
    document.querySelectorAll('[data-testid="astrid-live-scene-entry"]').forEach((scene) => scene.remove());
    vi.useRealTimers();
    vi.restoreAllMocks();
    act_(() => exitEditorTour());
  });

  it('shows a retry when the world fails to load and lands the stage after retry succeeds', async () => {
    vi.mocked(loadTourLiveScene).mockRejectedValueOnce(new Error('offline'));
    const view = createHarness();
    addScene('ready');
    goTo(1, 'land');
    expect(await view.findByRole('alert')).toHaveTextContent('could not load');
    expect(view.apply).not.toHaveBeenCalled();
    fireEvent.click(view.getByRole('button', { name: 'Retry demo' }));
    await waitFor(() => expect(view.apply).toHaveBeenCalledTimes(1));
    await waitFor(() => expect(ready()).toBe(true));
    expect(view.queryByRole('alert')).toBeNull();
  });

  let presentationClock = 0;
  async function beginAnchorPresentation() {
    presentationClock = 0;
    const realNow = performance.now.bind(performance);
    vi.spyOn(performance, 'now').mockImplementation(() => realNow() + presentationClock);
    const view = createHarness();
    const row = document.createElement('div');
    row.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS.stills);
    document.body.append(row);
    goTo(2, 'land');
    await waitFor(() => expect(view.previewHandle.seek).toHaveBeenCalledWith(0));
    return view;
  }

  const dwell = () => act(async () => {
    presentationClock += TOUR_ANCHOR_DWELL_MS + 32;
    await new Promise((resolve) => setTimeout(resolve, 35));
  });

  it('presents all four anchors in order with a readable dwell and holds the final frame', async () => {
    const { previewHandle } = await beginAnchorPresentation();
    expect(ready()).toBe(false);
    expect(previewHandle.seek.mock.calls).toEqual([[0]]);
    await dwell();
    expect(previewHandle.seek.mock.calls).toEqual([[0], [6.5]]);
    await dwell();
    expect(previewHandle.seek.mock.calls).toEqual([[0], [6.5], [10]]);
    await dwell();
    expect(previewHandle.seek.mock.calls).toEqual([[0], [6.5], [10], [13]]);
    expect(ready()).toBe(false);
    await dwell();
    expect(ready()).toBe(true);
    expect(harness.centered).toEqual([...TOUR_CLIP_IDS.stills]);
    expect(previewHandle.pause).toHaveBeenCalledTimes(1);
    expect(previewHandle.play).not.toHaveBeenCalled();
    await dwell();
    expect(previewHandle.seek).toHaveBeenCalledTimes(4);
  });

  it.each(['back', 'skip', 'exit', 'unmount', 'next-act'] as const)('cancels the anchor presentation on %s without delayed seeks', async (destination) => {
    const view = await beginAnchorPresentation();
    await dwell();
    expect(view.previewHandle.seek.mock.calls).toEqual([[0], [6.5]]);
    if (destination === 'back') act_(() => setEditorTourBeat(2, 'compose', true));
    if (destination === 'skip') act_(() => skipEditorTourAnimation());
    if (destination === 'exit') act_(() => exitEditorTour());
    if (destination === 'unmount') view.unmount();
    if (destination === 'next-act') {
      const row = document.createElement('div');
      row.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS.videos);
      document.body.append(row);
      goTo(3, 'land');
    }
    await dwell();
    const calls = view.previewHandle.seek.mock.calls.map(([time]) => time);
    expect(calls).toEqual(destination === 'next-act' ? [0, 6.5, 0] : [0, 6.5]);
    presentationClock += 10_000;
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 35)); });
    expect(view.previewHandle.seek.mock.calls.map(([time]) => time)).toEqual(calls);
    if (destination === 'skip') expect(ready()).toBe(true);
  });

  async function beginVideoLanding() {
    preview.replaceChildren();
    const view = createHarness();
    for (const id of [EDITOR_TOUR_TRACK_IDS.stills, EDITOR_TOUR_TRACK_IDS.videos]) {
      const row = document.createElement('div');
      row.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, id);
      document.body.append(row);
    }
    act_(() => setEditorTourBeat(2, 'land', true));
    await waitFor(() => expect(ready()).toBe(true));
    expect(view.previewHandle.seek).toHaveBeenLastCalledWith(13);
    view.previewHandle.seek.mockClear();
    view.previewHandle.play.mockClear();
    goTo(3, 'land');
    await waitFor(() => expect(view.apply).toHaveBeenCalledTimes(3));
    return view;
  }

  it('keeps the town frame while the new video composition arrives, then waits for decoded frame zero before playing', async () => {
    const view = await beginVideoLanding();
    // Track DOM and the preview handle exist, but the old paused composition is still displayed.
    const elsewhere = addDecodedVideo(0, document.body);
    addDecodedVideo(0, preview, '/different-video.mp4');
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 50)); });
    expect(view.previewHandle.seek).not.toHaveBeenCalled();
    expect(view.previewHandle.play).not.toHaveBeenCalled();
    expect(ready()).toBe(false);
    const video = addDecodedVideo(390, preview, new URL(EDITOR_TOUR_MEDIA.video.url, document.baseURI).href);
    await waitFor(() => expect(view.previewHandle.seek).toHaveBeenCalledWith(0));
    expect(view.previewHandle.play).not.toHaveBeenCalled();
    expect(ready()).toBe(false);
    video.dataset.previewPresentedFrame = '0';
    await waitFor(() => expect(view.previewHandle.play).toHaveBeenCalledTimes(1));
    expect(ready()).toBe(true);
    elsewhere.remove();
  });

  it.each(['before-seek', 'after-seek'] as const)('cancels video readiness %s when leaving the beat, without late playback', async (phase) => {
    const view = await beginVideoLanding();
    let video: HTMLElement | undefined;
    if (phase === 'after-seek') {
      video = addDecodedVideo(390);
      await waitFor(() => expect(view.previewHandle.seek).toHaveBeenCalledWith(0));
    }
    act_(() => setEditorTourBeat(3, 'compose', true));
    if (video) video.dataset.previewPresentedFrame = '0';
    else addDecodedVideo(0);
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 50)); });
    expect(view.previewHandle.play).not.toHaveBeenCalled();
    expect(view.previewHandle.seek).toHaveBeenCalledTimes(phase === 'after-seek' ? 1 : 0);
  });

  it('lets Skip finish a video wait without seeking or playing the old composition', async () => {
    const view = await beginVideoLanding();
    act_(() => skipEditorTourAnimation());
    await waitFor(() => expect(ready()).toBe(true));
    addDecodedVideo(0);
    await act(async () => { await new Promise((resolve) => setTimeout(resolve, 50)); });
    expect(view.previewHandle.seek).not.toHaveBeenCalled();
    expect(view.previewHandle.play).not.toHaveBeenCalled();
  });

  it('reports ready on compose without touching the timeline or booting a scene', async () => {
    const { apply, queryByTestId } = createHarness();
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).not.toHaveBeenCalled();
    expect(queryByTestId('warm-scene')).toBeNull();
  });

  it('warms the scene during act 1 respond and holds ready until it has booted', async () => {
    const { apply, findByTestId } = createHarness();
    await waitFor(() => expect(ready()).toBe(true));

    goTo(1, 'respond');
    const warm = await findByTestId('warm-scene');
    // Seeked into the clip's source range, so the world is compiled at the frame 1c will show.
    expect(warm).toHaveAttribute('data-source-time', String(TOUR_SCENE_SOURCE_FROM));
    expect(ready()).toBe(false);
    expect(apply).not.toHaveBeenCalled();

    act_(() => harness.warmups.at(-1)!.onReady?.({}));
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).not.toHaveBeenCalled();
  });

  it('lands each stage through ops.apply, scrolls to its first clip, then seeks 0 and plays (act 2 holds its last frame when entered instantly)', async () => {
    const { apply, calls, previewHandle } = createHarness();
    addScene('ready');

    goTo(1, 'land');
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).toHaveBeenCalledTimes(1);
    expect(apply.mock.calls[0][0]).toMatchObject({ source: 'editor-tour', version: 0 });
    expect(apply.mock.calls[0][0].operations.map((operation: { op: string }) => operation.op)).toEqual(['track.update', 'clip.add', 'clip.update']);
    expect(harness.centered).toEqual([TOUR_CLIP_IDS.scene]);
    expect(previewHandle.seek).toHaveBeenCalledWith(0);
    expect(previewHandle.play).toHaveBeenCalledTimes(1);
    expect(calls.indexOf('seek:0')).toBeGreaterThan(calls.indexOf('apply:clip.add'));
    expect(calls.indexOf('play')).toBeGreaterThan(calls.indexOf('seek:0'));
    // It pauses before seeking, so the seek isn't lost to an earlier act's playback.
    expect(calls.indexOf('pause')).toBeLessThan(calls.indexOf('seek:0'));

    // Staying on stage 1 through act 2's compose and respond applies nothing more.
    goTo(2, 'compose');
    await waitFor(() => expect(ready()).toBe(true));
    goTo(2, 'respond');
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).toHaveBeenCalledTimes(1);

    const stillsRow = document.createElement('div');
    stillsRow.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS.stills);
    document.body.append(stillsRow);
    act_(() => setEditorTourBeat(2, 'land', true));
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).toHaveBeenCalledTimes(2);
    expect(apply.mock.calls[1][0].operations[0].op).toBe('track.add');
    expect(apply.mock.calls[1][0].operations[0].payload).toMatchObject({ before: EDITOR_TOUR_TRACK_IDS.scene });
    expect(harness.centered).toEqual([TOUR_CLIP_IDS.scene, TOUR_CLIP_IDS.stills[3]]);
    // An instant arrival skips the presentation and holds the last reference frame.
    expect(previewHandle.seek).toHaveBeenCalledTimes(2);
    expect(previewHandle.play).toHaveBeenCalledTimes(1);
    expect(previewHandle.pause).toHaveBeenCalledTimes(2);
    expect(calls.slice(-2)).toEqual(['pause', 'seek:13']);

    const videosRow = document.createElement('div');
    videosRow.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS.videos);
    document.body.append(videosRow);
    goTo(3, 'land');
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).toHaveBeenCalledTimes(3);
    expect(apply.mock.calls[2][0].operations[0].payload).toMatchObject({ before: EDITOR_TOUR_TRACK_IDS.stills });
    expect(harness.centered.at(-1)).toBe(TOUR_CLIP_IDS.video);
    expect(previewHandle.play).toHaveBeenCalledTimes(2);
  });

  it('steps back a stage by removing the later rows at once, and replays the landing going forward', async () => {
    const { apply, previewHandle } = createHarness();
    addScene('ready');
    const rows = [EDITOR_TOUR_TRACK_IDS.stills, EDITOR_TOUR_TRACK_IDS.videos].map((id) => {
      const row = document.createElement('div');
      row.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, id);
      document.body.append(row);
      return row;
    });
    const targetsOf = () => apply.mock.calls.map(([patch]) => `${patch.operations[0].op}:${patch.operations[0].target}`);

    goTo(1, 'land');
    await waitFor(() => expect(ready()).toBe(true));
    act_(() => setEditorTourBeat(2, 'land', true));
    await waitFor(() => expect(ready()).toBe(true));
    expect(apply).toHaveBeenCalledTimes(2);

    // Back from land(2) to compose(2): the stills row goes at once, nothing is replayed.
    previewHandle.play.mockClear();
    act_(() => setEditorTourBeat(2, 'compose', true));
    await waitFor(() => expect(apply).toHaveBeenCalledTimes(3));
    expect(targetsOf()[2]).toBe(`track.remove:${EDITOR_TOUR_TRACK_IDS.stills}`);
    expect(previewHandle.play).not.toHaveBeenCalled();

    // Forward again lands the stills row afresh.
    act_(() => setEditorTourBeat(2, 'land', true));
    await waitFor(() => expect(apply).toHaveBeenCalledTimes(4));
    expect(apply.mock.calls[3][0].operations[0].op).toBe('track.add');

    // Back from land(1) to respond(1) removes the scene clip, with no warm-up and no waiting on a scene.
    act_(() => setEditorTourBeat(1, 'respond', true));
    await waitFor(() => expect(apply.mock.calls.slice(4).map(([patch]) => patch.operations[0].op)).toEqual(['track.remove', 'clip.remove']));
    expect(apply.mock.calls[5][0].operations[0].target).toBe(TOUR_CLIP_IDS.scene);
    expect(apply.mock.calls[5][0].operations[1]).toMatchObject({ op: 'track.update', target: EDITOR_TOUR_TRACK_IDS.scene, payload: { label: 'V1' } });
    await waitFor(() => expect(ready()).toBe(true));
    expect(harness.warmups).toHaveLength(0);
    rows.forEach((row) => row.remove());
  });

  it('holds act 1 land at 0 until the visible scene has painted, then plays and reports ready', async () => {
    const { previewHandle } = createHarness();
    const scene = addScene('loading');

    goTo(1, 'land');
    await waitFor(() => expect(previewHandle.seek).toHaveBeenCalledWith(0));
    await new Promise((resolve) => setTimeout(resolve, 150));
    expect(previewHandle.play).not.toHaveBeenCalled();
    expect(ready()).toBe(false);

    scene.setAttribute('data-phase', 'ready');
    await waitFor(() => expect(ready()).toBe(true));
    expect(previewHandle.play).toHaveBeenCalledTimes(1);
  });

  it('lets the first Enter (skipAnimation) end the scene wait', async () => {
    const { previewHandle } = createHarness();
    addScene('loading');

    goTo(1, 'land');
    await waitFor(() => expect(previewHandle.seek).toHaveBeenCalledWith(0));
    expect(ready()).toBe(false);

    act_(() => skipEditorTourAnimation());
    await waitFor(() => expect(ready()).toBe(true));
    expect(previewHandle.play).toHaveBeenCalledTimes(1);
  });

  it('never hangs on a scene that does not report: it plays and reports ready after the give-up wait', async () => {
    const realNow = performance.now.bind(performance);
    let offset = 0;
    vi.spyOn(performance, 'now').mockImplementation(() => realNow() + offset);
    const { previewHandle } = createHarness();
    addScene('loading');

    goTo(1, 'land');
    await waitFor(() => expect(previewHandle.seek).toHaveBeenCalledWith(0));
    expect(ready()).toBe(false);

    offset = 9000;
    await waitFor(() => expect(ready()).toBe(true));
    expect(previewHandle.play).toHaveBeenCalledTimes(1);
  });

  it('does not wait for the scene on later acts, where the preview shows other media', async () => {
    const { previewHandle } = createHarness();
    addScene('ready');
    goTo(1, 'land');
    await waitFor(() => expect(ready()).toBe(true));
    document.querySelectorAll('[data-testid="astrid-live-scene-entry"]').forEach((scene) => scene.remove());
    addScene('loading');

    const stillsRow = document.createElement('div');
    stillsRow.setAttribute(EDITOR_TOUR_TRACK_ATTRIBUTE, EDITOR_TOUR_TRACK_IDS.stills);
    document.body.append(stillsRow);
    act_(() => setEditorTourBeat(2, 'land', true));
    await waitFor(() => expect(ready()).toBe(true));
    expect(previewHandle.seek).toHaveBeenCalledTimes(2);
    expect(previewHandle.pause).toHaveBeenCalledTimes(2);
  });

  it('retries a stage whose apply threw instead of stalling the tour', async () => {
    const { apply } = createHarness();
    apply.mockImplementationOnce(() => { throw new Error('not ready'); });
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    addScene('ready');

    goTo(1, 'land');
    await waitFor(() => expect(ready()).toBe(true), { timeout: 3000 });
    expect(apply).toHaveBeenCalledTimes(2);
  });
});
