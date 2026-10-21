// The one world list: worlds in the video, then library worlds.
import type { TimelineSnapshot } from '@astrid/editor-sdk';
import { UNTITLED_WORLD, worldKey, worldsFromSnapshot, type ShotMove, type TimelineWorld, type LibraryEntry, type WorldEvent, type WorldUse } from './model';

/** One world the explorer can open: from the timeline, or from the project library. */
export type Row = {
  readonly key: string;
  readonly name: string;
  readonly duration: number;
  readonly authoredFps: number;
  readonly objectId: string;
  readonly revision: string;
  readonly uses: readonly WorldUse[];
  readonly events: readonly WorldEvent[];
  readonly shots: readonly ShotMove[];
  /** Present for timeline worlds, whose package already rides on their clips. */
  readonly liveScene?: Record<string, unknown>;
};

export function rowFromEntry(entry: LibraryEntry): Row {
  return {
    key: worldKey(entry),
    name: entry.name,
    duration: entry.duration,
    authoredFps: entry.authoredFps,
    objectId: entry.objectId,
    revision: entry.revision,
    uses: [],
    events: entry.events,
    shots: entry.shots,
  };
}

/** A timeline world's name: its saved name, else the clip's label, a name the package declares, a library world with the same
 * object or revision, a title from its entry file; "Untitled world" only when none exists. */
export function timelineWorldName(world: TimelineWorld, entry: LibraryEntry | undefined, library: readonly LibraryEntry[], index = 0): string {
  if (entry && !UNTITLED_WORLD.test(entry.name)) return entry.name;
  const sibling = library.find((e) => (e.objectId === world.objectId || e.revision === world.revision) && !UNTITLED_WORLD.test(e.name));
  return world.nameHints.label ?? world.nameHints.declared ?? sibling?.name ?? world.nameHints.file
    ?? entry?.name ?? (index === 0 ? 'Untitled world' : `Untitled world ${index + 1}`);
}

/** Timeline worlds first (named from the library when saved, else "Untitled world"), then library-only worlds. */
export function buildRows(snapshot: TimelineSnapshot | undefined, library: readonly LibraryEntry[]): { timeline: Row[]; library: Row[] } {
  const worlds = snapshot ? worldsFromSnapshot(snapshot) : [];
  const saved = new Map(library.map((entry) => [worldKey(entry), entry] as const));
  const onTimeline = new Set(worlds.map(worldKey));
  const timeline = worlds.map((world, index): Row => {
    const entry = saved.get(worldKey(world));
    return {
      key: worldKey(world),
      name: timelineWorldName(world, entry, library, index),
      duration: world.duration,
      authoredFps: world.authoredFps,
      objectId: world.objectId,
      revision: world.revision,
      uses: world.uses,
      events: entry?.events ?? [],
      shots: entry?.shots ?? [],
      liveScene: world.liveScene,
    };
  });
  return { timeline, library: library.filter((entry) => !onTimeline.has(worldKey(entry))).map(rowFromEntry) };
}
