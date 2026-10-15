import {test} from 'node:test';
import assert from 'node:assert/strict';
import {evaluationMetadata} from '../src/Evaluation';
import {prepareCompositionScene, DEFAULT_THEME, toRuntimeTheme} from '@banodoco/timeline-composition';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';

const track = {id: 'plate', kind: 'visual' as const, label: 'Picture', fit: 'cover' as const};
const clip = {id: 'p', track: 'plate', asset: 'a', at: 0, hold: 2, effects: {fade_in: .5}, opacity: .8};
const assets = {assets: {a: {file: 'a.jpg', type: 'image/jpeg', resolution: '200x100'}}};
const scene = {timeline: {theme: 'banodoco-default', tracks: [track], clips: [clip]}, assets, fps: 10,
  width: 200, height: 100, roles: {p: 'picture'}};

test('native metadata and Composition use the exact same preparation/frame answers', () => {
  const frames = [0, 3, 19, 20];
  const result = evaluationMetadata({props: {scene, frames}}).props.evaluation;
  const prepared = prepareCompositionScene([{track, clips: [clip]}], assets, 10, toRuntimeTheme(DEFAULT_THEME), 200, 100);
  assert.deepEqual(result, frames.map(frame => querySceneFrame(prepared, frame)));
  assert.equal(result[1].layers[0].opacity, .48);

});

test('metadata admission preserves the legacy planner and rejects invalid requested frames', () => {
  const legacy = evaluationMetadata({props: {spans: [{start: 0, duration: 5}], transitions: [], frames: [0, 5]}}).props.evaluation;
  assert.equal(legacy[0].layers.length, 1);
  assert.equal(legacy[1].layers.length, 0);
  assert.throws(() => evaluationMetadata({props: {scene, frames: [NaN]}}), /evaluation_inputs_invalid/);
});
