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
import { createEditorTourStagePatch, tourStageFocusClipId, tourTrackOrder } from './tourStages.ts';

const SceneSurface = lazy(() => import('@astrid/packs/rendering/ui/threejs-live-editor/SceneSurface')
  .then((module) => ({ default: module.SceneSurface })));

const RENDER_WAIT_MS = 3000;
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
 * and on each `land` beat play the 10 s from the start (act 2 holds on its start frame instead).
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
  const [retry, setRetry] = useState(0);
  const applying = useRef(false);

  // The world loads as soon as the tour mounts, well before the first `land` beat needs it.
  useEffect(() => {
    let active = true;
    loadTourLiveScene().then((scene) => { if (active) setLiveScene(scene); }, () => undefined);
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!loaded || !ops || !liveScene || applying.current || appliedStage >= stage) return;
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

  const warming = act === 1 && beat === 'respond' && appliedStage === 0;
  useEffect(() => {
    if (!warming) return;
    const timer = window.setTimeout(() => setWarm(true), WARMUP_GIVE_UP_MS);
    return () => window.clearTimeout(timer);
  }, [warming]);

  useEffect(() => {
    if (!loaded || appliedStage < stage) return;
    let cancelled = false;
    const isCancelled = () => cancelled;
    void (async () => {
      if (beat === 'respond' && act === 1) await waitFor(() => warm, WARMUP_GIVE_UP_MS, isCancelled);
      if (beat === 'land') {
        const topTrack = tourTrackOrder(stage)[0];
        await waitFor(
          () => document.querySelector(editorTourTrackSelector(topTrack)) !== null,
          RENDER_WAIT_MS,
          isCancelled,
        );
        const focusClipId = tourStageFocusClipId(stage);
        if (focusClipId) requestCenterTimelineClip(focusClipId);
        await waitFor(() => previewRef.current !== null, RENDER_WAIT_MS, isCancelled);
        // Pause before seeking: a seek issued while the previous act is still playing doesn't stick.
        previewRef.current?.pause();
        previewRef.current?.seek(0);
        // The scene lands first: hold at 0 until its first frame is painted (an Enter during the wait skips it),
        // so the card never shows over an empty preview and the moonrise plays from its start.
        if (act === 1) {
          const skipped = getEditorTourState().skipAnimation;
          await waitFor(
            () => document.querySelector(SCENE_READY_SELECTOR) !== null || getEditorTourState().skipAnimation !== skipped,
            SCENE_READY_GIVE_UP_MS,
            isCancelled,
          );
        }
        // Act 2's result is the start frame, which holds for the first second only: stay on it, paused.
        if (act !== 2) previewRef.current?.play();
      }
      if (!cancelled) markEditorTourReady('timeline');
    })();
    return () => { cancelled = true; };
  }, [runId, act, beat, stage, appliedStage, loaded, warm, previewRef]);

  return warming && liveScene ? <SceneWarmup liveScene={liveScene} onWarm={() => setWarm(true)} /> : null;
}
