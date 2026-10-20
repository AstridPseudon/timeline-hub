import { expect, it } from 'vitest';
import { querySceneFrame } from '@banodoco/timeline-composition/evaluation';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST, RUNTIME_TARGETED_EXECUTION_CAPABILITY } from '@/integrations/runtime/contract-metadata.ts';
import { RUNTIME_CLIENT_SCOPES } from '@/integrations/runtime/client.ts';
import { compilePlayerTransitions, preparePlayerClipOpacity, preparePlayerTrack } from '../compositions/playerEvaluation.ts';
import { createShotCompositionAdapter } from './shotCompositionAdapter.ts';
import { resolveCanonicalComposition } from './canonicalCompositionState.ts';
import closure from './mainImageCap.fixture.json';

// Verbatim raw closure from the original MAIN a411628f capture, documented in
// design/viewing-main-image-cap-actual-reference.md (2026-10-20, 11:54 UTC).
// MAIN f90 RGB240, f105 RGB122/124/130 over RGB5/8/20 => median opacity 0.5.
// This exercises source consumers only; it does not render or sample pixels.
it('preserves MAIN image-cap opacity through the canonical projection and public compiler', async () => {
  const original = structuredClone(closure);
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
  const result = resolveCanonicalComposition({ userId: null, hasShotClips: true, hasShotComposition: true,
    composition, compositionError: null, baseConfig: null });
  expect(result.status).toBe('ready');
  const config = result.config!;
  expect(config.output).toMatchObject({ fps: 30, resolution: '1920x1080' });
  expect(config.clips).toHaveLength(1);
  const clip = config.clips[0];
  expect.soft(clip).toMatchObject({ id: 'image-occurrence:image', at: 0, hold: 4, effects: { fade_out: 1 } });
  const compiled = compilePlayerTransitions(config);
  expect(compiled?.tracks).toHaveLength(1);
  const evaluation = preparePlayerTrack(config.tracks[0], config.clips, config.output.fps,
    1920, 1080, undefined, compiled);
  for (const [frame, opacity] of [[90, 1], [105, 0.5]]) {
    expect.soft(querySceneFrame(evaluation.scene, frame).layers).toMatchObject([
      { clipId: clip.id, contentFrame: frame },
    ]);
    expect.soft(preparePlayerClipOpacity(clip, config.output.fps)(frame)).toBe(opacity);
  }
  expect.soft(querySceneFrame(evaluation.scene, 120).layers).toEqual([]);
  expect(closure).toStrictEqual(original);
});
