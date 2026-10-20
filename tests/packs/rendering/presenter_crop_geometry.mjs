// Public facts from the ordinary generated host; no renderer or clock mirror.
import assert from 'node:assert/strict';
import {DEFAULT_THEME} from '@banodoco/timeline-composition';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {loadHostScene} from './native-scene.mjs';

const prepare = await loadHostScene(process.cwd());
export const basis = {width: 1920, height: 1080, fps: 30};
export const frames = [0, 3, 4, 5, 15, 29];
export const params = {mouth: {x: 151, y: 104, w: 19}, words: [[.1, .4]],
  chrome: 'none', blinkEvery: 0, seed: 7};
export const propsFor = (p = params, extra = {}) => ({
  timeline: {tracks: [{id: 'overlay', kind: 'visual'}], clips: [{
    id: 'presenter', track: 'overlay', clipType: 'am-presenter', at: 0, hold: 2,
    elementRef: {kind: 'effect', id: 'am-presenter', packId: 'astrid_motion'},
    params: p, ...extra,
  }]}, theme: DEFAULT_THEME, assets: {assets: {}},
});
export const inspect = (props, b = basis, selected = frames) => {
  assert.deepEqual(props.timeline.clips[0].elementRef,
    {kind: 'effect', id: 'am-presenter', packId: 'astrid_motion'});
  const scene = prepare(props, b, {});
  return selected.map(frame => {
    const answer = querySceneFrame(scene, frame);
    assert.equal(answer.layers.length, 1);
    const layer = answer.layers[0];
    assert.equal(layer.clipId, props.timeline.clips[0].id);
    return {frame, mouth: layer.diagnostics.mouth, motion: layer.diagnostics.motion};
  });
};

if (process.argv[2] === 'geometry') {
  const cases = {
    default: {mouth: undefined}, custom: {}, fractional: {mouth: {x: 152.5, y: 103.7, w: 20.6}},
    clamps: {mouth: {x: -20, y: 999, w: 0}},
    zoom: {zoom: 2, focus: {x: 190.4, y: 120.7}},
    focusClamp: {zoom: 99, focus: {x: -100, y: 999}},
    push: {push: {to: 3.5, frames: 28, at: 2}, focus: {x: 191.2, y: 110.4}},
    punch: {zoom: 3, punchAt: [1, 10]}, bob: {bob: 1, seed: 9},
    mosaic: {mosaicIn: {frames: 8}}, outer: {},
  };
  console.log(JSON.stringify([30, 24000 / 1001].flatMap(fps => Object.entries(cases).map(([name, p]) => {
    const props = propsFor({...params, ...p}, name === 'outer' ? {cropLeft: .1} : {});
    return {name, basis: {...basis, fps}, props, rows: inspect(props, {...basis, fps})};
  }))));
}
