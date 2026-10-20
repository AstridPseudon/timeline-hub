// ORCH-only experiment with immutable public10. No renderer, presenter math,
// source adoption, geometry claim, or product adapter is exercised here.
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {prepareScene, queryDrawFrame, querySceneFrame} from './package/dist/evaluation.js';

const fixture = ({fps = 30, speed = 1, incoming = true, endCap} = {}) => {
  const called = [];
  const clips = [
    {id: 'out', track: 'visual', clipType: 'effect-layer', at: 0, hold: 1},
    {id: 'in', track: 'visual', clipType: 'clock-probe', at: 1, hold: 2, speed,
      from: 17, params: {}, ...(endCap === undefined ? {} : {app: {canonicalTiming: {
        occurrenceStartMs: 0, occurrenceDurationMs: endCap}}})},
  ];
  const T = Math.round(.4 * fps);
  const track = {track: {id: 'visual', kind: 'visual'}, clips,
    transitions: incoming ? [null, null] : [{T, kind: 'dissolve', align: 'end'}, null],
    ...(incoming ? {incomingTransitions: [null, {T}]} : {})};
  const scene = prepareScene([track], {assets: {}}, fps, 1920, 1080, {capabilities: {
    components: {in: {identity: 'ORCH clock-only probe', frame: componentFrame => {
      called.push(componentFrame);
      return {presence: 'unknown', opaqueSupport: 'none',
        bounds: {status: 'known', rect: {x: 0, y: 0, width: 1920, height: 1080}},
        diagnostics: {motion: {observedFrame: componentFrame}}};
    }}},
  }});
  return {scene, called, plan: scene.tracks[0].prepared.plans[1]};
};

for (const fps of [30, 24000 / 1001]) {
  test(`incoming preroll: plan queries select zero, one scene query supplies component zero (${fps})`, () => {
    for (const speed of [.5, 1, 2]) {
      const {scene, plan, called} = fixture({fps, speed});
      assert.ok(plan.drawStart < Math.round(fps));
      assert.equal(queryDrawFrame(plan, 0).contentFrame, 0);
      assert.ok(queryDrawFrame(plan, Math.round(fps) - plan.drawStart).contentFrame > 0);
      assert.equal(called.length, 0); // Clock inspection evaluates no component.
      const answer = querySceneFrame(scene, plan.drawStart);
      const layer = answer.layers.find(row => row.clipId === 'in');
      assert.equal(layer.clipIndex, 1);
      assert.equal(layer.contentFrame, 0);
      assert.equal(layer.diagnostics.motion.observedFrame, 0);
      assert.deepEqual(called, [0]); // One component-zero read on this same root.
      const fixed = layer.diagnostics;
      for (const _sample of [0, 3, 4, 5]) assert.equal(fixed, layer.diagnostics);
      assert.deepEqual(called, [0]); // Holding the result adds no scene query.
    }
  });
}

test('native pad repeats zero through own start; authored-at is not a universal clock', () => {
  for (const incoming of [false, true]) {
    const {plan} = fixture({incoming});
    assert.equal(plan.drawStart, 18);
    assert.equal(plan.ownOffset, 12);
    assert.equal(queryDrawFrame(plan, 0).contentFrame, 0);
    assert.equal(queryDrawFrame(plan, plan.ownOffset).contentFrame, incoming ? 12 : 0);
  }
});

test('draw end is half-open even though queryDrawFrame itself does not filter mounting', () => {
  const {scene, plan, called} = fixture();
  const end = plan.drawStart + plan.drawDuration;
  assert.equal(querySceneFrame(scene, end).layers.some(row => row.clipId === 'in'), false);
  assert.deepEqual(called, []);
  assert.ok(queryDrawFrame(plan, plan.drawDuration).contentFrame > 0);
});

test('occurrence cap may leave no mounted zero: unknown rather than a synthesized callback', () => {
  const {scene, plan, called} = fixture({endCap: 0});
  assert.equal(plan.drawDuration, 0);
  assert.equal(queryDrawFrame(plan, 0).contentFrame, 0);
  assert.equal(querySceneFrame(scene, plan.drawStart).layers.some(row => row.clipId === 'in'), false);
  assert.deepEqual(called, []);
});
