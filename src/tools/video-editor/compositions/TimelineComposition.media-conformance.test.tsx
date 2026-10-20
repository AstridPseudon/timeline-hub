// @vitest-environment jsdom
import type { CSSProperties, ReactElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it, vi } from 'vitest';
import { Internals, Sequence, useCurrentFrame } from 'remotion';
import {
  TimelineComposition, compileCanonicalTransitions, toRuntimeTheme,
} from '@banodoco/timeline-composition';
import { compileAudioEnvelope } from '@banodoco/timeline-composition/evaluation';
import { TimelineRenderer } from './TimelineRenderer.tsx';
import { compilePlayerTransitions, playerEvaluationClip } from './playerEvaluation.ts';
import { resolveTimelineRenderTheme } from './installed-themes.ts';
import type { ResolvedTimelineClip, ResolvedTimelineConfig, TrackDefinition } from '../types/index.ts';
import type { AstridElementHost } from '../runtime/astrid-element-host.ts';

type EndpointProps = {
  src: string; trimBefore?: number; trimAfter?: number; playbackRate?: number;
  volume?: number | ((frame: number) => number); muted?: boolean; style?: CSSProperties;
};

// Only external media primitives are replaced. Sequence, Freeze, frame hooks,
// both compositions and all three media adapters execute their real code.
vi.mock('remotion', async importOriginal => {
  const actual = await importOriginal<typeof import('remotion')>();
  return {
    ...actual,
    useRemotionEnvironment: () => ({ isRendering: true, isClientSideRendering: false }),
    Audio: (props: EndpointProps) => <Endpoint kind="audio" {...props} />,
  };
});
vi.mock('@remotion/media', () => ({
  Video: (props: EndpointProps) => <Endpoint kind="video" {...props} />,
  Audio: (props: EndpointProps) => <Endpoint kind="audio" {...props} />,
}));
vi.mock('@astrid/packs/rendering/shared/managed-media', () => ({
  ManagedVideo: (props: EndpointProps) => <Endpoint kind="video" {...props} />,
}));

const Endpoint = ({ kind, ...props }: EndpointProps & { kind: string }) => {
  const frame = useCurrentFrame();
  // Remotion 4.0.509 audio/use-audio-frame.js and @remotion/media's
  // frameForVolumeProp both pass elapsed timeline frames for non-looping media.
  // Trim's internal negative Sequence is cancelled by useMediaStartsAt; speed
  // does not scale this argument. Use the installed hook/evaluator, not an oracle.
  const volumeFrame = Internals.useFrameForVolumeProp('repeat');
  const gain = Internals.evaluateVolume({ frame: volumeFrame, volume: props.volume, mediaVolume: 1 });
  return <i data-kind={kind} data-src={props.src} data-frame={frame}
    data-volume-frame={volumeFrame} data-gain={gain} data-callback={typeof props.volume === 'function'}
    data-trim-before={props.trimBefore} data-trim-after={props.trimAfter}
    data-rate={props.playbackRate} data-muted={props.muted} style={props.style} />;
};

const host: AstridElementHost = {
  descriptors: [], sequenceRegistry: {}, resolveComponent: () => undefined,
  resolveSequenceClipEntry: () => undefined, describeClipCapability: () => undefined,
};
const visual: TrackDefinition = { id: 'V1', kind: 'visual', label: 'Video', volume: 0.8 };
const audio: TrackDefinition = { id: 'A1', kind: 'audio', label: 'Audio', volume: 0.8 };

const renderFrame = (content: ReactElement, frame: number, fps: number) => {
  const video = {
    id: 'media-conformance', width: 1920, height: 1080, fps, durationInFrames: 300,
    defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
    nonce: [], schema: null, calculateMetadata: null, stack: null,
  };
  const markup = renderToStaticMarkup(
    <Internals.CompositionManager.Provider value={{ compositions: [video], currentCompositionMetadata: null,
      folders: [], canvasContent: { type: 'composition', compositionId: video.id } }}>
      <Internals.TimelineContext.Provider value={{ frame: { [video.id]: frame }, playing: false,
        imperativePlaying: { current: false }, audioAndVideoTags: { current: [] } }}>
        <Internals.CanUseRemotionHooksProvider>{content}</Internals.CanUseRemotionHooksProvider>
      </Internals.TimelineContext.Provider>
    </Internals.CompositionManager.Provider>,
  );
  const container = document.createElement('div');
  container.innerHTML = markup;
  return container;
};

