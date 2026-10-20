// @vitest-environment jsdom
import React from 'react';
import { Blob } from 'node:buffer';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { applyAudioEnvelope, audioEnvelopeAt, audioEnvelopeWav, compileAudioEnvelope, computeMediaTrim } from '@banodoco/timeline-composition/evaluation';
import { AUDIO_HOLD_LIMIT_MS, AUDIO_RETRY_DELAYS_MS, AudioTrack } from '@/tools/video-editor/compositions/AudioTrack';
import { playerEvaluationClip } from '@/tools/video-editor/compositions/playerEvaluation';

const state = vi.hoisted(() => ({
  props: [] as Record<string, unknown>[], rendering: false, premounting: false,
  holds: 0, retryGeneration: 0, reportFailure: vi.fn(), clearFailure: vi.fn(),
}));
vi.mock('remotion', async () => {
  const React = await import('react');
  const SequenceContext = React.createContext<{ premounting: boolean } | null>(null);
  const buffer = { delayPlayback: () => {
    state.holds++;
    let released = false;
    return { unblock: () => { if (!released) { released = true; state.holds--; } } };
  } };
  return {
    Internals: { SequenceContext },
    Sequence: ({ children }: React.PropsWithChildren) => <SequenceContext.Provider value={{ premounting: state.premounting }}>{children}</SequenceContext.Provider>,
    Audio: React.forwardRef<HTMLAudioElement, Record<string, unknown>>((props, ref) => {
      state.props.push(props);
      return <audio data-testid="audio" src={props.src as string} ref={ref} />;
    }),
    useBufferState: () => buffer,
    useRemotionEnvironment: () => ({ isRendering: state.rendering, isClientSideRendering: false }),
  };
});
vi.mock('@remotion/media', () => ({ Audio: (props: Record<string, unknown>) => {
  state.props.push(props);
  return <audio data-testid="audio" src={props.src as string} />;
} }));
vi.mock('@/tools/video-editor/compositions/PreviewMediaFailureContext.tsx', () => ({
  useOptionalPreviewAudioFailureReporter: () => ({
    retryGeneration: state.retryGeneration, reportFailure: state.reportFailure, clearFailure: state.clearFailure,
  }),
}));

const clip = {
  id: 'sound', at: 7.5, track: 'A1', clipType: 'media' as const,
  asset: 'source', from: 0.05, to: 0.55, speed: 2, volume: 0.8,
  params: { fadeIn: 0.1, fadeOut: 0.1 },
  assetEntry: { file: 'original.wav', src: 'https://example.test/original.wav', type: 'audio/wav' },
};
const track = { id: 'A1', kind: 'audio' as const, volume: 0.5 };
const plain = { ...clip, params: undefined };
const envelope = compileAudioEnvelope(playerEvaluationClip(clip), 30)!;
const prepared = {
  file: 'https://example.test/attempt.wav', envelope_key: JSON.stringify(envelope),
  source_from: 2 / 30, playback_rate: 2,
};
let blobs: Blob[];
let contexts: { close: ReturnType<typeof vi.fn> }[];
let channels: Float32Array[];
let sampleRate: number;
let fetchMock: ReturnType<typeof vi.fn>;
let decode: ReturnType<typeof vi.fn>;
let revoke: ReturnType<typeof vi.fn>;

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>(done => { resolve = done; });
  return { promise, resolve };
}
function decoded() {
  return { numberOfChannels: channels.length, sampleRate, getChannelData: (i: number) => channels[i].slice() };
}
const flush = () => act(async () => { await Promise.resolve(); });
const props = () => state.props.at(-1)!;
const audio = () => screen.getByTestId('audio') as HTMLAudioElement;
function playable() {
  Object.defineProperty(audio(), 'readyState', { configurable: true, value: HTMLMediaElement.HAVE_ENOUGH_DATA });
  fireEvent.canPlay(audio());
}

