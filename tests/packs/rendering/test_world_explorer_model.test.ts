import { describe, expect, it, vi } from 'vitest';
import type { ExtensionSettingsService, TimelineSnapshot } from '@astrid/editor-sdk';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../../../astrid/packs/rendering/ui/threejs-live-editor/identity';
import {
  TravelClock,
  addToLibrary,
  cameraIndexAt,
  camerasOrImplicit,
  chooseDefaultWorld,
  clampStretch,
  eventsInCamera,
  exploreKey,
  fitToBox,
  freeVisualTrack,
  keyAction,
  lastWorldKey,
  libraryKey,
  newClipId,
  readLibrary,
  removeFromLibrary,
  saveInfo,
  setStretchEnd,
  setStretchStart,
  speedScaleLabel,
  stretchDuration,
  wheelSpeedScale,
  worldKey,
  worldsFromSnapshot,
  worldTimeIn,
  type CameraMove,
  type LibraryEntry,
  type WorldEvent,
} from '../../../astrid/packs/rendering/ui/threejs-live-editor/explorer/model';

function packageBody(duration: number, authoredFps = 24) {
  return JSON.stringify({ formatVersion: 1, entry: { filename: 'index.html' }, manifest: { formatVersion: 1, entry: 'index.html', duration, authoredFps } });
}

function worldClip(id: string, track: string, at: number, world: { objectId: string; revision: string; duration?: number; body?: string }, extra: Record<string, unknown> = {}) {
  return {
    id, track, at, duration: 2, clipType: LIVE_SCENE_CLIP_TYPE_ID,
    app: { liveScene: { revision: world.revision, source: { objectId: world.objectId, revision: world.revision }, packageBody: world.body ?? packageBody(world.duration ?? 4), html: '<html></html>' } },
    ...extra,
  };
}

function snap(partial: Record<string, unknown>): TimelineSnapshot {
  return {
    projectId: 'p1', baseVersion: 1, currentVersion: 1, extensionRequirements: [], assetKeys: [], app: {},
    clips: [], tracks: [{ id: 'V1', kind: 'visual', label: 'V1', muted: false }], ...partial,
  } as unknown as TimelineSnapshot;
}

function fakeSettings(): ExtensionSettingsService & { map: Map<string, unknown> } {
  const map = new Map<string, unknown>();
  return {
    map,
    get: (k: string) => map.get(k) as never,
    set: (k: string, v: unknown) => { map.set(k, v); },
    delete: (k: string) => { map.delete(k); },
    keys: () => [...map.keys()],
    subscribe: () => ({ dispose: () => {} }) as never,
  } as ExtensionSettingsService & { map: Map<string, unknown> };
}

function entry(objectId: string, revision = 'r1', name = objectId): LibraryEntry {
  return { objectId, revision, name, duration: 4, authoredFps: 24, events: [{ name: 'hit', start: 1 }], cameras: [] };
}

