// @vitest-environment node
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {describe, expect, it} from 'vitest';

const fixtureRoot = new URL('./fixtures/main-popup-analog-vp8-webm/', import.meta.url);
const bytes = (name: string) => readFileSync(fileURLToPath(new URL(name, fixtureRoot)));
const read = (name: string) => JSON.parse(bytes(name).toString());
const sha = (value: Uint8Array | string) => createHash('sha256').update(value).digest('hex');
const native = read('native.json');
const analog = read('analog.json');
const manifest = read('manifest.json');
const probe = read('main-vector.json');

describe('explicit Chromium141-playable MAIN popup analog', () => {
  it('keeps the native fixture and authored timing data exact', () => {
    expect(sha(bytes('native.json'))).toBe('e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46');
    expect(sha(bytes('native.json'))).toBe(manifest.native_sha256);
    expect(sha(bytes('analog.json'))).toBe(manifest.analog_sha256);
    const expected = structuredClone(native.add.output);
    for (const change of manifest.changes) {
      const keys = change.pointer.slice(1).split('/');
      const key = keys.pop()!;
      const parent = keys.reduce((value: Record<string, unknown>, field: string) => value[field], expected);
      expect(parent[key]).toEqual(change.before);
      parent[key] = change.after;
    }
    expect(analog).toEqual(expected);
    expect(analog.parent_revision.payload.occurrences.map((row: {placement: object}) => row.placement))
      .toEqual([{start_ms: 8000, track: 'picture'}, {start_ms: 10000, track: 'picture'}]);
    expect(analog.internal_timeline_revisions[1].payload.clips[2])
      .toMatchObject({at: 0.125, from: 2, to: 6, hold: 4, speed: 2, params: null, opaque: [null, false, {}]});
  });

  it('records deterministic six-second VP8/WebM bytes and their full media probes', () => {
    expect(manifest.fixture_version).toBe('main-popup-analog-vp8-webm-v1');
    expect(manifest.browser_calibration).toMatchObject({id: '1020045451', selected_browser: 'Chromium141'});
    expect(manifest.regeneration).toEqual({
      runs: 2,
      byte_identical: true,
      source_duration_seconds: 6,
      source_fps: '24/1',
      source_frames: 144,
      video_only: true,
    });
    expect(new Set(manifest.media.map((media: {sha256: string}) => media.sha256)).size).toBe(2);
    for (const media of manifest.media) {
      expect(media.media_type).toBe('video/webm');
      expect(media.codec).toBe('vp8');
      expect(media.analog_media_id).toBe(`sha256:${media.sha256}`);
      expect(sha(bytes(media.file))).toBe(media.sha256);
      expect(bytes(media.file).byteLength).toBe(media.size_bytes);
      expect(media.probe).toMatchObject({
        codec_name: 'vp8',
        codec_type: 'video',
        width: 160,
        height: 90,
        pix_fmt: 'yuv420p',
        r_frame_rate: '24/1',
        avg_frame_rate: '24/1',
        time_base: '1/1000',
        start_time: '0.000000',
        duration: '6.000000',
        nb_frames: '144',
        format_name: 'matroska,webm',
      });
      expect(media.probe.size).toBe(media.size_bytes);
      expect(media.content).toEqual({
        content_type: 'video/webm',
        accept_ranges: 'bytes',
        etag: `sha256:${media.sha256}`,
        source_bytes: media.file,
      });
      expect(media.locator).toBe(
        `http://native-source-diagnostic.invalid/v1/objects/${encodeURIComponent(media.analog_media_id)}`,
      );
      expect(media.native_selection.duration_seconds).toBe(6);
    }
  });

  it('declares the real object route and media resolver lookup without changing the host', () => {
    expect(manifest.route_contract).toEqual({
      method: 'GET',
      locator_pattern: 'http://native-source-diagnostic.invalid/v1/objects/<encodeURIComponent(sha256:digest)>',
      content_type: 'video/webm',
      range_support: 'bytes; source bytes unchanged for 200 and 206 responses',
      digest_binding: 'ETag and manifest sha256 are the same content digest',
    });
    const view = probe.views.analog;
    expect(view.rawUnchanged).toBe(true);
    expect(view.host.builtins).toContain('media');
    expect(view.host.builtins).not.toContain('video');
    expect(view.host.media).toMatchObject({source: 'builtin', capabilities: {preview: 'browser'}});
    for (const media of manifest.media) {
      const rows = view.boundedDefaultVector.filter(
        (clip: {assetEntry: {media_id: string}}) => clip.assetEntry.media_id === media.analog_media_id,
      );
      expect(rows.length).toBeGreaterThan(0);
      expect(rows.every((row: {assetEntry: {src: string}}) => row.assetEntry.src === media.locator)).toBe(true);
    }
    expect(view.requests.some((request: {path: string}) => request.path.includes('/timelines/media-resolver/inspect'))).toBe(true);
    expect(manifest.media.every((media: {media_type: string}) => media.media_type === 'video/webm')).toBe(true);
    expect(manifest.media.every((media: {codec: string}) => media.codec === 'vp8')).toBe(true);
  });

  it('retains the exact six-row MAIN boundary candidate and separates the old H264 analog', () => {
    const {native: original, analog: derived} = probe.views;
    const timing = (rows: Record<string, unknown>[]) => rows.map(row => Object.fromEntries(
      ['id', 'track', 'at', 'from', 'to', 'hold', 'speed', 'canonicalTiming']
        .filter(key => key in row).map(key => [key, row[key]]),
    ));
    expect(timing(derived.boundedDefaultVector)).toEqual(timing(original.boundedDefaultVector));
    expect(derived.boundedDefaultVector.map((row: {id: string}) => row.id))
      .toEqual(['clip-a', 'clip-b', 'occ-a:clip-a', 'occ-a:reserved-child', 'occ-b:clip-a', 'occ-b:clip-b']);
    expect(derived.boundaryVectorsEqual).toBe(true);
    expect(derived.boundedDefaultVector[3]).toMatchObject({at: 8.125, from: 2, to: 5.75, speed: 2});
    expect(derived.boundedDefaultVector[4]).toMatchObject({at: 11, from: 2, to: 6, speed: 2});
    expect(manifest.prepared_h264_analog.status).toBe('retained; not scheduled for Chromium141');
    expect(manifest.prepared_h264_analog.media_sha256).toEqual([
      '76d92ca45c35355e403166557482a495123a8de51424fbdb44a17be3f2224a82',
      '726373f1b20c0f465efdd88e16484a403d53ebcc5c4993ed78ca987779181c56',
    ]);
    expect(manifest.media.map((media: {sha256: string}) => media.sha256)).not.toEqual(manifest.prepared_h264_analog.media_sha256);
  });
});
