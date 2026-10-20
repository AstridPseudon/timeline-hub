// Pure world-explorer model: worlds, uses, library, stretches, keys, travel clock.
import type { TimelineSnapshot, ExtensionSettingsService } from '@astrid/editor-sdk';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../identity';

export type Stop = { readonly time: number; readonly name: string };
export type Stretch = { readonly from: number; readonly to: number; readonly speed: number };
export type WorldUse = { clipId: string; track: string; at: number; from: number; to: number; speed: number };
export type LibraryEntry = { objectId: string; revision: string; name: string; duration: number; authoredFps: number; stops: Stop[] };
export type TimelineWorld = { objectId: string; revision: string; duration: number; authoredFps: number; uses: WorldUse[]; liveScene: Record<string, unknown> };

export const worldKey = (w: { objectId: string; revision: string }) => `${w.objectId}@${w.revision}`;

const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null && !Array.isArray(v);
const isPositive = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v) && v > 0;

/** Worlds placed on the timeline, grouped by objectId@revision, ordered by first use. */
export function worldsFromSnapshot(snapshot: TimelineSnapshot): TimelineWorld[] {
  const byKey = new Map<string, TimelineWorld>();
  const uses: { world: TimelineWorld; use: WorldUse }[] = [];
  for (const clip of snapshot.clips) {
    if (clip.clipType !== LIVE_SCENE_CLIP_TYPE_ID) continue;
    const ls = clip.app?.liveScene;
    if (!isRecord(ls) || !isRecord(ls.source)) continue;
    const { objectId, revision } = ls.source;
    if (typeof objectId !== 'string' || typeof revision !== 'string' || typeof ls.packageBody !== 'string') continue;
    const key = `${objectId}@${revision}`;
    let world = byKey.get(key);
    if (!world) {
      let body: unknown;
      try { body = JSON.parse(ls.packageBody); } catch { continue; }
      const manifest = isRecord(body) ? body.manifest : undefined;
      if (!isRecord(manifest) || !isPositive(manifest.duration) || !isPositive(manifest.authoredFps)) continue;
      world = { objectId, revision, duration: manifest.duration, authoredFps: manifest.authoredFps, uses: [], liveScene: ls };
      byKey.set(key, world);
    }
    const rate = clip.rate ?? 1;
    const from = clip.sourceOffset ?? 0;
    const to = clip.sourceEnd ?? from + clip.duration * rate;
    uses.push({ world, use: { clipId: clip.id, track: clip.track, at: clip.at, from, to, speed: rate } });
  }
  uses.sort((a, b) => a.use.at - b.use.at || (a.use.clipId < b.use.clipId ? -1 : a.use.clipId > b.use.clipId ? 1 : 0));
  const ordered: TimelineWorld[] = [];
  for (const { world, use } of uses) {
    if (world.uses.length === 0) ordered.push(world);
    world.uses.push(use);
  }
  return ordered;
}

export const libraryKey = (projectId: string | null | undefined) => `worldLibrary:${projectId ? projectId : 'none'}`;

function validStop(v: unknown): v is Stop {
  return isRecord(v) && typeof v.time === 'number' && Number.isFinite(v.time) && typeof v.name === 'string';
}

function validEntry(v: unknown): v is LibraryEntry {
  return isRecord(v)
    && typeof v.objectId === 'string'
    && typeof v.revision === 'string'
    && typeof v.name === 'string'
    && isPositive(v.duration)
    && isPositive(v.authoredFps)
    && Array.isArray(v.stops)
    && v.stops.every(validStop);
}

/** Library for one project; invalid stored entries are dropped. Never throws. */
export function readLibrary(settings: ExtensionSettingsService, projectId: string | null | undefined): LibraryEntry[] {
  let raw: unknown;
  try { raw = settings.get(libraryKey(projectId)); } catch { return []; }
  return Array.isArray(raw) ? raw.filter(validEntry) : [];
}

function writeLibrary(settings: ExtensionSettingsService, projectId: string | null | undefined, list: LibraryEntry[]): LibraryEntry[] {
  settings.set(libraryKey(projectId), list);
  return list;
}

/** Upserts by worldKey: replaces in place, or appends. */
export function addToLibrary(settings: ExtensionSettingsService, projectId: string | null | undefined, entry: LibraryEntry): LibraryEntry[] {
  const list = readLibrary(settings, projectId);
  const key = worldKey(entry);
  const i = list.findIndex((e) => worldKey(e) === key);
  if (i >= 0) list[i] = entry;
  else list.push(entry);
  return writeLibrary(settings, projectId, list);
}

export function removeFromLibrary(settings: ExtensionSettingsService, projectId: string | null | undefined, key: string): LibraryEntry[] {
  return writeLibrary(settings, projectId, readLibrary(settings, projectId).filter((e) => worldKey(e) !== key));
}

export const stretchDuration = (s: Stretch) => (s.to - s.from) / s.speed;

const MIN_STRETCH = 0.1;

