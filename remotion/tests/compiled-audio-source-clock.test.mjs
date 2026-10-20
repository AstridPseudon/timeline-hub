import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {describe, expect, it, vi} from 'vitest';
import {TimelineComposition, compileCanonicalTransitions, DEFAULT_THEME} from '@banodoco/timeline-composition';
import {compileAudioEnvelope} from '@banodoco/timeline-composition/evaluation';
import {compiledAudioSourceClock} from '../compiled-audio-source-clock.mjs';

const host = vi.hoisted(() => ({fps: 30, endpoints: []}));
// Execute the public AudioTrack and prepared-source admission with only the
// media/frame primitives mocked, as in the existing PCM kernel tests.
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

const endpoint = (compiledClip, clock) => {
  host.endpoints.length = 0;
  const clip = {...compiledClip, audio: {render_source: {
    file: 'http://attempt.invalid/envelope/source.wav',
    envelope_key: JSON.stringify(compileAudioEnvelope(compiledClip, host.fps)),
    ...clock,
  }}};
  renderToStaticMarkup(createElement(TimelineComposition, {
    timeline: {theme: 'default', tracks: [{id: 'A1', kind: 'audio'}], clips: [clip]},
    assets: {assets: {sound: {type: 'audio/wav', file: 'http://attempt.invalid/original.wav'}}},
    compiledTransitions: compileCanonicalTransitions([], host.fps, DEFAULT_THEME),
  }));
  expect(host.endpoints).toHaveLength(1);
  return host.endpoints[0];
};

// Literal compiled inputs, not canonical occurrence projections. The Agent's
// canonical eleven-vector contract is pending; no inheritance policy is tested here.
const fixtures = [
  ['trimmed double rate', {from: 0.051, to: 0.9, speed: 2}, 2, 27, 2],
  ['trimmed half rate', {from: 0.49, to: 1.01, speed: 0.5}, 15, 30, 0.5],
  ['already compiled occurrence', {from: 0.475, to: 1.475, speed: 1.5}, 14, 44, 1.5],
];

describe('public media clock adapter for compiled Agent clips', () => {
  it('uses public defaults and rate sanitization, with an explicit resolved fps', () => {
    for (const speed of [undefined, 0, -1, NaN, Infinity, '2']) {
      expect(compiledAudioSourceClock({speed}, 30)).toEqual({source_from: 0, playback_rate: 1});
    }
    for (const fps of [undefined, 0, -1, NaN, Infinity]) {
      expect(() => compiledAudioSourceClock({}, fps)).toThrow(/resolved fps required/);
    }
  });

  describe.each([30, 30000 / 1001])('at fps %s', fps => {
    it.each(fixtures)('agrees with public prepared-source admission: %s', (_, media, start, end, rate) => {
      host.fps = fps;
      const compiledClip = {id: 'sound', track: 'A1', asset: 'sound', at: 12.5,
        hold: 0.4, params: {fadeIn: 0.2}, ...media};
      const before = JSON.stringify(compiledClip);
      const clock = compiledAudioSourceClock(compiledClip, fps);
      expect(clock).toEqual({source_from: start / fps, playback_rate: rate});
      const audio = endpoint(compiledClip, clock);
      expect(audio).toMatchObject({src: 'http://attempt.invalid/envelope/source.wav',
        trimBefore: start, trimAfter: end, playbackRate: rate, volume: 1});
      expect(audio.trimBefore / fps).toBe(clock.source_from);
      expect(audio.playbackRate).toBe(clock.playback_rate);
      for (const wrong of [
        {...clock, source_from: media.from},
        {...clock, source_from: clock.source_from + 1 / fps},
        {...clock, playback_rate: rate + 0.25},
      ]) {
        expect(() => endpoint(compiledClip, wrong)).toThrow(/ENVELOPE_UNRENDERED/);
      }
      expect(JSON.stringify(compiledClip)).toBe(before);
    });
  });
});
