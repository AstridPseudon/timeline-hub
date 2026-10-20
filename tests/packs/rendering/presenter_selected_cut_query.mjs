// Read-only query of the exact retained four-still Root. No capture or SSR.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {basis, prepareRoot, propsFor, seriesInspection} from './presenter_crop_geometry.mjs';
import {source} from './query.mjs';

const retained = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
assert.deepEqual(retained.frames, [0, 3, 4, 5]);
assert.deepEqual(retained.basis, basis);
// The retained explicit public10 theme stays exact when querying public13.
assert.equal(createHash('sha256').update(fs.readFileSync(process.argv[2])).digest('hex'),
  'eabcc179baa4b97b6bdf1c8343ca270ef090e1306ab8791ee32787c3226385af');
assert.deepEqual(retained.props.timeline, propsFor().timeline);
assert.deepEqual(retained.props.assets, propsFor().assets);
const original = JSON.stringify(retained);
const scene = prepareRoot(retained.props, retained.basis, {});
// seriesInspection resolves this exact compiled ID and registered owner,
// checks the DrawPlan's component zero, then makes its one public ROI query.
const zero = seriesInspection(scene, retained.props);
const answers = retained.frames.map(frame => querySceneFrame(scene, frame));

// The selected-cut consumer asks the ordinary public evaluator for exactly
// the selected keys. The registered presenter owns the state codebook and
// motion rows; this test does not mirror its clock, hash, geometry, or math.
const selectedCutAggregate = (props, selected, expectedFrames,
  codebook = source.MOUTH_LEVEL) => {
  assert.deepEqual(selected, expectedFrames);
  const target = props.timeline.clips.find(clip => clip.id === 'presenter');
  assert.ok(target);
  assert.deepEqual(target.elementRef,
    {kind: 'effect', id: 'am-presenter', packId: 'astrid_motion'});
  const targetInScene = scene.tracks.flatMap(track => track.clips)
    .find(clip => clip.id === target.id);
  assert.deepEqual(targetInScene, target);
  assert.deepEqual(codebook, source.MOUTH_LEVEL);
  const rows = selected.map(frame => {
    const answer = querySceneFrame(scene, frame);
    const layers = answer.layers.filter(layer => layer.clipId === target.id);
    assert.equal(layers.length, 1);
    const layer = layers[0];
    assert.equal(layer.contentFrame, frame);
    const state = source.mouthStateAt(
      source.presenterAt(target.params, layer.contentFrame, retained.basis.fps).timing,
      layer.contentFrame);
    assert.equal(layer.diagnostics.motion.mouth, codebook[state]);
    assert.deepEqual(layer.diagnostics.motion,
      source.motionAt(target.params, layer.contentFrame, retained.basis.fps));
    return {frame, state, motion: layer.diagnostics.motion, mouth: layer.diagnostics.mouth};
  });
  return {frames: selected, rows, states: rows.map(row => row.state)};
};

const aggregate = selectedCutAggregate(retained.props, retained.frames, retained.frames);
const aggregateControls = [];
assert.throws(() => selectedCutAggregate(
  {...retained.props, timeline: {...retained.props.timeline,
    clips: [{...retained.props.timeline.clips[0],
      params: {...retained.props.timeline.clips[0].params, seed: 9}}]}},
  retained.frames, retained.frames));
aggregateControls.push('changed-state');
assert.throws(() => selectedCutAggregate(retained.props, retained.frames, retained.frames,
  {closed: 0, half: 0.25, open: 1}));
aggregateControls.push('changed-codebook');
assert.throws(() => selectedCutAggregate(retained.props, [0, 3, 5], retained.frames));
aggregateControls.push('omitted-selection');

const {erase, ...expected} = retained.rows[0];
// inspection.json is the capture's JSON boundary, which serializes -0 as 0.
// Match that same boundary; no geometry, pixel or threshold is normalized.
assert.deepEqual(JSON.parse(JSON.stringify(zero)), expected);

// Invalid selections refuse before the helper reaches querySceneFrame.
const controls = [];
const refuse = (name, props, id) => {
  assert.throws(() => seriesInspection(scene, props, id));
  controls.push(name);
};
refuse('missing-compiled-id', retained.props, 'missing');
refuse('ambiguous-compiled-id', {...retained.props, timeline: {...retained.props.timeline,
  clips: [...retained.props.timeline.clips, retained.props.timeline.clips[0]]}});
const changed = patch => ({...retained.props, timeline: {...retained.props.timeline,
  clips: [{...retained.props.timeline.clips[0], ...patch}]}});
refuse('foreign-owner', changed({elementRef: {kind: 'effect', id: 'am-presenter', packId: 'probe'}}));
refuse('stale-params', changed({params: {...retained.props.timeline.clips[0].params, seed: 9}}));
assert.equal(JSON.stringify(retained), original);
console.log(JSON.stringify({zero, answers, aggregate, aggregateControls, controls}));
