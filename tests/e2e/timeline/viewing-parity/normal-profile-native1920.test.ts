import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { compareRgbFrames, assertFrameWithinBound } from './normal-profile-native1920.compare';
import { PARITY_WIDTH, PARITY_HEIGHT, readNativeFrameMarker } from './normal-profile-native1920.dimensions';
import { PARITY_FRAMES } from './fixture';
import { PARITY_WIDTH as SOURCE_WIDTH, PARITY_HEIGHT as SOURCE_HEIGHT } from './media';
import { classifyPageDiagnostics } from './normal-profile-native1920.diagnostics';

const base = new URL('./', import.meta.url);
const root = new URL('../../../../', import.meta.url);
const manifest = JSON.parse(await readFile(new URL('normal-profile-native1920.manifest.json', base), 'utf8'));

test('separate proposal declares the existing normal profile, unchanged source and pending review', () => {
  assert.equal(manifest.name, 'normal-profile-native1920');
  assert.equal(manifest.actual_run_authorized, false);
  assert.equal(manifest.current_source_tuple, null);
  assert.equal(manifest.authored_output.resolution, '1920x1080');
  assert.deepEqual([manifest.expected_normal_profile.width, manifest.expected_normal_profile.height], [PARITY_WIDTH, PARITY_HEIGHT]);
  assert.deepEqual([SOURCE_WIDTH, SOURCE_HEIGHT], [640, 360]);
  assert.deepEqual(manifest.frame_controls.frames, [...PARITY_FRAMES]);
  assert.equal(manifest.frame_controls.max_channel_error, 2);
  assert.equal(manifest.frame_controls.max_outside_fraction, 0.001);
  assert.equal(manifest.frame_controls.negative_requires_full_passing_baseline, true);
  assert.equal(manifest.future_spec, 'tests/e2e/timeline/player-export-normal-profile-native1920.spec.ts');
});

test('fresh hashes protect every old helper, the four old cases, complete headers and seven product files', async () => {
  for (const [path, expected] of Object.entries({ ...manifest.protected_sha256, ...manifest.product_sha256 })) {
    const bytes = await readFile(new URL(path, root));
    assert.equal(createHash('sha256').update(bytes).digest('hex'), expected, path);
  }
});

test('proposal source changes only the explicit manifest dimensions, names, host and readiness samples', async () => {
  for (const variant of manifest.variants) {
    let expected = await readFile(new URL(variant.source, base), 'utf8');
    for (const [before, after] of variant.replacements) {
      assert.ok(expected.includes(before), `${variant.source}: missing declared source`);
      expected = expected.replaceAll(before, after);
    }
    assert.equal(await readFile(new URL(variant.target, base), 'utf8'), expected, variant.target);
  }
});

test('all four future cases retain their test bodies, twelve frames and baseline-before-negative order', async () => {
  const original = await readFile(new URL('../player-export-frame-parity.spec.ts', base), 'utf8');
  const proposal = await readFile(new URL('../player-export-normal-profile-native1920.proposal.ts', base), 'utf8');
  const names = (text: string) => [...text.matchAll(/ {2}test\('([^']+)'/g)].map(match => match[1]);
  assert.equal(names(proposal).length, 4);
  assert.deepEqual(names(proposal), names(original));
  assert.ok(proposal.indexOf('await compareAllFrames(page, exportPath, testInfo)', proposal.indexOf("test('picture-only"))
    < proposal.indexOf("patch.dataset.testOnlyPictureMismatch"));
  for (const audioCheck of ["codec_name: 'aac', sample_rate: '48000', channels: 2", 'expect(diagnostics.failures).toEqual([])']) {
    assert.ok(proposal.includes(audioCheck));
  }
});

test('native RGB dimensions reject 640, truncation and differently sized inputs without resizing', () => {
  const native = { width: PARITY_WIDTH, height: PARITY_HEIGHT, bytes: Buffer.alloc(PARITY_WIDTH * PARITY_HEIGHT * 3) };
  const old = { width: SOURCE_WIDTH, height: SOURCE_HEIGHT, bytes: Buffer.alloc(SOURCE_WIDTH * SOURCE_HEIGHT * 3) };
  for (const invalid of [old, { ...native, bytes: native.bytes.subarray(3) }, { ...native, width: 1919 }]) {
    assert.throws(() => compareRgbFrames(native, invalid, 52), /invalid export RGB frame dimensions\/bytes/);
    assert.throws(() => compareRgbFrames(invalid, native, 52), /invalid Player RGB frame dimensions\/bytes/);
  }
});

test('1920 comparator retains RGB 2 and strict .1% bound, including the planted mismatch', () => {
  const pixels = PARITY_WIDTH * PARITY_HEIGHT;
  const expected = { width: PARITY_WIDTH, height: PARITY_HEIGHT, bytes: Buffer.alloc(pixels * 3) };
  const actual = { ...expected, bytes: Buffer.alloc(pixels * 3, 2) };
  assertFrameWithinBound(compareRgbFrames(expected, actual, 52));
  for (let pixel = 0; pixel < Math.floor(pixels * 0.001); pixel++) actual.bytes[pixel * 3] = 3;
  assertFrameWithinBound(compareRgbFrames(expected, actual, 52));
  actual.bytes[Math.floor(pixels * 0.001) * 3] = 3;
  assert.throws(() => assertFrameWithinBound(compareRgbFrames(expected, actual, 52)), /2074\/2073600 pixels exceed 2\/255/);
});

test('readiness reads scaled cell coordinates directly in native RGB and rejects unmarked/wrong-size bytes', () => {
  const bytes = Buffer.alloc(PARITY_WIDTH * PARITY_HEIGHT * 3);
  const white = (x: number) => bytes.fill(255, (72 * PARITY_WIDTH + x * 3) * 3, (72 * PARITY_WIDTH + x * 3) * 3 + 3);
  assert.equal(readNativeFrameMarker(bytes), null);
  white(250);
  assert.equal(readNativeFrameMarker(bytes), 0);
  for (const bit of [0, 2, 3, 5]) white(24 + bit * 40);
  assert.equal(readNativeFrameMarker(bytes), 45);
  assert.equal(readNativeFrameMarker(bytes.subarray(3)), null);
});

test('native media code4, aborts without completed proof, auth errors and audio failures remain strict', () => {
  const origin = 'http://127.0.0.1:17340';
  const failures = [
    { kind: 'mediaerror' as const, url: `${origin}/api/astrid/v1/objects/result`, code: 4, message: 'DEMUXER_ERROR_NO_SUPPORTED_STREAMS' },
    { kind: 'requestfailed' as const, url: `${origin}/api/astrid/v1/objects/result`, method: 'GET', message: 'net::ERR_ABORTED', resourceType: 'media' },
    { kind: 'response' as const, url: `${origin}/api/astrid/v1/objects/result`, method: 'GET', status: 403 },
    { kind: 'pageerror' as const, message: 'audio decode failed' },
  ];
  assert.deepEqual(classifyPageDiagnostics(failures, origin, 'project').failures, failures);
});
