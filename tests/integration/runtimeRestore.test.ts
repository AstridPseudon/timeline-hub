import { expect, it } from 'vitest';
import { RuntimeDataProvider } from '../../src/integrations/runtime/dataProvider.ts';
import type { CommitAcceptedMutation, Transport } from '../../src/integrations/runtime/generated.ts';
import { DirectHarness } from '../e2e/local/support/harness.ts';
import { ASTRID_PYTHON, AstridCli, revisionSet } from '../e2e/local/support/astrid.ts';

it('M1 App restoreHistory uses the actual head pair and preserves the exact immutable closure through the Runtime door', async () => {
  const harness = new DirectHarness();
  try {
    await harness.start();
    const seed = await harness.seedThreeProducts();
    await harness.enableTimelineAuthoring(ASTRID_PYTHON);
    const astrid = await AstridCli.create(harness);
    const identity = await astrid.preflight();
    console.info('Restore integration source tuple:', revisionSet(identity));
    const projectId = harness.seed.projectId;
    const timelinePath = `/v1/projects/${projectId}/timelines/${seed.timelineId}`;
    const wire: Array<{ method: string; path: string; body: unknown; response: unknown }> = [];
    const transport: Transport = async (method, path, headers, body) => {
      const bytes = body instanceof Blob ? Buffer.from(await body.arrayBuffer()) : body ? Buffer.from(body) : undefined;
      const response = await harness.doorRequest(path, { method, headers, body: bytes });
      wire.push({ method, path, body: bytes ? JSON.parse(bytes.toString('utf8')) : undefined, response: response.json() });
      return { status: response.status, headers: {}, body: new Uint8Array(response.body) };
    };
    const provider = new RuntimeDataProvider({ projectId, baseUrl: harness.doorBase, transport });
    const before = await provider.loadTimelineCommandBasis(seed.timelineId);
    expect(before.head.revisionId).toBe(seed.headRevisionId);
    expect(before.canonicalDocument.shot_revisions).toHaveLength(1);
    expect(before.canonicalDocument.internal_timeline_revisions).toHaveLength(1);
    expect(before.canonicalDocument.parent_revision.payload.config).toMatchObject({ x_f2_opaque: seed.opaque.config });
    expect(before.canonicalDocument.internal_timeline_revisions[0].payload.clips).toEqual(expect.arrayContaining([
      expect.objectContaining({ id: seed.agentClipId, app: { f2Opaque: seed.opaque.clip } }),
    ]));

    const moved = await astrid.commitCaptured(projectId, seed.timelineId,
      { revision_id: before.head.revisionId, publication_id: before.head.publicationId },
      { kind: 'move', clipId: seed.appClipId, on: 5 }, 'restore-intervening-move');
    expect(moved.data.accepted_revision_id).not.toBe(before.head.revisionId);
    const restoreStart = wire.length;
    const result = await provider.shotComposition.restoreHistory!({
      projectId, parentDocumentId: seed.timelineId, revisionId: before.head.revisionId,
    });
    const restoreWire = wire.slice(restoreStart);
    expect(restoreWire.map(({ method, path }) => ({ method, path }))).toEqual([
      { method: 'GET', path: timelinePath },
      { method: 'GET', path: '/v1/health' },
      { method: 'POST', path: `${timelinePath}/composition-revisions/${before.head.revisionId}/restore` },
    ]);
    const [timelineRead, healthPreflight, restorePost] = restoreWire;
    expect(healthPreflight.response).toMatchObject({ status: 'ok' });
    const head = timelineRead.response;
    expect(head).toMatchObject({ project_id: projectId, timeline_id: seed.timelineId,
      head_revision_id: moved.data.accepted_revision_id, head_publication_id: moved.receipt.receipt_id });
    expect(restorePost.body).toEqual({
      expected_head: moved.data.accepted_revision_id, expected_publication_id: moved.receipt.receipt_id,
    });
    const accepted = restorePost.response as CommitAcceptedMutation;
    expect(accepted.data.status).toBe('accepted');
    expect(accepted.data.accepted_revision_id).toBe(before.head.revisionId);
    expect(result).toEqual({ newHead: before.head.revisionId });
    expect(accepted.receipt.receipt_id).toBeTruthy();
    expect(accepted.receipt.receipt_id).not.toBe(before.head.publicationId);
    expect(accepted.receipt.receipt_id).not.toBe(moved.receipt.receipt_id);
    expect(accepted.data.canonical_document).toEqual(before.canonicalDocument);

    // Read every immutable child through the App consumer as well as its restored parent.
    const readback = await new RuntimeDataProvider({ projectId, baseUrl: harness.doorBase, transport })
      .loadTimelineCommandBasis(seed.timelineId);
    expect(readback.head).toEqual({ revisionId: before.head.revisionId, publicationId: accepted.receipt.receipt_id });
    expect(readback.canonicalDocument).toEqual(before.canonicalDocument);
    const entry = readback.history?.items.find((item) => item.publication_id === accepted.receipt.receipt_id);
    expect(entry?.receipt).toEqual(accepted.receipt);
    expect(entry?.revision_id).toBe(before.head.revisionId);
    expect(wire.filter(({ method }) => method === 'POST').map(({ path }) => path)).toEqual([restorePost.path]);
  } finally {
    await harness.stop();
  }
});
