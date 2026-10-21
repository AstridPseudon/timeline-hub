import { lazy, Suspense, useEffect, useMemo, useRef, useState, type ChangeEvent, type KeyboardEvent, type MouseEvent, type PointerEvent } from 'react';
import type { ExtensionContext, PanelRenderProps, ProjectDocumentSurface, TimelineSnapshot } from '@astrid/editor-sdk';
import { LIVE_SCENE_CLIP_TYPE_ID } from '../identity';
import type { SceneExplore, SceneInfo, SceneStatus } from '../runtime';
import { loadLibrary, updateLibrary } from './library';
import { defaultExploreSpeed, FreeCamera, type ViewPose } from './camera';
import {
  camerasOrImplicit,
  cameraIndexAt,
  chooseDefaultWorld,
  clampStretch,
  clipName,
  eventsInCamera,
  exploreKey,
  fitToBox,
  freeVisualTrack,
  HINT_DISMISSED_KEY,
  keyAction,
  KEY_MAP,
  lastWorldKey,
  newClipId,
  removeEntry,
  renameEntry,
  setStretchEnd,
  setStretchStart,
  SHIFT_BOOST,
  speedScaleLabel,
  stretchDuration,
  stretchMatches,
  upsertEntry,
  withInfo,
  TravelClock,
  wheelSpeedScale,
  worldKey,
  worldsFromSnapshot,
  worldTitleFromFilename,
  type CameraMove,
  type LibraryEntry,
  type Stretch,
  type WorldEvent,
} from './model';
import { buildRows, rowFromEntry, type Row } from './rows';
import { Select } from './Select';
import { TimeBar, type BarMarker } from './TimeBar';
import { button, chip, clockText, ERROR_STYLE, errorMessage, OVERLAY_STYLE, PILL_STYLE, speedLabel, VIEWER_STYLE } from './ui';
import { WorldList } from './WorldList';

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
/** At this container width the panel uses its side column (the popped-out layout). */
const WIDE_REM = 38;
const SIDE_COLUMN = '13rem';
/** Both modes' controls share this height in the side layout, so the viewer keeps its size when the mode changes. */
const CONTROLS_MIN_HEIGHT = '10rem';
/** Wide enough to see the world, narrow enough that a big view does not stretch its edges. */
const VIEW_FOV = 50;
/** Radians of turn per dragged pixel. */
const LOOK_PER_PIXEL = 0.0035;
/** Touch pans and pinches move this many seconds of travel per 120 px. */
const TOUCH_PIXELS_PER_SECOND = 120;
const HINT_TEXT = 'Drag to look · WASD to move · Scroll for speed';
const TOUCH_HINT_TEXT = 'Drag to look · Two fingers to move';
/** The hint fades this long after the user has both looked and moved. */
const HINT_FADE_MS = 700;
/** A drag counts as looking once it has gone this far. */
const LOOKED_PIXELS = 12;

type Mode = 'explore' | 'cameras';
type Frame = { time: number; worldTime?: number; view?: ViewPose };
type Declared = { key: string; events: WorldEvent[]; cameras: CameraMove[]; explore: SceneExplore | null };

const percent = (time: number, duration: number) => `${duration > 0 ? Math.min(Math.max(time / duration, 0), 1) * 100 : 0}%`;

function aspectOf(resolution: string | undefined): number {
  const match = /^(\d+)x(\d+)$/.exec(resolution ?? '');
  if (!match) return FALLBACK_ASPECT;
  const width = Number(match[1]);
  const height = Number(match[2]);
  return width > 0 && height > 0 ? width / height : FALLBACK_ASPECT;
}

