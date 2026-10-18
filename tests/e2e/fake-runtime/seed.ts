/**
 * The fake Runtime's seed: small, fixed, and free of clocks and randomness.
 *
 * Content comes from the UI-facing seed `src/test/fakeRuntimeSeed.mjs` (read only): the demo timeline
 * and the two audio-reactive timelines. Assets are content-addressed. Every registry entry's bytes are
 * read from `public/`, hashed, and the entry is rewritten to `media_id = content_sha256 = sha256:<hex>`,
 * so the editor resolves it through `/v1/objects/sha256:...` and the Runtime provider's identity check
 * (ETag equals the registry digest) is exercised for real. The display-only `src` and `generationId`
 * fields are dropped: a `src` of `/example-image1.jpg` would be a Vite public path and silently bypass
 * the object route this seed exists to test.
 */
import { createHash } from 'node:crypto';
import fs from 'node:fs';

import { type BridgeTimelineFixtures, AUDIO_REACTIVE_FIXTURE_TIMELINE_ID, AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID, FIXTURE_PROJECT, FIXTURE_TIMELINE_ID, createAudioReactiveColourFixtures, createOffsetAudioReactiveColourFixtures, createTimelineFixtures } from '../../../src/test/fakeRuntimeSeed.mjs';
import type { FakeObjectStore } from '../../../src/test/fakeObjectStore.ts';

/** The canonical id of the one seeded project; its slug is `FIXTURE_PROJECT.slug`. */
export const DEMO_PROJECT_ID = 'demo-project-id';
export const DEMO_PROJECT_SLUG: string = FIXTURE_PROJECT.slug;

const PUBLIC_DIR = new URL('../../../public/', import.meta.url);
const SHA256_ID = /^sha256:[0-9a-f]{64}$/;

type RegistryEntry = BridgeTimelineFixtures['registry']['assets'][string];

export type SeededTimeline = {
  summary: Record<string, unknown> & { timeline_id: string };
  /** The parent composition the timeline starts from (registry rewritten to sha256 identities). */
  parentComposition: { config: Record<string, unknown>; registry: Record<string, unknown>; clips: unknown[]; occurrences: unknown[] };
};

type SeedAsset = { bytes: Uint8Array; mediaType: string; filename: string };

const assetCache = new Map<string, SeedAsset & { digest: string }>();

function readAsset(file: string, mediaType: string): SeedAsset & { digest: string } {
  const cached = assetCache.get(file);
  if (cached) return cached;
  const bytes = new Uint8Array(fs.readFileSync(new URL(file, PUBLIC_DIR)));
  const asset = { bytes, mediaType, filename: file, digest: `sha256:${createHash('sha256').update(bytes).digest('hex')}` };
  assetCache.set(file, asset);
  return asset;
}

function seedTimeline(fixture: BridgeTimelineFixtures): SeededTimeline {
  for (const clip of fixture.config.clips) {
    if ('media_id' in clip && !SHA256_ID.test(String(clip.media_id))) {
      throw new Error(`seed clip ${String(clip.id)} carries a non-sha256 media_id; the seed rewrites registry entries only`);
    }
  }
  const assets = Object.fromEntries(Object.entries(fixture.registry.assets).map(([key, entry]) => {
    const { src: _src, generationId: _generationId, ...kept } = entry;
    const asset = readAsset(entry.file, entry.type);
    return [key, { ...kept, media_id: asset.digest, content_sha256: asset.digest }];
  }));
  return {
    summary: fixture.timelineSummary,
    parentComposition: {
      config: fixture.config,
      registry: { ...fixture.registry, assets },
      clips: structuredClone(fixture.config.clips),
      occurrences: [],
    },
  };
}

/** Fresh, unshared seed timelines (default first). Call once per world build so no state leaks across a reset. */
export function createSeedTimelines(): SeededTimeline[] {
  return [
    createTimelineFixtures(),
    createAudioReactiveColourFixtures(),
    createOffsetAudioReactiveColourFixtures(),
  ].map(seedTimeline);
}

/** A fresh object store holding exactly the seeded assets, nothing a previous world ingested. */
export function createSeedObjectStore(): FakeObjectStore {
  const store: FakeObjectStore = new Map();
  for (const timeline of createSeedTimelines()) {
    for (const entry of Object.values((timeline.parentComposition.registry as { assets: Record<string, RegistryEntry> }).assets)) {
      const asset = readAsset(entry.file, entry.type);
      store.set(asset.digest, {
        projectId: DEMO_PROJECT_ID,
        bytes: asset.bytes,
        digest: asset.digest,
        mediaType: asset.mediaType,
        filename: asset.filename,
      });
    }
  }
  return store;
}

export const DEFAULT_TIMELINE_ID: string = FIXTURE_TIMELINE_ID;
export { AUDIO_REACTIVE_FIXTURE_TIMELINE_ID, AUDIO_REACTIVE_OFFSET_FIXTURE_TIMELINE_ID };