describe('worldsFromSnapshot', () => {
  it('groups repeated uses of one world and maps from/to/speed', () => {
    const s = snap({
      clips: [
        worldClip('c2', 'V2', 5, { objectId: 'w', revision: 'a' }, { sourceOffset: 1, sourceEnd: 3, rate: 2 }),
        worldClip('c1', 'V1', 1, { objectId: 'w', revision: 'a' }),
      ],
    });
    const worlds = worldsFromSnapshot(s);
    expect(worlds).toHaveLength(1);
    expect(worldKey(worlds[0])).toBe('w@a');
    expect(worlds[0].duration).toBe(4);
    expect(worlds[0].authoredFps).toBe(24);
    expect(worlds[0].uses).toEqual([
      { clipId: 'c1', track: 'V1', at: 1, from: 0, to: 2, speed: 1 },
      { clipId: 'c2', track: 'V2', at: 5, from: 1, to: 3, speed: 2 },
    ]);
    expect(worlds[0].liveScene).toMatchObject({ revision: 'a' });
  });

  it('orders worlds by first use and separates different worlds', () => {
    const s = snap({
      clips: [
        worldClip('b', 'V1', 9, { objectId: 'B', revision: 'x' }),
        worldClip('a', 'V1', 2, { objectId: 'A', revision: 'x' }),
        worldClip('a2', 'V1', 12, { objectId: 'A', revision: 'x' }),
      ],
    });
    const worlds = worldsFromSnapshot(s);
    expect(worlds.map((w) => w.objectId)).toEqual(['A', 'B']);
    expect(worlds[0].uses.map((u) => u.clipId)).toEqual(['a', 'a2']);
  });

  it('separates same objectId at different revisions', () => {
    const s = snap({ clips: [worldClip('a', 'V1', 0, { objectId: 'A', revision: 'r1' }), worldClip('b', 'V1', 1, { objectId: 'A', revision: 'r2' })] });
    expect(worldsFromSnapshot(s).map(worldKey)).toEqual(['A@r1', 'A@r2']);
  });

  it('ignores non-live-scene clips and malformed live scene data', () => {
    const s = snap({
      clips: [
        { id: 'img', track: 'V1', at: 0, duration: 2, clipType: 'haus.astrid.image', app: {} },
        { id: 'noapp', track: 'V1', at: 0, duration: 2, clipType: LIVE_SCENE_CLIP_TYPE_ID },
        worldClip('badbody', 'V1', 0, { objectId: 'X', revision: 'r', body: '{not json' }),
        worldClip('nodur', 'V1', 0, { objectId: 'Y', revision: 'r', body: packageBody(0) }),
      ],
    });
    expect(worldsFromSnapshot(s)).toEqual([]);
  });
});

describe('library persistence', () => {
  it('keys by project and keeps projects isolated', () => {
    expect(libraryKey('p1')).toBe('worldLibrary:p1');
    expect(libraryKey(null)).toBe('worldLibrary:none');
    const settings = fakeSettings();
    addToLibrary(settings, 'p1', entry('A'));
    expect(readLibrary(settings, 'p2')).toEqual([]);
    expect(readLibrary(settings, 'p1').map((e) => e.objectId)).toEqual(['A']);
  });

  it('upserts by worldKey and removes', () => {
    const settings = fakeSettings();
    addToLibrary(settings, 'p1', entry('A', 'r1', 'first'));
    addToLibrary(settings, 'p1', entry('B'));
    const list = addToLibrary(settings, 'p1', entry('A', 'r1', 'renamed'));
    expect(list.map((e) => e.name)).toEqual(['renamed', 'B']);
    expect(addToLibrary(settings, 'p1', entry('A', 'r2')).map(worldKey)).toEqual(['A@r1', 'B@r1', 'A@r2']);
    expect(removeFromLibrary(settings, 'p1', 'A@r2').map(worldKey)).toEqual(['A@r1', 'B@r1']);
    expect(readLibrary(settings, 'p1').map(worldKey)).toEqual(['A@r1', 'B@r1']);
  });

  it('tolerates garbage and drops invalid entries', () => {
    const settings = fakeSettings();
    settings.set(libraryKey('p1'), 'nope');
    expect(readLibrary(settings, 'p1')).toEqual([]);
    settings.set(libraryKey('p1'), [entry('ok'), { objectId: 'bad' }, null, { ...entry('neg'), duration: -1 }]);
    expect(readLibrary(settings, 'p1').map((e) => e.objectId)).toEqual(['ok']);
    expect(readLibrary(settings, undefined).map((e) => e.objectId)).toEqual([]);
  });

  it('drops invalid events and cameras, keeping the valid ones', () => {
    const settings = fakeSettings();
    settings.set(libraryKey('p1'), [{
      ...entry('A'),
      events: [{ name: 'ok', start: 1 }, { name: 'span', start: 2, end: 3 }, { name: 'bad' }, { name: 'nan', start: 2, end: 'x' }],
      cameras: [{ name: 'cam', start: 0, end: 4 }, { name: 'backwards', start: 5, end: 2 }, { name: 'nan', start: 0, end: 1, worldStart: NaN }],
    }]);
    const [read] = readLibrary(settings, 'p1');
    expect(read.events).toEqual([{ name: 'ok', start: 1 }, { name: 'span', start: 2, end: 3 }]);
    expect(read.cameras).toEqual([{ name: 'cam', start: 0, end: 4 }]);
  });

  it('reads an entry saved with only the old stops field as having no events or cameras', () => {
    const settings = fakeSettings();
    settings.set(libraryKey('p1'), [{ objectId: 'A', revision: 'r1', name: 'A', duration: 4, authoredFps: 24, stops: [{ time: 1, name: 'hit' }] }]);
    expect(readLibrary(settings, 'p1')).toEqual([{ objectId: 'A', revision: 'r1', name: 'A', duration: 4, authoredFps: 24, events: [], cameras: [] }]);
  });
});

