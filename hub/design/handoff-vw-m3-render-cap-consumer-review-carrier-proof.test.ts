import { expect, it } from 'vitest';
import { RuntimeDataProvider } from './app-source-e6c4aae/src/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from './app-source-e6c4aae/src/integrations/runtime/contract-metadata.ts';
import { RUNTIME_CLIENT_SCOPES } from './app-source-e6c4aae/src/integrations/runtime/client.ts';
import { createShotCompositionAdapter } from './app-source-e6c4aae/src/tools/video-editor/data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from './app-source-e6c4aae/src/tools/video-editor/data/shotCompositionProjection.ts';
import closure from './app-source-e6c4aae/src/tools/video-editor/data/mainImageCap.fixture.json';

// Information-loss probe on the handed-off source. Changing a prepared value
// here is a controlled diagnostic, not a new accepted immutable revision.
it('loses the stored4000/4500 distinction before command preview selection', async () => {
  const parent = closure.parent_revision;
  const prefix = `/v1/projects/${parent.project_id}`;
  const responses: Record<string, unknown> = {
    '/v1/health': { status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      runtime_instance_id: 'main-image-cap-instance', runtime_epoch: 1 },
    '/v1/handshake': { protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      actor_id: 'actor-1', realm_id: 'realm-1', scopes: [...RUNTIME_CLIENT_SCOPES],
      capabilities: [RUNTIME_TARGETED_EXECUTION_CAPABILITY] },
    '/v1/realm': { realm_id: 'realm-1' },
    [`${prefix}/timelines/${parent.timeline_id}/composition-revisions/${parent.revision_id}`]: parent,
    ...Object.fromEntries(closure.shot_revisions.map(shot =>
      [`${prefix}/shots/${shot.shot_id}/revisions/${shot.revision_id}`, shot])),
    ...Object.fromEntries(closure.internal_timeline_revisions.map(internal =>
      [`${prefix}/timelines/${internal.timeline_id}/revisions/${internal.revision_id}`, internal])),
  };
  const provider = new RuntimeDataProvider({ projectId: parent.project_id,
    baseUrl: 'http://main-image-cap.test', token: 'token', transport: async (method, path) => {
      expect(method).toBe(path === '/v1/handshake' ? 'POST' : 'GET');
      expect(responses).toHaveProperty(path);
      return { status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(responses[path])) };
    } });
  const graph = await provider.shotComposition.loadAtHead!({ projectId: parent.project_id,
    parentDocumentId: parent.timeline_id, headRevisionId: parent.revision_id });
  const composition = createShotCompositionAdapter(provider.shotComposition).prepare(graph);
  expect(composition.occurrences).toHaveLength(1);
  expect(composition.occurrences[0].durationMs).toBe(4000);
  const varied = { ...composition, occurrences: composition.occurrences.map(occurrence => ({ ...occurrence, durationMs: 4500 })) };
  const four = projectCanonicalComposition(composition).config;
  const fourAndHalf = projectCanonicalComposition(varied).config;
  expect(four).toStrictEqual(fourAndHalf);
  expect(four.clips).toHaveLength(1);
  expect(four.clips[0]).toMatchObject({ hold: 5, app: { canonicalTiming: { durationMs: 5000, occurrenceDurationMs: 5000 } } });
  expect(Object.keys(four.clips[0].app.canonicalTiming).sort()).toEqual([
    'durationMs', 'gain', 'muted', 'occurrenceDurationMs', 'occurrenceStartMs', 'sourceOffsetMs', 'speed',
  ]);
});
