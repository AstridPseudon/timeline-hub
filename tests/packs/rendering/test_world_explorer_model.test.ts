import { describe, expect, it } from 'vitest';
import type { ExtensionSettingsService, TimelineSnapshot } from '@astrid/editor-sdk';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../../../astrid/packs/rendering/ui/threejs-live-editor/identity';
import {
  TravelClock,
  addToLibrary,
  clampStretch,
  freeVisualTrack,
  keyAction,
  libraryKey,
  newClipId,
  readLibrary,
  removeFromLibrary,
  setStretchEnd,
  setStretchStart,
  stretchDuration,
  worldKey,
  worldsFromSnapshot,
  type LibraryEntry,
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
  return { objectId, revision, name, duration: 4, authoredFps: 24, stops: [{ time: 1, name: 'hit' }] };
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
    settings.set(libraryKey('p1'), [entry('ok'), { objectId: 'bad' }, null, { ...entry('neg'), duration: -1 }, { ...entry('stop'), stops: [{ time: 'x' }] }]);
    expect(readLibrary(settings, 'p1').map((e) => e.objectId)).toEqual(['ok']);
    expect(readLibrary(settings, undefined).map((e) => e.objectId)).toEqual([]);
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