/** Keeps from/to inside [0, duration] with at least MIN_STRETCH between them; bad speed becomes 1. */
export function clampStretch(s: Stretch, duration: number): Stretch {
  const speed = Number.isFinite(s.speed) && s.speed > 0 ? s.speed : 1;
  const from = Math.min(Math.max(s.from, 0), Math.max(0, duration - MIN_STRETCH));
  const to = Math.min(duration, Math.max(s.to, from + MIN_STRETCH));
  return { from, to, speed };
}

/** Moving the start never passes the end: it stops MIN_STRETCH short of it. */
export function setStretchStart(s: Stretch, t: number, duration: number): Stretch {
  return clampStretch({ ...s, from: Math.min(t, s.to - MIN_STRETCH) }, duration);
}

export function setStretchEnd(s: Stretch, t: number, duration: number): Stretch {
  return clampStretch({ ...s, to: Math.max(t, s.from + MIN_STRETCH) }, duration);
}

export type KeyAction =
  | { type: 'toggle' }
  | { type: 'seek'; time: number }
  | { type: 'setStart' }
  | { type: 'setEnd' };

export function keyAction(e: { key: string; shiftKey: boolean }, ctx: { time: number; duration: number }): KeyAction | undefined {
  switch (e.key) {
    case ' ':
    case 'Space':
      return { type: 'toggle' };
    case 'ArrowLeft':
    case 'ArrowRight': {
      const step = (e.shiftKey ? 5 : 1) * (e.key === 'ArrowLeft' ? -1 : 1);
      return { type: 'seek', time: Math.min(Math.max(ctx.time + step, 0), ctx.duration) };
    }
    case 'i':
    case 'I':
      return { type: 'setStart' };
    case 'o':
    case 'O':
      return { type: 'setEnd' };
    default:
      return undefined;
  }
}

/** First output visual track with no clip or shot overlapping [at, at+duration); else a new V-id. */
export function freeVisualTrack(snapshot: TimelineSnapshot, at: number, duration: number): { track: string; isNew: boolean } {
  const end = at + duration;
  const busy = (track: string) =>
    snapshot.clips.some((c) => c.track === track && c.at < end && c.at + c.duration > at)
    || (snapshot.shots ?? []).some((s) => s.track === track && s.at < end && s.at + s.duration > at);
  for (const t of snapshot.tracks) {
    if (t.kind === 'visual' && t.role !== 'source' && !busy(t.id)) return { track: t.id, isNew: false };
  }
  const ids = new Set(snapshot.tracks.map((t) => t.id));
  let n = 1;
  while (ids.has(`V${n}`)) n++;
  return { track: `V${n}`, isNew: true };
}

export function newClipId(snapshot: TimelineSnapshot, base = 'world'): string {
  const ids = new Set(snapshot.clips.map((c) => c.id));
  let n = 1;
  while (ids.has(`${base}-${n}`)) n++;
  return `${base}-${n}`;
}

const MAX_TICK_GAP_MS = 250;

/** Travel position for one world. next()/ack() give at most one render in flight. */
export class TravelClock {
  private _duration: number;
  private _loop: boolean;
  private _speed = 1;
  private _time = 0;
  private _playing = false;
  private _lastTickMs: number | undefined;
  private _inFlight: number | undefined;
  private _shown: number | undefined;

  constructor(opts: { duration: number; loop?: boolean }) {
    this._duration = Math.max(0, opts.duration);
    this._loop = opts.loop ?? false;
  }

  get time() { return this._time; }
  get playing() { return this._playing; }
  get speed() { return this._speed; }
  get inFlight() { return this._inFlight; }
  get shown() { return this._shown; }

  setDuration(d: number) {
    this._duration = Math.max(0, d);
    this._time = Math.min(this._time, this._duration);
  }

  setLoop(b: boolean) { this._loop = b; }

  setSpeed(s: number) { this._speed = Number.isFinite(s) && s >= 0 ? s : 1; }

  play() {
    if (this._time >= this._duration && !this._loop) this._time = 0;
    this._playing = true;
    this._lastTickMs = undefined;
  }

  pause() {
    this._playing = false;
    this._lastTickMs = undefined;
  }

  seek(t: number) {
    this._time = Math.min(Math.max(t, 0), this._duration);
  }

  tick(nowMs: number) {
    if (!this._playing) return;
    if (this._lastTickMs === undefined) { this._lastTickMs = nowMs; return; }
    const gap = Math.min(Math.max(nowMs - this._lastTickMs, 0), MAX_TICK_GAP_MS);
    this._lastTickMs = nowMs;
    this._time += (gap / 1000) * this._speed;
    if (this._time >= this._duration) {
      if (this._loop) this._time = this._duration > 0 ? this._time % this._duration : 0;
      else { this._time = this._duration; this._playing = false; this._lastTickMs = undefined; }
    }
  }

  next(): number | undefined {
    if (this._inFlight !== undefined) return undefined;
    if (this._shown === undefined || this._time !== this._shown) {
      this._inFlight = this._time;
      return this._time;
    }
    return undefined;
  }

  ack(sourceTime: number) {
    this._shown = sourceTime;
    this._inFlight = undefined;
  }

  fail() {
    this._inFlight = undefined;
    this.pause();
  }

  reset() {
    this._time = 0;
    this._shown = undefined;
    this._inFlight = undefined;
    this.pause();
  }
}
