/**
 * Pure checks for the opt-in whole-tab capture probe.
 *
 * These checks deliberately keep packet timestamps in the recorder's native
 * representation. They do not estimate an audio/video offset, align clips,
 * normalize levels, resample, or make a parity claim.
 */

export const CONTROLLED_AUDIO = Object.freeze({
  sampleRate: 48_000,
  channels: 2,
  durationSeconds: 6,
  webAudioFrequency: 880,
  webAudioAmplitude: 0.2,
  htmlAudioFrequency: 1_320,
  htmlAudioAmplitude: 0.18,
  leftFrequency: 1_760,
  rightFrequency: 1_980,
  channelAmplitude: 0.12,
});

export function nativeAudioChannelDiagnostic(channels) {
  const actualChannels = Number(channels);
  return {
    channels: actualChannels,
    status: actualChannels === 2 ? 'supported' : 'unsupported',
    requirement: 'native ffprobe audiochannels=2',
  };
}

function writeAscii(bytes, offset, value) {
  for (let index = 0; index < value.length; index += 1) bytes[offset + index] = value.charCodeAt(index);
}

/**
 * Build the private fixture's declared PCM source. This is a finite, native
 * 48 kHz stereo signal; it is not a substitute for decoded capture output.
 * @param {{sampleRate?: number, channels?: number, durationSeconds?: number,
 * frequency?: number, amplitude?: number, leftFrequency?: number|null,
 * rightFrequency?: number|null, channelAmplitude?: number}} options
 */
export function createSyntheticPcmWav({
  sampleRate = CONTROLLED_AUDIO.sampleRate,
  channels = CONTROLLED_AUDIO.channels,
  durationSeconds = CONTROLLED_AUDIO.durationSeconds,
  frequency = CONTROLLED_AUDIO.htmlAudioFrequency,
  amplitude = CONTROLLED_AUDIO.htmlAudioAmplitude,
  leftFrequency = null,
  rightFrequency = null,
  channelAmplitude = CONTROLLED_AUDIO.channelAmplitude,
} = {}) {
  if (!Number.isInteger(sampleRate) || sampleRate <= 0 || channels !== 2
    || !Number.isInteger(durationSeconds) || durationSeconds <= 0
    || !Number.isFinite(frequency) || frequency <= 0
    || !Number.isFinite(amplitude) || amplitude <= 0 || amplitude > 1
    || (leftFrequency !== null && (!Number.isFinite(leftFrequency) || leftFrequency <= 0))
    || (rightFrequency !== null && (!Number.isFinite(rightFrequency) || rightFrequency <= 0))
    || (leftFrequency === null) !== (rightFrequency === null)
    || !Number.isFinite(channelAmplitude) || channelAmplitude < 0 || channelAmplitude > 1) {
    throw new Error('Synthetic WAV parameters are invalid');
  }
  const frameCount = sampleRate * durationSeconds;
  const bytes = Buffer.alloc(44 + frameCount * channels * 2);
  writeAscii(bytes, 0, 'RIFF');
  bytes.writeUInt32LE(bytes.length - 8, 4);
  writeAscii(bytes, 8, 'WAVE');
  writeAscii(bytes, 12, 'fmt ');
  bytes.writeUInt32LE(16, 16);
  bytes.writeUInt16LE(1, 20);
  bytes.writeUInt16LE(channels, 22);
  bytes.writeUInt32LE(sampleRate, 24);
  bytes.writeUInt32LE(sampleRate * channels * 2, 28);
  bytes.writeUInt16LE(channels * 2, 32);
  bytes.writeUInt16LE(16, 34);
  writeAscii(bytes, 36, 'data');
  bytes.writeUInt32LE(bytes.length - 44, 40);
  for (let frame = 0; frame < frameCount; frame += 1) {
    const shared = amplitude * Math.sin(2 * Math.PI * frequency * frame / sampleRate);
    for (let channel = 0; channel < channels; channel += 1) {
      const sideFrequency = channel === 0 ? leftFrequency : rightFrequency;
      const side = sideFrequency === null
        ? 0
        : channelAmplitude * Math.sin(2 * Math.PI * sideFrequency * frame / sampleRate);
      bytes.writeInt16LE(Math.round((shared + side) * 32_767), 44 + (frame * channels + channel) * 2);
    }
  }
  return bytes;
}

/** @param {Array<{kind: string, readyState: string}>} tracks
 * @param {{mimeType?: string, requestedAudio?: boolean}} options
 */
export function assertCaptureCapabilities(tracks, {mimeType, requestedAudio = true} = {}) {
  if (!requestedAudio) throw new Error('The probe must request tab audio');
  if (!Array.isArray(tracks)) throw new Error('getDisplayMedia did not return a track list');

  const kinds = tracks.map((track) => track.kind);
  if (kinds.filter((kind) => kind === 'video').length !== 1) {
    throw new Error(`Expected one video track, got ${kinds.join(',') || 'none'}`);
  }
  if (kinds.filter((kind) => kind === 'audio').length !== 1) {
    throw new Error(`Expected one tab audio track, got ${kinds.join(',') || 'none'}`);
  }
  if (tracks.some((track) => track.readyState !== 'live')) {
    throw new Error('A captured track was not live when the recorder started');
  }
  if (typeof mimeType !== 'string' || !mimeType.includes('webm')) {
    throw new Error(`Unexpected MediaRecorder MIME type: ${mimeType ?? ''}`);
  }

  return {videoTracks: 1, audioTracks: 1, mimeType};
}

