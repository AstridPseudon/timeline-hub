// @vitest-environment jsdom
import { createElement } from 'react';
import { act, cleanup, fireEvent, render, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { WorldExplorerPanel } from '../../../astrid/packs/rendering/ui/threejs-live-editor/explorer/WorldExplorerPanel';
import { ingestPreparedPackage, parsePreparedScenePackage } from '../../../astrid/packs/rendering/ui/threejs-live-editor/authoring';
import { SAMPLE_WORLD } from '../../../astrid/packs/rendering/ui/threejs-live-editor/explorer/worlds/sample';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../../../astrid/packs/rendering/ui/threejs-live-editor/identity';

// Module-level handle on the scene surface: the mock records every render (all the props the panel passes) and keeps the latest callbacks.
const scene = vi.hoisted(() => ({
  renders: [] as Array<{ sourceTime: number; worldTime?: number; view?: { position: [number, number, number] }; width: number; height: number }>,
  onStatus: null as null | ((status: unknown) => void),
  onReady: null as null | ((info: unknown) => void),
}));

vi.mock('../../../astrid/packs/rendering/ui/threejs-live-editor/SceneSurface', () => ({
  SceneSurface: (props: {
    sourceTime: number; worldTime?: number; view?: { position: [number, number, number] }; width: number; height: number;
    onStatus: (status: unknown) => void; onReady: (info: unknown) => void;
  }) => {
    scene.renders.push({ sourceTime: props.sourceTime, worldTime: props.worldTime, view: props.view, width: props.width, height: props.height });
    scene.onStatus = props.onStatus;
    scene.onReady = props.onReady;
    return null;
  },
}));

// Deterministic animation frames: requestAnimationFrame queues, performance.now is a fake clock.
let pending = new Map<number, FrameRequestCallback>();
let nextFrame = 1;
let nowMs = 1000;

function frames(count: number) {
  for (let i = 0; i < count; i += 1) {
    nowMs += 16;
    const due = [...pending.values()];
    pending.clear();
    act(() => {
      for (const callback of due) callback(nowMs);
    });
  }
}

beforeEach(() => {
  pending = new Map();
  nextFrame = 1;
  nowMs = 1000;
  scene.renders.length = 0;
  scene.onStatus = null;
  scene.onReady = null;
  vi.stubGlobal('requestAnimationFrame', (callback: FrameRequestCallback) => {
    const id = nextFrame++;
    pending.set(id, callback);
    return id;
  });
  vi.stubGlobal('cancelAnimationFrame', (id: number) => {
    pending.delete(id);
  });
  vi.spyOn(performance, 'now').mockImplementation(() => nowMs);
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

async function sha256(bytes: Uint8Array): Promise<string> {
  const hash = await globalThis.crypto.subtle.digest('SHA-256', bytes as unknown as BufferSource);
  return `sha256:${Array.from(new Uint8Array(hash), (byte) => byte.toString(16).padStart(2, '0')).join('')}`;
}

/** In-memory project object store with real digests, mirroring test_live_scene_authoring. */
function makeStorage(objects = new Map<string, Uint8Array>()) {
  return {
    objects,
    async ingest(input: Uint8Array, mediaType: string, filename?: string) {
      const bytes = new Uint8Array(input);
      const digest = await sha256(bytes);
      objects.set(digest, bytes);
      return { object_id: digest, digest, media_type: mediaType, size: bytes.byteLength, filename };
    },
    async read(objectId: string) {
      const value = objects.get(objectId);
      if (!value) throw new Error(`unknown object ${objectId}`);
      return new Uint8Array(value);
    },
  };
}

function makeSettings(store = new Map<string, unknown>()) {
  return {
    store,
    get: (key: string) => store.get(key),
    set: (key: string, value: unknown) => { store.set(key, value); },
    delete: (key: string) => store.delete(key),
    keys: () => [...store.keys()],
    subscribe: () => ({ dispose() {} }),
  };
}

/** The sample package as a real live scene envelope, the same shape a timeline clip carries. */
async function sampleLiveScene() {
  const parsed = await parsePreparedScenePackage(new TextEncoder().encode(SAMPLE_WORLD.packageJson));
  const ingested = await ingestPreparedPackage(makeStorage(), parsed);
  return { liveScene: ingested.liveScene, duration: parsed.manifest.duration };
}
const SAMPLE = await sampleLiveScene();

/** What a scene declares when it supports free roam: a start view the viewer can move from. */
const EXPLORE = { start: { position: [0, 1, 5] as [number, number, number], target: [0, 1, 0] as [number, number, number] } };

function liveClip(id = 'c1') {
  return {
    id,
    track: 'V1',
    at: 2,
    duration: 3,
    clipType: LIVE_SCENE_CLIP_TYPE_ID,
    sourceOffset: 1,
    sourceEnd: 4,
    rate: 1,
    managed: false,
    app: { liveScene: SAMPLE.liveScene },
  };
}

type HarnessOptions = {
  projectId?: string | null;
  clips?: unknown[];
  settings?: ReturnType<typeof makeSettings>;
  storage?: ReturnType<typeof makeStorage>;
};

function makeHarness(options: HarnessOptions = {}) {
  const projectId = options.projectId === undefined ? 'p1' : options.projectId;
  const settings = options.settings ?? makeSettings();
  const storage = options.storage ?? makeStorage();
  let snapshot: Record<string, unknown> = {
    projectId,
    timelineId: 't1',
    baseVersion: 1,
    tracks: [{ id: 'V1', kind: 'visual', label: 'V1', muted: false }],
    clips: options.clips ?? [],
    outputMetadata: { resolution: '1280x720' },
  };
  const readerListeners = new Set<() => void>();
  const timeline = {
    validate: vi.fn(() => ({ valid: true, diagnostics: [] })),
    apply: vi.fn((patch: { operations: Array<{ target: string }> }) => ({
      affectedObjectIds: patch.operations.map((operation) => operation.target),
    })),
    flush: vi.fn(async () => ({ version: 2 })),
  };
  const toast = vi.fn();
  const report = vi.fn();
  const ctx = {
    creative: {
      reader: {
        snapshot: () => snapshot,
        subscribe: (listener: () => void) => {
          readerListeners.add(listener);
          return () => { readerListeners.delete(listener); };
        },
      },
      timeline,
      projectObjects: storage,
    },
    services: { settings, diagnostics: { report } },
    chrome: { toast },
  };

  let viewSnapshot: { playhead: { time: number }; selection: { selectedClipIds: Set<string> } } = {
    playhead: { time: 4 },
    selection: { selectedClipIds: new Set<string>() },
  };
  const viewListeners = new Set<() => void>();
  const seek = vi.fn();
  const video = {
    view: {
      getSnapshot: () => viewSnapshot,
      subscribe: (listener: () => void) => {
        viewListeners.add(listener);
        return { dispose: () => { viewListeners.delete(listener); } };
      },
    },
    seek,
  };

  return {
    ctx: ctx as unknown as Parameters<typeof WorldExplorerPanel>[0]['context'],
    raw: ctx,
    settings,
    storage,
    timeline,
    toast,
    report,
    seek,
    video,
    setClips(clips: unknown[]) {
      snapshot = { ...snapshot, clips };
      act(() => readerListeners.forEach((listener) => listener()));
    },
    setPlayhead(time: number) {
      viewSnapshot = { ...viewSnapshot, playhead: { time } };
    },
    selectClip(ids: string[]) {
      viewSnapshot = { ...viewSnapshot, selection: { selectedClipIds: new Set(ids) } };
      act(() => viewListeners.forEach((listener) => listener()));
    },
  };
}

function mount(harness: ReturnType<typeof makeHarness>, visible = true) {
  const element = (value: boolean) => createElement(WorldExplorerPanel, {
    context: harness.ctx,
    instanceId: 'explorer:worlds',
    visible: value,
    video: harness.video,
  } as never);
  const view = render(element(visible));
  return { ...view, setVisible: (value: boolean) => view.rerender(element(value)) };
}

function sceneStatus(status: { phase: string; revision?: string; sourceTime?: number; error?: string; view?: unknown }) {
  expect(scene.onStatus).toBeTruthy();
  act(() => scene.onStatus!({ revision: 'rev', ...status }));
}

/** Acknowledges the frame in flight with the time and view it showed, as the scene does. The panel then sends the newest one. */
function ackLastFrame() {
  const last = scene.renders.at(-1)!;
  sceneStatus({ phase: 'ready', sourceTime: last.sourceTime, view: last.view });
}

/** The view the scene was last handed. */
function lastView() {
  const view = scene.renders.at(-1)?.view;
  if (!view) throw new Error('the last frame carried no view');
  return view;
}

/**
 * Makes the open world ready the way the scene does: it declares what it can do (free roam or not), then reports its frames.
 * Free roam reveals only on a frame that carries the view, so the first ready frame is followed by the panel's view frame.
 */
async function readyWorld(explore = true) {
  await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
  act(() => scene.onReady!({ events: [], cameras: [], explore: explore ? EXPLORE : null }));
  const first = scene.renders.at(-1)!;
  sceneStatus({ phase: 'ready', sourceTime: first.sourceTime });
  ackLastFrame();
}

/** Adds the sample from the empty state and waits until the scene surface has been handed the world. */
async function addSampleWorld(view: ReturnType<typeof mount>) {
  fireEvent.click(view.getByRole('button', { name: 'Add Lantern Valley' }));
  await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
}

/** Opens the full world list from the docked header and picks one of its rows. */
function pickWorld(view: ReturnType<typeof mount>, name: string) {
  fireEvent.click(view.getByRole('button', { name: 'Choose world' }));
  const worlds = view.getByRole('group', { name: 'Worlds' });
  fireEvent.click(within(worlds).getByRole('button', { name }));
}

describe('World Explorer panel', () => {
  it('shows the empty state, adds the sample into the project library and opens it', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    expect(view.getByText(/A world is a live 3D scene/)).toBeTruthy();
    expect(view.getByRole('button', { name: 'Import world…' })).toBeTruthy();
    expect(view.queryByRole('button', { name: 'Choose world' })).toBeNull();

    await addSampleWorld(view);

    await waitFor(() => expect(harness.settings.store.get('worldLibrary:p1')).toHaveLength(1));
    expect(harness.settings.store.has('worldLibrary:none')).toBe(false);
    expect(harness.settings.store.get('worldLibrary:p1')).toEqual([
      expect.objectContaining({
        name: 'Lantern Valley',
        duration: SAMPLE.duration,
        events: [{ name: 'Dawn', start: 0, end: 3 }, { name: 'Lanterns rise', start: 3, end: 5 }, { name: 'Lantern flare', start: 5.5 }],
        cameras: [{ name: 'Valley walk', start: 0, end: 3 }, { name: 'Lantern close-up', start: 3, end: 6, worldStart: 3 }],
      }),
    ]);
    expect(harness.toast).toHaveBeenCalledWith('Added Lantern Valley to the library', 'info');
    // The sample is opened straight away: the header names it, the empty state is gone.
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('Lantern Valley');
    expect(view.queryByRole('button', { name: 'Add Lantern Valley' })).toBeNull();
  });

  it('lists a world from the timeline under In this video, shows its whole stretch and a band for its use', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);
    // The first world in the video opens by itself.
    await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('Scene 1');

    fireEvent.click(view.getByRole('button', { name: 'Choose world' }));
    const worlds = view.getByRole('group', { name: 'Worlds' });
    const inVideo = within(worlds).getByRole('list', { name: 'In this video' });
    // The accessible name drops the space before the separator, so the match allows any spacing there.
    expect(within(inVideo).getByRole('button', { name: /^Scene 1 0:06\s*· 1 use$/ })).toBeTruthy();
    expect(within(worlds).queryByRole('list', { name: 'Library' })).toBeNull();
    expect(within(worlds).queryByRole('button', { name: /^Lantern/ })).toBeNull();

    fireEvent.click(within(inVideo).getByRole('button', { name: /^Scene 1 0:06\s*· 1 use$/ }));
    expect(view.queryByRole('group', { name: 'Worlds' })).toBeNull();

    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    expect(view.getByText(/Stretch 0:00\.0 – 0:06\.0 · 6\.0 s at 1×/)).toBeTruthy();
    expect(view.getByTitle('On V1 at 0:02')).toBeTruthy();
  });

  it('never queues more than one frame ahead of the scene and sends exactly one newer time per ack', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);
    await readyWorld();
    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    ackLastFrame();

    fireEvent.click(view.getByRole('button', { name: 'Play' }));
    const start = scene.renders.length;
    frames(6);
    const inFlight = [...new Set(scene.renders.slice(start).map((render) => render.sourceTime))];
    expect(inFlight).toHaveLength(1);
    const sent = inFlight[0];
    expect(sent).toBeGreaterThan(0);

    const beforeAck = scene.renders.length;
    sceneStatus({ phase: 'ready', sourceTime: sent });
    frames(6);
    const afterAck = [...new Set(scene.renders.slice(beforeAck).map((render) => render.sourceTime))];
    expect(afterAck).toHaveLength(1);
    expect(afterAck[0]).toBeGreaterThan(sent);
  });

  it('handles travel keys on the Camera travel group, and ignores keys from focused controls', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    await readyWorld();
    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    const travel = view.getByRole('group', { name: 'Camera travel' });

    expect(view.getByText('0:00.0 / 0:06')).toBeTruthy();
    fireEvent.keyDown(travel, { key: 'ArrowRight' });
    expect(view.getByText('0:01.0 / 0:06')).toBeTruthy();
    fireEvent.keyDown(travel, { key: 'ArrowRight', shiftKey: true });
    expect(view.getByText('0:06.0 / 0:06')).toBeTruthy();
    fireEvent.keyDown(travel, { key: 'ArrowLeft', shiftKey: true });
    expect(view.getByText('0:01.0 / 0:06')).toBeTruthy();

    fireEvent.keyDown(travel, { key: 'i' });
    expect(view.getByText(/Stretch 0:01\.0 – 0:06\.0 · 5\.0 s at 1×/)).toBeTruthy();
    fireEvent.keyDown(travel, { key: 'ArrowRight' });
    fireEvent.keyDown(travel, { key: 'ArrowRight' });
    fireEvent.keyDown(travel, { key: 'o' });
    expect(view.getByText(/Stretch 0:01\.0 – 0:03\.0 · 2\.0 s at 1×/)).toBeTruthy();

    // Space toggles play and pause.
    fireEvent.keyDown(travel, { key: ' ' });
    expect(view.getByRole('button', { name: 'Pause' })).toBeTruthy();
    fireEvent.keyDown(travel, { key: ' ' });
    expect(view.getByRole('button', { name: 'Play' })).toBeTruthy();

    // Keys from a focused button or select belong to that control.
    fireEvent.keyDown(view.getByRole('button', { name: 'Play' }), { key: ' ' });
    expect(view.getByRole('button', { name: 'Play' })).toBeTruthy();
    expect(view.queryByRole('button', { name: 'Pause' })).toBeNull();
    fireEvent.keyDown(view.getByRole('combobox', { name: 'Speed' }), { key: 'ArrowRight' });
    expect(view.getByText('0:03.0 / 0:06')).toBeTruthy();
  });

  it('moves the free camera with keys on the World viewer in Explore, and Space pauses the world', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    await readyWorld();
    const viewer = view.getByRole('application', { name: 'World viewer' });
    expect(view.getByRole('button', { name: 'Explore' })).toHaveAttribute('aria-pressed', 'true');

    const before = [...lastView().position];
    fireEvent.keyDown(viewer, { key: 'ArrowRight' });
    frames(5);
    fireEvent.keyUp(viewer, { key: 'ArrowRight' });
    expect(lastView().position).not.toEqual(before);

    // The world plays until Space pauses it.
    expect(view.getByRole('button', { name: 'Pause' })).toBeTruthy();
    fireEvent.keyDown(viewer, { key: ' ' });
    expect(view.getByRole('button', { name: 'Play' })).toBeTruthy();
  });

  it('opens a world that declares no free roam in Cameras, with Explore disabled and a note', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);
    await readyWorld(false);

    expect(view.getByRole('button', { name: 'Cameras' })).toHaveAttribute('aria-pressed', 'true');
    expect(view.getByRole('button', { name: 'Explore' })).toBeDisabled();
    expect(view.getByText(/This world isn't explorable yet/)).toBeTruthy();
    expect(view.getByRole('group', { name: 'Camera travel' })).toBeTruthy();
  });

  it('opens the last world viewed in this project, else the first in the video', () => {
    const lantern = { objectId: 'sha256:lantern', revision: 'sha256:lantern', name: 'Lantern Valley', duration: 6, authoredFps: 30, events: [], cameras: [] };
    const spare = { ...lantern, objectId: 'sha256:spare', revision: 'sha256:spare', name: 'Spare' };
    const settings = makeSettings(new Map<string, unknown>([
      ['worldLibrary:p1', [spare, lantern]],
      ['lastWorld:p1', `${lantern.objectId}@${lantern.revision}`],
    ]));
    const harness = makeHarness({ settings });
    const view = mount(harness);
    // Lantern Valley is the second library world, but it was the last one viewed, so it opens.
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('Lantern Valley');
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('2 / 2');
  });

  it('pauses playback when the panel is hidden', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    await readyWorld();
    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    fireEvent.click(view.getByRole('button', { name: 'Play' }));
    frames(2);
    expect(view.getByRole('button', { name: 'Pause' })).toBeTruthy();

    view.setVisible(false);
    expect(view.getByRole('button', { name: 'Play' })).toBeTruthy();
    expect(pending.size).toBe(0);
    const renders = scene.renders.length;
    frames(4);
    expect(scene.renders.length).toBe(renders);
  });

  it('adds the stretch at the playhead on a free track, then seeks there and reports success', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    await waitFor(() => expect(view.getByRole('button', { name: 'Add to video' })).toBeEnabled());
    harness.setPlayhead(4);

    fireEvent.click(view.getByRole('button', { name: 'Add to video' }));

    await waitFor(() => expect(harness.toast).toHaveBeenCalledWith('Added to V1 at 0:04', 'info'));
    expect(harness.timeline.apply).toHaveBeenCalledTimes(1);
    const patch = harness.timeline.apply.mock.calls[0][0] as { operations: unknown[] };
    expect(patch.operations).toEqual([
      { op: 'clip.add', target: 'world-1', payload: { track: 'V1', at: 4, clipType: LIVE_SCENE_CLIP_TYPE_ID }, order: 0 },
      {
        op: 'clip.update',
        target: 'world-1',
        // The stretch opens on the sample's first camera (Valley walk, 0-3), not the whole world.
        payload: { mode: 'merge', from: 0, to: 3, speed: 1, app: { liveScene: expect.any(Object) } },
        order: 1,
      },
    ]);
    expect(harness.seek).toHaveBeenCalledWith(4);
    expect(harness.seek).toHaveBeenCalledTimes(1);
  });

  it('reports a failed add with an error toast and an inline message, and does not seek', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    await waitFor(() => expect(view.getByRole('button', { name: 'Add to video' })).toBeEnabled());
    harness.timeline.apply.mockImplementationOnce(() => {
      throw new Error('Track locked');
    });

    fireEvent.click(view.getByRole('button', { name: 'Add to video' }));

    await waitFor(() => expect(harness.toast).toHaveBeenCalledWith('Add to video failed: Track locked', 'error'));
    expect(view.getByRole('status')).toHaveTextContent('Could not add to the video: Track locked');
    expect(harness.seek).not.toHaveBeenCalled();
    expect(harness.report).toHaveBeenCalledWith(expect.objectContaining({ severity: 'error', code: 'world-explorer/add-failed' }));
  });

  it('disables Add to video with the reason when the timeline has no project id', () => {
    const harness = makeHarness({ projectId: null, clips: [liveClip()] });
    const view = mount(harness);
    fireEvent.click(view.getByRole('button', { name: 'Cameras' }));
    const add = view.getByRole('button', { name: 'Add to video' });
    expect(add).toBeDisabled();
    expect(add).toHaveAttribute('title', 'Open a timeline to add worlds to a video.');
    expect(view.getByText('Open a timeline to add worlds to a video.')).toBeTruthy();
  });

  it('follows the single selected live-scene clip in Cameras, and updates it with a single clip.update', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);
    harness.selectClip(['c1']);

    await waitFor(() => expect(view.getByText(/Stretch 0:01\.0 – 0:04\.0 · 3\.0 s at 1×/)).toBeTruthy());
    expect(view.getByRole('button', { name: 'Cameras' })).toHaveAttribute('aria-pressed', 'true');
    expect(view.getByText(/Editing clip on V1 at 0:02/)).toBeTruthy();
    const update = view.getByRole('button', { name: 'Update clip' });
    expect(update).toBeDisabled();

    await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
    // The travel clock opens at the stretch start (1 s); two steps forward, then the end moves to 3.
    const travel = view.getByRole('group', { name: 'Camera travel' });
    fireEvent.keyDown(travel, { key: 'ArrowRight' });
    fireEvent.keyDown(travel, { key: 'ArrowRight' });
    fireEvent.keyDown(travel, { key: 'o' });
    expect(view.getByText(/Stretch 0:01\.0 – 0:03\.0 · 2\.0 s at 1×/)).toBeTruthy();
    expect(view.getByRole('button', { name: 'Update clip' })).toBeEnabled();

    fireEvent.click(view.getByRole('button', { name: 'Update clip' }));

    await waitFor(() => expect(harness.toast).toHaveBeenCalledWith('Clip updated', 'info'));
    expect(harness.timeline.apply).toHaveBeenCalledTimes(1);
    const patch = harness.timeline.apply.mock.calls[0][0] as { operations: unknown[] };
    expect(patch.operations).toEqual([
      { op: 'clip.update', target: 'c1', payload: { mode: 'merge', from: 1, to: 3, speed: 1 }, order: 0 },
    ]);
  });

  it('keeps each project library separate when two projects share one settings store', async () => {
    const shared = makeSettings();
    const first = makeHarness({ projectId: 'p1', settings: shared });
    const viewA = mount(first);
    await addSampleWorld(viewA);
    await waitFor(() => expect(shared.store.get('worldLibrary:p1')).toHaveLength(1));
    viewA.unmount();

    const second = makeHarness({ projectId: 'p2', settings: shared });
    const viewB = mount(second);
    expect(viewB.getByText(/A world is a live 3D scene/)).toBeTruthy();
    expect(viewB.queryByRole('button', { name: 'Choose world' })).toBeNull();
    expect(shared.store.get('worldLibrary:p2')).toBeUndefined();

    fireEvent.click(viewB.getByRole('button', { name: 'Add Lantern Valley' }));
    await waitFor(() => expect(shared.store.get('worldLibrary:p2')).toHaveLength(1));
    expect(shared.store.get('worldLibrary:p1')).toHaveLength(1);
  });

  it('cancels the animation frame loop on unmount, so no scene renders follow', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    await readyWorld();
    // Explore runs its world clock and free camera on every frame while the panel is visible.
    frames(2);
    expect(pending.size).toBe(1);

    view.unmount();
    expect(pending.size).toBe(0);
    const renders = scene.renders.length;
    frames(4);
    expect(scene.renders.length).toBe(renders);
  });

  it('saves the events and cameras a library scene reports, only when they differ, and shows them on the next visit', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    await waitFor(() => expect(harness.settings.store.get('worldLibrary:p1')).toHaveLength(1));
    const set = vi.spyOn(harness.settings, 'set');

    act(() => scene.onReady!({ events: SAMPLE_WORLD.events, cameras: SAMPLE_WORLD.cameras, explore: EXPLORE }));
    expect(set).not.toHaveBeenCalled();

    act(() => scene.onReady!({ events: [{ name: 'Bridge', start: 1 }], cameras: SAMPLE_WORLD.cameras, explore: EXPLORE }));
    expect(set).toHaveBeenCalledTimes(1);
    expect(harness.settings.store.get('worldLibrary:p1')).toEqual([
      expect.objectContaining({ events: [{ name: 'Bridge', start: 1 }], cameras: SAMPLE_WORLD.cameras }),
    ]);
    expect(view.getByRole('button', { name: 'Bridge 0:01' })).toBeTruthy();
    expect(view.queryByRole('button', { name: 'Dawn 0:00' })).toBeNull();

    act(() => scene.onReady!({ events: [{ name: 'Bridge', start: 1 }], cameras: SAMPLE_WORLD.cameras, explore: EXPLORE }));
    expect(set).toHaveBeenCalledTimes(1);

    view.unmount();
    // The library's last copy stands in until the scene reports again, and the default world is the one last viewed.
    const again = mount(harness);
    expect(again.getByRole('button', { name: 'Bridge 0:01' })).toBeTruthy();
    expect(again.queryByRole('button', { name: 'Dawn 0:00' })).toBeNull();
  });

  /** Two library worlds: the sample (real package) and a spare entry that has no package behind it. */
  async function seededLibrary() {
    const storage = makeStorage();
    const parsed = await parsePreparedScenePackage(new TextEncoder().encode(SAMPLE_WORLD.packageJson));
    const ingested = await ingestPreparedPackage(storage, parsed);
    const lantern = {
      objectId: ingested.package.object_id,
      revision: ingested.package.digest,
      name: 'Lantern Valley',
      duration: parsed.manifest.duration,
      authoredFps: parsed.manifest.authoredFps,
      events: [{ name: 'Dawn', start: 0 }],
      cameras: [],
    };
    const spare = { ...lantern, objectId: 'sha256:spare', revision: 'sha256:spare', name: 'Spare' };
    const settings = makeSettings(new Map<string, unknown>([['worldLibrary:p1', [lantern, spare]]]));
    return { storage, settings, lantern, spare };
  }

  it('removes a library world without changing the selected one', async () => {
    const { storage, settings, lantern } = await seededLibrary();
    const harness = makeHarness({ settings, storage });
    const view = mount(harness);
    // The first library world opens by itself.
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('Lantern Valley');

    fireEvent.click(view.getByRole('button', { name: 'Choose world' }));
    fireEvent.click(view.getByRole('button', { name: 'Remove Spare from library' }));

    expect(settings.store.get('worldLibrary:p1')).toEqual([lantern]);
    expect(view.queryByRole('button', { name: 'Remove Spare from library' })).toBeNull();
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('Lantern Valley');
    expect(view.queryByRole('button', { name: /^Spare/ })).toBeNull();
  });

  it('selects the next library world when the selected one is removed, then shows the empty state', async () => {
    const { storage, settings, lantern, spare } = await seededLibrary();
    const harness = makeHarness({ settings, storage });
    const view = mount(harness);

    fireEvent.click(view.getByRole('button', { name: 'Choose world' }));
    fireEvent.click(view.getByRole('button', { name: 'Remove Lantern Valley from library' }));

    expect(settings.store.get('worldLibrary:p1')).toEqual([spare]);
    expect(view.getByRole('button', { name: 'Choose world' })).toHaveTextContent('Spare');

    fireEvent.click(view.getByRole('button', { name: 'Choose world' }));
    fireEvent.click(view.getByRole('button', { name: 'Remove Spare from library' }));

    expect(settings.store.get('worldLibrary:p1')).toEqual([]);
    expect(view.getByText(/A world is a live 3D scene/)).toBeTruthy();
    expect(view.queryByRole('button', { name: 'Choose world' })).toBeNull();
    expect(storage.objects.has(lantern.objectId)).toBe(true);
  });
});
