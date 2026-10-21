import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { TourCard } from './TourCard';
import { TOUR_CARD_ENTRANCE_MS } from './useTourCardEntrance';
import { EDITOR_TOUR_SCRIPT as SCRIPT } from '../tourScript';
import {
  exitEditorTour,
  getEditorTourState,
  setEditorTourBeat,
  skipEditorTourAnimation,
  startEditorTour,
  type EditorTourAct,
  type EditorTourBeat,
} from '@/shared/state/editorTourStore';

const play = vi.fn(() => Promise.resolve());
const cardReady = () => getEditorTourState().ready.card;

function renderAt(tourAct: EditorTourAct, beat: EditorTourBeat, options: { reducedMotion?: boolean; onSkip?: () => void } = {}) {
  const { reducedMotion = false } = options;
  const onSkip = 'onSkip' in options ? options.onSkip : vi.fn();
  vi.spyOn(window, 'matchMedia').mockImplementation((query) => ({ matches: reducedMotion, media: query } as MediaQueryList));
  startEditorTour();
  setEditorTourBeat(tourAct, beat);
  const onPrimary = vi.fn();
  const view = render(<TourCard onPrimary={onPrimary} onSkip={onSkip} />);
  return { ...view, onPrimary, onSkip };
}

const advance = (ms: number) => act(() => { vi.advanceTimersByTime(ms); });

beforeEach(() => {
  vi.useFakeTimers();
  vi.spyOn(HTMLMediaElement.prototype, 'play').mockImplementation(play);
  vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => undefined);
});

afterEach(() => {
  exitEditorTour();
  vi.useRealTimers();
  vi.restoreAllMocks();
  play.mockClear();
});

describe('TourCard', () => {
  it('opens with Astrid\'s welcome and reports ready once its entrance has played', () => {
    const { onPrimary, onSkip } = renderAt(1, 'welcome');
    expect(screen.getByRole('heading')).toHaveTextContent(SCRIPT.welcome.title);
    expect(screen.getByText(SCRIPT.welcome.body)).toBeInTheDocument();
    expect(screen.queryByRole('list')).toBeNull();
    advance(TOUR_CARD_ENTRANCE_MS - 1);
    expect(cardReady()).toBe(false);
    advance(1);
    expect(cardReady()).toBe(true);
    fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${SCRIPT.welcome.action}`) }));
    fireEvent.click(screen.getByRole('button', { name: /Skip tour/ }));
    expect(onPrimary).toHaveBeenCalledTimes(1);
    expect(onSkip).toHaveBeenCalledTimes(1);
  });

  it('on compose shows a quiet hint and never reports ready', () => {
    renderAt(1, 'compose');
    expect(screen.getByText(SCRIPT.hints.compose)).toBeInTheDocument();
    expect(screen.getByText('1 of 3')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Next/ })).toBeNull();
    advance(TOUR_CARD_ENTRANCE_MS * 2);
    expect(cardReady()).toBe(false);
  });

  it('on respond offers the reply its Next', () => {
    const { onPrimary } = renderAt(2, 'respond');
    expect(screen.getByText(SCRIPT.hints.respond)).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Next/ }));
    expect(onPrimary).toHaveBeenCalledTimes(1);
    advance(TOUR_CARD_ENTRANCE_MS * 2);
    expect(cardReady()).toBe(false);
  });

  it.each([1, 2, 3] as const)('explains act %i on land and reports ready once its entrance has played', (tourAct) => {
    const { onPrimary, onSkip, container } = renderAt(tourAct, 'land');
    const { title, body, labels } = SCRIPT.acts[tourAct].card;
    expect(screen.getByRole('heading')).toHaveTextContent(`${tourAct} · ${title}`);
    expect(screen.getByText(body)).toBeInTheDocument();
    for (const label of labels) expect(screen.getAllByText(label).length).toBeGreaterThan(0);
    for (const step of SCRIPT.strip) expect(screen.getAllByText(step).length).toBeGreaterThan(0);
    // The strip fills act by act: one thumbnail per step reached.
    expect(container.querySelectorAll('ol img, ol video')).toHaveLength(tourAct);

    expect(container.querySelector('.editor-tour-card-playing')).not.toBeNull();
    advance(TOUR_CARD_ENTRANCE_MS - 1);
    expect(cardReady()).toBe(false);
    advance(1);
    expect(cardReady()).toBe(true);
    expect(container.querySelector('[data-settled]')).not.toBeNull();
    expect(container.querySelector('.editor-tour-card-playing')).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: /Next/ }));
    fireEvent.click(screen.getByRole('button', { name: /Skip tour/ }));
    expect(onPrimary).toHaveBeenCalledTimes(1);
    expect(onSkip).toHaveBeenCalledTimes(1);
  });

  it('asks "Do you get it?" at the finale with the whole strip', () => {
    const { onPrimary, container } = renderAt(3, 'finale');
    expect(screen.getByRole('heading')).toHaveTextContent(SCRIPT.finale.title);
    for (const recap of SCRIPT.finale.recap) expect(screen.getByText(recap)).toBeInTheDocument();
    expect(container.querySelectorAll('ol img, ol video')).toHaveLength(3);
    expect(screen.queryByRole('button', { name: /Skip tour/ })).toBeNull();
    advance(TOUR_CARD_ENTRANCE_MS);
    expect(cardReady()).toBe(true);
    fireEvent.click(screen.getByRole('button', { name: new RegExp(SCRIPT.finale.action) }));
    expect(onPrimary).toHaveBeenCalledTimes(1);
  });

  it('settles at once on a skipAnimation bump', () => {
    const { container } = renderAt(2, 'land');
    advance(200);
    expect(cardReady()).toBe(false);
    act(() => skipEditorTourAnimation());
    expect(cardReady()).toBe(true);
    expect(container.querySelector('.editor-tour-card-playing')).toBeNull();
  });

  it('replays the entrance for the next beat after a skip', () => {
    renderAt(1, 'land');
    act(() => skipEditorTourAnimation());
    expect(cardReady()).toBe(true);
    act(() => setEditorTourBeat(2, 'land'));
    expect(cardReady()).toBe(false);
    advance(TOUR_CARD_ENTRANCE_MS);
    expect(cardReady()).toBe(true);
  });

  it('with reduced motion is ready at once, only fades in, and keeps videos still', () => {
    const { container } = renderAt(3, 'land', { reducedMotion: true });
    expect(cardReady()).toBe(true);
    expect(container.querySelector('.editor-tour-card-reduced')).not.toBeNull();
    expect(container.querySelector('.editor-tour-card-playing')).toBeNull();
    expect(container.querySelector('.editor-tour-playhead')).toBeNull();
    expect(play).not.toHaveBeenCalled();
  });

  it('plays the act-3 video with motion on', () => {
    renderAt(3, 'land');
    expect(play).toHaveBeenCalled();
  });

  it('names Esc without a skip handler', () => {
    renderAt(1, 'land', { onSkip: undefined });
    expect(screen.queryByRole('button', { name: /Skip tour/ })).toBeNull();
    expect(screen.getByText('Esc')).toBeInTheDocument();
  });
});
