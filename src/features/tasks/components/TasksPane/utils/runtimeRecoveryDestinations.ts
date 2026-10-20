import type { AstridRuntimeClient } from '@/integrations/runtime/client';
import type { RuntimeDataProvider } from '@/integrations/runtime/dataProvider';
import type { ManagedOutput, MediaSelection, Task } from '@/integrations/runtime/generated';
import type { TimelineCommandBasis } from '@/tools/video-editor/data/DataProvider';
import { asRecord } from '@/shared/lib/typeCoercion';
import { isRuntimeRecoveryOutput, readRuntimeRecoverySelection, runtimeTaskRecoveryPresentation } from './runtimeTaskRecovery';

export interface RuntimeRecoverySource {
  task: Task;
  output: ManagedOutput;
  mediaTuple: MediaSelection;
}

export interface RuntimeRecoveryDestination {
  id: string;
  name: string;
  owner: { kind: 'occurrence'; occurrenceId: string };
  shotId: string;
  shotRevisionId: string;
  internalTimelineId: string;
  internalRevisionId: string;
  parentTrackId: string;
  childTrackId: string;
}

export interface RuntimeRecoveryDestinations {
  basis: TimelineCommandBasis;
  bindings: RuntimeRecoveryDestination[];
}

/** Local routing data for a later qualified native command port, never a wire DTO. */
export interface RuntimeRecoveryPlacementDraft {
  projectId: string;
  timelineId: string;
  basis: TimelineCommandBasis;
  source: RuntimeRecoverySource;
  destination: RuntimeRecoveryDestination;
  on: number;
  sourceWindow: { from: number; to: number };
}

export function freezeRecoveryValue<T>(value: T): T {
  if (value && typeof value === 'object') {
    Object.values(value).forEach(freezeRecoveryValue);
    Object.freeze(value);
  }
  return value;
}

function identity(value: unknown): string {
  if (typeof value !== 'string' || !value.trim()) throw new Error('Missing destination identity');
  return value;
}

function tracks(value: unknown): Record<string, unknown>[] {
  if (!Array.isArray(value)) throw new Error('Missing explicit destination tracks');
  const rows = value.map((row) => {
    const record = asRecord(row);
    if (!record) throw new Error('Invalid destination track');
    identity(record.id);
    return record;
  });
  if (new Set(rows.map((row) => row.id)).size !== rows.length) throw new Error('Ambiguous destination tracks');
  return rows;
}

/** Uses only the existing provider's verified closure and a matching current head. */
export async function loadRuntimeRecoveryDestinations(
  provider: Pick<RuntimeDataProvider, 'loadTimelineCommandBasis'>,
  client: Pick<AstridRuntimeClient, 'getProjectTimeline'>,
  projectId: string,
  timelineId: string,
): Promise<RuntimeRecoveryDestinations> {
  identity(projectId);
  identity(timelineId);
  const basis = await provider.loadTimelineCommandBasis(timelineId);
  await assertRuntimeRecoveryHead(client, projectId, timelineId, basis);
  const document = basis.canonicalDocument;
  const parent = document.parent_revision.payload;
  const parentTracks = tracks(parent.tracks ?? asRecord(parent.config)?.tracks);
  const occurrences = document.parent_revision.payload.occurrences;
  if (!Array.isArray(occurrences)) throw new Error('Missing explicit occurrences');
  const bindings: RuntimeRecoveryDestination[] = [];
  for (const value of occurrences) {
    const occurrence = asRecord(value);
    if (!occurrence) throw new Error('Invalid occurrence');
    const occurrenceId = identity(occurrence.occurrence_id);
    const shotId = identity(occurrence.shot_id);
    const shotRevisionId = identity(occurrence.shot_revision_id);
    const shot = document.shot_revisions.find((row) => row.shot_id === shotId && row.revision_id === shotRevisionId);
    if (!shot) throw new Error('Missing occurrence shot binding');
    const internal = document.internal_timeline_revisions.filter((row) => row.revision_id === shot.internal_timeline_revision_id);
    if (internal.length !== 1) throw new Error('Ambiguous child timeline binding');
    const placement = asRecord(occurrence.placement);
    const parentTrackId = identity(placement?.track ?? occurrence.track);
    if (placement?.track !== undefined && occurrence.track !== undefined && placement.track !== occurrence.track) {
      throw new Error('Conflicting occurrence lane bindings');
    }
    if (!parentTracks.some((row) => row.id === parentTrackId)) throw new Error('Missing parent lane');
    for (const track of tracks(internal[0].payload.tracks)) {
      if (track.kind !== 'visual' || track.enabled === false || track.disabled === true || track.hidden === true) continue;
      const childTrackId = identity(track.id);
      const optionNumber = bindings.length + 1;
      bindings.push({
        // This key belongs only to the chooser. It never becomes a canonical identity.
        id: String(bindings.length),
        // ShotSelector uses name as cmdk's selection value. Keep the raw labels
        // readable, but make that local value unique without encoding authority
        // into the display name or parsing it back later.
        name: `${optionNumber} · ${typeof shot.payload.name === 'string' ? shot.payload.name : shotId} · ${occurrenceId} · ${typeof track.label === 'string' ? track.label : childTrackId}`,
        owner: { kind: 'occurrence', occurrenceId }, shotId, shotRevisionId,
        internalTimelineId: internal[0].timeline_id, internalRevisionId: internal[0].revision_id,
        parentTrackId, childTrackId,
      });
    }
  }
  return freezeRecoveryValue(structuredClone({ basis, bindings }));
}

export async function assertRuntimeRecoveryHead(
  client: Pick<AstridRuntimeClient, 'getProjectTimeline'>,
  projectId: string,
  timelineId: string,
  basis: TimelineCommandBasis,
) {
  const document = basis.canonicalDocument;
  const timeline = await client.getProjectTimeline(projectId, timelineId);
  if (document.project_id !== projectId || document.timeline_id !== timelineId
    || document.parent_revision.revision_id !== basis.head.revisionId
    || !basis.head.revisionId || !basis.head.publicationId
    || timeline.project_id !== projectId || timeline.timeline_id !== timelineId
    || timeline.head_revision_id !== basis.head.revisionId || timeline.head_publication_id !== basis.head.publicationId) {
    throw new Error('Selected timeline head changed or is outside the selected scope');
  }
}

export async function assertRuntimeRecoverySource(client: Pick<AstridRuntimeClient, 'getTask' | 'getManagedOutput' | 'getProjectMediaSelection'>, projectId: string, source: RuntimeRecoverySource) {
  const [task, output] = await Promise.all([
    client.getTask(source.task.task_id), client.getManagedOutput(source.output.association_id),
  ]);
  if (task.task_id !== source.task.task_id || task.version !== source.task.version
    || !runtimeTaskRecoveryPresentation(task, projectId) || !isRuntimeRecoveryOutput(task, output)
    || output.association_id !== source.output.association_id || output.object_id !== source.output.object_id
    || output.version !== source.output.version) throw new Error('Recovery output changed');
  const selected = await readRuntimeRecoverySelection(client, projectId, output);
  if ((Object.keys(source.mediaTuple) as (keyof MediaSelection)[]).some((key) => selected[key] !== source.mediaTuple[key])) {
    throw new Error('Recovery media selection changed');
  }
}