describe('saveInfo', () => {
  const hit: WorldEvent[] = [{ name: 'hit', start: 1 }];
  const bridge: WorldEvent[] = [{ name: 'Bridge', start: 2 }];
  const cam: CameraMove[] = [{ name: 'Wide', start: 0, end: 4 }];

  it('writes reported events and cameras only when they differ from the library entry', () => {
    const settings = fakeSettings();
    addToLibrary(settings, 'p1', entry('A'));
    const set = vi.spyOn(settings, 'set');

    expect(saveInfo(settings, 'p1', 'A@r1', { events: hit, cameras: [] })).toBe(false);
    expect(set).not.toHaveBeenCalled();

    expect(saveInfo(settings, 'p1', 'A@r1', { events: bridge, cameras: [] })).toBe(true);
    expect(set).toHaveBeenCalledTimes(1);
    expect(readLibrary(settings, 'p1')).toEqual([{ ...entry('A'), events: bridge, cameras: [] }]);

    expect(saveInfo(settings, 'p1', 'A@r1', { events: bridge, cameras: [] })).toBe(false);
    expect(set).toHaveBeenCalledTimes(1);

    expect(saveInfo(settings, 'p1', 'A@r1', { events: bridge, cameras: cam })).toBe(true);
    expect(set).toHaveBeenCalledTimes(2);
    expect(readLibrary(settings, 'p1')[0].cameras).toEqual(cam);

    expect(saveInfo(settings, 'p1', 'A@r1', { events: [], cameras: [] })).toBe(true);
    expect(readLibrary(settings, 'p1')[0]).toMatchObject({ events: [], cameras: [] });
  });

  it('ignores worlds that are not in this project library', () => {
    const settings = fakeSettings();
    addToLibrary(settings, 'p1', entry('A'));
    const set = vi.spyOn(settings, 'set');

    expect(saveInfo(settings, 'p1', 'B@r1', { events: bridge, cameras: [] })).toBe(false);
    expect(saveInfo(settings, 'p2', 'A@r1', { events: bridge, cameras: [] })).toBe(false);
    expect(set).not.toHaveBeenCalled();
    expect(readLibrary(settings, 'p1')[0].events).toEqual(hit);
  });
});

describe('stretch', () => {
  it('computes timeline duration from speed', () => {
    expect(stretchDuration({ from: 1, to: 5, speed: 2 })).toBe(2);
  });

  it('clamps to the world and keeps a minimum length', () => {
    expect(clampStretch({ from: -2, to: 99, speed: 1 }, 4)).toEqual({ from: 0, to: 4, speed: 1 });
    expect(clampStretch({ from: 3.99, to: 3.99, speed: 1 }, 4).to).toBeCloseTo(4);
    expect(clampStretch({ from: 3.95, to: 3.95, speed: 1 }, 4).from).toBeCloseTo(3.9);
    expect(clampStretch({ from: 0, to: 2, speed: 0 }, 4).speed).toBe(1);
    expect(clampStretch({ from: 0, to: 2, speed: NaN }, 4).speed).toBe(1);
  });

  it('moves start and end without crossing the other edge', () => {
    const s = { from: 1, to: 3, speed: 1 };
    expect(setStretchStart(s, 0.5, 4)).toEqual({ from: 0.5, to: 3, speed: 1 });
    expect(setStretchStart(s, 3.5, 4).from).toBeCloseTo(2.9);
    expect(setStretchEnd(s, 0.2, 4).to).toBeCloseTo(1.1);
    expect(setStretchEnd(s, 9, 4).to).toBe(4);
  });
});

