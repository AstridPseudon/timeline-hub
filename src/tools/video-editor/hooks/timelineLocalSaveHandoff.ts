import type { CanonicalDocument } from '@/integrations/runtime/timeline-commit-types.ts';
import type { LocalSaveSession } from '../commands/localSaveSession.ts';
import { toOutboxJson, type OutboxJson } from '../commands/commitOutbox.ts';
import { canonicalJsonStringify, type TimelineBundleEnvelope } from '../data/typed/timelineBundle.ts';
import { TimelineVersionConflictError, type TimelineCommandBasis, type TimelineHeadRevision, type TimelineSaveReceipt } from '../data/DataProvider.ts';
import type { AssetRegistry, TimelineConfig } from '../types/index.ts';

export interface TimelineSaveSource {
  config: TimelineConfig;
  registry: AssetRegistry;
  bundle?: TimelineBundleEnvelope | null;
  head?: TimelineHeadRevision;
}

/** Assembly supplies the ORIGINAL verified read, not loadTimelineCommandBasis at save time. */
export interface TimelineLocalSaveHandoff {
  capture(source: TimelineSaveSource): Promise<void>;
  flush(): Promise<TimelineSaveReceipt>;
}

const same = (a: unknown, b: unknown) => canonicalJsonStringify(a) === canonicalJsonStringify(b);

// Upstream config builders include optional undefined fields. Object omission
// also preserves the editor's explicit transition-clear action as a removal.
function authoredJson(value: unknown): OutboxJson {
  if (Array.isArray(value)) return value.map(authoredJson);
  if (value && typeof value === 'object' && Object.getPrototypeOf(value) === Object.prototype) {
    return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined)
      .map(([key, item]) => [key, authoredJson(item)]));
  }
  return toOutboxJson(value);
}

/** Parent-only upstream save mapping. Child/occurrence ownership needs its own authored assembly join. */
export function createTimelineLocalSaveHandoff(options: {
  initial: TimelineCommandBasis;
  source: TimelineSaveSource;
  session: LocalSaveSession;
  /** Read the upstream assembly after the session has adopted the complete canonical result. */
  adopted(basis: TimelineCommandBasis): { receipt: TimelineSaveReceipt; source: TimelineSaveSource };
}): TimelineLocalSaveHandoff {
  let initial = structuredClone(options.initial);
  let source = structuredClone(options.source);
  function refuse(message: string): never {
    throw new TimelineVersionConflictError(`Local document save retained: ${message}`);
  }
  function checkHead(value: TimelineSaveSource) {
    if (value.head?.projectId !== initial.canonicalDocument.project_id
      || value.head.timelineId !== initial.canonicalDocument.timeline_id
      || value.head.headRevisionId !== initial.head.revisionId
      || value.head.headPublicationId !== initial.head.publicationId) refuse('original verified authoring head is unavailable');
  }
  function authoredConfig(value: TimelineSaveSource, document: CanonicalDocument) {
    const original = document.parent_revision.payload.config as Record<string, unknown> | undefined;
    const config: Record<string, unknown> = { ...structuredClone(original), ...structuredClone(value.config) };
    // Match saveTimelineAtHead's parent-only partial clip merge. The closure
    // gate below runs first; display IDs never identify authored children.
    const clips = Array.isArray(original?.clips) ? original.clips as Record<string, unknown>[] : [];
    const byId = new Map(clips.map((clip) => [clip.id, clip]));
    config.clips = value.config.clips.map((clip) => ({ ...byId.get(clip.id), ...structuredClone(clip) }));
    // Upstream adds a default output on read; it is not an authored parent field.
    if (original && !Object.prototype.hasOwnProperty.call(original, 'output')) delete config.output;
    if (value.bundle !== undefined) config.bundle = structuredClone(value.bundle);
    else if (original && Object.prototype.hasOwnProperty.call(original, 'bundle')) config.bundle = structuredClone(original.bundle);
    return authoredJson(config) as Record<string, OutboxJson>;
  }
  return {
    capture(input) {
      try {
        const next = structuredClone(input);
        checkHead(source);
        checkHead(next);
        const before = options.session.getDocument() as unknown as CanonicalDocument;
        const parent = before.parent_revision.payload;
        if (before.shot_revisions.length || before.internal_timeline_revisions.length
          || (Array.isArray(parent.occurrences) && parent.occurrences.length)) refuse('child ownership/fork mapping is unavailable');
        const originalConfig = authoredConfig(source, before);
        if (!same(parent.config, originalConfig) || !same(parent.registry, source.registry)) {
          refuse('upstream source differs from the verified authored parent');
        }
        const after = structuredClone(before);
        const payload = after.parent_revision.payload;
        payload.config = authoredConfig(next, before);
        payload.registry = authoredJson(next.registry) as Record<string, OutboxJson>;
        for (const key of ['clips', 'tracks'] as const) {
          if (!Object.prototype.hasOwnProperty.call(parent, key)) continue;
          if (!same(parent[key], originalConfig[key])) refuse(`contradictory parent ${key} mirror`);
          payload[key] = (payload.config as Record<string, OutboxJson>)[key];
        }
        // The encoder supplies guards and created IDs; these bytes are never a wire DTO.
        const pending = options.session.appendDocument({ before, after,
          roots: [{ ref: 'parent', revisionId: before.parent_revision.revision_id, contentDigest: before.parent_revision.content_digest }],
          label: 'Edit timeline', step: { id: crypto.randomUUID(), label: 'Edit timeline', intent: 'Save local editor changes', tags: [] } });
        source = next;
        return pending;
      } catch (error) {
        return Promise.reject(error instanceof TimelineVersionConflictError ? error
          : new TimelineVersionConflictError(`Local document save retained: ${error instanceof Error ? error.message : String(error)}`));
      }
    },
    async flush() {
      try {
        const basis = await options.session.flush();
        const adopted = options.adopted(basis);
        const head = adopted.receipt.head;
        if (head.projectId !== initial.canonicalDocument.project_id || head.timelineId !== initial.canonicalDocument.timeline_id
          || head.headRevisionId !== basis.head.revisionId || head.headPublicationId !== basis.head.publicationId
          || !same(adopted.source.head, head)) refuse('canonical assembly did not adopt the accepted head');
        initial = structuredClone(basis);
        source = structuredClone(adopted.source);
        return adopted.receipt;
      }
      catch (error) {
        if (['blocked', 'conflict', 'error', 'recovery'].includes(options.session.getState().status)) {
          refuse(error instanceof Error ? error.message : String(error));
        }
        throw error;
      }
    },
  };
}
