import assert from 'node:assert/strict';
import {test} from 'node:test';
import {layerOpacity, ownFrame, overlapWindow, planTrack} from '../src/lib/transition-spans';

test('transition windows use half-open placement and preserve frozen source frames', () => {
  assert.deepEqual(overlapWindow(10, 4, 'end'), {start: 6, end: 10});
  const plans = planTrack(
    [{start: 0, duration: 10}, {start: 10, duration: 10}],
    [{T: 4, kind: 'dissolve', align: 'end'}],
  );

  assert.equal(plans[0].drawStart, 0);
  assert.equal(plans[0].drawDuration, 10);
  assert.equal(plans[1].drawStart, 6);
  assert.equal(plans[1].drawDuration, 14);
  assert.equal(plans[1].ownOffset, 4);
  assert.equal(ownFrame(plans[1], 0), 0);
  assert.equal(ownFrame(plans[1], 3), 0);
  assert.equal(ownFrame(plans[1], 4), 0);
  assert.equal(ownFrame(plans[1], 13), 9);
  assert.equal(ownFrame(plans[1], 20), 9);
  assert.equal(layerOpacity(plans[1], 0), 0);
  assert.equal(layerOpacity(plans[1], 2), .5);
  assert.equal(layerOpacity(plans[1], 4), 1);
});

test('start and center transitions extend draw spans without shifting own spans', () => {
  const start = planTrack(
    [{start: 0, duration: 10}, {start: 10, duration: 10}],
    [{T: 4, kind: 'dip', align: 'start'}],
  );
  assert.equal(start[0].drawDuration, 14);
  assert.equal(start[1].drawStart, 10);
  assert.equal(start[1].ownOffset, 0);
  assert.equal(ownFrame(start[0], 10), 9);
  assert.equal(ownFrame(start[0], 13), 9);

  const center = planTrack(
    [{start: 0, duration: 10}, {start: 10, duration: 10}],
    [{T: 5, kind: 'dip', align: 'center'}],
  );
  assert.deepEqual(overlapWindow(10, 5, 'center'), {start: 8, end: 13});
  assert.equal(center[1].drawStart, 8);
  assert.equal(center[1].drawDuration, 12);
  assert.equal(center[1].ownOffset, 2);
  assert.equal(center[1].fadeIn?.from, 2);
  assert.equal(center[1].fadeIn?.to, 5);
  assert.equal(center[0].fadeOut?.from, 8);
  assert.equal(center[0].fadeOut?.to, 10);
});

test('explicit incoming vectors preserve oversized windows and refuse conflicting or unsafe inputs', () => {
  const spans = [{start: 0, duration: 30}, {start: 30, duration: 30, endCap: 60}];
  const plans = planTrack(spans, [], [null, {T: 60}]);
  assert.deepEqual([plans[1].drawStart, plans[1].drawDuration, plans[1].ownOffset], [0, 60, 30]);
  assert.equal(ownFrame(plans[1], 0), 0);
  assert.equal(ownFrame(plans[1], 59), 29);
  assert.equal(layerOpacity(plans[1], 30), .5);
  assert.throws(() => planTrack(spans, [{T: 12, kind: 'dip', align: 'end'}], [null, {T: 12}]), /transition\/conflicting-policy/);
  assert.throws(() => planTrack(spans, [], [{T: 12}]), /transition\/invalid-vector/);
  for (const T of [0, NaN, Infinity, .5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => planTrack(spans, [], [null, {T}]), /transition\/invalid-duration/);
  }
  assert.throws(() => planTrack([{start: 0, duration: 1}, {start: 1, duration: Number.MAX_SAFE_INTEGER - 1}], [], [null, {T: Number.MAX_SAFE_INTEGER}]), /transition\/invalid-span/);
});
