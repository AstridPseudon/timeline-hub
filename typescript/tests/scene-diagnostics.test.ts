import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createElement, type ReactElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals, useCurrentFrame} from 'remotion';
import {prepareCompositionScene, querySceneFrame, querySceneOcclusion, TimelineComposition,
  DEFAULT_THEME, toRuntimeTheme, type TimelineClip, type TrackDefinition, type EffectProps,
  type ModifierBounds, type ModifierRegistry, type ComponentFrameSupport, type ComponentCapabilityContext} from '../src/index';
import {querySceneOcclusion as pureOcclusion} from '../src/evaluation';
import type {RenderBounds} from '../src/lib/render-bounds';

const assets = {assets: {}};
const track: TrackDefinition = {id: 'visual', kind: 'visual', label: 'Visual'};
const theme = toRuntimeTheme(DEFAULT_THEME);
const box = (x = 0, y = 0, width = 100, height = 100): ModifierBounds =>
  ({status: 'known', rect: {x, y, width, height}});
const clip = (id: string, overrides: Partial<TimelineClip> = {}): TimelineClip =>
  ({id, track: track.id, clipType: 'plate', at: 0, hold: 2, ...overrides});
let capabilityCalls = 0;
const plateAt = (clip: TimelineClip): ComponentFrameSupport => {
  const params = clip.params as {rect?: RenderBounds; kind?: string} | undefined;
  return {presence: params?.kind === 'absent' ? 'absent' : 'present',
    bounds: params?.kind === 'unknown' ? {status: 'unknown', reason: 'Fixture has no geometry declaration'}
      : {status: 'known', rect: params?.rect ?? {x: 0, y: 0, width: 100, height: 100}},
    opaqueSupport: params?.kind === 'glyph' ? 'none' : 'rect'};
};
// Registered ordinary fixture: drawing and capability use the same pure geometry.
const Plate = Object.assign(({clip}: EffectProps) => {
  const support = plateAt(clip);
  return support.presence === 'absent' || support.bounds.status === 'unknown' ? null
    : createElement('div', {style: {position: 'absolute', left: support.bounds.rect.x, top: support.bounds.rect.y,
      width: support.bounds.rect.width, height: support.bounds.rect.height,
      background: support.opaqueSupport === 'rect' ? 'black' : 'transparent'}}, support.opaqueSupport === 'none' ? 'O' : null);
}, {prepareSceneCapability: ({clip}: ComponentCapabilityContext) => ({identity: 'plate@1', frame: () => {
  capabilityCalls++;
  return plateAt(clip);
}})});
const prepare = (clips: TimelineClip[], modifiers?: ModifierRegistry) => prepareCompositionScene([{track, clips}],
  assets, 30, theme, 100, 100, modifiers, undefined, {}, '', {}, {effects: {plate: Plate}});
const known = (occluderId: string | null, fraction = 0) => ({status: 'known', occluderId, fraction});
const rectParams = (x: number, y: number, width: number, height: number) => ({rect: {x, y, width, height}});

test('public scene names full cover in actual same-track painter order without re-evaluating callbacks', () => {
  assert.strictEqual(querySceneOcclusion, pureOcclusion);
  capabilityCalls = 0;
  const scene = prepare([clip('lower'), clip('upper')]);
  const answer = querySceneFrame(scene, 0);
  assert.deepEqual(answer.layers.map(layer => [layer.clipId, layer.visible, layer.z]), [['lower', false, 1], ['upper', true, 0]]);
  assert.deepEqual(querySceneOcclusion(answer, 'lower', .9), known('upper', 1));
  assert.deepEqual(querySceneOcclusion(answer, 'upper', .98), known(null));
  assert.equal(capabilityCalls, 2);
  assert.deepEqual(querySceneOcclusion(querySceneFrame(prepare([clip('upper'), clip('lower')]), 0), 'lower', .9), known(null));
});

