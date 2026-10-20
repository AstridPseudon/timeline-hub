import { expect, it } from 'vitest';
import { randomUUID } from 'node:crypto';
import { RuntimeDataProvider } from '../../src/integrations/runtime/dataProvider.ts';
import type { CommitAcceptedMutation, Transport } from '../../src/integrations/runtime/generated.ts';
import { authoringBundleFromDocument } from '../../src/tools/video-editor/commands/authoringBundle.ts';
import { captureClipMove, finishClipMove } from '../../src/tools/video-editor/commands/clipMoveCapture.ts';
import { compositionPublication, DirectHarness } from '../e2e/local/support/harness.ts';
import { ASTRID_PYTHON, AstridCli, revisionSet } from '../e2e/local/support/astrid.ts';

it('M1 refuses an opaque-only parent clip mirror divergence before publication, and native App/Agent moves preserve accepted opaque data', async () => {
  const harness = new DirectHarness();
  try {
    await harness.start();
    const { projectId, timelineId, headRevisionId, image } = harness.seed;
    const timelinePath = `/v1/projects/${projectId}/timelines/${timelineId}`;
    const opaque = { version: 7, nested: [null, { text: 'keep opaque clip data', enabled: false }] };
    const clip = { id: 'mirror-probe', at: 0, track: 'V1', clipType: 'media', asset: 'image',
      from: 0, to: 3, speed: 1, x_mirror_probe: opaque };
    const publication = compositionPublication(harness.seed, headRevisionId, 'Mirror probe', 30);
    Object.assign(publication.parent_composition, {
      clips: [structuredClone(clip)],
      config: { ...publication.parent_composition.config, clips: [structuredClone(clip)] },
      registry: { assets: { image: { file: 'probe.png', type: 'image/png',
        media_id: image.objectId, content_sha256: image.digest } } },
    });
    // Use main's authenticated publication API, before authoring startup installs verified history.
    const seeded = await harness.runtimeJson('POST', `${timelinePath}/composition-revisions`, publication);
    expect(seeded.status, JSON.stringify(seeded.body)).toBe(200);
    const seedRevision = seeded.body.data.new_head;
    const rawPaths = [timelinePath, `${timelinePath}/composition-revisions`,
      `${timelinePath}/composition-revisions/${headRevisionId}`,
      `${timelinePath}/composition-revisions/${seedRevision}`];
    const readRaw = async () => Promise.all(rawPaths.map(async (path) => {
      const response = await harness.doorRequest(path);
      expect(response.status, path).toBe(200);
      return response.body.toString('utf8');
    }));
    const beforeBytes = await readRaw();
    const rawParent = JSON.parse(beforeBytes[3]);
    expect(rawParent.payload.clips).toEqual([clip]);
    expect(rawParent.payload.config.clips).toEqual([clip]);

    const divergent = structuredClone(publication);
    divergent.expected_head = seedRevision;
    divergent.parent_revision_id = randomUUID();
    // Only one opaque field differs; no invalid media, authority, timing or closure pins.
    delete (divergent.parent_composition.clips[0] as Record<string, unknown>).x_mirror_probe;
    expect(divergent.parent_composition.config.clips).toEqual([clip]);
    expect(divergent.parent_composition.clips).toEqual([Object.fromEntries(
      Object.entries(clip).filter(([key]) => key !== 'x_mirror_probe'),
    )]);
    const refused = await harness.runtimeJson('POST', `${timelinePath}/composition-revisions`, divergent);
    expect(refused.status, JSON.stringify(refused.body)).toBe(409);
    expect(refused.body).toMatchObject({ code: 'conflict',
      message: 'canonical parent clips and config.clips disagree',
      details: { reason: 'canonical_payload_mismatch' } });
    expect(await readRaw()).toEqual(beforeBytes);
    expect((await harness.doorRequest(`${timelinePath}/composition-revisions/${divergent.parent_revision_id}`)).status).toBe(404);

    await harness.enableTimelineAuthoring(ASTRID_PYTHON);
    const astrid = await AstridCli.create(harness);
    console.info('Mirror preservation source tuple:', revisionSet(await astrid.preflight()));
    const transport: Transport = async (method, path, headers, body) => {
      const bytes = body instanceof Blob ? Buffer.from(await body.arrayBuffer()) : body ? Buffer.from(body) : undefined;
      const response = await harness.doorRequest(path, { method, headers, body: bytes });
      return { status: response.status, headers: {}, body: new Uint8Array(response.body) };
    };
    const provider = new RuntimeDataProvider({ projectId, baseUrl: harness.doorBase, transport });
    const before = await provider.loadTimelineCommandBasis(timelineId);
    expect(before.head.revisionId).toBe(seedRevision);
    expect(before.canonicalDocument.parent_revision.payload).toEqual(rawParent.payload);
    const bundle = await authoringBundleFromDocument(before.canonicalDocument);
    const app = finishClipMove(captureClipMove(bundle, 'parent/clip:mirror-probe'), 5);
    const native = await astrid.python(['-c', `
import json, sys
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
document = json.loads(sys.argv[1])
bundle = bundle_from_document(document)
command = capture_move(bundle, 'parent/clip:mirror-probe', 5)
plan = execute(bundle, [command])
print(json.dumps(dict(before=bundle, command=command, bundle=plan.bundle, record=plan.records[0])))
`, JSON.stringify(before.canonicalDocument)]);
    const agent = JSON.parse(native.stdout.trim().split('\n').pop()!);
    expect(agent.before).toEqual(bundle);
    expect(agent.command).toEqual(app.command);
    expect(agent.bundle).toEqual(app.bundle);
    expect(agent.record).toEqual(app.record);
    expect(app.bundle.parent).toMatchObject({ clips: [{ ...clip, at: 5 }], config: { clips: [{ ...clip, at: 5 }] } });
    const accepted = await provider.commitTimeline({ api_version: 1, project_id: projectId, timeline_id: timelineId,
      base_revision_id: before.head.revisionId, base_publication_id: before.head.publicationId,
      commands: [app.command], source: { via: 'app' } }, 'mirror-probe-move');
    const readback = await provider.loadTimelineCommandBasis(timelineId);
    expect(readback.head.revisionId).not.toBe(seedRevision);
    expect(readback.canonicalDocument).toEqual(accepted.canonicalDocument);
    expect(readback.canonicalDocument.parent_revision.payload).toMatchObject({
      clips: [{ ...clip, at: 5 }], config: { clips: [{ ...clip, at: 5 }] },
    });
    // The accepted move creates a new immutable image; the original bytes remain readable.
    expect((await harness.doorRequest(`${timelinePath}/composition-revisions/${seedRevision}`)).json().payload)
      .toEqual(rawParent.payload);
  } finally {
    await harness.stop();
  }
});

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
    expect(wire.filter(({ method }) => method === 'POST').map(({ path }) => path)).toEqual([
      '/v1/handshake', restorePost.path, '/v1/handshake',
    ]);
  } finally {
    await harness.stop();
  }
});
