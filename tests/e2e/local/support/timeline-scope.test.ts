import assert from 'node:assert/strict';
import test from 'node:test';
import { timelineBase } from './timeline-scope.ts';

test('timeline paths keep seeded and created-project scopes explicit', () => {
  assert.equal(timelineBase({ projectId: 'seeded-project', timelineId: 'seeded-timeline' }),
    '/v1/projects/seeded-project/timelines/seeded-timeline');
  assert.equal(timelineBase({ projectId: 'created-project', timelineId: 'created-timeline' }),
    '/v1/projects/created-project/timelines/created-timeline');
});
