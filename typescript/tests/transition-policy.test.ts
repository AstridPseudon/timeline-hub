import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createElement, type ComponentProps, type ReactElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals, useCurrentFrame} from 'remotion';
import {Video} from '@remotion/media';
import {TimelineComposition, prepareCompositionScene, querySceneFrame, DEFAULT_THEME, toRuntimeTheme,
  type TimelineClip, type TrackDefinition, type AssetRegistry, type CompositionRegistries,
  type ModifierRegistry, type EffectProps} from '../src/index';
import {VisualClip} from '../src/VisualClip';

const theme = toRuntimeTheme(DEFAULT_THEME);
const track: TrackDefinition = {id: 'visual', kind: 'visual', label: 'Visual', volume: .8};
const assets: AssetRegistry = {assets: {video: {file: 'https://example.test/video.mp4', type: 'video/mp4', resolution: '1920x1080'}}};
const pair = (policy = true, id = 'fade'): TimelineClip[] => [
  {id: 'outgoing', track: track.id, at: 2, from: 1, to: 3, speed: 2, asset: 'video',
    transition: {id, durationFrames: 12, ...(policy ? {incomingPolicy: 'preroll-crossfade'} : {})}},
  {id: 'incoming', track: track.id, at: 3, from: 3, to: 5, speed: 2, volume: .5, asset: 'video',
    params: {fadeIn: .4, fadeOut: .4}},
];

const render = (content: ReactElement, frame: number, fps = 30) => {
  const video = {id: 'test', width: 1920, height: 1080, fps, durationInFrames: 200,
    defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
    nonce: [], schema: null, calculateMetadata: null, stack: null};
  return renderToStaticMarkup(createElement(Internals.CompositionManager.Provider, {
    value: {compositions: [video], currentCompositionMetadata: null, folders: [],
      canvasContent: {type: 'composition', compositionId: 'test'}},
  }, createElement(Internals.TimelineContext.Provider, {
    value: {frame: {test: frame}, playing: false, imperativePlaying: {current: false}, audioAndVideoTags: {current: []}},
  }, createElement(Internals.CanUseRemotionHooksProvider, null, content))));
};

const composition = (clips: TimelineClip[], registries: CompositionRegistries = {}, modifierRegistry?: ModifierRegistry,
  selectedTrack = track, selectedAssets = assets) => createElement(TimelineComposition, {
  timeline: {theme: 'default', tracks: [selectedTrack], clips}, assets: selectedAssets, registries, modifierRegistry,
});
const prepare = (clips: TimelineClip[], registries: CompositionRegistries = {}, fps = 30) =>
  prepareCompositionScene([{track, clips}], assets, fps, theme, 1920, 1080, undefined, undefined, {}, '', {}, registries);

