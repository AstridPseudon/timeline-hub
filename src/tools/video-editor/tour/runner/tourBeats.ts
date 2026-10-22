import { buildEditorTourRecord, recordEditorTour } from './tourRecord';
import { EDITOR_TOUR_ANCHORS, editorTourSelector } from '../anchors';
import {
  exitEditorTour,
  getEditorTourState,
  markEditorTourSent,
  setEditorTourBeat,
  skipEditorTourAnimation,
  subscribeEditorTour,
  type EditorTourState,
} from '@/shared/state/editorTourStore';

/**
 * The beat machine, and the only writer of `act`/`beat`.
 *   welcome -(OK)-> compose -(sent)-> respond -(Next)-> land -(Next)-> next act's compose ... -> finale -(I got it)-> exit
 * Acts 2 and 3 pass through respond on their own: once the reply has played, it moves on after a short hold.
 * Back returns to the previous place where the user acted (see `backEditorTour`).
 */

/** How long a finished reply holds on acts 2 and 3 before the tour moves on to `land`. */
export const RESPOND_HOLD_MS = 600;

const LAST_ACT = 3;

/** Whether the parts that present the current beat have finished animating. */
export function isEditorTourBeatReady({ beat, ready }: EditorTourState): boolean {
  switch (beat) {
    case 'compose':
    case 'respond':
      return ready.chat;
    case 'land':
      return ready.timeline && ready.card;
    case 'welcome':
    case 'finale':
      return ready.card;
  }
}

function advanceBeat(): void {
  const { act, beat } = getEditorTourState();
  if (beat === 'welcome') return setEditorTourBeat(1, 'compose');
  if (beat === 'compose') return; // leaves only when the composer's Send is pressed
  if (beat === 'respond') return setEditorTourBeat(act, 'land');
  if (beat === 'land') {
    return act < LAST_ACT ? setEditorTourBeat((act + 1) as typeof LAST_ACT, 'compose') : setEditorTourBeat(LAST_ACT, 'finale');
  }
  finishEditorTour();
}

/** Enter, and the card's OK / Next / "I got it" button: finish the animation first, then act. */
export function runEditorTourPrimary(): void {
  const state = getEditorTourState();
  if (state.status !== 'running') return;
  if (!isEditorTourBeatReady(state)) return skipEditorTourAnimation();
  if (state.beat === 'compose') {
    if (!state.sent) markEditorTourSent();
    return;
  }
  advanceBeat();
}

/**
 * ArrowLeft, Backspace and the card's Back: return to the previous place the user acted, with the beat
 * already finished (`instant`). Respond on acts 2 and 3 is never a place to return to, and welcome has no Back.
 */
export function backEditorTour(): void {
  const { status, act, beat } = getEditorTourState();
  if (status !== 'running') return;
  const previousAct = (act - 1) as typeof LAST_ACT;
  switch (beat) {
    case 'welcome':
      return;
    case 'compose':
      return act === 1 ? setEditorTourBeat(1, 'welcome', true) : setEditorTourBeat(previousAct, 'land', true);
    case 'respond':
      return setEditorTourBeat(act, 'compose', true);
    case 'land':
      return act === 1 ? setEditorTourBeat(1, 'respond', true) : setEditorTourBeat(act, 'compose', true);
    case 'finale':
      return setEditorTourBeat(LAST_ACT, 'land', true);
  }
}

/**
 * Esc, Skip, leaving the page, and the end of the finale: leave the tour and hand the user their own chat.
 * Ending at the finale is "completed"; ending anywhere earlier is "skipped". Either is recorded with where it ended.
 */
export function finishEditorTour(): void {
  const { status, act, beat } = getEditorTourState();
  if (status !== 'running') return;
  exitEditorTour();
  void recordEditorTour(buildEditorTourRecord(beat === 'finale' ? 'completed' : 'skipped', act, beat));
  focusRealComposer();
}

const FOCUS_WAIT_MS = 5000;

/**
 * The real chat remounts after the tour's own unmounts and may enable its composer only once it has
 * connected, so look again every frame for a few seconds. The tour's composer is read-only: never focus it.
 */
function focusRealComposer(deadline = Date.now() + FOCUS_WAIT_MS): void {
  if (typeof document === 'undefined') return;
  requestAnimationFrame(() => {
    const host = document.querySelector<HTMLElement>(editorTourSelector(EDITOR_TOUR_ANCHORS.chatComposer));
    const fieldSelector = 'textarea:not([readonly]):not([disabled]), input:not([readonly]):not([disabled]), [contenteditable="true"]';
    const field = host?.matches(fieldSelector) ? host : host?.querySelector<HTMLElement>(fieldSelector);
    if (field) return field.focus();
    if (Date.now() < deadline) focusRealComposer(deadline);
  });
}

/** Sending moves compose on to respond. Returns the unsubscribe. */
function watchEditorTourSendOnly(): () => void {
  return subscribeEditorTour((state) => {
    if (state.status === 'running' && state.beat === 'compose' && state.sent) {
      setEditorTourBeat(state.act, 'respond');
    }
  });
}

/**
 * On acts 2 and 3 a finished reply moves on to `land` by itself after RESPOND_HOLD_MS. The timer belongs
 * to one run/act/beat: any other state (a beat change, Back, Skip, exit) clears it, so it never fires late.
 */
function watchEditorTourAutoAdvance(): () => void {
  let timer: number | null = null;
  let armedKey: string | null = null;
  const disarm = () => {
    if (timer !== null) window.clearTimeout(timer);
    timer = null;
    armedKey = null;
  };
  const unsubscribe = subscribeEditorTour((state) => {
    const wanted = state.status === 'running' && state.beat === 'respond' && state.act > 1 && state.ready.chat
      ? `${state.runId}:${state.act}` : null;
    if (wanted === armedKey) return;
    disarm();
    if (wanted === null) return;
    armedKey = wanted;
    timer = window.setTimeout(() => {
      timer = null;
      armedKey = null;
      const now = getEditorTourState();
      if (now.status === 'running' && now.beat === 'respond' && `${now.runId}:${now.act}` === wanted) advanceBeat();
    }, RESPOND_HOLD_MS);
  });
  return () => { disarm(); unsubscribe(); };
}

/** The runner's watchers: Send moves compose on, and a finished reply on acts 2 and 3 moves on by itself. Returns the unsubscribe. */
export function watchEditorTourSend(): () => void {
  const stops = [watchEditorTourSendOnly(), watchEditorTourAutoAdvance()];
  return () => stops.forEach((stop) => stop());
}
