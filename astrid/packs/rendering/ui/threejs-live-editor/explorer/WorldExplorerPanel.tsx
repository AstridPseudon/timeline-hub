import { lazy, Suspense, useEffect, useMemo, useRef, useState, type ChangeEvent, type KeyboardEvent, type PointerEvent } from 'react';
import type { ExtensionContext, PanelRenderProps, TimelineSnapshot } from '@astrid/editor-sdk';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../identity';
import type { SceneStatus } from '../runtime';
import {
  addToLibrary,
  clampStretch,
  freeVisualTrack,
  keyAction,
  newClipId,
  readLibrary,
  removeFromLibrary,
  saveStops,
  setStretchEnd,
  setStretchStart,
  stretchDuration,
  TravelClock,
  worldKey,
  worldsFromSnapshot,
  type LibraryEntry,
  type Stop,
  type Stretch,
  type WorldUse,
} from './model';

type AuthoringModule = typeof import('../authoring');
const loadAuthoring = (): Promise<AuthoringModule> => import('../authoring');

const LazySceneSurface = lazy(() =>
  import('../SceneSurface').then(({ SceneSurface }) => ({ default: SceneSurface })),
);

/** Matches the name the sample module ships under; shown before the sample is opened. */
const SAMPLE_LABEL = 'Lantern Valley';
const SPEEDS = [0.5, 1, 2];
const MIN_VIEW_WIDTH = 160;
const FALLBACK_VIEW_WIDTH = 320;
const FALLBACK_ASPECT = 16 / 9;

// Same control chrome as the Transcript panel; pack TSX sits outside the app's Tailwind scan.
const button = 'min-h-10 sm:min-h-8 rounded-md px-2 text-xs hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50';
const select = 'min-h-10 sm:min-h-8 min-w-0 max-w-full rounded-md border border-border/70 bg-background px-2 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring';
const VIEWER_STYLE = { background: '#05060f' } as const;
const OVERLAY_STYLE = { background: 'rgba(5, 6, 15, 0.92)', color: 'rgba(255, 255, 255, 0.72)' } as const;
const ERROR_STYLE = { color: 'hsl(var(--destructive))' } as const;

/** m:ss, or m:ss.s with one decimal. Rounds on the displayed unit so 59.96 never reads 0:60.0. */
function clockText(seconds: number, decimals = 0): string {
  const unit = decimals ? 10 : 1;
  const ticks = Math.max(0, Math.round((Number.isFinite(seconds) ? seconds : 0) * unit));
  const minutes = Math.floor(ticks / (60 * unit));
  const rest = ticks - minutes * 60 * unit;
  const whole = String(Math.floor(rest / unit)).padStart(2, '0');
  return `${minutes}:${whole}${decimals ? `.${rest % unit}` : ''}`;
}

const speedLabel = (speed: number) => `${speed}×`;
const percent = (time: number, duration: number) => `${duration > 0 ? Math.min(Math.max(time / duration, 0), 1) * 100 : 0}%`;
const errorMessage = (cause: unknown) => (cause instanceof Error ? cause.message : String(cause));

function aspectOf(resolution: string | undefined): number {
  const match = /^(\d+)x(\d+)$/.exec(resolution ?? '');
  if (!match) return FALLBACK_ASPECT;
  const width = Number(match[1]);
  const height = Number(match[2]);
  return width > 0 && height > 0 ? width / height : FALLBACK_ASPECT;
}

function readSnapshot(ctx: ExtensionContext): TimelineSnapshot | undefined {
  try {
    return ctx.creative.reader.snapshot();
  } catch {
    return undefined;
  }
}

function reportError(ctx: ExtensionContext, code: string, message: string) {
  try {
    ctx.services.diagnostics.report({ severity: 'error', code, message });
  } catch {
    // Diagnostics are best effort; the inline message already tells the user.
  }
}

/** One world the explorer can open: from the timeline, or from the project library. */
type Row = {
  readonly key: string;
  readonly name: string;
  readonly duration: number;
  readonly objectId: string;
  readonly revision: string;
  readonly uses: readonly WorldUse[];
  readonly stops: readonly Stop[];
  /** Present for timeline worlds, whose package already rides on their clips. */
  readonly liveScene?: Record<string, unknown>;
};

