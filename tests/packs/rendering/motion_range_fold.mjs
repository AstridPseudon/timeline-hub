import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {performance} from 'node:perf_hooks';
import {DEFAULT_THEME, compileCanonicalTransitions, toRuntimeTheme} from '@banodoco/timeline-composition';
import {querySceneFrame} from '@banodoco/timeline-composition/evaluation';
import {foldSceneMotion, loadHostScene} from './native-scene.mjs';

const {mode, invalid} = JSON.parse(readFileSync(0, 'utf8'));
const prepare = await loadHostScene(process.cwd());
const basis = {fps: 30, width: 200, height: 100};
const clip = (id = 'compiled:one', extra = {}) => ({id, track: 'plate',
  clipType: 'range-probe', at: 0, hold: 20, params: {}, ...extra});
const props = clips => ({timeline: {tracks: [{id: 'plate', kind: 'visual'}], clips},
  assets: {assets: {plate: {file: 'plate.png', type: 'image', resolution: '200x100'}}},
  theme: DEFAULT_THEME});
const request = (extra = {}) => ({ranges: [[0, 301]], clipIds: ['compiled:one'],
  keys: ['phase'], maxFrames: 301, ...extra});
globalThis.rangeProbe = {preparations: 0, frames: 0};
const prepared = (clips = [clip()], b = basis, p = props(clips)) => {
  const original = JSON.stringify(p);
  const scene = prepare(p, b, {});
  assert.equal(JSON.stringify(p), original);
  assert.equal(scene.assets, p.assets);
  return scene;
};
const conserve = result => {
  for (const count of result.counts) {
    assert.equal(count.totalFrames, result.totalFrames);
    assert.equal(count.values.reduce((sum, v) => sum + v.count, 0)
      + count.unknownFrames + count.absentFrames, result.totalFrames);
  }
  return result;
};
let output;
if (mode === 'exact') {
  const scene = prepared();
  const frames = [];
  output = conserve(foldSceneMotion(scene, (sameScene, frame) => {
    assert.equal(sameScene, scene);
    frames.push(frame);
    return querySceneFrame(sameScene, frame);
  }, request()));
  assert.deepEqual(frames, Array.from({length: 301}, (_, i) => i));
  assert.equal(globalThis.rangeProbe.preparations, 1);
  assert.equal(globalThis.rangeProbe.frames, 301);
  const oldSamples = Array.from({length: 60}, (_, i) => Math.round(i * 300 / 59));
  assert.ok(!oldSamples.includes(181));
  assert.deepEqual(output.counts[0].values, [{value: 0, count: 300}, {value: 1, count: 1}]);
} else if (mode === 'unknown') {
  const scene = prepared([clip(undefined, {at: 2 / 30, hold: 4 / 30, params: {vary: true}})]);
  output = conserve(foldSceneMotion(scene, querySceneFrame, request({ranges: [[0, 7]],
    maxFrames: 7, keys: ['phase', 'missing']})));
  assert.deepEqual(output.counts.map(c => [c.values, c.unknownFrames, c.absentFrames]), [
    [[{value: 0, count: 1}], 3, 3], [[], 4, 3],
  ]);
} else if (mode === 'invalid-fact') {
  const scene = prepared([clip(undefined, {params: {invalid}})]);
  output = conserve(foldSceneMotion(scene, querySceneFrame, request({ranges: [[0, 2]]})));
  assert.deepEqual(output.counts[0].values, []);
  assert.equal(output.counts[0].unknownFrames, 2);
  assert.equal(output.counts[0].absentFrames, 0);
} else if (mode === 'invisible') {
  const scene = prepared([clip(undefined, {opacity: 0, params: {presence: 'absent'}})]);
  assert.equal(querySceneFrame(scene, 181).layers[0].visible, false);
  output = conserve(foldSceneMotion(scene, querySceneFrame, request()));
  assert.deepEqual(output.counts[0].values, [{value: 0, count: 300}, {value: 1, count: 1}]);
  assert.equal(output.counts[0].absentFrames, 0);
} else if (mode === 'clock') {
  const fps = 30000 / 1001;
  const scene = prepared([clip(undefined, {at: 1 / fps, hold: 8 / fps, speed: 2, from: 7})],
    {...basis, fps});
  output = conserve(foldSceneMotion(scene, querySceneFrame, request({ranges: [[0, 6]], keys: ['clock']})));
  assert.deepEqual(output.counts[0].values, [0, 2, 4, 6].map(value => ({value, count: 1})));
  assert.equal(output.counts[0].absentFrames, 2);
} else if (mode === 'ranges') {
  const clips = [clip('one'), clip('two', {track: 'other', speed: 2})];
  for (const c of clips) c.app = {astrid_shot_composition: {source_clip_id: 'same', occurrence_id: c.id}};
  const p = props(clips);
  p.timeline.tracks.push({id: 'other', kind: 'visual'});
  const scene = prepared(clips, basis, p);
  output = conserve(foldSceneMotion(scene, querySceneFrame, request({
    ranges: [[0, 2], [180, 182]], clipIds: ['two', 'one'], keys: ['phase', 'energy']})));
  assert.equal(output.totalFrames, 4);
  assert.deepEqual(output.counts.map(c => [c.clipId, c.key]), [
    ['two', 'phase'], ['two', 'energy'], ['one', 'phase'], ['one', 'energy'],
  ]);
  assert.deepEqual(output.counts[0].values, [{value: 0, count: 4}]);
  assert.deepEqual(output.counts[2].values, [{value: 0, count: 3}, {value: 1, count: 1}]);
  assert.deepEqual(output.counts[3].values, [{value: -.125, count: 4}]);
} else if (mode === 'preroll') {
  const clips = [clip('out', {hold: 1}), clip('in', {at: 1, hold: 1,
    transition: {type: 'fade', duration: .4}})];
  const p = props(clips);
  const track = p.timeline.tracks[0];
  p.compiledTransitions = compileCanonicalTransitions([{track, clips}], basis.fps, toRuntimeTheme(p.theme));
  const scene = prepared(clips, basis, p);
  output = conserve(foldSceneMotion(scene, querySceneFrame, request({
    ranges: [[21, 27]], clipIds: ['in'], keys: ['clock']})));
  assert.deepEqual(output.counts[0].values, [3, 4, 5, 6, 7, 8].map(value => ({value, count: 1})));
  assert.equal(globalThis.rangeProbe.preparations, 2);
  assert.equal(globalThis.rangeProbe.frames, 12);
} else if (mode === 'invalid-request') {
  const scene = prepared();
  let queries = 0;
  const query = (...args) => { queries++; return querySceneFrame(...args); };
  for (const change of [
    {maxFrames: undefined}, {maxFrames: 0}, {maxFrames: 3601}, {maxFrames: 300},
    {ranges: []}, {ranges: [[0, 0]]}, {ranges: [[2, 1]]}, {ranges: [[-1, 2]]},
    {ranges: [[0, 1.5]]}, {ranges: [[false, 1]]}, {ranges: [[0, 2], [1, 3]]},
    {ranges: [[2, 3], [0, 1]]}, {ranges: [[0, Number.MAX_SAFE_INTEGER + 1]]},
    {ranges: [[0, 1, 2]]}, {ranges: Array.from({length: 65}, (_, i) => [i, i + 1])},
    {clipIds: []}, {clipIds: ['compiled:one', 'compiled:one']}, {clipIds: ['same']},
    {clipIds: ['']}, {keys: []}, {keys: ['phase', 'phase']}, {keys: [1]},
    {keys: Array.from({length: 65}, (_, i) => String(i))},
  ]) assert.throws(() => foldSceneMotion(scene, query, request(change)), /scene_motion_/);
  assert.equal(queries, 0);
  const duplicate = {...scene, tracks: [...scene.tracks, ...scene.tracks]};
  assert.throws(() => foldSceneMotion(duplicate, query, request()), /clip_identity/);
  assert.equal(queries, 0);
  assert.throws(() => foldSceneMotion(scene, (s, f) => {
    const answer = querySceneFrame(s, f);
    answer.layers.push(answer.layers[0]);
    return answer;
  }, request()), /layer_identity/);
  assert.throws(() => foldSceneMotion(scene, (s, f) => ({...querySceneFrame(s, f), frame: f + 1}),
    request()), /frame_invalid/);
  output = {invalidRequestsRefused: true};
} else if (mode === 'cost') {
  const clips = Array.from({length: 8}, (_, i) => clip(String(i), {
    track: String(i), hold: 120, params: {distinct: true}}));
  const p = props(clips);
  p.timeline.tracks = clips.map(c => ({id: c.track, kind: 'visual'}));
  const startPrepare = performance.now();
  const scene = prepared(clips, basis, p);
  const prepareMs = performance.now() - startPrepare;
  const startFold = performance.now();
  output = conserve(foldSceneMotion(scene, querySceneFrame, request({ranges: [[0, 3600]],
    maxFrames: 3600, clipIds: clips.map(c => c.id),
    keys: Array.from({length: 8}, (_, i) => String(i))})));
  const foldMs = performance.now() - startFold;
  assert.equal(globalThis.rangeProbe.preparations, 8);
  assert.equal(globalThis.rangeProbe.frames, 28800);
  output = {totalFrames: output.totalFrames, factPairs: output.counts.length, prepareMs, foldMs,
    bytes: Buffer.byteLength(JSON.stringify(output))};
} else {
  throw new Error(`unknown test mode: ${mode}`);
}
console.log(JSON.stringify(output));
