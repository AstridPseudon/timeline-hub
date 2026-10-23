import frame1Url from './assets/frame-1.webp?url';
import frame2Url from './assets/frame-2.webp?url';
import still1Url from './assets/still-1.webp?url';
import still2Url from './assets/still-2.webp?url';
import videoUrl from './assets/video.mp4?url';

/**
 * Media slots for the editor tour. The stills and the video are placeholders for now; real media
 * replaces the files behind these slots without code changes.
 */

export interface EditorTourMediaSlot {
  url: string;
  width: number;
  height: number;
  durationSeconds?: number;
}

export interface EditorTourMedia {
  /** Lantern Valley's start and end frames (the explainer's "before"). */
  frames: readonly [EditorTourMediaSlot, EditorTourMediaSlot];
  /** The realistic start and end frames, 1 s each at either end of the stills row. */
  stills: readonly [EditorTourMediaSlot, EditorTourMediaSlot];
  /** The one 10 s shot made from the start and end frames, on the top row. */
  video: EditorTourMediaSlot;
}

const slot = (url: string, size: Omit<EditorTourMediaSlot, 'url'>): EditorTourMediaSlot =>
  Object.freeze({ url, ...size });

const FRAME_SIZE = { width: 1280, height: 720 } as const;
const STILL_SIZE = { width: 1280, height: 720 } as const;
const VIDEO_SIZE = { width: 1280, height: 720, durationSeconds: 10 } as const;

export const EDITOR_TOUR_MEDIA: EditorTourMedia = {
  frames: [
    slot(frame1Url, FRAME_SIZE),
    slot(frame2Url, FRAME_SIZE),
  ],
  stills: [
    slot(still1Url, STILL_SIZE),
    slot(still2Url, STILL_SIZE),
  ],
  video: slot(videoUrl, VIDEO_SIZE),
};
