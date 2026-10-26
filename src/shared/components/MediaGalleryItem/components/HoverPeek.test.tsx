// @vitest-environment jsdom
import { act, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { HoverPeekButton } from './HoverPeek';
import type { GeneratedImageWithMetadata } from '../../MediaGallery/types';

const FULL_URL = 'https://cdn.example/full.png';
const THUMB_URL = 'https://cdn.example/thumb.png';

const preloaded: string[] = [];

function imageFixture(overrides: Partial<GeneratedImageWithMetadata> = {}): GeneratedImageWithMetadata {
  return {
    id: 'img-1',
    url: FULL_URL,
    thumbUrl: THUMB_URL,
    prompt: 'Sunset',
    createdAt: '2026-01-01T00:00:00.000Z',
    ...overrides,
  } as GeneratedImageWithMetadata;
}

function renderPeek(options: { image?: GeneratedImageWithMetadata; onOpenLightbox?: () => void; isVideo?: boolean } = {}) {
  const onOpenLightbox = options.onOpenLightbox ?? vi.fn();
  const utils = render(
    <HoverPeekButton
      image={options.image ?? imageFixture()}
      thumbSrc={THUMB_URL}
      fullSrc={options.isVideo ? null : FULL_URL}
      videoSrc={options.isVideo ? 'https://cdn.example/clip.mp4' : null}
      isVideo={options.isVideo ?? false}
      metadataAspectRatio={null}
      projectAspectRatio={null}
      onOpenLightbox={onOpenLightbox}
    />,
  );
  return { ...utils, onOpenLightbox, eye: screen.getByLabelText('Preview') };
}

const peekEl = () => screen.queryByTestId('gallery-tile-peek');
const advance = (ms: number) => act(() => { vi.advanceTimersByTime(ms); });

describe('HoverPeekButton', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    preloaded.length = 0;
    vi.stubGlobal('Image', class {
      crossOrigin: string | null = null;
      onload: (() => void) | null = null;
      set src(value: string) { preloaded.push(value); }
    });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it('starts preloading the full image as soon as the eye is entered', () => {
    const { eye } = renderPeek();

    fireEvent.pointerEnter(eye);

    expect(preloaded).toContain(FULL_URL);
    expect(peekEl()).toBeNull();
  });

  it('opens the peek after the open delay, not before', () => {
    const { eye } = renderPeek();

    fireEvent.pointerEnter(eye);
    advance(119);
    expect(peekEl()).toBeNull();

    advance(1);
    expect(peekEl()).toBeInTheDocument();
  });

  it('stays open when the pointer moves from the eye onto the peek', () => {
    const { eye } = renderPeek();
    fireEvent.pointerEnter(eye);
    advance(120);

    fireEvent.pointerLeave(eye);
    fireEvent.pointerEnter(peekEl() as HTMLElement);
    advance(1000);

    expect(peekEl()).toBeInTheDocument();
  });

  it('closes after the grace period once the pointer leaves the peek', () => {
    const { eye } = renderPeek();
    fireEvent.pointerEnter(eye);
    advance(120);
    fireEvent.pointerLeave(eye);
    fireEvent.pointerEnter(peekEl() as HTMLElement);

    fireEvent.pointerLeave(peekEl() as HTMLElement);
    advance(119);
    expect(peekEl()).toBeInTheDocument();

    advance(1);
    expect(peekEl()).toBeNull();
  });

  it('cancels a pending open when the pointer leaves the eye early', () => {
    const { eye } = renderPeek();
    fireEvent.pointerEnter(eye);
    advance(60);
    fireEvent.pointerLeave(eye);

    advance(500);

    expect(peekEl()).toBeNull();
  });

  it('opens the lightbox and closes the peek when the peek is clicked', () => {
    const onOpenLightbox = vi.fn();
    const { eye } = renderPeek({ onOpenLightbox });
    fireEvent.pointerEnter(eye);
    advance(120);

    fireEvent.click(peekEl() as HTMLElement);

    expect(onOpenLightbox).toHaveBeenCalledWith(expect.objectContaining({ id: 'img-1' }));
    expect(peekEl()).toBeNull();
  });

  it('closes on Escape', () => {
    const { eye } = renderPeek();
    fireEvent.pointerEnter(eye);
    advance(120);
    expect(peekEl()).toBeInTheDocument();

    fireEvent.keyDown(window, { key: 'Escape' });

    expect(peekEl()).toBeNull();
  });

  it('keeps only one peek open: a second one closes the first', () => {
    const first = renderPeek();
    const second = render(
      <HoverPeekButton
        image={imageFixture({ id: 'img-2' })}
        thumbSrc={THUMB_URL}
        fullSrc={FULL_URL}
        videoSrc={null}
        isVideo={false}
        metadataAspectRatio={null}
        projectAspectRatio={null}
        onOpenLightbox={vi.fn()}
      />,
    );
    fireEvent.pointerEnter(first.eye);
    advance(120);
    expect(peekEl()).toBeInTheDocument();

    fireEvent.pointerEnter(screen.getAllByLabelText('Preview')[1]);
    advance(120);

    expect(screen.getAllByTestId('gallery-tile-peek')).toHaveLength(1);
    second.unmount();
  });

  it('clears its timers on unmount so a late open does not fire', () => {
    const { eye, unmount } = renderPeek();
    fireEvent.pointerEnter(eye);

    unmount();

    expect(() => advance(500)).not.toThrow();
  });

  it('renders a video peek with the full video and the thumbnail as poster', () => {
    const { eye } = renderPeek({ isVideo: true });
    fireEvent.pointerEnter(eye);
    advance(120);

    const video = peekEl()?.querySelector('video');
    expect(video).not.toBeNull();
    expect(video).toHaveAttribute('src', 'https://cdn.example/clip.mp4');
    expect(video).toHaveAttribute('poster', THUMB_URL);
    expect(preloaded).not.toContain(FULL_URL);
  });
});