beforeEach(() => {
  state.props.length = 0;
  state.rendering = false;
  state.premounting = false;
  state.holds = 0;
  state.retryGeneration = 0;
  state.reportFailure.mockClear();
  state.clearFailure.mockClear();
  blobs = [];
  contexts = [];
  sampleRate = 48000;
  channels = [Float32Array.from({ length: sampleRate }, (_, i) => i % 2 ? -3 : 2)];
  fetchMock = vi.fn().mockResolvedValue({ ok: true, arrayBuffer: async () => new ArrayBuffer(8) });
  decode = vi.fn().mockImplementation(async () => decoded());
  revoke = vi.fn();
  vi.stubGlobal('fetch', fetchMock);
  vi.stubGlobal('Blob', Blob);
  vi.stubGlobal('AudioContext', class {
    close = vi.fn().mockResolvedValue(undefined);
    decodeAudioData = decode;
    constructor() { contexts.push(this); }
  });
  vi.stubGlobal('URL', class extends URL {
    static createObjectURL(blob: Blob) { blobs.push(blob); return `blob:pcm-${blobs.length}`; }
    static revokeObjectURL = revoke;
  });
  vi.spyOn(HTMLMediaElement.prototype, 'load').mockImplementation(() => {});
});
afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('continuous PCM inside the App audio attempt', () => {
  it.each([44100, 48000])('bakes the full %s Hz source once, with native trim/rate and a constant scalar', async rate => {
    sampleRate = rate;
    channels = [Float32Array.from({ length: rate }, (_, i) => i % 2 ? -3 : 2), new Float32Array(rate).fill(0.75)];
    const authored = JSON.stringify(clip);
    const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    expect(screen.queryByTestId('audio')).toBeNull();
    expect(state.holds).toBe(1);
    await flush();
    expect(props()).toMatchObject({ src: 'blob:pcm-1', volume: 0.4, trimBefore: 2, trimAfter: 17, playbackRate: 2, pauseWhenBuffering: false, preload: 'auto' });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(decode).toHaveBeenCalledTimes(1);
    expect(contexts[0].close).toHaveBeenCalledTimes(1);
    const expected = channels.map(channel => channel.slice());
    applyAudioEnvelope(expected, rate, envelope, 2 / 30, 2);
    expect(new Uint8Array(await blobs[0].arrayBuffer())).toEqual(new Uint8Array(audioEnvelopeWav(expected, rate)));
    const wav = new DataView(await blobs[0].arrayBuffer());
    expect(wav.getUint32(24, true)).toBe(rate);
    expect(wav.getUint32(40, true)).toBe(rate * 2 * 4);
    // A between-frame sample proves that the retired callback table cannot pass.
    const sample = Math.round((2 / 30 + 2 * 0.017) * rate);
    const continuous = Math.fround(channels[0][sample] * audioEnvelopeAt(envelope, (sample / rate - 2 / 30) / 2));
    const stepHold = Math.fround(channels[0][sample] * audioEnvelopeAt(envelope, Math.floor((sample / rate - 2 / 30) / 2 * 30) / 30));
    expect(wav.getFloat32(44 + sample * 8, true)).toBe(continuous);
    expect(continuous).not.toBe(stepHold);
    act(playable);
    expect(state.holds).toBe(0);
    view.rerender(<AudioTrack track={track} clips={[{ ...clip }]} fps={30} />);
    await flush();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(JSON.stringify(clip)).toBe(authored);
    const signal = fetchMock.mock.calls[0][1].signal as AbortSignal;
    view.unmount();
    expect(signal.aborted).toBe(true);
    expect(revoke).toHaveBeenCalledExactlyOnceWith('blob:pcm-1');
  });

  it.each([
    { volume: 0.5, muted: false, gain: 0.4, amplify: undefined },
    { volume: 0.5, muted: true, gain: 0, amplify: undefined },
    { volume: 2, muted: false, gain: 1.6, amplify: true },
  ])('keeps prepared PCM and downstream scalar for $gain gain', ({ volume, muted, gain, amplify }) => {
    render(<AudioTrack track={{ ...track, volume, muted }} clips={[{ ...clip, audio: { render_source: prepared } }]} fps={30} />);
    expect(props()).toMatchObject({ src: prepared.file, volume: gain, trimBefore: 2, trimAfter: 17, playbackRate: 2 });
    expect(props().useWebAudioApi).toBe(amplify);
    expect(fetchMock).not.toHaveBeenCalled();
    expect(decode).not.toHaveBeenCalled();
  });

  it('retains the Web Audio amplification route for a baked envelope above unity', async () => {
    render(<AudioTrack track={track} clips={[{ ...clip, audio: { envelope: { keyframes: [{ at: 0, value: 3 }] } } }]} fps={30} />);
    await flush();
    expect(props()).toMatchObject({ volume: 0.4, useWebAudioApi: true });
    const wav = new DataView(await blobs[0].arrayBuffer());
    expect(wav.getFloat32(44, true)).toBe(6);
  });

  it('keeps the original child source clock when an occurrence shortens the native window', async () => {
    const bounded = { ...clip, app: { canonicalTiming: { occurrenceStartMs: 7500, occurrenceDurationMs: 125 } } };
    render(<AudioTrack track={track} clips={[bounded]} fps={30} />);
    await flush();
    expect(props()).toMatchObject({ trimBefore: 2, trimAfter: computeMediaTrim({ from: 0.05, to: 0.3 }, 30).trimAfter, playbackRate: 2 });
    const expected = channels.map(channel => channel.slice());
    applyAudioEnvelope(expected, sampleRate, envelope, 2 / 30, 2);
    expect(new Uint8Array(await blobs[0].arrayBuffer())).toEqual(new Uint8Array(audioEnvelopeWav(expected, sampleRate)));
  });

  it('uses the same admitted PCM in an export, with constant gain and no browser decoding', () => {
    state.rendering = true;
    render(<AudioTrack track={track} clips={[{ ...clip, audio: { render_source: prepared } }]} fps={30} />);
    expect(props()).toMatchObject({ src: prepared.file, volume: 0.4, playbackRate: 2, trimBefore: 2, trimAfter: 17 });
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('does not mount unprepared envelope audio during export', () => {
    state.rendering = true;
    vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => render(<AudioTrack track={track} clips={[clip]} fps={30} />)).toThrow('matching attempt-local envelope PCM');
    expect(state.props).toHaveLength(0);
  });

  it('aborts a superseded fetch and drops its late decoded completion', async () => {
    const pending = deferred<ReturnType<typeof decoded>>();
    decode.mockImplementationOnce(() => pending.promise);
    const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    const oldSignal = fetchMock.mock.calls[0][1].signal as AbortSignal;
    const next = { ...clip, assetEntry: { ...clip.assetEntry, src: 'https://example.test/next.wav' } };
    view.rerender(<AudioTrack track={track} clips={[next]} fps={30} />);
    await flush();
    expect(oldSignal.aborted).toBe(true);
    expect(blobs).toHaveLength(1);
    await act(async () => pending.resolve(decoded()));
    expect(blobs).toHaveLength(1);
    expect(props().src).toBe('blob:pcm-1');
    expect(contexts.every(context => context.close.mock.calls.length === 1)).toBe(true);
  });

  it('revokes prepared PCM and bakes fresh bytes after an envelope edit', async () => {
    const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    view.rerender(<AudioTrack track={track} clips={[{ ...clip, params: { fadeIn: 0.2 } }]} fps={30} />);
    await flush();
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(revoke).toHaveBeenCalledWith('blob:pcm-1');
    expect(props().src).toBe('blob:pcm-2');
  });

  it('retries fetch/decode failures in the existing budget, then supports the chrome Retry', async () => {
    vi.useFakeTimers();
    fetchMock.mockRejectedValue(new Error('offline'));
    const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    for (const delay of AUDIO_RETRY_DELAYS_MS) {
      expect(state.holds).toBe(1);
      await act(async () => vi.advanceTimersByTime(delay));
    }
    expect(fetchMock).toHaveBeenCalledTimes(4);
    expect(state.holds).toBe(0);
    expect(state.reportFailure).toHaveBeenCalledWith({ clipId: clip.id, source: clip.assetEntry.src });
    fetchMock.mockResolvedValue({ ok: true, arrayBuffer: async () => new ArrayBuffer(8) });
    state.retryGeneration++;
    view.rerender(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    act(playable);
    expect(state.clearFailure).toHaveBeenCalledWith(clip.id);
    expect(state.holds).toBe(0);
  });

  it('closes a failed decoder and aborts its attempt before a successful retry', async () => {
    vi.useFakeTimers();
    decode.mockRejectedValueOnce(new Error('bad decode'));
    render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    expect(contexts[0].close).toHaveBeenCalledTimes(1);
    expect(fetchMock.mock.calls[0][1].signal.aborted).toBe(true);
    await act(async () => vi.advanceTimersByTime(AUDIO_RETRY_DELAYS_MS[0]));
    expect(props().src).toBe('blob:pcm-1');
  });

  it('holds through preparation again after a previously playable native element fails', async () => {
    vi.useFakeTimers();
    render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    act(playable);
    expect(state.holds).toBe(0);
    act(() => fireEvent.error(audio()));
    expect(state.holds).toBe(1);
    const pending = deferred<ReturnType<typeof decoded>>();
    decode.mockImplementationOnce(() => pending.promise);
    await act(async () => vi.advanceTimersByTime(AUDIO_RETRY_DELAYS_MS[0]));
    expect(screen.queryByTestId('audio')).toBeNull();
    expect(state.holds).toBe(1);
    await act(async () => pending.resolve(decoded()));
    act(playable);
    expect(state.holds).toBe(0);
    expect(revoke).toHaveBeenCalledWith('blob:pcm-1');
  });

  it('bounds a stalled preparation hold without restarting its download, then joins when ready', async () => {
    vi.useFakeTimers();
    const response = deferred<{ ok: boolean; arrayBuffer: () => Promise<ArrayBuffer> }>();
    fetchMock.mockReturnValue(response.promise);
    render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    expect(state.holds).toBe(1);
    act(() => vi.advanceTimersByTime(AUDIO_HOLD_LIMIT_MS));
    expect(state.holds).toBe(0);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    await act(async () => response.resolve({ ok: true, arrayBuffer: async () => new ArrayBuffer(8) }));
    expect(state.holds).toBe(0);
    act(playable);
    expect(state.holds).toBe(0);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('premounts decoding without holding until the clip becomes active', async () => {
    state.premounting = true;
    const view = render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    const element = audio();
    expect(state.holds).toBe(0);
    state.premounting = false;
    view.rerender(<AudioTrack track={track} clips={[clip]} fps={30} />);
    expect(state.holds).toBe(1);
    expect(audio()).toBe(element);
    expect(fetchMock).toHaveBeenCalledTimes(1);
    act(playable);
    expect(state.holds).toBe(0);
  });

  it('renews the same hold as source chunks arrive before the native WAV element exists', async () => {
    vi.useFakeTimers();
    let chunk = deferred<{ done: boolean; value?: Uint8Array }>();
    const read = vi.fn(() => chunk.promise);
    fetchMock.mockResolvedValue({ ok: true, body: { getReader: () => ({ read }) } });
    render(<AudioTrack track={track} clips={[clip]} fps={30} />);
    await flush();
    for (let i = 0; i < 4; i++) {
      const pending = chunk;
      chunk = deferred();
      await act(async () => {
        vi.advanceTimersByTime(AUDIO_HOLD_LIMIT_MS / 2);
        pending.resolve({ done: false, value: new Uint8Array([i]) });
      });
      expect(state.holds).toBe(1);
    }
    await act(async () => chunk.resolve({ done: true }));
    expect(decode.mock.calls[0][0]).toEqual(Uint8Array.from([0, 1, 2, 3]).buffer);
    act(playable);
    expect(state.holds).toBe(0);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('keeps ordinary media readiness, progress, retry and teardown in the existing flow', () => {
    vi.useFakeTimers();
    const view = render(<AudioTrack track={track} clips={[plain]} fps={30} />);
    expect(props()).toMatchObject({ src: clip.assetEntry.src, volume: 0.4, playbackRate: 2 });
    expect(state.holds).toBe(1);
    for (let i = 0; i < 3; i++) {
      act(() => { vi.advanceTimersByTime(AUDIO_HOLD_LIMIT_MS / 2); fireEvent.progress(audio()); });
    }
    expect(state.holds).toBe(1);
    act(playable);
    expect(state.holds).toBe(0);
    const previous = audio();
    act(() => fireEvent.error(previous));
    expect(previous).not.toHaveAttribute('src');
    expect(state.holds).toBe(1);
    act(() => vi.advanceTimersByTime(AUDIO_RETRY_DELAYS_MS[0]));
    expect(audio()).not.toBe(previous);
    act(playable);
    expect(state.holds).toBe(0);
    view.unmount();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});