function finiteTimestamp(packet, field) {
  const value = Number(packet[field]);
  if (!Number.isFinite(value)) throw new Error(`Packet ${field} is not finite`);
  return value;
}

export function assertRawPts(ffprobe) {
  if (!ffprobe || !Array.isArray(ffprobe.streams) || !Array.isArray(ffprobe.packets)) {
    throw new Error('ffprobe output must include streams and packets');
  }
  const streams = ffprobe.streams.filter((stream) => stream.codec_type === 'video' || stream.codec_type === 'audio');
  if (streams.length !== 2 || new Set(streams.map((stream) => stream.codec_type)).size !== 2) {
    throw new Error('The recorder output must contain exactly one video and one audio stream');
  }
  for (const stream of streams) {
    if (typeof stream.time_base !== 'string' || stream.time_base === '0/0') {
      throw new Error(`Missing native time base for ${stream.codec_type}`);
    }
    const packets = ffprobe.packets
      .filter((packet) => Number(packet.stream_index) === Number(stream.index))
      .map((packet) => ({
        pts: finiteTimestamp(packet, 'pts'),
        ptsTime: finiteTimestamp(packet, 'pts_time'),
      }));
    if (packets.length === 0) throw new Error(`No raw PTS packets for ${stream.codec_type}`);
    for (let index = 1; index < packets.length; index += 1) {
      if (packets[index].pts < packets[index - 1].pts) {
        throw new Error(`${stream.codec_type} raw PTS regressed at packet ${index}`);
      }
      if (packets[index].ptsTime < packets[index - 1].ptsTime) {
        throw new Error(`${stream.codec_type} raw PTS time regressed at packet ${index}`);
      }
    }
  }
  return {
    streamCount: streams.length,
    packetCounts: Object.fromEntries(streams.map((stream) => [stream.codec_type,
      ffprobe.packets.filter((packet) => Number(packet.stream_index) === Number(stream.index)).length])),
    timeBases: Object.fromEntries(streams.map((stream) => [stream.codec_type, stream.time_base])),
  };
}

export function assertCaptureOutcome(ffprobe, capabilities) {
  if (capabilities?.videoTracks !== 1 || capabilities?.audioTracks !== 1) {
    throw new Error('Capability result did not retain both tracks');
  }
  const rawPts = assertRawPts(ffprobe);
  if (rawPts.packetCounts.video < 2 || rawPts.packetCounts.audio < 2) {
    throw new Error('The recorder output did not contain enough packets to inspect');
  }
  return {capabilities, rawPts};
}

export function assertVisualEvent(rawVideo, {width, height, preEventRgb, eventRgb} = {}) {
  if (!Buffer.isBuffer(rawVideo) || !Number.isInteger(width) || !Number.isInteger(height)) {
    throw new Error('Decoded visual event region is invalid');
  }
  const frameBytes = width * height * 3;
  if (frameBytes === 0 || rawVideo.byteLength === 0 || rawVideo.byteLength % frameBytes !== 0) {
    throw new Error('Decoded visual event region is not frame-aligned');
  }
  const colors = [preEventRgb, eventRgb];
  if (colors.some((color) => !Array.isArray(color) || color.length !== 3
    || color.some((channel) => !Number.isInteger(channel) || channel < 0 || channel > 255))) {
    throw new Error('Visual event colors are invalid');
  }
  const framesWithColor = colors.map((color) => {
    let count = 0;
    for (let offset = 0; offset < rawVideo.byteLength; offset += frameBytes) {
      let found = false;
      for (let pixel = offset; pixel < offset + frameBytes; pixel += 3) {
        if (rawVideo[pixel] === color[0] && rawVideo[pixel + 1] === color[1] && rawVideo[pixel + 2] === color[2]) {
          found = true;
          break;
        }
      }
      if (found) count += 1;
    }
    return count;
  });
  if (framesWithColor[0] === 0 || framesWithColor[1] === 0) {
    throw new Error('Captured video did not contain both pre-event and event marker colors');
  }
  return {frameCount: rawVideo.byteLength / frameBytes, framesWithPreEventColor: framesWithColor[0], framesWithEventColor: framesWithColor[1]};
}

/**
 * Decode-only marker diagnostics. VP8 is lossy, so exact RGB samples are not
 * evidence of event timing and are intentionally never required here.
 */
