// @vitest-environment jsdom
import React from 'react';
import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { applyAudioEnvelope, audioEnvelopeAt, audioEnvelopeWav, compileAudioEnvelope,
  computeMediaTrim, getSanitizedPlaybackRate } from '@banodoco/timeline-composition/evaluation';
import { AudioTrack } from '@/tools/video-editor/compositions/AudioTrack';
import { playerEvaluationClip } from '@/tools/video-editor/compositions/playerEvaluation';

const captures = vi.hoisted(() => ({ audio: [] as Record<string, unknown>[], report: vi.fn() }));
vi.mock('remotion', async () => {
  const React = await import('react');
  return {
    Internals: { SequenceContext: React.createContext(null) },
    Sequence: ({ children }: React.PropsWithChildren) => <>{children}</>,
    Audio: React.forwardRef<HTMLAudioElement, Record<string, unknown>>((props, ref) => {
      captures.audio.push(props);
      return <audio data-testid="audio" ref={ref} src={props.src as string} />;
    }),
    useBufferState: () => ({ delayPlayback: () => ({ unblock: () => {} }) }),
    useRemotionEnvironment: () => ({ isRendering: false, isClientSideRendering: false }),
    staticFile: (file: string) => `/static/${file}`,
  };
});
vi.mock('@remotion/media', () => ({ Audio: () => null }));
vi.mock('@/tools/video-editor/compositions/PreviewMediaFailureContext.tsx', () => ({
  useOptionalPreviewAudioFailureReporter: () => ({ reportFailure: captures.report }),
}));

const clip = {
  id: 'sound', at: 7.5, track: 'A1', clipType: 'media' as const,
  asset: 'source', from: 0.05, to: 0.55, speed: 2, volume: 0.8,
  params: { fadeIn: 0.1, fadeOut: 0.1 },
  assetEntry: { file: 'original.wav', src: 'https://example.test/original.wav', type: 'audio/wav' },
};
const envelope = compileAudioEnvelope(playerEvaluationClip(clip), 30)!;
const prepared = {
  file: 'https://example.test/attempt-envelope.wav', envelope_key: JSON.stringify(envelope),
  source_from: computeMediaTrim(clip, 30).trimBefore / 30,
  playback_rate: getSanitizedPlaybackRate(clip.speed),
};

afterEach(() => {
  cleanup();
  captures.audio.length = 0;
  captures.report.mockClear();
});
describe('continuousPCM policy / both-consumer contract: prepared source admission', () => {
  it('keeps the public full-source PCM/WAV positive exact before consumer admission', () => {
    const rate = 48000;
    const original = Float32Array.from({ length: rate }, (_, i) => i % 2 ? -2 : 3);
    const channel = original.slice();
    applyAudioEnvelope([channel], rate, envelope, prepared.source_from, prepared.playback_rate);
    const wav = new DataView(audioEnvelopeWav([channel], rate));
    expect(wav.getUint16(20, true)).toBe(3);
    expect(wav.getUint32(24, true)).toBe(rate);
    expect(wav.byteLength).toBe(44 + rate * 4);
    const expected = Float32Array.from(original, (value, i) => value * audioEnvelopeAt(
      envelope, (i / rate - 2 / 30) / 2));
    const actual = Float32Array.from({ length: rate }, (_, i) => wav.getFloat32(44 + i * 4, true));
    expect(new Uint8Array(actual.buffer).every((value, i) => value === new Uint8Array(expected.buffer)[i])).toBe(true);
  });

  it('plays a matching prepared positive with one constant half-track gain', () => {
    render(<AudioTrack track={{ id: 'A1', kind: 'audio', volume: 0.5 }}
      clips={[{ ...clip, audio: { render_source: prepared } }]} fps={30} />);
    expect(screen.getByTestId('audio')).toHaveAttribute('src', prepared.file);
    expect(captures.audio.at(-1)).toMatchObject({ volume: 0.4, trimBefore: 2, trimAfter: 17, playbackRate: 2 });
  });

  it.each([
    ['wrong envelope', { envelope_key: JSON.stringify({ keyframes: [{ at: 0, value: 1 }] }) }],
    ['raw fractional origin', { source_from: 0.05 }],
    ['wrong child rate', { playback_rate: 0.5 }],
    ['non-attempt URL', { file: 'blob:forged' }],
  ])('refuses %s instead of ignoring its prepared claim', (_name, change) => {
    render(<AudioTrack track={{ id: 'A1', kind: 'audio' }}
      clips={[{ ...clip, audio: { render_source: { ...prepared, ...change } } }]} fps={30} />);
    expect(screen.queryByTestId('audio')).toBeNull();
    expect(captures.report).toHaveBeenCalledWith({ clipId: clip.id, source: clip.assetEntry.src });
  });
});
