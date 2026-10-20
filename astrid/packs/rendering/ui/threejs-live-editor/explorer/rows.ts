// The one world list: worlds in the video, then library worlds.
import type { TimelineSnapshot } from '@astrid/editor-sdk';
import { worldKey, worldsFromSnapshot, type CameraMove, type LibraryEntry, type WorldEvent, type WorldUse } from './model';

/** One world the explorer can open: from the timeline, or from the project library. */
export type Row = {
  readonly key: string;
  readonly name: string;
  readonly duration: number;
  readonly objectId: string;
  readonly revision: string;
  readonly uses: readonly WorldUse[];
  readonly events: readonly WorldEvent[];
  readonly cameras: readonly CameraMove[];
  /** Present for timeline worlds, whose package already rides on their clips. */
  readonly liveScene?: Record<string, unknown>;
};

export function rowFromEntry(entry: LibraryEntry): Row {
  return {
    key: worldKey(entry),
    name: entry.name,
    duration: entry.duration,
    objectId: entry.objectId,
    revision: entry.revision,
    uses: [],
    events: entry.events,
    cameras: entry.cameras,
  };
}

/** Timeline worlds first (named from the library when saved, else "Scene N"), then library-only worlds. */
export function buildRows(snapshot: TimelineSnapshot | undefined, library: readonly LibraryEntry[]): { timeline: Row[]; library: Row[] } {
  const worlds = snapshot ? worldsFromSnapshot(snapshot) : [];
  const saved = new Map(library.map((entry) => [worldKey(entry), entry] as const));
  const onTimeline = new Set(worlds.map(worldKey));
  const timeline = worlds.map((world, index): Row => {
    const entry = saved.get(worldKey(world));
    return {
      key: worldKey(world),
      name: entry?.name ?? `Scene ${index + 1}`,
      duration: world.duration,
      objectId: world.objectId,
      revision: world.revision,
      uses: world.uses,
      events: entry?.events ?? [],
      cameras: entry?.cameras ?? [],
      liveScene: world.liveScene,
    };
  });
  return { timeline, library: library.filter((entry) => !onTimeline.has(worldKey(entry))).map(rowFromEntry) };
}
