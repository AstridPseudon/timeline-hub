import { expect } from '@playwright/test';
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { promisify } from 'node:util';
import { FAKE_RUNTIME_ORIGIN, PROJECT_SLUG, fakeRuntimeAuthHeaders, publishFakeRuntimeComposition } from './support';

const exec = promisify(execFile);
export const CAPTURE_TIMELINE = 'audio-reactive-colour-timeline';
export const TONES = { native: 440, amplified: 660, video: 880 } as const;
export type Backend = keyof typeof TONES;

// Real playable inputs, never used as the capture/comparison output. Distinct
// frequencies let the monitor recording prove inclusion of each live backend.
export async function createManagedTones(directory: string): Promise<Record<Backend, string>> {
  const objects = {} as Record<Backend, string>;
  for (const [backend, frequency] of Object.entries(TONES) as [Backend, number][]) {
    const video = backend === 'video';
    const file = join(directory, `${backend}.${video ? 'webm' : 'wav'}`);
    await exec('ffmpeg', [
      '-v', 'error', '-y',
      ...(video ? ['-f', 'lavfi', '-i', 'testsrc2=size=320x180:rate=30:duration=3'] : []),
      '-f', 'lavfi', '-i', `sine=frequency=${frequency}:sample_rate=48000:duration=3`,
      '-af', 'pan=stereo|c0=c0|c1=0.75*c0',
      ...(video ? ['-c:v', 'libvpx', '-deadline', 'realtime', '-cpu-used', '8', '-b:v', '300k', '-pix_fmt', 'yuv420p', '-c:a', 'libopus', '-b:a', '128k'] : ['-c:a', 'pcm_s16le']),
      // Omit random WebM container IDs so independent repetitions ingest the
      // same bytes, without changing the encoded video/audio or clip inputs.
      '-threads', '1', '-fflags', '+bitexact', file,
    ]);
    const bytes = await readFile(file);
    const id = `sha256:${createHash('sha256').update(bytes).digest('hex')}`;
    const response = await fetch(`${FAKE_RUNTIME_ORIGIN}/v1/projects/${PROJECT_SLUG}/objects`, {
      method: 'POST',
      headers: { ...fakeRuntimeAuthHeaders(), 'Content-Type': video ? 'video/webm' : 'audio/wav', 'Idempotency-Key': id, 'X-Original-Name': `${backend}.${video ? 'webm' : 'wav'}` },
      body: bytes,
    });
    expect(response.status).toBe(201);
    expect((await response.json()).data.object_id).toBe(id);
    objects[backend] = id;
  }
  return objects;
}

export async function publishCaptureFixture(objects: Record<Backend, string>, backends: Backend[], fade = false) {
  return publishFakeRuntimeComposition(({ config, registry }) => {
    config.tracks = [
      { id: 'background', kind: 'visual', label: 'Background' },
      { id: 'visual', kind: 'visual', label: 'Video', fit: 'contain' },
      ...backends.filter(backend => backend !== 'video').map(id => ({ id, kind: 'audio', label: id })),
    ];
    config.clips = [
      { id: 'background', clipType: 'audio-reactive-colour', track: 'background', at: 0, hold: 4, params: { schemaVersion: 1, initialColor: '#203040', events: [] } },
      ...backends.map(backend => ({
        id: backend, clipType: 'media', track: backend === 'video' ? 'visual' : backend,
        asset: backend, at: 0, from: 0, to: 3, speed: 1,
        volume: backend === 'amplified' ? 2 : 1,
        ...(fade ? { params: { fadeIn: 0.6, fadeOut: 0.6 } } : {}),
      })),
    ];
    registry.assets = Object.fromEntries(backends.map(backend => [backend, {
      media_id: objects[backend], type: backend === 'video' ? 'video/webm' : 'audio/wav',
      duration: 3, width: 320, height: 180,
    }]));
  }, CAPTURE_TIMELINE);
}
