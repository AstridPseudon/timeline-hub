// @vitest-environment jsdom
import { createElement } from 'react';
import { act, cleanup, fireEvent, render, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { WorldExplorerPanel } from '../../../astrid/packs/rendering/ui/threejs-live-editor/explorer/WorldExplorerPanel';
import { ingestPreparedPackage, parsePreparedScenePackage } from '../../../astrid/packs/rendering/ui/threejs-live-editor/authoring';
import { SAMPLE_WORLD } from '../../../astrid/packs/rendering/ui/threejs-live-editor/explorer/worlds/sample';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../../../astrid/packs/rendering/ui/threejs-live-editor/identity';

// Module-level handle on the scene surface: the mock records every render and keeps the latest callbacks.
const scene = vi.hoisted(() => ({
  renders: [] as Array<{ sourceTime: number }>,
  onStatus: null as null | ((status: unknown) => void),
  onReady: null as null | ((info: unknown) => void),
}));

vi.mock('../../../astrid/packs/rendering/ui/threejs-live-editor/SceneSurface', () => ({
  SceneSurface: (props: { sourceTime: number; onStatus: (status: unknown) => void; onReady: (info: unknown) => void }) => {
    scene.renders.push({ sourceTime: props.sourceTime });
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

function sceneStatus(status: { phase: string; revision?: string; sourceTime?: number; error?: string }) {
  expect(scene.onStatus).toBeTruthy();
  act(() => scene.onStatus!({ revision: 'rev', ...status }));
}

/** Adds the sample from the empty state and waits until the scene surface has been handed the world. */
async function addSampleWorld(view: ReturnType<typeof mount>) {
  fireEvent.click(view.getByRole('button', { name: 'Add Lantern Valley' }));
  await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
}

function pickOption(view: ReturnType<typeof mount>, name: string) {
  const option = view.getByRole('option', { name }) as HTMLOptionElement;
  fireEvent.change(view.getByRole('combobox', { name: 'World' }), { target: { value: option.value } });
}

describe('World Explorer panel', () => {
  it('shows the empty state, adds the sample into the project library and opens it', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    expect(view.getByText(/A world is a live 3D scene/)).toBeTruthy();
    expect(view.getByRole('button', { name: 'Import world…' })).toBeTruthy();
    expect(view.queryByRole('combobox', { name: 'World' })).toBeNull();

    await addSampleWorld(view);

    await waitFor(() => expect(harness.settings.store.get('worldLibrary:p1')).toHaveLength(1));
    expect(harness.settings.store.has('worldLibrary:none')).toBe(false);
    expect(harness.settings.store.get('worldLibrary:p1')).toEqual([
      expect.objectContaining({ name: 'Lantern Valley', duration: SAMPLE.duration, stops: [{ time: 0, name: 'Dawn' }, { time: 3, name: 'Lanterns' }] }),
    ]);
    expect(harness.toast).toHaveBeenCalledWith('Added Lantern Valley to the library', 'info');
    const [entry] = harness.settings.store.get('worldLibrary:p1') as Array<{ objectId: string; revision: string }>;
    expect(view.getByRole('combobox', { name: 'World' })).toHaveValue(`${entry.objectId}@${entry.revision}`);
    expect(view.queryByRole('button', { name: 'Add Lantern Valley' })).toBeNull();
  });

  it('lists a world from the timeline under In this video, shows its whole stretch and a band for its use', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);

    const group = view.container.querySelector('optgroup[label="In this video"]');
    expect(group).not.toBeNull();
    expect(view.getByRole('option', { name: 'Scene 1 · 0:06 · 1 use' })).toBeTruthy();
    expect(view.queryByRole('option', { name: /Lantern/ })).toBeNull();

    pickOption(view, 'Scene 1 · 0:06 · 1 use');

    await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
    expect(view.getByText(/Stretch 0:00\.0 – 0:06\.0 · 6\.0 s at 1×/)).toBeTruthy();
    expect(view.getByTitle('On V1 at 0:02')).toBeTruthy();
  });

  it('never queues more than one frame ahead of the scene and sends exactly one newer time per ack', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);
    pickOption(view, 'Scene 1 · 0:06 · 1 use');
    await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
    sceneStatus({ phase: 'ready', sourceTime: 0 });

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

  it('handles keys on the World viewer group, and ignores keys from focused controls', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    sceneStatus({ phase: 'ready', sourceTime: 0 });
    const group = view.getByRole('group', { name: 'World viewer' });

    expect(view.getByText('0:00.0 / 0:06')).toBeTruthy();
    fireEvent.keyDown(group, { key: 'ArrowRight' });
    expect(view.getByText('0:01.0 / 0:06')).toBeTruthy();
    fireEvent.keyDown(group, { key: 'ArrowRight', shiftKey: true });
    expect(view.getByText('0:06.0 / 0:06')).toBeTruthy();
    fireEvent.keyDown(group, { key: 'ArrowLeft', shiftKey: true });
    expect(view.getByText('0:01.0 / 0:06')).toBeTruthy();

    fireEvent.keyDown(group, { key: 'i' });
    expect(view.getByText(/Stretch 0:01\.0 – 0:06\.0 · 5\.0 s at 1×/)).toBeTruthy();
    fireEvent.keyDown(group, { key: 'ArrowRight' });
    fireEvent.keyDown(group, { key: 'ArrowRight' });
    fireEvent.keyDown(group, { key: 'o' });
    expect(view.getByText(/Stretch 0:01\.0 – 0:03\.0 · 2\.0 s at 1×/)).toBeTruthy();

    // Space toggles play and pause.
    fireEvent.keyDown(group, { key: ' ' });
    expect(view.getByRole('button', { name: 'Pause' })).toBeTruthy();
    fireEvent.keyDown(group, { key: ' ' });
    expect(view.getByRole('button', { name: 'Play' })).toBeTruthy();

    // Keys from a focused button or select belong to that control.
    fireEvent.keyDown(view.getByRole('button', { name: 'Play' }), { key: ' ' });
    expect(view.getByRole('button', { name: 'Play' })).toBeTruthy();
    expect(view.queryByRole('button', { name: 'Pause' })).toBeNull();
    fireEvent.keyDown(view.getByRole('combobox', { name: 'Speed' }), { key: 'ArrowRight' });
    expect(view.getByText('0:03.0 / 0:06')).toBeTruthy();
  });

  it('pauses playback when the panel is hidden', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    sceneStatus({ phase: 'ready', sourceTime: 0 });
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
        payload: { mode: 'merge', from: 0, to: SAMPLE.duration, speed: 1, app: { liveScene: expect.any(Object) } },
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
    pickOption(view, 'Scene 1 · 0:06 · 1 use');
    const add = view.getByRole('button', { name: 'Add to video' });
    expect(add).toBeDisabled();
    expect(add).toHaveAttribute('title', 'Open a timeline to add worlds to a video.');
    expect(view.getByText('Open a timeline to add worlds to a video.')).toBeTruthy();
  });

  it('follows the single selected live-scene clip, and updates it with a single clip.update', async () => {
    const harness = makeHarness({ clips: [liveClip()] });
    const view = mount(harness);
    harness.selectClip(['c1']);

    await waitFor(() => expect(view.getByText(/Stretch 0:01\.0 – 0:04\.0 · 3\.0 s at 1×/)).toBeTruthy());
    expect(view.getByText(/Editing clip on V1 at 0:02/)).toBeTruthy();
    const update = view.getByRole('button', { name: 'Update clip' });
    expect(update).toBeDisabled();

    await waitFor(() => expect(scene.renders.length).toBeGreaterThan(0));
    // The travel clock opens at the stretch start (1 s); two steps forward, then the end moves to 3.
    fireEvent.keyDown(view.getByRole('group', { name: 'World viewer' }), { key: 'ArrowRight' });
    fireEvent.keyDown(view.getByRole('group', { name: 'World viewer' }), { key: 'ArrowRight' });
    fireEvent.keyDown(view.getByRole('group', { name: 'World viewer' }), { key: 'o' });
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
    expect(viewB.queryByRole('combobox', { name: 'World' })).toBeNull();
    expect(shared.store.get('worldLibrary:p2')).toBeUndefined();

    fireEvent.click(viewB.getByRole('button', { name: 'Add Lantern Valley' }));
    await waitFor(() => expect(shared.store.get('worldLibrary:p2')).toHaveLength(1));
    expect(shared.store.get('worldLibrary:p1')).toHaveLength(1);
  });

  it('cancels the animation frame loop on unmount, so no scene renders follow', async () => {
    const harness = makeHarness();
    const view = mount(harness);
    await addSampleWorld(view);
    sceneStatus({ phase: 'ready', sourceTime: 0 });
    fireEvent.click(view.getByRole('button', { name: 'Play' }));
    frames(2);
    expect(pending.size).toBe(1);

    view.unmount();
    expect(pending.size).toBe(0);
    const renders = scene.renders.length;
    frames(4);
    expect(scene.renders.length).toBe(renders);
  });
});
