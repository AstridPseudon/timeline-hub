// Registered fixture components draw exactly the support they declare. This
// exercises public package exports, without claiming native AM/font parity.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Internals} from 'remotion';
import {TimelineComposition, prepareCompositionScene, toRuntimeTheme} from '@banodoco/timeline-composition';
import {querySceneFrame, querySceneOcclusion} from '@banodoco/timeline-composition/evaluation';
import {BUNDLED_THEMES} from '@banodoco/timeline-composition/registry.generated';

const {timeline, frames} = JSON.parse(readFileSync(0, 'utf8'));
const Rectangle = ({clip}) => {
  const {rect, support = 'rect'} = clip.params;
  return createElement('div', {'data-clip': clip.id, style: {position: 'absolute',
    left: rect.x, top: rect.y, width: rect.width, height: rect.height, boxSizing: 'border-box',
    background: support === 'rect' ? '#123456' : 'transparent',
    border: support === 'rect' ? undefined : '1px solid #123456'}});
};
const DeclaredRectangle = Object.assign(props => createElement(Rectangle, props), {
  prepareSceneCapability: ({clip}) => ({identity: JSON.stringify(clip.params), frame: () => ({
    presence: 'present', bounds: {status: 'known', rect: clip.params.rect},
    opaqueSupport: clip.params.support ?? 'rect',
  })}),
});
const registries = {effects: {'am-type': DeclaredRectangle, 'am-callout': DeclaredRectangle,
  'test-unknown': Rectangle}};
const theme = BUNDLED_THEMES['2rp'];
const assets = {assets: {}};
const tracks = [...timeline.tracks].reverse().map(track => ({track,
  clips: timeline.clips.filter(clip => clip.track === track.id)}));
const scene = prepareCompositionScene(tracks, assets, 30, toRuntimeTheme(theme),
  1920, 1080, undefined, undefined, {}, '', {}, registries);
const metadata = {id: 'cover', width: 1920, height: 1080, fps: 30, durationInFrames: 600,
  defaultProps: {}, folderName: null, parentFolderName: null, component: () => null,
  nonce: [], schema: null, calculateMetadata: null, stack: null};
const render = frame => renderToStaticMarkup(createElement(Internals.CompositionManager.Provider, {value: {
  compositions: [metadata], currentCompositionMetadata: null, folders: [],
  canvasContent: {type: 'composition', compositionId: 'cover'},
}}, createElement(Internals.TimelineContext.Provider, {value: {frame: {cover: frame}, playing: false,
  imperativePlaying: {current: false}, audioAndVideoTags: {current: []}}},
createElement(Internals.CanUseRemotionHooksProvider, null,
  createElement(TimelineComposition, {timeline, assets, theme, registries})))));
const result = {scene_frames: {}, scene_occlusions: {'0.9': {}, '0.98': {}}, html: {},
  scene_clip_identities: Object.fromEntries(timeline.clips.map(clip => {
    const source = clip.app?.astrid_shot_composition;
    return [clip.id, {clip_id: source?.source_clip_id ?? clip.id,
      occurrence_id: source?.occurrence_id ?? clip.shot_occurrence_id ?? clip.occurrence_id ?? ''}];
  }))};
for (const frame of frames) {
  const row = querySceneFrame(scene, frame);
  result.scene_frames[frame] = row;
  for (const threshold of ['0.9', '0.98']) {
    result.scene_occlusions[threshold][frame] = Object.fromEntries(timeline.clips.map(clip =>
      [clip.id, querySceneOcclusion(row, clip.id, Number(threshold))]));
  }
  const html = render(frame);
  result.html[frame] = html;
  // SSR proves the registered drawing and the evaluator use the same layout
  // and half-open mount, including fully occluded layers still being drawn.
  for (const clip of timeline.clips) {
    const mounted = row.layers.some(layer => layer.clipId === clip.id);
    assert.equal(html.includes(`data-clip="${clip.id}"`), mounted);
    if (mounted) {
      const {x, y, width, height} = clip.params.rect;
      const px = value => value === 0 ? '0' : `${value}px`;
      assert.ok(html.includes(`left:${px(x)};top:${px(y)};width:${px(width)};height:${px(height)}`));
    }
  }
}
console.log(JSON.stringify(result));
