import { renderHook } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { EDITOR_TOUR_MEDIA } from '../tourMedia.ts';
import { useTourMediaWarmup } from './useTourMediaWarmup.ts';

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

it('warms only the four reference images and H3 once per tour mount, then releases pending media requests', () => {
  const images: HTMLImageElement[] = [];
  vi.stubGlobal('Image', class {
    constructor() { const image = document.createElement('img'); images.push(image); return image; }
  });
  const loads: HTMLMediaElement[] = [];
  vi.spyOn(HTMLMediaElement.prototype, 'load').mockImplementation(function () { loads.push(this); });
  const pause = vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => undefined);
  const view = renderHook(useTourMediaWarmup);
  expect(images.map(image => image.getAttribute('src'))).toEqual(EDITOR_TOUR_MEDIA.stills.map(slot => slot.url));
  const video = loads[0];
  expect(video.getAttribute('src')).toBe(EDITOR_TOUR_MEDIA.video.url);
  expect(video.preload).toBe('auto');
  expect(video.paused).toBe(true);
  view.rerender();
  expect(images).toHaveLength(4);
  expect(loads).toHaveLength(1);
  view.unmount();
  expect(images.every(image => !image.hasAttribute('src'))).toBe(true);
  expect(video.hasAttribute('src')).toBe(false);
  expect(pause).toHaveBeenCalledTimes(1);
  expect(loads).toEqual([video, video]);
});
