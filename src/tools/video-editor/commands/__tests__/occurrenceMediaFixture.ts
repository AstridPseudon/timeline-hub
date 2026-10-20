import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import { stableOccurrenceDeepLink, stableOutputIdentity } from '../../data/shotComposition.ts';
import fixture from '../fixtures/recipe_m2_occurrence_media.json';

/** A display graph for the detached native fixture, never Runtime verification. */
export function occurrenceMediaFixtureGraph(raw: CanonicalDocument) {
  const head = { revisionId: raw.parent_revision.revision_id };
  const parent = raw.parent_revision.payload;
  const graph = {
    schema_version: 1,
    project: { project_id: raw.project_id, document_id: raw.timeline_id, role: 'project' },
    primary_timeline: { document_id: raw.timeline_id, role: 'primary_timeline', head: {
      revision_id: head.revisionId, content_digest: raw.parent_revision.content_digest,
    } },
    parent_composition: parent,
    shot_revisions: raw.shot_revisions.map((shot) => {
      const internal = raw.internal_timeline_revisions.find((row) => row.revision_id === shot.internal_timeline_revision_id)!;
      return { ...shot.payload, shot_id: shot.shot_id, revision_id: shot.revision_id, content_digest: shot.content_digest,
        document_role: 'shot_revision', dependencies: [], timing: { duration_ms: 10000 },
        assets: Object.entries(fixture.add.input.internal_timeline_revisions[0].payload.registry.assets).map(([asset_id, asset]) => ({
          ...asset, asset_id, object_id: asset.media_id,
        })),
        internal_timeline_revision: { revision_id: internal.revision_id, content_digest: internal.content_digest, timeline: internal.payload } };
    }),
    occurrences: fixture.add.input.parent_revision.payload.occurrences.map((occurrence, ordinal) => ({
      ...occurrence, parent_document_id: raw.timeline_id, revision_id: occurrence.shot_revision_id, ordinal,
      at_ms: occurrence.placement.start_ms,
      stable_deep_link: stableOccurrenceDeepLink(raw.project_id, raw.timeline_id, occurrence.shot_id, occurrence.shot_revision_id, occurrence.occurrence_id),
      output_identity: stableOutputIdentity(raw.project_id, raw.timeline_id, occurrence.occurrence_id),
    })),
    cases: { missing_dependency: { shot_id: 'missing', revision_id: 'missing', expected: 'missing_dependency' },
      stale_write_rejection: { expected_head_revision_id: head.revisionId, submitted_head_revision_id: head.revisionId, expected_status: 409 } },
  };
  return graph;
}
