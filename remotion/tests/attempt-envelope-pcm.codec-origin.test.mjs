import {execFileSync} from 'node:child_process';
import {mkdtempSync, rmSync} from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {afterAll, beforeAll, describe, expect, it} from 'vitest';

const run = (program, args, maxBuffer = 64 * 1024 * 1024) => execFileSync(program, args, {
  maxBuffer, stdio: ['ignore', 'pipe', 'pipe'], timeout: 30000,
});
const probe = file => JSON.parse(run('ffprobe', [
  '-v', 'error', '-show_entries',
  'format=format_name,duration,start_time:stream=index,codec_name,codec_type,sample_rate,channels,time_base,start_pts,start_time,duration,nb_frames,initial_padding',
  '-show_entries', 'stream_tags', '-of', 'json', file,
]).toString());

const firstPacket = file => JSON.parse(run('ffprobe', [
  '-v', 'error', '-select_streams', 'a:0', '-show_packets', '-read_intervals', '%+#1',
  '-show_entries', 'packet=pts,pts_time,dts,dts_time,duration,duration_time,side_data_list',
  '-of', 'json', file,
]).toString()).packets?.[0] ?? {};

const decode = file => run('ffmpeg', [
  '-v', 'error', '-nostdin', '-i', file, '-map', '0:a:0', '-threads', '1',
  '-c:a', 'pcm_f32le', '-f', 'f32le', 'pipe:1',
]);

const stream = metadata => metadata.streams.find(candidate => candidate.codec_type === 'audio');
const firstSkipSamples = packet => packet.side_data_list?.find(data =>
  data.side_data_type === 'Skip Samples')?.skip_samples ?? 0;

const channels = (bytes, channelCount) => {
  const sampleCount = bytes.length / (channelCount * 4);
  const output = Array.from({length: channelCount}, () => new Float32Array(sampleCount));
  for (let sample = 0; sample < sampleCount; sample++) {
    for (let channel = 0; channel < channelCount; channel++) {
      output[channel][sample] = bytes.readFloatLE((sample * channelCount + channel) * 4);
    }
  }
  return output;
};

const onset = (samples, threshold = 0.03) => {
  for (let sample = 0; sample < samples.length; sample++) {
    if (Math.abs(samples[sample]) > threshold) return sample;
  }
  return -1;
};

const fixtureNames = [
  'source.aac', 'source.mp3', 'source.m4a', 'source-offset.mka',
  'video.mp4', 'video-offset.mp4',
];
let scratch;
let source;
let fixtures;
let observations;

beforeAll(() => {
  scratch = mkdtempSync(path.join(os.tmpdir(), 'attempt-envelope-codec-origin-'));
  const left = path.join(scratch, 'left.wav');
  const right = path.join(scratch, 'right.wav');
  source = path.join(scratch, 'source.wav');
  // The delayed, unequal stereo tones give an origin marker on each channel
  // without relying on a codec-sensitive impulse or a generated sample file.
  run('ffmpeg', [
    '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=1.6',
    '-af', 'adelay=200:all=1,volume=0.8', '-t', '2', '-c:a', 'pcm_s16le', left,
  ]);
  run('ffmpeg', [
    '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=660:sample_rate=48000:duration=1.6',
    '-af', 'adelay=300:all=1,volume=-0.6', '-t', '2', '-c:a', 'pcm_s16le', right,
  ]);
  run('ffmpeg', [
    '-v', 'error', '-i', left, '-i', right, '-filter_complex', '[0:a][1:a]amerge=inputs=2[a]',
    '-map', '[a]', '-ar', '48000', '-t', '2', '-c:a', 'pcm_s16le', source,
  ]);

  run('ffmpeg', ['-v', 'error', '-i', source, '-c:a', 'aac', '-b:a', '128k', '-f', 'adts',
    path.join(scratch, 'source.aac')]);
  run('ffmpeg', ['-v', 'error', '-i', source, '-c:a', 'libmp3lame', '-b:a', '128k',
    path.join(scratch, 'source.mp3')]);
  run('ffmpeg', ['-v', 'error', '-i', source, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
    path.join(scratch, 'source.m4a')]);
  // Remuxing the AAC into Matroska deliberately retains a positive container
  // timestamp but does not preserve the MP4 skip-samples side data.
  run('ffmpeg', ['-v', 'error', '-itsoffset', '0.125', '-i', path.join(scratch, 'source.m4a'),
    '-map', '0:a:0', '-c', 'copy', path.join(scratch, 'source-offset.mka')]);
  run('ffmpeg', [
    '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=160x90:rate=30000/1001:duration=1.8',
    '-i', source, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'ultrafast',
    '-tune', 'zerolatency', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest',
    path.join(scratch, 'video.mp4'),
  ]);
  // The audio input offset is intentionally retained; this is the video case
  // whose AAC stream has a nonzero start but no skip-samples side data.
  run('ffmpeg', [
    '-v', 'error', '-itsoffset', '0.125', '-i', source, '-f', 'lavfi',
    '-i', 'testsrc2=size=160x90:rate=30000/1001:duration=1.8', '-map', '1:v:0', '-map', '0:a:0',
    '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '128k', '-shortest', path.join(scratch, 'video-offset.mp4'),
  ]);

  const reference = channels(decode(source), 2);
  fixtures = Object.fromEntries(fixtureNames.map(name => {
    const file = path.join(scratch, name);
    const metadata = probe(file);
    const audio = stream(metadata);
    const decoded = channels(decode(file), Number(audio.channels));
    return [name, {
      audio, packet: firstPacket(file), decoded,
      sampleCount: decoded[0].length,
      onset: decoded.map(channel => onset(channel)),
    }];
  }));
  observations = {reference, referenceOnset: reference.map(channel => onset(channel))};
});