/** The project's document store; undefined when the host has none. */
function projectDocuments(ctx: ExtensionContext): ProjectDocumentSurface | undefined {
  try {
    return ctx.creative.documents;
  } catch {
    return undefined;
  }
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

function readSetting<T>(ctx: ExtensionContext, key: string): T | undefined {
  try {
    return ctx.services.settings.get(key) as T | undefined;
  } catch {
    return undefined;
  }
}

function writeSetting(ctx: ExtensionContext, key: string, value: unknown) {
  try {
    ctx.services.settings.set(key, value);
  } catch {
    // Remembering is a convenience; never fail the panel over it.
  }
}

export function WorldExplorerPanel(props: PanelRenderProps & { context: ExtensionContext }) {
  const { context: ctx, video, visible, popout } = props;
  const storage = ctx.creative.projectObjects;

  const [snap, setSnap] = useState<TimelineSnapshot | undefined>(() => readSnapshot(ctx));
  const projectId = snap?.projectId ?? null;
  const [library, setLibrary] = useState<LibraryEntry[]>([]);
  const [libraryReady, setLibraryReady] = useState(false);
  const [selected, setSelected] = useState<Row | null>(null);
  const [loaded, setLoaded] = useState<{ key: string; liveScene: Record<string, unknown> } | null>(null);
  const [loadError, setLoadError] = useState<{ key: string; message: string } | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [sceneError, setSceneError] = useState<string | null>(null);
  const [declared, setDeclared] = useState<Declared | null>(null);
  const [modeChoice, setModeChoice] = useState<Mode>('explore');
  const [frame, setFrame] = useState<Frame>({ time: 0 });
  const [worldTime, setWorldTime] = useState(0);
  const [worldPaused, setWorldPaused] = useState(false);
  const [speedScale, setSpeedScale] = useState(1);
  const [hintDismissed, setHintDismissed] = useState(() => readSetting<boolean>(ctx, HINT_DISMISSED_KEY) === true);
  const [hintFading, setHintFading] = useState(false);
  const [keysOpen, setKeysOpen] = useState(false);
  const [touchSeen, setTouchSeen] = useState(false);
  const [cameraIndex, setCameraIndex] = useState(0);
  const [stretch, setStretch] = useState<Stretch>({ from: 0, to: 1, speed: 1 });
  const [loop, setLoop] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [shownTime, setShownTime] = useState(0);
  const [followedClipId, setFollowedClipId] = useState<string | null>(null);
  const [liveClipId, setLiveClipId] = useState<string | null>(null);
  const [stage, setStage] = useState({ width: 0, height: 0 });
  const [rootWidth, setRootWidth] = useState(0);
  const [listOpen, setListOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<{ tone: 'error' | 'info'; text: string; details?: string } | null>(null);

  // World time (Explore) and travel time (Cameras) are separate clocks over the same world.
  const worldClock = useRef<TravelClock | null>(null);
  const travelClock = useRef<TravelClock | null>(null);
  const roam = useRef<FreeCamera | null>(null);
  // Dragging turns the head rather than grabbing the world, so the cursor is a crosshair (hidden mid-drag).
  const [dragging, setDragging] = useState(false);
  const baseSpeed = useRef(1);
  const scaleRef = useRef(1);
  const shiftRef = useRef(false);
  const heldKeys = useRef(new Set<string>());
  const pointers = useRef(new Map<number, { x: number; y: number }>());
  // Frames are back-pressured: at most one render in flight, and only after the scene reported ready.
  const readyRef = useRef(false);
  const inFlight = useRef(false);
  const sentKey = useRef('');
  const exploreRef = useRef<SceneExplore | null | undefined>(undefined);
  const modeRef = useRef<Mode>('explore');
  const revealedRef = useRef(false);
  const camerasRef = useRef<CameraMove[]>([]);
  const cameraIndexRef = useRef(0);
  const focusTime = useRef<number | null>(null);
  const openRequest = useRef(0);
  const mounted = useRef(false);
  const rootRef = useRef<HTMLElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<HTMLDivElement>(null);
  const importInput = useRef<HTMLInputElement>(null);
  const seenClipRef = useRef<string | null | undefined>(undefined);
  const liveClipRef = useRef<string | null>(null);
  const projectRef = useRef<string | null | undefined>(undefined);
  const hintRef = useRef(hintDismissed);
  const lookedRef = useRef(false);
  const movedRef = useRef(false);
  const dragPixels = useRef(0);
  const hintTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const libraryRef = useRef<LibraryEntry[]>([]);
  const saveChain = useRef<Promise<void>>(Promise.resolve());

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      clearTimeout(hintTimer.current);
      worldClock.current = null;
      travelClock.current = null;
    };
  }, []);

  const documents = projectDocuments(ctx);
  libraryRef.current = library;
  // The library is a project document: read it when the project changes and whenever the panel is shown,
  // so worlds added from another timeline or by a collaborator appear.
  useEffect(() => {
    if (!visible || !projectId || !documents) return;
    let current = true;
    loadLibrary(documents, projectId).then(
      (list) => { if (current && mounted.current) { setLibrary(list); setLibraryReady(true); } },
      (cause) => {
        if (!current || !mounted.current) return;
        setLibraryReady(true);
        setNotice({ tone: 'error', text: `Could not load this project's worlds: ${errorMessage(cause)}` });
        reportError(ctx, 'world-explorer/library-load-failed', `World library load failed: ${errorMessage(cause)}`);
      },
    );
    return () => { current = false; };
  }, [visible, projectId, documents]);

  /** Shows a library change at once, then saves it to the project; saves run one after another. */
  function commitLibrary(change: (list: LibraryEntry[]) => LibraryEntry[], quiet = false): Promise<void> {
    if (!documents || !projectId) return Promise.resolve();
    const scope = projectId;
    libraryRef.current = change(libraryRef.current);
    setLibrary(libraryRef.current);
    const run = saveChain.current.then(async () => {
      const saved = await updateLibrary(documents, scope, change);
      if (mounted.current && projectRef.current === scope) { libraryRef.current = saved; setLibrary(saved); }
    });
    saveChain.current = run.catch(() => undefined);
    return run.catch((cause) => {
      // Registering worlds the timeline already uses is best effort: a read-only project still lists them.
      if (quiet) return;
      const message = errorMessage(cause);
      if (mounted.current) setNotice({ tone: 'error', text: `Could not save the world library: ${message}` });
      reportError(ctx, 'world-explorer/library-save-failed', `World library save failed: ${message}`);
    });
  }

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

  // Stop everything when the panel is hidden.
  useEffect(() => {
    if (visible) return;
    heldKeys.current.clear();
    pointers.current.clear();
    travelClock.current?.pause();
    setPlaying(false);
  }, [visible]);

  const rows = useMemo(() => buildRows(snap, library), [snap, library]);
  // A world used on this timeline that the project does not list yet joins the library, so every timeline of the project lists it.
  useEffect(() => {
    if (!libraryReady || !documents || !projectId) return;
    const missing = rows.timeline.filter((row) => row.liveScene && !library.some((entry) => worldKey(entry) === row.key));
    if (missing.length === 0) return;
    // Batched, and idempotent against a newer list, so two tabs registering the same worlds converge.
    const timer = setTimeout(() => {
      void commitLibrary((list) => missing.reduce(
        (next, row) => (next.some((entry) => worldKey(entry) === row.key) ? next : upsertEntry(next, {
          objectId: row.objectId, revision: row.revision, name: row.name, duration: row.duration, authoredFps: row.authoredFps,
          events: [...row.events], cameras: [...row.cameras],
        })),
        list,
      ), true);
    }, 400);
    return () => clearTimeout(timer);
  }, [libraryReady, rows, library, projectId, documents]);
  const allRows = useMemo(() => [...rows.timeline, ...rows.library], [rows]);
  const duration = selected?.duration ?? 0;
  const aspect = aspectOf(snap?.outputMetadata?.resolution);
  const liveScene = loaded && selected && loaded.key === selected.key ? loaded.liveScene : undefined;
  const info = selected && declared?.key === selected.key ? declared : null;
  // What the scene reported wins, even when empty; before it loads, the library's saved copy stands in.
  const events = selected ? (info ? info.events : [...selected.events]) : [];
  const cameras = useMemo(
    () => camerasOrImplicit(selected ? (info ? info.cameras : selected.cameras) : [], duration),
    [selected, info, duration],
  );
  const camera = cameras[Math.min(cameraIndex, cameras.length - 1)];
  // undefined until the scene reports; null when it declared no (valid) explore.
  const explore = info ? info.explore : undefined;
  const mode: Mode = explore === null ? 'cameras' : modeChoice;
  const ready = Boolean(liveScene) && revealed && !sceneError;
  const sampleSaved = library.some((entry) => entry.sample);
  const projectReady = Boolean(snap?.projectId && snap?.timelineId);
  const followedUse = followedClipId ? rows.timeline.flatMap((row) => row.uses).find((use) => use.clipId === followedClipId) : undefined;
  const followedDiffers = Boolean(followedUse) && !stretchMatches(followedUse!, stretch, snap?.outputMetadata?.fps ?? 30);
  const stretchValid = stretch.to > stretch.from && stretch.speed > 0;
  const addReason = !selected ? 'Choose a world to add.'
    : !projectReady ? 'Open a timeline to add worlds to a video.'
    : !storage ? 'Project storage is unavailable.'
    : !liveScene ? 'Opening world…'
    : busy ? 'Working…'
    : !stretchValid ? 'The range is empty.'
    : null;
  const speedOptions = [...new Set([...SPEEDS, stretch.speed])].sort((a, b) => a - b);
  const cameraEvents = useMemo(() => (camera ? eventsInCamera(events, camera) : []), [events, camera]);
  const eventMarkers: BarMarker[] = events.map((event, i) => ({
    key: `${i}:${event.start}:${event.name}`, from: event.start, to: event.end ?? event.start, title: event.name, time: clockText(event.start, 1),
  }));
  const cameraMarkers: BarMarker[] = cameraEvents.map(({ event, from, to }, i) => ({
    key: `${i}:${event.start}:${event.name}`, from, to: event.end === undefined ? from : to, title: event.name, time: clockText(from, 1),
  }));

  // The viewer is a free box in the side layout and a full-width strip when docked.
  const wide = rootWidth >= WIDE_REM * 16;
  const viewSize = useMemo(() => {
    if (wide) {
      const fitted = fitToBox(stage.width, stage.height, aspect);
      if (fitted.width > 0) return fitted;
    }
    const width = stage.width > 0 ? Math.max(MIN_VIEW_WIDTH, stage.width) : FALLBACK_VIEW_WIDTH;
    return { width, height: Math.round(width / aspect) };
  }, [wide, stage.width, stage.height, aspect]);

  // Measure the panel (layout switch) and the stage (viewer fit) in both dimensions; jsdom and hidden hosts keep the fallback.
  useEffect(() => {
    const root = rootRef.current;
    const element = stageRef.current;
    if (!root || !element) return;
    const measure = () => {
      setRootWidth(Math.floor(root.clientWidth));
      const width = Math.floor(element.clientWidth);
      const height = Math.floor(element.clientHeight);
      setStage((current) => (current.width === width && current.height === height ? current : { width, height }));
    };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(measure);
    observer.observe(root);
    observer.observe(element);
    return () => observer.disconnect();
  }, [wide]);

  // The wheel changes speed. React wheel listeners are passive, so attach one that may preventDefault.
  useEffect(() => {
    const element = viewerRef.current;
    if (!element) return;
    const onWheel = (event: WheelEvent) => {
      if (effectiveMode() !== 'explore' || !roam.current) return;
      event.preventDefault();
      const next = wheelSpeedScale(scaleRef.current, event.deltaY);
      if (next === scaleRef.current) return;
      scaleRef.current = next;
      setSpeedScale(next);
    };
    element.addEventListener('wheel', onWheel, { passive: false });
    return () => element.removeEventListener('wheel', onWheel);
  }, []);

  function effectiveMode(): Mode {
    return exploreRef.current === null ? 'cameras' : modeRef.current;
  }

  // Frame loop: only while visible with a world loaded. Advances world time, moves the free camera, offers the next frame.
  useEffect(() => {
    if (!visible || !liveScene) return;
    let handle = 0;
    let last = performance.now();
    const step = () => {
      const now = performance.now();
      const dt = Math.max(0, (now - last) / 1000);
      last = now;
      if (effectiveMode() === 'explore') {
        const world = worldClock.current;
        if (world) {
          world.tick(now);
          setWorldTime(world.time);
        }
        const held = heldKeys.current;
        const view = roam.current;
        // Always advance (not only while keys are held): velocity and look ease out after release.
        if (view && (held.size || view.moving)) {
          const axis = (plus: string, minus: string) => (held.has(plus) ? 1 : 0) - (held.has(minus) ? 1 : 0);
          view.advance(
            { forward: axis('forward+', 'forward-'), right: axis('right+', 'right-'), up: axis('up+', 'up-') },
            baseSpeed.current * scaleRef.current * (shiftRef.current ? SHIFT_BOOST : 1),
            dt,
          );
        }
      } else {
        const travel = travelClock.current;
        if (travel?.playing) {
          travel.tick(now);
          setShownTime(travel.time);
          if (!travel.playing) setPlaying(false);
        }
      }
      pump();
      handle = requestAnimationFrame(step);
    };
    handle = requestAnimationFrame(step);
    return () => cancelAnimationFrame(handle);
  }, [visible, liveScene]);

  // Open the default world: the last one viewed in this project, else the first in the video, else the first in the library.
  useEffect(() => {
    if (projectRef.current !== undefined && projectRef.current !== projectId) clearWorld();
    projectRef.current = projectId;
  }, [projectId]);
  useEffect(() => {
    // Wait for the project's library, so the last world viewed can be chosen over a timeline world.
    if (!visible || selected || liveClipId || allRows.length === 0 || (documents && projectId && !libraryReady)) return;
    const row = chooseDefaultWorld(rows.timeline, rows.library, readSetting<string>(ctx, lastWorldKey(projectId)));
    if (row) openWorld(row);
  }, [visible, selected, liveClipId, allRows.length, projectId, libraryReady]);

  // Follow the single selected live-scene clip: open its world in Cameras mode with its stretch.
  useEffect(() => {
    if (!liveClipId) return;
    const snapshot = readSnapshot(ctx);
    if (!snapshot) return;
    const world = worldsFromSnapshot(snapshot).find((candidate) => candidate.uses.some((use) => use.clipId === liveClipId));
    const use = world?.uses.find((candidate) => candidate.clipId === liveClipId);
    const row = world ? buildRows(snapshot, libraryRef.current).timeline.find((candidate) => candidate.key === worldKey(world)) : undefined;
    if (!row || !use) return;
    if (selected?.key === row.key && readyRef.current) {
      // The world is already open (say, the clip was just added from it): follow the clip without reloading the scene.
      followOpenClip(use, liveClipId);
      return;
    }
    openWorld(row, { stretch: { from: use.from, to: use.to, speed: use.speed }, clipId: liveClipId, mode: 'cameras' });
  }, [liveClipId]);

  /** Sends the newest time and view to the scene, at most one frame in flight. Reads refs only. */
  function pump() {
    if (!readyRef.current || inFlight.current) return;
    const mode = effectiveMode();
    const clock = mode === 'explore' ? worldClock.current : travelClock.current;
    if (!clock) return;
    const view = mode === 'explore' ? roam.current : null;
    const key = `${mode}|${clock.time}|${view ? view.version : -1}`;
    if (key === sentKey.current) return;
    sentKey.current = key;
    inFlight.current = true;
    setFrame(view ? { time: clock.time, worldTime: clock.time, view: view.pose(VIEW_FOV) } : { time: clock.time });
  }

  /** Follows a clip of the open world: Cameras mode on the camera holding its start, with its stretch. */
  function followOpenClip(use: { from: number; to: number; speed: number }, clipId: string) {
    const travel = travelClock.current;
    if (!travel || !selected) return;
    const next = clampStretch({ from: use.from, to: use.to, speed: use.speed }, selected.duration);
    const index = cameraIndexAt(camerasRef.current, next.from);
    modeRef.current = 'cameras';
    setModeChoice('cameras');
    enterCamera(index, next.from);
    travel.setSpeed(next.speed);
    setStretch(next);
    setFollowedClipId(clipId);
    pump();
  }

  function seekWorld(time: number) {
    const clock = worldClock.current;
    if (!clock) return;
    clock.seek(time);
    setWorldTime(clock.time);
    pump();
  }

  function seekTravel(time: number) {
    const clock = travelClock.current;
    if (!clock) return;
    clock.seek(time);
    setShownTime(clock.time);
    pump();
  }

  function toggleWorldPause() {
    const clock = worldClock.current;
    if (!clock || !readyRef.current) return;
    if (clock.playing) {
      clock.pause();
      setWorldPaused(true);
    } else {
      clock.play();
      setWorldPaused(false);
    }
  }

  function toggleTravel() {
    const clock = travelClock.current;
    if (!clock || !readyRef.current) return;
    if (clock.playing) {
      clock.pause();
      setPlaying(false);
    } else {
      clock.play();
      setPlaying(true);
    }
  }

  /** Closes the hint for good (the × button). */
  function dismissHint() {
    if (hintRef.current) return;
    hintRef.current = true;
    clearTimeout(hintTimer.current);
    setHintDismissed(true);
    writeSetting(ctx, HINT_DISMISSED_KEY, true);
  }

  /** The hint stays until the user has both looked and moved, then fades. */
  function noteHint(kind: 'looked' | 'moved') {
    if (hintRef.current) return;
    if (kind === 'looked') lookedRef.current = true;
    else movedRef.current = true;
    if (!lookedRef.current || !movedRef.current || hintTimer.current !== undefined) return;
    setHintFading(true);
    writeSetting(ctx, HINT_DISMISSED_KEY, true);
    hintTimer.current = setTimeout(() => {
      hintRef.current = true;
      if (mounted.current) setHintDismissed(true);
    }, HINT_FADE_MS);
  }

  /** Confines Cameras-mode travel to one camera and rests at its start (or the given time). */
  function enterCamera(index: number, at?: number) {
    const move = camerasRef.current[index];
    const travel = travelClock.current;
    if (!move || !travel) return;
    cameraIndexRef.current = index;
    setCameraIndex(index);
    travel.setWindow(move.start, move.end);
    travel.seek(at ?? move.start);
    travel.pause();
    setPlaying(false);
    setShownTime(travel.time);
  }

  function selectCamera(index: number, at?: number) {
    const move = cameras[index];
    if (!move) return;
    enterCamera(index, at);
    setStretch((current) => ({ from: move.start, to: move.end, speed: current.speed }));
    setFollowedClipId(null);
    pump();
  }

  function switchMode(next: Mode) {
    modeRef.current = next;
    setModeChoice(next);
    if (next === 'cameras') {
      const move = camerasRef.current[cameraIndexRef.current];
      const travel = travelClock.current;
      if (move && travel) travel.setWindow(move.start, move.end);
      travel?.pause();
      setPlaying(false);
      setShownTime(travel?.time ?? 0);
    }
    pump();
  }

  function dismissNotice() {
    setNotice(null);
  }

  // Try again reopens the same world, keeping its mode and stretch.
  function retryWorld() {
    if (selected) openWorld(selected, { stretch, clipId: followedClipId, mode: modeChoice });
  }

  function openWorld(row: Row, options: { stretch?: Stretch; clipId?: string | null; mode?: Mode } = {}) {
    const token = ++openRequest.current;
    const known = camerasOrImplicit(row.cameras, row.duration);
    const index = options.stretch ? cameraIndexAt(known, options.stretch.from) : 0;
    const next = clampStretch(options.stretch ?? { from: known[index].start, to: known[index].end, speed: 1 }, row.duration);
    const world = new TravelClock({ duration: row.duration, loop: true });
    world.play();
    const travel = new TravelClock({ duration: row.duration, loop });
    travel.setWindow(known[index].start, known[index].end);
    travel.setSpeed(next.speed);
    // A followed clip opens at the start of its stretch.
    travel.seek(next.from);
    const startMode = options.mode ?? 'explore';
    worldClock.current = world;
    travelClock.current = travel;
    roam.current = null;
    exploreRef.current = undefined;
    modeRef.current = startMode;
    camerasRef.current = known;
    cameraIndexRef.current = index;
    focusTime.current = options.stretch ? options.stretch.from : null;
    heldKeys.current.clear();
    pointers.current.clear();
    readyRef.current = false;
    inFlight.current = false;
    revealedRef.current = false;
    const first = startMode === 'explore' ? world : travel;
    sentKey.current = `${startMode}|${first.time}|-1`;
    setSelected(row);
    setFollowedClipId(options.clipId ?? null);
    setModeChoice(startMode);
    setCameraIndex(index);
    setStretch(next);
    setLoaded(null);
    setLoadError(null);
    setRevealed(false);
    setSceneError(null);
    setDeclared(null);
    setFrame({ time: first.time });
    setWorldTime(0);
    setWorldPaused(false);
    setShownTime(travel.time);
    setPlaying(false);
    setListOpen(false);
    setNotice(null);
    writeSetting(ctx, lastWorldKey(projectId), row.key);
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
    if (status.phase === 'ready') {
      readyRef.current = true;
      inFlight.current = false;
      setSceneError(null);
      // Reveal once the scene has drawn what the user will see first: the free view, or the camera.
      const declaredExplore = exploreRef.current;
      if (!revealedRef.current && declaredExplore !== undefined
        && (declaredExplore === null || status.view !== undefined || modeRef.current === 'cameras')) {
        revealedRef.current = true;
        setRevealed(true);
      }
      pump();
    } else if (status.phase === 'error') {
      readyRef.current = false;
      inFlight.current = false;
      setSceneError(status.error ?? 'The scene could not start.');
      worldClock.current?.fail();
      travelClock.current?.fail();
      setPlaying(false);
    }
  }

  function handleReady(reported: SceneInfo) {
    if (!selected) return;
    const events = reported.events.map((event) => ({ ...event }));
    const reportedCameras = reported.cameras.map((move) => ({ ...move }));
    setDeclared({ key: selected.key, events, cameras: reportedCameras, explore: reported.explore });
    // A library world keeps what its scene reported, so the next visit shows it before the scene loads.
    if (withInfo(libraryRef.current, selected.key, { events, cameras: reportedCameras }).length) {
      void commitLibrary((list) => withInfo(list, selected.key, { events, cameras: reportedCameras }));
    }
    exploreRef.current = reported.explore;
    if (reported.explore) {
      roam.current = new FreeCamera(reported.explore.start, reported.explore.bounds);
      baseSpeed.current = reported.explore.speed ?? defaultExploreSpeed(reported.explore.bounds);
    } else {
      roam.current = null;
    }
    // The scene's own cameras replace the library's copy; a followed clip picks the one holding its start.
    const next = camerasOrImplicit(reportedCameras, selected.duration);
    camerasRef.current = next;
    const followed = focusTime.current !== null;
    const index = followed ? cameraIndexAt(next, focusTime.current!) : 0;
    cameraIndexRef.current = index;
    setCameraIndex(index);
    const travel = travelClock.current;
    if (travel) {
      travel.setWindow(next[index].start, next[index].end);
      if (!followed) {
        travel.seek(next[index].start);
        setShownTime(travel.time);
        setStretch((current) => ({ from: next[index].start, to: next[index].end, speed: current.speed }));
      }
    }
    if (exploreRef.current === null && modeRef.current === 'explore') modeRef.current = 'cameras';
  }

  function pick(key: string) {
    const row = allRows.find((candidate) => candidate.key === key);
    // Picking the open world again (a double-click to rename) must not restart it.
    if (row && row.key !== selected?.key) openWorld(row);
    else setListOpen(false);
  }

  function stepWorld(direction: 1 | -1) {
    if (allRows.length < 2) return;
    const index = allRows.findIndex((candidate) => candidate.key === selected?.key);
    openWorld(allRows[(index + direction + allRows.length) % allRows.length]);
  }

  /** Clears the viewer when no world is left to show. */
  function clearWorld() {
    openRequest.current++;
    worldClock.current = null;
    travelClock.current = null;
    roam.current = null;
    exploreRef.current = undefined;
    readyRef.current = false;
    inFlight.current = false;
    setSelected(null);
    setFollowedClipId(null);
    setLoaded(null);
    setLoadError(null);
    setRevealed(false);
    setSceneError(null);
    setDeclared(null);
    setFrame({ time: 0 });
    setWorldTime(0);
    setShownTime(0);
    setPlaying(false);
    setNotice(null);
  }

  /** Removes a library entry only. Clips keep their own scene, and the project object stays. */
  function removeWorld(row: Row) {
    const index = allRows.findIndex((candidate) => candidate.key === row.key);
    const remaining = allRows.filter((candidate) => candidate.key !== row.key);
    void commitLibrary((list) => removeEntry(list, row.key));
    if (selected?.key !== row.key) return;
    // The next world takes its place, or the one before it when it was last.
    const next = remaining[Math.min(index, remaining.length - 1)];
    if (next) openWorld(next);
    else clearWorld();
  }

  /** Renames a world in the library (adding it there first when only the timeline lists it) and in the header when it is selected. */
  function renameWorld(row: Row, name: string) {
    const trimmed = name.trim();
    if (!trimmed) return;
    void commitLibrary((list) => (list.some((e) => worldKey(e) === row.key)
      ? renameEntry(list, row.key, trimmed)
      : upsertEntry(list, { objectId: row.objectId, revision: row.revision, name: trimmed, duration: row.duration, authoredFps: row.authoredFps, events: [...row.events], cameras: [...row.cameras] })));
    setSelected((current) => (current?.key === row.key ? { ...current, name: trimmed } : current));
  }

  function changeSpeed(speed: number) {
    travelClock.current?.setSpeed(speed);
    setStretch((current) => ({ ...current, speed }));
  }

  function toggleLoop(next: boolean) {
    setLoop(next);
    travelClock.current?.setLoop(next);
  }

  function setStartHere() {
    const clock = travelClock.current;
    if (!clock || !selected) return;
    setStretch((current) => setStretchStart(current, clock.time, selected.duration));
  }

  function setEndHere() {
    const clock = travelClock.current;
    if (!clock || !selected) return;
    setStretch((current) => setStretchEnd(current, clock.time, selected.duration));
  }

  function resetView() {
    roam.current?.resetSmooth();
    pump();
  }

  // ---- Free roam input: keys act only while the viewer has focus; Esc is never consumed.

  function onViewerKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    shiftRef.current = event.shiftKey;
    if (event.target !== event.currentTarget) return;
    // In Cameras mode the viewer owns the travel keys, so the film never sees them.
    if (effectiveMode() === 'cameras') {
      travelKey(event);
      return;
    }
    if (!roam.current) return;
    if (event.key === '?' && !event.ctrlKey && !event.metaKey && !event.altKey) {
      event.preventDefault();
      setKeysOpen((open) => !open);
      return;
    }
    const action = exploreKey(event);
    if (!action) return;
    event.preventDefault();
    if (action.type === 'move') {
      noteHint('moved');
      heldKeys.current.add(`${action.axis}${action.sign > 0 ? '+' : '-'}`);
    } else if (action.type === 'reset') resetView();
    else toggleWorldPause();
  }

  function onViewerKeyUp(event: KeyboardEvent<HTMLDivElement>) {
    shiftRef.current = event.shiftKey;
    const action = exploreKey(event);
    if (action?.type === 'move') heldKeys.current.delete(`${action.axis}${action.sign > 0 ? '+' : '-'}`);
  }

  function onViewerBlur() {
    heldKeys.current.clear();
    shiftRef.current = false;
    pointers.current.clear();
    setDragging(false);
  }

  function onViewerPointerDown(event: PointerEvent<HTMLDivElement>) {
    if ((event.target as HTMLElement).closest?.('button, [data-viewer-control]')) return;
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    if (event.pointerType === 'touch') setTouchSeen(true);
    event.currentTarget.focus();
    if (effectiveMode() !== 'explore' || !roam.current) return;
    event.currentTarget.setPointerCapture?.(event.pointerId);
    pointers.current.set(event.pointerId, { x: event.clientX, y: event.clientY });
    setDragging(true);
  }

  function onViewerPointerMove(event: PointerEvent<HTMLDivElement>) {
    const previous = pointers.current.get(event.pointerId);
    const view = roam.current;
    if (!previous || !view) return;
    const x = event.clientX;
    const y = event.clientY;
    if (!Number.isFinite(x) || !Number.isFinite(y)) return;
    if (pointers.current.size === 1) {
      // One pointer looks: dragging right turns the view right, dragging down looks down.
      view.lookBy(-(x - previous.x) * LOOK_PER_PIXEL, -(y - previous.y) * LOOK_PER_PIXEL);
      dragPixels.current += Math.hypot(x - previous.x, y - previous.y);
      if (dragPixels.current >= LOOKED_PIXELS) noteHint('looked');
    } else if (pointers.current.size === 2) {
      const other = [...pointers.current.entries()].find(([id]) => id !== event.pointerId)?.[1];
      if (other) {
        // Two fingers move: the pair's drag pans (the world follows the fingers), spreading them moves forward.
        const unit = (baseSpeed.current * scaleRef.current) / TOUCH_PIXELS_PER_SECOND;
        const before = { x: (previous.x + other.x) / 2, y: (previous.y + other.y) / 2, d: Math.hypot(previous.x - other.x, previous.y - other.y) };
        const after = { x: (x + other.x) / 2, y: (y + other.y) / 2, d: Math.hypot(x - other.x, y - other.y) };
        view.translate(-(after.x - before.x) * unit, (after.y - before.y) * unit, (after.d - before.d) * unit);
        noteHint('moved');
      }
    }
    pointers.current.set(event.pointerId, { x, y });
  }

  function onViewerPointerUp(event: PointerEvent<HTMLDivElement>) {
    pointers.current.delete(event.pointerId);
    if (!pointers.current.size) setDragging(false);
    event.currentTarget.releasePointerCapture?.(event.pointerId);
  }

  function onTravelKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    // Controls keep their own keys (Space on a button clicks it; typing in a select stays put).
    const target = event.target as HTMLElement;
    if (target.closest?.('input, select, textarea, button, [role=slider]')) return;
    travelKey(event);
  }

  /** Travel keys: Space play/pause, ←/→ ±1 s (Shift ±5 s), I/O set the range. They never reach the film. */
  function travelKey(event: KeyboardEvent<HTMLDivElement>) {
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    const clock = travelClock.current;
    if (!clock || !selected) return;
    const action = keyAction(event, { time: clock.time, duration: selected.duration });
    if (!action) return;
    event.preventDefault();
    event.stopPropagation();
    if (action.type === 'toggle') toggleTravel();
    else if (action.type === 'seek') seekTravel(Math.min(Math.max(action.time, clock.windowStart), clock.windowEnd));
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
      const name = worldTitleFromFilename(file.name);
      const entry: LibraryEntry = {
        objectId: ingested.package.object_id,
        revision: ingested.package.digest,
        name,
        duration: parsed.manifest.duration,
        authoredFps: parsed.manifest.authoredFps,
        events: [],
        cameras: [],
      };
      await commitLibrary((list) => upsertEntry(list, entry));
      openWorld(rowFromEntry(entry));
      ctx.chrome.toast(`Imported ${name}`, 'info');
    } catch (cause) {
      if (!mounted.current) return;
      const message = errorMessage(cause);
      setNotice({ tone: 'error', text: "This file isn't an Astrid world. Choose a .scene.json file.", details: message });
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
        events: sample.events.map((event) => ({ ...event })),
        cameras: sample.cameras.map((move) => ({ ...move })),
        sample: true,
      };
      // The same package already in the library is just selected, not saved twice.
      const existing = libraryRef.current.find((candidate) => worldKey(candidate) === worldKey(entry));
      if (existing) {
        openWorld(rowFromEntry(existing));
      } else {
        await commitLibrary((list) => upsertEntry(list, entry));
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
        { id, track, at, from: stretch.from, to: stretch.to, rate: stretch.speed, label: clipName(selected.name, mode === 'cameras' ? camera?.name : undefined) },
      ]);
      if (!mounted.current) return;
      // Select the new clip so the explorer follows it; a host without `select` just moves the playhead to it.
      video?.seek(at);
      (video as { select?: (clipIds: readonly string[]) => void } | undefined)?.select?.([id]);
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

  /** A click on a mode or Explore control hands focus back to the viewer, so the movement keys keep working. */
  function refocusViewer(event: MouseEvent<HTMLElement>) {
    const button = (event.target as HTMLElement).closest?.('button');
    if (!button || !button.closest('[data-refocus]') || button.disabled) return;
    viewerRef.current?.focus({ preventScroll: true });
  }

  // Nothing in the project yet: only the welcome card shows. Waits for the library so the card does not flash.
  const showEmpty = (libraryReady || !documents) && allRows.length === 0;
  const overlayText = sceneError ?? loadError?.message ?? (allRows.length ? 'Opening world…' : 'Loading worlds…');
  const overlayIsError = Boolean(sceneError || (loadError && loadError.key === selected?.key));
  const showOverlay = !ready && !showEmpty;
  const selectedIndex = allRows.findIndex((candidate) => candidate.key === selected?.key);
  const exploring = mode === 'explore' && ready && Boolean(explore);
  const showHint = exploring && !hintDismissed;
  const touch = touchSeen || (typeof window !== 'undefined' && typeof window.matchMedia === 'function' && window.matchMedia('(pointer: coarse)').matches);
  const canExpand = Boolean(popout) && !popout!.open;

  const importControl = (
    <input
      ref={importInput}
      className="sr-only"
      tabIndex={-1}
      type="file"
      aria-label="Import world file"
      accept=".json,application/json"
      onChange={(event) => { void importFile(event); }}
    />
  );
  const list = (
    <WorldList
      timeline={rows.timeline}
      library={rows.library}
      selectedKey={selected?.key}
      sampleLabel={SAMPLE_LABEL}
      offerSample={!sampleSaved}
      busy={busy}
      onPick={pick}
      onRemove={removeWorld}
      onRename={renameWorld}
      onAddSample={() => { void addSample(); }}
      onImport={() => importInput.current?.click()}
    />
  );

  const modeToggle = (
    <div role="group" aria-label="Mode" data-refocus className="inline-flex shrink-0 rounded-md border border-border/70 p-0.5">
      {(['explore', 'cameras'] as const).map((value) => {
        const active = mode === value;
        const unavailable = value === 'explore' && explore === null;
        return (
          <button
            key={value}
            type="button"
            aria-pressed={active}
            disabled={!selected || unavailable}
            title={unavailable ? 'This world is not explorable yet' : undefined}
            className="min-h-9 rounded px-3 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50 sm:min-h-7"
            style={active ? { background: 'hsl(var(--primary) / 0.15)', color: 'hsl(var(--primary))' } : undefined}
            onClick={() => switchMode(value)}
          >
            {value === 'explore' ? 'Explore' : 'Cameras'}
          </button>
        );
      })}
    </div>
  );
  const notExplorable = explore === null ? (
    <p className="text-[11px] text-muted-foreground">This world has no free view yet, so only its cameras can be shown.</p>
  ) : null;

  const eventButtons = (
    <div className="flex flex-wrap gap-1.5" role="group" aria-label="Events" data-refocus>
      {events.map((event, i) => (
        <button
          key={`${i}:${event.start}:${event.name}`}
          type="button"
          className={chip}
          disabled={!ready}
          title={event.end === undefined ? `At ${clockText(event.start, 1)}` : `${clockText(event.start, 1)} – ${clockText(event.end, 1)}`}
          onClick={() => seekWorld(event.start)}
        >
          {event.name} <span className="tabular-nums text-muted-foreground">{clockText(event.start)}</span>
        </button>
      ))}
    </div>
  );
  const cameraEventButtons = (
    <div className="flex flex-wrap gap-1.5" role="group" aria-label="Camera events">
      {cameraEvents.map(({ event, from }, i) => (
        <button
          key={`${i}:${event.start}:${event.name}`}
          type="button"
          className={chip}
          disabled={!ready}
          onClick={() => seekTravel(from)}
        >
          {event.name} <span className="tabular-nums text-muted-foreground">{clockText(from)}</span>
        </button>
      ))}
    </div>
  );

  // Side column: what lives beside the viewer when there is room.
  const sideColumn = (
    <aside
      aria-label="Worlds and cameras"
      className="flex min-h-0 shrink-0 flex-col gap-3 overflow-y-auto border-r border-border/70 p-3"
      style={{ width: SIDE_COLUMN }}
    >
      {list}
      <div className="flex flex-col gap-2 border-t border-border/70 pt-3">
        {modeToggle}
        {notExplorable}
        {mode === 'explore' ? (
          events.length ? (
            <>
              <p className="text-[10px] uppercase tracking-wide text-muted-foreground">Events</p>
              {eventButtons}
            </>
          ) : null
        ) : (
          <ul aria-label="Cameras" className="flex flex-col gap-1">
            {cameras.map((move, i) => {
              const covered = eventsInCamera(events, move);
              return (
                <li key={`${i}:${move.start}:${move.name}`} className="flex flex-col gap-0.5">
                  <button
                    type="button"
                    aria-current={i === cameraIndex ? 'true' : undefined}
                    className="min-h-8 truncate rounded-md px-2 py-1 text-left text-xs hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    style={i === cameraIndex ? { background: 'hsl(var(--primary) / 0.12)' } : undefined}
                    onClick={() => selectCamera(i)}
                  >
                    {move.name} <span className="tabular-nums text-muted-foreground">{clockText(move.start)} – {clockText(move.end)}</span>
                  </button>
                  {covered.map(({ event, from }, j) => (
                    <button
                      key={`${j}:${event.start}:${event.name}`}
                      type="button"
                      className="truncate rounded-md py-0.5 pl-5 pr-2 text-left text-[11px] text-muted-foreground hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      onClick={() => selectCamera(i, from)}
                    >
                      {event.name}
                    </button>
                  ))}
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </aside>
  );

  // Docked header: ‹ World name  2 / 5 ›, and the name opens the full list.
  const header = (
    <div className="flex flex-col gap-2">
      <div className="flex min-w-0 items-center gap-1">
        <button type="button" aria-label="Previous world" className={`${button} shrink-0`} disabled={allRows.length < 2} onClick={() => stepWorld(-1)}>‹</button>
        <button
          type="button"
          aria-label="Choose world"
          aria-expanded={listOpen}
          className={`${button} min-w-0 flex-1 truncate border border-border/70 text-left`}
          onClick={() => setListOpen((open) => !open)}
        >
          <span className="truncate">{selected?.name ?? 'Choose a world'}</span>
          {selectedIndex >= 0 ? <span className="ml-2 tabular-nums text-muted-foreground">{selectedIndex + 1} / {allRows.length}</span> : null}
        </button>
        <button type="button" aria-label="Next world" className={`${button} shrink-0`} disabled={allRows.length < 2} onClick={() => stepWorld(1)}>›</button>
      </div>
      {listOpen ? <div className="rounded-md border border-border/70 p-1">{list}</div> : null}
    </div>
  );

  return (
    <section
      ref={rootRef}
      className="flex h-full min-h-0 text-sm"
      aria-label="World Explorer"
      data-layout={wide ? 'side' : 'docked'}
      onClick={refocusViewer}
    >
      {wide && !showEmpty ? sideColumn : null}
      <div className={`flex min-h-0 min-w-0 flex-1 flex-col gap-3 p-3 ${wide ? '' : 'overflow-y-auto'}`}>
        {!wide && allRows.length > 0 ? header : null}
        {showEmpty ? (
          <div className="flex flex-col gap-3 rounded-md border border-border/70 p-3">
            <p className="text-sm text-muted-foreground">A world is a live 3D place. Look around freely, then add one of its cameras to your video.</p>
            <div className="flex flex-wrap gap-2">
              <button type="button" className={`${button} bg-primary/10 text-primary`} disabled={busy} onClick={() => { void addSample(); }}>Add {SAMPLE_LABEL} (sample)</button>
              <button type="button" className={`${button} border border-border`} disabled={busy} onClick={() => importInput.current?.click()}>Import world…</button>
            </div>
          </div>
        ) : null}
        {!wide && !showEmpty ? <div className="flex flex-wrap items-center gap-2">{modeToggle}{notExplorable}</div> : null}
        {importControl}

        {notice ? (
          <div role="status" className="flex items-start gap-2 text-[11px] text-muted-foreground" style={notice.tone === 'error' ? ERROR_STYLE : undefined}>
            <div className="min-w-0 flex-1">
              <p>{notice.text}</p>
              {notice.details ? (
                <details className="mt-1">
                  <summary className="cursor-pointer">Details</summary>
                  <p className="mt-1 break-words">{notice.details}</p>
                </details>
              ) : null}
            </div>
            <button
              type="button"
              aria-label="Dismiss"
              title="Dismiss"
              className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md text-muted-foreground hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              onClick={dismissNotice}
            >
              <svg aria-hidden="true" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
            </button>
          </div>
        ) : null}

        <div
          ref={stageRef}
          className={wide ? 'flex min-h-0 min-w-0 flex-1 items-center justify-center overflow-hidden' : 'w-full'}
          style={showEmpty ? { display: 'none' } : undefined}
        >
          <div
            ref={viewerRef}
            role="application"
            aria-label="World viewer"
            tabIndex={0}
            data-autofocus
            data-mode={mode}
            className="relative touch-none select-none overflow-hidden rounded-md border border-border/70 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-ring"
            style={{ ...VIEWER_STYLE, width: viewSize.width, height: viewSize.height, cursor: exploring ? (dragging ? 'none' : 'crosshair') : undefined }}
            onKeyDown={onViewerKeyDown}
            onKeyUp={onViewerKeyUp}
            onBlur={onViewerBlur}
            onPointerDown={onViewerPointerDown}
            onPointerMove={onViewerPointerMove}
            onPointerUp={onViewerPointerUp}
            onPointerCancel={onViewerPointerUp}
          >
            {liveScene && selected ? (
              <Suspense fallback={null}>
                <LazySceneSurface
                  key={selected.key}
                  source={liveScene}
                  sourceTime={frame.time}
                  worldTime={frame.worldTime}
                  view={frame.view}
                  width={viewSize.width}
                  height={viewSize.height}
                  showStatus={false}
                  onStatus={handleStatus}
                  onReady={handleReady}
                />
              </Suspense>
            ) : null}
            {showOverlay ? (
              <div className="absolute inset-0 grid place-items-center p-4 text-center text-xs" style={OVERLAY_STYLE}>
                {overlayIsError ? (
                  <div className="flex max-w-xs flex-col items-center gap-2">
                    <p>This world couldn&apos;t start</p>
                    <p className="text-[11px] opacity-70">{overlayText}</p>
                    <button type="button" className={`${button} border border-white/20`} onClick={retryWorld}>Try again</button>
                  </div>
                ) : overlayText}
              </div>
            ) : null}
            {exploring ? (
              <span
                aria-label="Camera speed"
                title="Scroll to change speed"
                className="absolute bottom-2 left-2 rounded-full px-2 py-0.5 text-[11px] tabular-nums"
                style={PILL_STYLE}
              >
                {speedScaleLabel(speedScale)}
              </span>
            ) : null}
            {exploring ? (
              <button
                type="button"
                data-viewer-control
                aria-label="Keys"
                aria-expanded={keysOpen}
                title="Show the key map (?)"
                className="absolute left-2 top-2 flex h-7 w-7 items-center justify-center rounded-full text-xs hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                style={PILL_STYLE}
                onClick={() => setKeysOpen((open) => !open)}
              >
                ?
              </button>
            ) : null}
            {exploring && keysOpen ? (
              <dl
                aria-label="Key map"
                data-viewer-control
                className="absolute left-2 top-11 m-0 grid grid-cols-[auto_auto] gap-x-3 gap-y-0.5 rounded-md px-3 py-2 text-[11px]"
                style={OVERLAY_STYLE}
              >
                {KEY_MAP.map((entry) => (
                  <div key={entry.keys} className="contents">
                    <dt className="whitespace-pre font-medium text-white">{entry.keys}</dt>
                    <dd className="m-0">{entry.does}</dd>
                  </div>
                ))}
              </dl>
            ) : null}
            {showHint ? (
              <div
                role="note"
                className="absolute bottom-2 right-2 flex max-w-[calc(100%-5rem)] items-center gap-1 rounded-full py-0.5 pl-3 pr-1 text-[11px] transition-opacity duration-700"
                style={{ ...PILL_STYLE, opacity: hintFading ? 0 : 1 }}
              >
                <span className="truncate">{touch ? TOUCH_HINT_TEXT : HINT_TEXT}</span>
                <button
                  type="button"
                  aria-label="Dismiss hint"
                  className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  onClick={dismissHint}
                >
                  <svg aria-hidden="true" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
                </button>
              </div>
            ) : null}
            {canExpand ? (
              <button
                type="button"
                aria-label="Pop out World Explorer"
                title="Pop out into a larger window"
                className="absolute right-2 top-2 flex h-7 w-7 items-center justify-center rounded-md hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                style={PILL_STYLE}
                onClick={() => popout!.onOpenChange(true)}
              >
                <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" /></svg>
              </button>
            ) : null}
          </div>
        </div>

        {showEmpty ? null : mode === 'explore' ? (
          <div className="flex shrink-0 flex-col gap-2" data-refocus style={wide ? { minHeight: CONTROLS_MIN_HEIGHT } : undefined}>
            <div className="flex flex-wrap items-center gap-2">
              <button type="button" className={`${button} w-16 border border-border`} disabled={!ready} onClick={toggleWorldPause}>
                {worldPaused ? 'Play' : 'Pause'}
              </button>
              <button type="button" className={`${button} border border-border`} disabled={!ready} title="Back to the start view (R)" onClick={resetView}>
                Reset view
              </button>
              <span className="ml-auto text-[11px] tabular-nums text-muted-foreground">
                World {clockText(worldTime, 1)} / {clockText(duration)}
              </span>
            </div>
            <TimeBar
              start={0}
              end={duration}
              time={worldTime}
              label="World time"
              valueText={clockText(worldTime, 1)}
              disabled={!selected}
              markers={eventMarkers}
              onSeek={seekWorld}
            />
            {!wide && events.length ? eventButtons : null}
            {ready && selected ? (
              <p className="truncate text-[11px] text-muted-foreground">To add this world to your video, <button type="button" className="underline underline-offset-2 hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-sm" onClick={() => switchMode('cameras')}>pick a camera →</button></p>
            ) : null}
          </div>
        ) : (
          <div
            role="group"
            aria-label="Camera travel"
            tabIndex={0}
            className="flex shrink-0 flex-col gap-2 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            style={wide ? { minHeight: CONTROLS_MIN_HEIGHT } : undefined}
            onKeyDown={onTravelKeyDown}
          >
            {!wide && selected && cameras.length > 1 ? (
              <Select label="Camera" value={String(cameraIndex)} onChange={(event) => selectCamera(Number(event.target.value))}>
                {cameras.map((move, i) => (
                  <option key={`${i}:${move.start}:${move.name}`} value={i} className="bg-background text-foreground">{move.name} · {clockText(move.start)} – {clockText(move.end)}</option>
                ))}
              </Select>
            ) : null}
            <div className="flex flex-wrap items-center gap-2">
              <button type="button" className={`${button} w-16 border border-border`} disabled={!ready} onClick={toggleTravel}>
                {playing ? 'Pause' : 'Play'}
              </button>
              <Select label="Speed" value={String(stretch.speed)} disabled={!selected} onChange={(event) => changeSpeed(Number(event.target.value))}>
                {speedOptions.map((speed) => <option key={speed} value={speed} className="bg-background text-foreground">{speedLabel(speed)}</option>)}
              </Select>
              <label className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <input type="checkbox" checked={loop} disabled={!selected} onChange={(event) => toggleLoop(event.target.checked)} />
                Loop
              </label>
              <span className="ml-auto text-[11px] tabular-nums text-muted-foreground">
                {clockText(shownTime, 1)} / {clockText(camera?.end ?? duration)}
              </span>
            </div>

            <TimeBar
              start={camera?.start ?? 0}
              end={camera?.end ?? duration}
              time={shownTime}
              label="Travel position"
              valueText={clockText(shownTime, 1)}
              disabled={!selected}
              markers={cameraMarkers}
              uses={(selected?.uses ?? []).map((use) => ({ key: use.clipId, from: use.from, to: use.to, title: `On ${use.track} at ${clockText(use.at)}` }))}
              range={selected ? { from: stretch.from, to: stretch.to } : undefined}
              onSeek={seekTravel}
              onRange={(next) => setStretch((current) => clampStretch({ ...current, ...next }, duration))}
            />

            {!wide && cameraEvents.length ? cameraEventButtons : null}

            {selected ? (
              <div className="flex items-center gap-2">
                <button type="button" className={`${button} border border-border`} title="Start the clip here (I)" onClick={setStartHere}>In (I)</button>
                <button type="button" className={`${button} border border-border`} title="End the clip here (O)" onClick={setEndHere}>Out (O)</button>
                <p className="min-w-0 flex-1 truncate text-[11px] tabular-nums text-muted-foreground">
                  {clockText(stretch.from, 1)}–{clockText(stretch.to, 1)} · {Number(stretchDuration(stretch).toFixed(1))} s{stretch.speed === 1 ? '' : ` at ${speedLabel(stretch.speed)}`}
                </p>
                {followedUse ? (
                  <>
                    <button
                      type="button"
                      className={`${button} shrink-0 hover:text-foreground text-muted-foreground`}
                      disabled={Boolean(addReason)}
                      title={addReason ?? 'Add this range to the video as a new clip at the playhead'}
                      onClick={() => { void addToVideo(); }}
                    >
                      Add as new
                    </button>
                    <button
                      type="button"
                      className={`${button} shrink-0 bg-primary/10 text-primary`}
                      disabled={!followedDiffers || busy}
                      title={followedDiffers ? 'Write this range back to the clip' : 'The clip already matches'}
                      onClick={() => { void updateClip(); }}
                    >
                      Update clip
                    </button>
                  </>
                ) : (
                  <button
                    type="button"
                    className={`${button} shrink-0 bg-primary/10 text-primary`}
                    disabled={Boolean(addReason)}
                    title={addReason ?? 'Add this range to the video at the playhead'}
                    onClick={() => { void addToVideo(); }}
                  >
                    Add to video
                  </button>
                )}
              </div>
            ) : null}
            <p className="min-h-4 text-[11px] text-muted-foreground">
              {followedUse ? `Editing clip on ${followedUse.track} at ${clockText(followedUse.at)}` : addReason}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

export default WorldExplorerPanel;
