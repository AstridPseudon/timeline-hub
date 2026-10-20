import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';
import { compositionPublication, type DirectHarness } from '../../local/support/harness';
import { generatePlayableVideo, mediaHash, PARITY_FPS, PARITY_HEIGHT, PARITY_WIDTH } from './media';

export { PARITY_FPS, PARITY_HEIGHT, PARITY_WIDTH } from './media';
export const PARITY_FRAMES = [0, 37, 44, 45, 52, 89, 90, 120, 121, 135, 143, 164] as const;
const exec = promisify(execFile);

interface Revision {
  revision_id: string;
  content_digest: string;
  payload: Record<string, unknown>;
  internal_timeline_revision_id?: string;
}
interface MediaPin { objectId: string; digest: string }
export interface FrameParityFixture {
  projectId: string;
  timelineId: string;
  headRevisionId: string;
  shotId: string;
  occurrenceId: string;
  shotRevisionId: string;
  internalRevisionId: string;
  parent: Revision;
  shot: Revision;
  internal: Revision;
  media: MediaPin[];
  sourceVideoMediaId: string;
  sourceVideoMetadata: Awaited<ReturnType<typeof generatePlayableVideo>>['metadata'];
}

export async function readRuntimeJson<T>(harness: DirectHarness, path: string): Promise<T> {
  const response = await harness.runtimeJson<T>('GET', path);
  assert.equal(response.status, 200, `GET ${path}: ${JSON.stringify(response.body)}`);
  return response.body;
}

export function timelineBase(fixture: Pick<FrameParityFixture, 'projectId' | 'timelineId'>): string {
  return `/v1/projects/${fixture.projectId}/timelines/${fixture.timelineId}`;
}

async function readClosure(harness: DirectHarness, fixture: Pick<FrameParityFixture,
  'projectId' | 'timelineId' | 'headRevisionId' | 'shotId' | 'shotRevisionId' | 'internalRevisionId'>) {
  type PublicRevision = Revision & { project_id: string; timeline_id?: string; shot_id?: string };
  const [parent, shot, internal] = await Promise.all([
    readRuntimeJson<PublicRevision>(harness, `${timelineBase(fixture)}/composition-revisions/${fixture.headRevisionId}`),
    readRuntimeJson<PublicRevision>(harness, `/v1/projects/${fixture.projectId}/shots/${fixture.shotId}/revisions/${fixture.shotRevisionId}`),
    readRuntimeJson<PublicRevision>(harness, `${timelineBase(fixture)}/revisions/${fixture.internalRevisionId}`),
  ]);
  for (const revision of [parent, shot, internal]) assert.equal(revision.project_id, fixture.projectId);
  assert.equal(parent.timeline_id, fixture.timelineId);
  assert.equal(shot.shot_id, fixture.shotId);
  assert.equal(internal.timeline_id, fixture.timelineId);
  // Authoring startup may add a verified baseline manifest to read metadata;
  // compare immutable identity/payload rather than that derived read decoration.
  const immutable = (revision: Revision): Revision => ({
    revision_id: revision.revision_id, content_digest: revision.content_digest, payload: revision.payload,
    ...(revision.internal_timeline_revision_id ? { internal_timeline_revision_id: revision.internal_timeline_revision_id } : {}),
  });
  return { parent: immutable(parent), shot: immutable(shot), internal: immutable(internal) };
}