function rowFromEntry(entry: LibraryEntry): Row {
  return {
    key: worldKey(entry),
    name: entry.name,
    duration: entry.duration,
    objectId: entry.objectId,
    revision: entry.revision,
    uses: [],
    stops: entry.stops,
  };
}

/** Timeline worlds first (named from the library when saved, else "Scene N"), then library-only worlds. */
function buildRows(snapshot: TimelineSnapshot | undefined, library: readonly LibraryEntry[]): { timeline: Row[]; library: Row[] } {
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
      stops: entry?.stops ?? [],
      liveScene: world.liveScene,
    };
  });
  return { timeline, library: library.filter((entry) => !onTimeline.has(worldKey(entry))).map(rowFromEntry) };
}

export function WorldExplorerPanel(props: PanelRenderProps & { context: ExtensionContext }) {
  const { context: ctx, video, visible } = props;
  const storage = ctx.creative.projectObjects;

  const [snap, setSnap] = useState<TimelineSnapshot | undefined>(() => readSnapshot(ctx));
  const projectId = snap?.projectId ?? null;
  const [library, setLibrary] = useState<LibraryEntry[]>([]);
  const [selected, setSelected] = useState<Row | null>(null);
  const [loaded, setLoaded] = useState<{ key: string; liveScene: Record<string, unknown> } | null>(null);
  const [loadError, setLoadError] = useState<{ key: string; message: string } | null>(null);
  const [sceneReady, setSceneReady] = useState(false);
  const [sceneError, setSceneError] = useState<string | null>(null);
  const [reported, setReported] = useState<{ key: string; stops: Stop[] } | null>(null);
  const [stretch, setStretch] = useState<Stretch>({ from: 0, to: 1, speed: 1 });
  const [loop, setLoop] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [shownTime, setShownTime] = useState(0);
  const [renderTime, setRenderTime] = useState(0);
  const [followedClipId, setFollowedClipId] = useState<string | null>(null);
  const [liveClipId, setLiveClipId] = useState<string | null>(null);
  const [viewWidth, setViewWidth] = useState(FALLBACK_VIEW_WIDTH);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<{ tone: 'error' | 'info'; text: string } | null>(null);

  const clockRef = useRef<TravelClock | null>(null);
  // Frames are back-pressured: at most one render in flight, and only after the scene reported ready.
  const readyRef = useRef(false);
  const sentRef = useRef(0);
  const openRequest = useRef(0);
  const mounted = useRef(false);
  const viewerRef = useRef<HTMLDivElement>(null);
  const barRef = useRef<HTMLDivElement>(null);
  const importInput = useRef<HTMLInputElement>(null);
  const scrubbing = useRef(false);
  const seenClipRef = useRef<string | null | undefined>(undefined);
  const liveClipRef = useRef<string | null>(null);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      clockRef.current = null;
    };
  }, []);

  const settings = ctx.services.settings;
  // The library is per project; read it again when the project changes.
  useEffect(() => {
    setLibrary(readLibrary(ctx.services.settings, projectId));
  }, [projectId]);

  // Observe only while visible. The reader drives the worlds list; the view store only moves the follow state.
  useEffect(() => {
    if (!visible) return;
    const refresh = () => {
      if (mounted.current) setSnap(readSnapshot(ctx));
    };
    const sync = () => {
      let ids: ReadonlySet<string> | undefined;
      try {
        ids = video?.view.getSnapshot().selection.selectedClipIds;
      } catch {
        ids = undefined;
      }
      const id = ids && ids.size === 1 ? [...ids][0] : null;
      // Only a change of the selected clip re-renders; playhead ticks are read lazily.
      if (id === seenClipRef.current) return;
      seenClipRef.current = id;
      let next: string | null = null;
      if (id) {
        const clip = readSnapshot(ctx)?.clips.find((candidate) => candidate.id === id);
        if (clip?.clipType === LIVE_SCENE_CLIP_TYPE_ID) next = id;
      }
      refresh();
      if (next !== liveClipRef.current) {
        liveClipRef.current = next;
        setLiveClipId(next);
      }
    };
    refresh();
    sync();
    const unsubscribe = ctx.creative.reader.subscribe?.(refresh);
    let viewSubscription: { dispose(): void } | undefined;
    try {
      viewSubscription = video?.view.subscribe(sync);
    } catch {
      viewSubscription = undefined;
    }
    return () => {
      unsubscribe?.();
      viewSubscription?.dispose();
    };
  }, [visible, ctx, video]);

  // Stop travelling when the panel is hidden.
  useEffect(() => {
    if (visible) return;
    clockRef.current?.pause();
    setPlaying(false);
  }, [visible]);

  const rows = useMemo(() => buildRows(snap, library), [snap, library]);
  const allRows = [...rows.timeline, ...rows.library];
  const duration = selected?.duration ?? 0;
  const aspect = aspectOf(snap?.outputMetadata?.resolution);
  const viewHeight = Math.round(viewWidth / aspect);
  const liveScene = loaded && selected && loaded.key === selected.key ? loaded.liveScene : undefined;
  const ready = Boolean(liveScene) && sceneReady && !sceneError;
  // A scene's reported stops win, even when empty: they are what the library keeps for it.
  const stops = selected
    ? (reported?.key === selected.key ? reported.stops : selected.stops)
    : [];
  const sampleSaved = library.some((entry) => entry.name === SAMPLE_LABEL);
  const projectReady = Boolean(snap?.projectId && snap?.timelineId);
  const followedUse = followedClipId ? rows.timeline.flatMap((row) => row.uses).find((use) => use.clipId === followedClipId) : undefined;
  const followedDiffers = Boolean(followedUse)
    && (followedUse!.from !== stretch.from || followedUse!.to !== stretch.to || followedUse!.speed !== stretch.speed);
  const stretchValid = stretch.to > stretch.from && stretch.speed > 0;
  const addReason = !selected ? 'Choose a world to add.'
    : !projectReady ? 'Open a timeline to add worlds to a video.'
    : !storage ? 'Project storage is unavailable.'
    : !liveScene ? 'Opening world…'
    : busy ? 'Working…'
    : !stretchValid ? 'The stretch is empty.'
    : null;
  const speedOptions = [...new Set([...SPEEDS, stretch.speed])].sort((a, b) => a - b);

  // Measure the viewer so the scene renders at panel width; jsdom and hidden hosts keep the fallback.
  useEffect(() => {
    const element = viewerRef.current;
    if (!element) return;
    const measure = () => {
      const width = Math.floor(element.clientWidth);
      if (width > 0) setViewWidth(Math.max(MIN_VIEW_WIDTH, width));
    };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  // Playback loop: only while visible and playing. Each frame advances the clock and offers the next frame.
  useEffect(() => {
    if (!visible || !playing) return;
    let frame = 0;
    const step = () => {
      const clock = clockRef.current;
      if (!clock) return;
      clock.tick(performance.now());
      setShownTime(clock.time);
      if (!clock.playing) {
        setPlaying(false);
        return;
      }
      pump();
      frame = requestAnimationFrame(step);
    };
    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [visible, playing]);

  // Follow the single selected live-scene clip: open its world with its stretch.
  useEffect(() => {
    if (!liveClipId) return;
    const snapshot = readSnapshot(ctx);
    if (!snapshot) return;
    const world = worldsFromSnapshot(snapshot).find((candidate) => candidate.uses.some((use) => use.clipId === liveClipId));
    const use = world?.uses.find((candidate) => candidate.clipId === liveClipId);
    const row = world ? buildRows(snapshot, readLibrary(settings, snapshot.projectId)).timeline.find((candidate) => candidate.key === worldKey(world)) : undefined;
    if (!row || !use) return;
    openWorld(row, { stretch: { from: use.from, to: use.to, speed: use.speed }, clipId: liveClipId });
  }, [liveClipId]);

  /** Sends the latest clock time to the scene, at most one frame in flight. Reads refs only. */
  function pump() {
    const clock = clockRef.current;
    if (!clock || !readyRef.current) return;
    const time = clock.next();
    if (time === undefined) return;
    if (time === sentRef.current) {
      clock.ack(time);
      return;
    }
    sentRef.current = time;
    setRenderTime(time);
  }

  function seekTo(time: number) {
    const clock = clockRef.current;
    if (!clock) return;
    clock.seek(time);
    setShownTime(clock.time);
    pump();
  }

  function togglePlay() {
    const clock = clockRef.current;
    if (!clock || !readyRef.current) return;
    if (clock.playing) {
      clock.pause();
      setPlaying(false);
    } else {
      clock.play();
      setPlaying(true);
    }
  }

  function openWorld(row: Row, options: { stretch?: Stretch; clipId?: string | null } = {}) {
    const token = ++openRequest.current;
    const next = clampStretch(options.stretch ?? { from: 0, to: row.duration, speed: 1 }, row.duration);
    const clock = new TravelClock({ duration: row.duration, loop });
    clock.setSpeed(next.speed);
    // A followed clip opens at the start of its stretch.
    const start = options.stretch ? next.from : 0;
    clock.seek(start);
    clockRef.current = clock;
    readyRef.current = false;
    sentRef.current = start;
    setSelected(row);
    setFollowedClipId(options.clipId ?? null);
    setStretch(next);
    setLoaded(null);
    setLoadError(null);
    setSceneReady(false);
    setSceneError(null);
    setReported(null);
    setRenderTime(start);
    setShownTime(start);
    setPlaying(false);
    setNotice(null);
    if (row.liveScene) {
      setLoaded({ key: row.key, liveScene: row.liveScene });
      return;
    }
    if (!storage) {
      setLoadError({ key: row.key, message: 'Project storage is unavailable, so this world cannot be opened.' });
      return;
    }
    loadAuthoring()
      .then(({ loadLiveSceneSource }) => loadLiveSceneSource(storage, row.objectId, row.revision))
      .then(({ liveScene: source }) => {
        if (!mounted.current || token !== openRequest.current) return;
        setLoaded({ key: row.key, liveScene: source });
      }, (cause: unknown) => {
        if (!mounted.current || token !== openRequest.current) return;
        const message = errorMessage(cause);
        setLoadError({ key: row.key, message });
        reportError(ctx, 'world-explorer/open-failed', `Could not open world: ${message}`);
      });
  }

  function handleStatus(status: SceneStatus) {
    const clock = clockRef.current;
    if (status.phase === 'ready') {
      readyRef.current = true;
      setSceneReady(true);
      setSceneError(null);
      clock?.ack(status.sourceTime ?? clock.time);
      pump();
    } else if (status.phase === 'error') {
      readyRef.current = false;
      setSceneError(status.error ?? 'The scene could not start.');
      clock?.fail();
      setPlaying(false);
    }
  }

  function handleReady(info: { stops: ReadonlyArray<{ time: number; name: string }> }) {
    if (!selected) return;
    const reportedStops = info.stops.map((stop) => ({ time: stop.time, name: stop.name }));
    setReported({ key: selected.key, stops: reportedStops });
    // A library world keeps its reported stops, so the next visit shows them before the scene loads.
    if (saveStops(settings, projectId, selected.key, reportedStops)) setLibrary(readLibrary(settings, projectId));
  }

  function pick(key: string) {
    const row = allRows.find((candidate) => candidate.key === key);
    if (row) openWorld(row);
  }

  /** Clears the viewer when no world is left to show. */
  function clearWorld() {
    openRequest.current++;
    clockRef.current = null;
    readyRef.current = false;
    setSelected(null);
    setFollowedClipId(null);
    setLoaded(null);
    setLoadError(null);
    setSceneReady(false);
    setSceneError(null);
    setReported(null);
    setRenderTime(0);
    setShownTime(0);
    setPlaying(false);
    setNotice(null);
  }

  /** Removes a library entry only. Clips keep their own scene, and the project object stays. */
  function removeWorld(row: Row) {
    const index = allRows.findIndex((candidate) => candidate.key === row.key);
    const remaining = allRows.filter((candidate) => candidate.key !== row.key);
    setLibrary(removeFromLibrary(settings, projectId, row.key));
    if (selected?.key !== row.key) return;
    // The next world takes its place, or the one before it when it was last.
    const next = remaining[Math.min(index, remaining.length - 1)];
    if (next) openWorld(next);
    else clearWorld();
  }

  function changeSpeed(speed: number) {
    clockRef.current?.setSpeed(speed);
    setStretch((current) => ({ ...current, speed }));
  }

  function toggleLoop(next: boolean) {
    setLoop(next);
    clockRef.current?.setLoop(next);
  }

  function setStartHere() {
    const clock = clockRef.current;
    if (!clock || !selected) return;
    setStretch((current) => setStretchStart(current, clock.time, selected.duration));
  }

  function setEndHere() {
    const clock = clockRef.current;
    if (!clock || !selected) return;
    setStretch((current) => setStretchEnd(current, clock.time, selected.duration));
  }

  function timeAt(clientX: number): number {
    const bar = barRef.current;
    if (!bar || !selected) return 0;
    const rect = bar.getBoundingClientRect();
    const fraction = rect.width > 0 ? Math.min(Math.max((clientX - rect.left) / rect.width, 0), 1) : 0;
    return fraction * selected.duration;
  }

  function onBarDown(event: PointerEvent<HTMLDivElement>) {
    if (!selected) return;
    event.currentTarget.setPointerCapture?.(event.pointerId);
    scrubbing.current = true;
    seekTo(timeAt(event.clientX));
  }

  function onBarMove(event: PointerEvent<HTMLDivElement>) {
    if (scrubbing.current) seekTo(timeAt(event.clientX));
  }

  function onBarUp(event: PointerEvent<HTMLDivElement>) {
    scrubbing.current = false;
    event.currentTarget.releasePointerCapture?.(event.pointerId);
  }

  function onGroupKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    // Controls keep their own keys (Space on a button clicks it; typing in a select stays put).
    const target = event.target as HTMLElement;
    if (target.closest?.('input, select, textarea, button')) return;
    const clock = clockRef.current;
    if (!clock || !selected) return;
    const action = keyAction(event, { time: clock.time, duration: selected.duration });
    if (!action) return;
    event.preventDefault();
    if (action.type === 'toggle') togglePlay();
    else if (action.type === 'seek') seekTo(action.time);
    else if (action.type === 'setStart') setStartHere();
    else setEndHere();
  }

  async function importFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    if (!storage) {
      setNotice({ tone: 'error', text: 'Project storage is unavailable, so the world cannot be imported.' });
      return;
    }
    setBusy(true);
    setNotice(null);
    try {
      const authoring = await loadAuthoring();
      const bytes = new Uint8Array(await file.arrayBuffer());
      const parsed = await authoring.parsePreparedScenePackage(bytes);
      const ingested = await authoring.ingestPreparedPackage(storage, parsed);
      if (!mounted.current) return;
      const name = file.name.replace(/\.[^.]*$/, '') || 'Imported world';
      const entry: LibraryEntry = {
        objectId: ingested.package.object_id,
        revision: ingested.package.digest,
        name,
        duration: parsed.manifest.duration,
        authoredFps: parsed.manifest.authoredFps,
        stops: [],
      };
      setLibrary(addToLibrary(settings, projectId, entry));
      openWorld(rowFromEntry(entry));
      ctx.chrome.toast(`Imported ${name}`, 'info');
    } catch (cause) {
      if (!mounted.current) return;
      const message = errorMessage(cause);
      setNotice({ tone: 'error', text: `Could not import this world: ${message}` });
      ctx.chrome.toast(`World import failed: ${message}`, 'error');
      reportError(ctx, 'world-explorer/import-failed', `World import failed: ${message}`);
    } finally {
      if (mounted.current) setBusy(false);
    }
  }

  async function addSample() {
    if (!storage) {
      setNotice({ tone: 'error', text: 'Project storage is unavailable, so the sample cannot be added.' });
      return;
    }
    setBusy(true);
    setNotice(null);
    try {
      const [authoring, { SAMPLE_WORLD: sample }] = await Promise.all([loadAuthoring(), import('./worlds/sample')]);
      const parsed = await authoring.parsePreparedScenePackage(new TextEncoder().encode(sample.packageJson));
      const ingested = await authoring.ingestPreparedPackage(storage, parsed);
      if (!mounted.current) return;
      const entry: LibraryEntry = {
        objectId: ingested.package.object_id,
        revision: ingested.package.digest,
        name: sample.name,
        duration: parsed.manifest.duration,
        authoredFps: parsed.manifest.authoredFps,
        stops: sample.stops.map((stop) => ({ time: stop.time, name: stop.name })),
      };
      // The same package already in the library is just selected, not saved twice.
      const existing = readLibrary(settings, projectId).find((candidate) => worldKey(candidate) === worldKey(entry));
      if (existing) {
        openWorld(rowFromEntry(existing));
      } else {
        setLibrary(addToLibrary(settings, projectId, entry));
        openWorld(rowFromEntry(entry));
        ctx.chrome.toast(`Added ${sample.name} to the library`, 'info');
      }
    } catch (cause) {
      if (!mounted.current) return;
      const message = errorMessage(cause);
      setNotice({ tone: 'error', text: `Could not add the sample world: ${message}` });
      ctx.chrome.toast(`Sample world failed: ${message}`, 'error');
      reportError(ctx, 'world-explorer/sample-failed', `Sample world failed: ${message}`);
    } finally {
      if (mounted.current) setBusy(false);
    }
  }

  async function addToVideo() {
    if (!selected || !liveScene || addReason) return;
    const snapshot = readSnapshot(ctx);
    if (!snapshot) return;
    setBusy(true);
    setNotice(null);
    try {
      const at = video?.view.getSnapshot().playhead.time ?? 0;
      const span = stretchDuration(stretch);
      const { track } = freeVisualTrack(snapshot, at, span);
      const id = newClipId(snapshot);
      const authoring = await loadAuthoring();
      await authoring.placeLiveScene(ctx, liveScene, selected.duration, [
        { id, track, at, from: stretch.from, to: stretch.to, rate: stretch.speed },
      ]);
      if (!mounted.current) return;
      // The timeline API offers no way for an extension to select a clip, so the playhead moves to the new clip instead.
      video?.seek(at);
      setSnap(readSnapshot(ctx));
      ctx.chrome.toast(`Added to ${track} at ${clockText(at)}`, 'info');
    } catch (cause) {
      if (!mounted.current) return;
      const message = errorMessage(cause);
      setNotice({ tone: 'error', text: `Could not add to the video: ${message}` });
      ctx.chrome.toast(`Add to video failed: ${message}`, 'error');
      reportError(ctx, 'world-explorer/add-failed', `Add to video failed: ${message}`);
    } finally {
      if (mounted.current) setBusy(false);
    }
  }

  async function updateClip() {
    if (!followedClipId || !followedUse || busy) return;
    setBusy(true);
    setNotice(null);
    try {
      const authoring = await loadAuthoring();
      await authoring.updateLiveSceneClip(ctx, followedClipId, stretch);
      if (!mounted.current) return;
      setSnap(readSnapshot(ctx));
      ctx.chrome.toast('Clip updated', 'info');
    } catch (cause) {
      if (!mounted.current) return;
      const message = errorMessage(cause);
      setNotice({ tone: 'error', text: `Could not update the clip: ${message}` });
      ctx.chrome.toast(`Clip update failed: ${message}`, 'error');
      reportError(ctx, 'world-explorer/update-failed', `Clip update failed: ${message}`);
    } finally {
      if (mounted.current) setBusy(false);
    }
  }

  const overlayText = sceneError ?? loadError?.message ?? (selected ? 'Opening world…' : 'Choose a world to travel through.');
  const overlayIsError = Boolean(sceneError || (loadError && loadError.key === selected?.key));
  const showOverlay = !ready;

  const optionLabel = (row: Row) => `${row.name} · ${clockText(row.duration)}${row.uses.length ? ` · ${row.uses.length} use${row.uses.length === 1 ? '' : 's'}` : ''}`;

  return (
    <section className="flex h-full min-h-0 flex-col gap-3 overflow-y-auto p-3 text-sm" aria-label="World Explorer">
      {/* The remove action stays quiet until its row is hovered or has focus inside it. */}
      <style>{'.world-explorer-remove{opacity:0}.world-explorer-library-row:hover .world-explorer-remove,.world-explorer-library-row:focus-within .world-explorer-remove{opacity:1}'}</style>
      {allRows.length > 0 ? (
        <div className="flex min-w-0 items-center gap-2">
          <select
            aria-label="World"
            className={`${select} min-w-0 flex-1`}
            value={selected?.key ?? ''}
            onChange={(event) => pick(event.target.value)}
          >
            {!selected ? <option value="">Choose a world</option> : null}
            {rows.timeline.length ? (
              <optgroup label="In this video">
                {rows.timeline.map((row) => <option key={row.key} value={row.key}>{optionLabel(row)}</option>)}
              </optgroup>
            ) : null}
            {rows.library.length ? (
              <optgroup label="Library">
                {rows.library.map((row) => <option key={row.key} value={row.key}>{optionLabel(row)}</option>)}
              </optgroup>
            ) : null}
          </select>
          <button type="button" className={`${button} shrink-0 border border-border`} disabled={busy} onClick={() => importInput.current?.click()}>
            Import world…
          </button>
          <input
            ref={importInput}
            className="sr-only"
            tabIndex={-1}
            type="file"
            aria-label="Import world file"
            accept=".json,application/json"
            onChange={(event) => { void importFile(event); }}
          />
        </div>
      ) : null}

      {rows.library.length ? (
        <ul aria-label="Library" className="flex flex-col gap-0.5">
          {rows.library.map((row) => (
            <li key={row.key} className="world-explorer-library-row flex min-w-0 items-center gap-1 rounded-md hover:bg-muted">
              <button
                type="button"
                className="min-h-8 min-w-0 flex-1 truncate rounded-md px-2 py-1 text-left text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                aria-current={row.key === selected?.key ? 'true' : undefined}
                onClick={() => pick(row.key)}
              >
                {row.name} <span className="tabular-nums text-muted-foreground">{clockText(row.duration)}</span>
              </button>
              <button
                type="button"
                aria-label={`Remove ${row.name} from library`}
                title={`Remove ${row.name} from library`}
                disabled={busy}
                className="world-explorer-remove flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-muted-foreground hover:bg-background hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
                onClick={() => removeWorld(row)}
              >
                <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
              </button>
            </li>
          ))}
        </ul>
      ) : null}

      {allRows.length > 0 && !sampleSaved ? (
        <p className="flex items-center justify-between gap-2 text-[11px] text-muted-foreground">
          <span>Sample world: {SAMPLE_LABEL}</span>
          <button type="button" className={`${button} border border-border`} disabled={busy} onClick={() => { void addSample(); }}>Add</button>
        </p>
      ) : null}

      {allRows.length === 0 ? (
        <div className="flex flex-col gap-3 rounded-md border border-border/70 p-3">
          <p className="text-sm text-muted-foreground">A world is a live 3D scene you can travel through. Find a stretch you like, then add it to your video.</p>
          <div className="flex flex-wrap gap-2">
            <button type="button" className={`${button} bg-primary/10 text-primary`} disabled={busy} onClick={() => { void addSample(); }}>Add {SAMPLE_LABEL}</button>
            <button type="button" className={`${button} border border-border`} disabled={busy} onClick={() => importInput.current?.click()}>Import world…</button>
            <input
              ref={importInput}
              className="sr-only"
              tabIndex={-1}
              type="file"
              aria-label="Import world file"
              accept=".json,application/json"
              onChange={(event) => { void importFile(event); }}
            />
          </div>
        </div>
      ) : null}

      {notice ? (
        <p role="status" className="text-[11px] text-muted-foreground" style={notice.tone === 'error' ? ERROR_STYLE : undefined}>{notice.text}</p>
      ) : null}

      <div
        ref={viewerRef}
        className="relative w-full overflow-hidden rounded-md border border-border/70"
        style={{ ...VIEWER_STYLE, height: viewHeight }}
      >
        {liveScene && selected ? (
          <Suspense fallback={null}>
            <LazySceneSurface
              key={selected.key}
              source={liveScene}
              sourceTime={renderTime}
              width={viewWidth}
              height={viewHeight}
              showStatus={false}
              onStatus={handleStatus}
              onReady={handleReady}
            />
          </Suspense>
        ) : null}
        {showOverlay ? (
          <div
            className="absolute inset-0 grid place-items-center p-4 text-center text-xs"
            style={{ ...OVERLAY_STYLE, ...(overlayIsError ? ERROR_STYLE : null) }}
          >
            {overlayText}
          </div>
        ) : null}
      </div>

      <div
        role="group"
        aria-label="World viewer"
        tabIndex={0}
        className="flex flex-col gap-3 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        onKeyDown={onGroupKeyDown}
      >
        <div className="flex flex-wrap items-center gap-2">
          <button type="button" className={`${button} w-16 border border-border`} disabled={!ready} onClick={togglePlay}>
            {playing ? 'Pause' : 'Play'}
          </button>
          <select
            aria-label="Speed"
            className={select}
            value={String(stretch.speed)}
            disabled={!selected}
            onChange={(event) => changeSpeed(Number(event.target.value))}
          >
            {speedOptions.map((speed) => <option key={speed} value={speed}>{speedLabel(speed)}</option>)}
          </select>
          <label className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <input type="checkbox" checked={loop} disabled={!selected} onChange={(event) => toggleLoop(event.target.checked)} />
            Loop
          </label>
          <span className="ml-auto text-[11px] tabular-nums text-muted-foreground">
            {clockText(shownTime, 1)} / {clockText(duration)}
          </span>
        </div>

        <div
          ref={barRef}
          role="slider"
          tabIndex={0}
          aria-label="Travel position"
          aria-valuemin={0}
          aria-valuemax={duration}
          aria-valuenow={Number(shownTime.toFixed(2))}
          aria-valuetext={clockText(shownTime, 1)}
          aria-disabled={!selected}
          className="relative h-7 touch-none select-none rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          onPointerDown={onBarDown}
          onPointerMove={onBarMove}
          onPointerUp={onBarUp}
          onPointerCancel={onBarUp}
        >
          <div className="absolute inset-x-0 top-1/2 h-1 -translate-y-1/2 rounded-full" style={{ background: 'hsl(var(--muted-foreground) / 0.25)' }} />
          {selected ? (
            <>
              {selected.uses.map((use) => (
                <div
                  key={use.clipId}
                  title={`On ${use.track} at ${clockText(use.at)}`}
                  className="absolute top-1/2 h-1 -translate-y-1/2 rounded-full"
                  style={{ left: percent(use.from, duration), width: percent(use.to - use.from, duration), background: 'hsl(var(--muted-foreground) / 0.45)' }}
                />
              ))}
              <div
                className="absolute top-1/2 h-2.5 -translate-y-1/2 rounded-full"
                style={{ left: percent(stretch.from, duration), width: percent(stretch.to - stretch.from, duration), background: 'hsl(var(--primary) / 0.45)' }}
              />
              {stops.map((stop) => (
                <span
                  key={`${stop.time}:${stop.name}`}
                  title={stop.name}
                  className="absolute top-1/2 h-3.5 w-px -translate-y-1/2"
                  style={{ left: percent(stop.time, duration), background: 'hsl(var(--foreground) / 0.6)' }}
                />
              ))}
              <div className="absolute inset-y-0 w-px" style={{ left: percent(shownTime, duration), background: 'hsl(var(--primary))' }} />
            </>
          ) : null}
        </div>

        {stops.length ? (
          <div className="flex flex-wrap gap-1.5">
            {stops.map((stop) => (
              <button
                key={`${stop.time}:${stop.name}`}
                type="button"
                className="h-7 rounded-full border border-border/70 px-2 text-[11px] hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
                disabled={!ready}
                onClick={() => seekTo(stop.time)}
              >
                {stop.name} <span className="tabular-nums text-muted-foreground">{clockText(stop.time)}</span>
              </button>
            ))}
          </div>
        ) : null}

        {selected ? (
          <div className="flex flex-wrap items-center gap-2">
            <button type="button" className={`${button} border border-border`} title="Set the stretch start to the travel position (I)" onClick={setStartHere}>Set start (I)</button>
            <button type="button" className={`${button} border border-border`} title="Set the stretch end to the travel position (O)" onClick={setEndHere}>Set end (O)</button>
            <p className="ml-auto text-[11px] tabular-nums text-muted-foreground">
              Stretch {clockText(stretch.from, 1)} – {clockText(stretch.to, 1)} · {stretchDuration(stretch).toFixed(1)} s at {speedLabel(stretch.speed)}
            </p>
          </div>
        ) : null}
      </div>

      <div className="flex flex-col gap-2 border-t border-border/70 pt-3">
        {followedUse ? (
          <p className="text-[11px] text-muted-foreground">Editing clip on {followedUse.track} at {clockText(followedUse.at)}</p>
        ) : null}
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            className={`${button} bg-primary/10 text-primary`}
            disabled={Boolean(addReason)}
            title={addReason ?? 'Add the selected stretch to the video at the playhead'}
            onClick={() => { void addToVideo(); }}
          >
            Add to video
          </button>
          {followedUse ? (
            <button
              type="button"
              className={`${button} border border-border`}
              disabled={!followedDiffers || busy}
              title={followedDiffers ? 'Write this stretch back to the clip' : 'The stretch matches the clip'}
              onClick={() => { void updateClip(); }}
            >
              Update clip
            </button>
          ) : null}
          {addReason ? <p className="text-[11px] text-muted-foreground">{addReason}</p> : null}
        </div>
      </div>
    </section>
  );
}

export default WorldExplorerPanel;
