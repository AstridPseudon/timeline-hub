import assert from 'node:assert/strict';
import {test} from 'node:test';
import {
  assertCaptureCapabilities,
  assertCaptureOutcome,
  assertRawPts,
  assertTone,
  assertVisualEvent,
} from './tab-audio-capture.analysis.mjs';

const capabilities = assertCaptureCapabilities([
  {kind: 'video', readyState: 'live'},
  {kind: 'audio', readyState: 'live'},
], {mimeType: 'video/webm;codecs=vp8,opus'});

function probeFixture() {
  return {
    streams: [
      {index: 0, codec_type: 'video', time_base: '1/1000'},
      {index: 1, codec_type: 'audio', time_base: '1/48000'},
    ],
    packets: [
      {stream_index: 0, pts: '0', pts_time: '0.000'},
      {stream_index: 1, pts: '0', pts_time: '0.000'},
      {stream_index: 0, pts: '33', pts_time: '0.033'},
      {stream_index: 1, pts: '960', pts_time: '0.020'},
    ],
  };
}

test('capability check requires one live video and one live tab-audio track', () => {
  assert.deepEqual(capabilities, {videoTracks: 1, audioTracks: 1, mimeType: 'video/webm;codecs=vp8,opus'});
  assert.throws(() => assertCaptureCapabilities([{kind: 'video', readyState: 'live'}], {
    mimeType: 'video/webm;codecs=vp8,opus',
  }), /one tab audio track/);
});

test('visual event check requires both exact marker colors in decoded frames', () => {
  const frame = (rgb) => Buffer.from([...rgb, ...rgb]);
  const rawVideo = Buffer.concat([frame([32, 48, 64]), frame([160, 32, 32])]);
  assert.deepEqual(assertVisualEvent(rawVideo, {
    width: 2,
    height: 1,
    preEventRgb: [32, 48, 64],
    eventRgb: [160, 32, 32],
  }), {frameCount: 2, framesWithPreEventColor: 1, framesWithEventColor: 1});
  assert.throws(() => assertVisualEvent(frame([32, 48, 64]), {
    width: 2,
    height: 1,
    preEventRgb: [32, 48, 64],
    eventRgb: [160, 32, 32],
  }), /both pre-event and event marker colors/);
});

test('raw PTS checks retain native per-stream timestamps without alignment', () => {
  assert.deepEqual(assertRawPts(probeFixture()), {
    streamCount: 2,
    packetCounts: {video: 2, audio: 2},
    timeBases: {video: '1/1000', audio: '1/48000'},
  });
  assert.deepEqual(assertCaptureOutcome(probeFixture(), capabilities).capabilities, capabilities);
  assert.throws(() => assertRawPts({
    ...probeFixture(),
    packets: [...probeFixture().packets, {stream_index: 0, pts: '32', pts_time: '0.032'}],
  }), /raw PTS regressed/);
});

test('tone check observes decoded channels without resampling or level normalization', () => {
  const sampleRate = 48_000;
  const samples = new Float32Array(sampleRate * 2);
  for (let index = 0; index < sampleRate; index += 1) {
    const tone = 0.1 * Math.sin(2 * Math.PI * 880 * index / sampleRate);
    samples[index * 2] = tone;
    samples[index * 2 + 1] = tone;
  }
  assert.equal(assertTone(samples, {sampleRate, channels: 2, frequency: 880}).channels, 2);
  assert.throws(() => assertTone(new Float32Array(samples.length), {sampleRate, channels: 2, frequency: 880}), /not present/);
});

