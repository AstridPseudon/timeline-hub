import { Suspense, lazy, useEffect, useRef, useState } from 'react';
import {
  editorTourStage,
  getEditorTourState,
  markEditorTourReady,
  useEditorTour,
  type EditorTourStage,
} from '@/shared/state/editorTourStore.ts';
import {
  useTimelineDataSelector,
  useTimelineMutableAdapters,
  useTimelineOpsFromStore,
} from '@/tools/video-editor/hooks/timelineStore.ts';
import { requestCenterTimelineClip } from '@/tools/video-editor/lib/timeline-viewport-events.ts';
import { editorTourTrackSelector } from '@/tools/video-editor/tour/anchors.ts';
import { loadTourLiveScene, TOUR_SCENE_SOURCE_FROM } from './tourSceneSource.ts';
import { createEditorTourStagePatch, createEditorTourStageRemovalPatch, tourStageFocusClipId, tourTrackOrder, TOUR_ANCHORS, TOUR_CLIP_IDS } from './tourStages.ts';

const SceneSurface = lazy(() => import('@astrid/packs/rendering/ui/threejs-live-editor/SceneSurface')
  .then((module) => ({ default: module.SceneSurface })));

const RENDER_WAIT_MS = 3000;
export const TOUR_ANCHOR_DWELL_MS = 1200;
const WARMUP_GIVE_UP_MS = 8000;
/** The longest `land` waits for the visible scene's first painted frame before showing the card over it anyway. */
const SCENE_READY_GIVE_UP_MS = 8000;
/** The visible live scene reports its phase on this element (the warm-up's `onReady` is the same signal). */
const SCENE_READY_SELECTOR = '[data-testid="astrid-live-scene-entry"][data-phase="ready"]';

function nextFrame(): Promise<void> {
  return new Promise((resolve) => requestAnimationFrame(() => resolve()));
}

/** Resolves once `check` is true on a frame, or after `timeoutMs` (the tour must never stall on a slow render). */
async function waitFor(check: () => boolean, timeoutMs: number, isCancelled: () => boolean): Promise<void> {
  const deadline = performance.now() + timeoutMs;
  while (!isCancelled() && !check() && performance.now() < deadline) await nextFrame();
}

/**
 * While beat 1 `respond` plays the scene is not on the timeline yet, so a hidden copy boots in an
 * invisible iframe; the real clip then lands on a browser that has already compiled the world.
 */
function SceneWarmup({ liveScene, onWarm }: { liveScene: Record<string, unknown>; onWarm: () => void }) {
  return (
    <div
      aria-hidden
      className="pointer-events-none fixed bottom-0 right-0 -z-10 h-[180px] w-[320px] overflow-hidden opacity-0"
    >
      <Suspense fallback={null}>
        <SceneSurface
          source={liveScene}
          sourceTime={TOUR_SCENE_SOURCE_FROM}
          width={320}
          height={180}
          onReady={onWarm}
        />
      </Suspense>
    </div>
  );
}

/**
 * Lives inside the tour's editor and takes the demo timeline to the tour's stage through the editor's
 * own ops (`track.add`, `clip.add`, `clip.update`), then presents it: scroll the new row into view,
 * and on each `land` beat play the 14 s from the start (act 2 presents each reference frame, then holds the last).
 * Reports `ready.timeline` per beat.
 */
