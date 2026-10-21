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
 */

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

/** Esc, and the end of the finale: leave the tour and hand the user their own chat. */
export function finishEditorTour(): void {
  if (getEditorTourState().status !== 'running') return;
  exitEditorTour();
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
export function watchEditorTourSend(): () => void {
  return subscribeEditorTour((state) => {
    if (state.status === 'running' && state.beat === 'compose' && state.sent) {
      setEditorTourBeat(state.act, 'respond');
    }
  });
}
