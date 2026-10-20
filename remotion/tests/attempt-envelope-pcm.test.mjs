import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync} from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {afterEach, beforeEach, describe, expect, it, vi} from 'vitest';
import {TimelineComposition, compileCanonicalTransitions, DEFAULT_THEME} from '@banodoco/timeline-composition';
import {applyAudioEnvelope, audioEnvelopeWav, compileAudioEnvelope} from '@banodoco/timeline-composition/evaluation';
import {prepareAttemptEnvelopePcm} from '../attempt-envelope-pcm.mjs';

const host = vi.hoisted(() => ({fps: 30, endpoints: []}));
// Media and frame-context primitives only. Public AudioTrack, envelope admission,
// trim/rate derivation and scalar gain execute unchanged; no browser or HTTP IO.
vi.mock('remotion', async importOriginal => ({
  ...await importOriginal(),
  AbsoluteFill: ({children}) => children,
  Sequence: ({children}) => children,
  useCurrentFrame: () => 0,
  useVideoConfig: () => ({fps: host.fps, width: 32, height: 32}),
  getRemotionEnvironment: () => ({isPlayer: false, isRendering: true}),
  useBufferState: () => ({}),
  Audio: props => { host.endpoints.push(props); return null; },
}));

let scratch, source, attemptDirectory;
const sampleRate = 30000, samples = 30000;
const clip = overrides => ({
  id: 'sound', track: 'A1', asset: 'sound', at: 0.25, from: 0, to: 1,
  hold: 0.4, params: {fadeIn: 0.2}, ...overrides,
});
const unityClock = {source_from: 0, playback_rate: 1};
const prepare = (authored, sourceClock = unityClock, options = {}) => prepareAttemptEnvelopePcm({
  clip: authored, fps: host.fps, source, attemptDirectory, sourceClock, ...options,
});

// Independent PCM16 input, with unequal channels. The preparation must perform
// actual decoding before using the public floating-point envelope/WAV helpers.
const pcm16 = () => {
  const bytes = Buffer.alloc(44 + samples * 4);
  bytes.write('RIFF'); bytes.writeUInt32LE(bytes.length - 8, 4); bytes.write('WAVEfmt ', 8);
  bytes.writeUInt32LE(16, 16); bytes.writeUInt16LE(1, 20); bytes.writeUInt16LE(2, 22);
  bytes.writeUInt32LE(sampleRate, 24); bytes.writeUInt32LE(sampleRate * 4, 28);
  bytes.writeUInt16LE(4, 32); bytes.writeUInt16LE(16, 34);
  bytes.write('data', 36); bytes.writeUInt32LE(samples * 4, 40);
  for (let i = 0; i < samples; i++) {
    bytes.writeInt16LE(8192, 44 + i * 4); bytes.writeInt16LE(-4096, 46 + i * 4);
  }
  return bytes;
};
const wav = prepared => {
  const bytes = readFileSync(prepared.path);
  expect(bytes.toString('ascii', 0, 4)).toBe('RIFF');
  expect(bytes.readUInt16LE(20)).toBe(3); // IEEE float, including >unity samples.
  expect(bytes.readUInt16LE(22)).toBe(2);
  expect(bytes.readUInt32LE(24)).toBe(sampleRate);
  expect(bytes.readUInt16LE(34)).toBe(32);
  expect(bytes.length).toBe(44 + samples * 8);
  return (sample, channel = 0) => bytes.readFloatLE(44 + (sample * 2 + channel) * 4);
};
const endpoint = (authored, prepared, track = {}) => {
  host.endpoints.length = 0;
  const runtimeClip = {...authored, audio: {...authored.audio, render_source: {
    file: 'http://attempt.invalid/envelope/source.wav', envelope_key: prepared.envelope_key,
    source_from: prepared.source_from, playback_rate: prepared.playback_rate,
  }}};
  renderToStaticMarkup(createElement(TimelineComposition, {
    timeline: {theme: 'default', tracks: [{id: 'A1', kind: 'audio', ...track}], clips: [runtimeClip]},
    assets: {assets: {sound: {type: 'audio/wav', file: 'http://attempt.invalid/original.wav'}}},
    compiledTransitions: compileCanonicalTransitions([], host.fps, DEFAULT_THEME),
  }));
  expect(host.endpoints).toHaveLength(1);
  return host.endpoints[0];
};

