// @vitest-environment node
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it, vi } from 'vitest';
import { TimelineComposition, compileCanonicalTransitions, DEFAULT_THEME, toRuntimeTheme, type TimelineClip as PublicClip } from '@banodoco/timeline-composition';
import {
  audioEnvelopeAt, compileAudioEnvelope, computeMediaTrim, getSanitizedPlaybackRate,
} from '@banodoco/timeline-composition/evaluation';
import reference from './shotCompositionAudio.reference.json';
import type { ResolvedTimelineClip } from '../types/index.ts';
type Json = Record<string, unknown>;
const host = vi.hoisted(() => ({ fps: 30, endpoints: [] as Json[] }));
vi.mock('remotion', async importOriginal => ({
  ...await importOriginal<typeof import('remotion')>(),
  AbsoluteFill: ({ children }: React.PropsWithChildren) => children,
  Sequence: ({ children }: React.PropsWithChildren) => children,
  useCurrentFrame: () => 0,
  useVideoConfig: () => ({ fps: host.fps, width: 32, height: 32 }),
  getRemotionEnvironment: () => ({ isPlayer: false, isRendering: true }),
  useBufferState: () => ({}),
  Audio: (props: Json) => { host.endpoints.push(props); return null; },
}));

function renderPublic(clip: ResolvedTimelineClip, prepared?: { source_from: number; playback_rate: number }) {
  host.endpoints.length = 0;
  const media = { ...clip, asset: 'sound', ...(prepared ? { audio: { render_source: {
    file: 'http://attempt.invalid/envelope.wav', envelope_key: JSON.stringify(compileAudioEnvelope(clip, host.fps)), ...prepared,
  } } } : {}) };
  renderToStaticMarkup(React.createElement(TimelineComposition, {
    timeline: { theme: 'default', tracks: [{ id: 'audio', kind: 'audio', label: 'Audio' }], clips: [media as unknown as PublicClip] },
    assets: { assets: { sound: { type: 'audio/wav', file: 'http://attempt.invalid/native.wav' } } },
    compiledTransitions: compileCanonicalTransitions([], host.fps, toRuntimeTheme(DEFAULT_THEME)),
  }));
  return host.endpoints[0];
}

describe.each([30, 30000 / 1001])('public11 clock on exact compiler output at fps %s', fps => {
  it.each(reference.results.map((row, index) => ({ ...row, index })))('$corpus: $id', row => {
    host.fps = fps;
    const clip = reference.results[row.index].clip as ResolvedTimelineClip;
    const before = structuredClone(clip);
    const trim = computeMediaTrim(clip, fps);
    const rate = getSanitizedPlaybackRate(clip.speed);
    const clock = { source_from: trim.trimBefore / fps, playback_rate: rate };
    const endpoint = renderPublic(clip, compileAudioEnvelope(clip, fps) ? clock : undefined);
    expect(endpoint.trimBefore).toBe(trim.trimBefore);
    expect(endpoint.trimAfter).toBe(trim.trimAfter);
    expect(endpoint.playbackRate).toBe(rate);
    expect(endpoint.volume).toBe(clip.volume ?? 1);
    expect(clip).toStrictEqual(before);
    if (clip.from === 0.125) {
      expect(trim.trimBefore).toBe(4);
      expect(clock.source_from).not.toBe(clip.from);
    }
    if (row.corpus === 'viewing' && row.id === 'params fades') {
      expect(trim.trimBefore).toBe(fps === 30 ? 2 : 1);
      expect(clock.source_from).not.toBe(clip.from);
      const envelope = compileAudioEnvelope(clip, fps)!;
      for (const [frame, gain] of [[0, 0], [1, 1 / 3], [3, 1], [7, 1], [12, 1], [14, 1 / 3], [15, 0]]) {
        expect(audioEnvelopeAt(envelope, frame / fps)).toBeCloseTo(gain, 12);
      }
    }
  });

  it('honours an explicit curve on a separate compiled-input control', () => {
    const clip = { id: 'curve-control', at: 0, track: 'audio', hold: 1, params: { fadeIn: 1, fadeInCurve: 'exponential-slow' } };
    const envelope = compileAudioEnvelope(clip, fps)!;
    const linear = compileAudioEnvelope({ ...clip, params: { fadeIn: 1 } }, fps)!;
    expect(audioEnvelopeAt(envelope, 0.5)).not.toBe(audioEnvelopeAt(linear, 0.5));
  });
});

it('requires the normal prepared-source producer for authored fades (still RED; no producer is invoked here)', () => {
  host.fps = 30;
  const fades = reference.results.filter(row => compileAudioEnvelope(row.clip as ResolvedTimelineClip, host.fps));
  expect(fades).toHaveLength(3);
  for (const row of fades) {
    // Original public boundary requirement. Synthetic prepared sources above only
    // exercise admission/clock plumbing; they are never producer evidence.
    expect.soft(() => renderPublic(row.clip as ResolvedTimelineClip)).not.toThrow();
  }
});