test('fractional thresholds use fixed rectangular support areas and include the threshold', () => {
  const answer = querySceneFrame(prepare([clip('target'), clip('ninety', {params: rectParams(0, 0, 90, 100)})]), 0);
  assert.equal(answer.layers[0].visible, true);
  assert.deepEqual(querySceneOcclusion(answer, 'target', .9), known('ninety', .9));
  assert.deepEqual(querySceneOcclusion(answer, 'target', .98), known(null));
  const cover = querySceneFrame(prepare([clip('target'), clip('cover', {params: rectParams(0, 0, 98, 100)})]), 0);
  assert.deepEqual(querySceneOcclusion(cover, 'target', .98), known('cover', .98));
  assert.deepEqual(querySceneOcclusion(cover, 'target', 1), known(null));
  for (const fraction of [NaN, Infinity, 0, -.1, 1.01]) {
    assert.throws(() => querySceneOcclusion(answer, 'target', fraction), /evaluation_inputs_invalid/);
  }
  for (const dimensions of [
    {width: undefined, height: answer.height}, {width: NaN, height: answer.height},
    {width: 0, height: answer.height}, {width: answer.width, height: undefined},
    {width: answer.width, height: NaN}, {width: answer.width, height: 0},
  ]) {
    assert.throws(() => querySceneOcclusion({...answer, ...dimensions} as typeof answer, 'target', .9), /evaluation_inputs_invalid/);
  }
});

test('track order and frontmost qualifying single layer determine the named occluder', () => {
  const scene = prepareCompositionScene([
    {track, clips: [clip('target')]},
    {track: {...track, id: 'upper'}, clips: [clip('back', {track: 'upper', params: rectParams(0, 0, 95, 100)}),
      clip('front', {track: 'upper', params: rectParams(0, 0, 90, 100)})]},
  ], assets, 30, theme, 100, 100, undefined, undefined, {}, '', {}, {effects: {plate: Plate}});
  assert.deepEqual(querySceneOcclusion(querySceneFrame(scene, 0), 'target', .9), known('front', .9));
  assert.deepEqual(querySceneOcclusion(querySceneFrame(scene, 0), 'target', .94), known('back', .95));
  // Two half-width plates collectively cover, but neither meets a single-layer threshold.
  const tiled = querySceneFrame(prepare([clip('target'), clip('left', {params: rectParams(0, 0, 50, 100)}),
    clip('right', {params: rectParams(50, 0, 50, 100)})]), 0);
  assert.deepEqual(querySceneOcclusion(tiled, 'target', .9), known(null));
});

test('unknown uppers and glyph holes stay unknown; transparent uppers cannot become opaque', () => {
  const query = (uppers: TimelineClip[]) => querySceneOcclusion(querySceneFrame(prepare([clip('target'), ...uppers]), 0), 'target', .9);
  assert.equal(query([clip('unknown', {params: {kind: 'unknown'}})]).status, 'unknown');
  assert.equal(query([clip('glyph', {params: {kind: 'glyph'}})]).status, 'unknown');
  assert.equal(query([clip('unknown', {params: {kind: 'unknown'}}), clip('transparent', {opacity: .5}),
    clip('glyph', {params: {kind: 'glyph'}})]).status, 'unknown');
  assert.deepEqual(query([clip('transparent', {opacity: .5})]), known(null));
  assert.deepEqual(query([clip('transparent', {opacity: .5}), clip('another', {opacity: .5})]), known(null));
  assert.deepEqual(query([clip('small-glyph', {params: {...rectParams(0, 0, 50, 100), kind: 'glyph'}})]), known(null));
  assert.deepEqual(query([clip('solid'), clip('unknown', {params: {kind: 'unknown'}})]), known('solid', 1));
  assert.deepEqual(query([clip('unknown', {params: {kind: 'unknown'}}), clip('solid')]), known('solid', 1));
});

test('absence, opacity zero and offscreen targets are distinct from occlusion; known-none differs from unknown', () => {
  for (const target of [clip('target', {params: {kind: 'absent'}}), clip('target', {opacity: 0}),
    clip('target', {params: rectParams(100, 0, 100, 100)}), clip('target', {params: rectParams(0, 0, 0, 100)})]) {
    const answer = querySceneFrame(prepare([target, clip('upper')]), 0);
    assert.equal(answer.layers[0].visible, false);
    assert.deepEqual(querySceneOcclusion(answer, 'target', .9), known(null));
  }
  assert.deepEqual(querySceneOcclusion(querySceneFrame(prepare([clip('target')]), 60), 'target', .9), known(null));
  assert.deepEqual(querySceneOcclusion(querySceneFrame(prepare([clip('target')]), 0), 'target', .9), known(null));
  assert.equal(querySceneOcclusion(querySceneFrame(prepare([clip('target', {params: {kind: 'unknown'}})]), 0), 'target', .9).status, 'unknown');
});