describe('keyAction', () => {
  const ctx = { time: 10, duration: 20 };
  it('maps space to toggle', () => {
    expect(keyAction({ key: ' ', shiftKey: false }, ctx)).toEqual({ type: 'toggle' });
    expect(keyAction({ key: 'Space', shiftKey: false }, ctx)).toEqual({ type: 'toggle' });
  });
  it('seeks by 1s, or 5s with shift, clamped', () => {
    expect(keyAction({ key: 'ArrowLeft', shiftKey: false }, ctx)).toEqual({ type: 'seek', time: 9 });
    expect(keyAction({ key: 'ArrowRight', shiftKey: true }, ctx)).toEqual({ type: 'seek', time: 15 });
    expect(keyAction({ key: 'ArrowLeft', shiftKey: true }, { time: 2, duration: 20 })).toEqual({ type: 'seek', time: 0 });
    expect(keyAction({ key: 'ArrowRight', shiftKey: true }, { time: 18, duration: 20 })).toEqual({ type: 'seek', time: 20 });
  });
  it('maps i and o to stretch edges in either case', () => {
    expect(keyAction({ key: 'i', shiftKey: false }, ctx)).toEqual({ type: 'setStart' });
    expect(keyAction({ key: 'I', shiftKey: true }, ctx)).toEqual({ type: 'setStart' });
    expect(keyAction({ key: 'o', shiftKey: false }, ctx)).toEqual({ type: 'setEnd' });
    expect(keyAction({ key: 'O', shiftKey: false }, ctx)).toEqual({ type: 'setEnd' });
  });
  it('ignores other keys', () => {
    expect(keyAction({ key: 'x', shiftKey: false }, ctx)).toBeUndefined();
  });
});

describe('freeVisualTrack', () => {
  const clip = (id: string, track: string, at: number, duration: number) => ({ id, track, at, duration, clipType: 'x' });

  it('returns the first visual output track with no overlap', () => {
    const s = snap({
      tracks: [{ id: 'V1', kind: 'visual', label: '', muted: false }, { id: 'V2', kind: 'visual', label: '', muted: false }],
      clips: [clip('a', 'V1', 0, 5)],
    });
    expect(freeVisualTrack(s, 2, 1)).toEqual({ track: 'V2', isNew: false });
    expect(freeVisualTrack(s, 5, 1)).toEqual({ track: 'V1', isNew: false });
  });

  it('skips tracks blocked by shot placements', () => {
    const s = snap({
      tracks: [{ id: 'V1', kind: 'visual', label: '', muted: false }, { id: 'V2', kind: 'visual', label: '', muted: false }],
      shots: [{ id: 'sh', shotId: 'x', name: 'x', at: 0, duration: 3, track: 'V1', clips: [] }],
    });
    expect(freeVisualTrack(s, 1, 1).track).toBe('V2');
  });

  it('creates a new V id when every track is busy, avoiding existing ids', () => {
    const s = snap({
      tracks: [{ id: 'V1', kind: 'visual', label: '', muted: false }, { id: 'V2', kind: 'visual', label: '', muted: false }],
      clips: [clip('a', 'V1', 0, 5), clip('b', 'V2', 0, 5)],
    });
    expect(freeVisualTrack(s, 0, 1)).toEqual({ track: 'V3', isNew: true });
  });

  it('ignores source-role and audio tracks', () => {
    const s = snap({
      tracks: [
        { id: 'V1', kind: 'visual', label: '', muted: false, role: 'source' },
        { id: 'A1', kind: 'audio', label: '', muted: false },
      ],
    });
    expect(freeVisualTrack(s, 0, 1)).toEqual({ track: 'V2', isNew: true });
  });
});

describe('newClipId', () => {
  it('returns the smallest free n', () => {
    const s = snap({ clips: [{ id: 'world-1' }, { id: 'world-3' }] });
    expect(newClipId(s)).toBe('world-2');
    expect(newClipId(snap({}), 'dup')).toBe('dup-1');
  });
});

