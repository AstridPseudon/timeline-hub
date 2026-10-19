import { createHash } from 'node:crypto';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { generatePlayableVideo, mediaHash, PARITY_FPS, PARITY_HEIGHT, PARITY_WIDTH } from './media';
import { AUDIO_REACTIVE_FIXTURE_TIMELINE_ID } from '../../../../src/test/fakeRuntimeSeed.mjs';
import {
  FAKE_RUNTIME_ORIGIN,
  PROJECT_SLUG,
  fakeRuntimeAuthHeaders,
  publishFakeRuntimeComposition,
  readFakeRuntimeComposition,
  TIMELINE_SLUG,
} from '../support';

export { PARITY_FPS, PARITY_HEIGHT, PARITY_WIDTH } from './media';

export const PARITY_FRAMES = [0, 37, 44, 45, 52, 89, 90, 120, 121, 135, 143, 164] as const;

export interface FrameParityFixture {
  readonly headRevisionId: string;
  readonly graphDigest: string;
  readonly sourceAudioMediaId: string;
  readonly sourceVideoMediaId: string;
  readonly sourceVideoMetadata: Awaited<ReturnType<typeof generatePlayableVideo>>['metadata'];
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

/** Publish one revision with real content-addressed picture and audible media. */
export async function publishFrameParityFixture(): Promise<FrameParityFixture> {
  const [demo, audio] = await Promise.all([
    readFakeRuntimeComposition(TIMELINE_SLUG),
    readFakeRuntimeComposition(AUDIO_REACTIVE_FIXTURE_TIMELINE_ID),
  ]);
  const demoAssets = assetsOf(demo.registry);
  const sourceAudio = assetsOf(audio.registry).source_audio;
  if (!sourceAudio?.media_id || !demoAssets['demo-hero']?.media_id || !demoAssets['demo-detail']?.media_id) {
    throw new Error('frame parity fixture is missing a seeded managed-media identity');
  }
  const directory = await mkdtemp(join(tmpdir(), 'frame-parity-media-'));
  const source = await generatePlayableVideo(directory).finally(async () => {
    await rm(directory, { recursive: true, force: true });
  });
  const response = await fetch(`${FAKE_RUNTIME_ORIGIN}/v1/projects/${PROJECT_SLUG}/objects`, {
    method: 'POST',
    headers: { ...fakeRuntimeAuthHeaders(), 'Content-Type': 'video/webm', 'Idempotency-Key': source.id, 'X-Original-Name': 'frame-marked.webm' },
    body: source.bytes,
  });
  if (response.status !== 201 || (await response.json()).data.object_id !== source.id) {
    throw new Error(`playable managed video ingest failed: ${response.status}`);
  }
  await assertManagedVideoHash(source.id);

  const published = await publishFakeRuntimeComposition((composition) => {
    const assets = assetsOf(composition.registry);
    assets.source_audio = structuredClone(sourceAudio);
    delete assets['demo-clip'];
    assets['parity-video'] = {
      media_id: source.id, type: 'video/webm', duration: 1.5, width: PARITY_WIDTH, height: PARITY_HEIGHT,
    };

    const config = composition.config;
    config.output = {
      resolution: `${PARITY_WIDTH}x${PARITY_HEIGHT}`,
      fps: PARITY_FPS,
      file: 'timeline-player-export-frame-parity.mp4',
      background: null,
      background_scale: null,
    };
    config.tracks = [
      // First visual track is foreground. Keep the video's marker visible at
      // its first frame even while the prior still's overlap frame is mounted.
      { id: 'V2', kind: 'visual', label: 'V2', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
      { id: 'V1', kind: 'visual', label: 'V1', scale: 1, fit: 'contain', opacity: 1, blendMode: 'normal' },
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
      { id: 'parity-managed-video', track: 'V2', at: 4, clipType: 'media', hold: 1.5, asset: 'parity-video', from: 0, to: 1.5, speed: 1 },
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
    sourceVideoMediaId: String(pinnedAssets['parity-video']?.media_id),
    sourceVideoMetadata: source.metadata,
    sourceImageMediaIds: [String(pinnedAssets['demo-hero']?.media_id), String(pinnedAssets['demo-detail']?.media_id)],
    config: pinned.config,
    registry: pinned.registry,
  };
}

export async function assertPinnedFrameParityFixture(fixture: FrameParityFixture): Promise<void> {
  await assertManagedVideoHash(fixture.sourceVideoMediaId);
  const current = await readFakeRuntimeComposition(TIMELINE_SLUG);
  if (current.headRevisionId !== fixture.headRevisionId) {
    throw new Error(`frame parity revision changed: expected ${fixture.headRevisionId}, got ${current.headRevisionId}`);
  }
  const currentDigest = graphDigest(current.config, current.registry);
  if (currentDigest !== fixture.graphDigest) {
    throw new Error(`frame parity graph changed: expected ${fixture.graphDigest}, got ${currentDigest}`);
  }
}

async function assertManagedVideoHash(id: string): Promise<void> {
  const response = await fetch(`${FAKE_RUNTIME_ORIGIN}/v1/objects/${encodeURIComponent(id)}`, {
    headers: fakeRuntimeAuthHeaders(),
  });
  if (!response.ok || mediaHash(new Uint8Array(await response.arrayBuffer())) !== id) {
    throw new Error(`managed video bytes differ from pinned source hash: ${id}`);
  }
}