test('partial offscreen target denominator is its clipped output rectangle, not full bounds or glyph pixels', () => {
  const answer = querySceneFrame(prepare([clip('target', {params: rectParams(-50, 0, 100, 100)}),
    clip('upper', {params: rectParams(0, 0, 45, 100)})]), 0);
  assert.deepEqual(querySceneOcclusion(answer, 'target', .9), known('upper', .9));
  assert.deepEqual(querySceneOcclusion(answer, 'target', .98), known(null));
  const full = querySceneFrame(prepare([clip('target', {params: rectParams(-50, 0, 100, 100)}), clip('upper')]), 0);
  assert.equal(full.layers[0].visible, false);
  assert.deepEqual(querySceneOcclusion(full, 'target', 1), known('upper', 1));
});

const modifier = (bounds: 'preserve' | 'unknown'): ModifierRegistry => ({shift: {
  kind: 'modifier', element: 'shift', hosts: ['composition'], bounds, alpha: 'preserve', support: 'preserve',
  // A half-turn preserves these 100x100 fixtures' filled outer rectangles while
  // moving internal semantic regions. Translation instead has undeclared bounds.
  wrap: (_instance, _context, children) => createElement('div', {style: {width: 100, height: 100,
    transform: bounds === 'preserve' ? 'rotate(180deg)' : 'translateX(10px)'}}, children),
}});

test('animation and undeclared modifier geometry cannot manufacture opaque occlusion', () => {
  for (const upper of [clip('upper', {entrance: 'fade-up'}), clip('upper', {cropTop: .1})]) {
    const answer = querySceneFrame(prepare([clip('target'), upper], modifier('unknown')), 10);
    assert.equal(answer.layers[0].visible, true);
    assert.equal(querySceneOcclusion(answer, 'target', .9).status, 'known');
  }
  const answer = querySceneFrame(prepare([clip('target'), clip('upper', {
    modifiers: [{id: 'shift', element: 'shift', params: {}}],
  })], modifier('unknown')), 10);
  assert.equal(answer.layers[0].visible, true);
  assert.equal(querySceneOcclusion(answer, 'target', .9).status, 'unknown');
});

test('opaque occlusion uses the actual transition and track opacity, modifier support and blend facts', () => {
  const tracks = [
    {track, clips: [clip('target', {hold: 3})]},
    {track: {...track, id: 'upper'}, clips: [
      clip('empty', {track: 'upper', clipType: undefined, hold: 1,
        transition: {id: 'fade', durationFrames: 12, incomingPolicy: 'preroll-crossfade'}}),
      clip('upper', {track: 'upper', at: 1}),
    ]},
  ];
  const prepareTracks = (upperTrack: TrackDefinition) => prepareCompositionScene([
    tracks[0], {...tracks[1], track: upperTrack},
  ], assets, 30, theme, 100, 100, undefined, undefined, {}, '', {}, {effects: {plate: Plate}});
  const scene = prepareTracks(tracks[1].track);
  const middle = querySceneFrame(scene, 24);
  assert.equal(middle.layers.find(layer => layer.clipId === 'upper')!.opacity, .5);
  assert.deepEqual(querySceneOcclusion(middle, 'target', .9), known(null));
  assert.deepEqual(querySceneOcclusion(querySceneFrame(scene, 30), 'target', .98), known('upper', 1));
  assert.deepEqual(querySceneOcclusion(querySceneFrame(prepareTracks({...tracks[1].track, opacity: .5}), 30), 'target', .9), known(null));
  assert.equal(querySceneOcclusion(querySceneFrame(prepareTracks({...tracks[1].track, blendMode: 'multiply'}), 30), 'target', .9).status, 'unknown');
  const preserved = prepare([clip('target'), clip('upper', {modifiers: [{id: 'shift', element: 'shift', params: {}}]})], modifier('preserve'));
  assert.deepEqual(querySceneOcclusion(querySceneFrame(preserved, 0), 'target', .98), known('upper', 1));
});

