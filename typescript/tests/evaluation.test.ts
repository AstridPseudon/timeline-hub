import assert from 'node:assert/strict';
import {test} from 'node:test';
import {
  applyAudioEnvelope,
  audioEnvelopeAt,
  compileAudioEnvelope,
  prepareTrack,
  queryTrackFrame,
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

// Keep the public result shape exercised as a compile-time contract too.
const _frameShape: TrackFrame = {frame: 0, layers: []};
void _frameShape;
