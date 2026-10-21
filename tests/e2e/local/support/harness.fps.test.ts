import assert from 'node:assert/strict';
import { test } from 'node:test';
import { compositionPublication } from './harness.ts';

test('split seed uses numeric Runtime fps while reproducing the rejected rational object call', () => {
  const normal = compositionPublication({ projectId: 'project', timelineId: 'timeline' }, null, 'Native parent split', 30000 / 1001);
  const bad = compositionPublication({ projectId: 'project', timelineId: 'timeline' }, null, 'Native parent split', {
    numerator: 30000, denominator: 1001,
  } as unknown as number);

  assert.equal(normal.parent_composition.config.output.fps, 30000 / 1001);
  assert.equal(typeof normal.parent_composition.config.output.fps, 'number');
  assert.equal(Number.isFinite(normal.parent_composition.config.output.fps), true);
  assert.deepEqual(bad.parent_composition.config.output.fps, { numerator: 30000, denominator: 1001 });
  assert.equal(Number.isFinite(bad.parent_composition.config.output.fps), false);
});
