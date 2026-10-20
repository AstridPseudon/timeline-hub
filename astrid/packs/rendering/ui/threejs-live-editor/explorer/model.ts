// Pure world-explorer model: worlds, uses, library, stretches, keys, travel clock.
import type { TimelineSnapshot, ExtensionSettingsService } from '@astrid/editor-sdk';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../identity';

/** Something that happens in the world, in world seconds; `end` is absent for a point event. */
export type WorldEvent = { readonly name: string; readonly start: number; readonly end?: number };
/** An authored camera: `start`/`end` in source seconds, `worldStart` the world time shown at `start` (default start). */
export type CameraMove = { readonly name: string; readonly start: number; readonly end: number; readonly worldStart?: number };
export type Stretch = { readonly from: number; readonly to: number; readonly speed: number };
export type WorldUse = { clipId: string; track: string; at: number; from: number; to: number; speed: number };
export type LibraryEntry = { objectId: string; revision: string; name: string; duration: number; authoredFps: number; events: WorldEvent[]; cameras: CameraMove[] };
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

function validEvent(v: unknown): v is WorldEvent {
  return isRecord(v) && typeof v.name === 'string' && typeof v.start === 'number' && Number.isFinite(v.start)
    && (v.end === undefined || (typeof v.end === 'number' && Number.isFinite(v.end)));
}

function validCamera(v: unknown): v is CameraMove {
  return isRecord(v) && typeof v.name === 'string'
    && typeof v.start === 'number' && Number.isFinite(v.start)
    && typeof v.end === 'number' && Number.isFinite(v.end) && v.end > v.start
    && (v.worldStart === undefined || (typeof v.worldStart === 'number' && Number.isFinite(v.worldStart)));
}

function validEntry(v: unknown): boolean {
  return isRecord(v)
    && typeof v.objectId === 'string'
    && typeof v.revision === 'string'
    && typeof v.name === 'string'
    && isPositive(v.duration)
    && isPositive(v.authoredFps);
}

/** Library for one project; invalid stored entries are dropped, and so are invalid events and cameras
 * (an entry saved with the old `stops` simply loses them). Never throws. */