/** Existing M1 fixture setup before authoring/Render; not an authoring-path proof. */
export async function prepareFrameParityFixture(harness: DirectHarness): Promise<FrameParityFixture> {
  const directory = await mkdtemp(join(tmpdir(), 'real-frame-parity-'));
  try {
    const source = await generatePlayableVideo(directory);
    const audioPath = join(directory, 'tone.wav');
    await exec('ffmpeg', ['-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=44100:duration=1',
      '-ac', '2', '-c:a', 'pcm_s16le', '-threads', '1', audioPath]);
    const ingest = async (bytes: Buffer, type: string, filename: string): Promise<MediaPin> => {
      const response = await harness.runtimeFetch(`/v1/projects/${harness.seed.projectId}/objects`, {
        method: 'POST', headers: { 'Content-Type': type, 'Idempotency-Key': randomUUID(), 'X-Original-Name': filename },
        body: new Uint8Array(bytes),
      });
      assert.ok([200, 201].includes(response.status), `ingest ${filename}: ${response.status}`);
      const { data } = await response.json();
      assert.equal(data.digest, mediaHash(bytes));
      assert.equal(data.object_id, data.digest);
      return { objectId: data.object_id, digest: data.digest };
    };
    const video = await ingest(source.bytes, 'video/webm', 'frame-marked.webm');
    const audio = await ingest(await readFile(audioPath), 'audio/wav', 'tone.wav');
    const { projectId, timelineId, headRevisionId: expectedHead, image } = harness.seed;
    const shotId = 'frame-parity-shot';
    const occurrenceId = 'frame-parity-occurrence';
    const shotRevisionId = randomUUID();
    const internalRevisionId = randomUUID();
    const publication = compositionPublication(harness.seed, expectedHead, 'Ordinary media frame parity', PARITY_FPS);
    const asset = (pin: MediaPin, type: string, duration?: number) => ({
      media_id: pin.objectId, content_sha256: pin.digest, type, ...(duration === undefined ? {} : { duration }),
    });
    // One canonical occurrence bounds the picture at 165 exclusive. No
    // transition policy is exercised here; the original c16 fixture is held
    // for the separate incoming-transition requirement, with its expectations.
    const clips = [
      { id: 'parity-image', track: 'V1', at: 0, clipType: 'media', hold: 4, asset: 'still' },
      { id: 'parity-video', track: 'V1', at: 4, clipType: 'media', hold: 1.5, asset: 'video', from: 0, to: 1.5, speed: 1 },
      { id: 'parity-audio', track: 'A1', at: 0.25, clipType: 'media', asset: 'audio', from: 0.05, to: 0.55,
        speed: 1, volume: 0.8, effects: [{ fade_in: 0.1, fade_out: 0.1 }] },
    ];
    Object.assign(publication.parent_composition, {
      config: { output: { resolution: `${PARITY_WIDTH}x${PARITY_HEIGHT}`, fps: PARITY_FPS, file: 'frame-parity.mp4' },
        tracks: [{ id: 'S1', kind: 'visual', label: 'S1' }], clips: [] },
      occurrences: [{ occurrence_id: occurrenceId, shot_id: shotId, shot_revision_id: shotRevisionId,
        placement: { start_ms: 0 }, source_offset: 0, duration_ms: 5500, speed: 1, track: 'S1',
        transform: {}, gain: 1, muted: false, provenance: {} }],
    });
    Object.assign(publication, {
      internal_timeline_revisions: [{ timeline_id: timelineId, revision_id: internalRevisionId, payload: {
        tracks: [{ id: 'V1', kind: 'visual', label: 'V1' }, { id: 'A1', kind: 'audio', label: 'A1' }],
        clips, effects: [], audio: [], layout: {}, assets: [],
        registry: { assets: { still: asset(image, 'image/png'), video: asset(video, 'video/webm', 1.5), audio: asset(audio, 'audio/wav', 1) } },
      } }],
      shot_revisions: [{ shot_id: shotId, revision_id: shotRevisionId, internal_timeline_revision_id: internalRevisionId,
        payload: { metadata: { title: 'Ordinary media' }, items: [], pools: [], selected_variants: {}, provenance: {},
          generation_inputs: {}, audio_bindings: [], text_bindings: [] } }],
    });
    const response = await harness.runtimeJson<{ data: { new_head: string; content_digests: Record<string, string> } }>('POST',
      `${timelineBase(harness.seed)}/composition-revisions`, publication);
    assert.equal(response.status, 200, JSON.stringify(response.body));
    assert.equal(response.body.data.new_head, publication.parent_revision_id);
    const pins = { projectId, timelineId, headRevisionId: response.body.data.new_head, shotId, occurrenceId, shotRevisionId, internalRevisionId };
    const closure = await readClosure(harness, pins);
    assert.equal(closure.parent.revision_id, pins.headRevisionId);
    assert.equal(closure.shot.revision_id, shotRevisionId);
    assert.equal(closure.internal.revision_id, internalRevisionId);
    assert.equal(closure.shot.internal_timeline_revision_id, internalRevisionId);
    assert.equal(closure.parent.content_digest, response.body.data.content_digests.parent);
    assert.equal(closure.shot.content_digest, response.body.data.content_digests[shotRevisionId]);
    assert.equal(closure.internal.content_digest, response.body.data.content_digests[internalRevisionId]);
    assert.deepEqual(closure.parent.payload.occurrences, publication.parent_composition.occurrences);
    const fixture = { ...pins, ...closure, media: [image, video, audio], sourceVideoMediaId: video.objectId, sourceVideoMetadata: source.metadata };
    await assertPinnedFrameParityFixture(harness, fixture);
    return fixture;
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

export async function assertPinnedFrameParityFixture(harness: DirectHarness, fixture: FrameParityFixture): Promise<void> {
  const head = await readRuntimeJson<{ items: Array<{ revision_id: string; is_current_head: boolean }> }>(harness,
    `${timelineBase(fixture)}/composition-revisions?limit=1`);
  assert.equal(head.items.find(item => item.is_current_head)?.revision_id, fixture.headRevisionId, 'fixture parent head changed');
  assert.deepEqual(await readClosure(harness, fixture), { parent: fixture.parent, shot: fixture.shot, internal: fixture.internal });
  for (const pin of fixture.media) {
    const response = await harness.runtimeFetch(`/v1/objects/${encodeURIComponent(pin.objectId)}`);
    assert.equal(response.status, 200);
    assert.equal(mediaHash(new Uint8Array(await response.arrayBuffer())), pin.digest, 'fixture media bytes changed');
  }
}
