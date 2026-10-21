import type { TimelinePatch, TimelinePatchOperation } from '@/sdk/video/timeline/patch.ts';
import type { AssetRegistry, AssetRegistryEntry, TimelineConfig } from '@/tools/video-editor/types/index.ts';
import type { EditorTourStage } from '@/shared/state/editorTourStore.ts';
import { EDITOR_TOUR_TRACK_IDS } from '@/tools/video-editor/tour/anchors.ts';
import { EDITOR_TOUR_MEDIA, type EditorTourMediaSlot } from '@/tools/video-editor/tour/tourMedia.ts';
import { EDITOR_TOUR_SCRIPT } from '@/tools/video-editor/tour/tourScript.ts';
import { TOUR_SCENE_SOURCE_FROM, TOUR_SCENE_SOURCE_TO } from './tourSceneSource.ts';

export const EDITOR_TOUR_TIMELINE_ID = 'tour-timeline';
export const EDITOR_TOUR_LIVE_SCENE_CLIP_TYPE = 'haus.astrid.liveScene';
/** The scene's length on the timeline, which the video row spans too. */
export const TOUR_SCENE_SECONDS = 10;
/** How long each anchor frame (start, end) holds on the stills row. */
export const TOUR_ANCHOR_SECONDS = 1;

export const TOUR_CLIP_IDS = Object.freeze({
  scene: 'tour-scene-clip',
  stills: ['tour-still-clip-start', 'tour-still-clip-end'],
  video: 'tour-video-clip',
} as const);

const TOUR_ASSET_IDS = Object.freeze({
  stills: ['tour-still-start', 'tour-still-end'],
  video: 'tour-video',
} as const);

/** The stills row: the realistic start frame at 0 s and end frame in the scene's last second. */
const ANCHORS = [
  { label: 'Start frame', at: 0 },
  { label: 'End frame', at: TOUR_SCENE_SECONDS - TOUR_ANCHOR_SECONDS },
] as const;

/** Shown until the media slot has a real file: a neutral dark frame, never an empty `src`. */
const NEUTRAL_FRAME_URL = `data:image/svg+xml,${encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="9"><rect width="16" height="9" fill="#14110f"/></svg>',
)}`;

/**
 * The empty demo timeline. The scene row exists from the start (a config with no tracks is migrated
 * into V1-V3), so stage 1 only has to place the clip and stages 2 and 3 add rows above.
 */
export function createEditorTourTimeline(): TimelineConfig {
  return {
    output: { resolution: '1280x720', fps: 30, file: 'tour.mp4' },
    tracks: [{ id: EDITOR_TOUR_TRACK_IDS.scene, kind: 'visual', label: 'Three.js' }],
    clips: [],
  };
}

function assetEntry(slot: EditorTourMediaSlot, type: string, label: string, duration?: number): AssetRegistryEntry {
  return {
    file: slot.url || NEUTRAL_FRAME_URL,
    type,
    resolution: `${slot.width}x${slot.height}`,
    ...(duration === undefined ? {} : { duration }),
    metadata: { filename: label },
  } as AssetRegistryEntry;
}

// The video clip reuses the card's own words: the model that made it.
const VIDEO_NAME = EDITOR_TOUR_SCRIPT.acts[3].card.labels[0];

export function createEditorTourAssetRegistry(media = EDITOR_TOUR_MEDIA): AssetRegistry {
  const assets: AssetRegistry['assets'] = {};
  media.stills.forEach((slot, index) => {
    assets[TOUR_ASSET_IDS.stills[index]] = assetEntry(slot, 'image/webp', ANCHORS[index].label);
  });
  assets[TOUR_ASSET_IDS.video] = assetEntry(
    media.video, 'video/mp4', VIDEO_NAME, media.video.durationSeconds ?? TOUR_SCENE_SECONDS,
  );
  return { assets };
}

/** The tracks that exist after `stage`, top row first. */
export function tourTrackOrder(stage: EditorTourStage): string[] {
  return [
    ...(stage >= 3 ? [EDITOR_TOUR_TRACK_IDS.videos] : []),
    ...(stage >= 2 ? [EDITOR_TOUR_TRACK_IDS.stills] : []),
    EDITOR_TOUR_TRACK_IDS.scene,
  ];
}

/** The clip a stage brings in first: what to scroll to once the stage has landed. */
export function tourStageFocusClipId(stage: EditorTourStage): string | null {
  if (stage === 1) return TOUR_CLIP_IDS.scene;
  if (stage === 2) return TOUR_CLIP_IDS.stills[0];
  if (stage === 3) return TOUR_CLIP_IDS.video;
  return null;
}

/**
 * The edit that takes the demo timeline from `stage - 1` to `stage`, in the editor's own patch
 * vocabulary: `track.add` (above the current top row), then `clip.add` + `clip.update` per clip.
 * `version: 0` skips the canonical-version check.
 */
export function createEditorTourStagePatch(
  stage: 1 | 2 | 3,
  liveScene: Record<string, unknown>,
): TimelinePatch {
  const operations: TimelinePatchOperation[] = [];
  if (stage === 1) {
    operations.push(
      {
        op: 'clip.add',
        target: TOUR_CLIP_IDS.scene,
        payload: { track: EDITOR_TOUR_TRACK_IDS.scene, at: 0, clipType: EDITOR_TOUR_LIVE_SCENE_CLIP_TYPE },
      },
      {
        op: 'clip.update',
        target: TOUR_CLIP_IDS.scene,
        payload: {
          mode: 'merge',
          from: TOUR_SCENE_SOURCE_FROM,
          to: TOUR_SCENE_SOURCE_TO,
          speed: 1,
          label: 'Lantern Valley',
          app: { liveScene },
        },
      },
    );
  } else {
    const row = stage === 2
      ? { track: EDITOR_TOUR_TRACK_IDS.stills, label: 'Frames', before: EDITOR_TOUR_TRACK_IDS.scene }
      : { track: EDITOR_TOUR_TRACK_IDS.videos, label: 'Video', before: EDITOR_TOUR_TRACK_IDS.stills };
    operations.push({ op: 'track.add', target: row.track, payload: { kind: 'visual', label: row.label, before: row.before } });
    if (stage === 2) {
      ANCHORS.forEach(({ label, at }, index) => {
        const clipId = TOUR_CLIP_IDS.stills[index];
        operations.push(
          { op: 'clip.add', target: clipId, payload: { track: row.track, at, clipType: 'hold' } },
          {
            op: 'clip.update',
            target: clipId,
            payload: { mode: 'merge', asset: TOUR_ASSET_IDS.stills[index], hold: TOUR_ANCHOR_SECONDS, volume: 0, label },
          },
        );
      });
    } else {
      operations.push(
        { op: 'clip.add', target: TOUR_CLIP_IDS.video, payload: { track: row.track, at: 0, clipType: 'media' } },
        {
          op: 'clip.update',
          target: TOUR_CLIP_IDS.video,
          payload: { mode: 'merge', asset: TOUR_ASSET_IDS.video, from: 0, to: TOUR_SCENE_SECONDS, speed: 1, label: VIDEO_NAME },
        },
      );
    }
  }
  return { version: 0, operations, source: 'editor-tour' };
}
