import assert from 'node:assert/strict';
import {test} from 'node:test';
import type {CSSProperties, ReactElement} from 'react';
import {createElement} from 'react';
import {composeClipLook} from '../src/ClipLook';
import {DEFAULT_THEME, toRuntimeTheme} from '../src/ThemeContext';
import {cropClipPath} from '../src/lib/clip-look';
import {prepareScene, querySceneFrame} from '../src/scene-evaluation';
import type {ModifierDeclaration} from '../src/modifier-types';
import type {AssetRegistry, TimelineClip, TrackDefinition} from '../src/types';
import {VIDEO_INTERPRETATION} from '../src/scene-capabilities';

const visualTrack: TrackDefinition = {id: 'video', kind: 'visual', label: 'Video'};
const assets: AssetRegistry = {assets: {}};
const clip = (overrides: Partial<TimelineClip> = {}): TimelineClip => ({
  id: 'clip', at: 0, hold: 1, track: 'video', ...overrides,
});
const mediaProof = (file: string, contentSha256: string) => ({
  version: 1 as const,
  objectId: `sha256:${contentSha256}`,
  contentSha256,
  file,
  interpretation: VIDEO_INTERPRETATION,
  stream: {
    index: 0, codec: 'h264' as const, pixelFormat: 'yuv420p', profile: 'Main', level: '40',
    sampleAspectRatio: '1:1' as const, width: 1920, height: 1080,
  },
});
const prepare = (
  clips: readonly TimelineClip[],
  sceneAssets: AssetRegistry = assets,
  options: Parameters<typeof prepareScene>[5] = {},
) => prepareScene([{track: visualTrack, clips, transitions: [null]}], sceneAssets, 30, 1920, 1080, options);

test('proven opaque visual media reports visible covered content', () => {
  const hash = 'a'.repeat(64);
  const file = 'video.mp4';
  const scene = prepare([clip({id: 'picture', asset: 'video'})], {
    assets: {video: {file, type: 'video/mp4', resolution: '1920x1080', content_sha256: hash}},
  }, {roles: {picture: 'picture'}, capabilities: {media: {video: mediaProof(file, hash)}}});
  const frame = querySceneFrame(scene, 0);
  assert.equal(frame.coverage, 'COVERED');
  assert.equal(frame.content, 'CONTENT');
  assert.equal(frame.layers[0].visible, true);
  assert.equal(frame.layers[0].opaqueSupport, 'rect');
  assert.deepEqual(frame.findings, []);
});

test('scene roles use own clip-ID entries and preserve the track fallback', () => {
  const ownRoles = JSON.parse('{"__proto__":"background"}') as Readonly<Record<string, string>>;
  const overridden = querySceneFrame(prepare([clip({id: '__proto__'})], assets, {roles: ownRoles}), 0);
  assert.equal(overridden.layers[0].role, 'background');

  for (const id of ['__proto__', 'constructor', 'toString']) {
    const fallback = querySceneFrame(prepare([clip({id})], assets, {roles: {}}), 0);
    assert.equal(fallback.layers[0].role, 'content');
  }
});

test('scene clip-look uses render crop and builtin entrance geometry with half-open clocks', () => {
  const support = {identity: 'plate@1', frame: () => ({presence: 'present' as const,
    opaqueSupport: 'rect' as const, bounds: {status: 'known' as const, rect: {x: 0, y: 0, width: 1920, height: 1080}}})};
  const sceneFor = (overrides: Partial<TimelineClip>) => prepareScene([{track: visualTrack,
    clips: [{...clip({id: 'plate', clipType: 'plate', ...overrides})} as TimelineClip], transitions: [null]}], assets, 30, 1920, 1080,
  {elements: new Set(['plate']), capabilities: {components: {plate: support}}});

  const cropped = querySceneFrame(sceneFor({cropTop: .1}), 0).layers[0];
  assert.deepEqual(cropped.bounds, {status: 'known', rect: {x: 0, y: 108, width: 1920, height: 972}});
  assert.equal(cropped.fullFrame, false);

  const scaledEarly = querySceneFrame(sceneFor({entrance: {id: 'scale-in', durationFrames: 18}}), 0).layers[0];
  assert.deepEqual(scaledEarly.bounds, {status: 'known', rect: {x: 144, y: 81, width: 1632, height: 918}});
  assert.equal(scaledEarly.opacity, 0);
  assert.deepEqual(querySceneFrame(sceneFor({entrance: 'scale-in'}), 18).layers[0].bounds,
    {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}});

  const fadedEarly = querySceneFrame(sceneFor({entrance: 'fade-up'}), 0).layers[0];
  assert.deepEqual(fadedEarly.bounds, {status: 'known', rect: {x: 0, y: 40, width: 1920, height: 1040}});
  assert.equal(fadedEarly.opacity, 0);
  assert.deepEqual(querySceneFrame(sceneFor({entrance: 'fade-up'}), 18).layers[0].bounds,
    {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}});
});