beforeEach(() => {
  host.fps = 30;
  scratch = mkdtempSync(path.join(os.tmpdir(), 'attempt-envelope-test-'));
  source = path.join(scratch, 'source.wav');
  attemptDirectory = path.join(scratch, 'attempt');
  mkdirSync(attemptDirectory);
  writeFileSync(source, pcm16());
});
afterEach(() => rmSync(scratch, {recursive: true, force: true}));

describe('inactive attempt PCM preparation with public package semantics', () => {
  it.each([
    ['linear', 0.5], ['equal-power', 0.7071067811865476],
    ['exponential-fast', 0.8175744761936437], ['exponential-moderate', 0.320821300824607],
    ['exponential-slow', 0.18242552380635635], ['s-curve', 0.5],
  ])('decodes both channels and applies the %s params curve once', (curve, halfway) => {
    const authored = clip({params: {fadeIn: 0.2, fadeInCurve: curve}});
    const prepared = prepare(authored), sample = wav(prepared);
    expect(sample(0)).toBe(0);
    expect(sample(3000)).toBeCloseTo(0.25 * halfway, 7);
    expect(sample(3000, 1)).toBeCloseTo(-0.125 * halfway, 7);
    expect(sample(6000)).toBe(0.25);
    expect(endpoint(authored, prepared)).toMatchObject({
      src: 'http://attempt.invalid/envelope/source.wav', trimBefore: 0, trimAfter: 30,
      playbackRate: 1, volume: 1,
    });
    if (curve === 's-curve') expect(sample(1500)).toBeCloseTo(0.25 * 0.15625, 7);
  });

  it('multiplies overlapping params fades without adding track/clip gain or mute', () => {
    const authored = clip({hold: 0.2, volume: 3, params: {fadeIn: 0.2, fadeOut: 0.2}});
    const prepared = prepare(authored), sample = wav(prepared);
    expect(sample(0)).toBe(0);
    expect(sample(3000)).toBe(0.0625);
    expect(sample(6000)).toBe(0);
    expect(endpoint(authored, prepared, {volume: 2}).volume).toBe(6);
    expect(endpoint(authored, prepared, {volume: 2, muted: true}).volume).toBe(0);
    expect(endpoint({...authored, volume: 0}, prepared).volume).toBe(0);
  });

  it.each([
    [30, 1 / 15, 2000, 3000],
    [30000 / 1001, 1001 / 15000, 2002, 3003],
  ])('retains the whole source and public rounded origin/rate at fps %s', (fps, origin, start, halfFade) => {
    host.fps = fps;
    const authored = clip({from: 0.051, to: 0.9, hold: 0.6, speed: 2,
      params: {fadeIn: 0.1, fadeOut: 0.1}});
    const clock = {source_from: origin, playback_rate: 2};
    const prepared = prepare(authored, clock), sample = wav(prepared);
    const media = endpoint(authored, prepared);
    // The literals above are checked against actual public trim/rate output,
    // rather than implementing its rounding/sanitization in this helper.
    expect(media.trimBefore).toBe(2);
    expect(media.trimBefore / fps).toBe(origin);
    expect(media.trimAfter).toBe(27);
    expect(media.playbackRate).toBe(clock.playback_rate);
    expect(sample(0)).toBe(0);
    expect(sample(start)).toBeCloseTo(0, 7);
    expect(sample(start + halfFade)).toBeCloseTo(0.125, 7);
    expect(sample(start + 2 * halfFade)).toBeCloseTo(0.25, 7);
    expect(sample(start + 5 * halfFade)).toBeCloseTo(0.125, 7);
    expect(sample(samples - 1)).toBe(0);
    const reference = [new Float32Array(samples).fill(0.25), new Float32Array(samples).fill(-0.125)];
    applyAudioEnvelope(reference, sampleRate, compileAudioEnvelope(authored, fps), origin, 2);
    expect(readFileSync(prepared.path)).toEqual(Buffer.from(audioEnvelopeWav(reference, sampleRate)));
  });

  it('keeps authored boost, multiply/minimum, channel order and PCM latency without clipping', () => {
    const authored = clip({volume: 2, audio: {envelope: {
      keyframes: [{at: 0, value: 4}],
      multiply: [{keyframes: [{at: 0, value: 3}]}],
      minimum: [{keyframes: [{at: 0, value: 0.5}]}, {keyframes: [{at: 0, value: 1}]}],
    }}});
    const input = pcm16();
    input.writeInt16LE(16384, 44 + 17 * 4);
    input.writeInt16LE(-8192, 46 + 29 * 4);
    writeFileSync(source, input);
    const prepared = prepare(authored), sample = wav(prepared);
    expect(sample(0)).toBe(1.5);
    expect(sample(17)).toBe(3);
    expect(sample(18)).toBe(1.5);
    expect(sample(29, 1)).toBe(-1.5);
    expect(sample(30, 1)).toBe(-0.75);
    const decoded = execFileSync('ffmpeg', ['-v', 'error', '-nostdin', '-i', prepared.path,
      '-map', '0:a:0', '-c:a', 'pcm_f32le', '-f', 'f32le', 'pipe:1'],
    {stdio: ['ignore', 'pipe', 'pipe'], timeout: 30000});
    expect(decoded.length).toBe(samples * 8);
    expect(decoded.readFloatLE(17 * 8)).toBe(3);
    expect(decoded.readFloatLE(29 * 8 + 4)).toBe(-1.5);
    expect(endpoint(authored, prepared, {volume: 1.5}).volume).toBe(3);
  });

  it('accepts actual prepared metadata and rejects wrong keys and source clocks in the public consumer', () => {
    const authored = clip({from: 0.051, speed: 2});
    const prepared = prepare(authored, {source_from: 1 / 15, playback_rate: 2});
    expect(endpoint(authored, prepared).src).toBe('http://attempt.invalid/envelope/source.wav');
    for (const wrong of [{envelope_key: '{}'}, {envelope_key: '['},
      {source_from: 0.051}, {playback_rate: 1}]) {
      expect(() => endpoint(authored, {...prepared, ...wrong})).toThrow(/ENVELOPE_UNRENDERED/);
    }
  });

  it('leaves input bytes/graph intact and allocates a fresh attempt file for each call', () => {
    const authored = clip(), before = JSON.stringify(authored);
    const digest = () => createHash('sha256').update(readFileSync(source)).digest('hex');
    const original = digest(), first = prepare(authored), second = prepare(authored);
    expect(first.path).not.toBe(second.path);
    expect(path.relative(attemptDirectory, first.path)).not.toMatch(/^\.\./);
    expect(readFileSync(first.path)).toEqual(readFileSync(second.path));
    expect(digest()).toBe(original);
    expect(JSON.stringify(authored)).toBe(before);
  });

  it('does no IO for clips without an envelope, including the existing effects-only shape', () => {
    expect(prepare(clip({params: {}, effects: [{fade_in: 0.1, fade_out: 0.1}]}), undefined,
      {source: '/does-not-exist.wav'})).toBeUndefined();
    expect(readdirSync(attemptDirectory)).toEqual([]);
  });

  it('refuses unresolved ducking and invalid curves before decoding or writing', () => {
    expect(() => prepare(clip({app: {astrid: {duck: {}}}}))).toThrow(/DUCK_UNRENDERED/);
    expect(() => prepare(clip({params: {fadeIn: 0.2, fadeInCurve: 'unknown'}}))).toThrow(/ENVELOPE_UNRENDERED/);
    expect(readdirSync(attemptDirectory)).toEqual([]);
  });

  it('refuses absent clocks, prepared inputs, missing sources and bounded-decode overflow without fallback', () => {
    expect(() => prepare(clip(), null)).toThrow(/public source clock required/);
    expect(() => prepare(clip({audio: {render_source: {}}}))).toThrow(/source already prepared/);
    expect(() => prepare(clip(), unityClock, {source: path.join(scratch, 'missing.wav')})).toThrow();
    expect(() => prepare(clip(), unityClock, {maxDecodedBytes: 16})).toThrow();
    expect(readdirSync(attemptDirectory)).toEqual([]);
  });
});
