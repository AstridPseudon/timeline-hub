import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { EDITOR_TOUR_ANCHORS, EDITOR_TOUR_TRACK_IDS, editorTourSelector, editorTourTrackSelector } from '../anchors';
import { UI_Z_LAYERS } from '@/shared/lib/uiLayers';
import { useEditorTour, type EditorTourAct, type EditorTourBeat } from '@/shared/state/editorTourStore';
import { TourCard } from '../card/TourCard';
import { TourSpotlight } from './TourSpotlight';
import { placeCard } from './cardPlacement';
import { backEditorTour, finishEditorTour, runEditorTourPrimary, watchEditorTourSend } from './tourBeats';
import { useSpotlightRects } from './useSpotlightRects';
import { useTourKeys } from './useTourKeys';

const ACT_TRACK: Record<EditorTourAct, string> = {
  1: EDITOR_TOUR_TRACK_IDS.scene,
  2: EDITOR_TOUR_TRACK_IDS.stills,
  3: EDITOR_TOUR_TRACK_IDS.videos,
};

/** What each beat spotlights: chat composer and Send, the transcript, the act's new row with the preview, or nothing (the welcome and the finale, centred). */
export function editorTourTargets(act: EditorTourAct, beat: EditorTourBeat): string[] {
  switch (beat) {
    case 'compose':
      return [editorTourSelector(EDITOR_TOUR_ANCHORS.chatComposer)];
    case 'respond':
      return [editorTourSelector(EDITOR_TOUR_ANCHORS.chatTranscript)];
    case 'land':
      return [editorTourTrackSelector(ACT_TRACK[act]), editorTourSelector(EDITOR_TOUR_ANCHORS.preview)];
    case 'welcome':
    case 'finale':
      return [];
  }
}

/**
 * The running tour's overlay: keys, spotlight with input shield, and the card beside it.
 * Registered in the editor page's tour slot (`useEditorTourHost`), which mounts it only while the tour
 * runs, so it is mounted exactly for the length of a run.
 */
export function EditorTourRunner() {
  useEffect(() => watchEditorTourSend(), []);
  useEndTourOnUnmount();
  useTourKeys(true);
  // On <body>, not inside the page: the page's own stacking context sits below the panes (the Tasks pane chat).
  return createPortal(<RunningTour />, document.body);
}

/** Leaving the page mid-tour ends it. Deferred a tick so a StrictMode remount does not. */
function useEndTourOnUnmount(): void {
  const mounted = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      setTimeout(() => { if (!mounted.current) finishEditorTour(); }, 0);
    };
  }, []);
}

function RunningTour() {
  const act = useEditorTour((s) => s.act);
  const beat = useEditorTour((s) => s.beat);
  const reducedMotion = useEditorTour((s) => s.reducedMotion);
  const rects = useSpotlightRects(editorTourTargets(act, beat));
  // The Send button is the one thing outside the card the user may press.
  const sendRects = useSpotlightRects(beat === 'compose' ? [editorTourSelector(EDITOR_TOUR_ANCHORS.chatSend)] : []);
  const cardRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 360, height: 160 });

  useLayoutEffect(() => {
    const card = cardRef.current;
    if (!card) return;
    const observer = new ResizeObserver(() => setSize({ width: card.offsetWidth, height: card.offsetHeight }));
    observer.observe(card);
    return () => observer.disconnect();
  }, []);

  const position = placeCard(rects, size, { width: window.innerWidth, height: window.innerHeight });
  return (
    <>
      <TourSpotlight rects={rects} clickable={sendRects[0] ?? null} reducedMotion={reducedMotion} />
      <div
        ref={cardRef}
        data-editor-tour-card-host
        className="fixed"
        style={{ zIndex: UI_Z_LAYERS.EDITOR_TOUR_CARD, left: position.left, top: position.top, transition: reducedMotion ? 'none' : 'left 420ms cubic-bezier(0.22, 1, 0.36, 1), top 420ms cubic-bezier(0.22, 1, 0.36, 1)' }}
      >
        <TourCard onPrimary={runEditorTourPrimary} onBack={backEditorTour} onSkip={finishEditorTour} />
      </div>
    </>
  );
}
