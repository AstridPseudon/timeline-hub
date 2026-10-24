import assert from 'node:assert/strict';
import test from 'node:test';
import { originalPageOwnerReady } from './p2-original-owner-ready.ts';

const previousOwnerIds = new Set(['old-owner']);
const settled = [{ ownerId: 'new-owner', intents: [] }];
const base = { connected: true, projectSelected: true, trackVisible: true, owners: settled, previousOwnerIds, projectId: 'project', timelineId: 'timeline' };

test('original-page readiness requires all original guards and a fresh settled owner', () => {
  assert.equal(originalPageOwnerReady(base), true);
  for (const key of ['connected', 'projectSelected', 'trackVisible']) {
    assert.equal(originalPageOwnerReady({ ...base, [key]: false }), false);
  }
  assert.equal(originalPageOwnerReady({ ...base, owners: [{ ownerId: 'old-owner', intents: [] }] }), false);
  assert.equal(originalPageOwnerReady({ ...base, owners: [{ ownerId: 'new-owner', pending: {}, intents: [] }] }), false);
  assert.equal(originalPageOwnerReady({ ...base, owners: [{ ownerId: 'new-owner', intents: ['gesture'] }] }), false);
  assert.equal(originalPageOwnerReady({ ...base, owners: [{ ownerId: 'foreign-owner', scope: { projectId: 'other', timelineId: 'timeline' }, intents: [] }] }), false);
});
