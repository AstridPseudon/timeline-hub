import { expect, it, vi } from 'vitest';
import { RuntimeDataProvider } from '@/integrations/runtime/dataProvider.ts';
import { RUNTIME_SCHEMA_DIGEST } from '@/integrations/runtime/contract-metadata.ts';
import type { CanonicalDocument, Transport } from '@/integrations/runtime/generated.ts';
import { createShotCompositionAdapter } from '../data/shotCompositionAdapter.ts';
import { projectCanonicalComposition } from '../data/shotCompositionProjection.ts';
import { buildTimelineData } from '../lib/timeline-data.ts';
import type { AssetRegistry, TimelineConfig, ResolvedTimelineClip } from '../types/index.ts';
import { authoringBundleFromDocument } from './authoringBundle.ts';
import { captureOccurrenceAddMedia } from './occurrenceMediaCapture.ts';
import { OccurrenceMediaState } from './occurrenceMediaPrimitives.ts';
import { occurrenceMediaPreview, projectOccurrenceMediaPreview } from './occurrenceMediaGesture.ts';
import fixture from './fixtures/recipe_m2_occurrence_media.json';

// Raw immutable images through the product graph adapter; no acceptance envelope or publication pins.
async function graphFor(document: CanonicalDocument) {
  const requests: string[] = [];
  const json = (value: unknown) => ({ status: 200, headers: {}, body: new TextEncoder().encode(JSON.stringify(value)) });
  const prefix = `/v1/projects/${document.project_id}`;
  const transport: Transport = async (method, path) => {
    requests.push(`${method} ${path}`);
    if (path === '/v1/health') return json({ status: 'ok', protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      runtime_epoch: 1, runtime_instance_id: 'instance-1' });
    if (path === '/v1/handshake') return json({ protocol: 'workspace.v1', schema_digest: RUNTIME_SCHEMA_DIGEST,
      session_id: 'session-1', actor_id: 'actor-1', realm_id: 'realm-1',
      scopes: ['handshake', 'projects:read', 'projects:write', 'objects:read', 'objects:write', 'tasks:read', 'tasks:write'],
      capabilities: ['execution_binding.targeted.v1'] });
    if (path === '/v1/realm') return json({ realm_id: 'realm-1', display_name: 'fixture', version: 1, created_at: '2026-10-19T00:00:00Z' });
    if (method === 'GET' && path === `${prefix}/timelines/${document.timeline_id}/composition-revisions/${document.parent_revision.revision_id}`) {
      return json({ project_id: document.project_id, timeline_id: document.timeline_id, ...document.parent_revision });
    }
    for (const shot of document.shot_revisions) {
      if (method === 'GET' && path === `${prefix}/shots/${shot.shot_id}/revisions/${shot.revision_id}`) {
        const internal = document.internal_timeline_revisions.find((row) => row.revision_id === shot.internal_timeline_revision_id)!;
        return json({ project_id: document.project_id, timeline_id: internal.timeline_id, ...shot });
      }
    }
    for (const internal of document.internal_timeline_revisions) {
      if (method === 'GET' && path === `${prefix}/timelines/${internal.timeline_id}/revisions/${internal.revision_id}`) {
        return json({ project_id: document.project_id, ...internal });
      }
    }
    throw new Error(`Unexpected request ${method} ${path}`);
  };
  const provider = new RuntimeDataProvider({ projectId: document.project_id, baseUrl: 'http://runtime.test', token: 'fixture', transport });
  const snapshots = vi.spyOn(provider, 'saveTimeline');
  const graph = await provider.shotComposition.loadAtHead!({ projectId: document.project_id,
    parentDocumentId: document.timeline_id, headRevisionId: document.parent_revision.revision_id });
  return { provider, graph: graph as Record<string, unknown>, requests, snapshots };
}

function vectors(clips: ResolvedTimelineClip[]) {
  return clips.map(({ id, at, from, to, hold, speed, asset, assetEntry, app }) => ({ id, at, from, to, hold, speed, asset,
    mediaId: assetEntry?.media_id, canonicalTiming: app?.canonicalTiming }));
}

