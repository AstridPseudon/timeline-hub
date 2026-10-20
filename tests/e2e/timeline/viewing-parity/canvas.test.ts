import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import baseline from '../../../../playwright.viewing-parity.config';
import nativeCodec from '../../../../playwright.viewing-parity.native-codec.config';
import native1920 from '../../../../playwright.viewing-parity.normal-profile-native1920.config';
import { NORMAL_PROFILE_NATIVE1920, ORIGINAL_640, readCanvasFrameMarker } from './canvas';
import { assertFrameWithinBound, compareRgbFrames } from './compare';
import { PARITY_FRAMES } from './fixture';
import { PARITY_HEIGHT, PARITY_WIDTH, readFrameMarker } from './media';

const base = new URL('./', import.meta.url);

for (const canvas of [ORIGINAL_640, NORMAL_PROFILE_NATIVE1920]) {
  const { width, height } = canvas;
  const image = () => ({ width, height, bytes: Buffer.alloc(width * height * 3, 64) });

  test(`${width}: native dimensions reject the other canvas and invalid RGB on both hosts`, () => {
    const other = canvas === ORIGINAL_640 ? NORMAL_PROFILE_NATIVE1920 : ORIGINAL_640;
    const invalid = [
      { ...other, bytes: Buffer.alloc(other.width * other.height * 3) },
      { ...image(), bytes: Buffer.alloc(width * height * 3 - 1) },
      { ...image(), bytes: Buffer.alloc(width * height * 3 + 1) },
      { ...image(), width: height, height: width },
    ];
    for (const frame of invalid) {
      assert.throws(() => compareRgbFrames(frame, image(), 52, canvas), /invalid Player RGB frame/);
      assert.throws(() => compareRgbFrames(image(), frame, 52, canvas), /invalid export RGB frame/);
    }
    assert.throws(() => assertFrameWithinBound(compareRgbFrames(image(), image(), 52, canvas), other), /invalid comparison/);
  });

  test(`${width}: unchanged 2/255 and .001 bounds accept the baseline before rejecting a picture patch`, () => {
    const reference = image();
    const player = image();
    player.bytes.fill(66);
    assertFrameWithinBound(compareRgbFrames(player, reference, 52, canvas), canvas);
    const allowed = Math.floor(width * height * 0.001);
    for (let pixel = 0; pixel < allowed; pixel++) player.bytes[pixel * 3] = 67;
    assertFrameWithinBound(compareRgbFrames(player, reference, 52, canvas), canvas);
    player.bytes[allowed * 3] = 67;
    assert.throws(() => assertFrameWithinBound(compareRgbFrames(player, reference, 52, canvas), canvas),
      new RegExp(`${allowed + 1}/${width * height} pixels exceed 2/255`));
    player.bytes.fill(255);
    assert.throws(() => assertFrameWithinBound(compareRgbFrames(player, reference, 52, canvas), canvas), /pixels exceed 2\/255/);
    assert.ok(reference.bytes.every(value => value === 64));
  });

  test(`${width}: readiness reads all 45 original source markers directly in native RGB`, () => {
    const bytes = Buffer.alloc(width * height * 3);
    const white = (x: number) => {
      const offset = ((24 * height / PARITY_HEIGHT) * width + x * width / PARITY_WIDTH) * 3;
      bytes.fill(255, offset, offset + 3);
    };
    assert.equal(readCanvasFrameMarker(bytes, canvas), null);
    for (let frame = 0; frame < 45; frame++) {
      bytes.fill(0);
      white(250);
      for (let bit = 0; bit < 6; bit++) if (frame & (1 << bit)) white(24 + bit * 40);
      assert.equal(readCanvasFrameMarker(bytes, canvas), frame);
      if (canvas === ORIGINAL_640) assert.equal(readCanvasFrameMarker(bytes), readFrameMarker(bytes));
    }
    assert.equal(readCanvasFrameMarker(Buffer.alloc(0), canvas), null);
    if (canvas === NORMAL_PROFILE_NATIVE1920) assert.equal(readCanvasFrameMarker(bytes.subarray(3), canvas), null);
  });
}

test('original640 stays the default; only the separately named config selects native1920 with Chrome155', () => {
  assert.deepEqual(ORIGINAL_640, { width: 640, height: 360, viewport: { width: 1600, height: 1000 } });
  assert.deepEqual(NORMAL_PROFILE_NATIVE1920, { width: 1920, height: 1080, viewport: { width: 2000, height: 1200 } });
  assert.equal(baseline.testMatch, 'player-export-frame-parity.spec.ts');
  assert.equal(nativeCodec.testMatch, baseline.testMatch);
  assert.equal(native1920.testMatch, 'player-export-normal-profile-native1920.spec.ts');
  assert.deepEqual(native1920.projects, nativeCodec.projects);
  assert.equal(native1920.globalSetup, './tests/e2e/timeline/viewing-parity/global-setup.ts');
  const { testMatch: _match, globalSetup: _setup, ...shared } = native1920;
  const { testMatch: _original, globalSetup: _oldSetup, ...expected } = nativeCodec;
  assert.deepEqual(shared, expected);
  const legacy = { width: 640, height: 360, bytes: Buffer.alloc(640 * 360 * 3) };
  assert.deepEqual(compareRgbFrames(legacy, legacy, 0), compareRgbFrames(legacy, legacy, 0, ORIGINAL_640));
  assertFrameWithinBound(compareRgbFrames(legacy, legacy, 0));
});

test('both entries register all five bodies with all twelve baseline frames before the picture negative', async () => {
  assert.equal(await readFile(new URL('../player-export-frame-parity.spec.ts', base), 'utf8'),
    "import { registerFrameParityCases } from './viewing-parity/cases';\n\nregisterFrameParityCases();\n");
  assert.equal(await readFile(new URL('../player-export-normal-profile-native1920.spec.ts', base), 'utf8'),
    "import { registerFrameParityCases } from './viewing-parity/cases';\nimport { NORMAL_PROFILE_NATIVE1920 } from './viewing-parity/canvas';\n\nregisterFrameParityCases(NORMAL_PROFILE_NATIVE1920);\n");
  const cases = await readFile(new URL('cases.ts', base), 'utf8');
  assert.deepEqual([...cases.matchAll(/\btest\('([^']+)'/g)].map(match => match[1]), [
    'normal App Render action downloads a valid native-size MP4 without a parity comparison',
    'fixture readiness seeks actual managed Player video and captures native frames without export',
    'compares native-size actual Player frames with decoded real CPU Remotion task output',
    'captures the actual Player page as one native-PTS VP8/Opus tab stream without a physical-mix claim',
    'picture-only one-host patch is reported as a mismatch after the full passing baseline',
  ]);
  assert.deepEqual([...PARITY_FRAMES], [0, 37, 44, 45, 52, 89, 90, 120, 121, 135, 143, 164]);
  const negative = cases.slice(cases.indexOf("test('picture-only"));
  assert.ok(negative.indexOf('await compareAllFrames(page, exportPath, testInfo)') < negative.indexOf('patch.dataset.testOnlyPictureMismatch'));
  assert.ok(negative.indexOf('assertFrameWithinBound(baseline, canvas)') < negative.indexOf('patch.dataset.testOnlyPictureMismatch'));
});