const opacityOf = (element: Element): number => {
  let opacity = 1;
  for (let node: HTMLElement | null = element as HTMLElement; node; node = node.parentElement) {
    if (node.style.opacity) opacity *= Number(node.style.opacity);
  }
  return opacity;
};

const media = (id: string, track: string, atFrame: number, fps: number, volume = 0.5): ResolvedTimelineClip => ({
  id, track, clipType: 'media', asset: id, at: atFrame / fps,
  from: 90 / fps, to: 330 / fps, hold: 60 / fps, speed: 2, volume,
  assetEntry: { type: track === 'A1' ? 'audio/wav' : 'video/mp4', src: `https://example.test/${id}` },
});

const entrypoints = (config: ResolvedTimelineConfig) => {
  const tracks = config.tracks.map(track => ({ track,
    clips: config.clips.filter(clip => clip.track === track.id).map(playerEvaluationClip) }));
  const compiled = compileCanonicalTransitions(tracks.filter(({ track }) => track.kind === 'visual'),
    config.output.fps, toRuntimeTheme(resolveTimelineRenderTheme(config)));
  expect(compilePlayerTransitions(config)).toEqual(compiled);
  const assets = { assets: Object.fromEntries(config.clips.map(clip => [clip.asset!, {
    ...clip.assetEntry!, file: clip.assetEntry!.src,
  }])) };
  const timeline = { ...config, theme: 'default', clips: tracks.flatMap(track => track.clips) };
  return [
    ['public', <TimelineComposition timeline={timeline} assets={assets} compiledTransitions={compiled} />],
    ['App', <TimelineRenderer config={config} astridElementHost={host} compiledTransitions={compiled} />],
  ] as const;
};

// All frame values are fixture expectations, independent of the planner output.
const boundaries = [
  { name: 'adjacent', own: 30, transition: 12, start: 18, mid: 24, end: 60 },
  { name: 'first', own: 60, transition: 12, start: 60, mid: 66, end: 90 },
  { name: 'gap', own: 60, transition: 12, start: 48, mid: 54, end: 90 },
  { name: 'overlap', own: 15, transition: 12, start: 3, mid: 9, end: 45 },
  { name: 'oversized', own: 30, transition: 60, start: 0, mid: 30, end: 90 },
];