describe('TravelClock', () => {
  it('advances at speed while playing and records the first tick only', () => {
    const c = new TravelClock({ duration: 10 });
    c.setSpeed(2);
    c.play();
    c.tick(1000);
    expect(c.time).toBe(0);
    c.tick(1500);
    expect(c.time).toBeCloseTo(0.5); // 500ms gap clamped to 250ms, x2
    c.pause();
    c.tick(3000);
    expect(c.time).toBeCloseTo(0.5);
  });

  it('stops at the end without loop, and restarts on play', () => {
    const c = new TravelClock({ duration: 1 });
    c.play();
    c.tick(0);
    c.tick(200);
    c.tick(400);
    c.tick(600);
    c.tick(800);
    c.tick(1000);
    expect(c.time).toBeCloseTo(1);
    expect(c.playing).toBe(false);
    c.play();
    expect(c.time).toBe(0);
    expect(c.playing).toBe(true);
  });

  it('wraps when looping', () => {
    const c = new TravelClock({ duration: 1, loop: true });
    c.play();
    c.tick(0);
    c.tick(250);
    c.tick(500);
    c.tick(750);
    c.tick(1000);
    c.tick(1250);
    expect(c.playing).toBe(true);
    expect(c.time).toBeCloseTo(0.25);
  });

  it('clamps large gaps to 250ms', () => {
    const c = new TravelClock({ duration: 10 });
    c.play();
    c.tick(0);
    c.tick(60_000);
    expect(c.time).toBeCloseTo(0.25);
  });

  it('seeks clamp and keep the playing state', () => {
    const c = new TravelClock({ duration: 4 });
    c.seek(9);
    expect(c.time).toBe(4);
    c.seek(-1);
    expect(c.time).toBe(0);
    c.play();
    c.seek(2);
    expect(c.playing).toBe(true);
  });

  it('back-pressure: one render in flight, then newer time only', () => {
    const c = new TravelClock({ duration: 10 });
    expect(c.next()).toBe(0);
    expect(c.inFlight).toBe(0);
    expect(c.next()).toBeUndefined();
    c.ack(0);
    expect(c.shown).toBe(0);
    expect(c.inFlight).toBeUndefined();
    expect(c.next()).toBeUndefined();
    c.seek(2);
    expect(c.next()).toBe(2);
    c.seek(3);
    expect(c.next()).toBeUndefined();
    c.ack(2);
    expect(c.next()).toBe(3);
  });

  it('seek while in flight keeps the old render pending until ack', () => {
    const c = new TravelClock({ duration: 10 });
    c.seek(1);
    expect(c.next()).toBe(1);
    c.seek(5);
    expect(c.next()).toBeUndefined();
    expect(c.inFlight).toBe(1);
    c.ack(1);
    expect(c.next()).toBe(5);
  });

  it('fail clears the in-flight render and pauses', () => {
    const c = new TravelClock({ duration: 10 });
    c.play();
    c.tick(0);
    c.tick(100);
    expect(c.next()).toBeDefined();
    c.fail();
    expect(c.inFlight).toBeUndefined();
    expect(c.playing).toBe(false);
    expect(c.next()).toBeDefined();
  });

  it('reset returns to zero, unshown, paused', () => {
    const c = new TravelClock({ duration: 10 });
    c.seek(4);
    c.ack(c.next() as number);
    c.play();
    c.reset();
    expect([c.time, c.shown, c.inFlight, c.playing]).toEqual([0, undefined, undefined, false]);
  });
});

