// @vitest-environment jsdom
import React from 'react';
import { createRequire } from 'node:module';
import path from 'node:path';
import { render, renderHook } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { applyAudioEnvelope, audioEnvelopeAt, compileAudioEnvelope } from '@banodoco/timeline-composition/evaluation';
import { AudioTrack } from './AudioTrack';
import type { ResolvedTimelineClip } from '../types';

let previewProps: { volume: number | ((frame: number) => number); useWebAudioApi?: boolean };
const buffer = { delayPlayback: () => ({ unblock: () => undefined }) };

vi.mock('remotion', async () => {
  const React = await import('react');
  return {
    Internals: { SequenceContext: React.createContext(null) },
    Sequence: ({ children }: React.PropsWithChildren) => children,
    Audio: React.forwardRef<HTMLAudioElement, typeof previewProps & { src: string }>((props, ref) => {
      previewProps = props;
      return <audio ref={ref} src={props.src} />;
    }),
    useBufferState: () => buffer,
    useRemotionEnvironment: () => ({ isRendering: false, isClientSideRendering: false }),
  };
});
vi.mock('@remotion/media', () => ({ Audio: () => null }));

// Load the installed hook, bypassing the App's mocked media boundary above.
const require = createRequire(import.meta.url);
const remotionDirectory = path.dirname(require.resolve('remotion'));
const { evaluateVolume } = require(path.join(remotionDirectory, 'volume-prop.js')) as {
  evaluateVolume: (props: { frame: number; volume: typeof previewProps.volume; mediaVolume: number }) => number;
};
const { useVolume } = require(path.join(remotionDirectory, 'use-amplification.js')) as {
  useVolume: (props: {
    mediaRef: React.RefObject<HTMLAudioElement>;
    volume: number;
    logLevel: string;
    source: object;
    shouldUseWebAudioApi: boolean;
  }) => React.MutableRefObject<{ gainNode: GainNode } | null>;
};
const { SharedAudioContext } = require(path.join(remotionDirectory, 'audio/shared-audio-tags.js')) as {
  SharedAudioContext: React.Context<{ audioContext: object; gainNode: object } | null>;
};

const clip: ResolvedTimelineClip = {
  id: 'fade', track: 'audio', clipType: 'media', at: 0, from: 0, to: 3,
  params: { fadeIn: 0.6, fadeOut: 0.6 },
  assetEntry: { file: 'audio.wav', src: 'https://example.com/audio.wav', type: 'audio/wav' },
};

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe('App audio callback scheduling (inert ports, no media playback)', () => {
  it.each([0.8, 2])('retains the frame gain between renders at base volume %s', (baseVolume) => {
    vi.spyOn(HTMLMediaElement.prototype, 'load').mockImplementation(() => undefined);
    const mounted = render(<AudioTrack track={{ id: 'audio', kind: 'audio', label: 'Audio' }} clips={[{ ...clip, volume: baseVolume }]} fps={30} />);
    const { volume, useWebAudioApi } = previewProps;
    expect(typeof volume).toBe('function');
    expect(useWebAudioApi).toBe(baseVolume > 1 ? true : undefined);

    // This is only a gain sink. No AudioContext, source, clock, RAF, or PCM is run.
    class GainSink {
      gain: { value: number };
      constructor(_context: object, options: { gain: number }) {
        this.gain = { value: options.gain };
      }
      connect() {}
      disconnect() {}
    }
    vi.stubGlobal('GainNode', GainSink);
    const mediaRef = { current: document.createElement('audio') };
    const source = { attemptToConnect() {}, get: () => ({ connect() {}, disconnect() {} }) };
    const context = { audioContext: {}, gainNode: {} };
    const wrapper = ({ children }: React.PropsWithChildren) => (
      <SharedAudioContext.Provider value={context}>{children}</SharedAudioContext.Provider>
    );
    const callback = vi.fn(volume as (frame: number) => number);
    const hook = renderHook(({ frame }) => useVolume({
      mediaRef, source, logLevel: 'error', shouldUseWebAudioApi: !!useWebAudioApi,
      volume: evaluateVolume({ frame, volume: callback, mediaVolume: 1 }),
    }), { wrapper, initialProps: { frame: 2 } });
    const gain = () => useWebAudioApi ? hook.result.current.current!.gainNode.gain.value : mediaRef.current.volume;
    expect(gain()).toBeCloseTo(baseVolume * 2 / 18, 12);

    // Model source progress after the frame-2 commit, withholding the next frame
    // render as a delayed RAF would. currentTime does not drive this gain hook.
    mediaRef.current.currentTime = 3 / 30;
    expect(callback.mock.calls.map(([frame]) => frame)).toEqual([2]);
    expect(gain()).toBeCloseTo(baseVolume * 2 / 18, 12);
    expect(gain()).not.toBeCloseTo((volume as (frame: number) => number)(3), 12);

    hook.rerender({ frame: 3 });
    expect(callback.mock.calls.map(([frame]) => frame)).toEqual([2, 3]);
    expect(gain()).toBeCloseTo(baseVolume * 3 / 18, 12);
    hook.unmount();
    mounted.unmount();
  });

  it('bakes the envelope into both source channels independently of frame renders', () => {
    const fps = 30;
    const sampleRate = 48000;
    const envelope = compileAudioEnvelope(clip, fps)!;
    const channels = [new Float32Array(4801).fill(0.125), new Float32Array(4801).fill(0.09375)];
    applyAudioEnvelope(channels, sampleRate, envelope);
    for (const frame of [2, 3]) {
      const sample = frame * sampleRate / fps;
      const gain = audioEnvelopeAt(envelope, sample / sampleRate);
      expect(channels[0][sample]).toBeCloseTo(0.125 * gain, 8);
      expect(channels[1][sample]).toBeCloseTo(0.09375 * gain, 8);
    }
    expect(channels[0][4800]).toBeGreaterThan(channels[0][3200]);
  });

  it('distinguishes continuous sample baking from the App export frame table inside a marker', () => {
    const envelope = compileAudioEnvelope(clip, 30)!;
    const frameGain = 2 * audioEnvelopeAt(envelope, 3 / 30);
    // The unchanged frame-3 marker starts at sample 5200 (frame 3.25).
    const channels = [new Float32Array(5201).fill(0.125)];
    applyAudioEnvelope(channels, 48000, envelope);
    const bakedGain = 2 * channels[0][5200] / 0.125;
    expect(frameGain).toBeCloseTo(1 / 3, 12);
    expect(bakedGain).toBeCloseTo(3.25 / 9, 7);
    expect(20 * Math.log10(bakedGain / frameGain)).toBeGreaterThan(0.5);
  });
});
