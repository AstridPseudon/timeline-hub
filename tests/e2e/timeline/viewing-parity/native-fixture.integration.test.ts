import assert from 'node:assert/strict';
import { test } from 'node:test';
import { DirectHarness } from '../../local/support/harness';
import {
  nativeFrameParitySetup,
  prepareFrameParityFixture,
  prepareNativeFrameParityRealm,
  readRuntimeJson,
  timelineBase,
} from './fixture';
import { ORIGINAL_640 } from './canvas';

test('native retained frame fixture restores through /v1 with no legacy seed or forged task write', async () => {
  const harness = new DirectHarness();
  try {
    await harness.start({ seed: false, beforeRuntimeStart: async current => {
      await prepareNativeFrameParityRealm(current, ORIGINAL_640);
    }});
    await harness.enableTimelineAuthoring(process.env.ASTRID_PYTHON!);
    const setup = nativeFrameParitySetup(harness);
    const empty = await readRuntimeJson<{ head_revision_id: string; head_publication_id: string }>(harness,
      `${timelineBase({ projectId: setup.projectId, timelineId: setup.timelineId })}`);
    assert.deepEqual({ project_id: empty.project_id, timeline_id: empty.timeline_id,
      head_revision_id: empty.head_revision_id, head_publication_id: empty.head_publication_id },
    { project_id: setup.projectId, timeline_id: setup.timelineId,
      head_revision_id: setup.head.revision_id, head_publication_id: setup.head.publication_id });

    const fixture = await prepareFrameParityFixture(harness, ORIGINAL_640, setup);
    assert.equal(fixture.media.length, 3);
    assert.equal(fixture.sourceVideoMediaId, fixture.media[1].objectId);
    assert.deepEqual(fixture.parent.payload.config, setup.document.parent_revision.payload.config);
    assert.equal(harness.audit().filter(entry => entry.method === 'POST' && entry.path.endsWith('/composition-revisions')).length, 0);

    const objectsBefore = (await readRuntimeJson<{ items: unknown[] }>(harness,
      `/v1/projects/${fixture.projectId}/objects?limit=50`)).items;
    const forged = await harness.runtimeJson('POST', '/v1/tasks', {
      project: fixture.projectId,
      capability_id: 'rendering.render',
      capability_digest: `sha256:${'0'.repeat(64)}`,
      input_object_ids: [],
      spec: {
        authority_context: {
          mode: 'composed_capture', project_id: fixture.projectId, timeline_id: fixture.timelineId,
          revision_id: fixture.headRevisionId,
          capture_snapshot: { config: { clips: [{ id: 'forged', hold: 999 }] }, registry: {} },
        },
        inputs: { filmstrip_authority: '{}' },
      },
    });
    assert.notEqual(forged.status, 201);
    const objectsAfter = (await readRuntimeJson<{ items: unknown[] }>(harness,
      `/v1/projects/${fixture.projectId}/objects?limit=50`)).items;
    assert.deepEqual(objectsAfter, objectsBefore);
    assert.equal(harness.audit().filter(entry => entry.method === 'POST' && entry.path.endsWith('/composition-revisions')).length, 0);
  } finally {
    await harness.stop();
  }
});