const speakerAt = (frame: number): ComponentFrameSupport => ({
  presence: 'present', opaqueSupport: 'rect', bounds: box(),
  diagnostics: {motion: {zoom: 1 + frame / 24, panX: frame * 2, mouthOpen: frame % 4 / 4},
    face: box(frame * 2, 10, 20 * (1 + frame / 24), 30 * (1 + frame / 24)),
    mouth: box(frame * 2 + 5, 30, 10, 5 + frame % 4),
    // Explicit layout box and CSS size, not measured glyph bounds/font alpha.
    text: {bounds: box(0, 80, 80, 20), minPx: 12 + frame / 2}},
});
const rendered: {frame: number; faceX: number; mouthX: number; minPx: number; zoom: number}[] = [];
const Speaker = Object.assign((_props: EffectProps) => {
  const frame = useCurrentFrame();
  const diagnostics = speakerAt(frame).diagnostics!;
  const face = (diagnostics.face as {status: 'known'; rect: RenderBounds}).rect;
  const mouth = (diagnostics.mouth as {status: 'known'; rect: RenderBounds}).rect;
  rendered.push({frame, faceX: face.x, mouthX: mouth.x, minPx: diagnostics.text!.minPx!, zoom: diagnostics.motion!.zoom});
  return createElement('div', {style: {position: 'absolute', width: 100, height: 100, background: 'black', overflow: 'hidden'}},
    createElement('div', {style: {position: 'absolute', left: face.x, top: face.y, width: face.width, height: face.height, background: 'red'}}),
    createElement('div', {style: {position: 'absolute', left: mouth.x, top: mouth.y, width: mouth.width, height: mouth.height, background: 'white'}}),
    createElement('div', {style: {position: 'absolute', left: 0, top: 80, width: 80, height: 20,
      overflow: 'hidden', fontSize: diagnostics.text!.minPx}}, 'Fixture'));
}, {prepareSceneCapability: () => ({identity: 'speaker@1', frame: speakerAt})});

const render = (content: ReactElement, frame: number, fps: number) => {
  const video = {id: 'test', width: 100, height: 100, fps, durationInFrames: 200,
    defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
    nonce: [], schema: null, calculateMetadata: null, stack: null};
  return renderToStaticMarkup(createElement(Internals.CompositionManager.Provider, {
    value: {compositions: [video], currentCompositionMetadata: null, folders: [], canvasContent: {type: 'composition', compositionId: 'test'}},
  }, createElement(Internals.TimelineContext.Provider, {
    value: {frame: {test: frame}, playing: false, imperativePlaying: {current: false}, audioAndVideoTags: {current: []}},
  }, createElement(Internals.CanUseRemotionHooksProvider, null, content))));
};