describe('public compiled media adapter conformance (no decoded AV claim)', () => {
  it.each([24, 30, 24000 / 1001])('keeps real volume callback arguments in timeline time at fps %s', fps => {
    // Exercise Remotion's actual internal trim Sequence as well as the untrimmed
    // endpoint context. Neither source trim nor rate belongs in volume(frame).
    const Probe = () => {
      const argument = Internals.useFrameForVolumeProp('repeat');
      return <b data-argument={argument} data-local={useCurrentFrame()} />;
    };
    for (const elapsed of [0, 6, 29]) {
      const document = renderFrame(<Sequence from={30}>
        <Sequence from={-45}><Probe /></Sequence>
      </Sequence>, 30 + elapsed, fps);
      expect(document.querySelector('b')).toHaveAttribute('data-argument', String(elapsed));
      expect(document.querySelector('b')).toHaveAttribute('data-local', String(45 + elapsed));
    }
  });

  it.each([24, 30, 24000 / 1001])('preserves native video clocks/gain/trim/hold at fps %s', fps => {
    for (const boundary of boundaries) {
      for (const [gain, muted] of [[0.5, false], [2, false], [0.5, true], [2, true]] as const) {
        const incoming = { ...media('incoming', 'V1', boundary.own, fps, gain),
          transition: { type: 'cross-fade', duration: boundary.transition / fps } };
        const config: ResolvedTimelineConfig = {
          output: { fps, resolution: '1920x1080', file: 'conformance.mp4' }, registry: {}, tracks: [{ ...visual, muted }],
          clips: [...(boundary.name === 'first' ? [] : [media('outgoing', 'V1', 0, fps)]), incoming],
        };
        for (const [entrypoint, content] of entrypoints(config)) {
          for (const [frame, local, opacity] of [
            [boundary.start, 0, 0], [boundary.mid, boundary.mid - boundary.start, 0.5],
            [boundary.own, boundary.own - boundary.start, boundary.name === 'first' ? 0 : boundary.name === 'oversized' ? 0.5 : 1],
            [boundary.end - 1, boundary.end - boundary.start - 1, 1],
          ]) {
            const document = renderFrame(content, frame, fps);
            const endpoint = document.querySelector('[data-src="https://example.test/incoming"]');
            expect(endpoint, `${entrypoint}/${boundary.name}/${frame}`).not.toBeNull();
            expect(endpoint).toHaveAttribute('data-frame', String(local));
            expect(endpoint).toHaveAttribute('data-trim-before', '90');
            expect(endpoint).toHaveAttribute('data-trim-after', '330');
            expect(endpoint).toHaveAttribute('data-rate', '2');
            expect(endpoint).toHaveAttribute('data-gain', String(muted ? 0 : gain * 0.8));
            expect(endpoint).toHaveAttribute('data-muted', String(muted));
            expect(opacityOf(endpoint!)).toBeCloseTo(opacity, 12);
          }
          expect(renderFrame(content, boundary.end, fps)
            .querySelector('[data-src="https://example.test/incoming"]')).toBeNull();
        }
      }
    }
  });

  it.each([24, 30, 24000 / 1001])('preserves audio fades, authored envelopes and prepared-source admission at fps %s', fps => {
    for (const explicitEnvelope of [false, true]) {
      for (const gain of [0.5, 2]) {
        for (const muted of [false, true]) {
          const authored = { ...media('sound', 'A1', 30, fps, gain), params: { fadeIn: 12 / fps, fadeOut: 12 / fps },
            ...(explicitEnvelope ? { audio: { envelope: { keyframes: [
              { at: 0, value: 0 }, { at: 12 / fps, value: 2 }, { at: 30 / fps, value: 0 },
            ] } } } : {}),
          };
          const envelope = compileAudioEnvelope(playerEvaluationClip(authored), fps)!;
          const clip = { ...authored, audio: { ...authored.audio, render_source: {
            file: 'https://example.test/prepared-envelope.wav', envelope_key: JSON.stringify(envelope),
            source_from: 90 / fps, playback_rate: 2,
          } } };
          const config: ResolvedTimelineConfig = {
            output: { fps, resolution: '1920x1080', file: 'audio.mp4' }, registry: {},
            tracks: [visual, { ...audio, muted }], clips: [media('picture', 'V1', 30, fps), clip],
          };
          for (const [entrypoint, content] of entrypoints(config)) {
            for (const [frame, local, multiplier] of explicitEnvelope
              ? [[30, 0, 0], [36, 6, 1], [42, 12, 2], [54, 24, 2 / 3], [59, 29, 1 / 9]]
              : [[30, 0, 0], [36, 6, 0.5], [42, 12, 1], [54, 24, 0.5], [59, 29, 1 / 12]]) {
              const endpoint = renderFrame(content, frame, fps).querySelector('[data-kind="audio"]');
              expect(endpoint, `${entrypoint}/${frame}`).not.toBeNull();
              expect(endpoint).toHaveAttribute('data-frame', String(local));
              expect(endpoint).toHaveAttribute('data-trim-before', '90');
              expect(endpoint).toHaveAttribute('data-trim-after', '330');
              expect(endpoint).toHaveAttribute('data-rate', '2');
              const base = muted ? 0 : gain * 0.8;
              // Public source already carries its envelope; App invokes its actual
              // per-frame callback. A source URL assertion is no PCM parity proof.
              expect(endpoint).toHaveAttribute('data-src', entrypoint === 'public'
                ? 'https://example.test/prepared-envelope.wav' : authored.assetEntry!.src);
              expect(endpoint).toHaveAttribute('data-callback', String(entrypoint === 'App'));
              expect(Number(endpoint!.getAttribute('data-gain'))).toBeCloseTo(entrypoint === 'public' ? base : base * multiplier, 12);
              expect(endpoint).toHaveAttribute('data-volume-frame', String(local));
            }
            expect(renderFrame(content, 60, fps).querySelector('[data-kind="audio"]')).toBeNull();
          }
        }
      }
    }
  });

  for (const entrypoint of ['public', 'App']) {
    it.each([24, 30, 24000 / 1001])(`${entrypoint} keeps video fades separate from native audio gain and mute at fps %s`, fps => {
      for (const gain of [0.5, 2]) {
        for (const muted of [false, true]) {
          const clip = { ...media('fading-video', 'V1', 30, fps, gain),
            effects: { fade_in: 12 / fps, fade_out: 12 / fps } };
          const config: ResolvedTimelineConfig = {
            output: { fps, resolution: '1920x1080', file: 'fade.mp4' }, registry: {},
            tracks: [{ ...visual, muted }], clips: [clip],
          };
          for (const [name, content] of entrypoints(config)) {
            if (name !== entrypoint) continue;
            for (const [frame, local, opacity] of [[30, 0, 0], [36, 6, 0.5], [42, 12, 1], [54, 24, 0.5], [59, 29, 1 / 12]]) {
              const endpoint = renderFrame(content, frame, fps).querySelector('[data-kind="video"]')!;
              expect(endpoint).toHaveAttribute('data-frame', String(local));
              expect(endpoint).toHaveAttribute('data-gain', String(muted ? 0 : gain * 0.8));
              expect(endpoint).toHaveAttribute('data-muted', String(muted));
              expect(opacityOf(endpoint)).toBeCloseTo(opacity, 12);
            }
            expect(renderFrame(content, 60, fps).querySelector('[data-kind="video"]')).toBeNull();
          }
        }
      }
    });
  }

  it.each([24, 30, 24000 / 1001])('passes unprocessed native audio through both adapters at fps %s', fps => {
    for (const gain of [0.5, 2]) {
      const config: ResolvedTimelineConfig = {
        output: { fps, resolution: '1920x1080', file: 'native-audio.mp4' }, registry: {},
        tracks: [visual, audio], clips: [media('picture', 'V1', 30, fps), media('native-audio', 'A1', 30, fps, gain)],
      };
      for (const [, content] of entrypoints(config)) {
        for (const [frame, local] of [[30, 0], [36, 6], [59, 29]]) {
          const endpoint = renderFrame(content, frame, fps).querySelector('[data-kind="audio"]');
          expect(endpoint).toHaveAttribute('data-src', 'https://example.test/native-audio');
          expect(endpoint).toHaveAttribute('data-frame', String(local));
          expect(endpoint).toHaveAttribute('data-gain', String(gain * 0.8));
          expect(endpoint).toHaveAttribute('data-callback', 'false');
          expect(endpoint).toHaveAttribute('data-trim-before', '90');
          expect(endpoint).toHaveAttribute('data-trim-after', '330');
          expect(endpoint).toHaveAttribute('data-rate', '2');
        }
        expect(renderFrame(content, 60, fps).querySelector('[data-kind="audio"]')).toBeNull();
      }
    }
  });

  it('retains a custom host subtree when another track has a canonical vector', () => {
    const custom: TrackDefinition = { ...visual, id: 'custom' };
    const HostClock = () => <b data-host-frame={useCurrentFrame()} />;
    const customHost: AstridElementHost = { ...host,
      resolveComponent: id => id === 'custom-clock' ? HostClock : undefined };
    const config: ResolvedTimelineConfig = {
      output: { fps: 30, resolution: '1920x1080', file: 'host.mp4' }, registry: {}, tracks: [visual, custom],
      clips: [media('native', 'V1', 0, 30),
        { ...media('host-a', custom.id, 0, 30), clipType: 'custom-clock' },
        { ...media('host-b', custom.id, 30, 30), clipType: 'custom-clock', transition: { type: 'crossfade', duration: 0.4 } }],
    };
    const compiled = compilePlayerTransitions(config)!;
    expect(compiled.tracks.map(track => track.trackId)).toEqual(['V1']);
    const content = <TimelineRenderer config={config} astridElementHost={customHost} compiledTransitions={compiled} />;
    expect(renderFrame(content, 36, 30).querySelector('[data-host-frame="6"]')).not.toBeNull();
    expect(renderFrame(content, 59, 30).querySelector('[data-host-frame="29"]')).not.toBeNull();
    expect(renderFrame(content, 60, 30).querySelector('[data-host-frame]')).toBeNull();
  });
});