test('scene clip-look matches full-canvas wrapper origin for off-center scale and fade-up', () => {
  const width = 1920;
  const height = 1080;
  const fps = 30;
  const theme = toRuntimeTheme(DEFAULT_THEME);
  const support = {identity: 'plate@1', frame: () => ({presence: 'present' as const,
    opaqueSupport: 'rect' as const, bounds: {status: 'known' as const, rect: {x: 100, y: 200, width: 600, height: 300}}})};
  const sceneFor = (entrance: TimelineClip['entrance'], crop = false) => prepareScene([{track: visualTrack,
    clips: [clip({id: 'plate', clipType: 'plate', entrance, ...(crop ? {cropTop: .1, cropLeft: .2} : {})})], transitions: [null]}],
  assets, fps, width, height, {elements: new Set(['plate']), capabilities: {components: {plate: support}}});
  const renderTree = (entrance: TimelineClip['entrance'], crop = false) => {
    const node = composeClipLook({clip: {...clip({id: 'plate', clipType: 'plate', entrance,
      ...(crop ? {cropTop: .1, cropLeft: .2} : {})})}, fps, kind: 'element', children: createElement('div')}, 6, theme) as
      ReactElement<{style: CSSProperties; children: ReactElement<{style?: CSSProperties}>}>;
    const animation = node.props.children;
    const renderAnimation = animation.type as (props: typeof animation.props) => ReactElement<{style: CSSProperties}>;
    return {outer: node.props.style, wrapper: renderAnimation(animation.props).props.style};
  };

  const scaled = renderTree({id: 'scale-in', durationFrames: 18, easing: 'linear'}, true);
  assert.equal(scaled.outer.clipPath, cropClipPath({cropTop: .1, cropLeft: .2} as TimelineClip));
  assert.equal(scaled.wrapper.transform, 'scale(0.9)');
  const scaledLayer = querySceneFrame(sceneFor({id: 'scale-in', durationFrames: 18, easing: 'linear'}, true), 6).layers[0];
  assert.deepEqual(scaledLayer.bounds, {status: 'known', rect: {x: 384, y: 234, width: 342, height: 270}});
  assert.equal(scaledLayer.opacity, 1 / 3);

  const faded = renderTree({id: 'fade-up', durationFrames: 18, easing: 'linear'});
  assert.equal(faded.wrapper.transform, 'translateY(26.66666666666667px)');
  const fadedLayer = querySceneFrame(sceneFor({id: 'fade-up', durationFrames: 18, easing: 'linear'}), 6).layers[0];
  assert.equal(fadedLayer.bounds.status, 'known');
  if (fadedLayer.bounds.status === 'known') {
    assert.equal(fadedLayer.bounds.rect.x, 100);
    assert.equal(fadedLayer.bounds.rect.width, 600);
    assert.ok(Math.abs(fadedLayer.bounds.rect.y - 226.66666666666667) < 1e-12);
    assert.ok(Math.abs(fadedLayer.bounds.rect.height - 300) < 1e-12);
  }
  assert.equal(fadedLayer.opacity, 1 / 3);
});

test('known clip-look does not manufacture geometry through an unknown custom modifier', () => {
  const modifier: ModifierDeclaration = {kind: 'modifier', element: 'custom', hosts: ['composition'],
    bounds: 'unknown', alpha: 'preserve', support: 'preserve',
    wrap: (_instance, _context, children) => createElement('span', null, children)};
  const scene = prepareScene([{track: visualTrack, clips: [clip({id: 'plate', clipType: 'plate', entrance: 'fade-up',
    modifiers: [{id: 'custom', element: 'custom', params: {}}]})], transitions: [null]}], assets, 30, 1920, 1080,
  {elements: new Set(['plate']), modifiers: {custom: modifier}, capabilities: {components: {plate: {
    identity: 'plate@1', frame: () => ({presence: 'present', opaqueSupport: 'rect',
      bounds: {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}}}),
  }}}});
  const layer = querySceneFrame(scene, 0).layers[0];
  assert.equal(layer.bounds.status, 'unknown');
  assert.ok(layer.findings.some(finding => finding.code === 'unknown-modifier-bounds'));
});