describe('TravelClock window', () => {
  it('starts as the whole world', () => {
    const c = new TravelClock({ duration: 6 });
    expect([c.windowStart, c.windowEnd]).toEqual([0, 6]);
  });

  it('pulls the time into the window and confines seek', () => {
    const c = new TravelClock({ duration: 10 });
    c.setWindow(2, 5);
    expect([c.windowStart, c.windowEnd, c.time]).toEqual([2, 5, 2]);
    c.seek(9);
    expect(c.time).toBe(5);
    c.seek(0);
    expect(c.time).toBe(2);
  });

  it('clamps the window to the world', () => {
    const c = new TravelClock({ duration: 4 });
    c.setWindow(-1, 9);
    expect([c.windowStart, c.windowEnd]).toEqual([0, 4]);
    c.setWindow(3, 1);
    expect([c.windowStart, c.windowEnd]).toEqual([3, 3]);
  });

  it('play from the window end restarts at the window start', () => {
    const c = new TravelClock({ duration: 10 });
    c.setWindow(2, 3);
    c.seek(3);
    c.play();
    expect(c.time).toBe(2);
    expect(c.playing).toBe(true);
  });

  it('stops at the window end without loop', () => {
    const c = new TravelClock({ duration: 10 });
    c.setWindow(2, 3);
    c.seek(2);
    c.play();
    c.tick(0);
    c.tick(250);
    c.tick(500);
    c.tick(750);
    c.tick(1000);
    expect(c.time).toBe(3);
    expect(c.playing).toBe(false);
  });

  it('wraps inside the window when looping', () => {
    const c = new TravelClock({ duration: 10, loop: true });
    c.setWindow(2, 3);
    c.seek(2.5);
    c.play();
    c.tick(0);
    c.tick(250);
    c.tick(500);
    expect(c.time).toBeCloseTo(2);
    c.tick(750);
    expect(c.time).toBeCloseTo(2.25);
    expect(c.playing).toBe(true);
  });

  it('reset returns to the window start', () => {
    const c = new TravelClock({ duration: 10 });
    c.setWindow(2, 5);
    c.seek(4);
    c.reset();
    expect(c.time).toBe(2);
  });

  it('shrinking the duration shrinks the window', () => {
    const c = new TravelClock({ duration: 10 });
    c.setWindow(2, 8);
    c.setDuration(5);
    expect([c.windowStart, c.windowEnd]).toEqual([2, 5]);
    c.setDuration(1);
    expect([c.windowStart, c.windowEnd]).toEqual([1, 1]);
  });
});

describe('camerasOrImplicit', () => {
  it('gives an empty world one implicit whole-world camera', () => {
    expect(camerasOrImplicit([], 4)).toEqual([{ name: 'Whole world', start: 0, end: 4 }]);
    expect(camerasOrImplicit([], -1)).toEqual([{ name: 'Whole world', start: 0, end: 0 }]);
  });

  it('returns a copy of declared cameras', () => {
    const cams: CameraMove[] = [{ name: 'A', start: 0, end: 2 }];
    const out = camerasOrImplicit(cams, 4);
    expect(out).toEqual(cams);
    expect(out).not.toBe(cams);
  });
});

describe('worldTimeIn', () => {
  it('defaults worldStart to start, so world time equals source time', () => {
    const cam: CameraMove = { name: 'a', start: 2, end: 6 };
    expect(worldTimeIn(cam, 2)).toBe(2);
    expect(worldTimeIn(cam, 5)).toBe(5);
  });

  it('offsets world time by worldStart', () => {
    const cam: CameraMove = { name: 'b', start: 2, end: 6, worldStart: 10 };
    expect(worldTimeIn(cam, 2)).toBe(10);
    expect(worldTimeIn(cam, 5)).toBe(13);
  });
});

describe('cameraIndexAt', () => {
  const cams: CameraMove[] = [{ name: 'a', start: 0, end: 4 }, { name: 'b', start: 4, end: 8 }];

  it('finds the camera holding a time', () => {
    expect(cameraIndexAt(cams, 2)).toBe(0);
    expect(cameraIndexAt(cams, 6)).toBe(1);
    expect(cameraIndexAt(cams, 0)).toBe(0);
  });

  it('gives a shared boundary to the later camera', () => {
    expect(cameraIndexAt(cams, 4)).toBe(1);
  });

  it('includes the end of the last camera', () => {
    expect(cameraIndexAt(cams, 8)).toBe(1);
  });

  it('before the first camera is index 0', () => {
    expect(cameraIndexAt([{ name: 'a', start: 2, end: 4 }], 1)).toBe(0);
  });

  it('in a gap, gives the earlier camera', () => {
    const gapped: CameraMove[] = [{ name: 'a', start: 0, end: 2 }, { name: 'b', start: 5, end: 8 }];
    expect(cameraIndexAt(gapped, 3.5)).toBe(0);
  });

  it('past the last camera, gives the last camera', () => {
    expect(cameraIndexAt(cams, 9)).toBe(1);
  });

  it('is 0 with no cameras', () => {
    expect(cameraIndexAt([], 3)).toBe(0);
  });
});