it('keeps the native ADD authored window and projects the same after-document consistently', async () => {
  const input: CanonicalDocument = { ...structuredClone(fixture.add.input), schema_version: 1 };
  const output: CanonicalDocument = { ...structuredClone(fixture.add.output), schema_version: 1 };
  const before = structuredClone({ input, output });
  const base = await graphFor(input), after = await graphFor(output);
  const original = await authoringBundleFromDocument(input), reopened = await authoringBundleFromDocument(output);
  const args = fixture.add.commands[0].args;
  const result = captureOccurrenceAddMedia(original, 'occurrence:occ-a', args.row, args.media, fixture.add.verified_media);
  expect([result.command]).toEqual(fixture.add.commands);
  expect([result.record]).toEqual(fixture.add.records);
  for (const placement of result.bundle.placements) {
    const acceptedPlacement = reopened.placements.find((row) => row.occurrence_id === placement.occurrence_id)!;
    expect(result.bundle.shots[String(placement.shot_id)].internal_timeline)
      .toEqual(reopened.shots[String(acceptedPlacement.shot_id)].internal_timeline);
  }
  const rawRow = new OccurrenceMediaState(reopened).entity('occurrence:occ-a/clip:reserved-child');
  expect(rawRow).toEqual(args.row); // Includes null, opaque, hold, raw local start and the full [2,6) window.
  const parent = input.parent_revision.payload;
  const seed = await buildTimelineData({ ...parent.config as TimelineConfig, clips: parent.clips as TimelineConfig['clips'] },
    parent.registry as AssetRegistry, undefined, 1, undefined, { projectId: input.project_id, timelineId: input.timeline_id,
      headRevisionId: input.parent_revision.revision_id });
  const local = projectOccurrenceMediaPreview(occurrenceMediaPreview(result.bundle, base.graph), seed, base.provider.shotComposition)!;
  const reopenedSeed = { ...seed, head: { ...seed.head!, headRevisionId: output.parent_revision.revision_id } };
  const sameDocumentLocal = projectOccurrenceMediaPreview(occurrenceMediaPreview(reopened, after.graph), reopenedSeed, after.provider.shotComposition)!;
  expect(vectors(sameDocumentLocal.config.clips)).toEqual(vectors(local.config.clips));
  const prepared = createShotCompositionAdapter(after.provider.shotComposition).prepare(after.graph);
  // The accepted hook uses precisely this default projection. The fixture itself has no publication receipt.
  const acceptedConfig = projectCanonicalComposition(prepared).config;
  const accepted = await buildTimelineData(acceptedConfig, { assets: acceptedConfig.registry }, undefined, 2, undefined, reopenedSeed.head);
  expect(local.head?.headRevisionId).toBe(input.parent_revision.revision_id);
  expect(accepted.head?.headRevisionId).toBe(output.parent_revision.revision_id);
  expect(local.head?.headPublicationId).toBeUndefined();
  expect(accepted.head?.headPublicationId).toBeUndefined();
  expect(after.graph).not.toHaveProperty('accepted_identity');
  expect(base.snapshots).not.toHaveBeenCalled();
  expect(after.snapshots).not.toHaveBeenCalled();
  for (const env of [base, after]) {
    expect(env.requests.filter((request) => !request.startsWith('GET ') && request !== 'POST /v1/handshake')).toEqual([]);
  }
  expect({ input, output }).toEqual(before);
  expect(new OccurrenceMediaState(reopened).entity('occurrence:occ-a/clip:reserved-child')).toEqual(args.row);
  console.info('same-document vectors', JSON.stringify({ local: vectors(local.resolvedConfig.clips), accepted: vectors(accepted.resolvedConfig.clips) }));
  expect.soft(vectors(accepted.config.clips)).toEqual(vectors(sameDocumentLocal.config.clips));
  expect.soft(vectors(accepted.resolvedConfig.clips)).toEqual(vectors(sameDocumentLocal.resolvedConfig.clips));
});
