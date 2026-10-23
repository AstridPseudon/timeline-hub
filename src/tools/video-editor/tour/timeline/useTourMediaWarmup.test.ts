import { renderHook } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { EDITOR_TOUR_MEDIA } from '../tourMedia.ts';
import { useTourMediaWarmup } from './useTourMediaWarmup.ts';

afterEach(() => { vi.unstubAllGlobals(); vi.restoreAllMocks(); });

it('warms both source frames, four reference images and H3 once, tolerates early decode failure, and releases pending media requests', async () => {
  const images: HTMLImageElement[] = [];
  const decode = vi.fn().mockRejectedValue(new Error('decode not available yet'));
  vi.stubGlobal('Image', class {
    constructor() { const image = document.createElement('img'); image.decode = decode; images.push(image); return image; }
  });
  const loads: HTMLMediaElement[] = [];
  vi.spyOn(HTMLMediaElement.prototype, 'load').mockImplementation(function () { loads.push(this); });
  const pause = vi.spyOn(HTMLMediaElement.prototype, 'pause').mockImplementation(() => undefined);
  const view = renderHook(useTourMediaWarmup);
  expect(images.map(image => image.getAttribute('src'))).toEqual([...EDITOR_TOUR_MEDIA.frames, ...EDITOR_TOUR_MEDIA.stills].map(slot => slot.url));
  await Promise.resolve(); // Early decode rejection is handled; visible media retains retry ownership.
  expect(decode).toHaveBeenCalledTimes(6);
  const video = loads[0];
  expect(video.getAttribute('src')).toBe(EDITOR_TOUR_MEDIA.video.url);
  expect(video.preload).toBe('auto');
  expect(video.paused).toBe(true);
  view.rerender();
  expect(images).toHaveLength(6);
  expect(loads).toHaveLength(1);
  view.unmount();
  expect(images.every(image => !image.hasAttribute('src'))).toBe(true);
  expect(video.hasAttribute('src')).toBe(false);
  expect(pause).toHaveBeenCalledTimes(1);
  expect(loads).toEqual([video, video]);
});
