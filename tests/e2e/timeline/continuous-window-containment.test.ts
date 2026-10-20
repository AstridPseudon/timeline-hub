import {createHash} from 'node:crypto';
import {describe, expect, it} from 'vitest';
import {applyAudioEnvelope, audioEnvelopeAt, compileAudioEnvelope} from '@banodoco/timeline-composition/evaluation';

const PROPOSAL_RATE = 48_000;
const WINDOW_SAMPLES = 200;
const PROPOSAL_MARKERS = Array.from({length: 6}, (_, index) => ({
  first: 12_000 + 800 * index,
  last: 12_600 + 800 * index,
  frequency: 1_200 + 240 * index,
}));
const MARKER_SECONDS = PROPOSAL_MARKERS.map((marker) => ({
  first: marker.first / PROPOSAL_RATE,
  last: marker.last / PROPOSAL_RATE,
  frequency: marker.frequency,
}));
const SOURCE_DURATION_SECONDS = 0.4;

const CASES = [
  {
    name: '30fps-trim-rate-one',
    sampleRate: 48_000,
    fps: 30,
    from: 0.25,
    to: 0.45,
    speed: 1,
    fadeIn: 0.02,
    fadeOut: 0.02,
    fadeInCurve: 'linear',
    fadeOutCurve: 'linear',
  },
  {
    name: 'rationalfps-trim-rate-one-point-five-overlap',
    sampleRate: 48_000,
    fps: 30_000 / 1_001,
    from: 0.24,
    to: 0.46,
    speed: 1.5,
    fadeIn: 0.16,
    fadeOut: 0.15,
    fadeInCurve: 'equal-power',
    fadeOutCurve: 's-curve',
  },
  {
    name: 'rationalfps-44k-trim-rate-three-quarters-overlap',
    sampleRate: 44_100,
    fps: 30_000 / 1_001,
    from: 0.249,
    to: 0.46,
    speed: 0.75,
    fadeIn: 0.12,
    fadeOut: 0.12,
    fadeInCurve: 's-curve',
    fadeOutCurve: 'equal-power',
  },
] as const;

type Marker = {first: number; last: number; frequency: number};
type Window = {marker: number; first: number; last: number; phase: number};

const markersAtRate = (sampleRate: number): Marker[] => MARKER_SECONDS.map((marker) => ({
  first: Math.round(marker.first * sampleRate),
  last: Math.round(marker.last * sampleRate),
  frequency: marker.frequency,
}));

const sourceFor = (sampleRate: number): Float32Array[] => {
  const channels = [
    new Float32Array(Math.ceil(SOURCE_DURATION_SECONDS * sampleRate)),
    new Float32Array(Math.ceil(SOURCE_DURATION_SECONDS * sampleRate)),
  ];
  const markers = markersAtRate(sampleRate);
  for (let sample = 0; sample < channels[0].length; sample++) {
    const marker = markers.find((candidate) => sample >= candidate.first && sample < candidate.last);
    if (!marker) continue;
    const value = 0.5 * Math.sin(2 * Math.PI * marker.frequency * sample / sampleRate);
    channels[0][sample] = value;
    channels[1][sample] = value * 0.75;
  }
  return channels;
};

const fixedWindows = (markers: readonly Marker[], phase: number): Window[] => markers.flatMap((marker, markerIndex) => {
  const windows: Window[] = [];
  for (let first = phase; first + WINDOW_SAMPLES <= marker.last; first += WINDOW_SAMPLES) {
    if (first < marker.first) continue;
    windows.push({marker: markerIndex, first, last: first + WINDOW_SAMPLES, phase});
  }
  return windows;
});

const isInsideMarker = (markers: readonly Marker[], sample: number): boolean => markers.some((marker) => (
  sample >= marker.first && sample < marker.last
));

const bytesHash = (channels: readonly Float32Array[]): string => {
  const hash = createHash('sha256');
  for (const channel of channels) hash.update(new Uint8Array(channel.buffer));
  return hash.digest('hex');
};

const energy = (channel: Float32Array, first: number, last: number): number => {
  let sum = 0;
  for (let sample = first; sample < last; sample++) sum += channel[sample] ** 2;
  return sum;
};

const makeClip = (fixture: typeof CASES[number]) => ({
  id: `continuous-window-${fixture.name}`,
  at: 0,
  track: 'A1',
  from: fixture.from,
  to: fixture.to,
  speed: fixture.speed,
  params: {
    fadeIn: fixture.fadeIn,
    fadeOut: fixture.fadeOut,
    fadeInCurve: fixture.fadeInCurve,
    fadeOutCurve: fixture.fadeOutCurve,
  },
});

