import { useEffect } from 'react';
import { EDITOR_TOUR_MEDIA } from '../tourMedia.ts';

/** Warm the five generated media URLs while the earlier tour steps run. Browser hints,
 * not a download/decoder readiness guarantee: the timeline still waits for painted video frames. */
export function useTourMediaWarmup(): void {
  useEffect(() => {
    const images = EDITOR_TOUR_MEDIA.stills.map(({ url }) => {
      const image = new Image();
      image.crossOrigin = 'anonymous';
      image.src = url;
      return image;
    });
    const video = document.createElement('video');
    video.preload = 'auto';
    video.muted = true;
    video.crossOrigin = 'anonymous';
    video.src = EDITOR_TOUR_MEDIA.video.url;
    video.load();
    return () => {
      images.forEach((image) => image.removeAttribute('src'));
      video.pause();
      video.removeAttribute('src');
      video.load();
    };
  }, []);
}
