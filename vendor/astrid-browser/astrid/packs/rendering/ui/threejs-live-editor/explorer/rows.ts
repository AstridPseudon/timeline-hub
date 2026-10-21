// The one world list: worlds in the video, then library worlds.
import type { TimelineSnapshot } from '@astrid/editor-sdk';
import { PLACEHOLDER_LABEL, UNTITLED_WORLD, worldKey, worldsFromSnapshot, type ShotMove, type TimelineWorld, type LibraryEntry, type WorldEvent, type WorldUse } from './model';

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
  /** Set only when another row has the same name: which side this one is on, so the picker can tell them apart. */
  readonly qualifier?: 'in video' | 'library';
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
  const adopt = (name: string) => library.find((e) => e.name.toLowerCase() === name.toLowerCase())?.name ?? name;
  const label = world.nameHints.label && !PLACEHOLDER_LABEL.test(world.nameHints.label) ? adopt(world.nameHints.label) : undefined;
  const file = world.nameHints.file ? adopt(world.nameHints.file) : undefined;
  return label ?? world.nameHints.declared ?? sibling?.name ?? file
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
  const libraryRows = library.filter((entry) => !onTimeline.has(worldKey(entry))).map(rowFromEntry);
  const counts = new Map<string, number>();
  for (const row of [...timeline, ...libraryRows]) counts.set(row.name.toLowerCase(), (counts.get(row.name.toLowerCase()) ?? 0) + 1);
  const qualify = (row: Row, qualifier: 'in video' | 'library'): Row => ((counts.get(row.name.toLowerCase()) ?? 0) > 1 ? { ...row, qualifier } : row);
  return { timeline: timeline.map((row) => qualify(row, 'in video')), library: libraryRows.map((row) => qualify(row, 'library')) };
}
