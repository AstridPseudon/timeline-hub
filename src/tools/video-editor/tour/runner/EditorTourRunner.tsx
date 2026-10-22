import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { EDITOR_TOUR_ANCHORS, EDITOR_TOUR_TRACK_IDS, editorTourSelector, editorTourTrackSelector } from '../anchors';
import { UI_Z_LAYERS } from '@/shared/lib/uiLayers';
import { useEditorTour, type EditorTourAct, type EditorTourBeat } from '@/shared/state/editorTourStore';
import { TourCard } from '../card/TourCard';
import { TourSpotlight } from './TourSpotlight';
import { backEditorTour, finishEditorTour, runEditorTourPrimary, watchEditorTourSend } from './tourBeats';
import { placeCard } from './cardPlacement';
import { useSettledRects } from './useSettledRects';
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
  const runId = useEditorTour((s) => s.runId);
  const beatKey = `${runId}:${act}:${beat}`;
  // The card and spotlight show the beat whose targets have settled; it trails the store's beat by a frame or two.
  const settled = useSettledRects(beatKey, useSpotlightRects(editorTourTargets(act, beat)));
  const [, shownAct, shownBeat] = settled.beatKey.split(':') as [string, `${EditorTourAct}`, EditorTourBeat];
  const pending = settled.beatKey !== beatKey;
  // The Send button is the one thing outside the card the user may press.
  const sendRects = useSpotlightRects(beat === 'compose' ? [editorTourSelector(EDITOR_TOUR_ANCHORS.chatSend)] : []);
  const cardRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 360, height: 160 });

  // The shown beat swaps the card's content and size. Read the new size before paint, so the move starts
  // toward the spot for the new card and the content changes as the card starts to move.
  useLayoutEffect(() => {
    const card = cardRef.current;
    if (!card) return;
    setSize((previous) => (previous.width === card.offsetWidth && previous.height === card.offsetHeight ? previous : { width: card.offsetWidth, height: card.offsetHeight }));
  }, [settled.beatKey]);

  // Later size changes within a beat (content loading in).
  useLayoutEffect(() => {
    const card = cardRef.current;
    if (!card) return;
    const observer = new ResizeObserver(() => setSize((previous) => (previous.width === card.offsetWidth && previous.height === card.offsetHeight ? previous : { width: card.offsetWidth, height: card.offsetHeight })));
    observer.observe(card);
    return () => observer.disconnect();
  }, []);

  const position = placeCard(settled.value, size, { width: window.innerWidth, height: window.innerHeight });
  return (
    <>
      <TourSpotlight rects={settled.value} clickable={sendRects[0] ?? null} reducedMotion={reducedMotion} />
      <div
        ref={cardRef}
        data-editor-tour-card-host
        className="fixed left-0 top-0"
        style={{
          zIndex: UI_Z_LAYERS.EDITOR_TOUR_CARD,
          transform: `translate3d(${position.left}px, ${position.top}px, 0)`,
          willChange: 'transform',
          transition: reducedMotion || !settled.animate ? 'none' : 'transform 450ms cubic-bezier(0.22, 1, 0.36, 1)',
          // Between the store's beat changing and the card showing it, the old card's buttons would act on the new beat.
          pointerEvents: pending ? 'none' : undefined,
        }}
      >
        <TourCard act={Number(shownAct) as EditorTourAct} beat={shownBeat} onPrimary={runEditorTourPrimary} onBack={backEditorTour} onSkip={finishEditorTour} />
      </div>
    </>
  );
}