export function diagnoseVisualEvent(rawVideo, {width, height, preEventRgb, eventRgb} = {}) {
  if (!Buffer.isBuffer(rawVideo) || !Number.isInteger(width) || !Number.isInteger(height)) {
    throw new Error('Decoded visual event region is invalid');
  }
  const frameBytes = width * height * 3;
  if (frameBytes === 0 || rawVideo.byteLength === 0 || rawVideo.byteLength % frameBytes !== 0) {
    throw new Error('Decoded visual event region is not frame-aligned');
  }
  const colors = [preEventRgb, eventRgb];
  if (colors.some((color) => !Array.isArray(color) || color.length !== 3
    || color.some((channel) => !Number.isInteger(channel) || channel < 0 || channel > 255))) {
    throw new Error('Visual event colors are invalid');
  }
  const exactColorFrameCounts = colors.map((color) => {
    let count = 0;
    for (let offset = 0; offset < rawVideo.byteLength; offset += frameBytes) {
      for (let pixel = offset; pixel < offset + frameBytes; pixel += 3) {
        if (rawVideo[pixel] === color[0] && rawVideo[pixel + 1] === color[1] && rawVideo[pixel + 2] === color[2]) {
          count += 1;
          break;
        }
      }
    }
    return count;
  });
  return {
    frameCount: rawVideo.byteLength / frameBytes,
    exactColorFrameCounts,
    phaseClaim: false,
    diagnosticOnly: true,
  };
}

export function assertTone(samples, {sampleRate, channels, frequency}) {
  if (!(samples instanceof Float32Array) || samples.length === 0) throw new Error('Decoded audio is empty');
  if (!Number.isInteger(sampleRate) || sampleRate <= 0 || !Number.isInteger(channels) || channels < 1) {
    throw new Error('Decoded audio format is invalid');
  }
  const sampleCount = Math.floor(samples.length / channels);
  const measurements = [];
  for (let channel = 0; channel < channels; channel += 1) {
    let sin = 0;
    let cos = 0;
    for (let index = 0; index < sampleCount; index += 1) {
      const phase = 2 * Math.PI * frequency * index / sampleRate;
      const value = samples[index * channels + channel];
      sin += value * Math.sin(phase);
      cos += value * Math.cos(phase);
    }
    measurements.push(2 * Math.hypot(sin, cos) / sampleCount);
  }
  if (measurements.some((amplitude) => !Number.isFinite(amplitude) || amplitude < 0.001)) {
    throw new Error(`Controlled ${frequency} Hz tone was not present in every captured channel`);
  }
  return {sampleRate, channels, frequency, amplitudes: measurements};
}

function measureTone(samples, {sampleRate, channels, frequency, channel}) {
  const sampleCount = samples.length / channels;
  let sin = 0;
  let cos = 0;
  for (let index = 0; index < sampleCount; index += 1) {
    const phase = 2 * Math.PI * frequency * index / sampleRate;
    const value = samples[index * channels + channel];
    sin += value * Math.sin(phase);
    cos += value * Math.cos(phase);
  }
  return 2 * Math.hypot(sin, cos) / sampleCount;
}

/**
 * Detect the deliberately separated left/right source without downmixing.
 * A mono recorder output is a refusal, not stereo evidence.
 */
export function assertStereoTones(samples, {
  sampleRate,
  channels,
  leftFrequency,
  rightFrequency,
  minAmplitude = 0.001,
  maxLeakage = 0.02,
  maxLeakageRatio = 0.25,
}) {
  if (!(samples instanceof Float32Array) || samples.length === 0
    || !Number.isInteger(sampleRate) || sampleRate <= 0
    || channels !== 2 || samples.length % channels !== 0) {
    throw new Error('Stereo detector requires exactly two interleaved channels');
  }
  for (const [name, frequency] of [['left', leftFrequency], ['right', rightFrequency]]) {
    if (!Number.isFinite(frequency) || frequency <= 0) throw new Error(`Invalid ${name} detector frequency`);
  }
  const left = measureTone(samples, {sampleRate, channels, frequency: leftFrequency, channel: 0});
  const leftLeakage = measureTone(samples, {sampleRate, channels, frequency: leftFrequency, channel: 1});
  const right = measureTone(samples, {sampleRate, channels, frequency: rightFrequency, channel: 1});
  const rightLeakage = measureTone(samples, {sampleRate, channels, frequency: rightFrequency, channel: 0});
  if (left < minAmplitude || right < minAmplitude) {
    throw new Error(`Separated L/R tones were not present in their expected channels: ${left}/${right}`);
  }
  if (leftLeakage > maxLeakage || rightLeakage > maxLeakage
    || leftLeakage > left * maxLeakageRatio || rightLeakage > right * maxLeakageRatio) {
    throw new Error(`Separated L/R tones leaked across channels: ${leftLeakage}/${rightLeakage}`);
  }
  return {
    sampleRate,
    channels,
    leftFrequency,
    rightFrequency,
    amplitudes: {left, right},
    leakage: {leftIntoRight: leftLeakage, rightIntoLeft: rightLeakage},
    controls: {minAmplitude, maxLeakage, maxLeakageRatio},
  };
}