test('unresolved or unproven media remains unknown instead of being treated as absent', () => {
  const unresolved = querySceneFrame(prepare([clip({asset: 'missing'})]), 0);
  assert.equal(unresolved.coverage, 'UNKNOWN');
  assert.equal(unresolved.layers[0].visible, 'unknown');
  assert.ok(unresolved.findings.some(({code}) => code === 'unknown-media-alpha'));

  const hash = 'b'.repeat(64);
  const unproven = querySceneFrame(prepare([clip({id: 'unproven', asset: 'video'})], {
    assets: {video: {file: 'video.mp4', type: 'video/mp4', resolution: '1920x1080', content_sha256: hash}},
  }), 0);
  assert.equal(unproven.coverage, 'UNKNOWN');
  assert.equal(unproven.layers[0].visible, 'unknown');
  assert.ok(unproven.findings.some(({code}) => code === 'unknown-media-alpha'));
});

test('assetless native holds are visibly absent, while declared component support stays explicit', () => {
  const absent = querySceneFrame(prepare([clip({id: 'hold'})]), 0);
  assert.equal(absent.coverage, 'GAP');
  assert.equal(absent.layers[0].visible, false);
  assert.deepEqual(absent.findings, []);

  const component = clip({id: 'title', clipType: 'title'});
  const capability = {
    identity: 'title@1',
    frame: () => ({
      presence: 'present' as const,
      bounds: {status: 'known' as const, rect: {x: 0, y: 0, width: 1920, height: 1080}},
      opaqueSupport: 'none' as const,
    }),
  };
  const supported = querySceneFrame(prepare([component], assets, {
    elements: new Set(['title']), capabilities: {components: {title: capability}},
  }), 0);
  assert.equal(supported.layers[0].visible, true);
  assert.equal(supported.layers[0].coverage, 'partial');
  assert.deepEqual(supported.findings, []);

  const unknown = querySceneFrame(prepare([component], assets, {elements: new Set(['title'])}), 0);
  assert.equal(unknown.layers[0].visible, 'unknown');
  assert.ok(unknown.findings.some(({code}) => code === 'unknown-component-internals'));
  assert.ok(unknown.findings.some(({code}) => code === 'unknown-component-bounds'));
  assert.equal(unknown.coverage, 'UNKNOWN');
});

test('unknown modifier output bounds produce a finding and unknown coverage', () => {
  const hash = 'c'.repeat(64);
  const file = 'video.mp4';
  const modifier: ModifierDeclaration = {
    kind: 'modifier', element: 'vignette', hosts: ['composition'], bounds: 'unknown',
    alpha: 'preserve', support: 'preserve',
    wrap: (_instance, _context, children) => createElement('div', null, children),
  };
  const scene = prepare([clip({id: 'picture', asset: 'video', modifiers: [{id: 'v', element: 'vignette', params: {}}]})], {
    assets: {video: {file, type: 'video/mp4', resolution: '1920x1080', content_sha256: hash}},
  }, {
    roles: {picture: 'picture'},
    capabilities: {media: {video: mediaProof(file, hash)}},
    modifiers: {vignette: modifier},
  });
  const frame = querySceneFrame(scene, 0);
  assert.equal(frame.layers[0].visible, 'unknown');
  assert.equal(frame.layers[0].opacity, null);
  assert.equal(frame.coverage, 'UNKNOWN');
  assert.ok(frame.findings.some(({code}) => code === 'unknown-modifier-bounds'));
});

test('scene incoming vector consumes occurrence caps with ceil quantization and keeps omitted policy unchanged', () => {
  const clips = [clip({at: 0}), {...clip({id: 'incoming', at: 1}),
    app: {canonicalTiming: {occurrenceStartMs: 0, occurrenceDurationMs: 1501}}}];
  const fps = 24000 / 1001;
  const scene = prepareScene([{track: visualTrack, clips, transitions: [], incomingTransitions: [null, {T: 60}]}],
    assets, fps, 1920, 1080);
  const cap = Math.ceil(1.501 * fps);
  assert.equal(scene.tracks[0].prepared.plans[1].drawDuration, cap);
  assert.equal(querySceneFrame(scene, cap - 1).layers.at(-1)!.clipId, 'incoming');
  assert.deepEqual(querySceneFrame(scene, cap).layers, []);
  const native = prepareScene([{track: visualTrack, clips, transitions: []}], assets, fps, 1920, 1080);
  assert.equal(querySceneFrame(native, cap).layers[0].clipId, 'incoming');
});