describe('eventsInCamera', () => {
  const span = (name: string, start: number, end: number): WorldEvent => ({ name, start, end });

  it('maps events on an aligned camera to source time, clipping spans to the window', () => {
    const cam: CameraMove = { name: 'c', start: 4, end: 8 };
    const events: WorldEvent[] = [
      span('inside', 5, 6),
      { name: 'point-mid', start: 6 },
      { name: 'point-start-edge', start: 4 },
      { name: 'point-end-edge', start: 8 },
      span('clip-left', 2, 6),
      span('clip-right', 7, 12),
      span('before', 0, 3),
      span('after', 9, 10),
    ];
    expect(eventsInCamera(events, cam)).toEqual([
      { event: events[0], from: 5, to: 6 },
      { event: events[1], from: 6, to: 6 },
      { event: events[2], from: 4, to: 4 },
      { event: events[3], from: 8, to: 8 },
      { event: events[4], from: 4, to: 6 },
      { event: events[5], from: 7, to: 8 },
    ]);
  });

  it('shows the same event from two cameras with different worldStart', () => {
    const event = span('shared', 3, 5);
    const a: CameraMove = { name: 'A', start: 0, end: 4 };
    const b: CameraMove = { name: 'B', start: 10, end: 14, worldStart: 2 };
    expect(eventsInCamera([event], a)).toEqual([{ event, from: 3, to: 4 }]);
    expect(eventsInCamera([event], b)).toEqual([{ event, from: 11, to: 13 }]);
  });

  it('drops events outside the camera window', () => {
    const cam: CameraMove = { name: 'B', start: 10, end: 14, worldStart: 2 };
    expect(eventsInCamera([span('gone', 0, 1), span('late', 7, 9)], cam)).toEqual([]);
  });

  it('returns nothing for no events', () => {
    expect(eventsInCamera([], { name: 'c', start: 0, end: 4 })).toEqual([]);
  });
});

describe('exploreKey', () => {
  const move = (axis: 'forward' | 'right' | 'up', sign: 1 | -1) => ({ type: 'move', axis, sign });

  it('maps w/a/s/d and arrows to forward and right with the right sign', () => {
    for (const key of ['w', 'W', 'ArrowUp']) expect(exploreKey({ key })).toEqual(move('forward', 1));
    for (const key of ['s', 'S', 'ArrowDown']) expect(exploreKey({ key })).toEqual(move('forward', -1));
    for (const key of ['d', 'D', 'ArrowRight']) expect(exploreKey({ key })).toEqual(move('right', 1));
    for (const key of ['a', 'A', 'ArrowLeft']) expect(exploreKey({ key })).toEqual(move('right', -1));
  });

  it('maps e/q to up', () => {
    expect(exploreKey({ key: 'e' })).toEqual(move('up', 1));
    expect(exploreKey({ key: 'E' })).toEqual(move('up', 1));
    expect(exploreKey({ key: 'q' })).toEqual(move('up', -1));
    expect(exploreKey({ key: 'Q' })).toEqual(move('up', -1));
  });

  it('maps r to reset and space to pause', () => {
    expect(exploreKey({ key: 'r' })).toEqual({ type: 'reset' });
    expect(exploreKey({ key: 'R' })).toEqual({ type: 'reset' });
    expect(exploreKey({ key: ' ' })).toEqual({ type: 'pause' });
    expect(exploreKey({ key: 'Space' })).toEqual({ type: 'pause' });
  });

  it('ignores modifier chords', () => {
    expect(exploreKey({ key: 'w', ctrlKey: true })).toBeUndefined();
    expect(exploreKey({ key: 'w', metaKey: true })).toBeUndefined();
    expect(exploreKey({ key: 'w', altKey: true })).toBeUndefined();
  });

  it('ignores Escape, Tab, Shift and unbound keys', () => {
    expect(exploreKey({ key: 'Escape' })).toBeUndefined();
    expect(exploreKey({ key: 'Tab' })).toBeUndefined();
    expect(exploreKey({ key: 'Shift' })).toBeUndefined();
    expect(exploreKey({ key: 'x' })).toBeUndefined();
  });
});