export function readLibrary(settings: ExtensionSettingsService, projectId: string | null | undefined): LibraryEntry[] {
  let raw: unknown;
  try { raw = settings.get(libraryKey(projectId)); } catch { return []; }
  if (!Array.isArray(raw)) return [];
  return raw.filter(validEntry).map((entry): LibraryEntry => {
    const e = entry as Record<string, unknown>;
    return {
      objectId: e.objectId as string,
      revision: e.revision as string,
      name: e.name as string,
      duration: e.duration as number,
      authoredFps: e.authoredFps as number,
      events: Array.isArray(e.events) ? e.events.filter(validEvent) : [],
      cameras: Array.isArray(e.cameras) ? e.cameras.filter(validCamera) : [],
    };
  });
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

const sameJson = (a: unknown, b: unknown) => JSON.stringify(a) === JSON.stringify(b);

/** Keeps the events and cameras a library world's scene reported. Writes only when the entry exists and they differ; returns whether it wrote. */
export function saveInfo(
  settings: ExtensionSettingsService,
  projectId: string | null | undefined,
  key: string,
  info: { events: readonly WorldEvent[]; cameras: readonly CameraMove[] },
): boolean {
  const entry = readLibrary(settings, projectId).find((e) => worldKey(e) === key);
  if (!entry || (sameJson(entry.events, info.events) && sameJson(entry.cameras, info.cameras))) return false;
  addToLibrary(settings, projectId, { ...entry, events: [...info.events], cameras: [...info.cameras] });
  return true;
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
  private _start = 0;
  private _end: number;
  private _loop: boolean;
  private _speed = 1;
  private _time = 0;
  private _playing = false;
  private _lastTickMs: number | undefined;
  private _inFlight: number | undefined;
  private _shown: number | undefined;

  constructor(opts: { duration: number; loop?: boolean }) {
    this._duration = Math.max(0, opts.duration);
    this._end = this._duration;
    this._loop = opts.loop ?? false;
  }

  get time() { return this._time; }
  get playing() { return this._playing; }
  get speed() { return this._speed; }
  get inFlight() { return this._inFlight; }
  get shown() { return this._shown; }

  get windowStart() { return this._start; }
  get windowEnd() { return this._end; }

  setDuration(d: number) {
    this._duration = Math.max(0, d);
    this._start = Math.min(this._start, this._duration);
    this._end = Math.min(this._end, this._duration);
    this._time = Math.min(this._time, this._end);
  }

  /** Confines travel (seek, play, loop) to [start, end]; the time is pulled into it. */
  setWindow(start: number, end: number) {
    this._start = Math.min(Math.max(start, 0), this._duration);
    this._end = Math.min(Math.max(end, this._start), this._duration);
    this._time = Math.min(Math.max(this._time, this._start), this._end);
  }

  setLoop(b: boolean) { this._loop = b; }

  setSpeed(s: number) { this._speed = Number.isFinite(s) && s >= 0 ? s : 1; }

  play() {
    if (this._time >= this._end && !this._loop) this._time = this._start;
    this._playing = true;
    this._lastTickMs = undefined;
  }

  pause() {
    this._playing = false;
    this._lastTickMs = undefined;
  }

  seek(t: number) {
    this._time = Math.min(Math.max(t, this._start), this._end);
  }

  tick(nowMs: number) {
    if (!this._playing) return;
    if (this._lastTickMs === undefined) { this._lastTickMs = nowMs; return; }
    const gap = Math.min(Math.max(nowMs - this._lastTickMs, 0), MAX_TICK_GAP_MS);
    this._lastTickMs = nowMs;
    this._time += (gap / 1000) * this._speed;
    if (this._time >= this._end) {
      const length = this._end - this._start;
      if (this._loop) this._time = length > 0 ? this._start + ((this._time - this._start) % length) : this._start;
      else { this._time = this._end; this._playing = false; this._lastTickMs = undefined; }
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
    this._time = this._start;
    this._shown = undefined;
    this._inFlight = undefined;
    this.pause();
  }
}

// ---- Cameras: authored moves through the world, in source time.

export const WHOLE_WORLD_CAMERA = 'Whole world';

/** The world's cameras; a world that declares none gets one implicit camera covering all of it. */
export function camerasOrImplicit(cameras: readonly CameraMove[], duration: number): CameraMove[] {
  return cameras.length ? [...cameras] : [{ name: WHOLE_WORLD_CAMERA, start: 0, end: Math.max(duration, 0) }];
}

/** World time shown at a source time inside a camera: worldStart + (sourceTime - start). */
export const worldTimeIn = (camera: CameraMove, sourceTime: number) => (camera.worldStart ?? camera.start) + (sourceTime - camera.start);

/** Index of the camera whose source range holds `time` (end exclusive, the last one inclusive); else the nearest earlier one; else 0. */
export function cameraIndexAt(cameras: readonly CameraMove[], time: number): number {
  let found = -1;
  for (let i = 0; i < cameras.length; i++) {
    if (time >= cameras[i].start && (time < cameras[i].end || (i === cameras.length - 1 && time <= cameras[i].end))) return i;
    if (cameras[i].start <= time) found = i;
  }
  return Math.max(found, 0);
}

/** An event as seen from one camera: its overlap with the camera's world window, mapped to source time. */
export type CameraEvent = { readonly event: WorldEvent; readonly from: number; readonly to: number };

/** Events whose world time overlaps the camera's world-time window (touching counts for a point), clipped and mapped to source time. */
export function eventsInCamera(events: readonly WorldEvent[], camera: CameraMove): CameraEvent[] {
  const w0 = camera.worldStart ?? camera.start;
  const w1 = w0 + (camera.end - camera.start);
  const out: CameraEvent[] = [];
  for (const event of events) {
    const e0 = event.start;
    const e1 = event.end ?? event.start;
    if (e1 < w0 || e0 > w1) continue;
    out.push({ event, from: camera.start + (Math.max(e0, w0) - w0), to: camera.start + (Math.min(e1, w1) - w0) });
  }
  return out;
}

// ---- Free roam keys, view fitting, default world.

export type ExploreKey =
  | { type: 'move'; axis: 'forward' | 'right' | 'up'; sign: 1 | -1 }
  | { type: 'reset' }
  | { type: 'pause' };

/** The keys the free viewer handles. Modifier chords (Cmd/Ctrl/Alt) and Esc are never handled. */
export function exploreKey(e: { key: string; ctrlKey?: boolean; metaKey?: boolean; altKey?: boolean }): ExploreKey | undefined {
  if (e.ctrlKey || e.metaKey || e.altKey) return undefined;
  switch (e.key) {
    case 'w': case 'W': case 'ArrowUp': return { type: 'move', axis: 'forward', sign: 1 };
    case 's': case 'S': case 'ArrowDown': return { type: 'move', axis: 'forward', sign: -1 };
    case 'd': case 'D': case 'ArrowRight': return { type: 'move', axis: 'right', sign: 1 };
    case 'a': case 'A': case 'ArrowLeft': return { type: 'move', axis: 'right', sign: -1 };
    case 'e': case 'E': return { type: 'move', axis: 'up', sign: 1 };
    case 'q': case 'Q': return { type: 'move', axis: 'up', sign: -1 };
    case 'r': case 'R': return { type: 'reset' };
    case ' ': case 'Space': return { type: 'pause' };
    default: return undefined;
  }
}

export const SPEED_SCALE_MIN = 0.1;
export const SPEED_SCALE_MAX = 10;
export const SHIFT_BOOST = 3;

/** One wheel notch is a 25% change; deltaY > 0 (scroll down) slows down. */
export function wheelSpeedScale(scale: number, deltaY: number): number {
  if (!Number.isFinite(deltaY) || deltaY === 0) return scale;
  const next = scale * (deltaY < 0 ? 1.25 : 0.8);
  return Math.min(SPEED_SCALE_MAX, Math.max(SPEED_SCALE_MIN, Math.round(next * 100) / 100));
}

/** "1×", "1.25×", "0.5×". */
export const speedScaleLabel = (scale: number) => `${Number(scale.toFixed(2))}×`;

/** Largest `aspect` box that fits inside boxWidth x boxHeight, whole pixels. */
export function fitToBox(boxWidth: number, boxHeight: number, aspect: number): { width: number; height: number } {
  if (!(boxWidth > 0) || !(boxHeight > 0) || !(aspect > 0)) return { width: 0, height: 0 };
  const width = Math.floor(Math.min(boxWidth, boxHeight * aspect));
  return { width, height: Math.floor(width / aspect) };
}

/** The last world viewed in this project if it is still listed; else the first world in the video; else the first library world. */
export function chooseDefaultWorld<T extends { key: string }>(timeline: readonly T[], library: readonly T[], lastKey: string | undefined): T | undefined {
  return [...timeline, ...library].find((row) => row.key === lastKey) ?? timeline[0] ?? library[0];
}

export const lastWorldKey = (projectId: string | null | undefined) => `lastWorld:${projectId ? projectId : 'none'}`;
export const HINT_DISMISSED_KEY = 'exploreHintDismissed';
