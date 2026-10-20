// @vitest-environment node
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {describe, expect, it} from 'vitest';

const fixtureRoot = new URL('./fixtures/main-popup-analog/', import.meta.url);
const bytes = (name: string) => readFileSync(fileURLToPath(new URL(name, fixtureRoot)));
const read = (name: string) => JSON.parse(bytes(name).toString());
const sha = (value: Uint8Array | string) => createHash('sha256').update(value).digest('hex');
const native = read('native.json');
const analog = read('analog.json');
const manifest = read('manifest.json');
const probe = read('main-vector.json');

describe('explicit playable MAIN popup analog preparation', () => {
  it('keeps the native fixture exact and enumerates every analog change', () => {
    expect(sha(bytes('native.json'))).toBe('e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46');
    expect(sha(bytes('native.json'))).toBe(manifest.native_sha256);
    expect(sha(bytes('analog.json'))).toBe(manifest.analog_sha256);
    expect(sha(JSON.stringify(native.add.output))).toBe(manifest.native_output_sha256);
    const expected = structuredClone(native.add.output);
    for (const change of manifest.changes) {
      const keys = change.pointer.slice(1).split('/');
      const key = keys.pop()!;
      const parent = keys.reduce((value, field) => value[field], expected);
      expect(parent[key]).toEqual(change.before);
      expect(change.reason).toBeTruthy();
      parent[key] = change.after;
    }
    expect(analog).toEqual(expected);
    expect(manifest.changes.filter((change: {pointer: string}) => change.pointer.endsWith('/clipType')))
      .toEqual([expect.objectContaining({before: 'video', after: 'media'})]);
    expect(analog.parent_revision.payload.occurrences.map((row: {placement: object}) => row.placement))
      .toEqual([{start_ms: 8000, track: 'picture'}, {start_ms: 10000, track: 'picture'}]);
    const raw = analog.internal_timeline_revisions[1].payload.clips[2];
    expect(raw).toMatchObject({at: 0.125, from: 2, to: 6, hold: 4, speed: 2, params: null, opaque: [null, false, {}]});
  });

  it('binds distinct actual six-second MP4 bytes to their analog managed identities', () => {
    expect(new Set(manifest.media.map((media: {sha256: string}) => media.sha256)).size).toBe(2);
    for (const media of manifest.media) {
      expect(sha(bytes(media.file))).toBe(media.sha256);
      expect(media.analog_media_id).toBe(`sha256:${media.sha256}`);
      expect(bytes(media.file).byteLength).toBe(media.size_bytes);
      expect(media.probe).toMatchObject({codec_name: 'h264', pix_fmt: 'yuv420p', nb_frames: '144', duration: '6.000000'});
      expect(native.add.verified_media.find((entry: {selection: {object_id: string}}) => entry.selection.object_id === media.native_media_id).duration_seconds).toBe(6);
    }
  });

  it('records the same six rows through MAIN boundaries with valid numeric FPS', () => {
    const {native: original, analog: derived} = probe.views;
    const timing = (rows: Record<string, unknown>[]) => rows.map(row => Object.fromEntries(
      ['id', 'track', 'at', 'from', 'to', 'hold', 'speed', 'canonicalTiming'].filter(key => key in row).map(key => [key, row[key]]),
    ));
    expect(timing(derived.boundedDefaultVector)).toEqual(timing(original.boundedDefaultVector));
    expect(derived.boundedDefaultVector.map((row: {id: string}) => row.id))
      .toEqual(['clip-a', 'clip-b', 'occ-a:clip-a', 'occ-a:reserved-child', 'occ-b:clip-a', 'occ-b:clip-b']);
    expect(derived.boundaryVectorsEqual).toBe(true);
    expect(original.frameDiagnostics.frames.every((row: {finite: boolean}) => !row.finite)).toBe(true);
    expect(derived.frameDiagnostics.output.fps).toBe(30000 / 1001);
    expect(derived.frameDiagnostics.frames.map((row: {start: number; duration: number; finite: boolean}) => [row.start, row.duration, row.finite]))
      .toEqual([[30, 60, true], [150, 60, true], [270, 30, true], [244, 56, true], [330, 60, true], [450, 60, true]]);
    expect(derived.boundedDefaultVector[3]).toMatchObject({at: 8.125, from: 2, to: 5.75, speed: 2});
    expect(derived.boundedDefaultVector[4]).toMatchObject({at: 11, from: 2, to: 6, speed: 2});
  });

  it('prepares boundary neighborhoods without clamping the excluded film end', () => {
    expect(probe.boundarySamples).toEqual([
      {time: 8, frames: [239, 240, 241]},
      {time: 8.125, frames: [243, 244, 245]},
      {time: 9, frames: [269, 270, 271]},
      {time: 10, frames: [299, 300, 301]},
      {time: 10.125, frames: [302, 303, 304]},
      {time: 11, frames: [329, 330, 331]},
      {time: 13, frames: [389, 390, 391]},
      {time: 15, frames: [449, 450, 451]},
      {time: 17, frames: [508, 509, 510]},
    ]);
    expect(manifest.capture_extent_note).toContain('no authored output/clip changes or seek clamping');
    expect(native.add.output.parent_revision.payload.config.output.fps).toEqual({numerator: 30000, denominator: 1001});
  });

  it('uses the real MAIN host and provider resolver without claiming a physical run', () => {
    const view = probe.views.analog;
    expect(view.rawUnchanged).toBe(true);
    expect(view.host.builtins).toContain('media');
    expect(view.host.builtins).not.toContain('video');
    expect(view.host.video).toBeUndefined();
    expect(view.host.media).toMatchObject({source: 'builtin', capabilities: {preview: 'browser'}});
    for (const media of manifest.media) {
      const row = view.boundedDefaultVector.find((clip: {assetEntry: {media_id: string}}) => clip.assetEntry.media_id === media.analog_media_id);
      expect(row.assetEntry.src).toBe(`http://native-source-diagnostic.invalid/v1/objects/${encodeURIComponent(media.analog_media_id)}`);
    }
    expect(view.requests.some((request: {path: string}) => request.path.includes('/timelines/media-resolver/inspect'))).toBe(true);
    expect(manifest.app_main).toBe('580508eed1bf6ed95caaf476c9d69a4672472a2f');
    expect(manifest.status).toBe('OFFLINE_PREPARATION_AGENT_SIX_ROWS_PENDING_NO_READY_GRANT');
    expect(sha(bytes('main-vector.json'))).toBe(manifest.support_sha256['main-vector.json']);
    expect(probe.qualification).toContain('NO_FRAMES_OR_PUBLIC_SCENE');
  });
});
