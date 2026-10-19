import { createHash } from 'node:crypto';
import { AUDIO_REACTIVE_FIXTURE_TIMELINE_ID } from '../../../../src/test/fakeRuntimeSeed.mjs';
import {
  publishFakeRuntimeComposition,
  readFakeRuntimeComposition,
  TIMELINE_SLUG,
} from '../support';

export const PARITY_FPS = 30;
export const PARITY_WIDTH = 640;
export const PARITY_HEIGHT = 360;

export const PARITY_FRAMES = [0, 44, 45, 52, 89, 90, 120, 164] as const;

export interface FrameParityFixture {
  readonly headRevisionId: string;
  readonly graphDigest: string;
  readonly sourceAudioMediaId: string;
  readonly sourceVideoMediaId: string;
  readonly sourceImageMediaIds: readonly string[];
  readonly config: Record<string, unknown>;
  readonly registry: Record<string, unknown>;
}

type Asset = Record<string, unknown> & { media_id?: string };

function assetsOf(registry: Record<string, unknown>): Record<string, Asset> {
  const assets = registry.assets;
  if (!assets || typeof assets !== 'object' || Array.isArray(assets)) {
    throw new Error('frame parity fixture requires registry.assets');
  }
  return assets as Record<string, Asset>;
}

function graphDigest(config: Record<string, unknown>, registry: Record<string, unknown>): string {
  return `sha256:${createHash('sha256').update(JSON.stringify({ config, registry })).digest('hex')}`;
}

/**
 * Extends the existing seeded demo through the normal test publish route. The
 * source audio is copied from the checked-in audible fixture, while the image
 * and video bytes remain the fake Runtime's existing content-addressed media.
 */
export async function publishFrameParityFixture(): Promise<FrameParityFixture> {
  const [demo, audio] = await Promise.all([
    readFakeRuntimeComposition(TIMELINE_SLUG),
    readFakeRuntimeComposition(AUDIO_REACTIVE_FIXTURE_TIMELINE_ID),
  ]);
  const demoAssets = assetsOf(demo.registry);
  const audioAssets = assetsOf(audio.registry);
  const sourceAudio = audioAssets.source_audio;
  const sourceImage1 = demoAssets['demo-hero'];
  const sourceImage2 = demoAssets['demo-detail'];
  const sourceVideo = demoAssets['demo-clip'];
  if (!sourceAudio?.media_id || !sourceImage1?.media_id || !sourceImage2?.media_id || !sourceVideo?.media_id) {
    throw new Error('frame parity fixture is missing a seeded managed-media identity');
  }

  const published = await publishFakeRuntimeComposition((composition) => {
    const assets = assetsOf(composition.registry);
    assets.source_audio = structuredClone(sourceAudio);

    const config = composition.config;
    config.output = {
      resolution: `${PARITY_WIDTH}x${PARITY_HEIGHT}`,
      fps: PARITY_FPS,
      file: 'timeline-player-export-frame-parity.mp4',
      background: null,
      background_scale: null,
    };
    config.tracks = [
      { id: 'V1', kind: 'visual', label: 'V1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
      { id: 'V2', kind: 'visual', label: 'V2', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
      { id: 'A1', kind: 'audio', label: 'A1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
    ];
    config.clips = [
      { id: 'parity-image-a', track: 'V1', at: 0, clipType: 'media', hold: 1.5, asset: 'demo-hero' },
      {
        id: 'parity-image-b',
        track: 'V1',
        at: 1.5,
        clipType: 'media',
        hold: 1.5,
        asset: 'demo-detail',
        transition: { type: 'crossfade', duration: 0.5 },
      },
      { id: 'parity-hard-cut', track: 'V1', at: 3, clipType: 'media', hold: 1, asset: 'demo-hero' },
      { id: 'parity-managed-video', track: 'V2', at: 4, clipType: 'media', hold: 1.5, asset: 'demo-clip', from: 0, to: 1.5, speed: 1 },
      {
        id: 'parity-audio',
        track: 'A1',
        at: 0.25,
        clipType: 'media',
        hold: 0.5,
        asset: 'source_audio',
        from: 0.05,
        to: 0.55,
        speed: 1,
        volume: 0.8,
        effects: [{ fade_in: 0.1, fade_out: 0.1 }],
      },
    ];
  }, TIMELINE_SLUG);

  const pinned = await readFakeRuntimeComposition(TIMELINE_SLUG);
  if (pinned.headRevisionId !== published.headRevisionId) {
    throw new Error(`frame parity publish was not accepted at the read-back head: ${published.headRevisionId} != ${pinned.headRevisionId}`);
  }
  const pinnedAssets = assetsOf(pinned.registry);
  return {
    headRevisionId: pinned.headRevisionId,
    graphDigest: graphDigest(pinned.config, pinned.registry),
    sourceAudioMediaId: String(pinnedAssets.source_audio?.media_id),
    sourceVideoMediaId: String(pinnedAssets['demo-clip']?.media_id),
    sourceImageMediaIds: [String(pinnedAssets['demo-hero']?.media_id), String(pinnedAssets['demo-detail']?.media_id)],
    config: pinned.config,
    registry: pinned.registry,
  };
}

export async function assertPinnedFrameParityFixture(fixture: FrameParityFixture): Promise<void> {
  const current = await readFakeRuntimeComposition(TIMELINE_SLUG);
  if (current.headRevisionId !== fixture.headRevisionId) {
    throw new Error(`frame parity revision changed: expected ${fixture.headRevisionId}, got ${current.headRevisionId}`);
  }
  const currentDigest = graphDigest(current.config, current.registry);
  if (currentDigest !== fixture.graphDigest) {
    throw new Error(`frame parity graph changed: expected ${fixture.graphDigest}, got ${currentDigest}`);
  }
}

