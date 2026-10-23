import type { ProjectObjectMetadata, ProjectObjectStorage } from '@/sdk/video/assets/projectObjects.ts';

/** Lantern Valley, moon overlook: world 22-32 s (the moon up, lanterns lifting off at 24). */
export const TOUR_SCENE_SOURCE_FROM = 50;
export const TOUR_SCENE_SOURCE_TO = 60;

async function sha256(bytes: Uint8Array): Promise<string> {
  const hash = await globalThis.crypto.subtle.digest('SHA-256', bytes as unknown as BufferSource);
  return `sha256:${Array.from(new Uint8Array(hash), (byte) => byte.toString(16).padStart(2, '0')).join('')}`;
}

/** Content-addressed bytes held in memory only; the tour never talks to a project object plane. */
function createMemoryObjectStorage(): ProjectObjectStorage {
  const objects = new Map<string, Uint8Array>();
  return {
    async ingest(bytes, mediaType, filename): Promise<ProjectObjectMetadata> {
      const digest = await sha256(bytes);
      const objectId = `tour-object-${digest.slice('sha256:'.length)}`;
      objects.set(objectId, new Uint8Array(bytes));
      return { object_id: objectId, digest, media_type: mediaType, size: bytes.byteLength, filename };
    },
    async read(objectId) {
      const bytes = objects.get(objectId);
      if (!bytes) throw new Error(`Tour object ${objectId} is not in memory.`);
      return new Uint8Array(bytes);
    },
  };
}

let liveScenePromise: Promise<Record<string, unknown>> | null = null;

/**
 * The `app.liveScene` envelope of the vendored Lantern Valley (inline html, no project storage).
 * The ~640 KB world loads lazily and is built once per page load.
 */
export function loadTourLiveScene(): Promise<Record<string, unknown>> {
  liveScenePromise ??= (async () => {
    const [{ SAMPLE_WORLD }, { parsePreparedScenePackage, ingestPreparedPackage }] = await Promise.all([
      import('@astrid/packs/rendering/ui/threejs-live-editor/explorer/worlds/sample'),
      import('@astrid/packs/rendering/ui/threejs-live-editor/authoring'),
    ]);
    const parsed = await parsePreparedScenePackage(new TextEncoder().encode(SAMPLE_WORLD.packageJson));
    return (await ingestPreparedPackage(createMemoryObjectStorage(), parsed)).liveScene;
  })().catch((error) => {
    liveScenePromise = null;
    throw error;
  });
  return liveScenePromise;
}
