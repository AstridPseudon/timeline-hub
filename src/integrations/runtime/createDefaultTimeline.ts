import { ReighRuntimeClient } from './client.ts';
import { generateUUID } from '@/shared/lib/taskCreation/ids.ts';
import { createDefaultTimelineConfig } from '@/tools/video-editor/lib/defaults.ts';

type RuntimeTimeline = Record<string, unknown> & {
  timeline_id?: unknown;
  head_revision_id?: unknown;
  archived?: unknown;
  is_default?: unknown;
  slug?: unknown;
};

function timelineId(value: RuntimeTimeline | undefined): string | undefined {
  return typeof value?.timeline_id === 'string' && value.timeline_id.length > 0
    ? value.timeline_id
    : undefined;
}

function chooseTimeline(timelines: RuntimeTimeline[]): RuntimeTimeline | undefined {
  const active = timelines.filter((timeline) => timeline.archived !== true);
  const preferred = (candidates: RuntimeTimeline[]) => candidates.find((timeline) => timeline.is_default === true)
    ?? candidates.find((timeline) => timeline.slug === 'main')
    ?? candidates.find((timeline) => timeline.slug === 'rough-cut')
    ?? candidates[0];
  return preferred(active.filter((timeline) => (
    typeof timeline.head_revision_id === 'string' && timeline.head_revision_id.length > 0
  ))) ?? preferred(active);
}

async function stableUuid(seed: string): Promise<string> {
  const input = new TextEncoder().encode(seed);
  const digest = new Uint8Array(await globalThis.crypto.subtle.digest('SHA-256', input)).slice(0, 16);
  digest[6] = (digest[6] & 0x0f) | 0x50;
  digest[8] = (digest[8] & 0x3f) | 0x80;
  const hex = Array.from(digest, (byte) => byte.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

async function publishEmptyTimeline(
  projectId: string,
  targetTimelineId: string,
  name: string,
  client: ReighRuntimeClient,
  key: string,
): Promise<void> {
  const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'timeline';
  const parentRevisionId = await stableUuid(`reigh-parent-revision:${projectId}:${targetTimelineId}`);
  await client.publishParentComposition(
    projectId,
    targetTimelineId,
    {
      project_id: projectId,
      timeline_id: targetTimelineId,
      expected_head: null,
      parent_revision_id: parentRevisionId,
      parent_composition: {
        slug,
        name,
        config: createDefaultTimelineConfig() as unknown as Record<string, unknown>,
        registry: { assets: {} },
        clips: [],
        occurrences: [],
      },
      shot_revisions: [],
      internal_timeline_revisions: [],
    },
    key,
  );
}

/** Publish a new empty canonical parent composition through the current Runtime contract. */
export async function createCanonicalTimeline(
  projectId: string,
  options: { name?: string; timelineId?: string; idempotencyKey?: string } = {},
  client: ReighRuntimeClient = new ReighRuntimeClient(),
): Promise<string> {
  const targetTimelineId = options.timelineId
    ?? (options.idempotencyKey
      ? await stableUuid(`reigh-timeline:${options.idempotencyKey}`)
      : generateUUID());
  await publishEmptyTimeline(
    projectId,
    targetTimelineId,
    options.name ?? 'Timeline',
    client,
    options.idempotencyKey ?? `reigh-timeline-create-${projectId}-${targetTimelineId}`,
  );
  return targetTimelineId;
}

/** Ensure a project has a canonical Runtime composition, repairing an existing headless shell. */
export async function ensureProjectHasTimeline(
  projectId: string,
  client: ReighRuntimeClient = new ReighRuntimeClient(),
): Promise<string> {
  const timelines = await client.listTimelines(projectId) as RuntimeTimeline[];
  const existing = chooseTimeline(timelines);
  const existingId = timelineId(existing);
  if (existingId && typeof existing?.head_revision_id === 'string' && existing.head_revision_id.length > 0) {
    return existingId;
  }
  if (existingId) {
    await publishEmptyTimeline(projectId, existingId, 'Main', client, `reigh-first-timeline-${projectId}`);
    return existingId;
  }
  return createCanonicalTimeline(
    projectId,
    {
      name: 'Main',
      timelineId: await stableUuid(`reigh-first-timeline:${projectId}`),
      idempotencyKey: `reigh-first-timeline-${projectId}`,
    },
    client,
  );
}