afterAll(() => rmSync(scratch, {recursive: true, force: true}));

describe('inactive attempt PCM decoder-origin characterization', () => {
  it('generates stereo compressed fixtures with their actual stream clocks', () => {
    expect(observations.reference).toHaveLength(2);
    expect(observations.reference[0]).toHaveLength(86400);
    expect(observations.referenceOnset).toEqual([9606, 14405]);
    expect(Object.keys(fixtures)).toEqual(fixtureNames);
    expect(fixtures['source.aac'].audio).toMatchObject({
      codec_name: 'aac', sample_rate: '48000', channels: 2, time_base: '1/28224000',
    });
    expect(fixtures['source.aac'].audio).not.toHaveProperty('start_time');
    expect(fixtures['source.mp3'].audio).toMatchObject({
      codec_name: 'mp3', sample_rate: '48000', channels: 2, time_base: '1/14112000',
      start_time: '0.023021',
    });
    expect(fixtures['source.m4a'].audio).toMatchObject({
      codec_name: 'aac', sample_rate: '48000', channels: 2, time_base: '1/48000',
      start_time: '0.000000',
    });
    expect(fixtures['source-offset.mka'].audio).toMatchObject({
      codec_name: 'aac', sample_rate: '48000', channels: 2, time_base: '1/1000',
      start_time: '0.104000',
    });
    expect(fixtures['video.mp4'].audio).toMatchObject({
      codec_name: 'aac', sample_rate: '48000', channels: 2, time_base: '1/48000',
      start_time: '0.000000',
    });
    expect(fixtures['video-offset.mp4'].audio).toMatchObject({
      codec_name: 'aac', sample_rate: '48000', channels: 2, time_base: '1/48000',
      start_time: '0.103000',
    });
  });

  it('records decoder priming metadata separately from stream start', () => {
    expect(firstSkipSamples(fixtures['source.aac'].packet)).toBe(0);
    expect(firstSkipSamples(fixtures['source.mp3'].packet)).toBe(1105);
    expect(firstSkipSamples(fixtures['source.m4a'].packet)).toBe(1024);
    expect(firstSkipSamples(fixtures['source-offset.mka'].packet)).toBe(0);
    expect(firstSkipSamples(fixtures['video.mp4'].packet)).toBe(1024);
    expect(firstSkipSamples(fixtures['video-offset.mp4'].packet)).toBe(0);
    expect(fixtures['source.mp3'].packet.pts_time).toBe('0.000000');
    expect(fixtures['source.m4a'].packet.pts_time).toBe('-0.021333');
    expect(fixtures['source-offset.mka'].packet.pts_time).toBe('0.104000');
  });

  it('compares full decoded stereo count and onset against the original PCM', () => {
    const expected = {
      'source.aac': {samples: 88064, onset: [10630, 15429]},
      'source.mp3': {samples: 86400, onset: [9606, 14406]},
      'source.m4a': {samples: 87040, onset: [9606, 14405]},
      'source-offset.mka': {samples: 88064, onset: [10630, 15429]},
      'video.mp4': {samples: 87040, onset: [9606, 14405]},
      'video-offset.mp4': {samples: 80896, onset: [10630, 15429]},
    };
    for (const name of fixtureNames) {
      const result = fixtures[name];
      expect(result.sampleCount, name).toBe(expected[name].samples);
      expect(result.onset, name).toEqual(expected[name].onset);
    }
  });

  it('shows which nonzero starts preserve PCM onset and which shift it', () => {
    const onsetDelta = name => fixtures[name].onset.map((sample, channel) =>
      sample - observations.referenceOnset[channel]);
    expect(onsetDelta('source.mp3')).toEqual([0, 1]);
    expect(onsetDelta('source-offset.mka')).toEqual([1024, 1024]);
    expect(onsetDelta('video-offset.mp4')).toEqual([1024, 1024]);
    expect(Number(fixtures['source.mp3'].audio.start_time) * 48000).toBeCloseTo(1105, 1);
    expect(Number(fixtures['source-offset.mka'].audio.start_time) * 48000).toBeCloseTo(4992, 6);
    expect(Number(fixtures['video-offset.mp4'].audio.start_time) * 48000).toBeCloseTo(4944, 6);
  });

  it('keeps rational timeline clocks explicit without deriving source policy', () => {
    const fps = 30000 / 1001;
    const sourceFrom = 7 * 1001 / 30000;
    const playbackRate = 3 / 2;
    expect(fps).toBeCloseTo(29.97002997002997, 14);
    expect(sourceFrom).toBeCloseTo(0.23356666666666666, 14);
    expect(playbackRate).toBe(1.5);
    for (const name of fixtureNames) {
      expect(fixtures[name].audio.sample_rate, name).toBe('48000');
      expect(fixtures[name].audio.channels, name).toBe(2);
    }
  });
});