describe('wheelSpeedScale', () => {
  it('scrolling up speeds up by 25% a notch', () => {
    expect(wheelSpeedScale(1, -1)).toBe(1.25);
  });

  it('scrolling down slows down by 20% a notch', () => {
    expect(wheelSpeedScale(1, 1)).toBe(0.8);
  });

  it('clamps to [0.1, 10]', () => {
    expect(wheelSpeedScale(10, -1)).toBe(10);
    expect(wheelSpeedScale(0.1, 1)).toBe(0.1);
  });

  it('leaves the scale unchanged for zero or invalid deltas', () => {
    expect(wheelSpeedScale(1, 0)).toBe(1);
    expect(wheelSpeedScale(1, NaN)).toBe(1);
  });
});

describe('speedScaleLabel', () => {
  it('formats the scale with a multiplication sign', () => {
    expect(speedScaleLabel(1)).toBe('1×');
    expect(speedScaleLabel(1.25)).toBe('1.25×');
    expect(speedScaleLabel(0.5)).toBe('0.5×');
  });
});

describe('fitToBox', () => {
  it('is bounded by width when the box is tall', () => {
    expect(fitToBox(100, 300, 16 / 9)).toEqual({ width: 100, height: 56 });
  });

  it('is bounded by height when the box is wide', () => {
    expect(fitToBox(300, 100, 16 / 9)).toEqual({ width: 177, height: 99 });
  });

  it('returns whole pixels', () => {
    const { width, height } = fitToBox(333, 201, 4 / 3);
    expect(Number.isInteger(width)).toBe(true);
    expect(Number.isInteger(height)).toBe(true);
  });

  it('returns 0x0 for zero or invalid inputs', () => {
    expect(fitToBox(0, 100, 2)).toEqual({ width: 0, height: 0 });
    expect(fitToBox(100, -5, 2)).toEqual({ width: 0, height: 0 });
    expect(fitToBox(100, 100, 0)).toEqual({ width: 0, height: 0 });
    expect(fitToBox(NaN, 100, 1)).toEqual({ width: 0, height: 0 });
    expect(fitToBox(100, 100, NaN)).toEqual({ width: 0, height: 0 });
  });
});

describe('chooseDefaultWorld', () => {
  const timeline = [{ key: 'a' }, { key: 'b' }];
  const library = [{ key: 'c' }, { key: 'd' }];

  it('prefers the last viewed world while it is still listed', () => {
    expect(chooseDefaultWorld(timeline, library, 'b')?.key).toBe('b');
    expect(chooseDefaultWorld(timeline, library, 'd')?.key).toBe('d');
  });

  it('falls back to the first timeline world', () => {
    expect(chooseDefaultWorld(timeline, library, 'gone')?.key).toBe('a');
    expect(chooseDefaultWorld(timeline, library, undefined)?.key).toBe('a');
  });

  it('falls back to the first library world when the timeline is empty', () => {
    expect(chooseDefaultWorld([], library, undefined)?.key).toBe('c');
    expect(chooseDefaultWorld([], library, 'gone')?.key).toBe('c');
  });

  it('is undefined when there are no worlds', () => {
    expect(chooseDefaultWorld([], [], 'a')).toBeUndefined();
  });
});

describe('lastWorldKey', () => {
  it('is per project', () => {
    expect(lastWorldKey('p1')).toBe('lastWorld:p1');
    expect(lastWorldKey('p2')).not.toBe(lastWorldKey('p1'));
    expect(lastWorldKey(null)).toBe('lastWorld:none');
    expect(lastWorldKey(undefined)).toBe('lastWorld:none');
  });
});