test('actual native render inputs use preroll source clock, unchanged trims/rate/gain, and no extra mount', () => {
  const seen: {id: string; frame: number; source: number; volume: number; muted: boolean; trimAfter: number}[] = [];
  // Observe the real VisualClip result under the real Sequence/TransitionLayer
  // clock, before handing it to the decoder. No decoder, browser or pixels claimed.
  const NativeProbe = ({content}: {content: ReactElement<ComponentProps<typeof VisualClip>>}) => {
    assert.equal(content.type, VisualClip);
    const video = VisualClip(content.props) as ReactElement<{
      trimBefore: number; trimAfter: number; playbackRate: number; volume: number; muted: boolean;
    }>;
    assert.equal(video.type, Video);
    const frame = useCurrentFrame();
    const {trimBefore, trimAfter, playbackRate, volume, muted} = video.props;
    seen.push({id: content.props.clip.id, frame, source: trimBefore + frame * playbackRate, volume, muted, trimAfter});
    return createElement('i', {'data-source': trimBefore + frame * playbackRate});
  };
  const modifiers: ModifierRegistry = {probe: {kind: 'modifier', element: 'probe', hosts: ['composition'],
    bounds: 'preserve', alpha: 'preserve', support: 'preserve',
    wrap: (_instance, _context, content) => createElement(NativeProbe, {content: content as ReactElement<ComponentProps<typeof VisualClip>>})}};
  for (const id of ['fade', 'cross-fade']) {
    for (const policy of [false, true]) {
      for (const [align, beforeDraw, midpoint, clocks] of [
        ['end', 77, 84, [[78, 0, 90, 0, 90], [84, 6, 102, 0, 90], [89, 11, 112, 0, 90],
          [90, 12, 114, 0, 90], [119, 41, 172, 29, 148]]],
        ['center', 83, 90, [[84, 0, 90, 0, 90], [90, 6, 102, 0, 90], [95, 11, 112, 5, 100],
          [96, 12, 114, 6, 102], [119, 35, 160, 29, 148]]],
        ['start', 89, 96, [[90, 0, 90, 0, 90], [96, 6, 102, 6, 102], [101, 11, 112, 11, 112],
          [102, 12, 114, 12, 114], [119, 29, 148, 29, 148]]],
      ] as const) {
        const clips = pair(policy, id).map(clip => Object.freeze({...clip,
          ...(clip.transition ? {transition: {...clip.transition as object, align}} : {}),
          modifiers: [{id: 'probe', element: 'probe', params: {}}]}));
        const before = JSON.stringify(clips);
        const scene = prepareCompositionScene([{track, clips}], assets, 30, theme, 1920, 1080, modifiers);
        for (const [frame, nativeFrame, source, legacyFrame, legacySource] of clocks) {
          seen.length = 0;
          render(composition(clips, {}, modifiers), frame);
          const incoming = seen.find(item => item.id === 'incoming')!;
          assert.deepEqual(incoming, {id: 'incoming', frame: policy ? nativeFrame : legacyFrame,
            source: policy ? source : legacySource, volume: .4, muted: false, trimAfter: 150});
          const layer = querySceneFrame(scene, frame).layers.find(layer => layer.clipId === 'incoming')!;
          assert.equal(layer.contentFrame, policy ? nativeFrame : legacyFrame);
          if (frame === midpoint) {
            assert.deepEqual(querySceneFrame(scene, frame).layers.map(layer => layer.transitionOpacity),
              !policy && id === 'fade' ? [0, 0] : [1, .5]);
          }
        }
        for (const [frame, expected] of [[beforeDraw, ['outgoing']], [120, []]] as const) {
          seen.length = 0;
          render(composition(clips, {}, modifiers), frame);
          assert.deepEqual(seen.map(item => item.id), expected);
          assert.deepEqual(querySceneFrame(scene, frame).layers.map(layer => layer.clipId), expected);
        }
        seen.length = 0;
        render(composition(clips, {}, modifiers, {...track, muted: true}), midpoint);
        assert.equal(seen.find(item => item.id === 'incoming')!.volume, 0);
        assert.equal(seen.find(item => item.id === 'incoming')!.muted, true);
        assert.equal(JSON.stringify(clips), before);
      }
    }
  }
});

test('public scene capability and actual element clock share preroll plus speed remap at rational fps', () => {
  const rendered: number[] = [];
  const queried: number[] = [];
  const Clock = Object.assign((_props: EffectProps) => {
    rendered.push(useCurrentFrame());
    return createElement('b', null, 'clock');
  }, {prepareSceneCapability: () => ({identity: 'clock@1', frame: (frame: number) => {
    queried.push(frame);
    return {presence: 'present' as const, opaqueSupport: 'rect' as const,
      bounds: {status: 'known' as const, rect: {x: 0, y: 0, width: 1920, height: 1080}}};
  }})});
  const registries = {effects: {clock: Clock}};
  for (const [fps, outgoingAt, incomingAt, from, to, T, middle, boundary, end, nativeClock, boundaryClock] of [
    [30, 2, 3, 3, 5, 12, 84, 90, 120, 12, 24],
    [24000 / 1001, 0, 1001 / 1000, 1001 / 1000, 3003 / 1000, 6, 21, 24, 48, 6, 12],
  ]) {
    for (const policy of [false, true]) {
      const clips: TimelineClip[] = [
        {id: 'outgoing', track: track.id, at: outgoingAt, from, to, speed: 2,
          transition: {id: 'fade', durationFrames: T, ...(policy ? {incomingPolicy: 'preroll-crossfade'} : {})}},
        {id: 'incoming', track: track.id, at: incomingAt, from, to, speed: 2, clipType: 'clock'},
      ];
      const scene = prepare(clips, registries, fps);
      for (const [frame, expected] of [[middle, policy ? nativeClock : 0], [boundary, policy ? boundaryClock : 0]]) {
        rendered.length = 0;
        render(composition(clips, registries), frame, fps);
        assert.deepEqual(rendered, [expected]);
        queried.length = 0;
        querySceneFrame(scene, frame);
        assert.deepEqual(queried, [expected]);
      }
      rendered.length = 0;
      render(composition(clips, registries), end, fps);
      assert.deepEqual(rendered, []);
      assert.deepEqual(querySceneFrame(scene, end).layers, []);
    }
  }
});

