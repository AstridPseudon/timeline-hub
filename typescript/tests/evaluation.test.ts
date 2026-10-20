import assert from 'node:assert/strict';
import {test} from 'node:test';
import {
  applyAudioEnvelope,
  audioEnvelopeAt,
  compileAudioEnvelope,
  computeMediaTrim,
  getSanitizedPlaybackRate,
  prepareTrack,
  declareAppTransition,
  prepareDeclaredTrack,
  queryTrackFrame,
  type TransitionSpec,
  type TrackFrame,
} from '../src/evaluation';
import type {TimelineClip} from '../src/types';

test('track queries use half-open draw bounds and retain mounted zero-opacity layers', () => {
  const track = prepareTrack(
    [{start: 0, duration: 3}, {start: 3, duration: 2}],
    [null],
  );

  const at2 = queryTrackFrame(track, 2);
  const at3 = queryTrackFrame(track, 3);
  const at5 = queryTrackFrame(track, 5);
  assert.deepEqual(at2.layers.map(({clipIndex}) => clipIndex), [0]);
  assert.deepEqual(at3.layers.map(({clipIndex}) => clipIndex), [1]);
  assert.deepEqual(at5.layers, []);

  const transition = prepareTrack(
    [{start: 0, duration: 10}, {start: 10, duration: 10}],
    [{T: 4, kind: 'dissolve', align: 'end'}],
  );
  const at6 = queryTrackFrame(transition, 6);
  const at10 = queryTrackFrame(transition, 10);
  assert.deepEqual(at6.layers.map(({clipIndex}) => clipIndex), [0, 1]);
  assert.equal(at6.layers[1].opacity, 0);
  assert.deepEqual(at10.layers.map(({clipIndex}) => clipIndex), [1]);
  assert.equal(at10.layers[0].opacity, 1);
});

test('audio envelope evaluation accepts representative fade input and applies gain in place', () => {
  const clip: TimelineClip = {
    id: 'audio', at: 0, hold: 1, track: 'music',
    params: {fadeIn: .5, fadeOut: .25},
  };
  const envelope = compileAudioEnvelope(clip, 4);
  assert.ok(envelope);
  assert.equal(audioEnvelopeAt(envelope, 0), 0);
  assert.equal(audioEnvelopeAt(envelope, .25), .5);
  assert.equal(audioEnvelopeAt(envelope, .5), 1);

  const channel = new Float32Array([1, 1, 1]);
  applyAudioEnvelope([channel], 4, envelope);
  assert.deepEqual([...channel].map((value) => Number(value.toFixed(6))), [0, .5, 1]);
});

test('public media clock helpers preserve trim rounding and strict half-open source bounds', () => {
  const occurrenceFixture: TimelineClip & {occurrence: {id: string}} = {
    id: 'occurrence-clip', at: 12.5, hold: 4, speed: 1.5, track: 'audio',
    from: 0.49, to: 1.01, occurrence: {id: 'occurrence-1'},
  };
  assert.deepEqual(computeMediaTrim(occurrenceFixture, 30), {trimBefore: 15, trimAfter: 30});
  assert.equal(getSanitizedPlaybackRate(occurrenceFixture.speed), 1.5);
  assert.deepEqual(computeMediaTrim({from: .5, to: .5}, 30), {trimBefore: 15});
  assert.deepEqual(computeMediaTrim({from: .5, to: .49}, 30), {trimBefore: 15});
});

test('public media clock helpers preserve defaults, invalid-rate fallback and fractional-fps rounding', () => {
  const defaultFixture: TimelineClip = {id: 'default', at: 0, hold: 2, track: 'audio'};
  assert.deepEqual(computeMediaTrim(defaultFixture, 30), {trimBefore: 0});
  assert.deepEqual(computeMediaTrim({from: .5, to: 1.5}, 29.97), {trimBefore: 15, trimAfter: 45});

  for (const invalid of [undefined, 0, -1, Number.NaN, Number.POSITIVE_INFINITY]) {
    assert.equal(getSanitizedPlaybackRate(invalid), 1);
  }
  assert.equal(getSanitizedPlaybackRate(defaultFixture.speed), 1);
  assert.equal(getSanitizedPlaybackRate(.5), .5);
  assert.equal(getSanitizedPlaybackRate(2), 2);
});

