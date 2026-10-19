import assert from 'node:assert/strict';
import { test } from 'node:test';
import { assertFrameWithinBound, compareRgbFrames, type RgbFrame } from './compare';
import { PARITY_HEIGHT, PARITY_WIDTH } from './media';

function image(): RgbFrame {
  return { width: PARITY_WIDTH, height: PARITY_HEIGHT, bytes: Buffer.alloc(PARITY_WIDTH * PARITY_HEIGHT * 3, 64) };
}

test('same comparator accepts baseline then rejects an opaque one-host patch with pixel metric', () => {
  const reference = image();
  const player = image();
  assertFrameWithinBound(compareRgbFrames(player, reference, 52));
  player.bytes.fill(255, 0, 30 * 30 * 3);
  assert.throws(() => assertFrameWithinBound(compareRgbFrames(player, reference, 52)), /900\/230400 pixels exceed 2\/255; max channel error=191\/255/);
  assert.equal(reference.bytes.every(value => value === 64), true);
});

test('strict RGB threshold and 0.1 percent boundary remain unchanged', () => {
  const reference = image();
  const player = image();
  player.bytes.fill(66);
  assertFrameWithinBound(compareRgbFrames(player, reference, 0));
  for (let pixel = 0; pixel < 230; pixel++) player.bytes[pixel * 3] = 67;
  assertFrameWithinBound(compareRgbFrames(player, reference, 0));
  player.bytes[230 * 3] = 67;
  assert.throws(() => assertFrameWithinBound(compareRgbFrames(player, reference, 0)), /231\/230400 pixels exceed 2\/255/);
});

test('rejects empty, truncated, extra and wrong-dimension images on either host', () => {
  const invalid = [
    { width: 0, height: 0, bytes: Buffer.alloc(0) },
    { ...image(), bytes: Buffer.alloc(1) },
    { ...image(), bytes: Buffer.alloc(PARITY_WIDTH * PARITY_HEIGHT * 3 + 1) },
    { ...image(), width: 360, height: 640 },
  ];
  for (const frame of invalid) {
    assert.throws(() => compareRgbFrames(frame, image(), 0), /invalid Player RGB frame/);
    assert.throws(() => compareRgbFrames(image(), frame, 0), /invalid export RGB frame/);
  }
});