test('public render keeps plain image cuts/crossfades and default dip, refusing unknown opt-in implementations', () => {
  const images: AssetRegistry = {assets: {video: {file: 'https://example.test/image.jpg', type: 'image/jpeg'}}};
  const clips = pair(false).map(clip => ({...clip, from: undefined, to: undefined, speed: undefined, hold: 1}));
  const cut = clips.map(clip => ({...clip, transition: undefined}));
  assert.equal((render(composition(cut, {}, undefined, track, images), 84).match(/<img /g) ?? []).length, 1);
  assert.equal((render(composition(cut, {}, undefined, track, images), 90).match(/<img /g) ?? []).length, 1);
  const crossfade = [{...clips[0], transition: {id: 'cross-fade', durationFrames: 12}}, clips[1]];
  const dissolve = render(composition(crossfade, {}, undefined, track, images), 84);
  assert.equal((dissolve.match(/<img /g) ?? []).length, 2);
  assert.match(dissolve, /opacity:0\.5/);
  const dip = render(composition(clips, {}, undefined, track, images), 84);
  assert.equal((dip.match(/opacity:0[;"]/g) ?? []).length, 2);
  const native = [{...clips[0], transition: {id: 'fade', durationFrames: 12, incomingPolicy: 'preroll-crossfade'}}, clips[1]];
  assert.match(render(composition(native, {}, undefined, track, images), 84), /opacity:0\.5/);
  assert.throws(() => prepare(pair(true, 'custom')), /Unknown transition/);
  const custom = {transitions: {custom: () => ({presentation: null, timing: null})}};
  assert.throws(() => prepare(pair(true, 'custom'), custom), /Unsupported incoming transition policy or implementation/);
});

test('overlapping windows use the same per-boundary clocks in the public scene and render', () => {
  const rendered: [string, number][] = [];
  const queried: [string, number][] = [];
  const Clock = Object.assign(({clip}: EffectProps) => {
    rendered.push([clip.id, useCurrentFrame()]);
    return createElement('b', null, clip.id);
  }, {prepareSceneCapability: ({clip}: {clip: TimelineClip}) => ({identity: clip.id, frame: (frame: number) => {
    queried.push([clip.id, frame]);
    return {presence: 'present' as const, opaqueSupport: 'rect' as const,
      bounds: {status: 'known' as const, rect: {x: 0, y: 0, width: 1920, height: 1080}}};
  }})});
  const registries = {effects: {clock: Clock}};
  for (const policy of [false, true]) {
    const clips: TimelineClip[] = [
      {id: 'a', track: track.id, clipType: 'clock', at: 0, hold: 1,
        transition: {id: 'fade', durationFrames: 12, align: 'start', incomingPolicy: 'preroll-crossfade'}},
      {id: 'b', track: track.id, clipType: 'clock', at: 1, hold: .4,
        transition: {id: 'fade', durationFrames: 12, ...(policy ? {incomingPolicy: 'preroll-crossfade'} : {})}},
      {id: 'c', track: track.id, clipType: 'clock', at: 1.4, hold: 1},
    ];
    const scene = prepare(clips, registries);
    for (const [frame, expected] of [[36, [['a', 29], ['b', 6], ['c', policy ? 6 : 0]]],
      [42, [['c', policy ? 12 : 0]]]] as const) {
      rendered.length = 0;
      render(composition(clips, registries), frame);
      assert.deepEqual(rendered, expected);
      queried.length = 0;
      const answer = querySceneFrame(scene, frame);
      assert.deepEqual(queried, expected);
      assert.deepEqual(answer.layers.map(layer => layer.transitionOpacity), frame === 42 ? [1] : policy ? [1, .5, .5] : [1, 0, 0]);
    }
  }
});