// Keep the public result shape exercised as a compile-time contract too.
const _frameShape: TrackFrame = {frame: 0, layers: []};
void _frameShape;

test('incoming preroll policy advances content without changing own frames or half-open mounts', () => {
  const spans = [{start: 60, duration: 30}, {start: 90, duration: 30}];
  for (const kind of ['dip', 'dissolve'] as const) {
    for (const [align, before, start, middle, end, atBoundary, last] of [
      ['end', 77, 78, 84, 90, 12, 41],
      ['center', 83, 84, 90, 96, 6, 35],
      ['start', 89, 90, 96, 102, 0, 29],
    ] as const) {
      const spec = {T: 12, kind, align, incomingPolicy: 'preroll-crossfade'} as const;
      const track = prepareTrack(spans, [spec]);
      assert.deepEqual(queryTrackFrame(track, before).layers.map(layer => layer.clipIndex), [0]);
      const first = queryTrackFrame(track, start).layers;
      assert.equal(first[1].contentFrame, 0);
      assert.equal(first[1].opacity, 0);
      const mid = queryTrackFrame(track, middle).layers;
      assert.deepEqual(mid.map(layer => layer.opacity), [1, .5]);
      assert.equal(mid[1].contentFrame, 6);
      const boundary = queryTrackFrame(track, 90).layers.find(layer => layer.clipIndex === 1)!;
      assert.equal(boundary.ownFrame, 0);
      assert.equal(boundary.contentFrame, atBoundary);
      assert.deepEqual(queryTrackFrame(track, end).layers.map(layer => layer.clipIndex), [1]);
      assert.equal(queryTrackFrame(track, end).layers[0].opacity, 1);
      assert.equal(queryTrackFrame(track, 119).layers[0].contentFrame, last);
      assert.deepEqual(queryTrackFrame(track, 120).layers, []);
      const legacy = prepareTrack(spans, [{T: 12, kind, align}]);
      assert.deepEqual(queryTrackFrame(legacy, middle).layers.map(layer => layer.opacity), kind === 'dip' ? [0, 0] : [1, .5]);
      assert.equal(queryTrackFrame(legacy, 90).layers.find(layer => layer.clipIndex === 1)!.contentFrame, 0);
    }
  }
});

test('policy is per boundary, preserves cut admission, and composes overlapping transition windows', () => {
  const spans = [{start: 0, duration: 30}, {start: 30, duration: 12}, {start: 42, duration: 30}];
  const incoming: TransitionSpec = {T: 12, kind: 'dip', align: 'start', incomingPolicy: 'preroll-crossfade'};
  const outgoing: TransitionSpec = {T: 12, kind: 'dip', align: 'end'};
  const mixed = prepareTrack(spans, [incoming, outgoing]);
  assert.deepEqual(queryTrackFrame(mixed, 36).layers.map(layer => [layer.contentFrame, layer.opacity]), [[29, 1], [6, 0], [0, 0]]);
  const both = prepareTrack(spans, [incoming, {...outgoing, incomingPolicy: 'preroll-crossfade'}]);
  assert.deepEqual(queryTrackFrame(both, 36).layers.map(layer => [layer.contentFrame, layer.opacity]), [[29, 1], [6, .5], [6, .5]]);
  assert.deepEqual(queryTrackFrame(both, 42).layers.map(layer => [layer.clipIndex, layer.contentFrame]), [[2, 12]]);
  for (const start of [28, 31]) { // unsupported overlap or gap remains a cut
    const cut = prepareTrack([{start: 0, duration: 30}, {start, duration: 30}], [incoming]);
    assert.equal(cut.plans[1].drawStart, start);
    assert.equal(cut.plans[1].incomingPolicy, undefined);
  }
  const oversized = prepareTrack(spans, [{...incoming, T: 13}]);
  assert.equal(oversized.plans[1].incomingPolicy, undefined);
  const adjacent = prepareTrack([{start: 0, duration: 30}, {start: 29, duration: 30}], [{...incoming, align: 'end'}]);
  assert.equal(queryTrackFrame(adjacent, 24).layers[1].contentFrame, 6);
});

