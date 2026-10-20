// @vitest-environment node
import { execFileSync, type ExecFileSyncOptionsWithBufferEncoding } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import type { TimelineClip } from '@banodoco/timeline-composition';
import {
  applyAudioEnvelope, audioEnvelopeAt, audioEnvelopeWav, compileAudioEnvelope,
  type AudioCurve, type AudioEnvelope,
} from '@banodoco/timeline-composition/evaluation';

// 03:20 policy for BOTH App preview and normal Agent export. These are shared
// PCM goldens, not evidence that either consumer's preparation is wired.
// Identity fixture clock only; occurrence clocks await Agent's compiled contract.
const clock = { sourceFrom: 0, playbackRate: 1 } as const;
const clip = (overrides: Partial<TimelineClip> = {}): TimelineClip => ({
  id: 'continuous-pcm', track: 'A1', asset: 'source', at: 0, from: 0, to: 1,
  speed: clock.playbackRate, hold: 1, ...overrides,
});

function bake(input: readonly Float32Array[], rate: number, envelope: AudioEnvelope) {
  const output = input.map(channel => channel.slice());
  applyAudioEnvelope(output, rate, envelope, clock.sourceFrom, clock.playbackRate);
  return output;
}

// Same FFprobe/FFmpeg readback used by the attempt-PCM tests. Decode the entire
// float WAV at its original rate/channels: no resample, normalize, shift or trim.
function decode(channels: readonly Float32Array[], rate: number) {
  const directory = mkdtempSync(join(tmpdir(), 'continuous-pcm-'));
  try {
    const file = join(directory, 'source.wav');
    writeFileSync(file, Buffer.from(audioEnvelopeWav(channels, rate)));
    const options: ExecFileSyncOptionsWithBufferEncoding = { stdio: ['ignore', 'pipe', 'pipe'], timeout: 30_000 };
    const probe = JSON.parse(execFileSync('ffprobe', [
      '-v', 'error', '-show_streams', '-of', 'json', file,
    ], options).toString());
    expect(probe.streams).toHaveLength(1);
    expect(probe.streams[0]).toMatchObject({
      codec_name: 'pcm_f32le', sample_rate: String(rate), channels: channels.length,
    });
    const raw = execFileSync('ffmpeg', [
      '-v', 'error', '-nostdin', '-i', file, '-map', '0:a:0',
      '-c:a', 'pcm_f32le', '-f', 'f32le', 'pipe:1',
    ], { ...options, maxBuffer: 4 * 1024 * 1024 });
    expect(raw.length).toBe(channels[0].length * channels.length * 4);
    return channels.map((channel, index) => Float32Array.from(channel, (_, sample) =>
      raw.readFloatLE((sample * channels.length + index) * 4)));
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

// The reference queries the public evaluator at EVERY source sample. Identity
// clocks make sample/rate the declared clip-local time; no frame-table rounding.
function reference(input: readonly Float32Array[], rate: number, envelope: AudioEnvelope) {
  return input.map(channel => Float32Array.from(channel, (value, sample) =>
    value * audioEnvelopeAt(envelope, sample / rate)));
}

const clocks = [
  { fps: 30, rate: 44_100 }, { fps: 30, rate: 48_000 },
  { fps: 30_000 / 1001, rate: 44_100 }, { fps: 30_000 / 1001, rate: 48_000 },
];

describe('shared continuous PCM goldens: App preview + normal Agent export', () => {
  for (const { fps, rate } of clocks) {
    for (const curve of ['linear', 'equal-power', 's-curve'] as const satisfies readonly AudioCurve[]) {
      it(`${fps}fps / ${rate}Hz: ${curve} overlapping fades match every decoded source sample`, () => {
        const authored = clip({ hold: 0.2, params: {
          fadeIn: 0.2, fadeOut: 0.2, fadeInCurve: curve, fadeOutCurve: curve,
        } });
        const before = JSON.stringify(authored);
        const envelope = compileAudioEnvelope(authored, fps)!;
        const input = [new Float32Array(rate).fill(0.25), new Float32Array(rate).fill(-0.125)];
        const original = input.map(channel => channel.slice());
        const actual = decode(bake(input, rate, envelope), rate);
        expect(actual).toEqual(reference(input, rate, envelope));
        expect(input).toEqual(original);
        expect(JSON.stringify(authored)).toBe(before);
        expect(actual[0][0]).toBe(0);
        expect(actual[0][rate - 1]).toBe(0);
        // Literal independent landmarks at 30fps; the rational-fps plan is
        // queried as compiled, rather than copying its frame rounding policy.
        if (fps === 30) {
          const halfway = curve === 'equal-power' ? 0.5 : 0.25;
          expect(actual[0][rate / 10]).toBeCloseTo(0.25 * halfway, 7);
          if (curve === 's-curve') expect(actual[0][rate / 20]).toBeCloseTo(0.25 * 0.15625 * 0.84375, 7);
        }
      });
    }
  }

  it.each(clocks)('$fps fps / $rate Hz: keeps unequal channel impulses at their source sample indices', ({ fps, rate }) => {
    const envelope = compileAudioEnvelope(clip({ params: { fadeIn: 0.2 } }), fps)!;
    const input = [new Float32Array(rate), new Float32Array(rate)];
    input[0][17] = 0.5;
    input[1][29] = -0.25;
    input[0][rate - 1] = -0.75;
    const actual = decode(bake(input, rate, envelope), rate);
    expect(actual).toEqual(reference(input, rate, envelope));
    expect(Array.from(actual[0]).flatMap((value, index) => value ? [index] : [])).toEqual([17, rate - 1]);
    expect(Array.from(actual[1]).flatMap((value, index) => value ? [index] : [])).toEqual([29]);
  });

  it('retains >unity envelope boosts in float WAV while constant base gain stays separate', () => {
    const authored = clip({ volume: 3, audio: { envelope: {
      keyframes: [{ at: 0, value: 4 }],
      multiply: [{ keyframes: [{ at: 0, value: 3 }] }],
      minimum: [{ keyframes: [{ at: 0, value: 0.5 }] }, { keyframes: [{ at: 0, value: 1 }] }],
    } } });
    const envelope = compileAudioEnvelope(authored, 30)!;
    expect(compileAudioEnvelope({ ...authored, volume: 1 }, 30)).toEqual(envelope);
    expect(compileAudioEnvelope(clip({ volume: 3 }), 30)).toBeUndefined();
    const input = [new Float32Array(48_000).fill(0.5), new Float32Array(48_000).fill(-0.25)];
    const actual = decode(bake(input, 48_000, envelope), 48_000);
    expect(actual).toEqual(reference(input, 48_000, envelope));
    expect(actual[0][17]).toBe(3);
    expect(actual[1][29]).toBe(-1.5);
  });

  it('detects a twice-applied envelope independently of the once-baked reference', () => {
    const envelope = compileAudioEnvelope(clip({ params: { fadeIn: 0.2 } }), 30)!;
    const input = [new Float32Array(48_000).fill(0.25)];
    const once = bake(input, 48_000, envelope);
    expect(decode(once, 48_000)).toEqual(reference(input, 48_000, envelope));
    expect(once[0][4800]).toBe(0.125);
    const twice = bake(once, 48_000, envelope);
    expect(twice[0][4800]).toBe(0.0625);
    expect(twice).not.toEqual(once);
  });

  it('DELIBERATE policy change: frame 3.25 is +0.69524dB above the retired frame-3 step hold', () => {
    const envelope = compileAudioEnvelope(clip({ to: 3, hold: 3,
      params: { fadeIn: 0.6, fadeOut: 0.6 } }), 30)!;
    const output = bake([new Float32Array(3 * 48_000).fill(1)], 48_000, envelope);
    // Retained marker starts at source sample 5200 = frame 3.25. Base gain x2
    // remains downstream; the old table's frame-3 value is exactly 1/3.
    const queried = 2 * audioEnvelopeAt(envelope, 5200 / 48_000);
    expect(queried).toBeCloseTo(3.25 / 9, 15);
    expect(20 * Math.log10(queried / (1 / 3))).toBeCloseTo(0.6952421251842384, 12);
    const continuous = 2 * output[0][5200];
    expect(continuous).toBeCloseTo(3.25 / 9, 7);
    expect(20 * Math.log10(continuous / (1 / 3))).toBeCloseTo(0.6952421251842384, 5);
    expect(20 * Math.log10(continuous / (1 / 3))).toBeGreaterThan(0.5);
  });
});