test('declared face/mouth/text and intrinsic motion share the actual component clock at speed 2, preroll and rational fps', () => {
  const registries = {effects: {speaker: Speaker}};
  for (const [fps, incomingAt, transitionFrames, middle, boundary, end, expectedFrame, expectedBoundary] of [
    [30, 1, 12, 24, 30, 60, 12, 24],
    [24000 / 1001, 1001 / 1000, 6, 21, 24, 48, 6, 12],
  ]) {
    for (const policy of [false, true]) {
      const clips = [clip('outgoing', {clipType: undefined, hold: incomingAt,
        transition: {id: 'fade', durationFrames: transitionFrames, ...(policy ? {incomingPolicy: 'preroll-crossfade'} : {})}}),
      clip('speaker', {clipType: 'speaker', at: incomingAt, from: 0, to: incomingAt * 2, speed: 2})];
      const scene = prepareCompositionScene([{track, clips}], assets, fps, theme, 100, 100,
        undefined, undefined, {}, 'fixture-renderer', {}, registries);
      for (const [frame, expected] of [[middle, policy ? expectedFrame : 0], [boundary, policy ? expectedBoundary : 0]]) {
        const layer = querySceneFrame(scene, frame).layers.find(layer => layer.clipId === 'speaker')!;
        assert.deepEqual(layer.diagnostics, {motion: {zoom: 1 + expected / 24, panX: expected * 2, mouthOpen: expected % 4 / 4},
          face: box(expected * 2, 10, 20 * (1 + expected / 24), 30 * (1 + expected / 24)),
          mouth: box(expected * 2 + 5, 30, 10, 5 + expected % 4), text: {bounds: box(0, 80, 80, 20), minPx: 12 + expected / 2}});
        rendered.length = 0;
        const markup = render(createElement(TimelineComposition, {
          timeline: {theme: 'default', tracks: [track], clips}, assets, registries,
        }), frame, fps);
        assert.deepEqual(rendered, [{frame: expected, faceX: expected * 2, mouthX: expected * 2 + 5, minPx: 12 + expected / 2, zoom: 1 + expected / 24}]);
        assert.match(markup, new RegExp('font-size:' + (12 + expected / 2) + 'px'));
      }
      assert.deepEqual(querySceneFrame(scene, end).layers, []);
    }
  }
  // Fixed expected values independently pin helper behavior; not just render/query agreement.
  assert.deepEqual(speakerAt(12).diagnostics, {motion: {zoom: 1.5, panX: 24, mouthOpen: 0},
    face: box(24, 10, 30, 45), mouth: box(29, 30, 10, 5), text: {bounds: box(0, 80, 80, 20), minPx: 18}});
});

test('missing diagnostic declarations stay unknown instead of implying static motion or empty regions', () => {
  const declared = querySceneFrame(prepare([clip('plate')]), 0).layers[0];
  assert.equal(Object.hasOwn(declared, 'diagnostics'), false);
  const uninstrumented = querySceneFrame(prepare([clip('unknown', {clipType: 'uninstrumented'})]), 0).layers[0];
  assert.equal(uninstrumented.visible, 'unknown');
  assert.equal(uninstrumented.diagnostics, undefined);
});

test('explicit unknown diagnostics and component-owned fact objects survive queries without mutation', () => {
  const source: ComponentFrameSupport = {presence: 'present', opaqueSupport: 'none', bounds: box(),
    diagnostics: {face: {status: 'unknown', reason: 'No admitted face source'},
      text: {bounds: {status: 'unknown', reason: 'No admitted font metrics'}, minPx: 18}}};
  const before = JSON.stringify(source);
  const Declared = Object.assign(() => null, {prepareSceneCapability: () => ({identity: 'partial@1', frame: () => source})});
  const preparePartial = (overrides: Partial<TimelineClip>) => prepareCompositionScene([
    {track, clips: [clip('partial', {clipType: 'partial', ...overrides})]},
  ], assets, 30, theme, 100, 100, undefined, undefined, {}, '', {}, {effects: {partial: Declared}});
  const answer = querySceneFrame(preparePartial({}), 12).layers[0];
  assert.deepEqual(answer.diagnostics, source.diagnostics);
  assert.equal(answer.diagnostics!.motion, undefined);
  assert.equal(answer.diagnostics!.mouth, undefined);
  assert.equal(querySceneFrame(preparePartial({entrance: 'fade-up'}), 12).layers[0].diagnostics!.text!.minPx, undefined);
  assert.equal(JSON.stringify(source), before);
  assert.equal(querySceneFrame(preparePartial({}), 12).layers[0].diagnostics!.text!.minPx, 18);
});

