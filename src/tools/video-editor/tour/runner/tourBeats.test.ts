import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  editorTourStage,
  exitEditorTour,
  getEditorTourState,
  markEditorTourReady,
  setEditorTourBeat,
  startEditorTour,
} from '@/shared/state/editorTourStore';
import { finishEditorTour, runEditorTourPrimary, watchEditorTourSend } from './tourBeats';
import { beginEditorTour, hasSeenEditorTour, startEditorTourIfFirstRun } from './tourFlag';

let stopWatching: (() => void) | undefined;

beforeEach(() => {
  exitEditorTour();
  localStorage.clear();
  stopWatching = watchEditorTourSend();
  startEditorTour();
  passWelcome();
});

afterEach(() => {
  stopWatching?.();
  stopWatching = undefined;
  exitEditorTour();
  localStorage.clear();
});

/** The welcome card has played its entrance and the user pressed OK. */
function passWelcome() {
  markEditorTourReady('card');
  runEditorTourPrimary();
}

/** Presents the current beat as the parts would: the chat sets its flag, the timeline and card set theirs. */
function readyChat() {
  markEditorTourReady('chat');
}
function readyLand() {
  markEditorTourReady('timeline');
  markEditorTourReady('card');
}

describe('tour beat machine', () => {
  it('opens on the welcome, which waits for its card and then goes to act 1 compose', () => {
    startEditorTour();
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'welcome' });

    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ beat: 'welcome', skipAnimation: 1 });

    markEditorTourReady('card');
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'compose', sent: false });
  });

  it('waits for the chat to be ready before Send is accepted in compose', () => {
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'compose', sent: false });

    runEditorTourPrimary();

    expect(getEditorTourState()).toMatchObject({ beat: 'compose', sent: false, skipAnimation: 1 });
  });

  it('sends on primary once the chat is ready, and the watcher moves compose on to respond', () => {
    readyChat();
    runEditorTourPrimary();

    // Send reset by the respond beat change; the watcher did the move.
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'respond', sent: false, ready: { chat: false } });
  });

  it('keeps respond until the chat is ready, then lands on primary', () => {
    readyChat();
    runEditorTourPrimary();
    expect(getEditorTourState().beat).toBe('respond');

    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ beat: 'respond', skipAnimation: 1 });

    readyChat();
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'land' });
  });

  it('requires both timeline and card before land advances', () => {
    readyChat();
    runEditorTourPrimary();
    readyChat();
    runEditorTourPrimary();
    expect(getEditorTourState().beat).toBe('land');

    markEditorTourReady('timeline');
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ act: 1, beat: 'land' });

    markEditorTourReady('card');
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ act: 2, beat: 'compose', sent: false });
  });

  it('plays the whole three-act journey and ends on finale primary', () => {
    const stages: number[] = [];
    for (const act of [1, 2, 3] as const) {
      // compose: send, then respond: chat ready, then land
      expect(getEditorTourState()).toMatchObject({ act, beat: 'compose' });
      readyChat();
      runEditorTourPrimary();
      expect(getEditorTourState()).toMatchObject({ act, beat: 'respond' });
      readyChat();
      runEditorTourPrimary();
      expect(getEditorTourState()).toMatchObject({ act, beat: 'land' });
      readyLand();
      stages.push(editorTourStage(act, 'land'));
      runEditorTourPrimary();
    }

    // After act 3 lands, the next primary goes to finale, not a fourth compose.
    expect(getEditorTourState()).toMatchObject({ act: 3, beat: 'finale' });
    expect(stages).toEqual([1, 2, 3]);

    // finale waits on card readiness
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ beat: 'finale', status: 'running' });

    markEditorTourReady('card');
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ status: 'idle' });
  });

  it('Esc finishes the tour from every beat', () => {
    const beats = [
      [1, 'welcome'],
      [1, 'compose'],
      [1, 'respond'],
      [2, 'land'],
      [3, 'finale'],
    ] as const;
    for (const [act, beat] of beats) {
      startEditorTour();
      setEditorTourBeat(act, beat);
      finishEditorTour();
      expect(getEditorTourState().status).toBe('idle');
    }
  });

  it('exit focuses the real composer, never the tour\'s read-only one', async () => {
    vi.stubGlobal('requestAnimationFrame', (cb: FrameRequestCallback) => setTimeout(() => cb(0), 0));
    document.body.innerHTML = '<textarea id="tour" data-editor-tour="chat-composer" readonly></textarea>';

    finishEditorTour();
    // The tour's composer unmounts and the real one mounts a frame or two later.
    setTimeout(() => {
      document.body.innerHTML = '<div data-editor-tour="chat-composer"><textarea id="real"></textarea></div>';
    }, 5);

    await vi.waitFor(() => expect(document.activeElement?.id).toBe('real'));
    document.body.innerHTML = '';
    vi.unstubAllGlobals();
  });

  it('finishing while idle is a no-op', () => {
    exitEditorTour();
    const before = getEditorTourState();

    finishEditorTour();
    runEditorTourPrimary();

    expect(getEditorTourState()).toBe(before);
  });

  it('a reload mid-tour leaves the seen flag set and does not restart the tour', () => {
    // Start from a fresh first run: the beforeEach already started a tour, which would block the trigger.
    exitEditorTour();
    localStorage.clear();
    expect(startEditorTourIfFirstRun(true)).toBe(true);
    setEditorTourBeat(2, 'land');
    expect(hasSeenEditorTour()).toBe(true);

    // The page reloads: the in-memory store is back to idle.
    exitEditorTour();

    expect(hasSeenEditorTour()).toBe(true);
    expect(startEditorTourIfFirstRun(true)).toBe(false);
    expect(getEditorTourState().status).toBe('idle');
  });

  it('replay starts a larger run at the welcome', () => {
    readyChat();
    runEditorTourPrimary();
    readyChat();
    runEditorTourPrimary();
    readyLand();
    runEditorTourPrimary();
    expect(getEditorTourState()).toMatchObject({ act: 2, beat: 'compose' });
    const firstRun = getEditorTourState().runId;

    beginEditorTour();

    expect(getEditorTourState()).toMatchObject({
      runId: firstRun + 1,
      status: 'running',
      act: 1,
      beat: 'welcome',
      sent: false,
      ready: { chat: false, timeline: false, card: false },
    });
  });
});