describe('continuous reference fixed-window containment (ORCH audit)', () => {
  it('pins the proposed source support and retains every fixed grid phase', () => {
    expect(PROPOSAL_MARKERS).toEqual([
      {first: 12_000, last: 12_600, frequency: 1_200},
      {first: 12_800, last: 13_400, frequency: 1_440},
      {first: 13_600, last: 14_200, frequency: 1_680},
      {first: 14_400, last: 15_000, frequency: 1_920},
      {first: 15_200, last: 15_800, frequency: 2_160},
      {first: 16_000, last: 16_600, frequency: 2_400},
    ]);

    for (let phase = 0; phase < WINDOW_SAMPLES; phase++) {
      const windows = fixedWindows(PROPOSAL_MARKERS, phase);
      expect(windows).toHaveLength(phase === 0 ? 18 : 12);
      expect(windows.every((window) => (
        window.first >= PROPOSAL_MARKERS[window.marker].first
        && window.last <= PROPOSAL_MARKERS[window.marker].last
      ))).toBe(true);
    }
  });

  for (const fixture of CASES) {
    it(`proves strict nonzero containment with the public clock: ${fixture.name}`, () => {
      const markers = markersAtRate(fixture.sampleRate);
      const source = sourceFor(fixture.sampleRate);
      const expectedHash = bytesHash(source);
      const clip = makeClip(fixture) as Parameters<typeof compileAudioEnvelope>[0];
      const envelope = compileAudioEnvelope(clip, fixture.fps);
      expect(envelope).toBeDefined();

      const transformed = source.map((channel) => channel.slice());
      applyAudioEnvelope(transformed, fixture.sampleRate, envelope!, fixture.from, fixture.speed);

      let maximumClockError = 0;
      for (let sample = 0; sample < source[0].length; sample++) {
        const clock = (sample / fixture.sampleRate - fixture.from) / fixture.speed;
        for (let channel = 0; channel < source.length; channel++) {
          const expected = source[channel][sample] * audioEnvelopeAt(envelope!, clock);
          maximumClockError = Math.max(maximumClockError, Math.abs(expected - transformed[channel][sample]));
        }
      }
      expect(maximumClockError).toBeLessThan(1e-7);

      let containedWindowCount = 0;
      let positiveWindowCount = 0;
      const phaseCounts: number[] = [];
      for (let phase = 0; phase < WINDOW_SAMPLES; phase++) {
        const windows = fixedWindows(markers, phase);
        phaseCounts.push(windows.length);
        expect(windows.length).toBeGreaterThanOrEqual(
          fixture.sampleRate === PROPOSAL_RATE ? markers.length * 2 : markers.length,
        );
        for (const window of windows) {
          containedWindowCount++;
          for (let sample = window.first; sample < window.last; sample++) {
            expect(isInsideMarker(markers, sample)).toBe(true);
          }
          for (const channel of transformed) {
            expect(energy(channel, window.first, window.last)).toBeGreaterThan(0);
          }
          positiveWindowCount++;
        }
      }
      expect(positiveWindowCount).toBe(containedWindowCount);
      expect(containedWindowCount).toBeGreaterThanOrEqual(12 * 2);
      expect(bytesHash(source)).toBe(expectedHash);

      const crossingCandidateCount = markers.reduce((count, marker) => (
        count + Array.from({length: WINDOW_SAMPLES}, (_, phase) => {
          const candidates = [];
          for (let first = phase - WINDOW_SAMPLES; first <= marker.last; first += WINDOW_SAMPLES) {
            if (first < marker.first || first + WINDOW_SAMPLES > marker.last) candidates.push(first);
          }
          return candidates.length;
        }).reduce((sum, value) => sum + value, 0)
      ), 0);
      expect(crossingCandidateCount).toBeGreaterThan(0);
      console.log('CONTAINMENT_SUMMARY', JSON.stringify({
        case: fixture.name,
        sampleRate: fixture.sampleRate,
        fps: fixture.fps,
        channels: source.length,
        samplePhase: `${WINDOW_SAMPLES} integer phases`,
        markerLengths: markers.map((marker) => marker.last - marker.first),
        phaseCountRange: [Math.min(...phaseCounts), Math.max(...phaseCounts)],
        containedWindowCount,
        sourceHash: expectedHash,
        maximumClockError,
      }));
    });
  }
});