export function EditorTourTimelineDriver() {
  const runId = useEditorTour((state) => state.runId);
  const act = useEditorTour((state) => state.act);
  const beat = useEditorTour((state) => state.beat);
  const stage = editorTourStage(act, beat);
  const ops = useTimelineOpsFromStore();
  const { previewRef } = useTimelineMutableAdapters();
  const loaded = useTimelineDataSelector((data) => !data.isLoading && data.data !== null);
  const [appliedStage, setAppliedStage] = useState<EditorTourStage>(0);
  const [liveScene, setLiveScene] = useState<Record<string, unknown> | null>(null);
  const [warm, setWarm] = useState(false);
  const [sceneLoadAttempt, setSceneLoadAttempt] = useState(0);
  const [sceneLoadError, setSceneLoadError] = useState(false);
  const [retry, setRetry] = useState(0);
  const applying = useRef(false);

  // The world loads as soon as the tour mounts, well before the first `land` beat needs it.
  useEffect(() => {
    let active = true;
    setSceneLoadError(false);
    loadTourLiveScene().then(
      (scene) => { if (active) setLiveScene(scene); },
      () => { if (active) setSceneLoadError(true); },
    );
    return () => { active = false; };
  }, [sceneLoadAttempt]);

  useEffect(() => {
    if (!loaded || !ops || applying.current) return;
    if (appliedStage > stage) {
      // Back: the later acts' rows leave at once, one stage at a time (a move back is never more than one).
      applying.current = true;
      try {
        ops.apply(createEditorTourStageRemovalPatch(appliedStage as 1 | 2 | 3));
        setAppliedStage((appliedStage - 1) as EditorTourStage);
      } catch (error) {
        console.error('Editor tour: could not step the demo timeline back; retrying.', error);
        window.setTimeout(() => setRetry((count) => count + 1), 250);
      } finally {
        applying.current = false;
      }
      return;
    }
    if (!liveScene || appliedStage >= stage) return;
    applying.current = true;
    const next = (appliedStage + 1) as 1 | 2 | 3;
    try {
      ops.apply(createEditorTourStagePatch(next, liveScene));
      setAppliedStage(next);
    } catch (error) {
      console.error('Editor tour: could not apply the demo timeline stage; retrying.', error);
      window.setTimeout(() => setRetry((count) => count + 1), 250);
    } finally {
      applying.current = false;
    }
  }, [loaded, ops, liveScene, stage, appliedStage, retry]);

  const instant = useEditorTour((state) => state.instant);
  const warming = act === 1 && beat === 'respond' && appliedStage === 0 && !instant;
  useEffect(() => {
    if (!warming) return;
    const timer = window.setTimeout(() => setWarm(true), WARMUP_GIVE_UP_MS);
    return () => window.clearTimeout(timer);
  }, [warming]);

  useEffect(() => {
    if (!loaded || appliedStage !== stage) return;
    let cancelled = false;
    const isCancelled = () => {
      const current = getEditorTourState();
      return cancelled || current.status !== 'running' || current.runId !== runId || current.act !== act || current.beat !== beat;
    };
    void (async () => {
      if (beat === 'respond' && act === 1 && !instant) await waitFor(() => warm, WARMUP_GIVE_UP_MS, isCancelled);
      if (beat === 'land') {
        const topTrack = tourTrackOrder(stage)[0];
        await waitFor(
          () => document.querySelector(editorTourTrackSelector(topTrack)) !== null,
          RENDER_WAIT_MS,
          isCancelled,
        );
        if (isCancelled()) return;
        await waitFor(() => previewRef.current !== null, RENDER_WAIT_MS, isCancelled);
        if (isCancelled()) return;
        // Pause before seeking so an earlier act's playback cannot overwrite the new position.
        previewRef.current?.pause();
        if (act === 2) {
          const skipped = getEditorTourState().skipAnimation;
          const anchors = instant ? [TOUR_ANCHORS.length - 1] : TOUR_ANCHORS.map((_, index) => index);
          for (const index of anchors) {
            if (isCancelled() || getEditorTourState().skipAnimation !== skipped) break;
            requestCenterTimelineClip(TOUR_CLIP_IDS.stills[index]);
            previewRef.current?.seek(TOUR_ANCHORS[index].at);
            if (!instant) await waitFor(
              () => getEditorTourState().skipAnimation !== skipped,
              TOUR_ANCHOR_DWELL_MS,
              isCancelled,
            );
          }
        } else {
          const focusClipId = tourStageFocusClipId(stage);
          if (focusClipId) requestCenterTimelineClip(focusClipId);
          previewRef.current?.seek(0);
          // Wait for the first painted world frame before playing the flight.
          if (act === 1 && !instant) {
            const skipped = getEditorTourState().skipAnimation;
            await waitFor(
              () => document.querySelector(SCENE_READY_SELECTOR) !== null || getEditorTourState().skipAnimation !== skipped,
              SCENE_READY_GIVE_UP_MS,
              isCancelled,
            );
          }
          if (!isCancelled()) previewRef.current?.play();
        }
      }
      if (!isCancelled()) markEditorTourReady('timeline');
    })();
    return () => { cancelled = true; };
  }, [runId, act, beat, stage, appliedStage, loaded, warm, instant, previewRef]);

  if (sceneLoadError) return (
    <div role="alert" className="fixed bottom-6 left-1/2 z-[2147483647] flex -translate-x-1/2 items-center gap-3 rounded-lg border bg-background p-4 text-sm text-foreground shadow-lg">
      <span>The Lantern Valley demo could not load. Check your connection and try again.</span>
      <button type="button" className="shrink-0 rounded-md bg-primary px-3 py-2 text-primary-foreground" onClick={() => setSceneLoadAttempt((count) => count + 1)}>Retry demo</button>
    </div>
  );
  return warming && liveScene ? <SceneWarmup liveScene={liveScene} onWarm={() => setWarm(true)} /> : null;
}