test('unknown transforms and even preserved outer bounds invalidate final semantic regions, retaining intrinsic motion', () => {
  for (const [overrides, modifiers] of [
    [{entrance: 'fade-up'}, undefined], [{cropTop: .1}, undefined],
    [{modifiers: [{id: 'shift', element: 'shift', params: {}}]}, modifier('unknown')],
    [{modifiers: [{id: 'shift', element: 'shift', params: {}}]}, modifier('preserve')],
    [{modifiers: [{id: 'missing', element: 'missing', params: {}}]}, undefined],
  ] as [Partial<TimelineClip>, ModifierRegistry | undefined][]) {
    const clips = [clip('speaker', {clipType: 'speaker', ...overrides})];
    const scene = prepareCompositionScene([{track, clips}], assets, 30, theme, 100, 100,
      modifiers, undefined, {}, '', {}, {effects: {speaker: Speaker}});
    const layer = querySceneFrame(scene, 12).layers[0];
    assert.deepEqual(layer.diagnostics!.motion, {zoom: 1.5, panX: 24, mouthOpen: 0});
    assert.equal(layer.diagnostics!.face!.status, 'unknown');
    assert.equal(layer.diagnostics!.mouth!.status, 'unknown');
    assert.equal(layer.diagnostics!.text!.bounds.status, 'unknown');
    assert.equal(layer.diagnostics!.text!.minPx, undefined);
  }
});

test('nonfinite diagnostic scalars, sizes and invalid rectangles stay unknown with findings', () => {
  const Invalid = Object.assign(() => null, {prepareSceneCapability: () => ({identity: 'invalid@1', frame: () => ({
    ...speakerAt(0), diagnostics: {motion: {zoom: NaN}, face: box(0, 0, -1, 10),
      mouth: box(Infinity, 0, 1, 1), text: {bounds: box(), minPx: Infinity}},
  })})});
  const scene = prepareCompositionScene([{track, clips: [clip('invalid', {clipType: 'invalid'})]}], assets, 30, theme,
    100, 100, undefined, undefined, {}, '', {}, {effects: {invalid: Invalid}});
  const answer = querySceneFrame(scene, 0);
  const layer = answer.layers[0];
  assert.equal(layer.diagnostics!.motion, undefined);
  assert.equal(layer.diagnostics!.face!.status, 'unknown');
  assert.equal(layer.diagnostics!.mouth!.status, 'unknown');
  assert.equal(layer.diagnostics!.text!.minPx, undefined);
  assert.equal(layer.diagnostics!.text!.bounds.status, 'known');
  assert.equal(layer.findings.filter(finding => finding.code === 'invalid-component-diagnostics').length, 4);
  assert.equal(layer.opacity, 1);
  assert.equal(layer.visible, true);
});

test('malformed motion stays unknown without accepting scalars or throwing on null', () => {
  for (const motion of [42, null, []]) {
    const Invalid = Object.assign(() => null, {prepareSceneCapability: () => ({identity: 'invalid-motion@1', frame: () => ({
      presence: 'present' as const, opaqueSupport: 'none' as const, bounds: box(),
      diagnostics: {motion} as unknown as ComponentFrameSupport['diagnostics'],
    })})});
    const scene = prepareCompositionScene([{track, clips: [clip('invalid-motion', {clipType: 'invalid-motion'})]}], assets,
      30, theme, 100, 100, undefined, undefined, {}, '', {}, {effects: {['invalid-motion']: Invalid}});
    const layer = querySceneFrame(scene, 0).layers[0];
    assert.equal(layer.diagnostics!.motion, undefined);
    assert.ok(layer.findings.some(finding => finding.code === 'invalid-component-diagnostics'));
  }
});

test('plain, null-prototype and explicit empty motion records remain valid', () => {
  const nullPrototype = Object.create(null) as Record<string, number>;
  nullPrototype.panX = 2;
  for (const motion of [{zoom: 1}, nullPrototype, {}]) {
    const Valid = Object.assign(() => null, {prepareSceneCapability: () => ({identity: 'valid-motion@1', frame: () => ({
      presence: 'present' as const, opaqueSupport: 'none' as const, bounds: box(),
      diagnostics: {motion} as ComponentFrameSupport['diagnostics'],
    })})});
    const scene = prepareCompositionScene([{track, clips: [clip('valid-motion', {clipType: 'valid-motion'})]}], assets,
      30, theme, 100, 100, undefined, undefined, {}, '', {}, {effects: {['valid-motion']: Valid}});
    const layer = querySceneFrame(scene, 0).layers[0];
    assert.deepEqual(layer.diagnostics!.motion, {...motion});
    assert.deepEqual(layer.findings, []);
  }
});