test('App admission carries only explicit policy and still refuses unsupported custom transitions and overlap', () => {
  const clips = [{id: 'a', start: 60, duration: 30}, {id: 'b', start: 90, duration: 30}];
  for (const type of ['fade', 'crossfade', 'cross-fade']) {
    const input = Object.freeze({type, duration: .4, incomingPolicy: 'preroll-crossfade' as const});
    const declaration = declareAppTransition('visual', 'a', input, 30, 'timeline-composition');
    const layer = queryTrackFrame(prepareDeclaredTrack('visual', clips, [declaration], 'timeline-composition'), 84).layers[1];
    assert.deepEqual([layer.ownFrame, layer.contentFrame, layer.opacity], [0, 6, .5]);
    assert.throws(() => prepareDeclaredTrack('visual', [clips[0], {...clips[1], start: 89}], [declaration], 'timeline-composition'), /overlap/);
  }
  assert.throws(() => declareAppTransition('visual', 'a', {type: 'custom', duration: .4,
    incomingPolicy: 'preroll-crossfade'}, 30, 'timeline-composition'), /No admitted contribution/);
  assert.throws(() => prepareTrack(clips, [{T: 12, kind: 'dip', align: 'end',
    incomingPolicy: 'unknown' as never}]), /Unsupported incoming transition policy/);
});

test('public incoming vector represents first clips and leaves audio envelope gain unchanged', () => {
  const clip: TimelineClip = {id: 'first', at: 2, hold: 1, track: 'v', volume: .4, params: {fadeIn: .5}};
  const before = JSON.stringify(clip);
  const envelope = compileAudioEnvelope(clip, 30);
  const track = prepareTrack([{start: 60, duration: 30}], [], [{T: 12}]);
  assert.deepEqual(queryTrackFrame(track, 59).layers, []);
  assert.deepEqual(queryTrackFrame(track, 66).layers.map(layer => [layer.ownFrame, layer.contentFrame, layer.opacity]), [[6, 6, .5]]);
  assert.deepEqual(queryTrackFrame(track, 90).layers, []);
  assert.deepEqual(compileAudioEnvelope(clip, 30), envelope);
  assert.equal(JSON.stringify(clip), before);
});

test('native outgoing pairs cannot encode canonical first, gap, overlap or oversized incoming declarations', () => {
  const spec = {T: 12, kind: 'dissolve', align: 'end', incomingPolicy: 'preroll-crossfade'} as const;
  const first = prepareTrack([{start: 60, duration: 30}], [spec]);
  assert.equal(queryTrackFrame(first, 66).layers[0].opacity, 1);
  assert.equal(queryTrackFrame(prepareTrack([{start: 60, duration: 30}], [], [{T: 12}]), 66).layers[0].opacity, .5);
  for (const [S, T, midpoint] of [[60, 12, 54], [15, 12, 9], [30, 60, 30]]) {
    const spans = [{start: 0, duration: 30}, {start: S, duration: 30}];
    const native = prepareTrack(spans, [{...spec, T}]);
    const canonical = prepareTrack(spans, [], [null, {T}]);
    assert.notEqual(queryTrackFrame(native, midpoint).layers.find(layer => layer.clipIndex === 1)?.opacity, .5);
    assert.equal(queryTrackFrame(canonical, midpoint).layers.find(layer => layer.clipIndex === 1)!.opacity, .5);
  }
});
