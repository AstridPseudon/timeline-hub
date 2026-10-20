import assert from 'node:assert/strict';
import {test} from 'node:test';
import {
  assertCaptureCapabilities,
  assertCaptureOutcome,
  assertRawPts,
  assertTone,
  assertStereoTones,
  assertVisualEvent,
  CONTROLLED_AUDIO,
  createSyntheticPcmWav,
  diagnoseVisualEvent,
  nativeAudioChannelDiagnostic,
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

test('decoded marker data is diagnostic and makes no phase claim', () => {
  const diagnostic = diagnoseVisualEvent(Buffer.from([31, 47, 63, 159, 31, 31]), {
    width: 2,
    height: 1,
    preEventRgb: [32, 48, 64],
    eventRgb: [160, 32, 32],
  });
  assert.deepEqual(diagnostic, {
    frameCount: 1,
    exactColorFrameCounts: [0, 0],
    phaseClaim: false,
    diagnosticOnly: true,
  });
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
    const tone = 0.1 * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.webAudioFrequency * index / sampleRate);
    samples[index * 2] = tone;
    samples[index * 2 + 1] = tone;
  }
  assert.equal(assertTone(samples, {sampleRate, channels: 2, frequency: CONTROLLED_AUDIO.webAudioFrequency}).channels, 2);
  assert.throws(() => assertTone(new Float32Array(samples.length), {
    sampleRate,
    channels: 2,
    frequency: CONTROLLED_AUDIO.webAudioFrequency,
  }), /not present/);
});

test('native ffprobe channel diagnostic marks mono unsupported before decode', () => {
  assert.deepEqual(nativeAudioChannelDiagnostic(2), {
    channels: 2,
    status: 'supported',
    requirement: 'native ffprobe audiochannels=2',
  });
  assert.deepEqual(nativeAudioChannelDiagnostic(1), {
    channels: 1,
    status: 'unsupported',
    requirement: 'native ffprobe audiochannels=2',
  });
});

test('left/right detector rejects mono and swapped channels', () => {
  const sampleRate = CONTROLLED_AUDIO.sampleRate;
  const samples = new Float32Array(sampleRate * 2);
  for (let index = 0; index < sampleRate; index += 1) {
    samples[index * 2] = CONTROLLED_AUDIO.channelAmplitude
      * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.leftFrequency * index / sampleRate);
    samples[index * 2 + 1] = CONTROLLED_AUDIO.channelAmplitude
      * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.rightFrequency * index / sampleRate);
  }
  const result = assertStereoTones(samples, {
    sampleRate,
    channels: 2,
    leftFrequency: CONTROLLED_AUDIO.leftFrequency,
    rightFrequency: CONTROLLED_AUDIO.rightFrequency,
  });
  assert.equal(result.channels, 2);

  const swapped = new Float32Array(samples.length);
  for (let index = 0; index < sampleRate; index += 1) {
    swapped[index * 2] = samples[index * 2 + 1];
    swapped[index * 2 + 1] = samples[index * 2];
  }
  assert.throws(() => assertStereoTones(swapped, {
    sampleRate,
    channels: 2,
    leftFrequency: CONTROLLED_AUDIO.leftFrequency,
    rightFrequency: CONTROLLED_AUDIO.rightFrequency,
  }), /not present/);
  assert.throws(() => assertStereoTones(new Float32Array(sampleRate), {
    sampleRate,
    channels: 1,
    leftFrequency: CONTROLLED_AUDIO.leftFrequency,
    rightFrequency: CONTROLLED_AUDIO.rightFrequency,
  }), /exactly two interleaved channels/);
});

test('full-tab source controls distinguish the independent oscillator and HTMLAudio tones', () => {
  const sampleRate = CONTROLLED_AUDIO.sampleRate;
  const samples = new Float32Array(sampleRate * 2);
  for (let index = 0; index < sampleRate; index += 1) {
    const webAudio = CONTROLLED_AUDIO.webAudioAmplitude
      * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.webAudioFrequency * index / sampleRate);
    const htmlAudio = CONTROLLED_AUDIO.htmlAudioAmplitude
      * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.htmlAudioFrequency * index / sampleRate);
    samples[index * 2] = webAudio + htmlAudio;
    samples[index * 2 + 1] = webAudio + htmlAudio;
  }
  assert.doesNotThrow(() => assertTone(samples, {
    sampleRate,
    channels: 2,
    frequency: CONTROLLED_AUDIO.webAudioFrequency,
  }));
  assert.doesNotThrow(() => assertTone(samples, {
    sampleRate,
    channels: 2,
    frequency: CONTROLLED_AUDIO.htmlAudioFrequency,
  }));

  const pureWebAudio = new Float32Array(samples.length);
  for (let index = 0; index < sampleRate; index += 1) {
    const value = CONTROLLED_AUDIO.webAudioAmplitude
      * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.webAudioFrequency * index / sampleRate);
    pureWebAudio[index * 2] = value;
    pureWebAudio[index * 2 + 1] = value;
  }
  assert.throws(() => assertTone(pureWebAudio, {
    sampleRate,
    channels: 2,
    frequency: CONTROLLED_AUDIO.htmlAudioFrequency,
  }), /not present/);
  const pureHtmlAudio = new Float32Array(samples.length);
  for (let index = 0; index < sampleRate; index += 1) {
    const value = CONTROLLED_AUDIO.htmlAudioAmplitude
      * Math.sin(2 * Math.PI * CONTROLLED_AUDIO.htmlAudioFrequency * index / sampleRate);
    pureHtmlAudio[index * 2] = value;
    pureHtmlAudio[index * 2 + 1] = value;
  }
  assert.throws(() => assertTone(pureHtmlAudio, {
    sampleRate,
    channels: 2,
    frequency: CONTROLLED_AUDIO.webAudioFrequency,
  }), /not present/);
});

test('synthetic HTMLAudio source is a finite native 48 kHz stereo PCM WAV', () => {
  const wav = createSyntheticPcmWav();
  assert.equal(wav.toString('ascii', 0, 4), 'RIFF');
  assert.equal(wav.toString('ascii', 8, 12), 'WAVE');
  assert.equal(wav.readUInt16LE(20), 1);
  assert.equal(wav.readUInt16LE(22), CONTROLLED_AUDIO.channels);
  assert.equal(wav.readUInt32LE(24), CONTROLLED_AUDIO.sampleRate);
  assert.equal(wav.readUInt16LE(34), 16);
  assert.equal(wav.readUInt32LE(40), wav.length - 44);
});
