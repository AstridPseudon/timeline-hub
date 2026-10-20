// One layout function feeds the registered draw and the public capability.
// Rectangles are declared layout/support, never inferred glyph or media alpha.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals, useCurrentFrame} from 'remotion';
import {TimelineComposition, prepareCompositionScene, toRuntimeTheme} from '@banodoco/timeline-composition';
import {querySceneFrame, querySceneOcclusion} from '@banodoco/timeline-composition/evaluation';
import {BUNDLED_THEMES} from '@banodoco/timeline-composition/registry.generated';

const {timeline, frames, width = 1920, height = 1080} = JSON.parse(readFileSync(0, 'utf8'));
const layout = (params, frame) => {
  const shift = rect => ({...rect, x: rect.x + (params.dx ?? 0) * frame});
  const known = rect => ({status: 'known', rect: shift(rect)});
  return {
    presence: params.absent ? 'absent' : 'present',
    bounds: params.unknown ? {status: 'unknown', reason: 'undeclared output'} : known(params.rect),
    opaqueSupport: 'rect',
    diagnostics: params.omitDiagnostics ? undefined : {
      motion: {position: frame},
      ...(params.face ? {face: known(params.face)} : {}),
      ...(params.mouth ? {mouth: known(params.mouth)} : {}),
      ...(params.textRect ? {text: {bounds: known(params.textRect), minPx: params.fontPx}} : {}),
    },
  };
};
const Rectangle = ({clip}) => {
  const frame = useCurrentFrame();
  const facts = layout(clip.params, frame);
  if (facts.presence === 'absent') return null;
  const region = (name, rect, text, fontSize) => createElement('div', {
    key: name, 'data-region': `${clip.id}:${name}`, style: {position: 'absolute',
      left: rect.x, top: rect.y, width: rect.width, height: rect.height,
      background: '#123456', boxSizing: 'border-box', ...(text ? {fontSize, overflow: 'hidden'} : {}),
    },
  }, text);
  // Unknown output still draws; it supplies no trustworthy check geometry.
  const output = {...clip.params.rect, x: clip.params.rect.x + (clip.params.dx ?? 0) * frame};
  return createElement('div', {'data-clip': clip.id}, [
    region('output', output),
    ...(facts.diagnostics?.face ? [region('face', facts.diagnostics.face.rect)] : []),
    ...(facts.diagnostics?.mouth ? [region('mouth', facts.diagnostics.mouth.rect)] : []),
    ...(facts.diagnostics?.text ? [region('text', facts.diagnostics.text.bounds.rect, clip.params.text, clip.params.fontPx)] : []),
  ]);
};
const DeclaredRectangle = Object.assign(Rectangle, {
  prepareSceneCapability: ({clip}) => ({identity: JSON.stringify(clip.params),
    frame: frame => layout(clip.params, frame)}),
});
const registries = {effects: Object.fromEntries([
  'am-type', 'am-callout', 'am-sprite', 'am-presenter', 'am-footage', 'test-panel',
].map(name => [name, DeclaredRectangle]))};
const theme = BUNDLED_THEMES['2rp'];
const assets = {assets: {}};
const tracks = [...timeline.tracks].reverse().map(track => ({track,
  clips: timeline.clips.filter(clip => clip.track === track.id)}));
const scene = prepareCompositionScene(tracks, assets, 30, toRuntimeTheme(theme), width, height,
  undefined, undefined, {}, '', {}, registries);
const metadata = {id: 'regions', width, height, fps: 30, durationInFrames: 600,
  defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
  nonce: [], schema: null, calculateMetadata: null, stack: null};
const render = frame => renderToStaticMarkup(createElement(Internals.CompositionManager.Provider, {value: {
  compositions: [metadata], currentCompositionMetadata: null, folders: [],
  canvasContent: {type: 'composition', compositionId: 'regions'},
}}, createElement(Internals.TimelineContext.Provider, {value: {frame: {regions: frame}, playing: false,
  imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
createElement(Internals.CanUseRemotionHooksProvider, null,
  createElement(TimelineComposition, {timeline, assets, theme, registries})))));
const result = {scene_frames: {}, scene_occlusions: {'0.98': {}}, html: {},
  scene_clip_identities: Object.fromEntries(timeline.clips.map(clip => {
    const source = clip.app?.astrid_shot_composition;
    return [clip.id, {clip_id: source?.source_clip_id ?? clip.id,
      occurrence_id: source?.occurrence_id ?? clip.shot_occurrence_id ?? clip.occurrence_id ?? ''}];
  }))};
for (const frame of frames) {
  const row = querySceneFrame(scene, frame);
  result.scene_frames[frame] = row;
  result.scene_occlusions['0.98'][frame] = Object.fromEntries(row.layers.map(layer =>
    [layer.clipId, querySceneOcclusion(row, layer.clipId, .98)]));
  const html = render(frame);
  result.html[frame] = html;
  const px = value => value === 0 ? '0' : `${value}px`;
  for (const layer of row.layers) {
    const clip = timeline.clips.find(clip => clip.id === layer.clipId);
    assert.equal(html.includes(`data-clip="${clip.id}"`), !clip.params.absent);
    if (clip.params.absent) continue;
    for (const [name, region] of Object.entries({output: layer.bounds,
      face: layer.diagnostics?.face, mouth: layer.diagnostics?.mouth, text: layer.diagnostics?.text?.bounds})) {
      if (region?.status !== 'known') continue;
      const {x, y, width: w, height: h} = region.rect;
      assert.ok(html.includes(`data-region="${clip.id}:${name}" style="position:absolute;left:${px(x)};top:${px(y)};width:${px(w)};height:${px(h)}`));
    }
    if (layer.diagnostics?.text?.minPx) assert.ok(html.includes(`font-size:${px(layer.diagnostics.text.minPx)}`));
  }
  for (const clip of timeline.clips) {
    if (!row.layers.some(layer => layer.clipId === clip.id)) assert.ok(!html.includes(`data-clip="${clip.id}"`));
  }
}
console.log(JSON.stringify(result));
